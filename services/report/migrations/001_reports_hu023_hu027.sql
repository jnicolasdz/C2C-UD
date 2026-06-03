-- Ejecutar solo si ya existe la tabla reports y no quieres borrar el volumen de la base de datos.
ALTER TABLE reports ADD COLUMN IF NOT EXISTS user_id VARCHAR(80);
ALTER TABLE reports ADD COLUMN IF NOT EXISTS send_status VARCHAR(50) DEFAULT 'PENDIENTE' NOT NULL;
ALTER TABLE reports ADD COLUMN IF NOT EXISTS delivery_message TEXT;
ALTER TABLE reports ADD COLUMN IF NOT EXISTS send_attempts INTEGER DEFAULT 0 NOT NULL;
ALTER TABLE reports ADD COLUMN IF NOT EXISTS retry_count INTEGER DEFAULT 0 NOT NULL;
ALTER TABLE reports ADD COLUMN IF NOT EXISTS last_send_attempt_at TIMESTAMPTZ;
ALTER TABLE reports ADD COLUMN IF NOT EXISTS is_deleted BOOLEAN DEFAULT false NOT NULL;
ALTER TABLE reports ADD COLUMN IF NOT EXISTS deleted_at TIMESTAMPTZ;

CREATE INDEX IF NOT EXISTS ix_reports_user_id ON reports(user_id);
CREATE INDEX IF NOT EXISTS ix_reports_user_email ON reports(user_email);
CREATE INDEX IF NOT EXISTS ix_reports_send_status ON reports(send_status);
CREATE INDEX IF NOT EXISTS ix_reports_is_deleted ON reports(is_deleted);
