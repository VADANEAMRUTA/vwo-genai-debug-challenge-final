## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()

from pypdf import PdfReader

def read_financial_document(path: str) -> str:
    """Extract and clean text content from a financial PDF document"""
    print(f"📄 Reading document: {path}")
    try:
        if not os.path.exists(path):
            return f"Error: File not found at path '{path}'"
            
        reader = PdfReader(path)
        full_report = ""
        
        for page_num, page in enumerate(reader.pages, 1):
            content = page.extract_text()
            if content:
                # Clean up the text
                content = ' '.join(content.split())
                full_report += f"[Page {page_num}]\n{content}\n\n"
        
        if not full_report.strip():
            return "No text could be extracted from the document. The file might be scanned or image-based."
        
        print(f"✅ Successfully read {len(reader.pages)} pages")
        return full_report.strip()
        
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

print("✅ Tools initialized successfully")