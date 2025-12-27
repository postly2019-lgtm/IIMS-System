#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Setting up Tailwind CSS..."
# Check if we are in a build environment that supports linux binary
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    if [ ! -f tailwindcss ]; then
        echo "Downloading Tailwind CLI..."
        curl -sL https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-linux-x64 -o tailwindcss
        chmod +x tailwindcss
    fi
    
    echo "Building CSS..."
    ./tailwindcss -i ./intelligence/static/css/input.css -o ./intelligence/static/css/output.css --minify
else
    echo "Skipping Tailwind build (Non-Linux environment). Ensure CSS is built or use CDN fallback."
fi

echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Running migrations..."
python manage.py migrate
