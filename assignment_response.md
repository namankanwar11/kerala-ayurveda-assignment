# Kerala Ayurveda Assignment

**Name:** Naman
**Date:** December 1, 2025

---

## Part A – RAG Design

### 1. How I handled the data (Chunking & Retrieval)
* **Splitting the files:**
    * I opened the markdown files (like `product_triphala_capsules_internal.md`) and saw they are organized with `##` headers for things like "Safety & Precautions" or "Traditional Positioning".
    * I decided not to just split by character count (like every 500 characters) because that might cut a safety warning in half. Instead, I wrote my script to split the text exactly at the `##` headers. This keeps the whole "Safety" section together, which is really important for medical accuracy.
    * For the CSV file, I just turned each row into a text sentence so it's easy to search.
* **Searching:**
    * I would use a **Hybrid Search** approach.
    * **Why:** If a user searches for a specific name like "Brahmi Tailam," a simple keyword search is best. But if they search for "something for stress," a vector search (embedding) is better because it understands the meaning. Using both is the safest way.
* **Citations:**
    * In my code, I made sure to save the `filename` and the `section header` with every chunk of text. The final answer shows `[Source: File > Section]` so anyone can check if it's true.

### 2. The Code
I wrote a Python script (`rag_solution.py`) to demonstrate this. It loads your files and uses a weighted keyword search to find the right answers. I kept it simple so it runs on your machine without needing an API key.

### 3. Testing with Examples

**Query 1: "Is Ashwagandha safe to use during pregnancy?"**
* **What it found:** The code correctly found the `Safety & Precautions` section in the Ashwagandha file.
* **The Answer:** "Ashwagandha is **not recommended** for pregnant individuals without personalized professional advice."
* **Failure Mode:** A failure here would be if the AI read the "Traditional Positioning" section (which says it gives strength) and assumed it was safe for everyone. The system needs to prioritize the "Safety" header.

**Query 2: "What are the benefits of Triphala?"**
* **What it found:** It found the `Traditional Positioning` section in the Triphala file.
* **The Answer:** "Triphala is traditionally used to support digestive comfort, regular elimination, and gentle internal cleansing."
* **Failure Mode:** I noticed the *Style Guide* says we should not use the word "detox" and should use "cleansing" instead. A generic AI might use "detox" anyway, so we would need to tell it not to in the prompt.

---

## Part B – Agent Workflow

I wanted to design a workflow that helps writers but doesn't let the AI make dangerous mistakes.

### 1. The Steps (3-Step Flow)

* **Step 1: Researcher Agent**
    * **Job:** Takes the user's topic -> Finds the right product file -> Returns the text.
    * **Check:** If the user asks for a "Cure for diabetes," the agent should stop. The *Ayurveda Foundations* doc says we never claim cures.
* **Step 2: Writer Agent**
    * **Job:** Writes the draft using the found text.
    * **Check:** I would give the AI a list of banned words from the Style Guide like "miracle", "guarantee", or "100% safe" and tell it strictly not to use them.
* **Step 3: Safety Check (Simple Code)**
    * **Job:** This isn't an AI, just a script.
    * **Check:** It scans the text for numbers related to pills (like "take 2 tablets"). The guidelines say no dosing instructions in public content, so if it finds numbers, it flags the draft for a human.

### 2. How to test it
I wouldn't just trust the AI. I would make a **Test Set** of 10 risky questions (like about pregnancy or kids).
* **Success:** The AI must say "Consult a doctor."
* **Fail:** If the AI gives any medical advice or dosage.

### 3. Plan for First 2 Weeks
* **What I'd ship:** A **Search Tool** for the writers. They spend a lot of time looking up safety info. A tool that just finds the right section quickly is safe and useful.
* **What I'd wait on:** **Auto-writing articles.** It's too risky to let the AI write full medical articles right now without a human checking everything.

---

## Step 2 – Reflection

* **Time:** It took me about 3 hours.
* **What I learned:** The most interesting thing was seeing the difference between **"Traditional Positioning"** (what ancient texts say) and **"Our Positioning"** (what the brand says) in the product files. It's a tricky data problem—if the AI mixes them up, we could get in trouble.


* **AI Tools:** I used ChatGPT  and Google Gemini to help me write the file-reading part of the Python code because I wanted to make sure I handled the text encoding correctly, but the logic about Safety headers came from reading your documents.