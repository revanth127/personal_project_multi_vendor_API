# Multi-Vendor Marketplace API

A FastAPI-based multi-vendor marketplace with role-based access control, implementing a clean layered architecture.

## Architecture Overview

This project follows a **layered architecture pattern**:
```
API Routes (app/api/v1/endpoints/) 
    -> Services (app/services/)
    -> Repositories (app/repositories/) 
    -> Models (app/models/)
```

## Features

- **Role-based Access Control**: Buyers and sellers with different permissions
- **Product Management**: Sellers can create, update, and delete products
- **Order Management**: Buyers can place orders, sellers can manage order status
- **Product Filtering**: Pagination, price ranges, seller filtering, search
- **Order Lifecycle**: pending -> confirmed -> shipped -> delivered -> cancelled
- **Structured Logging**: Request/response logging with performance metrics
- **JWT Authentication**: Secure token-based authentication
- **Comprehensive Testing**: Unit and integration tests with pytest

## Tech Stack

- **FastAPI**: Modern Python web framework
- **PostgreSQL**: Primary database
- **SQLAlchemy 2.0**: ORM with async support
- **Alembic**: Database migrations
- **JWT**: Token-based authentication
- **Argon2**: Password hashing
- **Pydantic**: Data validation
- **Pytest**: Testing framework
- **Docker**: Containerization

## Quick Start

### Using Docker (Recommended)

1. **Clone and setup**:
```bash
git clone <repository-url>
cd personal-project-the-multi-vendor-marketplace-api
cp .env.example .env
```

2. **Start services**:
```bash
docker-compose up -d
```

3. **Run migrations** (optional, separate service):
```bash
docker-compose --profile migration up alembic
```

4. **Access API**:
- API: http://localhost:8000
- Documentation: http://localhost:8000/docs
- Database: localhost:5432

### Local Development

1. **Install dependencies**:
```bash
pip install -r requirements.txt
pip install -r requirements-test.txt
```

2. **Setup database**:
```bash
# Create PostgreSQL database
createdb marketplace

# Run migrations
alembic upgrade head
```

3. **Run application**:
```bash
uvicorn app.main:app --reload
```

4. **Run tests**:
```bash
pytest app/tests/ -v
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/users/register` - User registration

### Products
- `GET /api/v1/products/` - Browse products with filters
- `POST /api/v1/products/` - Create product (seller only)
- `PUT /api/v1/products/{id}` - Update product (seller only)
- `DELETE /api/v1/products/{id}` - Delete product (seller only)

### Orders
- `POST /api/v1/orders/buy/{product_id}` - Place order (buyer only)
- `GET /api/v1/orders/` - Get user orders
- `GET /api/v1/orders/{id}/items` - Get order items
- `PUT /api/v1/orders/{id}/status` - Update order status

## Product Filtering

The product listing endpoint supports:
- `skip`: Pagination offset (default: 0)
- `limit`: Items per page (default: 15, max: 100)
- `min_price`: Minimum price filter
- `max_price`: Maximum price filter
- `seller_id`: Filter by specific seller
- `search`: Search product names

Example:
```
GET /api/v1/products/?skip=0&limit=10&min_price=10&max_price=100&search=laptop
```

## Order Lifecycle

Orders follow this state transition:
```
pending -> confirmed -> shipped -> delivered
    \-> cancelled (buyer only, any stage)
```

- **Buyer**: Can cancel their own orders
- **Seller**: Can confirm, ship, and mark as delivered

## Testing

Run the test suite:
```bash
# All tests
pytest app/tests/ -v

# Specific test file
pytest app/tests/test_auth.py -v

# With coverage
pytest app/tests/ --cov=app --cov-report=html
```

## Project Structure

```
app/
|-- api/v1/
|   |-- endpoints/          # API route handlers
|   |-- api.py             # API router configuration
|-- core/                   # Core application logic
|-- services/               # Business logic layer
|-- repositories/           # Data access layer
|-- middleware/             # Custom middleware
|-- models/               # Database models
|-- schemas/              # Pydantic schemas
|-- tests/                # Test suite
|-- database.py           # Database configuration
|-- main.py               # FastAPI application
|-- config.py             # Settings management
|-- oauth2.py             # JWT authentication
|-- utils.py              # Utility functions
```

## Environment Variables

Create a `.env` file based on `.env.example`:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/marketplace
SECRET_KEY=your-super-secret-key
DEBUG=True
```

## Development Notes

- The application uses SQLAlchemy 2.0 with async support
- All database operations are handled through the repository layer
- Business logic is separated into services
- Authentication uses JWT tokens with 30-minute expiration
- Passwords are hashed using Argon2
- All endpoints are under `/api/v1/` for versioning
- Structured logging tracks request/response times and errors

## Production Deployment

For production deployment:

1. **Security**:
   - Change `SECRET_KEY` to a strong random value
   - Use HTTPS in production
   - Set `DEBUG=False`

2. **Database**:
   - Use managed PostgreSQL service
   - Configure connection pooling
   - Set up regular backups

3. **Performance**:
   - Add Redis for caching (future enhancement)
   - Configure proper CORS settings
   - Set up monitoring and alerting

## License

This project is for educational purposes.