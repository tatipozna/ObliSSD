Universidad ORT Uruguay  
Facultad de Ingeniería

**Obligatorio IA \- Creación Chatbot**

Tatiana Poznanski \- 221056  
Martin Edelman \- 263630  
Gonzalo Gularte \- 270959

Sistemas de Soporte de Decisión

Profesores: Carlos Nieves, Santiago Diaz,  
**2025**

# **Repositorio de GitHub**

[https://github.com/tatipozna/ObliSSD](https://github.com/tatipozna/ObliSSD)

# **Documentación de Endpoints**

### Backend API (Puerto 8000\)

|   Endpoint    | Método |            Descripción             |               Parámetros               |                  Respuesta                   |
| :-----------: | :----: | :--------------------------------: | :------------------------------------: | :------------------------------------------: |
|       /       |  GET   |          Página principal          |                   \-                   |         FileResponse con index.html          |
|     /chat     |  GET   |     Procesamiento de consultas     | query (string) \- Consulta del usuario |     {"respuesta": "texto de respuesta"}      |
| /debug/chunks |  GET   | Depuración de chunks de documentos |                   \-                   | Información sobre división de documentos PDF |
| /debug/search |  GET   |  Depuración de búsqueda semántica  |  query (string) \- Consulta de prueba  |     Información sobre chunks recuperados     |

## **Detalles de los Endpoints**

### GET /chat

- **Entrada:** parámetro query con la consulta del usuario
- **Procesamiento:** utiliza RAG (Retrieval-Augmented Generation) para buscar información relevante en los documentos PDF
- **Salida:** JSON con la respuesta del asistente
- **Manejo de errores:** devuelve mensajes de error específicos con códigos de estado HTTP apropiados

### GET /debug/chunks

- **Entrada:** sin parámetros
- **Procesamiento:** analiza cómo se dividieron los documentos PDF en chunks de la información de locales
- **Salida:** información sobre el total de chunks, muestras y chunks que contienen información de horarios

### GET /debug/search

- **Entrada:** parámetro query con la consulta de prueba
- **Procesamiento:** ejecuta una búsqueda semántica y devuelve los chunks más relevantes
- **Salida:** JSON con la consulta y los chunks recuperados con sus metadatos

#

# **Resumen del Trabajo**

## **Procesamiento de PDFs e Índice Semántico**

### Librerías utilizadas:

- **PyMuPDF (fitz):** extracción de texto de archivos PDF
- **FAISS:** Vector store para búsqueda semántica eficiente
- **OpenAI Embeddings:** generación de embeddings vectoriales
- **RecursiveCharacterTextSplitter:** división inteligente de texto

### Esquema de Chunking Optimizado:

- **Catálogo de Productos:** 200 caracteres, overlap 50
- **Ubicación Física:** 300 caracteres, overlap 80
- **Información de Locales:** 600 caracteres, overlap 150
- **Separadores:** \["\\n\\n", "\\n", ".", "\!", "?", ",", " ", ""\]
- **Metadatos:** cada chunk incluye información sobre fuente, tipo y ID único

### Procesamiento de documentos:

**Tres tipos de documentos procesados con chunking diferenciado:**  
1\. Catálogo de Productos (metadata: type="producto", source="catalogo")  
2\. Información de Locales (metadata: type="local", source="locales")  
3\. Ubicación Física de Productos (metadata: type="ubicacion", source="ubicaciones")

## **Integración con LangChain y OpenAI**

### Configuración del modelo:

- **LLM:** GPT-4o-mini con temperatura 0.1 para respuestas consistentes
- **Chain:** RetrievalQA con chain_type="stuff"
- **Retriever:** búsqueda por similitud con k=12 documentos (optimizado para mejor cobertura)

### Prompt Engineering:

- Prompt personalizado con instrucciones específicas para Tienda Alemana
- Instrucciones detalladas para productos, ubicaciones y sucursales
- Manejo especial de días de atención y horarios
- Criterios específicos para consultas de stock, precios y disponibilidad
- Respuestas basadas únicamente en el contexto proporcionado

### Funcionalidades avanzadas:

- Chunking diferenciado por tipo de documento para optimizar la recuperación
- Sistema de metadatos enriquecido para mejor categorización
- Manejo inteligente de respuestas vacías o irrelevantes

###

### Chunking Diferenciado

El sistema utiliza diferentes configuraciones de chunking según el tipo de documento:

- **Productos:** chunks pequeños (200 caracteres) para información específica y precios
- **Ubicaciones:** chunks medianos (300 caracteres) para descripciones de ubicación
- **Locales:** chunks grandes (600 caracteres) para información completa de sucursales

###

### Retrieval Optimizado

- **k=12 documentos:** aumentado para mejor cobertura de información
- **Búsqueda semántica:** utiliza embeddings de OpenAI para encontrar contenido relevante
- **Metadatos estructurados:** permite filtrado y categorización precisa

###

### Prompt Engineering Avanzado

**El prompt incluye instrucciones específicas para:**

- Consultas de productos con precios y características
- Ubicaciones exactas con góndola y sección
- Información completa de sucursales con horarios
- Manejo de consultas de stock y disponibilidad

# **Diseño del backend**

### Framework: FastAPI

- **Ventajas:** alto rendimiento, documentación automática, validación de tipos
- **CORS:** configurado para permitir conexiones desde el frontend (localhost:3000)

### Estructura del proyecto:

backend/  
├── app.py \# Aplicación principal  
├── requirements.txt \# Dependencias  
├── pdf/ \# Documentos PDF fuente  
│ ├── Catálogo de Productos.pdf  
│ ├── Información de Locales.pdf  
│ └── Ubicación Física de Productos.pdf

### Manejo de errores:

- Try-catch en endpoints principales
- Respuestas JSON estructuradas
- Códigos de estado HTTP apropiados
- Mensajes de error descriptivos
- Manejo especial de respuestas vacías o irrelevantes

### Endpoints de depuración:

- **/debug/chunks:** analiza la división de documentos PDF
- **/debug/search:** permite probar búsquedas semánticas y ver chunks recuperados

#

# **Implementación del Frontend**

### Framework: React 18 con Vite

- **Ventajas:** desarrollo rápido, hot-reload, bundling optimizado

### Estructura del proyecto:

frontend/  
├── src/  
│ ├── components/  
│ │ ├── Chat.jsx \# Componente principal del chat  
│ │ └── Chat.css \# Estilos del chat  
│ ├── services/  
│ │ └── api.js \# Cliente HTTP para backend  
│ ├── App.jsx \# Componente raíz  
│ └── main.jsx \# Punto de entrada

### Funcionalidades principales:

- **Chat en tiempo real:** interfaz conversacional intuitiva
- **Manejo de estado:** useState para mensajes y carga
- **Comunicación HTTP:** axios con interceptores para manejo de errores
- **UX/UI:** indicadores de carga, scroll automático, diseño responsivo

### Características de diseño:

- Diseño glassmorphism con efectos de blur
- Colores de la bandera alemana (negro, rojo, amarillo)
- Totalmente responsivo (mobile-first)
- Animaciones suaves y transiciones

# **Manual de Instalación y Ejecución**

### Prerrequisitos

1. Python 3.8+
2. Node.js 16+ y npm
3. Clave API de OpenAI
4. Git (opcional, para clonar el repositorio)

## **Configuración del Backend**

1. **Navegar al directorio backend:** cd backend

2. **Crear entorno virtual (recomendado):** python \-m venv venv

3. **Activar entorno virtual:**  
   \# Windows PowerShell  
   venv\\Scripts\\Activate.ps1

   \# Windows Command Prompt  
   venv\\Scripts\\activate

   \# macOS/Linux  
   source venv/bin/activate

4. **Instalar dependencias:** pip install \-r requirements.txt

5. **Configurar variables de entorno:**  
   \# Windows PowerShell \- Crear archivo .env en la carpeta backend  
   echo "OPENAI_API_KEY=tu_clave_api_aqui" | Out-File \-FilePath .env \-Encoding utf8

6. **Alternativamente, crear manualmente el archivo .env con:** OPENAI_API_KEY=tu_clave_api_aqui

7. **Ejecutar el servidor:** python app.py

El backend estará disponible en http://localhost:8000

###

## **Configuración del Frontend**

1. **Navegar al directorio frontend:** cd frontend
2. **Instalar dependencias:** npm install
3. **Ejecutar el servidor de desarrollo:** npm run dev

El frontend estará disponible en http://localhost:3000

###

## **Estructura de Archivos del Proyecto**

ObliSSD/  
├── backend/  
│ ├── app.py \# Servidor FastAPI  
│ ├── requirements.txt \# Dependencias Python  
│ ├── .env \# Variables de entorno (crear)  
│ └── pdf/ \# Documentos PDF  
├── frontend/  
│ ├── src/ \# Código fuente React  
│ ├── package.json \# Dependencias Node.js  
│ └── vite.config.js \# Configuración Vite  
├── start_frontend.sh \# Script de inicio  
└── README.md \# Este archivo

## **Troubleshooting**

### Errores comunes:

1. **Error de conexión:** verificar que ambos servidores estén corriendo
2. **Error de API Key:** asegurar que la variable OPENAI_API_KEY esté configurada en el archivo .env
3. **Error de dependencias:** ejecutar pip install \-r requirements.txt y npm install
4. **Error de CORS:** verificar configuración de CORS en app.py
5. **Error de PowerShell:** si hay problemas con scripts, ejecutar Set-ExecutionPolicy \-ExecutionPolicy RemoteSigned \-Scope CurrentUser
6. **Respuestas vacías:** verificar que los PDFs estén en la carpeta backend/pdf/
