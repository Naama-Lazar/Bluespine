Bluespine Medical Policy AI Agent 🩺🤖
An automated RAG-based (Retrieval-Augmented Generation) pipeline designed to analyze medical insurance policies.
The agent extracts structured billing rules, clinical exclusions, and frequency limits from PDF documents, translates them into executable SQL logic, and validates the results against the original source text.

🌟 Key Features
PDF Extraction & Cleaning: Intelligent parsing of medical policies, filtering out "noise" (disclaimers, headers) to focus on reimbursement logic.

RAG Engine: Uses FAISS and HuggingFace Embeddings (all-MiniLM-L6-v2) to index and retrieve semantically relevant policy sections.

AI Analysis: Leverages Llama-3.3-70b (via Groq) to generate structured JSON reports, including rule atomicity and SQL queries.

Validation Guardrails: * Zero-Hallucination: Cross-references extracted CPT/HCPCS codes against the source PDF.

Verbatim Quotes: Validates that extracted quotes exist word-for-word in the policy.

HTML Reporting: Generates a clean, readable visual report for the final output.

📂 Project Structure
Bluespine/
├── main.py                # Main entry point - Orchestrates the flow
├── api_key.txt            # Your Groq API key (Keep this private!)
├── requirements.txt       # Project dependencies
├── core/
│   ├── __init__.py
│   ├── agent.py           # LLM logic & pipeline orchestration
│   ├── rag_engine.py      # RAG logic (Vector DB, Splitting, Retrieval)
│   └── prompts.py         # Advanced system prompts & SQL schema
├── utils/
│   ├── __init__.py
│   ├── pdf_utils.py       # PDF parsing & text cleaning
│   └── formatters.py      # HTML generation & Validation logic
├── input_files/           # Place source PDF policies here
└── output_files/          # Resulting HTML reports are saved here

🚀 How to Run
Place a medical policy PDF in the input_files/ folder.

Update the filename in main.py if necessary:

Python
run_agent("input_files/your-policy-file.pdf")
Run the application:

Bash
python main.py
View the results in the output_files/ directory as an .html file.

🛠️ Technology Stack
Language: Python 3.9+

LLM: Llama-3.3-70b-versatile (Groq Cloud)

Orchestration: LangChain

Vector Store: FAISS

Embeddings: HuggingFace (sentence-transformers)

PDF Processing: PyPDF2 & Regex

🧪 Validation Logic
To ensure clinical accuracy, the agent performs two main checks:

Code Validation: Ensures any 5-digit code (CPT/HCPCS) mentioned in the SQL or description actually exists in the PDF text.

Quote Validation: Uses text normalization to verify that the "quote" field provided by the AI is a verbatim snippet from the policy.

