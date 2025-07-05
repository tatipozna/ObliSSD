# Tienda Alemana - Frontend

Este es un frontend moderno desarrollado en React usando Vite que se conecta a la API FastAPI del chatbot de Tienda Alemana.

## 🇩🇪 Sobre Tienda Alemana

Tienda Alemana es una tienda especializada en productos alemanes auténticos, desde cervezas tradicionales hasta comida típica alemana. Nuestro chatbot te ayuda a encontrar productos, ubicaciones de locales y resolver todas tus consultas sobre productos alemanes.

## Características

- 🚀 **Vite**: Build tool ultrarrápido
- ⚛️ **React**: Interfaz de usuario moderna y responsiva
- 🎨 **Diseño moderno**: Interfaz limpia con gradientes y efectos glassmorphism
- 📱 **Responsive**: Funciona perfectamente en desktop y móvil
- 🇩🇪 **Temática alemana**: Diseño y contenido especializado en productos alemanes
- 🔄 **Tiempo real**: Animaciones de carga y efectos de escritura
- 🌐 **CORS habilitado**: Comunicación segura con la API

## Estructura del proyecto

```
frontend/
├── src/
│   ├── components/
│   │   ├── Chat.jsx          # Componente principal del chat
│   │   └── Chat.css          # Estilos del chat
│   ├── App.jsx               # Componente principal de la aplicación
│   ├── App.css               # Estilos globales
│   ├── main.jsx              # Punto de entrada de React
│   └── index.css             # Estilos base
├── index.html                # Archivo HTML principal
├── package.json              # Dependencias y scripts
└── vite.config.js            # Configuración de Vite
```

## Instalación y uso

### 1. Instalar dependencias

```bash
cd frontend
npm install
```

### 2. Iniciar el servidor de desarrollo

```bash
npm run dev
```

El frontend estará disponible en `http://localhost:3000`

### 3. Iniciar el backend FastAPI

En otra terminal, desde el directorio raíz del proyecto:

```bash
# Instalar dependencias de Python (si no están instaladas)
pip install -r requirements.txt

# Iniciar el servidor FastAPI
uvicorn app:app --reload
```

El backend estará disponible en `http://localhost:8000`

## Scripts disponibles

- `npm run dev`: Inicia el servidor de desarrollo
- `npm run build`: Construye la aplicación para producción
- `npm run preview`: Previsualiza la build de producción
- `npm run lint`: Ejecuta el linter

## Funcionalidades

### Chat en tiempo real

- Interfaz de chat moderna con burbujas de mensajes
- Animaciones de carga con indicador de escritura
- Scroll automático a los mensajes más recientes
- Mensajes con timestamp

### Integración con API

- Conexión automática con FastAPI backend
- Manejo de errores de conexión
- Encoding URL para caracteres especiales
- Respuestas JSON estructuradas

### Diseño responsivo

- Funciona en desktop y móvil
- Gradientes y efectos glassmorphism
- Tipografía moderna con Google Fonts
- Iconos emoji para mejor UX

## Configuración

### Cambiar la URL de la API

Si necesitas cambiar la URL de la API, modifica el archivo `src/components/Chat.jsx`:

```javascript
const response = await fetch(`http://localhost:8000/chat?query=${encodeURIComponent(userMessage)}`);
```

### Personalizar el diseño

Los estilos están en `src/components/Chat.css` y pueden ser modificados según tus preferencias.

## Producción

Para deployar en producción:

1. Construye la aplicación:

```bash
npm run build
```

2. Los archivos estáticos se generarán en la carpeta `dist/`

3. Puedes servir estos archivos con cualquier servidor web estático

## Tecnologías utilizadas

- **React 18**: Library de UI
- **Vite**: Build tool y dev server
- **CSS3**: Estilos con gradientes, animations y glassmorphism
- **Google Fonts**: Tipografía Inter
- **ESLint**: Linting de código

## Próximas características

- [ ] Historial de conversaciones
- [ ] Modo oscuro/claro
- [ ] Exportar conversaciones
- [ ] Configuración de usuario
- [ ] Soporte para archivos adjuntos
- [ ] Notificaciones push
