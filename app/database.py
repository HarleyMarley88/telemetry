from cassandra.cluster import Cluster

session = None

def get_session():
    global session

    if session is None:
        cluster = Cluster(["cassandra"])
        session = cluster.connect()

    return session