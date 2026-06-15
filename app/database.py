from cassandra.cluster import Cluster



cluster = Cluster(["cassandra"])
session = cluster.connect("demo")