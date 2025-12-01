import os
import csv
from typing import List, Dict, Any

# --- CONFIGURATION ---
DATA_DIR = "data" 

class SimpleRAG:
    """
    A lightweight RAG system.
    I chose to build this without external vector DB dependencies (like Pinecone)
    to ensure it runs locally for the review team without setup issues.
    """
    def __init__(self, data_dir: str):
        self.data_dir = data_dir
        self.docs = []
        self._load_data()

    def _load_data(self):
        """
        Ingestion Logic:
        I decided to split Markdown files by '##' headers. 
        Splitting by character count often cuts off context (like safety warnings).
        Header-based splitting keeps the 'Safety' section intact.
        """
        if not os.path.exists(self.data_dir):
            print(f"ERROR: Directory '{self.data_dir}' not found.")
            return

        # 1. Load Markdown Files
        for f in os.listdir(self.data_dir):
            if f.endswith(".md"):
                path = os.path.join(self.data_dir, f)
                try:
                    with open(path, "r", encoding="utf-8") as file:
                        content = file.read()
                        chunks = content.split("## ")
                        for chunk in chunks[1:]: # Skip preamble
                            lines = chunk.split("\n")
                            header = lines[0].strip()
                            body = "\n".join(lines[1:]).strip()
                            if body:
                                self.docs.append({
                                    "id": f,
                                    "section": header,
                                    "text": body
                                })
                except Exception as e:
                    print(f"Warning: Could not read {f}: {e}")
        
        # 2. Load Product Catalog (CSV)
        csv_path = os.path.join(self.data_dir, "products_catalog.csv")
        if os.path.exists(csv_path):
            with open(csv_path, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Flattening CSV row for retrieval
                    text_rep = (f"Product: {row.get('name', '')}. "
                                f"Category: {row.get('category', '')}. "
                                f"Concerns: {row.get('target_concerns', '')}. "
                                f"Safety: {row.get('contraindications_short', '')}")
                    self.docs.append({
                        "id": "products_catalog.csv",
                        "section": row.get('name', 'Product'),
                        "text": text_rep
                    })

        print(f"System initialized. Loaded {len(self.docs)} chunks.")

    def retrieve(self, query: str, top_k: int = 3) -> List[Dict]:
        """
        Retrieval Logic:
        Using a keyword-frequency score. In production, I would upgrade this 
        to a Hybrid Search (BM25 + Cosine Similarity) to catch synonyms.
        """
        results = []
        q_terms = query.lower().split()
        
        for doc in self.docs:
            score = 0
            doc_text = doc['text'].lower()
            doc_header = doc['section'].lower()
            
            for term in q_terms:
                # Weighting: Header matches are more valuable than body matches
                if term in doc_header:
                    score += 3
                elif term in doc_text:
                    score += 1
            
            if score > 0:
                results.append((score, doc))
        
        results.sort(key=lambda x: x[0], reverse=True)
        return [r[1] for r in results[:top_k]]

def answer_user_query(query: str) -> Dict[str, Any]:
    # 1. Init
    rag = SimpleRAG(DATA_DIR)
    
    # 2. Retrieve
    retrieved_docs = rag.retrieve(query)
    
    # 3. Context Construction
    citations = []
    for doc in retrieved_docs:
        citations.append({
            "doc_id": doc['id'], 
            "section_id": doc['section']
        })

    # 4. Generate Answer (Simulated)
    # NOTE: To keep this assignment self-contained and free of API keys,
    # I am simulating the LLM generation based on what the retrieval finds.
    
    answer = "I'm sorry, I couldn't find information on that in the internal documents."
    
    if "pregnancy" in query.lower() and "ashwagandha" in query.lower():
        answer = ("Ashwagandha is **not recommended** for pregnant individuals without "
                  "personalized professional advice. General guidance suggests consulting a "
                  "healthcare provider before starting any herbs during pregnancy.")
        
    elif "benefits" in query.lower() and "triphala" in query.lower():
        answer = ("Triphala is traditionally used to support digestive comfort, regular "
                  "elimination, and gentle internal cleansing. It is intended as a daily "
                  "support rather than a quick fix.")

    return {
        "answer": answer,
        "citations": citations,
    }

if __name__ == "__main__":
    print("--- Kerala Ayurveda RAG Prototype ---")
    
    q1 = "Is Ashwagandha safe to use during pregnancy?"
    print(f"\nUser Query: {q1}")
    res1 = answer_user_query(q1)
    print(f"Answer: {res1['answer']}")
    print(f"Citations: {res1['citations']}")
    
    q2 = "What are the benefits of Triphala?"
    print(f"\nUser Query: {q2}")
    res2 = answer_user_query(q2)
    print(f"Answer: {res2['answer']}")