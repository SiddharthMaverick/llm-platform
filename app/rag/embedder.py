import os
from sentence_transformers import SentenceTransformer

# Set cache directory for offline operation
os.environ['SENTENCE_TRANSFORMERS_HOME'] = os.path.join(os.path.expanduser("~"), '.cache', 'sentence-transformers')

# Load model and cache it locally for offline use
model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)


def embed_text(texts):
    """
    Embed text using local SentenceTransformer model.
    Model is cached locally after first download for offline operation.
    """
    return model.encode(texts)