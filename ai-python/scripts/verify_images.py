import os
from PIL import Image

DATA_DIR = 'data'

invalid_files = []
valid_image_count = 0

print(f"🔎 Verificando imagens no diretório: '{os.path.abspath(DATA_DIR)}'...")

for root, dirs, files in os.walk(DATA_DIR):
    for filename in files:
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')):
            file_path = os.path.join(root, filename)
            try:
                with Image.open(file_path) as img:
                    img.verify()
                valid_image_count += 1
            except (IOError, SyntaxError, Image.UnidentifiedImageError) as e:
                print(f"❌ Arquivo inválido encontrado: {file_path}")
                invalid_files.append(file_path)

print("\n--- Relatório Final ---")
if not invalid_files:
    print("✅ Todas as imagens foram verificadas e parecem estar válidas!")
else:
    print(f"🚨 Encontrados {len(invalid_files)} arquivos problemáticos. Por favor, remova-os ou corrija-os.")

print(f"📊 Total de imagens válidas: {valid_image_count}")