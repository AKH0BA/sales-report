-- Customers
INSERT INTO customers (first_name, last_name, region) VALUES
('John', 'Watson', 'East'),
('Chris', 'James', 'West'),
('Giorgio', 'Giovanni', 'North'),
('Thomas', 'Thompson', 'South'),
('Andrew', 'Jonson', 'East');

-- Products
INSERT INTO products (product_name,category,price) VALUES
('Laptop','Electronics',900),
('Phone','Electronics',500),
('Headphones','Accessories',80),
('Backpack','Accessories',60),
('Tablet','Electronics',300);

-- Orders
INSERT INTO orders (customer_id, order_date, status) VALUES
(1,'2025-10-01','paid'),
(2,'2025-10-01','paid'),
(3,'2025-10-02','paid'),
(4,'2025-10-03','paid'),
(5,'2025-10-04','paid'),
(1,'2025-10-05','refunded'),
(2,'2025-10-06','paid');

-- Order items
INSERT INTO order_items (order_id,product_id,quantity,unit_price) VALUES
(1,1,1,900),      -- Laptop
(1,3,2,80),       -- Headphones
(2,2,2,500),      -- 2 Phones
(3,5,1,300),      -- Tablet
(3,4,1,60),       -- Backpack
(4,3,1,80),       -- Headphones
(5,2,1,500),      -- Phone
(6,1,1,900),      -- Refunded order (will be excluded in KPIs)
(7,4,2,60);       -- Backpack x2