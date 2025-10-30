  -- Recent sentiment trend
SELECT bucket, origin, avg_compound
    FROM sentiment_daily
    WHERE bucket > NOW() - INTERVAL '30 days'
    ORDER BY bucket DESC;

    -- Long-term sentiment comparison
SELECT bucket, origin, avg_compound
    FROM sentiment_daily
    WHERE bucket BETWEEN '2025-01-01' AND '2025-02-31'
    ORDER BY bucket;


SELECT * FROM articles   
    WHERE origin = 'source1'   
        AND published > NOW() - INTERVAL '7 days'  
    ORDER BY published DESC;

SELECT origin, bucket, avg_compound, positive_count  
    FROM sentiment_daily  
    WHERE bucket > NOW() - INTERVAL '30 days'  
      AND origin = 'source1'  
    ORDER BY bucket DESC;

    -- Monitor compression ratios  
SELECT * FROM chunk_compression_stats('articles');  
SELECT * FROM chunk_compression_stats('sentiments');  
  
  -- Check continuous aggregate refresh status  
SELECT * FROM timescaledb_information.jobs   
    WHERE proc_name = 'policy_refresh_continuous_aggregate';  
  
  -- Monitor chunk count and sizes  
SELECT * FROM timescaledb_information.chunks   
    WHERE hypertable_name IN ('articles', 'sentiments');

    
-- Verify hypertable creation, after data insert  
SELECT * FROM timescaledb_information.hypertables   
WHERE hypertable_name IN ('articles', 'sentiments');