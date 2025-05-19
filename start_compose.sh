#!/bin/bash

# Monitora todos os arquivos do projeto, exceto node_modules e .git
find . -type f ! -path "./node_modules/*" ! -path "./.git/*" | entr -r docker-compose up --build
