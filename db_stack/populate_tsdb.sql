CREATE TABLE articles (
        hash TEXT NOT NULL,
        published TIMESTAMPTZ NOT NULL,
        origin TEXT,

        author TEXT,
        title TEXT,
        url TEXT,
        text TEXT,

        PRIMARY KEY (hash)
    );

CREATE TYPE finbert_score_enum AS ENUM ('positive', 'neutral', 'negative');

CREATE TABLE sentiments (
        hash TEXT NOT NULL,
        published TIMESTAMPTZ NOT NULL,
        origin TEXT,

        finbert_score finbert_score_enum,
        neg DOUBLE PRECISION,
        neu DOUBLE PRECISION,
        pos DOUBLE PRECISION,
        compound DOUBLE PRECISION,
        pos_count INTEGER,
        neg_count INTEGER,
        sentiment_m2 DOUBLE PRECISION,

        PRIMARY KEY (hash),
        UNIQUE (hash), 
        FOREIGN KEY (hash) REFERENCES articles(hash)
    );


SELECT create_hypertable(
       'articles',
       'published',
       chunk_time_interval => INTERVAL '7 days'
    );

SELECT create_hypertable(
       'sentiments',
       'published',
       chunk_time_interval => INTERVAL '7 days'
    );


CREATE INDEX idx_articles_origin_published ON articles (origin, published DESC);
CREATE INDEX idx_sentiments_origin_published ON sentiments (origin, published DESC);

ALTER TABLE articles SET (
        timescaledb.compress,
        timescaledb.compress_segmentby = 'origin',
        timescaledb.compress_orderby = 'published DESC'
    );

SELECT add_compression_policy('articles',
        compress_after => INTERVAL '30 days');

ALTER TABLE sentiments SET (
        timescaledb.compress,
        timescaledb.compress_segmentby = 'origin',
        timescaledb.compress_orderby = 'published DESC'
    );

SELECT add_compression_policy('sentiments',
        compress_after => INTERVAL '30 days');



CREATE MATERIALIZED VIEW sentiment_daily
    WITH (timescaledb.continuous) AS
    SELECT
        time_bucket('1 day', published) AS bucket,
        origin,
        COUNT(*) as article_count,
        COUNT(*) FILTER (WHERE finbert_score = 'positive') as positive_count,  
        COUNT(*) FILTER (WHERE finbert_score = 'neutral') as neutral_count,  
        COUNT(*) FILTER (WHERE finbert_score = 'negative') as negative_count, 
        AVG(compound) as avg_compound,
        AVG(pos) as avg_pos,
        AVG(neg) as avg_neg,
        AVG(neu) as avg_neu,
        STDDEV(compound) as stddev_compound
    FROM sentiments
    GROUP BY bucket, origin;

SELECT add_continuous_aggregate_policy('sentiment_daily',
        start_offset => INTERVAL '3 days',
        end_offset => INTERVAL '1 hour', 
        schedule_interval => INTERVAL '1 hour');

CREATE INDEX idx_sentiment_daily_origin_bucket ON sentiment_daily (origin, bucket DESC);

ALTER MATERIALIZED VIEW sentiment_daily SET (  
    timescaledb.compress,  
    timescaledb.compress_segmentby = 'origin',  
    timescaledb.compress_orderby = 'bucket DESC'  
);  
  
SELECT add_compression_policy('sentiment_daily',  
    compress_after => INTERVAL '7 days');




