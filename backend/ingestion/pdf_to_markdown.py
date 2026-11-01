from pathlib import Path
import pymupdf4llm



class PDFToMarkdown:
    """convert pdf document to markdown format"""


    def convert_pdf_to_markdown(self, pdf_path: str, output_dir: str) -> str:

        """convert a pdf document to markdown format
        
        Args: 
            pdf_path (str): path of pdf document that to be converted to markdown format
            output_dir (str): path of output directory where the markdown file will be saved
        Returns :
            Return the markdown file path
        """
        pdf_file = Path(pdf_path)

        if not pdf_file.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        output_dir_path = Path(output_dir)
        output_dir_path.mkdir(parents=True, exist_ok=True)


        markdown_content = pymupdf4llm.to_markdown(str(pdf_path))
        markdown_file = output_dir_path / f"{pdf_file.stem}.md"

        markdown_file.write_text(markdown_content, encoding="utf-8")

        return str(markdown_file)


    def convert_entire_pdf_directory_to_markdown(self, pdf_dir: str, output_dir: str) -> list[str]:
        """convert all pdf documents in a directory to markdown format
        
        Args: 
            pdf_dir (str): path of directory that contains pdf documents that to be converted to markdown format
            output_dir (str): path of output directory where the markdown files will be saved
        Returns :
            Return the list of markdown file paths
        """
        pdf_directory = Path(pdf_dir)

        if not pdf_directory.exists():
            raise FileNotFoundError(f"PDF directory not found: {pdf_dir}")

        output_dir_path = Path(output_dir)
        output_dir_path.mkdir(parents=True, exist_ok=True)

        markdown_files = []
        for pdf_file in pdf_directory.glob("*.pdf"):
            markdown_file_path = self.convert_pdf_to_markdown(pdf_path = str(pdf_file), output_dir = str(output_dir_path))
            markdown_files.append(markdown_file_path)

        return markdown_files


if __name__ == "__main__":

    repo_root = Path(__file__).resolve().parents[1] # backend
    pdf_dir = repo_root / "data" / "raw_pdfs"   

    pdf_to_markdown_converter = PDFToMarkdown()

    markdown_files = pdf_to_markdown_converter.convert_entire_pdf_directory_to_markdown(pdf_dir=str(pdf_dir), output_dir=str(repo_root / "data" / "markdowns"))
    print(f"markdown content: {markdown_files}")

    print(f"Successfully converted {len(markdown_files)} PDF files to Markdown format.")

    for markdown_file in markdown_files:
        print(f"Markdown file saved at: {markdown_file}")