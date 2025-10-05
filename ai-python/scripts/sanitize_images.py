import os
from PIL import Image

DATA_DIR = 'data'
sanitized_count = 0
error_count = 0

print(f"✨ Iniciando padronização de imagens em '{os.path.abspath(DATA_DIR)}'...")
print("Este processo irá re-salvar todas as imagens em um formato JPEG padrão (RGB).")

for root, dirs, files in os.walk(DATA_DIR):
    for filename in files:
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            file_path = os.path.join(root, filename)
            try:
                with Image.open(file_path) as img:
                    img.convert('RGB').save(file_path, 'jpeg', quality=90)
                sanitized_count += 1
                print(f"✅ Padronizado: {filename}")
            except Exception as e:
                print(f"❌ Erro ao processar {file_path}: {e}")
                error_count += 1

print("\n--- Relatório Final da Padronização ---")
print(f"✨ {sanitized_count} imagens foram processadas e salvas com sucesso.")
if error_count > 0:
    print(f"🚨 {error_count} imagens encontraram erros e podem precisar de atenção manual.")
else:
    print("✅ Nenhum erro encontrado durante o processo.")