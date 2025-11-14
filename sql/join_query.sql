-- Comprehensive JOIN query across all e-commerce tables
-- This query retrieves complete order information including customer details,
-- order items with product information, and payment details

SELECT
    -- Customer Information
    c.customer_id,
    c.first_name,
    c.last_name,
    c.email,
    c.phone,
    c.country,
    c.city,
    c.address AS customer_address,
    
    -- Order Information
    o.order_id,
    o.order_date,
    o.status AS order_status,
    o.total_amount AS order_total,
    o.shipping_address,
    
    -- Order Items Information
    oi.order_item_id,
    oi.quantity,
    oi.unit_price,
    oi.subtotal AS item_subtotal,
    
    -- Product Information
    p.product_id,
    p.product_name,
    p.category,
    p.description,
    p.price AS product_price,
    p.stock,
    
    -- Payment Information
    py.payment_id,
    py.payment_method,
    py.amount AS payment_amount,
    py.payment_date,
    py.status AS payment_status,
    py.transaction_id
    
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
INNER JOIN order_items oi ON o.order_id = oi.order_id
INNER JOIN products p ON oi.product_id = p.product_id
LEFT JOIN payments py ON o.order_id = py.order_id

ORDER BY c.customer_id, o.order_id, oi.order_item_id;


-- Alternative Query 1: Summary view (one row per order)
-- SELECT
--     c.customer_id,
--     c.first_name,
--     c.last_name,
--     c.email,
--     o.order_id,
--     o.order_date,
--     o.status,
--     o.total_amount,
--     COUNT(oi.order_item_id) AS num_items,
--     py.payment_method,
--     py.status AS payment_status
-- FROM customers c
-- INNER JOIN orders o ON c.customer_id = o.customer_id
-- LEFT JOIN order_items oi ON o.order_id = oi.order_id
-- LEFT JOIN payments py ON o.order_id = py.order_id
-- GROUP BY o.order_id
-- ORDER BY o.order_date DESC;


-- Alternative Query 2: Revenue Analysis
-- SELECT
--     c.customer_id,
--     c.first_name,
--     c.last_name,
--     COUNT(DISTINCT o.order_id) AS total_orders,
--     SUM(o.total_amount) AS total_spent,
--     AVG(o.total_amount) AS avg_order_value,
--     COUNT(DISTINCT p.category) AS num_categories
-- FROM customers c
-- LEFT JOIN orders o ON c.customer_id = o.customer_id
-- LEFT JOIN order_items oi ON o.order_id = oi.order_id
-- LEFT JOIN products p ON oi.product_id = p.product_id
-- GROUP BY c.customer_id
-- ORDER BY total_spent DESC;


-- Alternative Query 3: Product Performance
-- SELECT
--     p.product_id,
--     p.product_name,
--     p.category,
--     COUNT(oi.order_item_id) AS times_ordered,
--     SUM(oi.quantity) AS total_quantity_sold,
--     SUM(oi.subtotal) AS total_revenue,
--     AVG(oi.unit_price) AS avg_price
-- FROM products p
-- LEFT JOIN order_items oi ON p.product_id = oi.product_id
-- LEFT JOIN orders o ON oi.order_id = o.order_id
-- GROUP BY p.product_id
-- ORDER BY total_revenue DESC;
