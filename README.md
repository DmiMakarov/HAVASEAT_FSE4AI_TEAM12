# Digit Recognition Application

A full-stack application for recognizing digits in images using Vue 3 frontend and a backend API.

> 🎉 **New!** Check out [SETUP_COMPLETE.md](./SETUP_COMPLETE.md) for a complete overview of what's included!

## 🏗️ Architecture

- **Frontend**: Vue 3 + Vite with modern UI and animations
- **Backend**: API service for digit recognition (to be implemented)
- **Docker**: Containerized deployment with Docker Compose

## 📋 Prerequisites

- Docker and Docker Compose (for containerized setup)
- OR Node.js v18+ (for local development)

## 🚀 Quick Start with Docker

### Using Make Commands (Easiest)

```bash
# View all available commands
make help

# Start development environment
make up

# Stop all services
make stop

# View logs
make logs

# Clean up
make clean
```

### Using Startup Script

```bash
# Start development environment
./start.sh

# Stop services
./start.sh stop
```

### Manual Docker Compose

1. **Clone the repository**
```bash
git clone <repository-url>
cd HAVASEAT_FSE4AI_TEAM12
```

2. **Create environment file**
```bash
cp env.example .env
```

3. **Edit `.env` file** with your configuration:
```env
# Frontend Configuration
VITE_FRONTEND_HOST=localhost
VITE_FRONTEND_PORT=3000

# Backend API Configuration
VITE_BACKEND_HOST=localhost
VITE_BACKEND_PORT=5000

# Backend Service Configuration (for Docker)
BACKEND_HOST=backend
BACKEND_PORT=5000
```

4. **Start the application**
```bash
docker-compose up
```

The frontend will be available at `http://localhost:3000`

## 💻 Local Development (Without Docker)

### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Create `.env` file**
```bash
cp ../env.example .env
```

4. **Start development server**
```bash
npm run dev
```

5. **Build for production**
```bash
npm run build
```

## 🐳 Docker Commands

### Build and Start Services
```bash
docker-compose up --build
```

### Stop Services
```bash
docker-compose down
```

### View Logs
```bash
# All services
docker-compose logs -f

# Frontend only
docker-compose logs -f frontend

# Backend only
docker-compose logs -f backend
```

### Rebuild Specific Service
```bash
docker-compose build frontend
docker-compose up -d frontend
```

## 📁 Project Structure

