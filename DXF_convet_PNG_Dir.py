import sys
import os
import ezdxf
import matplotlib.pyplot as plt
from matplotlib.patches import *

def DXF_convert_PNG(ruta_dxf, ruta_imagen, DPI, Ancho_Linea):
    try:
        # Leer el archivo DXF
        doc = ezdxf.readfile(ruta_dxf)

        # Crear un nuevo dibujo de Matplotlib
        fig, ax = plt.subplots()

        # Recorrer todas las entidades en los modelspace
        msp = doc.modelspace()

        ax.set_facecolor(((1/255) * 28, (1/255) * 37, (1/255) * 44))

        for entidad in msp:
            capa = str(entidad.dxf.linetype).lower()

            if capa == 'continuous':
                Color = (0.0, 0.0, 0.0)
            else:
                Color = 'GREEN'

            if entidad.dxftype() == 'LINE':
                plt.plot([entidad.dxf.start[0], entidad.dxf.end[0]], [entidad.dxf.start[1], entidad.dxf.end[1]], color=Color, antialiased=True, linewidth=Ancho_Linea)
            elif entidad.dxftype() == 'CIRCLE':
                circulo = Circle((entidad.dxf.center[0], entidad.dxf.center[1]), entidad.dxf.radius, fill=False, color=Color, antialiased=True, linewidth=Ancho_Linea)
                ax.add_patch(circulo)
            elif entidad.dxftype() == 'ARC':
                arco = Arc((entidad.dxf.center[0], entidad.dxf.center[1]), 2*entidad.dxf.radius, 2*entidad.dxf.radius, theta1=entidad.dxf.start_angle, theta2=entidad.dxf.end_angle, fill=False, color=Color, antialiased=True, linewidth=Ancho_Linea)
                ax.add_patch(arco)
            elif entidad.dxftype() in 'LWPOLYLINE':
                puntos = [punto for punto in entidad]
                plt.plot(*zip(*puntos), color=Color, antialiased=True, linewidth=Ancho_Linea)

        ax.axis('equal')
        plt.box(False)
        plt.xticks([])
        plt.yticks([])
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

        plt.savefig(ruta_imagen, dpi=DPI, bbox_inches='tight', pad_inches=0)
        plt.close(fig)  # Cerrar la figura para liberar memoria

        print(f"Archivo {ruta_dxf} convertido correctamente a {ruta_imagen}")
    except Exception as e:
        print(f"Ha ocurrido un error al procesar {ruta_dxf}: {e}")

def process_folder():
    try:
        # Tomar las rutas desde los argumentos de la línea de comandos
        ruta_carpeta = sys.argv[1]
        DPI = int(sys.argv[2])
        Ancho_Linea = float(sys.argv[3])

        # Verificar si la carpeta existe
        if not os.path.isdir(ruta_carpeta):
            print(f"La carpeta {ruta_carpeta} no existe.")
            return

        # Recorrer todos los archivos en la carpeta
        for filename in os.listdir(ruta_carpeta):
            if filename.lower().endswith('.dxf'):
                ruta_dxf = os.path.join(ruta_carpeta, filename)
                ruta_imagen = os.path.join(ruta_carpeta, os.path.splitext(filename)[0] + '.png')
                DXF_convert_PNG(ruta_dxf, ruta_imagen, DPI, Ancho_Linea)

        print("Proceso terminado correctamente")
    except Exception as e:
        print(f"Ha ocurrido un error: {e}")

if __name__ == "__main__":
    process_folder()