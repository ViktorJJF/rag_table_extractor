import requests
from bs4 import BeautifulSoup
import htmltabletomd

# Definir los encabezados para simular una solicitud de navegador
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
    "Accept-Language": "es-ES,es;q=0.9",
}

# URL de la página web a scrapear
url = "https://salcobrand.cl/content/servicio-al-cliente/tabla-despacho"

# Realizar la solicitud HTTP
response = requests.get(url, headers=headers)
response.raise_for_status()  # Verificar que la solicitud fue exitosa

# Analizar el contenido HTML
soup = BeautifulSoup(response.text, 'html.parser')

# Extraer el contenido de texto de toda la página
contenido_texto = soup.get_text(separator="\n", strip=True)

# Encontrar y convertir todas las tablas en el documento a formato Markdown
tablas = soup.find_all('table')
tablas_markdown = []

if tablas:
    for tabla in tablas:
        print(tabla)
        # Convertir cada tabla HTML a formato Markdown
        tablas_markdown.append(htmltabletomd.convert_table(str(tabla)))
    # Unir todas las tablas en una sola cadena de texto
    contenido_tablas = '\n\n'.join(tablas_markdown)
    # Concatenar el texto general con las tablas en formato Markdown
    contenido_completo = f"{contenido_texto}\n\n{contenido_tablas}"
else:
    contenido_completo = contenido_texto

# Guardar el resultado en un archivo de texto
with open('contenido_y_tablas_extraidos.md', 'w', encoding='utf-8') as file:
    file.write(contenido_completo)

print("Contenido y tablas extraídos y guardados en contenido_y_tablas_extraidos.md.")
