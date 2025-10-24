#!/bin/bash
# Setup script for Next.js frontend template
# Run this after copying the template to your project

set -e

echo "🚀 Setting up Next.js frontend..."

# Check if we're in the frontend directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: package.json not found. Please run this script from the frontend directory."
    exit 1
fi

# Install dependencies
echo "📦 Installing npm dependencies..."
npm install

# Initialize shadcn/ui (if not already initialized)
if [ ! -d "components/ui" ] || [ -z "$(ls -A components/ui 2>/dev/null)" ]; then
    echo "🎨 Initializing shadcn/ui..."
    echo "Note: This will use the configuration from components.json"
    # The components.json is already configured, so we just need to add initial components
    npx shadcn-ui@latest add button card input label textarea --yes --overwrite
else
    echo "✅ shadcn/ui components already present"
fi

# Copy environment variables if needed
if [ ! -f ".env.local" ] && [ -f ".env.example" ]; then
    echo "📝 Creating .env.local from .env.example..."
    cp .env.example .env.local
    echo "⚠️  Please update .env.local with your actual API URL"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Update .env.local with your backend API URL"
echo "  2. Run 'npm run dev' to start the development server"
echo "  3. Open http://localhost:3000 in your browser"
echo ""
echo "To add more shadcn/ui components, run:"
echo "  bash ../scripts/add-component.sh <component-name>"
echo ""
