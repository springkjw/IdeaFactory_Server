#! /bin/bash

{
    docker-compose down &&
    echo "Finish Down and Start Up"
} || {
    echo "Start Up"
}

docker-compose up -d --build
# docker-compose exec web python3 /home/ubuntu/src/manage.py migrate