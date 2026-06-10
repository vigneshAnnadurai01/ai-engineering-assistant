from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
from openai import AsyncOpenAI
import uuid
import os

app = FastAPI(title="MCP Production Server")

# ==========================
# OPENAI CLIENT
# ==========================

client = AsyncOpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# ==========================
# REQUEST MODEL
# ==========================

class UserRequest(BaseModel):
    query: str


# ==========================
# MCP TOOLS (NO ANALYSIS CHANGE)
# ==========================


class AccountTool:
    async def execute(self, query: str, document=None):
        return {
            "tool": "AccountTool Tool",
            "result": f"AccountTool processed: {query}",
            "doc_received": bool(document)
        }


class Account_AnalyticsTool:
    async def execute(self, query: str, document=None):
        return {
            "tool": "Account_AnalyticsTool Tool",
            "result": f"Account_AnalyticsTool processed: {query}",
            "doc_received": bool(document)
        }


class General_AssistantTool:
    async def execute(self, query: str, document=None):
        return {
            "tool": "General_Assistant Tool",
            "result": f"Chat response: {query}",
            "doc_received": bool(document)
        }


# ==========================
# MCP SERVER (ROUTER)
# ==========================

class MCPServer:

    def __init__(self):
        self.tools = {
            "AccountTool": AccountTool(),
            "Account_AnalyticsTool": Account_AnalyticsTool(),
            "General_Assistant": General_AssistantTool()
        }

    async def route_tool(self, tool_name: str, query: str, document=None):
        return await self.tools[tool_name].execute(query, document)


mcp_server = MCPServer()


# ==========================
# LLM AGENT (ONLY ROUTING)
# ==========================

class LLMAgent:

    async def process(self, query: str, document=None):

        task_id = str(uuid.uuid4())

        response = await client.chat.completions.create(
            model="gpt-5",
            messages=[
                {
                    "role": "system",
                    "content": """
You are an MCP tool router.

Choose ONLY ONE:
AccountTool
Account_AnalyticsTool
General_Assistant

Rules:
- Return only one word
- No explanation
"""
                },
                {
                    "role": "user",
                    "content": query
                }
            ]
        )

        tool_name = response.choices[0].message.content.strip().lower()

        result = await mcp_server.route_tool(
            tool_name=tool_name,
            query=query,
            document=document
        )

        return {
            "task_id": task_id,
            "selected_tool": tool_name,
            "response": result
        }


agent = LLMAgent()


# ==========================
# API ENDPOINT
# ==========================

@app.post("/chat")
async def chat(
    query: str = Form(...),
    document: UploadFile = File(None)
):

    result = await agent.process(query, document)

    return {
        "status": "success",
        "data": result
    }