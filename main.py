from langchain_unstructured import UnstructuredLoader
import json

file_paths = [
    "./pdf_with_tables.pdf"
]


loader = UnstructuredLoader(file_paths)

docs = loader.load()

for doc in docs:
    print(doc.metadata)
    print(doc.page_content)
    print("-"*100)
