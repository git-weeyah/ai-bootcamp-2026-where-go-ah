from pathlib import Path

import streamlit as st

from core import ui
from core.auth import require_login

st.set_page_config(page_title="About Us", page_icon="ℹ️")
require_login()

ui.hero("About Us", "Because nobody grows up knowing the difference between MOM, ICA, CPF and HDB.", "ℹ️")
st.image(str(Path(__file__).resolve().parent.parent / "assets" / "about_hero.svg"), use_container_width=True)

st.markdown(
    """
**Where Go Ah?** helps you find the right government agency and service when you only know your
*problem*, not the jargon. Ask in plain English or Singlish, e.g. *"My IC gone sia, where replace?"*
"""
)

st.subheader("The problem 🤯")
c1, c2, c3 = st.columns(3)
c1.metric("Agencies", "Many", help="Too many acronyms, honestly.")
c2.metric("Websites visited before finding the right one", "5+ 😵", help="Statistically unscientific, emotionally accurate.")
c3.metric("Times you said \"aiyo\"", "∞")
st.markdown(
    "Government services are organised by agency, but people think in life events: *lost my IC*, *need a flat "
    "to rent*, *just had a baby*. Finding the right agency first means knowing the jargon first."
)

st.subheader("Project scope 🎯")
in_scope, out_scope = st.columns(2)
with in_scope:
    st.success(
        "**In scope**\n\n"
        "- Routing a described situation to the right **agency** and **service**\n"
        "- A short, grounded explanation of why that agency fits\n"
        "- A link to the official page for the next step\n"
        "- Plain English and Singlish questions\n"
        "- Five pilot areas: housing, identity, tax, family support and driving\n"
        "- Adding your own documents to the searchable index"
    )
with out_scope:
    st.error(
        "**Out of scope**\n\n"
        "- Submitting applications or handling personal data on your behalf\n"
        "- Personalised eligibility decisions, legal or financial advice\n"
        "- Live data such as queue times, application status or account details\n"
        "- Agencies and services not yet in the knowledge base\n"
        "- Production-grade authentication (the login is a demo gate)"
    )

st.subheader("Objectives 🧭")
st.markdown(
    """
1. **Reduce the search burden.** Get from a plain-language problem to the correct agency in one question.
2. **Stay trustworthy.** Answer only from curated official content, always cite the source URL, and say
   *"I don't know"* instead of guessing.
3. **Be transparent.** Show the agency, a confidence score and the date each source was last verified.
4. **Resist misuse.** Keep the model inside its rules even when questions or documents try to override them.
5. **Stay maintainable.** Let anyone extend coverage by dropping in a Markdown file or uploading a document.
"""
)

st.subheader("How we help 🛠️")
st.markdown(
    """
1. 🗣️ **You describe the problem.** Singlish welcome, no need to know the agency name.
2. 🔍 **We search official sources.** Only curated government pages, no random forum auntie advice.
3. 📍 **We point you to the right place.** Agency, service, and the official link. Done lah.

See the **Methodology** page for the full data flow and a flowchart for each use case.
"""
)

st.subheader("Data sources 📚")
st.markdown(
    "The knowledge base is a set of Markdown summaries written from official Singapore Government websites. "
    "Each file records its agency, category, topic, source URL and the date it was last verified."
)
st.table(
    [
        {"Agency": "Housing & Development Board (HDB)", "Category": "Housing", "Files": 7, "Covers": "Public rental and open-market rental: eligibility, application, rents and deposits, flat types"},
        {"Agency": "Immigration & Checkpoints Authority (ICA)", "Category": "Identity", "Files": 3, "Covers": "Lost IC, IC replacement and updating particulars, passports"},
        {"Agency": "Inland Revenue Authority of Singapore (IRAS)", "Category": "Tax", "Files": 3, "Covers": "Individual income tax, tax rates, GST"},
        {"Agency": "Ministry of Social and Family Development (MSF)", "Category": "Family", "Files": 2, "Covers": "Baby Bonus, family and caregiver support"},
        {"Agency": "Singapore Police Force / Traffic Police", "Category": "Driving", "Files": 3, "Covers": "Singapore driving licence, qualified driving licence, application, replacement and renewal"},
    ]
)
st.caption(
    "Sources: hdb.gov.sg, ica.gov.sg, iras.gov.sg, msf.gov.sg, police.gov.sg. "
    "Documents you upload are also searchable, but are not vetted by us."
)

st.subheader("Features ✨")
f1, f2 = st.columns(2)
with f1:
    st.info("💬 **Natural-language chat**\n\nAsk in English or Singlish and get agency, service, reason and link.")
    st.info("🛡️ **\"I don't know\" guardrail**\n\nNothing relevant in the sources means no guessing, just a pointer to gov.sg.")
    st.info("🏷️ **Agency filter**\n\nNarrow the search to one agency from the chat sidebar.")
with f2:
    st.info("📊 **Confidence and freshness**\n\nEach answer shows a similarity-based confidence and the last-verified date.")
    st.info("📄 **Upload documents**\n\nAdd PDF, Markdown or text files; they are searchable in chat at once. Duplicates are skipped.")
    st.info("🔁 **Rebuild index**\n\nReset the index to the bundled knowledge base in one click.")

st.subheader("Who it's for 👥")
a, b = st.columns(2)
with a:
    st.info("🏠 **New renters & homeowners**\n\nHDB, grants, and the paperwork maze.")
    st.info("🪪 **Lost-IC-and-panicking people**\n\nBreathe. We'll tell you where to go.")
with b:
    st.info("👶 **New parents & families**\n\nBirth registration, schemes, benefits.")
    st.info("🌏 **Anyone unsure which agency applies**\n\nSingapore residents, this one's for you.")

st.subheader("Built with 🧱")
st.markdown(
    "Streamlit · OpenAI `text-embedding-3-small` and `gpt-4o-mini` · Chroma vector store · "
    "LangChain text splitters · pypdf. Retrieval-augmented generation (RAG) keeps answers tied to the sources above."
)

st.subheader("FAQ 🙋")
with st.expander("Are you the government?"):
    st.write("Nope! We just read their homepages so you don't have to. 📚")
with st.expander("Can I trust every answer?"):
    st.write("We cite official sources and say \"I don't know\" rather than guess. Still, always double-check.")
with st.expander("Why does it say it doesn't know?"):
    st.write(
        "Either your topic is not in the knowledge base yet, or no source was close enough to your question. "
        "Try rephrasing, clear the agency filter, or upload the relevant document."
    )
with st.expander("How up to date is the information?"):
    st.write("Every answer shows the date its source was last verified. Fees and rules change, so check the official page.")
with st.expander("Why Singlish?"):
    st.write("Because \"Please advise on the procedure for replacement of identity card\" is not how anyone talks. 😄")

st.warning(
    "**Disclaimer:** This is **not an official government site**. It is a starting layer that points you to "
    "official sources. Information may be outdated, so always verify on the official website before acting.",
    icon="⚠️",
)
