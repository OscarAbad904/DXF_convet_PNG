import argparse
from PIL import Image
import os

def redimensionar_imagen(img, tamaño=(224, 224)):
    return img.resize(tamaño, Image.Resampling.LANCZOS)

def convertir_y_redimensionar_bmp(ruta_archivo):
    try:
        # Comprobar si el archivo es un BMP
        if not ruta_archivo.lower().endswith('.bmp'):
            return False

        # Abrir la imagen BMP
        with Image.open(ruta_archivo) as img:
            # Redimensionar la imagen
            img_redimensionada = redimensionar_imagen(img)
            
            # Crear el nombre del nuevo archivo PNG
            ruta_png = os.path.splitext(ruta_archivo)[0] + '.png'
            
            # Guardar como PNG
            img_redimensionada.save(ruta_png, 'PNG')

        # Eliminar el archivo BMP original
        os.remove(ruta_archivo)
        return True
    except Exception as e:
        print(f"Error durante la conversión de {ruta_archivo}: {str(e)}")
        return False

def redimensionar_png_existente(ruta_archivo):
    try:
        with Image.open(ruta_archivo) as img:
            # Redimensionar la imagen
            img_redimensionada = redimensionar_imagen(img)
            
            # Sobrescribir el archivo original
            img_redimensionada.save(ruta_archivo, 'PNG')
        return True
    except Exception as e:
        print(f"Error durante el redimensionamiento de {ruta_archivo}: {str(e)}")
        return False

def procesar_directorio(directorio):
    archivos_procesados = 0
    for root, dirs, files in os.walk(directorio):
        for file in files:
            ruta_completa = os.path.join(root, file)
            if file.lower().endswith('.bmp'):
                if convertir_y_redimensionar_bmp(ruta_completa):
                    archivos_procesados += 1
            elif file.lower().endswith('.png'):
                if redimensionar_png_existente(ruta_completa):
                    archivos_procesados += 1
    return archivos_procesados

def main():
    parser = argparse.ArgumentParser(description='Convierte archivos BMP a PNG, redimensiona todos los PNG a 224x224 y elimina los BMP originales.')
    parser.add_argument('directorio', help='Ruta del directorio que contiene los archivos a procesar')
    args = parser.parse_args()

    if not os.path.isdir(args.directorio):
        print(f"Error: {args.directorio} no es un directorio válido.")
        return

    total_procesados = procesar_directorio(args.directorio)
    print(f"Proceso terminado. {total_procesados} archivos procesados.")

if __name__ == '__main__':
    main()