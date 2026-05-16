# Ecommerce Microservices

This project is a simple e-commerce microservices demo using FastAPI, PostgreSQL, RabbitMQ, and Docker Compose.

## Services

- `user-service` — user registration, login, JWT authentication
- `product-service` — product management
- `payment-service` — payment simulator for checkout flow
- `order-service` — order creation, payment orchestration, user order history
- `notification-service` — listens for order events and prints notifications
- `postgres-db` — shared PostgreSQL database
- `rabbitmq` — messaging broker for notifications

## What’s improved

- CORS support added to all FastAPI services via `CORS_ORIGINS`
- `/health` endpoints added to each service for readiness checks
- Order workflow improved to support:
  - pending orders
  - payment simulation via `POST /orders/{order_id}/pay`
  - order completion via `POST /orders/{order_id}/complete`
  - user order history via `GET /me/orders`
- Notification service handles RabbitMQ events and fetches user email from the user service

## Run locally

1. Start services:

```bash
docker compose up --build
```

2. Use the service URLs:

- User service: `http://localhost:8000`
- Product service: `http://localhost:8001`
- Order service: `http://localhost:8002`
- Notification service: `http://localhost:8003`
- Payment service: `http://localhost:8004`

## Example workflow

1. Create a user
2. Login and get JWT
3. Create a product
4. Create an order
5. Pay the order
6. Complete the order
7. View order history

## Smoke test

Run the simple smoke test script:

```bash
bash smoke_test.sh
```

## Notes

- For production, change the JWT secret and use database migrations (Alembic).
- Frontend can use the `CORS_ORIGINS` environment variable to restrict allowed domains.
