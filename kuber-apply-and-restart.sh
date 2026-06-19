#!/bin/bash

echo "Название Deployment: telemetry-api"

kubectl apply -f deployment.yml 
kubectl apply -f service.yml 
kubectl apply -f configmap.yml 
kubectl apply -f secret.yml 
kubectl apply -f cassandra-statefulset.yml
kubectl apply -f cassandra-service.yml
kubectl apply -f kafka-statefulset.yml
kubectl apply -f kafka-service.yml


kubectl rollout restart statefulset cassandra -n telemetry
kubectl rollout restart statefulset kafka -n telemetry
kubectl rollout restart deployment telemetry-api -n telemetry

echo "Готово!"
