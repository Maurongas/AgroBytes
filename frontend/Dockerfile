FROM node:20-slim

WORKDIR /app

# Copiamos primero los archivos de dependencias
COPY package*.json ./

# Instalamos los paquetes
RUN npm install

# Copiamos el resto del código
COPY . .

EXPOSE 3000

# Servidor de desarrollo de Vite escuchando en todas las redes de Docker
CMD ["npx", "vite", "--host", "0.0.0.0", "--port", "3000"]
