import argparse
from PIL import Image
import os

def convertir_bmp_a_png(ruta_archivo):
    try:
        # Comprobar si el archivo existe y es un BMP
        if not os.path.exists(ruta_archivo):
            raise FileNotFoundError("El archivo no existe.")
        if not ruta_archivo.lower().endswith('.bmp'):
            raise ValueError("El archivo no es un BMP.")

        # Abrir la imagen BMP
        with Image.open(ruta_archivo) as img:
            # Crear el nombre del nuevo archivo PNG
            ruta_png = os.path.splitext(ruta_archivo)[0] + '.png'
            
            # Guardar como PNG
            img.save(ruta_png, 'PNG')

        # Eliminar el archivo BMP original
        os.remove(ruta_archivo)
        
        print(f"Conversión exitosa: {ruta_archivo} -> {ruta_png}")
    except Exception as e:
        print(f"Error durante la conversión: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Convierte un archivo BMP a PNG y elimina el original.')
    parser.add_argument('ruta', help='Ruta del archivo BMP a convertir')
    args = parser.parse_args()

    convertir_bmp_a_png(args.ruta)

if __name__ == '__main__':
    main()
