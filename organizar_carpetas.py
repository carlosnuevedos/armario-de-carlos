import json
import os
import shutil

json_path = "catalogo_info.json"
base_dir = "fotos_yupoo"

if not os.path.exists(json_path):
    print("No se encontró el archivo catalogo_info.json")
    exit()

with open(json_path, 'r', encoding='utf-8') as f:
    metadata = json.load(f)

movidos = 0
for filename, info in metadata.items():
    marca = info.get("marca", "Otras")
    
    # Normalizamos el nombre de la marca para que sea seguro para carpetas (minúsculas y sin espacios raros)
    marca_folder = marca.lower().replace(" ", "_").replace("/", "_")
    
    # Ruta de la subcarpeta por marca (ej: fotos_yupoo/nike/)
    marca_dir = os.path.join(base_dir, marca_folder)
    os.makedirs(marca_dir, exist_ok=True)
    
    # Ruta origen y destino del archivo
    origen = os.path.join(base_dir, filename)
    destino = os.path.join(marca_dir, filename)
    
    # Si la foto existe en la raíz, la movemos a su subcarpeta
    if os.path.exists(origen):
        shutil.move(origen, destino)
        movidos += 1

print(f"¡Listo! Se han organizado {movidos} fotos en subcarpetas por marca dentro de '{base_dir}'.")