import requests
from bs4 import BeautifulSoup

palabra = input("¿Qué producto quieres buscar?: ")

url = f"https://listado.mercadolibre.com.co/{palabra}"

respuesta = requests.get(url)

if respuesta.status_code == 200:
    soup = BeautifulSoup(respuesta.text, 'html.parser')
    productos = soup.find_all('li', class_='ui-search-layout__item', limit=5)
    for i, producto in enumerate(productos, start=1):
        titulo = producto.find('h3', class_='poly-component__title-wrapper')
        precio = producto.find('span', class_='andes-money-amount andes-money-amount--cents-superscript')

        titulo_texto = titulo.text if titulo else "Sin título"
        precio_texto = precio.get_text(strip=True) if precio else "Sin precio"

        print(f"{i}. {titulo_texto} - Precio: {precio_texto}")
else:
    print("No se pudo acceder a Mercado Libre.")
