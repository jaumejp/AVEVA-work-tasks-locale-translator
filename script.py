import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from deep_translator import GoogleTranslator
from threading import Lock
from config import translate_from, translate_to, source_directory_name, target_directory_name
import chardet

progress = 0
progress_lock = Lock()

def detect_encoding(file_path):
    try:
        with open(file_path, 'rb') as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
            encoding = result['encoding']
            return encoding
    except Exception as e:
        print(f"Error detectant codificació a: {file_path}: {e}")
        return 'utf-8' 

def translate(text):
    try:
        # translator = GoogleTranslator(source=translate_from, target=translate_to)
        # translated = translator.translate(text)
        translated = "hola"
        return translated
    except Exception as e:
        print(f"Error traduïnt el text: {e}")
        return text

def modify_line(line):
    array_striped = line.split(':', 1)
    
    if len(array_striped) != 2:
        return line + '\n'

    left, right = array_striped[0], array_striped[1]

    if len(right) == 1 and right.upper() not in ('A', 'I'): 
        return f"{left}:{right}\n"
    
    text_translated = translate(right)
    return f"{left}:{text_translated}\n"


def process_file(file_in_path, file_out_path):    
    encoding = detect_encoding(file_in_path)
    try:
        with open(file_in_path, 'r', encoding=encoding) as file_in, open(file_out_path, 'w', encoding=encoding) as file_out:
            for line in file_in:
                line_aux = line.strip()
                line_modified = modify_line(line)
                file_out.write(line_modified)
    except:
        print(f"Error a {file_out_path}")


    with progress_lock:
        global progress
        progress += 1

def verify_directory(source_directory, new_directory, total_elements):
    global progress
    elements = [element for element in os.listdir(source_directory)]
    tasks = []

    with ThreadPoolExecutor(max_workers=4) as executor:
        for element in elements:
            full_path_in = os.path.join(source_directory, element)
            full_path_out = os.path.join(new_directory, element)

            if os.path.isdir(full_path_in):
                if not os.path.exists(full_path_out):
                    os.makedirs(full_path_out)
                verify_directory(full_path_in, full_path_out, total_elements)
                continue
            
            tasks.append(executor.submit(process_file, full_path_in, full_path_out))

        for future in as_completed(tasks):
            future.result()
            print(f"{progress}/{total_elements} arxius procesats.")

def main():
    current_directory = os.getcwd()
    source_directory = os.path.join(current_directory, source_directory_name)
    new_directory = os.path.join(current_directory, 'es-ES')

    if not os.path.exists(new_directory):
        os.makedirs(new_directory)

    total_elements = sum([len(files) for r, d, files in os.walk(source_directory)])
    print(f"Total elements a procesar: {total_elements}")

    verify_directory(source_directory, new_directory, total_elements)

if __name__ == "__main__":
    start_time = time.time()

    main()

    end_time = time.time()

    elapsed_time = end_time - start_time
    hours = elapsed_time // 3600
    minutes = (elapsed_time % 3600) // 60
    seconds = elapsed_time % 60

    print(f"Temps execució: {int(hours)} hores, {int(minutes)} min, {int(seconds)} seg")
