from cassandra.cluster import Cluster
import os

CASSANDRA_HOST = os.getenv(
    "CASSANDRA_HOST",
    "host.docker.internal"
)

cluster = Cluster([CASSANDRA_HOST])
session = cluster.connect("demo")