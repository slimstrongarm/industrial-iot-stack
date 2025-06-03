#!/bin/bash
# Docker wrapper script for WSL + Claude Code compatibility
# This script allows Docker commands to work in WSL without WSL integration enabled
DOCKER_HOST=tcp://localhost:2375 "/mnt/c/Program Files/Docker/Docker/resources/bin/docker.exe" "$@"