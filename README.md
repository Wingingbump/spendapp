# SpendApp

A personal finance application that helps you track your spending by connecting to your bank accounts using Plaid.

## Setup

### Using Docker (Recommended)

1. Create a `.env` file in the root directory with your Plaid API credentials:
```
PLAID_CLIENT_ID=your_client_id
PLAID_SECRET=your_secret
PLAID_ENV=sandbox
```

2. Build and start the containers:
```bash
docker-compose up --build
```

3. Initialize the database:
```bash
docker-compose exec backend flask db init
docker-compose exec backend flask db migrate
docker-compose exec backend flask db upgrade
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000
- Database: localhost:5432

### Manual Setup

#### Backend Setup

1. Create a virtual environment and activate it:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

3. Create a `.env` file in the backend directory with your Plaid API credentials:
```
PLAID_CLIENT_ID=your_client_id
PLAID_SECRET=your_secret
PLAID_ENV=sandbox
```

#### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Start the development server:
```bash
npm start
```

## Testing

### Backend Tests
```bash
cd backend
python -m unittest tests/test_plaid_integration.py
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Features

- Connect bank accounts using Plaid
- View account balances
- Track transactions
- Categorize spending
- View spending analytics

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request