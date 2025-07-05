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

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React development server
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
    
    # Configuración diferente para cada tipo de documento
    
    # Para productos: chunks más grandes para mantener precio y descripción juntos
    product_splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,  # Aumentado para mantener información completa del producto
        chunk_overlap=100,
        separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
    )
    
    # Para ubicaciones: chunks medianos
    location_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=80,
        separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
    )
    
    # Para locales: chunks grandes para mantener toda la info de cada sucursal junta
    store_splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,  # Chunks más grandes para mantener información completa de sucursales
        chunk_overlap=150,
        separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
    )
    
    # Procesar catálogo de productos
    catalogo_chunks = product_splitter.split_text(pdf_producto)
    for i, chunk in enumerate(catalogo_chunks):
        if chunk.strip():
            doc = Document(
                page_content=chunk,
                metadata={"source": "catalogo", "type": "producto", "chunk_id": i}
            )
            documents.append(doc)
    
    # Procesar ubicaciones
    ubicaciones_chunks = location_splitter.split_text(pdf_ubicaciones)
    for i, chunk in enumerate(ubicaciones_chunks):
        if chunk.strip():
            doc = Document(
                page_content=chunk,
                metadata={"source": "ubicaciones", "type": "ubicacion", "chunk_id": i}
            )
            documents.append(doc)
    
    # Procesar información de locales
    locales_chunks = store_splitter.split_text(pdf_locales)
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

# Aumentar el número de chunks recuperados para mejor contexto
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 12}  # Aumentado de 8 a 12
)

from langchain.prompts import PromptTemplate

template = """Eres un asistente experto de Tienda Alemana. Tu trabajo es responder preguntas sobre productos, ubicaciones y sucursales.

Contexto disponible:
{context}

Pregunta del usuario: {question}

INSTRUCCIONES IMPORTANTES:
1. Para preguntas sobre productos: Busca información completa incluyendo precio, stock, características
2. Para preguntas sobre ubicaciones: Especifica góndola, sección, pasillo exacto
3. Para preguntas sobre sucursales: 
   - Proporciona dirección exacta
   - Horarios completos y precisos
   - Días de atención específicos
   - CUIDADO: "todos los días" incluye domingos, "lunes a sábado" NO incluye domingos
4. Para consultas de stock o disponibilidad: Revisa toda la información disponible
5. Para preguntas sobre precios: Busca y compara todos los productos que cumplan los criterios

Respuesta detallada:"""

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
    pdf_locales = load_pdf("pdf/Información de Locales.pdf")
    
    # Usar el mismo splitter que para locales
    store_splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=150,
        separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
    )
    
    chunks = store_splitter.split_text(pdf_locales)
    
    return JSONResponse(content={
        "total_chunks": len(chunks),
        "chunks_sample": chunks[:3],  # Mostrar primeros 3 chunks
        "chunks_with_horarios": [chunk for chunk in chunks if any(word in chunk.lower() for word in ['horario', 'hora', 'abre', 'cierra', 'domingo', 'lunes'])]
    })

@app.get("/debug/search")
def debug_search(query: str):
    """Endpoint para debuggear qué chunks se están recuperando"""
    docs = retriever.get_relevant_documents(query)
    
    return JSONResponse(content={
        "query": query,
        "retrieved_chunks": [
            {
                "content": doc.page_content,
                "metadata": doc.metadata
            } for doc in docs
        ]
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
