import requests
from bs4 import BeautifulSoup

def decode_cfemail(cfemail):
    # Decode the obfuscated email using the key in the first two characters
    r = int(cfemail[:2], 16)
    email = ''.join(
        chr(int(cfemail[i:i+2], 16) ^ r) for i in range(2, len(cfemail), 2)
    )
    return email

# Fetch the HTML content of the page
url = "https://test.cl"
html = requests.get(url).text

# Parse HTML
soup = BeautifulSoup(html, 'html.parser')

# Find all elements with data-cfemail attribute and decode the emails
for element in soup.find_all(attrs={"data-cfemail": True}):
    cfemail = element['data-cfemail']
    decoded_email = decode_cfemail(cfemail)
    
    # Replace the content of the element with the decoded email
    element.string = decoded_email  # Replaces the obfuscated text with the decoded email

    # Remove the data-cfemail attribute to prevent confusion
    del element['data-cfemail']
