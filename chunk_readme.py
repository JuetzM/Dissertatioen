import os
import re
import tiktoken

# Konfigurationsvariablen
MAX_TOKENS = 2048
OVERLAP_TOKENS = 200
CHUNK_DIR = 'readme_chunks'
README_FILE = 'README.md'
ENCODING = 'cl100k_base'  # GPT-4 Encoding

# Initialisiere das Tokenizer-Modul
enc = tiktoken.get_encoding(ENCODING)

def count_tokens(text):
    return len(enc.encode(text))

def split_into_chunks(text, max_tokens, overlap_tokens):
    chunks = []
    current_chunk = []
    current_chunk_tokens = 0

    for line in text.split('\n'):
        line_tokens = count_tokens(line)
        if current_chunk_tokens + line_tokens > max_tokens:
            chunks.append('\n'.join(current_chunk))
            current_chunk = current_chunk[-overlap_tokens:]  # Überlappung
            current_chunk_tokens = count_tokens('\n'.join(current_chunk))
        
        current_chunk.append(line)
        current_chunk_tokens += line_tokens

    if current_chunk:
        chunks.append('\n'.join(current_chunk))

    return chunks

def save_chunks(chunks, base_filename):
    if not os.path.exists(CHUNK_DIR):
        os.makedirs(CHUNK_DIR)

    for i, chunk in enumerate(chunks):
        chunk_filename = os.path.join(CHUNK_DIR, f'{base_filename}_chunk_{i+1:02d}.md')
        with open(chunk_filename, 'w') as chunk_file:
            chunk_file.write(chunk)

def main():
    if not os.path.exists(README_FILE):
        print(f"Fehler: Die Datei {README_FILE} wurde nicht gefunden.")
        return

    with open(README_FILE, 'r') as readme_file:
        readme_text = readme_file.read()

    chunks = split_into_chunks(readme_text, MAX_TOKENS, OVERLAP_TOKENS)
    save_chunks(chunks, 'README')

    print(f"Die Datei {README_FILE} wurde erfolgreich in {len(chunks)} Chunks aufgeteilt und im Verzeichnis {CHUNK_DIR} gespeichert.")

if __name__ == '__main__':
    main()