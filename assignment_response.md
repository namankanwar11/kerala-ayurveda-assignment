# Kerala Ayurveda Assignment Submission

## Part A: Small RAG Design
* **Chunking:** Used Markdown header splitting (`##`) to preserve semantic context of sections. CSV rows treated as individual documents.
* **Retrieval:** Implemented a keyword-frequency retrieval system. In production, this would be upgraded to Hybrid Search (Vector Embeddings + BM25).
* **Citations:** System returns `doc_id` and `section_id` with every answer.

## Part B: Agentic Workflow
1.  **Workflow:**
    * **Researcher:** Retrieves raw chunks from vector store.
    * **Drafter:** Generates text using `content_style_and_tone_guide.md`.
    * **Safety Check:** Filters for banned terms (e.g., "cure", "miracle").
2.  **Evaluation:**
    * **Golden Set:** 10 curated Q&A pairs.
    * **Metric:** Hallucination rate (facts in output vs facts in source).
3.  **Prioritization:**
    * **Week 1-2:** Ship the internal RAG Search tool for content writers.
    * **Postpone:** Automated publishing to public web (requires human review).

## Reflection
* **Time:** 3 hours.
* **Tools:** Python for logic, VS Code for dev.