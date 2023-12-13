import tkinter as tk
from tkinter import ttk
from tkinter import *
from ttkthemes import ThemedStyle
import pandas as pd
import pyodbc
import ezdxf
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Arc
from PIL import Image
import os.path as path

def consulta_cd(cd_unico):
    try:
        conexion = pyodbc.connect('DRIVER={SQL Server};SERVER=SQLSERVER;UID=o.abad;Trusted_Connection=Yes;APP=2007 Microsoft Office system;WSID=EMEIND08')
        consulta_sql = f"SELECT * FROM DESPIECE_PEDIDOS WHERE CodLinea = '{cd_unico}'"
        
        RsConsulta = pd.read_sql(consulta_sql, conexion)

        return RsConsulta
    
    except Exception as e:
        print(f"Ha ocurrido un error: {e}")
        return None

def load_data(*event):
    try:
        # Ejecutar consulta SQL
        RsConsulta = consulta_cd(self_Main.TexBox.get())

        # Limpiar datos antiguos
        for Nodo in self_Main.tree.get_children():
            self_Main.tree.delete(Nodo)

        # Cargar datos
        if not RsConsulta.empty:
            for i, row in RsConsulta.iterrows():
                for column in RsConsulta.columns:
                    self_Main.tree.insert('', 'end', text="Item", values=(column, row[column]))

                    if column == 'RUTADXFGENERADO':
                        ruta_dxf = row[column]

                        #Rasterizar DXF a png
                        dxf_a_imagen(ruta_dxf, 'C:\Temp\DXF_Temp.png')

                        # Crear etiqueta con imagen
                        if path.exists('C:\Temp\DXF_Temp.png'):
                            imagen = tk.PhotoImage(file='C:\Temp\DXF_Temp.png')
                            self_Main.etiqueta.configure(image=imagen)
                            self_Main.etiqueta.image = imagen  # Guardar una referencia a la imagen

    except Exception as e:
        print(f"Ha ocurrido un error: {e}")
        return None

#Reordena por columna
def sortby(tree, col, descending):
    try:
        #Función para ordenar los datos
        data = [(self_Main.tree.set(child, col), child) for child in self_Main.tree.get_children('')]
        data.sort(reverse=descending)

        for ix, item in enumerate(data):
            self_Main.tree.move(item[1], '', ix)

        self_Main.tree.heading('#1', text='Nombre del campo')
        self_Main.tree.heading('#2', text='Valor')

        # Cambiar el texto del encabezado para incluir la flecha de ordenación
        if descending:
            self_Main.tree.heading(col, text=f'{col} ↓', command=lambda: sortby(tree, col, 0))
            self_Main.tree.heading(col, text=f'{col} ↓', command=lambda: sortby(tree, col, 0))
        else:
            self_Main.tree.heading(col, text=f'{col} ↑', command=lambda: sortby(tree, col, 1))
    except Exception as e:
        print(f"Ha ocurrido un error: {e}")
        return None

#Copia al portapapeles el valor de '#2' con Ctl+c
def copy_to_clipboard(*event):
    try:
        """Función para copiar al portapapeles."""
        selected_item = self_Main.tree.selection()[0]  # Obtener el elemento seleccionado
        value = self_Main.tree.item(selected_item, 'values')[1]  # Obtener el valor de la columna '#2'
        self_Main.clipboard_clear()  # Limpiar el portapapeles
        self_Main.clipboard_append(value)  # Añadir el valor al portapapeles

    except Exception as e:
        print(f"Ha ocurrido un error: {e}")
        return None
    
#Copia al portapapeles el valor de '#2' con clic derecho
def show_context_menu(event):
    try:
        """Función para mostrar el menú contextual."""
        self_Main.context_menu.tk_popup(event.x_root, event.y_root)

    except Exception as e:
        print(f"Ha ocurrido un error: {e}")
        return None

