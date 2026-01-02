#!/usr/bin/env bash
# Build script for IIMS System - Railway/Render/Production
# Exit on error
set -o errexit

echo "=========================================="
echo "🚀 IIMS System - Build Process Starting"
echo "=========================================="

# Display environment info
echo "📋 Environment Information:"
echo "   Python Version: $(python --version)"
echo "   Pip Version: $(pip --version)"
echo "   OS Type: $OSTYPE"
echo ""

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ Dependencies installed successfully"
echo ""

# Setup Tailwind CSS (if applicable)
echo "🎨 Setting up Tailwind CSS..."
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    if [ ! -f tailwindcss ]; then
        echo "   Downloading Tailwind CLI..."
        curl -sL https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-linux-x64 -o tailwindcss
        chmod +x tailwindcss
        echo "   ✅ Tailwind CLI downloaded"
    else
        echo "   ℹ️  Tailwind CLI already exists"
    fi
    
    # Check if input CSS exists
    if [ -f "./intelligence/static/css/input.css" ]; then
        echo "   Building CSS..."
        ./tailwindcss -i ./intelligence/static/css/input.css -o ./intelligence/static/css/output.css --minify
        echo "   ✅ CSS built successfully"
    else
        echo "   ⚠️  Input CSS not found, skipping Tailwind build"
    fi
else
    echo "   ℹ️  Skipping Tailwind build (Non-Linux environment)"
    echo "   💡 Ensure CSS is pre-built or use CDN fallback"
fi
echo ""

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --no-input --clear
echo "✅ Static files collected"
echo ""

echo "=========================================="
echo "✅ Build Process Completed Successfully!"
echo "=========================================="
