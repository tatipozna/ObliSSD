from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv
import fitz
from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles

load_dotenv() 
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

app = FastAPI()

def load_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text("text") 
    return text

pdf_producto = load_pdf("pdf/Catálogo de Productos.pdf")
pdf_locales = load_pdf("pdf/Información de Locales.pdf")
pdf_ubicaciones = load_pdf("pdf/Ubicación Física de Productos.pdf")

combined_texts = [pdf_producto, pdf_locales, pdf_ubicaciones]

embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_texts(combined_texts, embeddings)

llm = ChatOpenAI(model_name="gpt-4.1-2025-04-14")

retriever = vectorstore.as_retriever()
answer_bot = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

@app.get("/")
def get_index():
    return FileResponse("index.html")

@app.get("/chat")
def chat(query: str):
    response = answer_bot.run(query)

    if not response or response.strip() == "The information provided doesn't include":
        response = "No se encontró información relevante."

    return JSONResponse(content={"respuesta": response})
