# Reflexion Agent

A LangGraph-based reflection agent that implements a generate-reflect cycle for creating and refining content using StateGraph for flexible state management.

## Project Setup from Scratch

Follow these steps to initialize and set up the project from scratch:

### 1. Initialize Project with uv

```bash
# Initialize a new Python project
uv init

# Add all required dependencies  
uv add python-dotenv black isort langchain langchain-openai langgraph
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
- `pyproject.toml`: Project dependencies managed by uv
- `.env_template`: Template for environment variables
- `.env`: Your actual environment variables (not committed to git)

## Architecture

This project will implement:

- **StateGraph**: Custom state management using TypedDict
- **Generation Node**: Creates content using LangChain generation chain
- **Reflection Node**: Provides critiques and improvement suggestions
- **Conditional Logic**: Controls flow based on message count or approval criteria

## Development

### Code Formatting

Format your code using the included tools:

```bash
black .
isort .
```

### Running the Application

```bash
# Make sure virtual environment is activated
source .venv/bin/activate

# Run the main application
python main.py
```

## Next Steps

1. Implement the StateGraph architecture in `main.py`
2. Create the LangChain chains in `chains.py`
3. Define your graph nodes and conditional logic
4. Test the generate-reflect cycle

## Dependencies

- `langchain`: LLM framework
- `langchain-openai`: OpenAI integration
- `langgraph`: Graph-based agent framework
- `python-dotenv`: Environment variable management
- `black`, `isort`: Code formatting tools