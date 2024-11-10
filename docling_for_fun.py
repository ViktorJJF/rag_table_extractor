from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.pipeline.standard_pdf_pipeline import StandardPdfPipeline
from docling.datamodel.document import ConversionResult, TextItem, TableItem, PictureItem
from docling_core.transforms.chunker import HierarchicalChunker
from PIL import Image
from pathlib import Path

# doc_converter = DocumentConverter()



# # to explicitly prefetch:
# # artifacts_path = StandardPdfPipeline.download_models_hf()
# # print(artifacts_path)

artifacts_path = "/home/vscode/.cache/huggingface/hub/models--ds4sd--docling-models/snapshots/a8a57426c20d9f7bc0343cfd84e8b439425e5561"

pipeline_options = PdfPipelineOptions(artifacts_path=artifacts_path)
doc_converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
    }
)

conv_result: ConversionResult = doc_converter.convert("https://viktorfiles.s3.sa-east-1.amazonaws.com/correo_databot_informe_2023.pdf")

# doc = conv_result.document
# chunks = list(HierarchicalChunker().chunk(doc))
# for chunk in chunks:
#     print(chunk)

# conv_result.document.print_element_tree()

# Define folder to save images
image_folder = Path("./downloaded_images")
image_folder.mkdir(exist_ok=True)

## Iterate the elements in reading order, including hierachy level:
for item, level in conv_result.document.iterate_items():
    if isinstance(item, TextItem):
        print(item.text)
    elif isinstance(item, TableItem):
        table_df = item.export_to_dataframe()
        print(table_df.to_markdown())
    elif isinstance(item, PictureItem):
        print(
                f"The model populated the `data` portion of picture {item.self_ref}:\n{item}"
            )
        img = item.image.pil_image
        img_file_path = image_folder / f"image_{item.self_ref}.png"
        img.save(img_file_path)
        print(f"Image saved at: {img_file_path}")
    
    
# # print(f'''{conv_result=}''')
# # print(f'''{doc_converter=}''')
# pages=conv_result.pages
# for page in pages:
#     print(f'''{page.content=}''')
