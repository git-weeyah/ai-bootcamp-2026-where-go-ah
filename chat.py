import json

import streamlit as st
import streamlit.components.v1 as components

from core import ingest, rag, ui, vectorstore
from core.auth import require_login

require_login()

if "indexed" not in st.session_state:
    with st.spinner("Preparing knowledge base..."):
        ingest.ensure_index()
    st.session_state["indexed"] = True

with st.sidebar:
    if st.button("Rebuild index"):
        with st.spinner("Rebuilding..."):
            n = ingest.rebuild_index()
        st.success(f"Re-indexed {n} chunks.")
    agencies = sorted({m["agency"] for m in vectorstore.get_collection().get()["metadatas"] if m.get("agency")})
    agency_filter = st.selectbox("Filter by agency", ["All"] + agencies)

ui.hero("Where Go Ah?", "Tell me your problem and I'll find the right government agency, so you can skip the 45-minute queue at the wrong counter.", "🇸🇬")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

EXAMPLES = [
    "🏠 Eh, I'm a foreigner working here leh. Can I rent a whole HDB flat on the open market or not?",
    "🪪 Aiyo, I lost my NRIC! How to report and get a replacement ah?",
    "💰 How much income tax do Singapore tax residents need to pay ah?",
    "👶 Got second child already, what can I get from the Baby Bonus scheme?",
    "🚗 I'm a foreigner with overseas licence. Can I drive in Singapore, or must I convert to Singapore licence? When ah?",
]
intro = st.empty()
if not st.session_state["messages"]:
    with intro.container():
        st.markdown("**Staring at the box and nothing comes to mind? Borrow one of these:**")
        for i, example in enumerate(EXAMPLES):
            if st.button(example, key=f"intro_{i}", use_container_width=True):
                st.session_state["prefill"] = example

if prefill := st.session_state.pop("prefill", None):
    components.html(
        f"""<script>
        const box = window.parent.document.querySelector('textarea[data-testid="stChatInputTextArea"]');
        if (box) {{
            Object.getOwnPropertyDescriptor(window.parent.HTMLTextAreaElement.prototype, 'value').set.call(box, {json.dumps(prefill)});
            box.dispatchEvent(new Event('input', {{bubbles: true}}));
            box.focus();
        }}
        </script>""",
        height=0,
    )


def md(text):
    return text.replace("\\$", "$").replace("$", "\\$")


def render_meta(agency, confidence, last_verified):
    if not agency:
        return
    st.badge(agency, icon=":material/account_balance:", color="blue")
    parts = []
    if confidence is not None:
        parts.append(f"Confidence: {confidence:.0%}")
    if last_verified:
        parts.append(f"Last verified: {last_verified}")
    if parts:
        st.caption(" · ".join(parts))


for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"], avatar="🙋" if msg["role"] == "user" else "🇸🇬"):
        render_meta(msg.get("agency"), msg.get("confidence"), msg.get("last_verified"))
        st.markdown(md(msg["content"]))

if q := st.chat_input("e.g. I want to rent a house lah. How ah?"):
    intro.empty()
    st.session_state["messages"].append({"role": "user", "content": q})
    with st.chat_message("user", avatar="🙋"):
        st.markdown(q)
    with st.chat_message("assistant", avatar="🇸🇬"):
        with st.spinner("Checking official sources..."):
            res = rag.answer(q, None if agency_filter == "All" else agency_filter)
        render_meta(res.get("agency"), res.get("confidence"), res.get("last_verified"))
        st.markdown(md(res["answer"]))
    st.session_state["messages"].append(
        {"role": "assistant", "content": res["answer"], "agency": res.get("agency"), "confidence": res.get("confidence"), "last_verified": res.get("last_verified")}
    )

if st.session_state["messages"]:
    asked = {m["content"] for m in st.session_state["messages"] if m["role"] == "user"}
    suggestions = [e for e in EXAMPLES if e not in asked]
    if suggestions:
        st.markdown("**Bureaucracy never ends, huh?** Pick your next adventure:")
        for example in suggestions:
            if st.button(example, key=f"more_{EXAMPLES.index(example)}", use_container_width=True):
                st.session_state["prefill"] = example
                st.rerun()
    if st.button("New chat", icon=":material/add_comment:", type="primary"):
        st.session_state["messages"] = []
        st.session_state.pop("prefill", None)
        st.rerun()
