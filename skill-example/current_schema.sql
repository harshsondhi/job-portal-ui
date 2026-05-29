-- Snapshot of current database schema (pg_dump --schema-only output)

CREATE TABLE users (
    id          SERIAL PRIMARY KEY,
    email       VARCHAR(255) NOT NULL UNIQUE,
    username    VARCHAR(100) NOT NULL,
    created_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

CREATE TABLE orders (
    id          SERIAL PRIMARY KEY,
    customer_id INTEGER      NOT NULL REFERENCES users(id),
    total       NUMERIC(10, 2) NOT NULL,
    status      VARCHAR(50)  NOT NULL DEFAULT 'pending',
    created_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_orders_status ON orders(status);
