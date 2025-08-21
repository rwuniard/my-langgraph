# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a LangGraph-based reflection agent that implements a generate-reflect cycle for creating and refining Twitter posts. The agent uses OpenAI's API through LangChain to iteratively improve content based on automated critiques.

## Architecture

The project follows a graph-based architecture using LangGraph:

- **Generation Node**: Creates Twitter posts using a generation prompt
- **Reflection Node**: Critiques posts and provides improvement suggestions  
- **Graph Flow**: Generate → Reflect → Generate (up to 6 iterations) → End

Key components:
- `main.py`: Defines the MessageGraph with nodes and conditional edges
- `chains.py`: Contains LangChain Expression Language (LCEL) chains for generation and reflection prompts
- The graph terminates after 6 messages or when approved

## Development Setup

Working directory: `reflection-agent/`

### Environment Setup
```bash
# Create virtual environment
uv venv

# Activate environment  
source .venv/bin/activate

# Install dependencies
uv pip install -e .
```

### Environment Variables
Copy `.env_template` to `.env` and configure:
```bash
cp .env_template .env
```

Required variables:
- `OPENAI_API_KEY`: OpenAI API key for LLM access
- Optional LangSmith tracing variables for debugging

### Running the Application
```bash
python main.py
```

## Code Formatting
The project includes Black and isort for code formatting:
```bash
black .
isort .
```

## Dependencies

Core dependencies managed in `pyproject.toml`:
- `langchain`: LLM framework
- `langchain-openai`: OpenAI integration
- `langgraph`: Graph-based agent framework  
- `python-dotenv`: Environment variable management
- `black`, `isort`: Code formatting tools

## Key Patterns

- Uses `MessageGraph` for stateful conversation flows
- Implements conditional edges based on message count
- Chains combine prompts with LLMs using LCEL syntax (`prompt | llm`)
- State is maintained as a sequence of `BaseMessage` objects