#!/bin/bash
docker system prune -a
docker build -t sdf .
