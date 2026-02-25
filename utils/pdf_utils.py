import PyPDF2
import re

def extract_text_from_pdf(file_path):
    """
    Extracts all text content from a PDF file.
    Args:
        file_path (str): The path to the PDF file.
    Returns:
        str: The complete extracted text from the PDF.
    """
    text = ""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text


def generate_html(data):
    """
    Generates an HTML report from policy data.
    Args:
        data (dict): Dictionary containing 'policy_name' and a 'rules' list.
    Returns:
            str: Formatted HTML document string.
    """
    if not data: return "<h1>No Data Found</h1>"
    html = f"<html><body>"
    html += f"<h1>Policy Name: {data.get('policy_name')}</h1>"
    html += "<hr><h3>Rules List:</h3>"
    for rule in data.get('rules', []):
        html += f"""
        <div>
            <h2>Rule Name: {rule.get('rule_name')}</h2>
            <p><b>Description:</b> {rule.get('description')}</p>
            <p><b>SQL-based implementation:</b></p>
            <pre style="background:#eee; padding:10px;">{rule.get('sql')}</pre>
            <p><b>SQL Validation:</b> {rule.get('sql_valid')}</p>
            <p><b>Invalid Codes Found:</b> {rule.get('invalid_codes')}</p>
            <p><b>Logic Confidence:</b> {rule.get('logic_confidence')}</p>
            <p><b>Classification (Rule Type):</b> {rule.get('classification')}</p>
            <p><b>Quote:</b> <i>"{rule.get('quote')}"</i></p>
            <p><b>Quote Validation:</b> {rule.get('quote_valid')}</p>
        </div>
        <hr>
        """

    html += "</body></html>"
    return html

def clean_policy_text(raw_text):
    """
        Optimizes policy text for LLM analysis by removing noise and extracting core content.
        Args:
            raw_text (str): Raw string extracted from the PDF.
        Returns:
            str: Cleaned text focused on reimbursement logic and policy codes.
    """
    text = re.sub(r'\s+', ' ', raw_text)
    content_match = re.search(
        r"(PURPOSE:.*?Policy Applicable Codes:.*?)(?=(RELATED HIGHMARK POLICIES|$))",
        text,
        re.IGNORECASE
    )
    # Falls back to the first 6,000 characters if 'PURPOSE' or 'Codes' headers are not found,
    # ensuring key context for the LLM.
    if content_match:
        interesting_text = content_match.group(1)
    else:
        interesting_text = text[:6000]

    noise_phrases = [
        r"Highmark Reimbursement Policy Bulletin",
        r"Application is based on how the provider is contracted",
        r"This Policy supersedes direction provided in Bulletins prior",
        r"A checked box indicates the policy is applicable"
    ]
    for phrase in noise_phrases:
        interesting_text = re.sub(phrase, "", interesting_text, flags=re.IGNORECASE)

    return interesting_text.strip()