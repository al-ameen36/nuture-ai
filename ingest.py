import os.path
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
)
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.core import Settings
from dotenv import load_dotenv

load_dotenv()

Settings.llm = Gemini(model="models/gemini-1.5-flash-001")
Settings.embed_model = GeminiEmbedding(model="models/text-embedding-001")


# check if storage already exists
PERSIST_DIR = os.environ.get("PERSIST_DIR")
if not os.path.exists(PERSIST_DIR):
    # load the documents and create the index
    documents = SimpleDirectoryReader("data").load_data()
    index = VectorStoreIndex.from_documents(documents)
    # store it for later
    index.storage_context.persist(persist_dir=PERSIST_DIR)