```
.
├── docker-compose.yml           # Docker compose configuration
├── env.example                  # Environment variables template
├── Makefile                     # Make commands for Docker
├── start.sh                     # Startup script
├── run-tests.sh                 # Test runner script
├── README.md                    # This file
├── TEST_SUMMARY.md              # Test suite overview
└── frontend/
    ├── Dockerfile              # Docker configuration
    ├── .dockerignore           # Docker ignore file
    ├── package.json            # Node dependencies
    ├── vite.config.js          # Vite configuration
    ├── vitest.config.js        # Test configuration
    ├── TESTING.md              # Testing guide
    └── src/
        ├── main.js             # Application entry point
        ├── App.vue             # Root component
        ├── __tests__/          # App-level tests
        │   └── App.test.js
        ├── components/         # Vue components
        │   ├── ImageUpload.vue
        │   └── __tests__/      # Component tests
        │       └── ImageUpload.test.js
        └── services/           # API services
            ├── api.js
            └── __tests__/      # Service tests
                └── api.test.js
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `VITE_FRONTEND_HOST` | Frontend dev server host | `localhost` | No |
| `VITE_FRONTEND_PORT` | Frontend dev server port | `3000` | No |
| `VITE_BACKEND_HOST` | Backend API host | `localhost` | Yes |
| `VITE_BACKEND_PORT` | Backend API port | `5000` | Yes |
| `BACKEND_HOST` | Backend service name (Docker) | `backend` | Docker only |
| `BACKEND_PORT` | Backend service port (Docker) | `5000` | Docker only |

### Docker Networking

When running with Docker Compose:
- Frontend and backend communicate via the `digit-recognition-network`
- Use service names (e.g., `backend`) as hostnames
- Ports are mapped to host machine as configured in `.env`

## 🔌 Backend API

The frontend expects a backend API with the following endpoint:

**POST** `/api/recognize`

**Request:**
- Content-Type: `multipart/form-data`
- Body: Form data with `image` field containing the image file

**Response:**
```json
{
  "digits": "12345"
}
```

Alternative response formats are also supported:
- `{ "result": "12345" }`
- `{ "recognized_digits": "12345" }`

## 🎨 Frontend Features

- ✨ Modern, animated UI with gradient backgrounds
- 📤 Drag-and-drop image upload
- 🖼️ Real-time image preview
- 🔢 Display of recognized digits
- 📱 Fully responsive design
- 🌓 Light/dark mode support
- ⚡ Fast hot-reload in development
- 🚀 Optimized production builds with nginx

## 🛠️ Troubleshooting

### Port Already in Use
If you get a "port already in use" error:
```bash
# Change the port in .env file
VITE_FRONTEND_PORT=8080
```

### Backend Connection Issues
- Make sure backend service is running
- Check `VITE_BACKEND_HOST` and `VITE_BACKEND_PORT` in `.env`
- For Docker: use service name `backend` as host
- For local dev: use `localhost` as host

### Docker Build Issues
```bash
# Clean rebuild
docker-compose down -v
docker-compose build --no-cache
docker-compose up
```

### Frontend Not Loading
```bash
# Check container status
docker-compose ps

# View logs
docker-compose logs frontend

# Restart service
docker-compose restart frontend
```

## 🧪 Testing

The frontend includes a comprehensive test suite using Vitest and Vue Test Utils.

### Running Tests

**Using Make (Recommended):**
```bash
make test              # Run all tests
make test-watch        # Watch mode
make test-ui           # Interactive UI
make test-coverage     # With coverage
```

**Using Test Script:**
```bash
./run-tests.sh         # Standard tests
./run-tests.sh watch   # Watch mode
./run-tests.sh ui      # Interactive UI
./run-tests.sh coverage # With coverage
```

### Test Coverage

The test suite covers:
- ✅ API service with mocked HTTP requests
- ✅ Component rendering and user interactions
- ✅ File upload and validation
- ✅ Digit recognition workflow
- ✅ Error handling
- ✅ Loading states

**Documentation:**
- [frontend/TESTING.md](./frontend/TESTING.md) - Detailed testing guide
- [TEST_SUMMARY.md](./TEST_SUMMARY.md) - Test suite overview and statistics

## 🎯 Next Steps

1. Start the application: `make up`
2. Access frontend at http://localhost:3000
3. Run tests: `make test`
4. Add your backend service to `docker-compose.yml`
5. Update `.env` with backend configuration

## 📝 Development Notes

### Hot Reload in Docker

The Docker setup includes volume mounting for hot reload:
```yaml
volumes:
  - ./frontend:/app
  - /app/node_modules
```

This allows code changes to reflect immediately without rebuilding the container.

## 🐳 Docker Quick Reference

| Command | Description |
|---------|-------------|
| `make up` | Start development server |
| `make start` | Start in background |
| `make stop` | Stop all services |
| `make logs` | View application logs |
| `make test` | Run tests |
| `make test-coverage` | Run tests with coverage |
| `make shell` | Open shell in container |
| `make clean` | Clean up containers and volumes |
| `make status` | Check container status |

### Container Details

- **Base Image**: Node.js 18 Alpine
- **Features**: Hot reload, live code sync, HMR
- **Network**: Custom bridge network for service communication
- **Port**: 3000 (configurable via .env)

## 📄 License

MIT

## 👥 Team

HAVASEAT FSE4AI TEAM12

