import streamlit as st

st.set_page_config(page_title="Where Go Ah?", page_icon="🇸🇬")

pg = st.navigation(
    [
        st.Page("chat.py", title="Where Go Ah?", icon=":material/chat:", default=True),
        st.Page("pages/1_About_Us.py", title="About Us", icon=":material/info:"),
        st.Page("pages/2_Methodology.py", title="Methodology", icon=":material/explore:"),
        st.Page("pages/3_Upload_Documents.py", title="Upload Documents", icon=":material/upload_file:"),
    ]
)
pg.run()
