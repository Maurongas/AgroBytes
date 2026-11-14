FROM node:20-slim

WORKDIR /app

# Desactiva encuestas interactivas que apagan el contenedor
ENV NEXT_TELEMETRY_DISABLED=1

# Copiamos primero los archivos de dependencias
COPY package*.json ./

# Instalamos los paquetes
RUN npm install

# Copiamos el resto del código
COPY . .

EXPOSE 3000

# Comando directo forzando a escuchar en todas las redes de Docker
CMD ["npx", "next", "dev", "-H", "0.0.0.0"]