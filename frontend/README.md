# Vue Digit Recognition Frontend

A Vue 3 + Vite application for uploading images and recognizing digits using a backend API.

## Features

- 📤 Image upload via click or drag-and-drop
- 🖼️ Image preview before recognition
- 🔢 Display recognized digits from backend
- ⚡ Fast and modern UI with Vue 3 + Vite
- 🎨 Clean, minimal design with responsive layout
- ⚙️ Configurable backend connection via environment variables

## Prerequisites

- Node.js (v16 or higher)
- npm or yarn

## Setup

1. Install dependencies:
```bash
npm install
```

2. Create a `.env` file in the root directory (copy from `env.example`):
```bash
cp env.example .env
```

3. Configure your backend settings in `.env`:
```env
VITE_BACKEND_HOST=localhost
VITE_BACKEND_PORT=5000
```

## Development

Run the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:3000`

## Build for Production

Build the application:
```bash
npm run build
```

Preview the production build:
```bash
npm run preview
```

## Backend API Requirements

The frontend expects the backend to expose the following endpoint:

### POST `/api/recognize`

**Request:**
- Content-Type: `multipart/form-data`
- Body: Form data with an `image` field containing the uploaded image file

**Response:**
- Content-Type: `application/json`
- Body: JSON object with recognized digits

Example response formats (any of these will work):
```json
{
  "digits": "12345"
}
```
or
```json
{
  "result": "12345"
}
```
or
```json
{
  "recognized_digits": "12345"
}
```

## Project Structure

```
├── index.html                 # HTML entry point
├── package.json              # Dependencies and scripts
├── vite.config.js            # Vite configuration
├── env.example               # Environment variables template
├── src/
│   ├── main.js               # Application entry point
│   ├── App.vue               # Root component
│   ├── style.css             # Global styles
│   ├── components/
│   │   └── ImageUpload.vue   # Image upload component
│   └── services/
│       └── api.js            # API service for backend communication
```

## Technologies Used

- **Vue 3** - Progressive JavaScript framework
- **Vite** - Next generation frontend tooling
- **Axios** - HTTP client for API requests

## License

MIT

