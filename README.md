# AI-powered-PDF-Question-Answering-Chatbot
AI PDF Chatbot  An AI-powered PDF Question Answering Chatbot that allows users to upload PDF documents and interact with their content through a conversational interface. .
The system uses Retrieval-Augmented Generation (RAG) to understand the uploaded documents, retrieve relevant information, and generate context-aware answers using a Large Language Model.

The application is designed to make information extraction from large PDF documents faster and easier. Instead of manually searching through lengthy documents, users can simply ask questions in natural language and receive relevant answers based on the PDF content.

# Key Features
📄 Upload and process PDF documents
🤖 AI-powered conversational PDF assistant
🔎 Semantic search across PDF content
🧠 Retrieval-Augmented Generation (RAG)
✂️ Document text extraction and chunking
🔢 Text embeddings for semantic retrieval
🗄️ Vector database for storing document embeddings
💬 Natural-language question answering
📚 Context-aware responses based on retrieved PDF content
⚡ FastAPI backend for processing and AI services
💻 Interactive frontend for document upload and chat
🔐 Secure API key configuration using environment variables
How It Works

The PDF Bot follows a RAG-based pipeline:

PDF Upload → Text Extraction → Text Chunking → Embeddings → Vector Database → User Query → Similarity Search → Relevant Context → LLM → Final Answer

When a PDF is uploaded, its text is extracted and divided into smaller chunks. Each chunk is converted into a vector embedding and stored in the vector database.

When the user asks a question, the query is converted into an embedding and compared against the stored document embeddings. The most relevant chunks are retrieved and provided as context to the LLM, which generates the final answer.

# Technology Stack

Frontend: React

Backend: Python, FastAPI, Uvicorn

AI / RAG: LangChain, Large Language Model

Vector Database: ChromaDB

Embeddings: Gemini Embeddings

Document Processing: PDF text extraction and document chunking

# Use Cases
📑 Chat with research papers
📚 Ask questions about books and study material
🏢 Analyze company documents
📋 Search technical documentation
🎓 Educational PDF assistant
📊 Extract information from reports
⚡ Quickly find information in large PDF files
Project Goal

The main goal of this project is to demonstrate how Generative AI, RAG, vector databases, embeddings, and document processing can be combined to build a practical AI assistant capable of answering questions from private document data.
