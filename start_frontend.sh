#!/bin/bash

# Script para iniciar el entorno de desarrollo completo

echo "🚀 Iniciando entorno de desarrollo SSD Chatbot..."

# Función para verificar si un puerto está en uso
check_port() {
    local port=$1
    if netstat -tuln | grep -q ":$port "; then
        echo "✅ Puerto $port en uso"
        return 0
    else
        echo "❌ Puerto $port no está en uso"
        return 1
    fi
}

# Verificar que el backend esté ejecutándose
echo "🔍 Verificando backend en puerto 8000..."
if ! check_port 8000; then
    echo "⚠️  El backend no está ejecutándose."
    echo "   Por favor, ejecuta el backend primero con: python app.py"
    echo "   O usa el archivo start_backend.bat"
    exit 1
fi

# Cambiar al directorio del frontend
cd frontend

# Verificar si node_modules existe
if [ ! -d "node_modules" ]; then
    echo "📦 Instalando dependencias..."
    npm install
fi

# Iniciar el servidor de desarrollo
echo "🎯 Iniciando servidor de desarrollo React..."
npm run dev
