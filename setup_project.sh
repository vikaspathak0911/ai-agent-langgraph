#!/bin/bash

# Create main files
touch README.md
touch requirements.txt

# Create src directory and files
mkdir -p src
touch src/graph_basic.py
touch src/graph_enhanced.py
touch src/memory.py
touch src/tools.py

# Create data directory and memory.json
mkdir -p data
touch data/memory.json

# Create tests directory and test_cases.py
mkdir -p tests
touch tests/test_cases.py

echo "Directory structure created successfully!"
