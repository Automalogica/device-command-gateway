-- ── Inicialização do banco — Plataforma de Comando de Câmeras ──────────────

CREATE TYPE command_status AS ENUM (
    'PENDING',
    'PROCESSING',
    'DONE',
    'ERROR',
    'DLQ'
);

CREATE TABLE IF NOT EXISTS camera_commands (
    id              BIGSERIAL           PRIMARY KEY,
    request_id      VARCHAR(100)        NOT NULL UNIQUE,  -- ex: lucas_20260610143022847
    camera_id       VARCHAR(100)        NOT NULL,
    command         VARCHAR(50)         NOT NULL,
    params          TEXT,
    status          command_status      NOT NULL DEFAULT 'PENDING',
    retry_count     SMALLINT            NOT NULL DEFAULT 0,
    error_message   TEXT,
    created_at      TIMESTAMPTZ         NOT NULL DEFAULT NOW(),
    started_at      TIMESTAMPTZ,
    finished_at     TIMESTAMPTZ
);

-- Índice para o poll dos workers: busca rápida por PENDING ordenado por chegada
CREATE INDEX idx_camera_commands_pending
    ON camera_commands (status, created_at)
    WHERE status = 'PENDING';

-- Índice para consultas por request_id (correlação nos logs)
CREATE INDEX idx_camera_commands_request_id
    ON camera_commands (request_id);

-- Índice para consultas por câmera (monitoramento de erros por device)
CREATE INDEX idx_camera_commands_camera_id
    ON camera_commands (camera_id, created_at DESC);