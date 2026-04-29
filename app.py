import streamlit as st
import json
from pdf_parser import parse_pdf
from agent import analyze_tender, evaluate_fit
from company_profile import get_profile
import tempfile
import os

st.set_page_config(page_title="Analyzátor zakázek", page_icon="📋", layout="wide")

st.title("📋 Analyzátor veřejných zakázek")
st.caption("Nahraj PDF zadávací dokumentace a agent vyhodnotí, zda má smysl se přihlásit.")

uploaded_file = st.file_uploader("Nahraj PDF zakázky", type="pdf")

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    with st.spinner("Čtu dokument..."):
        text = parse_pdf(tmp_path)
    os.unlink(tmp_path)

    if not text.strip():
        st.error("Nepodařilo se přečíst PDF.")
        st.stop()

    with st.spinner("Analyzuji zakázku pomocí AI..."):
        tender = analyze_tender(text)

    with st.spinner("Vyhodnocuji shodu s profilem firmy..."):
        profile = get_profile()
        fit = evaluate_fit(tender, profile)

    # Verdikt nahoře
    verdict_color = {
        "DOPORUČENO": "success",
        "PODMÍNEČNĚ": "warning",
        "NEDOPORUČENO": "error",
    }.get(fit["verdikt"], "info")

    if verdict_color == "success":
        st.success(f"✅ Verdikt: {fit['verdikt']}  |  Skóre: {fit['skore']}/100")
    elif verdict_color == "warning":
        st.warning(f"⚠️ Verdikt: {fit['verdikt']}  |  Skóre: {fit['skore']}/100")
    else:
        st.error(f"❌ Verdikt: {fit['verdikt']}  |  Skóre: {fit['skore']}/100")

    st.markdown(f"> {fit['zduvodneni']}")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📄 Detail zakázky")
        st.markdown(f"**Předmět:** {tender['predmet']}")
        st.markdown(f"**Zadavatel:** {tender['zadavatel']}")
        st.markdown(f"**Hodnota:** {tender['hodnota']}")
        st.markdown(f"**Termín podání:** {tender['termin_podani'] or 'neuvedeno'}")
        st.markdown(f"**Shrnutí:** {tender['shrnuti']}")

        if tender["kvalifikace"]:
            st.markdown("**Kvalifikační požadavky:**")
            for k in tender["kvalifikace"]:
                st.markdown(f"- {k}")

        if tender["rizika"]:
            st.markdown("**Rizika:**")
            for r in tender["rizika"]:
                st.markdown(f"- {r}")

    with col2:
        st.subheader("🏢 Vyhodnocení shody")

        if fit["shoda"]:
            st.markdown("**✅ Co sedí:**")
            for s in fit["shoda"]:
                st.markdown(f"- {s}")

        if fit["problemy"]:
            st.markdown("**❌ Problémy:**")
            for p in fit["problemy"]:
                st.markdown(f"- {p}")

        if fit["doporucene_kroky"]:
            st.markdown("**➡️ Doporučené kroky:**")
            for d in fit["doporucene_kroky"]:
                st.markdown(f"- {d}")

    st.divider()
    with st.expander("Raw JSON výstup"):
        st.json({"zakázka": tender, "vyhodnocení": fit})