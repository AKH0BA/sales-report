--Here we Create Customers table
CREATE TABLE customers (
customer_id SERIAL PRIMARY KEY,
first_name TEXT NOT NULL,
last_name TEXT NOT NULL,
region TEXT CHECK (region IN ('East', 'West', 'North', 'South'))
);

--Here we Create Products Table
CREATE TABLE products (
product_id SERIAL PRIMARY KEY,
product_name TEXT NOT NULL,
category TEXT NOT NULL,
price NUMERIC(10,2) NOT NULL CHECK (price>=0)
);

--Orders (one row per order)
CREATE TABLE orders (
order_id SERIAL PRIMARY KEY,
customer_id INT NOT NULL REFERENCES customers(customer_id),
order_date DATE NOT NULL,
status TEXT NOT NULL CHECK (status IN ('paid', 'refunded', 'pending')) DEFAULT 'paid'
);

--Order Items
CREATE TABLE order_items (
order_item_id SERIAL PRIMARY KEY,
order_id INT NOT NULL REFERENCES orders(order_id) ON DELETE CASCADE,
product_id INT NOT NULL REFERENCES products(product_id),
quantity INT NOT NULL CHECK (quantity > 0),
unit_price NUMERIC(10,2) NOT NULL CHECK (unit_price >= 0)
);

CREATE INDEX idx_orders_date ON orders(order_date);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_order_items_prod ON order_items (product_id);