#!/bin/bash

IMAGE_NAME="iso-builder"
CONTAINER_NAME="iso-builder-container"

if [ "$EUID" -ne 0 ]; then
  echo "Ce script doit être lancé avec sudo"
  exit 1
fi

echo "Construction de l'image Docker..."
docker build -t $IMAGE_NAME .

if [ "$(docker ps -aq -f name=$CONTAINER_NAME)" ]; then
    echo "Suppression de l'ancien conteneur..."
    docker rm -f $CONTAINER_NAME
fi

echo "Lancement du conteneur..."
docker run -it --name $CONTAINER_NAME $IMAGE_NAME
