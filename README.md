# Prometheus AI — RAG Chat Platform

A futuristic Retrieval Augmented Generation (RAG) workspace with a polished web experience, built using FastAPI, Ollama, and FAISS. Ask questions, upload documents, and shape responses with session memory, system prompt overrides, and mode selection.

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green)
![Ollama](https://img.shields.io/badge/Ollama-local-lightgrey)

## 🎯 Features

- **📚 RAG-powered knowledge**: Retrieve answers from your uploaded documents using FAISS vector search
- **🧠 Session memory**: Keep context across the chat and clear memory when needed
- **⚙️ Mode selection**: Choose Chat, Summarize, Explain, Code Review, or Answer modes
- **📝 Custom system prompt**: Override assistant behavior for more control
- **🚀 Streaming replies**: See the model answer as it generates in real time
- **📤 Document upload**: Add PDFs or plain text files on the fly
- **🔐 Local inference**: Run Ollama locally with no external API key required
- **🎨 Futuristic UI**: Modern Prometheus-branded interface with responsive layout

## 📋 Prerequisites

- **Python 3.9+**
- **Ollama** installed and available on your PATH
- **Git** (optional, for cloning the repo)
- **8GB+ RAM** (16GB+ recommended for model performance)

## 🚀 Quick Start

1. Clone the repo and enter the folder:

```bash
git clone https://github.com/SiddharthMaverick/llm-platform.git
cd llm-platform
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

3. Install Python dependencies:

```bash
pip install -r requirements.txt
```

4. Start the Ollama server in a separate terminal:

```bash
ollama serve
```

5. Pull the model used by the app:

```bash
ollama pull phi3
```

6. Run the FastAPI app:

```bash
uvicorn app.main:app --reload
```

7. Open the app in your browser:

```bash
http://localhost:8000
```

## 💡 Usage

- Enter a prompt in the chat box
- Select your preferred mode
- Toggle document context on or off
- Add a custom system prompt to refine responses
- Upload documents to expand the knowledge base
- Reset the session or clear session memory anytime

## 📘 API Docs

Visit:

```bash
http://localhost:8000/docs
```

## 🗂 Project Structure

```
llm-platform/
├── app/
│   ├── main.py                      # FastAPI application entry point
│   ├── routes/
│   │   └── chat.py                  # Chat endpoints
│   ├── services/
│   │   ├── ollama_service.py        # Ollama client configuration
│   │   └── rag_service.py           # RAG pipeline logic
│   ├── rag/
│   │   ├── startup.py               # Initialize RAG on app start
│   │   ├── embedder.py              # Text embedding (384-dim vectors)
│   │   ├── ingest.py                # PDF reading and text chunking
│   │   ├── retriever.py             # Query embedding and search
│   │   ├── vector_store.py          # FAISS index and document storage
│   │   └── build_index.py           # Index building utilities
│   ├── schemas/
│   │   └── chat.py                  # Request/Response data models
│   ├── core/
│   │   ├── config.py                # Configuration management
│   │   └── logging.py               # Logging setup
│   └── documents/
│       └── *.pdf                    # Research papers (12 documents)
├── static/
│   └── index.html                   # Frontend (single-page app)
├── requirements.txt                 # Python dependencies
├── .env                             # Environment configuration
├── .gitignore                       # Git ignore rules
├── README.md                        # This file
└── FRONTEND_SETUP.md               # Frontend-specific docs
```

## 🏗 Architecture

```
User Query
    ↓
Frontend (index.html)
    ↓
FastAPI Backend (/chat endpoint)
    ↓
RAG Pipeline:
  1. Embed Query → 384-dim vector
  2. Search FAISS Index → Top 3 chunks
  3. Get Document Context
    ↓
LLM Generation:
  1. Send Context + Query to Ollama
  2. Stream Response Token by Token
    ↓
Frontend Display (Real-time streaming)
```

## 📚 How RAG Works

### Indexing Phase (Startup)

1. **Read PDFs** → Extract text from `app/documents/*.pdf`
2. **Chunk Text** → Split into 500-character overlapping chunks
3. **Embed Chunks** → Convert to 384-dimensional vectors using SentenceTransformer
4. **Store Index** → Add vectors to FAISS index + store original text

### Query Phase (Runtime)

1. **Embed Query** → Convert user question to 384-dimensional vector
2. **Search Index** → Find 3 most similar chunks using L2 distance
3. **Create Context** → Combine retrieved chunks with metadata
4. **Generate Response** → Send context + query to Ollama
5. **Stream Output** → Send tokens in real-time to frontend

### Vector Similarity

```
Query: "What is attention?"
    ↓
Embedding: [0.2, -0.5, 0.8, ..., 0.1]  (384 values)
    ↓
Search: Compare against all chunk embeddings
    ↓
Results:
  1. "Attention mechanism allows..." (distance: 0.32)
  2. "Self-attention computes..." (distance: 0.45)
  3. "Multi-head attention enables..." (distance: 0.58)
```

## 🔧 Configuration

### Environment Variables (.env)

```env
OLLAMA_HOST=http://localhost:11434    # Ollama server address
MODEL_NAME=phi3                        # Model to use (phi3, mistral, etc.)
```

### RAG Parameters

Edit values in `app/rag/startup.py`:

```python
chunk_size=500          # Characters per chunk
k=3                     # Number of retrieved chunks
```

Edit values in `app/rag/retriever.py`:

```python
k=3                     # Results per query
```

### Server Configuration

Change FastAPI port:
```bash
uvicorn app.main:app --reload --port 8001
```

## 🐛 Troubleshooting

### Issue: "No connection could be made - target machine actively refused it"

**Cause**: Ollama server not running

**Solution**:
```bash
# Terminal 1
ollama serve

# Terminal 2
ollama pull phi3
```

### Issue: "Model not found" or "pull: manifest unknown"

**Cause**: Model not downloaded

**Solution**:
```bash
ollama pull phi3
ollama list          # Verify installation
```

### Issue: "Port 8000 already in use"

**Cause**: Another application using port 8000

**Solution**:
```bash
uvicorn app.main:app --reload --port 8001
```

### Issue: App slow or OOM (Out of Memory)

**Cause**: Insufficient RAM

**Solution**:
- Use smaller model: `ollama pull mistral` (smaller than phi3)
- Reduce chunk count: Edit `retriever.py` `k=1` instead of `k=3`
- Increase system RAM or use cloud deployment

### Issue: PDF files not indexing

**Cause**: PDFs in wrong format or corrupted

**Solution**:
```bash
# Check error logs
# Try re-downloading PDFs
# Verify PDF readability
```

### Issue: CORS errors in browser console

**Cause**: Frontend can't access backend

**Solution**:
- Ensure backend is running on http://localhost:8000
- Check firewall settings
- Clear browser cache (Ctrl+Shift+Delete)

## 📦 Dependencies

Key packages:
- **FastAPI** - Web framework
- **Uvicorn** - ASGI server
- **FAISS** - Vector similarity search
- **SentenceTransformers** - Text embeddings
- **PyPDF** - PDF reading
- **Ollama** - LLM inference client
- **NumPy** - Numerical operations

See `requirements.txt` for complete list.

## 🎓 Learning Resources

- [RAG Fundamentals](https://python.langchain.com/docs/modules/data_connection/)
- [FAISS Documentation](https://github.com/facebookresearch/faiss)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/)
- [Ollama Models](https://ollama.ai/library)
- [Transformers & Attention](https://arxiv.org/abs/1706.03762)

## 🚀 Deployment

### Local Network Access

Allow other machines to access your app:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Then access from: `http://<your-machine-ip>:8000`

### Docker (Optional)

```bash
docker build -t llm-rag .
docker run -p 8000:8000 llm-rag
```

### Cloud Deployment

- **Azure**: Use Azure Container Instances or App Service
- **AWS**: Deploy to EC2 or Lambda
- **Google Cloud**: Cloud Run or Compute Engine
- **Hugging Face Spaces**: Gradio version

## 📝 Adding More Documents

1. Add PDF files to `app/documents/` folder
2. Restart the application
3. System automatically indexes all PDFs

Supported formats: PDF

## 🔐 Security

- **No API Keys**: Uses local Ollama (no external calls)
- **No Data Collection**: Everything runs locally
- **No Authentication**: For local/trusted networks only
- **For Production**: Add authentication, HTTPS, rate limiting

## 📈 Performance

- **Indexing**: ~2-3 seconds for all documents
- **Query Response**: ~2-5 seconds per question
- **Memory Usage**: ~500MB-2GB (depends on chunk count)
- **Model Download**: ~2.5GB (Phi3)

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- [ ] Document upload UI
- [ ] Multiple models support
- [ ] Conversation history
- [ ] User authentication
- [ ] Query analytics
- [ ] Different embedding models

## 📄 License

MIT License - see LICENSE file

## ⚠️ Important Notes

- **First Run**: App takes 2-3 minutes to index all documents on startup
- **Memory**: Requires 8GB+ RAM. More documents = more RAM needed
- **Offline**: Works completely offline after initial setup
- **Model Size**: Phi3 is 2.5GB. Choose lighter models if needed

## 🆘 Need Help?

1. Check [Troubleshooting](#-troubleshooting) section
2. Review error messages in terminal
3. Check Ollama logs: `ollama serve` terminal
4. Open an issue on GitHub

## 🎯 Roadmap

- [ ] Web UI for document upload
- [ ] Query history and sessions
- [ ] Multiple model support with UI selector
- [ ] Export conversations to PDF
- [ ] Rate limiting and usage analytics
- [ ] Docker Compose setup
- [ ] Kubernetes deployment guide
- [ ] Mobile app (React Native)

## 💡 Tips for Best Results

1. **Ask specific questions** - More specific queries = better answers
2. **Use examples** - "Explain like I'm 5" works better
3. **Citation tracking** - Check which documents provided context
4. **Combine with docs** - Use for understanding, not replacement
5. **Experiment with models** - Try `mistral` for faster responses

## 📧 Contact

For questions or suggestions, please open an issue on GitHub.

---

**Happy querying!** 🚀 If you find this useful, please give it a ⭐

Last Updated: May 18, 2026
