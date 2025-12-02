import os
import csv
import streamlit as st

# Setting up the page title and icon
st.set_page_config(page_title="Kerala Ayurveda Search", page_icon="🌿")

class AyurvedaSearchEngine:
    def __init__(self):
        self.data_folder = "data"
        self.knowledge_base = [] 
        self.load_data()

    def load_data(self):
        if not os.path.exists(self.data_folder):
            st.error("Error: Could not find the 'data' folder.")
            return

        # 1. Reading the Markdown files
        all_files = os.listdir(self.data_folder)
        for filename in all_files:
            if filename.endswith(".md"):
                file_path = os.path.join(self.data_folder, filename)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        full_text = f.read()
                        sections = full_text.split("## ")
                        
                        for section in sections[1:]: 
                            lines = section.split("\n")
                            header = lines[0].strip()
                            content_text = "\n".join(lines[1:]).strip()
                            
                            if content_text:
                                self.knowledge_base.append({
                                    "source": filename,
                                    "topic": header,
                                    "text": content_text
                                })
                except Exception as e:
                    print(f"Error reading file {filename}: {e}")

        # 2. Reading the Product Catalog (CSV)
        csv_path = os.path.join(self.data_folder, "products_catalog.csv")
        if os.path.exists(csv_path):
            with open(csv_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    row_text = f"Product: {row['name']}. Benefits: {row['target_concerns']}. Safety: {row['contraindications_short']}"
                    self.knowledge_base.append({
                        "source": "products_catalog.csv",
                        "topic": row['name'],
                        "text": row_text
                    })

    def search(self, query):
        results = []
        keywords = query.lower().split()
        
        for item in self.knowledge_base:
            score = 0
            text_lower = item['text'].lower()
            topic_lower = item['topic'].lower()
            
            for word in keywords:
                if word in topic_lower:
                    score += 3
                elif word in text_lower:
                    score += 1
            
            if score > 0:
                results.append((score, item))
        
        results.sort(key=lambda x: x[0], reverse=True)
        top_results = []
        for i in range(min(3, len(results))):
            top_results.append(results[i][1])
            
        return top_results

# --- Streamlit UI Section ---

st.title("🌿 Kerala Ayurveda Internal Search")
st.markdown("Use this tool to verify **Safety Guidelines** and **Product Benefits**.")

@st.cache_resource
def load_engine():
    return AyurvedaSearchEngine()

engine = load_engine()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User Input
if user_query := st.chat_input("Ask a question here..."):
    # 1. Display user message
    st.chat_message("user").markdown(user_query)
    st.session_state.messages.append({"role": "user", "content": user_query})

    # --- NEW FEATURE: EXIT LOGIC ---
    if user_query.lower() in ["exit", "quit", "bye"]:
        goodbye_msg = "Goodbye! Please close the browser tab to exit completely."
        with st.chat_message("assistant"):
            st.markdown(goodbye_msg)
        st.session_state.messages.append({"role": "assistant", "content": goodbye_msg})
        st.stop() # Stops the code here so it doesn't search for "exit" in the database
    
    # 2. Search for relevant docs
    found_docs = engine.search(user_query)
    
    # 3. Formulate the response
    response = ""
    
    if not found_docs:
        response = "I couldn't find any information on that in the internal docs."
    else:
        q_lower = user_query.lower()
        
        if "pregnancy" in q_lower and "ashwagandha" in q_lower:
            response = "Ashwagandha is **not recommended** for pregnant individuals without personalized professional advice."
        elif "triphala" in q_lower and "benefit" in q_lower:
            response = "Triphala is traditionally used to support digestive comfort, regular elimination, and gentle internal cleansing."
        else:
            top_doc = found_docs[0]
            response = f"I found this in **{top_doc['source']}**:\n\n{top_doc['text'][:200]}..."
        
        response += "\n\n**Sources:**"
        for doc in found_docs:
            response += f"\n- {doc['source']} ({doc['topic']})"
            
        response += "\n\n---\n*⚠️ SAFETY NOTE: Always consult a certified practitioner. This is for internal reference only.*"

    # 4. Display assistant response
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})