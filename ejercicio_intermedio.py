import requests
from bs4 import BeautifulSoup

# Pedir palabra clave
palabra = input("¿Qué producto quieres buscar?: ")

# Crear la URL de búsqueda
url = f"https://listado.mercadolibre.com.co/{palabra}"

# Hacer la solicitud a la página
respuesta = requests.get(url)

# Verificar si la respuesta fue exitosa
if respuesta.status_code == 200:
    # Analizar el HTML con BeautifulSoup
    soup = BeautifulSoup(respuesta.text, 'html.parser')
    
    # Buscar los primeros 5 productos
    productos = soup.find_all('li', class_='ui-search-layout__item', limit=5)
    
    # Mostrar los resultados
    for i, producto in enumerate(productos, start=1):
        titulo = producto.find('h3', class_='poly-component__title-wrapper')
        precio = producto.find('span', class_='andes-money-amount andes-money-amount--cents-superscript')

        titulo_texto = titulo.text if titulo else "Sin título"
        precio_texto = precio.get_text(strip=True) if precio else "Sin precio"

        print(f"{i}. {titulo_texto} - Precio: {precio_texto}")
else:
    print("No se pudo acceder a Mercado Libre.")
