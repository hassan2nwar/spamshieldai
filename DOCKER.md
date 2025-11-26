# Docker Setup for SpamShield AI

This project is now dockerized and can be run using Docker Compose.

## Prerequisites

- Docker Desktop (or Docker Engine + Docker Compose)
- At least 2GB of free disk space

## Quick Start

1. **Create environment file:**
   ```bash
   # Copy the template to create your .env file
   cp env.template .env
   ```
   
   Or create a `.env` file manually with the following variables:
   ```env
   API_PORT=5000
   API_HOST=0.0.0.0
   FRONTEND_PORT=3000
   VITE_API_URL=http://localhost:5000
   CORS_ORIGINS=http://localhost:3000,http://localhost:5173,http://127.0.0.1:3000,http://127.0.0.1:5173
   FLASK_ENV=production
   FLASK_DEBUG=false
   ```

2. **Build and start all services:**
   ```bash
   docker-compose up --build
   ```

2. **Access the application:**
   - Frontend: http://localhost:3000
   - API: http://localhost:5000

3. **Stop the services:**
   ```bash
   docker-compose down
   ```

## Services

### API Service
- **Port:** 5000
- **Technology:** Python Flask
- **Health Check:** http://localhost:5000/api/health

### Frontend Service
- **Port:** 3000 (mapped to container port 80)
- **Technology:** React + Vite, served with Nginx
- **Build:** Static files are built during Docker image creation

## Development

### Rebuild after code changes:
```bash
docker-compose up --build
```

### View logs:
```bash
docker-compose logs -f
```

### Run in detached mode:
```bash
docker-compose up -d
```

### Stop and remove containers:
```bash
docker-compose down
```

### Remove volumes and images:
```bash
docker-compose down -v --rmi all
```

## Environment Variables

All configuration is managed through the `.env` file. Key variables:

- **API_PORT**: Port for the API service (default: 5000)
- **API_HOST**: Host binding for the API (default: 0.0.0.0)
- **FRONTEND_PORT**: Port for the frontend service (default: 3000)
- **VITE_API_URL**: API URL used by the frontend (default: http://localhost:5000)
- **CORS_ORIGINS**: Comma-separated list of allowed CORS origins
- **FLASK_ENV**: Flask environment (production/development)
- **FLASK_DEBUG**: Enable Flask debug mode (true/false)

The `.env` file is automatically loaded by docker-compose. You can customize these values to match your deployment environment.

## Troubleshooting

1. **Port already in use:**
   - Change the port mappings in `docker-compose.yml` if ports 3000 or 5000 are already in use

2. **Models not found:**
   - Ensure the `models/` directory exists with `spam_classifier.pkl` and `vectorizer.pkl`

3. **Frontend can't connect to API:**
   - Check that both services are running: `docker-compose ps`
   - Verify API health: `curl http://localhost:5000/api/health`
   - Check CORS settings in `api/app.py`

## Production Considerations

For production deployment:
1. Use environment-specific configuration files
2. Set up proper secrets management
3. Use a reverse proxy (e.g., Traefik, Nginx) for SSL termination
4. Configure resource limits in `docker-compose.yml`
5. Set up logging and monitoring
6. Use multi-stage builds (already implemented for frontend)

