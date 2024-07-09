import os
import re
import sys
import pyautogui
import time
import subprocess
import pyperclip
import tkinter as tk
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
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal

    # Crear una nueva ventana de diálogo
    dialog = tk.Toplevel(root)

    # Configurar el tamaño de la ventana
    dialog.geometry("1200x600")  # Ajusta el tamaño según tus necesidades

    # Añadir un widget de texto para mostrar las rutas
    text_widget = tk.Text(dialog)
    text_widget.pack(fill="both", expand=True)

    if rutas:
        rutas_str = "\n".join(rutas)
        text_widget.insert("end", f"Las rutas localizadas son:\n{rutas_str}")
    else:
        text_widget.insert("end", "No se encontraron rutas DWG.")
        messagebox.showinfo("Información", 'No se encontraron archivos DWG en el archivo de texto.')
        print('No se encontraron archivos DWG en el archivo de texto.')
        sys.exit(1)

def buscar_ventana_autocad():
    """Busca una ventana de AutoCAD abierta."""
    ventanas = pyautogui.getAllWindows()
    for ventana in ventanas:
        if "AutoCAD" in ventana.title:
            return ventana
    return None

def abrir_autocad(ruta_autocad):
    """Abre AutoCAD LT."""
    ventana_autocad = buscar_ventana_autocad()
    if ventana_autocad:
        ventana_autocad.activate()
        time.sleep(2)
    else:
        try:
            subprocess.Popen([ruta_autocad])
            print(f'Abriendo AutoCAD LT')
            time.sleep(10)  # Esperar a que AutoCAD LT se abra completamente
            messagebox.showinfo("Información", "Si AutoCAD está abierto, pulse Aceptar para continuar")
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
            
            # Copiar ruta al portapapeles
            pyperclip.copy(ruta)

            # Abrir archivo
            print(f'Abrindo archivo {ruta}')
            pyautogui.hotkey('ctrl', 'o',interval=0.1)  # Abrir archivo
            time.sleep(1)
            pyautogui.hotkey('ctrl', 'v', interval=0.1)  # Pegar ruta
            pyautogui.press('enter')
            time.sleep(2)
            
            # Mostrar cuadro de mensaje con opción de cancelar
            respuesta = messagebox.askokcancel("Información", f'¿Se abrió el archivo {ruta}?\n\nPulse Aceptar para continuar\n\nPulse Cancelar para finalizar el proceso')
            if not respuesta:
                messagebox.showinfo("Información", "Proceso cancelado por el usuario.")
                print("Proceso cancelado por el usuario.")
                sys.exit(1)
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
    
    mostrar_rutas(rutas_dwg)       

    ruta_autocad = "C:\\Program Files\\Autodesk\\AutoCAD LT 2024\\acadlt.exe"
    abrir_autocad(ruta_autocad)
    abrir_dwg(rutas_dwg)
    messagebox.showinfo("Información", "Proceso terminado")
    print(f'Proceso terminado')