# Kerala Ayurveda - Internal RAG Assignment

**Submitted by:** Naman
**Context:** Content Engineering / AI Engineer Role

## Overview
This project is a prototype of a **Retrieval-Augmented Generation (RAG)** system designed for Kerala Ayurveda's internal use. It helps content writers find verified safety information and product benefits using a secure search engine.

I have converted the initial Python script into a **Streamlit Web App** so it can be easily tested by non-technical stakeholders (like the CBO) via a web browser.

## Features
* **Web Chat Interface:** A user-friendly chat UI built with Streamlit.
* **Safety-First Search:** Prioritizes "Safety & Precautions" headers to prevent medical hallucinations.
* **Automatic Compliance:** Appends a mandatory safety disclaimer to every response to ensure medical guidelines are followed.
* **Hybrid-Style Retrieval:** Uses a weighted keyword algorithm to find both specific products and general concepts.

## Project Structure
```text
kerala-ayurveda-assignment/
├── data/                    # The provided content pack (Markdown & CSV)
├── rag_solution.py          # The Streamlit Web App logic
├── requirements.txt         # List of dependencies (streamlit)
├── assignment_response.md   # My written report on Agent Design & Safety
└── README.md                # This file