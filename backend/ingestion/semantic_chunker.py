from pathlib import Path
from dotenv import load_dotenv


from langchain_core.documents import Document
from langchain_experimental.text_splitter import SemanticChunker



def read_markdown_file(markdown_file: str) -> str:
    """Read the content of a markdown file and return it as a string.
    
    Args:
        markdown_file (str): Path to the markdown file.
    Returns:
        str: Content of the markdown file.
    """

    markdown_content = Path(markdown_file).read_text(encoding="utf-8")  
    return str(markdown_content)


def chunk_markdown_file_content(markdown_file: str, embeddings) -> list[Document]:
    """Chunk the content of a markdown file into smaller documents using semantic chunking.
    
    Args:
        markdown_file (str): Path to the markdown file.
        embeddings: Azure OpenAI Embedding Model for semantic chunking.
    Returns:
        list[Document]: List of Document objects containing the semantic chunked content.
    """

    markdown_content = read_markdown_file(markdown_file)
    chunker = SemanticChunker(embeddings=embeddings, breakpoint_threshold_type="percentile")


    documents = chunker.create_documents([markdown_content])

    return documents


if __name__ == "__main__":
    import os 
    from langchain_openai import AzureChatOpenAIEmbeddings
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    api_version = os.getenv("AZURE_OPENAI_API_EMBEDDING_VERSION")
    embedding_model = os.getenv("AZURE_OPENAI_EMBEDDING_MODEL")

    if not endpoint or not api_key or not api_version or not embedding_model:
        raise ValueError("Please set the environment variables: AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, AZURE_OPENAI_API_EMBEDDING_VERSION, AZURE_OPENAI_EMBEDDING_MODEL")

    embeddings = AzureChatOpenAIEmbeddings(
        model = "text-embedding-ada-002",
        azure_endpoint = endpoint,
        azure_api_key = api_key,
        azure_api_version = api_version
        )

    markdown_file_path = "../data/markdowns/2024_Apple.md"  
    chunks = chunk_markdown_file_content(markdown_file=markdown_file_path, embeddings=embeddings)
    print(f"Number of chunks created: {len(chunks)}")

    for index, chunk in enumerate(chunks):
        print("#"*50)
        print(f"Chunk {index + 1}: {chunk.page_content[:100]}...")  