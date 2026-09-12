SELECT 
    o.id AS order_id,
    o.customer_name,
    o.customer_phone,
    o.status AS order_status,
    o.total_amount,
    p.name AS product_name,
    p.category,
    p.volume,
    oi.quantity,
    oi.unit_price,
    (oi.quantity * oi.unit_price) AS subtotal
FROM delivery.orders o
JOIN delivery.order_items oi ON o.id = oi.order_id
JOIN delivery.products p ON oi.product_id = p.id
ORDER BY o.created_at DESC;

SELECT 
    o.id AS order_id,
    o.customer_name,
    p.name AS product_name,
    oi.quantity,
    oi.unit_price,
    o.total_amount
FROM delivery.orders o
JOIN delivery.order_items oi ON o.id = oi.order_id
JOIN delivery.products p ON oi.product_id = p.id
WHERE o.id = 'SEU_ID_HEXADECIMAL_AQUI';

