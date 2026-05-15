from pypdf import PdfReader


def read_pdf(path):

    reader = PdfReader(path)

    text = ""

    for page in reader.pages:
        text += page.extract_text()

    return text

def chunk_text(
    text,
    source,
    chunk_size=500
):

    chunks = []

    chunk_id = 0

    for i in range(0, len(text), chunk_size):

        chunk = text[i:i + chunk_size]

        chunks.append({
            "text": chunk,
            "source": source,
            "chunk_id": chunk_id
        })

        chunk_id += 1

    return chunks