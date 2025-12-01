# Assignment Response: Kerala Ayurveda RAG & Agents

**Submitted by:** Naman
**Date:** December 1, 2025

---

## Part A – Small RAG Design

### 1. RAG Approach & Decisions
* **Chunking Strategy:**
    * I examined the Markdown files (like `product_triphala_capsules_internal.md`) and saw they are structured with clear headers like `## Safety & Precautions`.
    * Instead of arbitrary character splitting, I used a **Header-based semantic splitter**. This ensures that if we retrieve the "Safety" section, we get the *entire* warning context, not just half a sentence.
* **Retrieval Method:**
    * I recommend starting with **Hybrid Search** (Keyword + Embeddings).
    * **Why:** Pure vector search often fails on specific Sanskrit product names (like "Brahmi Tailam"). Pure keyword search misses concepts (like searching for "stress" and expecting "Ashwagandha").
* **Citations:**
    * I designed the return object to include `doc_id` and `section_id`. This allows the UI to render `[Source: Ashwagandha Dossier > Safety]` next to the text, which is critical for medical trust.

### 2. Function Design
*Please see `rag_solution.py` for the executable code.*

I implemented a `SimpleRAG` class that parses the provided headers. I chose to simulate the API call to ensure the code runs on your machine without needing my personal OpenAI key.

### 3. Example Queries & Failure Analysis

**Query 1: "Is Ashwagandha safe to use during pregnancy?"**
* **Retrieved Docs:** `product_ashwagandha_tablets_internal.md` (Section: Safety & Precautions).
* **System Answer:** "Ashwagandha is **not recommended** for pregnant individuals without personalized professional advice."
* **Potential Failure Mode:** The model might see the "Traditional Positioning" section (which talks about strength/stamina) and assume it's safe. The system prompt needs to prioritize the *Safety* header over *Traditional* headers.

**Query 2: "What are the benefits of Triphala?"**
* **Retrieved Docs:** `product_triphala_capsules_internal.md` and `products_catalog.csv`.
* **System Answer:** "Triphala is traditionally used to support digestive comfort, regular elimination, and gentle internal cleansing."
* **Potential Failure Mode:** The model might use the word "Detox." I noticed in `product_triphala_capsules_internal.md` that the brand specifically avoids "detox" in favor of "cleansing". A standard LLM won't know this brand preference without negative constraint prompting.

---

## Part B – Agentic Workflow

### 1. Workflow Design (Drafting Assistant)
I designed this workflow to assist writers, not replace them, given the safety risks.

* **Step 1: The Researcher (Retrieval)**
    * **Role:** Takes the brief -> Finds specific product dossiers -> Returns raw text.
    * **Guardrail:** If the brief asks for a medical cure (e.g., "Cure for diabetes"), the agent flags it immediately based on `ayurveda_foundations.md` rules about not claiming cures.
* **Step 2: The Drafter (LLM + Style Guide)**
    * **Role:** Writes the content using the retrieved text.
    * **Guardrail:** **Negative Constraint Prompting.** I would inject instructions to forbid specific words found in the Style Guide: `["miracle", "cure", "guarantee", "100%"]`.
* **Step 3: The Safety Checker (Deterministic)**
    * **Role:** A simple Regex script, not an LLM.
    * **Check:** It scans for dosage numbers (e.g., "2 tablets"). The `ayurveda_foundations.md` doc explicitly bans specific dosing in public content, so this should trigger an automatic rejection.

### 2. Evaluation Loop
To trust this system, we need to measure Safety over Creativity.

* **Golden Set:** I'd write 10 "tricky" questions (e.g., pregnancy, chronic illness) and define the *only* acceptable answer (usually: "Consult a doctor").
* **Metric:** **Safety Compliance Rate.** How often does the model mistakenly give medical advice? This must be 0%.

### 3. Prioritisation (First 2 Weeks)
* **Ship:** A **"Smart Search" UI**. Writers currently spend time hunting for the "Safety" clause. A tool that simply retrieves the right section (RAG only, no generation) is safe and immediately high-value.
* **Postpone:** **Auto-Publishing.** The risk of the AI making a claim that violates the `product_ashwagandha_tablets_internal.md` safety section is too high to automate right now. We need humans in the loop.

---

## Step 2 – Reflection

* **Time Spent:** ~3 hours.
* **Most Interesting Observation:** I found the distinction between **"Traditional Positioning"** and **"Our Positioning"** in the product files fascinating. It's a subtle data problem—if the RAG retrieves the "Traditional" text, the LLM might claim the product "cures leprosy" (ancient text), which would be a legal liability. The system *must* prioritize "Our Positioning."
* **AI Tool Use:** I used ChatGPT to help write the boilerplate Python code for reading files, but the logic regarding the "Safety headers" and the specific "Failure Modes" came from my reading of your provided documents.