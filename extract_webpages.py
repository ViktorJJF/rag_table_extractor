from langchain_unstructured import UnstructuredLoader

# Load the webpage content
loader = UnstructuredLoader(web_url="https://www.imahe.cl/content/8-servicio-tecnico")
docs = loader.load()

# Write the output to a file
output_file = "webpage_content.txt"
with open(output_file, "w", encoding="utf-8") as f:
    for doc in docs:
        f.write(f"{doc.page_content}\n\n")