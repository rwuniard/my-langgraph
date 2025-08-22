from dotenv import load_dotenv
import os

load_dotenv()

from langchain_tavily import TavilySearch
from langchain_core.tools import StructuredTool
from langgraph.prebuilt import ToolNode
from schemas import AnswerQuestion, RevisedAnswer







tavily_search_tool = TavilySearch(api_key=os.getenv("TAVILY_API_KEY"), max_results=5)


def run_queries(search_queries: list[str], **kwargs):
    """Run a list of search queries and return the results."""
    queries = [{"query": query} for query in search_queries]    
    results = tavily_search_tool.batch(queries)
    return results


execute_tools = ToolNode(
    tools = [
        StructuredTool.from_function(
            func = run_queries,
            name = AnswerQuestion.__name__,
            description = "Run a list of search queries and return the AnswerQuestion results.",
            args_schema = AnswerQuestion,
        ),
        StructuredTool.from_function(
            func = run_queries,
            name = RevisedAnswer.__name__,
            description = "Run a list of search queries and return the RevisedAnswer results.",
            args_schema = RevisedAnswer,
        )
    ]
)






