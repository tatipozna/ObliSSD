

echo "🚀 Iniciando entorno de desarrollo SSD Chatbot..."

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

echo "🔍 Verificando backend en puerto 8000..."
if ! check_port 8000; then
    echo "⚠️  El backend no está ejecutándose."
    echo "   Por favor, ejecuta el backend primero con: python app.py"
    echo "   O usa el archivo start_backend.bat"
    exit 1
fi

cd frontend

if [ ! -d "node_modules" ]; then
    echo "📦 Instalando dependencias..."
    npm install
fi

echo "🎯 Iniciando servidor de desarrollo React..."
npm run dev
