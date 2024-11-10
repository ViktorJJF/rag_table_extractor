import time
start_time = time.time()
from pathlib import Path
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.document import ConversionResult, TextItem, TableItem, PictureItem

# Define the path for the Hugging Face cached model
artifacts_path = "/home/vscode/.cache/huggingface/hub/models--ds4sd--docling-models/snapshots/a8a57426c20d9f7bc0343cfd84e8b439425e5561"

# Define folder to save images
image_folder = Path("./downloaded_images")
image_folder.mkdir(exist_ok=True)

# Set up PDF pipeline options and document converter with image generation enabled
pipeline_options = PdfPipelineOptions(artifacts_path=artifacts_path, generate_picture_images=True)
doc_converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
    }
)

# Convert document
conv_result: ConversionResult = doc_converter.convert("https://viktorfiles.s3.sa-east-1.amazonaws.com/1711641321_V3.0Propuesta_Databot_CL_2024(3).pdf")

# Iterate through items in document and process them
for item, level in conv_result.document.iterate_items():
    if isinstance(item, TextItem):
        print(item.text)
    elif isinstance(item, TableItem):
        table_df = item.export_to_dataframe()
        print('INICIO DE TABLA')
        print(table_df.to_markdown())
        print('FIN DE TABLA')
    elif isinstance(item, PictureItem):
        if item.image is not None:
            # Sanitize self_ref to create a valid file name
            sanitized_ref = item.self_ref.replace('#', '').replace('/', '_')
            img_file_path = image_folder / f"image_{sanitized_ref}.png"
            
            # Save image data to file
            img = item.image.pil_image
            print(f"Image data type: {item.self_ref}")
            img.save(img_file_path)
            print(f"Image saved at: {img_file_path}")
        else:
            print(f"No image data available for picture item {item.self_ref}")

end_time = time.time()
print(f"Total time taken: {end_time - start_time} seconds")