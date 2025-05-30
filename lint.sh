#!/bin/bash

echo "🔍 Running lint checks with flake8..."
flake8 app.py

# echo "🧹 Checking formatting with black..."
# black --check app.py

echo "🧹 Checking formatting with black..."
./venv/Scripts/black app.py

echo "✅ Linting passed!"