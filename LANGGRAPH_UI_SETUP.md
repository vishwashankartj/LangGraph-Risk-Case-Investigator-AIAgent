# LangGraph Studio UI Setup

## Quick Start

Your High-Risk Investigation Agent now has a visual chat UI!

### Option 1: Use the Official Web UI (Recommended)

1. **Start the LangGraph server:**
```bash
cd /Users/vishwashankarjanakiraman/High_Risk_Investigative_Agent
./start_ui_server.sh
```
(This script automatically uses the Python 3.11 virtual environment)

2. **Open the Agent Chat UI:**
- Visit: https://agentchat.vercel.app
- Enter these settings:
  - **Graph ID**: `investigation_agent`
  - **Deployment URL**: `http://localhost:2024`
  - **LangSmith API key**: (optional - leave blank for local use)

3. **Start investigating:**
- Type: "Investigate user USER123"
- Watch the agent nodes execute in real-time!

### Option 2: Local Development UI

```bash
# Create local UI (if you want custom ization)
npx create-agent-chat-app --project-name investigation-ui
cd investigation-ui
pnpm install
pnpm dev
```

## What You'll See

The UI will show:
- ✅ **Real-time node execution** (Triage → Analysis → Narrative → Decision)
- ✅ **Live data gathering** progress
- ✅ **Pattern detection** results
- ✅ **Risk scores** as they're calculated
- ✅ **Final recommendations** with justifications

## Configuration

Your `langgraph.json`:
```json
{
  "dependencies": ["."],
  "graphs": {
    "investigation_agent": "./src/graph.py:create_investigation_graph"
  },
  "env": ".env"
}
```

## Server Commands

```bash
# Start development server (auto-reload)
langgraph dev

# Start production server
langgraph start

# Check server status
langgraph status
```

## How to Use in Chat UI

**Example Prompts:**
- "Investigate user USER456"
- "Analyze account ACC789"
- "Check transaction TXN001"

The agent will automatically:
1. Gather data from all sources
2. Calculate risk score
3. Detect suspicious patterns
4. Generate investigation narrative
5. Provide final recommendation

## Troubleshooting

**Server won't start?**
- Make sure you're in the project directory
- Check that `.env` file exists
- Verify `langgraph-cli` is installed

**UI can't connect?**
- Ensure server is running on `http://localhost:2024`
- Check that graph ID matches: `investigation_agent`
- Try without LangSmith API key for local testing

## Next Steps

- **Customize the UI**: Fork the agent-chat-ui project
- **Add streaming**: See real-time token generation
- **Deploy**: Use LangSmith for cloud hosting

Enjoy your interactive investigation agent! 🕵️✨
