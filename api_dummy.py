import os
import pathlib
import pathway as pw
from dotenv import load_dotenv
from common.embedder import embeddings, index_embeddings
from common.prompt import prompt
from llm_app import chunk_texts, extract_texts

load_dotenv()

# Define the Dropbox folder path where files will be uploaded
dropbox_folder_path = os.environ.get("C:\Users\nawka\Dropbox", "/usr/local/documents")

# Function to read files from the Dropbox folder
def read_files_from_dropbox_folder():
    files = []
    for file in os.listdir(dropbox_folder_path):
        if file.endswith(".pdf"):
            file_path = pathlib.Path(dropbox_folder_path) / file
            with open(file_path, "rb") as f:
                files.append(f.read())
    return files

def run(host, port):
    # Given a user query
    query, response_writer = pw.io.http.rest_connector(
        host=host,
        port=port,
        schema=QueryInputSchema,
        autocommit_duration_ms=50,
    )

    # Read PDF files from the Dropbox folder
    pdf_files = read_files_from_dropbox_folder()

    # Process the PDF files and convert them into documents
    documents = pw.io.fs.read(pdf_files, format="binary")
    
    # Chunk input data into smaller documents
    documents = documents.select(texts=extract_texts(pw.this.data))
    documents = documents.select(chunks=chunk_texts(pw.this.texts))
    documents = documents.flatten(pw.this.chunks).rename_columns(chunk=pw.this.chunks)

    # Compute embeddings for each document using the OpenAI Embeddings API
    embedded_data = embeddings(context=documents, data_to_embed=pw.this.chunk)

    # Construct an index on the generated embeddings in real-time
    index = index_embeddings(embedded_data)

    # Generate embeddings for the query from the OpenAI Embeddings API
    embedded_query = embeddings(context=query, data_to_embed=pw.this.query)

    # Build a prompt using indexed data
    responses = prompt(index, embedded_query, pw.this.query)

    # Feed the prompt to ChatGPT and obtain the generated answer.
    response_writer(responses)

    # Run the pipeline
    pw.run()

class QueryInputSchema(pw.Schema):
    query: str
