CREATE SCHEMA IF NOT EXISTS delivery;


-- =========================================================
-- SEQUENCES
-- =========================================================

CREATE SEQUENCE IF NOT EXISTS delivery.products_id_seq;

CREATE SEQUENCE IF NOT EXISTS delivery.orders_id_seq;

CREATE SEQUENCE IF NOT EXISTS delivery.order_items_id_seq;

CREATE SEQUENCE IF NOT EXISTS delivery.order_approvals_id_seq;

CREATE SEQUENCE IF NOT EXISTS delivery.messages_id_seq;

CREATE SEQUENCE IF NOT EXISTS delivery.chat_message_history_id_seq;

CREATE SEQUENCE IF NOT EXISTS delivery.conversation_logs_id_seq;


-- =========================================================
-- CUSTOMER SESSIONS
-- =========================================================

CREATE TABLE IF NOT EXISTS delivery.customer_sessions (
    customer_phone VARCHAR(50) NOT NULL,
    customer_name VARCHAR(100),
    address VARCHAR(255),
    payment_method VARCHAR(50),
    cash_received NUMERIC(10,2),
    items JSONB DEFAULT '[]'::jsonb,
    state VARCHAR(50) NOT NULL DEFAULT 'IDLE'::character varying,
    session_data JSONB DEFAULT '{}'::jsonb,
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT customer_sessions_pkey PRIMARY KEY (customer_phone)
);


-- =========================================================
-- PRODUCTS
-- =========================================================

CREATE TABLE IF NOT EXISTS delivery.products (
    id INTEGER NOT NULL DEFAULT nextval('delivery.products_id_seq'::regclass),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    category VARCHAR(50) NOT NULL,
    volume VARCHAR(20) NOT NULL,
    price NUMERIC(10,2) NOT NULL,
    stock_quantity INTEGER NOT NULL DEFAULT 0,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT products_pkey PRIMARY KEY (id)
);


-- =========================================================
-- ORDERS
-- =========================================================

CREATE TABLE IF NOT EXISTS delivery.orders (
    id VARCHAR(20) NOT NULL,
    customer_name VARCHAR(100) NOT NULL,
    customer_phone VARCHAR(30) NOT NULL,
    address TEXT NOT NULL,
    delivery_fee NUMERIC(10,2) NOT NULL DEFAULT 5.00,
    total_amount NUMERIC(10,2) NOT NULL,
    payment_method VARCHAR(20) NOT NULL,
    cash_received NUMERIC(10,2),
    change_due NUMERIC(10,2),
    status VARCHAR(30) NOT NULL DEFAULT 'PENDING_APPROVAL'::character varying,
    approved_notified BOOLEAN DEFAULT false,
    delivery_notified BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT orders_pkey PRIMARY KEY (id)
);


-- =========================================================
-- ORDER ITEMS
-- =========================================================

CREATE TABLE IF NOT EXISTS delivery.order_items (
    id INTEGER NOT NULL DEFAULT nextval('delivery.order_items_id_seq'::regclass),
    order_id VARCHAR(20),
    product_id INTEGER,
    quantity INTEGER NOT NULL,
    unit_price NUMERIC(10,2) NOT NULL,
    CONSTRAINT order_items_pkey PRIMARY KEY (id),
    CONSTRAINT order_items_order_id_fkey
        FOREIGN KEY (order_id)
        REFERENCES delivery.orders(id)
        ON DELETE CASCADE,
    CONSTRAINT order_items_product_id_fkey
        FOREIGN KEY (product_id)
        REFERENCES delivery.products(id)
);


-- =========================================================
-- ORDER APPROVALS
-- =========================================================

CREATE TABLE IF NOT EXISTS delivery.order_approvals (
    id INTEGER NOT NULL DEFAULT nextval('delivery.order_approvals_id_seq'::regclass),
    order_id VARCHAR(20),
    approver_name VARCHAR(100) NOT NULL,
    action VARCHAR(20) NOT NULL,
    rejection_reason TEXT,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT order_approvals_pkey PRIMARY KEY (id),
    CONSTRAINT order_approvals_order_id_fkey
        FOREIGN KEY (order_id)
        REFERENCES delivery.orders(id)
        ON DELETE CASCADE
);


