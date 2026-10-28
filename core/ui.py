from pathlib import Path

import streamlit as st

_ASSETS = Path(__file__).resolve().parent.parent / "assets"

_CSS = """
<style>
.block-container { padding-top: 2rem; max-width: 900px; }
h1, h2, h3 { letter-spacing: -0.01em; }
[data-testid="stSidebar"] { border-right: 1px solid #e6cbb8; }
.wga-hero {
  background: linear-gradient(135deg, #B3262A 0%, #D9582F 60%, #E8A100 100%);
  color: #fff; border-radius: 20px; padding: 1.6rem 1.8rem; margin-bottom: 1.2rem;
  box-shadow: 0 8px 24px rgba(179,38,42,.28); position: relative; overflow: hidden;
}
.wga-hero h1 { color: #fff; margin: 0; padding: 0; font-size: 2.1rem; }
.wga-hero p { margin: .3rem 0 0; font-size: 1.05rem; opacity: .95; }
.wga-hero { display: flex; align-items: center; gap: 1.2rem; }
.wga-hero .wga-text { flex: 1 1 auto; min-width: 0; }
.wga-hero .wga-emoji { flex: 0 0 auto; font-size: 4.2rem; line-height: 1; opacity: .35; }
@media (max-width: 640px) {
  .wga-hero .wga-emoji { display: none; }
}
.wga-card {
  background: #fff; border: 1px solid #e6cbb8; border-radius: 16px; padding: 1rem 1.2rem;
  box-shadow: 0 2px 10px rgba(0,0,0,.04); height: 100%;
}
.wga-chip {
  display: inline-block; background: #fff; border: 1px solid #e0a894; color: #B3262A;
  border-radius: 999px; padding: .25rem .8rem; margin: .15rem .2rem; font-size: .9rem;
}
[data-testid="stChatMessage"] {
  background: #fff; border: 1px solid #e6cbb8; border-radius: 16px; padding: .8rem 1rem;
  box-shadow: 0 2px 8px rgba(0,0,0,.03);
}
[data-testid="stMetric"] {
  background: #fff; border: 1px solid #e6cbb8; border-radius: 16px; padding: .8rem 1rem;
}
.stButton > button, .stDownloadButton > button, [data-testid="stFormSubmitButton"] > button {
  border-radius: 999px; font-weight: 600;
}
[data-testid="stExpander"] { background: #fff; border-radius: 12px; }
</style>
"""


def setup() -> None:
    st.logo(str(_ASSETS / "logo.svg"), icon_image=str(_ASSETS / "logo_icon.svg"), size="large")
    st.markdown(_CSS, unsafe_allow_html=True)


def hero(title: str, subtitle: str = "", emoji: str = "🇸🇬") -> None:
    st.markdown(
        f'<div class="wga-hero"><div class="wga-text"><h1>{title}</h1><p>{subtitle}</p></div>'
        f'<span class="wga-emoji">{emoji}</span></div>',
        unsafe_allow_html=True,
    )


def card(html: str) -> None:
    st.markdown(f'<div class="wga-card">{html}</div>', unsafe_allow_html=True)


def chips(items: list[str]) -> str:
    return "".join(f'<span class="wga-chip">{i}</span>' for i in items)
