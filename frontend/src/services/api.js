import axios from "axios";

// Configuración de la API para Tienda Alemana
const API_BASE_URL = "http://localhost:8000";

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 segundos timeout para consultas complejas
  headers: {
    "Content-Type": "application/json",
  },
});

// Interceptor para manejo de errores
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error("API Error:", error);

    if (error.code === "ECONNABORTED") {
      error.message = "La consulta está tomando demasiado tiempo. Por favor, intenta de nuevo.";
    } else if (error.response?.status === 500) {
      error.message = "Error interno del servidor. Intenta de nuevo más tarde.";
    } else if (!error.response) {
      error.message = "No se pudo conectar con el servidor. Verifica que esté ejecutándose.";
    }

    return Promise.reject(error);
  }
);

export const chatService = {
  // Envía una consulta al chatbot de Tienda Alemana
  sendMessage: async (query) => {
    const response = await api.get("/chat", {
      params: { query },
    });
    return response.data;
  },
};

export default api;