#Crea una imagen PNG de un archivo DXF
def dxf_a_imagen(ruta_dxf, ruta_imagen):
    try:
        # Leer el archivo DXF
        doc = ezdxf.readfile(ruta_dxf)

        # Crear un nuevo dibujo de Matplotlib
        fig, ax = plt.subplots()

        # Recorrer todas las entidades en los modelospace
        msp = doc.modelspace()

        for entidad in msp:
            if entidad.dxftype() == 'LINE':
                # Dibujar una línea desde el punto inicial al final
                plt.plot([entidad.dxf.start[0], entidad.dxf.end[0]], [entidad.dxf.start[1], entidad.dxf.end[1]], color='black', antialiased=True, linewidth=0.8)

            elif entidad.dxftype() == 'CIRCLE':
                # Dibujar un círculo
                circulo = Circle((entidad.dxf.center[0], entidad.dxf.center[1]), entidad.dxf.radius, fill=False, antialiased=True, linewidth=0.8)
                ax.add_patch(circulo)
            elif entidad.dxftype() == 'ARC':
                # Dibujar un arco
                arco = Arc((entidad.dxf.center[0], entidad.dxf.center[1]), 2*entidad.dxf.radius, 2*entidad.dxf.radius, theta1=entidad.dxf.start_angle, theta2=entidad.dxf.end_angle, fill=False, antialiased=True, linewidth=0.8)
                ax.add_patch(arco)

        # Ajustar los límites de la gráfica para que incluyan todas las entidades
        ax.axis('equal')
        
        # Eliminar las barras de las gráficas
        plt.box(False)
        
        # Eliminar los valores de los ejes
        plt.xticks([])
        plt.yticks([])

        # Guardar la figura como imagen
        plt.savefig(ruta_imagen, dpi=100)

    except Exception as e:
        print(f"Ha ocurrido un error: {e}")
        return None

#Clase de la self principal    
class self_Principal(tk.Tk):
    tree = None 
    etiqueta = None
    TexBox = None

    def __init__(self):
        super().__init__()    
        
        # Configura el estilo del encabezado
        estilo = ThemedStyle(self)
        estilo.theme_use('plastik') 

        self.title('Consulta Valores en Despiece')
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        Contenedor1 = ttk.Frame(self)
        Contenedor1.grid(row=0,column=0, sticky='nsew')
        Contenedor2 = ttk.Frame(self)
        Contenedor2.grid(row=1,column=0, sticky='nsew')

        # Hacer que la columna 0 se redimensione con la self
        Contenedor2.grid_rowconfigure(0, weight=1)

        # Crear entrada de texto
        label = ttk.Label(Contenedor1, text="Codigo unico")
        label.grid(row=0, column=0, padx=5, pady=5)
        self.TexBox = ttk.Entry(Contenedor1, justify='center')
        self.TexBox.grid(row=0, column=1, padx=5, pady=5)

        self.TexBox.bind('<Return>', load_data)

        # Crear botón
        button = ttk.Button(Contenedor1, text="Cargar datos", command=load_data)
        button.grid(row=0, column=2, padx=5, pady=5)

        # Crear tabla
        self.tree = ttk.Treeview(Contenedor2, columns=('Nombre del campo', 'Valor'))
        self.tree.column('#0', width=0, minwidth=0, stretch=tk.NO)  # Ocultar la columna 'Item'
        self.tree.heading('#1', text='Nombre del campo', command=lambda: sortby(self.tree, 'Nombre del campo', 0))
        self.tree.column('#1', width=250, minwidth=150)
        self.tree.heading('#2', text='Valor', command=lambda: sortby(self.tree, 'Valor', 0))
        self.tree.column('#2', width=650, minwidth=250)
        self.tree.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

        self.tree.bind('<Control-c>', copy_to_clipboard)

        # Crear menú contextual
        context_menu = tk.Menu(self, tearoff=0)
        context_menu.add_command(label="Copiar", command=copy_to_clipboard)

        # Añadir el evento de mostrar el menú contextual
        self.tree.bind('<Button-3>', show_context_menu)

        # Crear barra de desplazamiento
        scrollbar = ttk.Scrollbar(Contenedor2, orient='vertical', command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.etiqueta = ttk.Label(Contenedor2, image="")
        self.etiqueta.grid(row=0, column=2, sticky='ne', padx=5, pady=5)

        # Crear la lista de opciones
        Estilo = ThemedStyle(self)
        Estilos = Estilo.get_themes()

        # Crear una variable de tipo StringVar para almacenar el valor seleccionado
        variable = StringVar(self)

        # Crear la barra de menú
        barra_menu = Menu(self)

        # Añadir elementos al menú
        menu_estilos = Menu(barra_menu, tearoff=0)

        for estilo in Estilos:
            def cambiar_estilo(value=estilo):
                variable.set(value)
                Estilo.theme_use(value)
            menu_estilos.add_command(label=estilo, command=cambiar_estilo)

        barra_menu.add_cascade(label="Estilo", menu=menu_estilos)

        self.config(menu=barra_menu)
    def load_data(self):
        self.tree.delete(*self.tree.get_children())

self_Main = self_Principal()
self_Main.mainloop()