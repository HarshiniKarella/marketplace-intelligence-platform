-- ============================================================
-- Raw -> Core transformations
-- ============================================================


-- 1. Customers
INSERT INTO core.customers (
    customer_id,
    customer_unique_id,
    customer_zip_code_prefix,
    customer_city,
    customer_state
)
SELECT
    customer_id,
    customer_unique_id,
    customer_zip_code_prefix::INTEGER,
    customer_city,
    customer_state
FROM raw.customers;


-- 2. Product categories
INSERT INTO core.product_categories (
    product_category_name,
    product_category_name_english
)
SELECT DISTINCT
    p.product_category_name,
    t.product_category_name_english
FROM raw.products p
LEFT JOIN raw.product_category_name_translation t
    ON p.product_category_name = t.product_category_name
WHERE NULLIF(p.product_category_name, '') IS NOT NULL;


-- 3. Products
INSERT INTO core.products (
    product_id,
    product_category_name,
    product_name_length,
    product_description_length,
    product_photos_qty,
    product_weight_g,
    product_length_cm,
    product_height_cm,
    product_width_cm
)
SELECT
    product_id,
    NULLIF(product_category_name, ''),
    NULLIF(product_name_lenght, '')::INTEGER,
    NULLIF(product_description_lenght, '')::INTEGER,
    NULLIF(product_photos_qty, '')::INTEGER,
    NULLIF(product_weight_g, '')::NUMERIC,
    NULLIF(product_length_cm, '')::NUMERIC,
    NULLIF(product_height_cm, '')::NUMERIC,
    NULLIF(product_width_cm, '')::NUMERIC
FROM raw.products;


-- 4. Sellers
INSERT INTO core.sellers (
    seller_id,
    seller_zip_code_prefix,
    seller_city,
    seller_state
)
SELECT
    seller_id,
    seller_zip_code_prefix::INTEGER,
    seller_city,
    seller_state
FROM raw.sellers;


-- 5. Orders
INSERT INTO core.orders (
    order_id,
    customer_id,
    order_status,
    order_purchase_timestamp,
    order_approved_at,
    order_delivered_carrier_date,
    order_delivered_customer_date,
    order_estimated_delivery_date
)
SELECT
    order_id,
    customer_id,
    order_status,
    order_purchase_timestamp::TIMESTAMP,
    NULLIF(order_approved_at, '')::TIMESTAMP,
    NULLIF(order_delivered_carrier_date, '')::TIMESTAMP,
    NULLIF(order_delivered_customer_date, '')::TIMESTAMP,
    order_estimated_delivery_date::TIMESTAMP
FROM raw.orders;


-- 6. Order items
INSERT INTO core.order_items (
    order_id,
    order_item_id,
    product_id,
    seller_id,
    shipping_limit_date,
    price,
    freight_value
)
SELECT
    order_id,
    order_item_id::INTEGER,
    product_id,
    seller_id,
    shipping_limit_date::TIMESTAMP,
    price::NUMERIC(12, 2),
    freight_value::NUMERIC(12, 2)
FROM raw.order_items;


-- 7. Payments
INSERT INTO core.order_payments (
    order_id,
    payment_sequential,
    payment_type,
    payment_installments,
    payment_value
)
SELECT
    order_id,
    payment_sequential::INTEGER,
    payment_type,
    payment_installments::INTEGER,
    payment_value::NUMERIC(12, 2)
FROM raw.order_payments;


-- 8. Reviews
INSERT INTO core.order_reviews (
    review_id,
    order_id,
    review_score,
    review_comment_title,
    review_comment_message,
    review_creation_date,
    review_answer_timestamp
)
SELECT
    review_id,
    order_id,
    review_score::SMALLINT,
    NULLIF(review_comment_title, ''),
    NULLIF(review_comment_message, ''),
    review_creation_date::TIMESTAMP,
    review_answer_timestamp::TIMESTAMP
FROM raw.order_reviews;