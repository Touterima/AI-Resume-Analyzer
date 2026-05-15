import streamlit as st
import fitz  # PyMuPDF
import docx
import re
from datetime import datetime
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# ====================== INITIALISATION SESSION STATE ======================
if "openai_client" not in st.session_state:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    if OPENAI_API_KEY:
        try:
            st.session_state.openai_client = OpenAI(api_key=OPENAI_API_KEY)
            st.session_state.ai_mode = "openai"
            st.session_state.ai_status = "✅ OpenAI Activé"
        except Exception as e:
            st.session_state.openai_client = None
            st.session_state.ai_mode = "demo"
            st.session_state.ai_status = "🔄 Mode Démo"
    else:
        st.session_state.openai_client = None
        st.session_state.ai_mode = "demo"
        st.session_state.ai_status = "🔄 Mode Démo"

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="wide")
st.title("📄 AI Resume Analyzer")
st.markdown("**Scoring ATS + Suggestions intelligentes**")

# Affichage du mode actuel
#st.info(st.session_state.ai_status)

# ==================== FONCTIONS ====================
def extract_text_from_pdf(pdf_file):
    text = ""
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_docx(docx_file):
    doc = docx.Document(docx_file)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text(file):
    try:
        if file.type == "application/pdf":
            return extract_text_from_pdf(file)
        elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            return extract_text_from_docx(file)
        else:
            return file.getvalue().decode("utf-8")
    except:
        return "Erreur lors de l'extraction du texte."

# ==================== ANALYSE ATS ====================
ATS_KEYWORDS = {
    "technical": ["python", "java", "javascript", "sql", "aws", "docker", "kubernetes", "react", "node", "django", "flask", "azure"],
    "soft": ["leadership", "communication", "teamwork", "agile", "scrum", "problem solving"],
    "experience": ["managed", "led", "developed", "optimized", "increased", "développé", "géré", "optimisé"]
}

def calculate_ats_score(text, job_description=""):
    text_lower = text.lower()
    score = 0
    details = {}
    
    words = len(text.split())
    if 400 <= words <= 800:
        score += 25
        details["Longueur"] = "✅ Bonne (400-800 mots)"
    else:
        details["Longueur"] = f"⚠️ {words} mots (idéal : 400-800)"
    
    found_tech = sum(1 for kw in ATS_KEYWORDS["technical"] if kw in text_lower)
    tech_score = min(30, found_tech * 3)
    score += tech_score
    details["Mots-clés"] = f"{found_tech} mots-clés techniques détectés"
    
    sections = ["experience", "education", "skills", "projects", "summary", "expérience", "formation", "compétences"]
    found_sections = sum(1 for s in sections if s in text_lower)
    score += found_sections * 6
    details["Structure"] = f"{found_sections}/6 sections détectées"
    
    final_score = min(100, round(score))
    return final_score, details

# ==================== MODE DÉMO ====================
def get_demo_suggestions(score):
    return f"""
**🔄 Mode Démo Activé**

**Score ATS : {score}/100**

### Points forts :
- CV analysé avec succès

### Axes d’amélioration prioritaires :
- **Quantifier** au maximum vos réalisations (ex : +40%, -30%, 2M TND, 150 clients…)
- Commencer chaque ligne par un **verbe d’action** (Développé, Optimisé, Dirigé, Augmenté, Implémenté, Collaboré…)
- Ajouter une section **Compétences Techniques** visible en haut
- Adapter le CV à chaque offre d’emploi

### Recommandations :
1. CV idéalement sur **1 page**
2. Utiliser des puces simples (`-` ou `•`)
3. Éviter tableaux, colonnes et images
4. Mettre les dates au format `MM/AAAA`

"""

# ==================== SUGGESTIONS ====================
def get_ai_suggestions(text, score, job_desc=""):
    if st.session_state.ai_mode == "demo" or not st.session_state.openai_client:
        return get_demo_suggestions(score)

    prompt = f"""Tu es un expert en recrutement senior et en optimisation de CV pour les ATS.

CV du candidat :
{text[:6500]}

Score ATS actuel : {score}/100

Description du poste :
{job_desc if job_desc else "Aucune description fournie."}

Analyse ce CV et réponds en français de façon professionnelle et encourageante avec :
1. Points forts du CV
2. Points faibles / axes d'amélioration majeurs
3. Suggestions concrètes et prioritaires (contenu + format)
4. Mots-clés recommandés à ajouter selon le poste"""

    try:
        response = st.session_state.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=900
        )
        return response.choices[0].message.content
    except Exception as e:
        return get_demo_suggestions(score)

# ==================== INTERFACE ====================
uploaded_file = st.file_uploader("Déposez votre CV (PDF, DOCX ou TXT)", type=["pdf", "docx", "txt"])

job_description = st.text_area("Collez la description du poste (optionnel mais recommandé)", height=150)

if uploaded_file:
    with st.spinner("Analyse du CV en cours..."):
        text = extract_text(uploaded_file)
        
        score, details = calculate_ats_score(text, job_description)
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.metric("**Score ATS**", f"{score}/100",
                     delta="Excellent" if score >= 85 else "Bon" if score >= 70 else "À améliorer")
        
        with col2:
            for k, v in details.items():
                st.write(f"**{k}** : {v}")
        
        st.subheader("📋 Texte extrait")
        st.text_area("", text[:2000] + "..." if len(text) > 2000 else text, height=250)
        
        st.subheader("💡 Suggestions d'amélioration")
        suggestions = get_ai_suggestions(text, score, job_description)
        st.markdown(suggestions)
        
        if st.button("📥 Télécharger le rapport complet"):
            report = f"""RAPPORT AI RESUME ANALYZER
Date : {datetime.now().strftime("%d/%m/%Y %H:%M")}
Mode : {st.session_state.ai_mode.upper()}
Score ATS : {score}/100

Détails : {details}

Suggestions :
{suggestions}
"""
            st.download_button(
                label="Télécharger le rapport",
                data=report,
                file_name=f"rapport_cv_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                mime="text/plain"
            )

st.sidebar.caption("Made with ❤️ pour optimiser tes candidatures")