#!/bin/bash

echo "Название Deployment: telemetry-api"
read DEPLOYMENT_NAME


kubectl apply -f deployment.yml 
kubectl apply -f service.yml 
kubectl apply -f configmap.yml 
kubectl apply -f secret.yml 
kubectl apply -f cassandra-statefulset.yml
kubectl apply -f cassandra-service.yml
kubectl apply -f kafka-statefulset.yml
kubectl apply -f kafka-service.yml

kubectl rollout restart deployment telemetry-api -n telemetry
kubectl rollout restart statefulset cassandra -n telemetry
kubectl rollout restart statefulset kafka -n telemetry
echo "Готово!"
