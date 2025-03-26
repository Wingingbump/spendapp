# SpendApp

A modern expense tracking application with secure authentication and Plaid integration.

## Features

- User authentication with JWT
- Secure password hashing
- PostgreSQL database integration
- React frontend with Tailwind CSS
- FastAPI backend
- Docker containerization
- Plaid integration (coming soon)

## Project Structure

```
.
├── backend/
│   ├── auth/           # Authentication utilities
│   ├── models/         # Database models
│   ├── routes/         # API routes
│   ├── services/       # Business logic
│   ├── tests/          # Unit tests
│   ├── Dockerfile      # Backend container configuration
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/ # React components
│   │   └── App.tsx     # Main application component
│   ├── Dockerfile      # Frontend container configuration
│   └── package.json
├── docker-compose.yml  # Container orchestration
└── .env.example        # Example environment variables
```

## Setup

1. Clone the repository
```bash
git clone <repository-url>
cd spendapp
```

2. Create environment files
```bash
cp backend/.env.example backend/.env
# Edit backend/.env with your configuration
```

3. Start the application
```bash
docker-compose up --build
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000

## Development

### Prerequisites
- Docker
- Docker Compose

### Running in development mode
```bash
docker-compose up --build
```

The development environment includes:
- Hot reloading for both frontend and backend
- PostgreSQL database
- Volume mounts for local development

### Running tests
```bash
# Backend tests
docker-compose exec backend pytest

# Frontend tests
docker-compose exec frontend npm test
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.