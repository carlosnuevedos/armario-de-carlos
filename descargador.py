import os
import time
import json
import requests
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Referer': 'https://jsl68.x.yupoo.com/'
}

CARPETA_DESTINO = "fotos_yupoo"
os.makedirs(CARPETA_DESTINO, exist_ok=True)

json_path = "catalogo_info.json"
metadata_productos = {}

# Si ya existe un registro previo, lo cargamos para continuar sin perder datos
if os.path.exists(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        try:
            metadata_productos = json.load(f)
        except:
            pass

def detectar_marca(texto):
    """Detecta automáticamente la marca basándose en palabras clave en chino y español"""
    texto_lower = texto.lower()
    
    # Mapeo de términos comunes en Yupoo a su marca correspondiente
    if any(k in texto for k in ['耐克', 'nike', '科比', '莫兰特', '欧文', '乔丹', '空军', '气垫', '刺客']):
        return "Nike"
    elif any(k in texto for k in ['阿迪', 'adidas', 'ub', '猎鹰', 'f50', '椰子', 'yeezy']):
        return "Adidas"
    elif any(k in texto for k in ['新百伦', 'nb', 'new balance']):
        return "New Balance"
    elif any(k in texto for k in ['hoka', '霍卡']):
        return "Hoka"
    elif any(k in texto for k in ['昂跑', 'on running', 'cloud']):
        return "On Running"
    elif any(k in texto for k in ['布鲁克斯', 'brooks']):
        return "Brooks"
    elif any(k in texto for k in ['lv', 'gucci', '巴黎', 'prada', 'dior', '蒙口', '大鹅']):
        return "Lujo / Otras"
    elif any(k in texto for k in ['匡威', 'converse', '万斯', 'vans', '彪马', 'puma']):
        return "Otras Marcas"
        
    return "Otras"

urls_descargadas = set()
contador = len([f for f in os.listdir(CARPETA_DESTINO) if f.startswith('producto_')]) + 1

# Rango de páginas (puedes ajustarlo según por dónde vayas)
for pagina in range(58, 91):
    url = f"https://jsl68.x.yupoo.com/albums?page={pagina}"
    print(f"Procesando página {pagina}...")
    
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        print(f"No se pudo acceder a la página {pagina}")
        break
        
    soup = BeautifulSoup(response.text, 'html.parser')
    imagenes = soup.find_all('img')
    
    for img in imagenes:
        img_url = img.get('data-src') or img.get('src')
        if not img_url:
            continue
            
        if img_url.startswith('//'):
            img_url = "https:" + img_url
            
        if any(palabra in img_url.lower() for palabra in ['icon', 'logo', 'avatar', 'loading']):
            continue
            
        if img_url in urls_descargadas:
            continue
            
        urls_descargadas.add(img_url)
        
        # Extraer el título del producto desde el atributo alt o el contenedor padre
        titulo = img.get('alt') or ""
        if not titulo or len(titulo.strip()) < 2:
            parent = img.find_parent('a') or img.find_parent()
            if parent:
                titulo = parent.get('title') or parent.get_text(strip=True)
        
        if not titulo:
            titulo = f"Artículo #{contador}"

        try:
            img_data = requests.get(img_url, headers=HEADERS).content
            nombre_archivo = f"producto_{contador}.jpg"
            ruta_completa = os.path.join(CARPETA_DESTINO, nombre_archivo)
            
            with open(ruta_completa, 'wb') as f:
                f.write(img_data)
            
            # Guardamos la marca y el título detectados automáticamente
            marca = detectar_marca(titulo)
            metadata_productos[nombre_archivo] = {
                "titulo": titulo,
                "marca": marca
            }
            
            # Actualizamos el archivo JSON en tiempo real por seguridad
            with open(json_path, 'w', encoding='utf-8') as jf:
                json.dump(metadata_productos, jf, ensure_ascii=False, indent=4)

            print(f"Descargado: {nombre_archivo} [{marca}]")
            contador += 1
            time.sleep(0.1)
        except Exception as e:
            print(f"Error al descargar imagen: {e}")

print(f"\n¡Proceso finalizado! Se han guardado las imágenes y el archivo de información '{json_path}'.")