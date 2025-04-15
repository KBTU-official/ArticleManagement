import requests
import fitz  # PyMuPDF for PDF extraction
import re
import spacy
import pycountry

# Load NLP Model
nlp = spacy.load("en_core_web_sm")


def find_country(text):
    """Detect country using NLP and PyCountry."""
    country_candidates = []
    doc = nlp(text)

    for ent in doc.ents:
        if ent.label_ in ["GPE", "LOC"]:
            for country in pycountry.countries:
                if ent.text.lower() in country.name.lower():
                    country_candidates.append(country.name)

    return country_candidates[0] if country_candidates else "Unknown"


def extract_journal_name(text):
    """Extract journal name using regex and NLP."""
    match = re.search(r"(?i)published in (.*?)[.,]", text)
    if match:
        return match.group(1).strip()

    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "ORG":
            return ent.text

    return "Unknown"


def extract_authors(text):
    """Extract author names using NLP."""
    doc = nlp(text)
    authors = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]

    if not authors:
        author_match = re.search(r"(?i)by\s+([\w\s,]+)", text)
        if author_match:
            authors = [name.strip() for name in author_match.group(1).split(",")]

    return ", ".join(authors[:5]) if authors else "Unknown"


def extract_title(text, doc):
    """Extract the title from PDF metadata or the first few lines."""
    title = doc.metadata.get("title", "").strip()
    if title:
        return title

    lines = text.split("\n")
    for line in lines:
        if len(line.split()) > 3:
            return line.strip()

    return "Unknown Title"


def extract_abstract(text):
    """Extract an abstract using NLP sentence segmentation."""
    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]
    
    return " ".join(sentences[:5]) if sentences else "Unknown"


def extract_year(text):
    """Extract the publication year using regex."""
    match = re.search(r"\b(19|20)\d{2}\b", text)
    
    return match.group() if match else "Unknown"


def search_article_online(title):
    """Search for an article URL using CrossRef and Semantic Scholar APIs."""
    crossref_url = f"https://api.crossref.org/works?query.title={title}&rows=1"
    response = requests.get(crossref_url)

    if response.status_code == 200:
        data = response.json()
        if "message" in data and "items" in data["message"] and data["message"]["items"]:
            doi = data["message"]["items"][0].get("DOI")
            if doi:
                return f"https://doi.org/{doi}"

    semantic_url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={title}&fields=url"
    response = requests.get(semantic_url)

    if response.status_code == 200:
        data = response.json()
        if "data" in data and data["data"]:
            return data["data"][0].get("url", "No link found")

    return f"https://www.google.com/search?q={title.replace(' ', '+')}+site:researchgate.net+OR+site:springer.com+OR+site:ncbi.nlm.nih.gov"


def extract_article_info(pdf_path):
    """Extract metadata from a given PDF and search for its link online."""
    doc = fitz.open(pdf_path)
    full_text = " ".join([page.get_text("text") for page in doc])

    title = extract_title(full_text, doc)

    return {
        "title": title,
        "abstract": extract_abstract(full_text),
        "year": extract_year(full_text),
        "country": find_country(full_text),
        "journal_name": extract_journal_name(full_text),
        "authors": extract_authors(full_text),
        "article_link": search_article_online(title),  # Get the actual URL
    }
