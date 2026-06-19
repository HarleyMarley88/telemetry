from cassandra.cluster import Cluster
import os
session = None
CASSANDRA_HOST = os.getenv("CASSANDRA_HOST")
def get_session():
    global session

    if session is None:
        cluster = Cluster([CASSANDRA_HOST])
        session = cluster.connect()

    return session