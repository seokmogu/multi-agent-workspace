#!/bin/bash
# Helper script to add shadcn/ui components

set -e

if [ -z "$1" ]; then
    echo "Usage: bash add-component.sh <component-name>"
    echo ""
    echo "Examples:"
    echo "  bash add-component.sh dialog"
    echo "  bash add-component.sh table"
    echo "  bash add-component.sh toast"
    echo ""
    echo "Available components:"
    echo "  button, card, input, label, textarea, select, dialog,"
    echo "  dropdown-menu, tabs, table, toast, alert-dialog, etc."
    echo ""
    echo "See https://ui.shadcn.com/docs/components for full list"
    exit 1
fi

COMPONENT=$1

echo "📦 Adding shadcn/ui component: $COMPONENT"

# Change to frontend directory if not already there
if [ ! -f "package.json" ]; then
    if [ -d "frontend" ]; then
        cd frontend
    else
        echo "❌ Error: Not in frontend directory and frontend/ not found"
        exit 1
    fi
fi

npx shadcn-ui@latest add $COMPONENT --yes

echo "✅ Component '$COMPONENT' added successfully!"
echo ""
echo "Import it in your components:"
echo "  import { ComponentName } from '@/components/ui/$COMPONENT'"
