#!/bin/bash
# Docker Compose wrapper script for WSL + Claude Code compatibility
# This script allows docker-compose commands to work in WSL without WSL integration enabled
DOCKER_HOST=tcp://localhost:2375 "/mnt/c/Program Files/Docker/Docker/resources/bin/docker-compose.exe" "$@"