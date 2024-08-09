import os
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
)
from dotenv import load_dotenv

load_dotenv()

print("Ingesting documents...")

# Check if storage already exists
PERSIST_DIR = os.environ.get("PERSIST_DIR")
if not PERSIST_DIR:
    print("PERSIST_DIR environment variable is not set.")
elif not os.path.exists(PERSIST_DIR):
    # Load the documents and create the index
    if not os.path.exists("data"):
        print("Data directory does not exist.")
    else:
        try:
            documents = SimpleDirectoryReader("data").load_data()
            if not documents:
                print("No documents found to index.")
            else:
                index = VectorStoreIndex.from_documents(documents)
                # Store it for later
                index.storage_context.persist(persist_dir=PERSIST_DIR)
                print(f"Index successfully persisted to {PERSIST_DIR}")
        except Exception as e:
            print(f"Error loading documents: {e}")

print("Documents ingested")
