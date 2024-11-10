from unstructured.partition.pdf import partition_pdf
import html2markdown

fname = "./pdf_with_tables2.pdf"

elements = partition_pdf(filename=fname,
                        infer_table_structure=True,
                        strategy='hi_res',
                       )

# for el in elements:
#     if el.category == "Table":
#         print(el.text)
#     else:
#         print(el.category)
#         print(el.text)

tables = [el for el in elements if el.category == "Table"]

for table in tables:
    print("Original Text:")
    print(table.text)
    print("\nMarkdown Table:")
    # Convert HTML to markdown
    markdown_table = html2markdown.convert(table.metadata.text_as_html)
    print(markdown_table)
    print("\n---\n")
    
