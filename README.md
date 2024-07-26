# File Translator Script

Este script traduce el contenido de archivos de texto en un directorio de origen y guarda las traducciones en un directorio de destino. Utiliza el módulo `deep-translator` para realizar la traducción y `chardet` para detectar la codificación de los archivos.

## Requisitos

Antes de ejecutar el script, asegúrate de tener instalados los siguientes paquetes de Python:

```bash
pip install deep-translator
pip install chardet
```

## Configuración

Clona el proyecto y añade la carpeta en-US con toda la información (substituyendo la del repositorio). 

Una vez ejecutado el script copia la carpeta con las nuevas traduciones en la carpeta /AVEVA/Work Tasks/Locales tal como indica la documentación de AVEVA.

Debes proporcionar un archivo de configuración llamado `config.py` en el mismo directorio que el script. Este archivo debe definir las siguientes variables:

- `translate_from`: El idioma de origen para la traducción (por ejemplo, `'english'` para inglés).
- `translate_to`: El idioma de destino para la traducción (por ejemplo, `'spanish'` para español).
- `source_directory_name`: El nombre del directorio que contiene los archivos de origen. (Debería ser: `'en-US'`).
- `target_directory_name`: El nombre del directorio donde se guardarán los archivos traducidos. (Debería ser: `'xx-XX'`)

Ejemplo de `config.py`:

```python
translate_from = 'english'
translate_to = 'german'
source_directory_name = 'en-US'
target_directory_name = 'de-DE'
```

## Cómo Funciona

1. **Detección de Codificación**: El script detecta automáticamente la codificación de cada archivo usando `chardet`.
2. **Traducción**: Traduce el contenido de los archivos línea por línea usando `deep-translator`. Los caracteres de un solo carácter que no sean 'A' ni 'I' se mantienen sin cambios.
3. **Escritura de Archivos**: Guarda las traducciones en el directorio de destino especificado, manteniendo la estructura de directorios original.
4. **Busca por `:`**: Traducirá solo la parte derecha después del primer `:`.
## Uso

1. **Preparar el Directorio**: Asegúrate de que el directorio de origen contenga los archivos que deseas traducir y que el directorio de destino esté vacío o no exista.
2. **Ejecutar el Script**: Ejecuta el script en tu entorno Python:

    ```bash
    python script.py
    ```

## Funcionalidad

- **`detect_encoding(file_path)`**: Detecta la codificación de un archivo.
- **`translate(text)`**: Traduce el texto del idioma de origen al idioma de destino.
- **`modify_line(line)`**: Modifica una línea del archivo según la lógica especificada (traduce si no es un carácter de una sola letra que sea 'A' ni 'I').
- **`process_file(file_in_path, file_out_path)`**: Procesa un archivo de entrada y guarda el resultado en un archivo de salida.
- **`verify_directory(source_directory, new_directory, total_elements)`**: Verifica y traduce todos los archivos en un directorio, manteniendo la estructura de directorios.
- **`main()`**: Función principal que configura el directorio de origen y destino y calcula el número total de archivos a procesar.

## Ejemplo

Si tienes un archivo de texto `example.txt` en el directorio `source` con el contenido:

```
name:John
age:30
city:New York
```

Después de ejecutar el script, si estás traduciendo del inglés al español, el archivo `example.txt` en el directorio `target` podría verse así:

```
name:John
age:30
city:Nueva York
```
