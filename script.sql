CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TYPE report_status AS ENUM ('pending', 'processed', 'reject');
CREATE TYPE bug_type AS ENUM ('rota', 'visual', 'conexao', 'report', 'outro');


CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    telefone VARCHAR(11) UNIQUE NOT NULL,
    cpf VARCHAR(11) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    icon INTEGER,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);


CREATE TABLE street_segment (
    segment_id BIGSERIAL PRIMARY KEY,
    osm_id BIGINT UNIQUE,
    name VARCHAR(255) NOT NULL,
    geom geometry(LineString, 4326),
    avg_risk_score NUMERIC,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);


CREATE TABLE reports (
    report_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(user_id),
    location geometry(Point, 4326) NOT NULL,
    street_segment_id BIGINT REFERENCES street_segment(segment_id),
    data_image DATE,
    image_path VARCHAR(255),
    risk_score FLOAT,
    comentario_v VARCHAR(255),
    nota_v INTEGER,
    comentario_a VARCHAR(255),
    nota_a INTEGER,
    comentario_t VARCHAR(255),
    nota_t INTEGER,
    comentario_m VARCHAR(255),
    nota_m INTEGER,
    comentario_al VARCHAR(255),
    nota_al INTEGER,
    comentario_s VARCHAR(255),
    nota_s INTEGER,
    user_rating INTEGER,
    report_status report_status NOT NULL DEFAULT 'pending',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);


CREATE OR REPLACE FUNCTION atualizar_media_risk_score()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO street_segment (segment_id, updated_at, avg_risk_score)
    VALUES (NEW.street_segment_id, NOW(), 
        (SELECT AVG(risk_score) FROM reports WHERE street_segment_id = NEW.street_segment_id))
    ON CONFLICT (segment_id) DO UPDATE
    SET avg_risk_score = EXCLUDED.avg_risk_score,
        updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER atualizar_media_risk_score
AFTER INSERT OR UPDATE ON reports
FOR EACH ROW
EXECUTE FUNCTION atualizar_media_risk_score();


CREATE TABLE bug_report (
    bug_report_id BIGSERIAL PRIMARY KEY,
    user_id UUID REFERENCES users(user_id),
    name VARCHAR(255) NOT NULL,
    bug_type bug_type NOT NULL DEFAULT 'outro',
    descricao VARCHAR(255),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);


CREATE TABLE bug_images_report (
    bug_report_image_id BIGSERIAL PRIMARY KEY,
    bug_report_id BIGINT REFERENCES bug_report(bug_report_id),
    imagem TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);


CREATE TABLE route_rating (
    route_rating_id BIGSERIAL PRIMARY KEY,
    user_id UUID REFERENCES users(user_id),
    trip_shape TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
