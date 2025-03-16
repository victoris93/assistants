import click
import sys
import os
from llama_index.llms.ollama import Ollama
from llama_parse import LlamaParse
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, PromptTemplate
from llama_index.core.embeddings import resolve_embed_model
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.agent import ReActAgent
import subprocess
from utils import load_model
from prompts import rag_neurosci_context
from dotenv import load_dotenv

load_dotenv()

@click.command()
@click.argument("model", type=str)
@click.argument("docs_path", type=str)
@click.argument("input", type=str, required=False)

def query_vect_database(model, docs_path, input):

    if input is None:
        prompt = sys.stdin.read()
    else:
        try:
            with open(input, 'rb') as file:
                prompt = file.read().decode('utf-8')
        except FileNotFoundError:
            prompt = input

    context = rag_neurosci_context()
    llm = load_model(model)

    index_path = f"{docs_path}/index"
    embed_model = resolve_embed_model("local:BAAI/bge-m3")

    # if there is no index locally, create on
    if not os.path.exists(index_path):
        parser = LlamaParse(result_type="markdown")
        file_extractor = {".pdf": parser}
        documents = SimpleDirectoryReader(docs_path, file_extractor=file_extractor).load_data()
        vector_index = VectorStoreIndex.from_documents(documents,  embed_model=embed_model)
        vector_index.storage_context.persist(index_path)
    else:
        storage_context = StorageContext.from_defaults(persist_dir=index_path)
        vector_index = load_index_from_storage(storage_context, embed_model=embed_model)

    query_engine = vector_index.as_query_engine(llm=llm)

    tools = [
        QueryEngineTool(
            query_engine=query_engine,
            metadata=ToolMetadata(
                name="library",
                description="Scientific literature on machine learning and methods"
            ),
        )
    ]

    agent = ReActAgent.from_tools(tools=tools, llm=llm, verbose=False, context=context)
    result = agent.query(prompt)
    click.echo(str(result))

if __name__ == "__main__":
    query_vect_database()

# Next step: streamlit