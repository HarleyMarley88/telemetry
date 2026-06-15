CREATE KEYSPACE IF NOT EXISTS demo
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

USE demo;

CREATE TABLE IF NOT EXISTS tag_history_v2 (
    tag_name text,
    day text,
    ts timestamp,
    value double,
    PRIMARY KEY ((tag_name, day), ts)
    
) WITH CLUSTERING ORDER BY (ts DESC);