-- =========================================================
-- MESSAGES
-- =========================================================

CREATE TABLE IF NOT EXISTS delivery.messages (
    id INTEGER NOT NULL DEFAULT nextval('delivery.messages_id_seq'::regclass),
    customer_phone VARCHAR(50) NOT NULL,
    sender VARCHAR(20) NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    order_id VARCHAR(255),
    CONSTRAINT messages_pkey PRIMARY KEY (id),
    CONSTRAINT messages_order_id_fkey
        FOREIGN KEY (order_id)
        REFERENCES delivery.orders(id)
        ON DELETE SET NULL
);


-- =========================================================
-- CHAT MESSAGE HISTORY
-- =========================================================

CREATE TABLE IF NOT EXISTS delivery.chat_message_history (
    id INTEGER NOT NULL DEFAULT nextval('delivery.chat_message_history_id_seq'::regclass),
    customer_phone VARCHAR(30) NOT NULL,
    sender_type VARCHAR(20) NOT NULL,
    raw_message TEXT NOT NULL,
    detected_intentions JSONB,
    extracted_entities JSONB,
    order_id VARCHAR(20),
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chat_message_history_pkey PRIMARY KEY (id),
    CONSTRAINT chat_message_history_order_id_fkey
        FOREIGN KEY (order_id)
        REFERENCES delivery.orders(id)
        ON DELETE SET NULL
);


-- =========================================================
-- CONVERSATION LOGS
-- =========================================================

CREATE TABLE IF NOT EXISTS delivery.conversation_logs (
    id INTEGER NOT NULL DEFAULT nextval('delivery.conversation_logs_id_seq'::regclass),
    customer_phone VARCHAR(30) NOT NULL,
    raw_message TEXT NOT NULL,
    detected_intentions JSONB,
    extracted_entities JSONB,
    order_id VARCHAR(20),
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT conversation_logs_pkey PRIMARY KEY (id),
    CONSTRAINT conversation_logs_order_id_fkey
        FOREIGN KEY (order_id)
        REFERENCES delivery.orders(id)
        ON DELETE SET NULL
);


-- =========================================================
-- INDEXES
-- =========================================================

CREATE INDEX IF NOT EXISTS idx_messages_customer_phone
    ON delivery.messages USING btree (customer_phone);

CREATE INDEX IF NOT EXISTS idx_messages_order_id
    ON delivery.messages USING btree (order_id);

CREATE INDEX IF NOT EXISTS idx_chat_history_phone_created
    ON delivery.chat_message_history
    USING btree (customer_phone, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_orders_status
    ON delivery.orders USING btree (status);

CREATE INDEX IF NOT EXISTS search_idx
    ON delivery.products
    USING gin (
        to_tsvector(
            'portuguese'::regconfig,
            (
                (
                    COALESCE(name, ''::character varying)::text
                    || ' '::text
                )
                || COALESCE(description, ''::text)
            )
        )
    );


-- =========================================================
-- AJUSTE DAS SEQUENCES
-- =========================================================

ALTER SEQUENCE delivery.products_id_seq
    OWNED BY delivery.products.id;

ALTER SEQUENCE delivery.order_items_id_seq
    OWNED BY delivery.order_items.id;

ALTER SEQUENCE delivery.order_approvals_id_seq
    OWNED BY delivery.order_approvals.id;

ALTER SEQUENCE delivery.messages_id_seq
    OWNED BY delivery.messages.id;

ALTER SEQUENCE delivery.chat_message_history_id_seq
    OWNED BY delivery.chat_message_history.id;

ALTER SEQUENCE delivery.conversation_logs_id_seq
    OWNED BY delivery.conversation_logs.id;
