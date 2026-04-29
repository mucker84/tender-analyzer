from openai import OpenAI
from dotenv import load_dotenv
from company_profile import get_profile
import json

load_dotenv()
client = OpenAI()

def analyze_tender(text: str) -> dict:
    prompt = f"""
Jsi expert na analýzu zadávací dokumentace veřejných zakázek.
Z následujícího textu extrahuj klíčové informace a vrať je jako JSON.

Text zakázky:
{text[:8000]}

Vrať POUZE JSON v tomto formátu, nic jiného:
{{
    "predmet": "co se poptává",
    "hodnota": "odhadovaná hodnota zakázky nebo null",
    "termin_podani": "termín podání nabídky nebo null",
    "zadavatel": "název zadavatele",
    "kvalifikace": ["požadavek 1", "požadavek 2"],
    "hodnotici_kriteria": ["kritérium 1", "kritérium 2"],
    "rizika": ["riziko 1", "riziko 2"],
    "shrnuti": "2-3 věty o zakázce"
}}
"""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    raw = response.choices[0].message.content.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]

    return json.loads(raw.strip())


def evaluate_fit(tender: dict, profile: dict) -> dict:
    prompt = f"""
Jsi zkušený poradce pro veřejné zakázky.
Porovnej zakázku s profilem firmy a vyhodnoť, zda má firma smysl se přihlásit.

ZAKÁZKA:
{json.dumps(tender, ensure_ascii=False, indent=2)}

PROFIL FIRMY:
{json.dumps(profile, ensure_ascii=False, indent=2)}

Vrať POUZE JSON v tomto formátu, nic jiného:
{{
    "verdikt": "DOPORUČENO" nebo "NEDOPORUČENO" nebo "PODMÍNEČNĚ",
    "skore": číslo 0-100,
    "shoda": ["co sedí 1", "co sedí 2"],
    "problemy": ["co chybí nebo nevyhovuje 1", "co chybí nebo nevyhovuje 2"],
    "doporucene_kroky": ["krok 1", "krok 2"],
    "zduvodneni": "2-3 věty celkového hodnocení"
}}
"""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    raw = response.choices[0].message.content.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]

    return json.loads(raw.strip())


if __name__ == "__main__":
    from pdf_parser import parse_pdf
    import sys

    if len(sys.argv) < 2:
        print("Použití: python agent.py soubor.pdf")
        sys.exit(1)

    print("\n--- Čtu dokument ---")
    text = parse_pdf(sys.argv[1])

    print("\n--- Analyzuji zakázku ---")
    tender = analyze_tender(text)
    print(json.dumps(tender, ensure_ascii=False, indent=2))

    print("\n--- Vyhodnocuji shodu s profilem firmy ---")
    profile = get_profile()
    fit = evaluate_fit(tender, profile)
    print(json.dumps(fit, ensure_ascii=False, indent=2))