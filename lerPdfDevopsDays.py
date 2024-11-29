import os
import csv
import re
from PyPDF2 import PdfReader

# Diretório base para varrer
BASE_DIR = 'Past_Events'

# Arquivo CSV de saída
OUTPUT_CSV = 'word_mapping.csv'

def extract_words_from_text(content):
    """Extrai palavras de um conteúdo de texto."""
    return re.findall(r'\b\w+\b', content.lower())

def extract_words_from_file(file_path):
    """Lê o conteúdo de um arquivo (PDF ou texto) e extrai palavras."""
    words = []
    if file_path.lower().endswith('.pdf'):
        try:
            reader = PdfReader(file_path)
            content = ''
            for page in reader.pages:
                content += page.extract_text()
            words = extract_words_from_text(content)
        except Exception as e:
            print(f"Erro ao processar o PDF {file_path}: {e}")
    else:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                words = extract_words_from_text(content)
        except Exception as e:
            print(f"Erro ao ler o arquivo {file_path}: {e}")
    return words

def map_words_to_csv(base_dir, output_csv):
    """Varrer pastas, mapear palavras e salvar em CSV."""
    rows = []
    for root, dirs, files in os.walk(base_dir):
        # Extrair ano e nome do evento a partir do caminho
        path_parts = os.path.relpath(root, base_dir).split(os.sep)
        if len(path_parts) == 2:  # Garantir que há ano e nome do evento
            year, event_name = path_parts
            for file in files:
                file_path = os.path.join(root, file)
                print(f"Processando arquivo: {file_path}")
                words = extract_words_from_file(file_path)
                for word in words:
                    rows.append([year, event_name, word])

    # Salvar as palavras no arquivo CSV
    with open(output_csv, 'w', encoding='utf-8', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Ano', 'Nome do Evento', 'Palavra'])
        csv_writer.writerows(rows)

    print(f"Processamento concluído! Arquivo CSV salvo em: {output_csv}")

if __name__ == "__main__":
    map_words_to_csv(BASE_DIR, OUTPUT_CSV)
