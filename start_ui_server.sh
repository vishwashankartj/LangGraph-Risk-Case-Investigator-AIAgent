#!/bin/bash

# Launch script for High-Risk Investigation Agent with LangGraph UI
# Compatible with Python 3.9+

echo "🕵️  Starting High-Risk Investigation Agent Server..."
echo ""
echo "📍 Server will run on: http://localhost:8000"
echo "🎨 Open the UI at: https://agentchat.vercel.app"
echo ""
echo "Settings for UI:"
echo "  - Graph ID: investigation_agent"
echo "  - Deployment URL: http://localhost:8000"
echo "  - LangSmith API Key: (leave blank)"
echo ""
echo "Starting server..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

cd "$(dirname "$0")"

# Activate Python 3.11 virtual environment
source venv_311/bin/activate

# Start the LangGraph development server
langgraph dev --port 2024

