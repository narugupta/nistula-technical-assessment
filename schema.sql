-- =====================================================
-- Nistula Unified Messaging Platform Schema
-- =====================================================
--
-- This schema supports:
-- - Unified guest messaging across channels
-- - AI-assisted hospitality workflows
-- - Escalation management
-- - Operational analytics
-- - Future multi-tenant SaaS scalability
--
-- =====================================================


-- =====================================================
-- GUESTS
-- =====================================================
--
-- Canonical guest profiles across channels.
-- external_guest_ref currently uses a lightweight
-- source-prefixed identity approach.
--
CREATE TABLE guests (

    id SERIAL PRIMARY KEY,

    tenant_id VARCHAR(255) NOT NULL,

    guest_name VARCHAR(255) NOT NULL,

    external_guest_ref VARCHAR(255) NOT NULL
);


-- =====================================================
-- CHANNEL IDENTITIES
-- =====================================================
--
-- Links guests to platform-specific identities.
-- This enables future identity resolution logic.
--
CREATE TABLE channel_identities (

    id SERIAL PRIMARY KEY,

    guest_id INTEGER NOT NULL
        REFERENCES guests(id),

    source VARCHAR(50) NOT NULL,

    external_user_id VARCHAR(255) NOT NULL
);


-- =====================================================
-- GUEST PROFILES
-- =====================================================
--
-- Stores operational guest metadata and preferences.
--
CREATE TABLE guest_profiles (

    id SERIAL PRIMARY KEY,

    guest_id INTEGER NOT NULL
        REFERENCES guests(id),

    total_conversations INTEGER DEFAULT 0,

    total_messages INTEGER DEFAULT 0,

    preferred_channel VARCHAR(50),

    last_seen_at TIMESTAMP,

    guest_preferences TEXT
);


-- =====================================================
-- CONVERSATIONS
-- =====================================================
--
-- Conversations behave like message threads.
-- Multiple guest messages can belong to the
-- same conversation lifecycle.
--
CREATE TABLE conversations (

    id SERIAL PRIMARY KEY,

    tenant_id VARCHAR(255) NOT NULL,

    guest_id INTEGER NOT NULL
        REFERENCES guests(id),

    source VARCHAR(50) NOT NULL,

    property_id VARCHAR(255) NOT NULL,

    booking_ref VARCHAR(255),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- =====================================================
-- MESSAGES
-- =====================================================
--
-- Central unified messaging table.
-- Stores inbound messages, AI responses,
-- workflow actions, and operational metadata.
--
CREATE TABLE messages (

    id SERIAL PRIMARY KEY,

    message_id UUID NOT NULL UNIQUE,

    tenant_id VARCHAR(255) NOT NULL,

    conversation_id INTEGER NOT NULL
        REFERENCES conversations(id),

    guest_name VARCHAR(255) NOT NULL,

    message_text TEXT NOT NULL,

    query_type VARCHAR(100),

    confidence_score FLOAT DEFAULT 0.0,

    ai_generated BOOLEAN DEFAULT FALSE,

    agent_edited BOOLEAN DEFAULT FALSE,

    sent_via VARCHAR(50),

    ai_reply_text TEXT,

    action VARCHAR(50),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- =====================================================
-- MESSAGE EVENTS
-- =====================================================
--
-- Tracks message lifecycle events.
-- Useful for auditability and debugging.
--
CREATE TABLE message_events (

    id SERIAL PRIMARY KEY,

    message_id INTEGER NOT NULL
        REFERENCES messages(id),

    event_type VARCHAR(100) NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- =====================================================
-- AGENTS
-- =====================================================
--
-- Internal operations agents handling escalations.
--
CREATE TABLE agents (

    id SERIAL PRIMARY KEY,

    full_name VARCHAR(255) NOT NULL,

    email VARCHAR(255),

    active BOOLEAN DEFAULT TRUE
);


-- =====================================================
-- ESCALATIONS
-- =====================================================
--
-- Messages requiring human intervention
-- are routed into escalation workflows.
--
CREATE TABLE escalations (

    id SERIAL PRIMARY KEY,

    message_id INTEGER NOT NULL
        REFERENCES messages(id),

    assigned_agent_id INTEGER
        REFERENCES agents(id),

    severity VARCHAR(50),

    escalation_reason TEXT,

    status VARCHAR(50) DEFAULT 'open',

    sla_deadline TIMESTAMP,

    resolved BOOLEAN DEFAULT FALSE,

    escalation_notes TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- =====================================================
-- FAILED EVENTS
-- =====================================================
--
-- Dead-letter style operational table for
-- failed workflow processing attempts.
--
CREATE TABLE failed_events (

    id SERIAL PRIMARY KEY,

    event_type VARCHAR(100),

    payload TEXT,

    failure_reason TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- =====================================================
-- PROCESSING METRICS
-- =====================================================
--
-- Tracks AI orchestration performance
-- and operational observability metrics.
--
CREATE TABLE processing_metrics (

    id SERIAL PRIMARY KEY,

    message_id INTEGER
        REFERENCES messages(id),

    ai_latency_ms FLOAT,

    confidence_score FLOAT,

    action VARCHAR(50),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- =====================================================
-- DESIGN DECISIONS
-- =====================================================
--
-- 1. Guest identities are separated from
--    channel-specific identities to support
--    future cross-platform identity resolution.
--
-- 2. Conversations are modeled as reusable
--    threads instead of creating a new
--    conversation for every message.
--
-- 3. AI workflow metadata such as
--    confidence_score, sent_via,
--    agent_edited, and action are stored
--    directly on messages for operational
--    observability and auditability.
--
-- 4. tenant_id fields were included to
--    support future multi-tenant SaaS
--    scalability for multiple villa operators.
--


-- =====================================================
-- HARDEST DESIGN DECISION
-- =====================================================
--
-- The hardest design decision was guest
-- identity resolution across multiple channels.
--
-- In hospitality systems, the same guest may
-- interact through WhatsApp, Instagram,
-- Booking.com, Airbnb, or direct inquiries
-- using slightly different names or identifiers.
--
-- A naive schema can easily create duplicate
-- guest records and fragmented conversation
-- history.
--
-- To address this, the schema separates
-- canonical guest records from channel-specific
-- identities using a dedicated
-- channel_identities table.
--
-- This design allows future support for
-- advanced identity matching strategies
-- without redesigning the core schema.
--
-- Another important decision was modeling
-- conversations as reusable threads rather
-- than creating a new conversation per
-- inbound message.
-- =====================================================