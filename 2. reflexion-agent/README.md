# Reflexion Agent

A LangGraph-based reflection agent that implements a generate-reflect cycle for creating and refining content using StateGraph for flexible state management.

## Project Setup from Scratch

Follow these steps to initialize and set up the project from scratch:

### 1. Initialize Project with uv

```bash
# Initialize a new Python project
uv init

# Add all required dependencies  
uv add python-dotenv black isort langchain langchain-openai langchain-tavily langgraph grandalf
```

### 2. Create Environment Files

Create the environment template file:

```bash
# Create .env_template
cat > .env_template << 'EOF'
# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Optional: LangSmith Tracing (for debugging)
LANGCHAIN_TRACING_V2=false
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=your_langsmith_api_key_here
LANGCHAIN_PROJECT=reflexion-agent

# Tavily key
TAVILY_API_KEY=your_tavily_api_key_here
EOF
```

Copy the template to create your actual environment file:

```bash
cp .env_template .env
```

Open the `.env` file in your editor and add your OpenAI API key:

```
OPENAI_API_KEY="sk-..."
```

### 3. Activate Virtual Environment

```bash
# Activate the virtual environment created by uv init
source .venv/bin/activate
```

### 4. Configure IDE Python Interpreter

To ensure your IDE uses the correct Python environment:

**For VS Code:**
1. Open Command Palette: `Shift+Cmd+P` (Mac) or `Ctrl+Shift+P` (Windows/Linux)
2. Select `Python: Select Interpreter`
3. Choose `Enter interpreter path...`
4. Enter the absolute path to your virtual environment:
   ```
   /absolute/path/to/your/project/2. reflexion-agent/.venv/bin/python
   ```

**Example path:**
```
/Users/yourusername/Projects/python/my-langgraph/2. reflexion-agent/.venv/bin/python
```

This ensures your IDE can:
- Load environment variables from `.env` file
- Use the correct Python interpreter with installed dependencies
- Provide proper code completion and debugging

## Project Structure

After setup, your project should have:

- `main.py`: The main entry point for running the agent
- `chains.py`: LangChain Expression Language (LCEL) chains for generation and reflection
- `schemas.py`: Pydantic models for structured outputs (AnswerQuestion, RevisedAnswer, Reflection)
- `tool_executor.py`: Tool execution logic for Tavily search integration
- `diagram.mmd`: Mermaid diagram showing the agent flow
- `pyproject.toml`: Project dependencies managed by uv
- `.env_template`: Template for environment variables
- `.env`: Your actual environment variables (not committed to git)

## Architecture

This project implements:

- **StateGraph**: Custom state management using TypedDict for agent orchestration
- **First Responder Node**: Creates initial research responses (~250 words) with built-in reflection
- **Tool Execution Node**: Runs Tavily search queries to gather additional information
- **Revisor Node**: Refines answers using search results and adds citations
- **Conditional Logic**: Controls flow between research and revision cycles
- **Structured Outputs**: Uses Pydantic models for consistent response formatting

## Development

### Code Formatting

Format your code using the included tools:

```bash
black .
isort .
```

### Running the Application

```bash
# Run using uv (recommended)
uv run python main.py

# Or activate virtual environment and run
source .venv/bin/activate
python main.py
```

The application will execute a research workflow on AI-powered SOC startups, showing progress indicators as it:
1. Generates an initial draft response with self-critique
2. Executes web searches using Tavily API
3. Revises the response with search results and citations
4. Repeats the research cycle up to 2 iterations for quality improvement

## Example Output

The agent processes complex research questions and provides structured outputs with:
- Initial draft answer (~250 words)
- Self-reflection identifying missing/superfluous content
- Search queries for additional research
- Revised answer with citations and references
- Progress tracking through each iteration

## Dependencies

- `langchain`: LLM framework and core components
- `langchain-openai`: OpenAI GPT model integration
- `langchain-tavily`: Tavily search API integration for research
- `langgraph`: Graph-based agent framework for state management
- `python-dotenv`: Environment variable management
- `grandalf`: Graph visualization and layout algorithms
- `black`, `isort`: Code formatting tools