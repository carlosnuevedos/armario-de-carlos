import json
import os

base_dir = "fotos_yupoo"
catalogo = {}

if os.path.exists(base_dir):
    # os.walk recorre la carpeta principal y todas sus subcarpetas hacia abajo
    for root, dirs, files in os.walk(base_dir):
        for filename in files:
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.avif')):
                
                # Obtenemos la ruta relativa para saber en qué subcarpeta está exactamente
                rel_path = os.path.relpath(root, base_dir)
                
                if rel_path == ".":
                    carpeta = "general"
                    marca_nombre = "General"
                else:
                    # Usamos la última subcarpeta como nombre de marca o categoría principal
                    partes_ruta = rel_path.replace("\\", "/").split("/")
                    marca_nombre = partes_ruta[-1].replace("_", " ").title()
                    carpeta = rel_path.replace("\\", "/")

                titulo = f"{marca_nombre} - {os.path.splitext(filename)[0]}"
                
                catalogo[filename] = {
                    "titulo": titulo,
                    "marca": marca_nombre,
                    "carpeta": carpeta
                }

    with open("catalogo_info.json", "w", encoding="utf-8") as f:
        json.dump(catalogo, f, ensure_ascii=False, indent=4)
        
    print(f"¡Éxito! Se han indexado {len(catalogo)} fotos explorando todas las subcarpetas.")
else:
    print(f"No se encuentra la carpeta '{base_dir}'.")