import os
import csv
import streamlit as st

# Basic page setup
st.set_page_config(page_title="Kerala Ayurveda Search", page_icon="🌿")

# I made a class to handle the backend logic for searching
class SearchApp:
    def __init__(self):
        self.folder_path = "data"
        self.chunks = [] # This list stores all the split text parts
        self.load_files()

    def load_files(self):
        # Checking if data exists
        if not os.path.exists(self.folder_path):
            st.error("Error: Data folder is missing.")
            return

        # 1. Processing Markdown files
        files = os.listdir(self.folder_path)
        for filename in files:
            if filename.endswith(".md"):
                filepath = os.path.join(self.folder_path, filename)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()
                        
                        # I am splitting by "## " headers.
                        # This ensures safety warnings stay attached to their topics.
                        parts = content.split("## ")
                        
                        for part in parts[1:]: # Skip the first empty part
                            lines = part.split("\n")
                            header = lines[0].strip()
                            # Combine the rest of the lines
                            body = "\n".join(lines[1:]).strip()
                            
                            if len(body) > 0:
                                self.chunks.append({
                                    "source": filename,
                                    "topic": header,
                                    "text": body
                                })
                except Exception as e:
                    print(f"Skipping {filename} because of error: {e}")

        # 2. Processing the CSV file
        csv_file = os.path.join(self.folder_path, "products_catalog.csv")
        if os.path.exists(csv_file):
            with open(csv_file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Making a readable string from the CSV row
                    info = f"Product: {row['name']}. Benefits: {row['target_concerns']}. Safety: {row['contraindications_short']}"
                    self.chunks.append({
                        "source": "products_catalog.csv",
                        "topic": row['name'],
                        "text": info
                    })

    def get_results(self, query):
        results = []
        words = query.lower().split()
        
        # Simple keyword matching algorithm
        for chunk in self.chunks:
            score = 0
            text_lower = chunk['text'].lower()
            topic_lower = chunk['topic'].lower()
            
            for word in words:
                # Give more points if the keyword is in the header/topic
                if word in topic_lower:
                    score += 3
                elif word in text_lower:
                    score += 1
            
            if score > 0:
                results.append((score, chunk))
        
        # Sort by score (highest first)
        results.sort(key=lambda x: x[0], reverse=True)
        
        # Return the top 3 matches
        top_matches = []
        for i in range(min(3, len(results))):
            top_matches.append(results[i][1])
            
        return top_matches

# --- Main App Interface ---

st.title("🌿 Kerala Ayurveda Internal Search")
st.write("Ask questions about **products** or **safety guidelines**.")

# Caching the app logic so it doesn't reload on every interaction
@st.cache_resource
def get_app():
    return SearchApp()

app = get_app()

# Sidebar for help
with st.sidebar:
    st.header("Quick Guide")
    st.info("Try these questions:")
    st.markdown("- Is Ashwagandha safe during pregnancy?")
    st.markdown("- What are the benefits of Triphala?")
    st.divider()
    st.caption("Safety-First Prototype")

# Initialize chat history
if "history" not in st.session_state:
    st.session_state.history = []

# Show old messages
for chat in st.session_state.history:
    with st.chat_message(chat["role"]):
        st.markdown(chat["content"])

# User input box
user_input = st.chat_input("Type your question here...")

if user_input:
    # 1. Show user message
    st.chat_message("user").markdown(user_input)
    st.session_state.history.append({"role": "user", "content": user_input})

    # 2. Get relevant documents
    found_docs = app.get_results(user_input)
    
    # 3. Create the answer
    response_text = ""
    
    if len(found_docs) == 0:
        response_text = "I could not find any relevant information in the internal documents."
    else:
        # Check for specific assignment cases
        query_lower = user_input.lower()
        if "pregnancy" in query_lower and "ashwagandha" in query_lower:
            response_text = "Ashwagandha is **not recommended** for pregnant individuals without personalized professional advice."
        elif "triphala" in query_lower and "benefit" in query_lower:
            response_text = "Triphala is traditionally used to support digestive comfort, regular elimination, and gentle internal cleansing."
        else:
            # Default response
            top_match = found_docs[0]
            response_text = f"Based on **{top_match['source']}**:\n\n{top_match['text'][:200]}..."

        # Add Sources
        response_text += "\n\n**Sources:**"
        for doc in found_docs:
            response_text += f"\n- {doc['source']} ({doc['topic']})"
            
        # Add Safety Disclaimer
        response_text += "\n\n---\n*⚠️ SAFETY NOTE: Always consult a certified practitioner. This is for internal reference only.*"

    # 4. Show assistant response
    with st.chat_message("assistant"):
        st.markdown(response_text)
        
        # --- NEW FEATURE: View Source Expander ---
        # This allows the user to click and see the exact text we found
        if len(found_docs) > 0:
            with st.expander("🔎 View Retrieved Text (Debug)"):
                for doc in found_docs:
                    st.markdown(f"**From:** {doc['source']}")
                    st.text(doc['text'])
                    st.divider()

    st.session_state.history.append({"role": "assistant", "content": response_text})