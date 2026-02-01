from typing import TypedDict, Annotated, Sequence
import operator
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate

from config.settings import MODEL, SYSTEM_PROMPT

from src.tools import combined_retriever


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]

class SQLResponse(BaseModel):
    sql_query: str = Field(..., description="The MySQL query that answers the user request.")
    explanation: str = Field(..., description="A short explanation mentioning which tables were used in the query.")

parser = PydanticOutputParser(pydantic_object=SQLResponse)
text2sql_prompt = SYSTEM_PROMPT.format(format_instructions=parser.get_format_instructions())

tools = [combined_retriever]

llm = ChatOpenAI(model=MODEL, temperature=0)
# llm = llm.with_structured_output(SQLResponse)
llm_with_tools = llm.bind_tools(tools)



def call_model(state: AgentState):
    messages = list(state["messages"])

    if not any(isinstance(msg, SystemMessage) for msg in messages):
        
        messages = [SystemMessage(content=text2sql_prompt)] + messages

    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}


def should_continue(state: AgentState):
    messages = state['messages']
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tools"
    return END

# Build the graph
workflow = StateGraph(AgentState)

workflow.add_node("agent", call_model)
workflow.add_node("tools", ToolNode(tools))

workflow.set_entry_point("agent")

workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools",
        END: END
    }
)

workflow.add_edge("tools", "agent")

# Compile the graph
agent_app = workflow.compile()


