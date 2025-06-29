# Connected Agents: Routing Agent + Specialized Agents

This project connects the **Routing Agent** with two pre-built specialized agents:
- **Academic Research Agent** - for academic research and literature analysis
- **FOMC Research Agent** - for Federal Reserve meeting analysis

## 🏗️ **Project Structure**

```
backend/
├── academic-research/          # Academic Research Agent (pre-built)
│   ├── academic_research/
│   │   ├── agent.py           # academic_coordinator (LlmAgent)
│   │   └── sub_agents/
├── fomc-research/             # FOMC Research Agent (pre-built)
│   ├── fomc_research/
│   │   ├── agent.py           # root_agent (Agent)
│   │   └── sub_agents/
└── routing-agent/             # Routing Agent (connects the above)
    ├── routing_agent/
    │   ├── agent.py           # routing_agent (LlmAgent)
    │   ├── prompt.py          # Routing logic
    │   └── __init__.py
    ├── setup_connected_agents.py  # Setup script
    ├── test_connection.py     # Connection test
    └── pyproject.toml         # Dependencies
```

## 🚀 **Quick Start**

### **1. Setup the Connected Agents**

```bash
# Navigate to the routing agent directory
cd backend/routing-agent

# Run the setup script
python setup_connected_agents.py --project-id YOUR_PROJECT_ID --location us-central1
```

### **2. Test the Connection**

```bash
# Test that all agents can be imported
python test_connection.py
```

### **3. Run the Routing Agent**

```bash
# Activate the virtual environment
poetry shell

# Run the routing agent
adk run routing_agent
```

## 🎯 **How It Works**

### **Before (Separate Agents)**
```
User → Academic Research Agent (for academic queries)
User → FOMC Research Agent (for financial queries)
```

### **After (Connected via Routing Agent)**
```
User → Routing Agent → [Analyzes Query] → Academic Research Agent
                    → [Analyzes Query] → FOMC Research Agent
```

## 📋 **Example Interactions**

### **Academic Research Queries**
```
User: "I need help analyzing this research paper on machine learning"

Routing Agent: I'll route this to the Academic Research Agent since you're asking about analyzing a research paper. This agent specializes in academic literature analysis and can help you understand the paper's contributions, find related research, and suggest future directions.

[Automatically calls Academic Research Agent]
```

### **FOMC Research Queries**
```
User: "What was the impact of the latest Fed meeting on markets?"

Routing Agent: I'll route this to the FOMC Research Agent since you're asking about Federal Reserve meetings and market impact. This agent specializes in analyzing FOMC meetings, statements, and their financial market implications.

[Automatically calls FOMC Research Agent]
```

### **Ambiguous Queries**
```
User: "I want to analyze economic policy"

Routing Agent: I need to clarify what type of economic policy analysis you're looking for. Are you:
1. Analyzing academic research papers about economic policy (Academic Research Agent)
2. Analyzing current Federal Reserve policy decisions and their market impact (FOMC Research Agent)

Please provide more context so I can route you to the most appropriate agent.
```

## 🔧 **Setup Details**

### **Prerequisites**
- Python 3.9+
- Poetry
- Google Cloud CLI
- Google Cloud Project with Vertex AI enabled

### **Environment Variables**
The setup script creates a `.env` file with:
```bash
GOOGLE_GENAI_USE_VERTEXAI=true
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
```

### **Dependencies**
The routing agent automatically imports the specialized agents by:
1. Adding their directories to `sys.path`
2. Importing their main agents as tools
3. Making them available for routing

## 🧪 **Testing**

### **Test Connection**
```bash
python test_connection.py
```

Expected output:
```
🚀 Testing Routing Agent Connection
==================================================
📁 Current Directory Structure:
==============================
Current directory: /path/to/backend/routing-agent
Backend directory: /path/to/backend

Academic Research: ✅ /path/to/backend/academic-research
  Academic agent.py: ✅ /path/to/backend/academic-research/academic_research/academic_research/agent.py
FOMC Research: ✅ /path/to/backend/fomc-research
  FOMC agent.py: ✅ /path/to/backend/fomc-research/fomc_research/fomc_research/agent.py

🧪 Testing Agent Connection...
==================================================
1. Testing routing agent import...
   ✅ Routing agent imported successfully

2. Testing specialized agents availability...
   ✅ Specialized agents are available

3. Testing Academic Research Agent...
   ✅ Academic Research Agent imported successfully
   📋 Agent name: academic_coordinator
   📋 Agent description: analyzing seminal papers provided by the users...

4. Testing FOMC Research Agent...
   ✅ FOMC Research Agent imported successfully
   📋 Agent name: root_agent
   📋 Agent description: Use tools and other agents provided to generate an analysis report...

5. Testing routing agent tools...
   📋 Number of tools available: 2
   📋 Tool 1: academic_coordinator
   📋 Tool 2: root_agent

==================================================
✅ Connection test completed!

🎯 Ready to use! You can now:
1. Run: adk run routing_agent
2. Ask academic questions: 'I need help analyzing this research paper'
3. Ask FOMC questions: 'What was the impact of the latest Fed meeting?'
```

## 🛠 **Troubleshooting**

### **Import Errors**
If you get import errors:
```bash
# Make sure you're in the right directory
cd backend/routing-agent

# Check if specialized agents exist
ls ../academic-research/
ls ../fomc-research/

# Re-run setup
python setup_connected_agents.py --project-id YOUR_PROJECT_ID
```

### **Agent Not Found**
If agents are not found:
```bash
# Check the directory structure
python test_connection.py

# The script will show you exactly what's missing
```

### **Authentication Issues**
```bash
# Authenticate with Google Cloud
gcloud auth application-default login
gcloud auth application-default set-quota-project YOUR_PROJECT_ID

# Enable required APIs
gcloud services enable aiplatform.googleapis.com
gcloud services enable agentengine.googleapis.com
```

## 🎨 **Customization**

### **Adding New Specialized Agents**
1. Add the new agent directory to `backend/`
2. Update the import logic in `routing_agent/agent.py`
3. Add routing logic in `routing_agent/prompt.py`
4. Update the setup script

### **Modifying Routing Logic**
Edit `routing_agent/prompt.py` to:
- Add new keywords
- Modify decision framework
- Include additional examples

## 📚 **Agent Capabilities**

### **Academic Research Agent**
- Analyze seminal papers
- Find citing papers
- Generate research directions
- Literature reviews
- Academic writing assistance

### **FOMC Research Agent**
- FOMC meeting analysis
- Statement comparisons
- Market impact analysis
- Rate change predictions
- Economic policy analysis

## 🚀 **Deployment**

### **Local Development**
```bash
cd backend/routing-agent
poetry shell
adk run routing_agent
```

### **Production Deployment**
```bash
# Deploy to Google Agent Engine
python deployment/deploy.py --project-id YOUR_PROJECT_ID --location us-central1
```

## 📞 **Support**

If you encounter issues:
1. Run `python test_connection.py` to diagnose
2. Check the setup logs
3. Verify Google Cloud credentials
4. Ensure all agents are properly installed

The routing agent provides a seamless experience where you only need to interact with one agent, and it automatically routes your requests to the most appropriate specialized agent based on your query content. 