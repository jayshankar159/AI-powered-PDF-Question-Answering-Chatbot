from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Optional
import os
from dotenv import load_dotenv
import socket

from .models import QueryRequest
from .rag_pipeline import RAGPipeline

load_dotenv()

app = FastAPI(title="RAG Chatbot API - Local")

# CORS middleware - Allow all local network
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        f"http://{socket.gethostbyname(socket.gethostname())}:3000",
        "*"  # Allow all local network
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG pipeline
rag_pipeline = RAGPipeline(api_key=os.getenv("GEMINI_API_KEY"))

@app.get("/")
async def root():
    return {
        "message": "RAG Chatbot API is running",
        "local_ip": socket.gethostbyname(socket.gethostname()),
        "host": os.getenv("HOST", "0.0.0.0"),
        "port": os.getenv("PORT", "8000")
    }

@app.get("/network-info")
async def network_info():
    """Get network information for local access"""
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    return {
        "hostname": hostname,
        "local_ip": local_ip,
        "access_urls": [
            f"http://localhost:8000",
            f"http://127.0.0.1:8000",
            f"http://{local_ip}:8000"
        ]
    }

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload and process a document"""
    try:
        content = await file.read()
        result = rag_pipeline.process_document(content, file.filename)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query")
async def query(request: QueryRequest):
    """Process a query"""
    try:
        result = rag_pipeline.query(
            query_text=request.query,
            session_id=request.session_id,
            file_ids=request.file_ids,
            use_tools=request.use_tools
        )
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history/{session_id}")
async def get_history(session_id: str):
    """Get chat history for a session"""
    try:
        history = rag_pipeline.get_chat_history(session_id)
        return JSONResponse(content={"history": history})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/document/{file_id}")
async def delete_document(file_id: str):
    """Delete a document"""
    try:
        rag_pipeline.delete_document(file_id)
        return JSONResponse(content={"message": "Document deleted successfully"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host=host, port=port)