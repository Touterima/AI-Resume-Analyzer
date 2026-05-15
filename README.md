# 📄 AI Resume Analyzer

**Optimisez vos CV pour les ATS et augmentez vos chances d'être retenu**

Un outil intelligent qui analyse votre CV, lui attribue un **score ATS sur 100**, détecte ses faiblesses et vous donne des suggestions concrètes d’amélioration grâce à l’IA.

---

## ✨ Fonctionnalités

- **Upload facile** : Supporte les fichiers **PDF, DOCX et TXT**
- **Scoring ATS détaillé** sur 100 points (longueur, mots-clés, structure, lisibilité)
- **Deux modes d’IA** :
  - Mode **OpenAI** (gpt-4o-mini) → Suggestions très personnalisées
  - Mode **Démo** automatique (activé si pas de clé API)
- **Analyse selon le poste** : Collez la description de l’offre pour des conseils ciblés
- **Texte extrait visible** pour vérification
- **Export du rapport complet** en fichier texte
- Interface moderne et intuitive avec **Streamlit**

---

## 🖥️ Aperçu

![Interface](https://via.placeholder.com/800x450?text=AI+Resume+Analyzer+Screenshot)  
*(Ajoute une capture d’écran ici plus tard)*

---

## 🚀 Installation

### 1. Cloner le repository

  ```bash
  git clone https://github.com/Touterima/AI-Resume-Analyzer.git
  cd ai-resume-analyzer
```

### 2. Installer les dépendances
 ```bash
 pip install -r requirements.txt
 ```

### 3. Configuration 
 Créez un fichier .env à la racine du projet :
 ```bash
 OPENAI_API_KEY=sk-proj-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
 ```
 Si vous ne mettez pas de clé, l’application fonctionne automatiquement en Mode Démo.

 ### 📋 Contenu du fichier requirements.txt 

  streamlit
  pymupdf
  python-docx
  openai
  python-dotenv

### ▶️ Lancement
 ```bash
 streamlit run app.py
 ```
### 📊 Comment ça marche ?

Déposez votre CV (PDF ou Word)
(Optionnel) Collez la description du poste
L’application analyse automatiquement :
Score ATS global
Forces et faiblesses
Suggestions d’amélioration

Téléchargez le rapport complet


### 🛠 Technologies utilisées

Frontend : Streamlit
Extraction de texte : PyMuPDF (fitz) + python-docx
IA : OpenAI (gpt-4o-mini) avec fallback Mode Démo
Gestion des variables : python-dotenv


### 🎯 Améliorations futures (Roadmap)

 Génération d’une version améliorée du CV par IA
 Support de plusieurs langues (Anglais/Français automatique)
 Export PDF direct du CV optimisé
 Historique des analyses
 Détection automatique du métier cible
 Version multilingue complète


### 🤝 Contribution
Les contributions sont les bienvenues ! N’hésitez pas à :

Ouvrir une Issue
Faire une Pull Request
Proposer de nouvelles fonctionnalités
