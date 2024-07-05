import argparse
from PIL import Image
import os

def convertir_bmp_a_png(ruta_archivo):
    try:
        # Comprobar si el archivo es un BMP
        if not ruta_archivo.lower().endswith('.bmp'):
            return False

        # Abrir la imagen BMP
        with Image.open(ruta_archivo) as img:
            # Crear el nombre del nuevo archivo PNG
            ruta_png = os.path.splitext(ruta_archivo)[0] + '.png'
            
            # Guardar como PNG
            img.save(ruta_png, 'PNG')

        # Eliminar el archivo BMP original
        os.remove(ruta_archivo)
        return True
    except Exception as e:
        print(f"Error durante la conversión de {ruta_archivo}: {str(e)}")
        return False

def procesar_directorio(directorio):
    archivos_convertidos = 0
    for root, dirs, files in os.walk(directorio):
        for file in files:
            if file.lower().endswith('.bmp'):
                ruta_completa = os.path.join(root, file)
                if convertir_bmp_a_png(ruta_completa):
                    archivos_convertidos += 1
    return archivos_convertidos

def main():
    parser = argparse.ArgumentParser(description='Convierte todos los archivos BMP a PNG en un directorio y elimina los originales.')
    parser.add_argument('directorio', help='Ruta del directorio que contiene los archivos BMP a convertir')
    args = parser.parse_args()

    if not os.path.isdir(args.directorio):
        print(f"Error: {args.directorio} no es un directorio válido.")
        return

    total_convertidos = procesar_directorio(args.directorio)
    print(f"Proceso terminado. {total_convertidos} archivos convertidos.")

if __name__ == '__main__':
    main()