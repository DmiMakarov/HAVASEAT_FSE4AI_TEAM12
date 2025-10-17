# Development Dockerfile
FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source files
COPY . .

# Expose the port from environment variable (default 3000)
EXPOSE ${VITE_FRONTEND_PORT:-3000}

# Start development server
CMD ["npm", "run", "dev"]

