import os
from fastapi import FastAPI
from pydantic import BaseModel
from llama_index.core import (
    StorageContext,
    load_index_from_storage,
)
from dotenv import load_dotenv
from prompt_templates import query_template
from llama_index.core import Settings
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.gemini import GeminiEmbedding

load_dotenv()
app = FastAPI()

Settings.llm = Gemini(model="models/gemini-1.5-flash-001")
Settings.embed_model = GeminiEmbedding(model="models/text-embedding-001")

storage_context = StorageContext.from_defaults(
    persist_dir=os.environ.get("PERSIST_DIR")
)
index = load_index_from_storage(storage_context)

query_engine = index.as_query_engine()


async def ask_nuture(user_query: str):
    formatted_query = query_template.format(user_query=user_query)
    response = query_engine.query(formatted_query)
    return response


class Query(BaseModel):
    q: str


@app.post("/query")
async def query(query: Query):
    answer = await ask_nuture(query.q)
    return {"response": answer["response"], "embeddings": []}
