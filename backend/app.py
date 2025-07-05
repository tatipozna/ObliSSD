from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
import os
from dotenv import load_dotenv
import fitz
from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

load_dotenv() 
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def load_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text("text") 
    return text

def create_optimized_documents():
    """Crea documentos con chunking optimizado para mejor retrieval"""
    documents = []
    
    pdf_producto = load_pdf("pdf/Catálogo de Productos.pdf")
    pdf_locales = load_pdf("pdf/Información de Locales.pdf")
    pdf_ubicaciones = load_pdf("pdf/Ubicación Física de Productos.pdf")
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,  
        chunk_overlap=50,  
        separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
    )
    
    catalogo_chunks = text_splitter.split_text(pdf_producto)
    for i, chunk in enumerate(catalogo_chunks):
        if chunk.strip():
            doc = Document(
                page_content=chunk,
                metadata={"source": "catalogo", "type": "producto", "chunk_id": i}
            )
            documents.append(doc)
    
    ubicaciones_chunks = text_splitter.split_text(pdf_ubicaciones)
    for i, chunk in enumerate(ubicaciones_chunks):
        if chunk.strip():
            doc = Document(
                page_content=chunk,
                metadata={"source": "ubicaciones", "type": "ubicacion", "chunk_id": i}
            )
            documents.append(doc)
    
    locales_chunks = text_splitter.split_text(pdf_locales)
    for i, chunk in enumerate(locales_chunks):
        if chunk.strip():
            doc = Document(
                page_content=chunk,
                metadata={"source": "locales", "type": "local", "chunk_id": i}
            )
            documents.append(doc)
    
    return documents

documents = create_optimized_documents()

embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(documents, embeddings)

llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.1)

retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 8} 
)

from langchain.prompts import PromptTemplate

template = """Eres un asistente de Tienda Alemana. Usa el contexto proporcionado para responder la pregunta del usuario de manera precisa y completa.

Contexto:
{context}

Pregunta: {question}

Instrucciones:
- Responde basándote únicamente en la información del contexto
- Si preguntan por productos con ciertas características (ej: precio, disponibilidad), revisa TODA la información disponible
- Si preguntan por sucursales con ciertas características (ej: horarios, días, dirección), revisa TODA la información disponible
- IMPORTANTE: Lee cuidadosamente los días de atención:
  * "todos los días" o "todos los días de la semana" = incluye domingos
  * "de lunes a sábado" = NO incluye domingos
- La Tienda Alemana Central es sede principal
- De las sucursales proporciona dirección, horarios y días exactos según el contexto
- Si no tienes información suficiente, indica que no encontraste esa información específica
- No respondas en markdown, solo texto plano


Respuesta:"""

PROMPT = PromptTemplate(
    template=template,
    input_variables=["context", "question"]
)

answer_bot = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    chain_type_kwargs={"prompt": PROMPT}
)

@app.get("/")
def get_index():
    return FileResponse("index.html")

@app.get("/chat")
def chat(query: str):
    try:
        response = answer_bot.run(query)
        
        if not response or response.strip() == "" or "The information provided doesn't include" in response:
            response = "No se encontró información relevante para su consulta."
        
        return JSONResponse(content={"respuesta": response})
    
    except Exception as e:
        return JSONResponse(
            content={"respuesta": f"Error al procesar la consulta: {str(e)}"}, 
            status_code=500
        )

@app.get("/debug/chunks")
def debug_chunks():
    """Endpoint para verificar cómo se están dividiendo los documentos"""
    pdf_producto = load_pdf("pdf/Catálogo de Productos.pdf")
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=50,
        separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
    )
    
    chunks = text_splitter.split_text(pdf_producto)
    
    return JSONResponse(content={
        "total_chunks": len(chunks),
        "chunks_sample": chunks[:5],  
        "chunks_with_prices": [chunk for chunk in chunks if '$' in chunk]
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

