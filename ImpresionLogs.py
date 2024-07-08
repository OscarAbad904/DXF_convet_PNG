import os
import re
import sys
import pyautogui
import time
import subprocess
from tkinter import Tk, filedialog, messagebox

def leer_archivo(ruta_archivo):
    """Lee el archivo de texto y extrae las rutas de los archivos DWG sin duplicados."""
    rutas_dwg = set()
    try:
        with open(ruta_archivo, 'r', encoding='latin-1') as archivo:
            for linea in archivo:
                # Buscar las rutas de archivos DWG en las líneas del archivo de texto
                match = re.search(r'\\.*?\.dwg', linea, re.IGNORECASE)
                if match:
                    rutas_dwg.add(match.group(0))
    except UnicodeDecodeError as e:
        print(f'Error de decodificación: {e}')
    return list(rutas_dwg)

def mostrar_rutas(rutas):
    """Muestra un cuadro de mensaje con las rutas localizadas."""
    if rutas:
        rutas_str = "\n".join(rutas)
        messagebox.showinfo("Rutas Localizadas", f"Las rutas localizadas son:\n{rutas_str}")
    else:
        messagebox.showinfo("Rutas Localizadas", "No se encontraron rutas DWG.")

def abrir_autocad(ruta_autocad):
    """Abre AutoCAD LT."""
    ventana_autocad = pyautogui.getWindowsWithTitle("AutoCAD")
    if ventana_autocad:
        ventana_autocad[0].activate()
        time.sleep(2)
    else:
        try:
            subprocess.Popen([ruta_autocad])
            print(f'Abriendo AutoCAD LT')
            time.sleep(10)  # Esperar a que AutoCAD LT se abra completamente
            messagebox.showinfo("Información", "Si AutoCAD esta abieto, pulse Aceptar para continuar")
        except Exception as e:
            print(f'Error al abrir AutoCAD LT: {e}')
            sys.exit(1)

def abrir_dwg(rutas_dwg):
    """Abre los archivos DWG usando AutoCAD LT."""
    for ruta in rutas_dwg:
        try:
            print(f"Asegurarse de que AutoCAD LT esté en primer plano")
            # Asegurarse de que AutoCAD LT esté en primer plano
            ventana_autocad = pyautogui.getWindowsWithTitle("AutoCAD")
            if ventana_autocad:
                ventana_autocad[0].activate()
            else:
                print("No se encontró la ventana de AutoCAD.")
                continue
            time.sleep(1)
            
            # Abrir archivo
            print(f'Abrindo archivo {ruta}')
            pyautogui.hotkey('ctrl', 'o',interval=0.5)  # Abrir archivo
            time.sleep(1)
            pyautogui.typewrite(ruta)
            pyautogui.press('enter')
            time.sleep(2)  # Esperar a que el archivo se abra completamente
            messagebox.showinfo("Información", f'¿Se abrio el archivo {ruta}?, pulse Aceptar para continuar')
        except Exception as e:
            print(f'Error al abrir {ruta}: {e}')

if __name__ == "__main__":
    # Crear una ventana de diálogo para seleccionar el archivo de texto
    root = Tk()
    root.withdraw()  # Ocultar la ventana principal
    ruta_archivo_texto = filedialog.askopenfilename(
        title="Seleccionar archivo de texto",
        filetypes=[("Archivos de texto", "*.txt")]
    )

    if not ruta_archivo_texto:
        messagebox.showinfo("Información", 'No se seleccionó ningún archivo.')
        print('No se seleccionó ningún archivo.')
        sys.exit(1)

    if not os.path.exists(ruta_archivo_texto):
        messagebox.showinfo("Información", f'El archivo {ruta_archivo_texto} no existe.')
        print(f'El archivo {ruta_archivo_texto} no existe.')
        sys.exit(1)

    rutas_dwg = leer_archivo(ruta_archivo_texto)
    if not rutas_dwg:
        messagebox.showinfo("Información", 'No se encontraron archivos DWG en el archivo de texto.')
        print('No se encontraron archivos DWG en el archivo de texto.')
        sys.exit(1)

    ruta_autocad = "C:\\Program Files\\Autodesk\\AutoCAD LT 2024\\acadlt.exe"
    abrir_autocad(ruta_autocad)
    abrir_dwg(rutas_dwg)
    messagebox.showinfo("Información", "Proceso terminado")
    print(f'Proceso terminado')