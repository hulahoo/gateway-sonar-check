#! /bin/sh

echo "Start executing migrations..."
python3 src/apps/models/migrations.py

echo "Start receiving messages..."
python3 main.py