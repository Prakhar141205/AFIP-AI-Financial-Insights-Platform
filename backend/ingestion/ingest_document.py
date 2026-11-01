import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import AzureOpenAIEmbeddings

from ingestion.pdf_to_markdown import PDFToMarkdown
from ingestion.semantic_chunker import chunk_markdown_file_content
# from rag.

load_dotenv()


def parse_company_year(pdf_file: str) -> tuple[str, str]:
    """Parse the company name and year from the PDF file name.
        summary files name format is: {year}_{company_name}.pdf
    Args:
        pdf_file (str): Path to the PDF file.
    Returns:
        tuple[str, str]: A tuple containing the company name and year.
    """

    stem = Path(pdf_file).stem
    parts = stem.split("_")
    if len(parts) < 2:
        raise ValueError(f"Invalid PDF file name format: {pdf_file}. Expected format: {{year}}_{{company_name}}.pdf")
    if parts and parts[0].isdigit():
        year = parts[0]
        company_name = "_".join(parts[1:])
    elif len(parts) >= 2:
        year = parts[-1]
        company_name = "_".join(parts[:-1])
    else:
        company = stem
        year = ""

    return company_name, year


def ingest_pdf_document(pdf_file: str, embeddings, vector_store) -> None:
    """Ingest a PDF document by converting it to markdown, chunking the content, and returning the documents.
    
    Args:
        pdf_file (str): Path to the PDF file.
        output_dir (str): Path to the output directory where the markdown file will be saved.
        embeddings: Azure OpenAI Embedding Model for semantic chunking.
    Returns:
        list: List of Document objects containing the semantic chunked content.
    """
    pdf_file = Path(pdf_file)
    company_name, year = parse_company_year(str(pdf_file))
    print(f"Ingesting {pdf_file.name} as company={company_name!r}, year={year!r}")



    # Convert PDF to Markdown

    pdf_to_markdown = PDFToMarkdown()

    markdown_file_path = pdf_to_markdown.convert_pdf_to_markdown(pdf_file, "data/markdowns")

    # Chunk Markdown Content
    chunks = chunk_markdown_file_content(markdown_file_path, embeddings)

    print(f"Generated {len(chunks)} chunks for {pdf_file.name}")

    documents = chunk_markdown_file_content(markdown_file_path, embeddings)

    return documents