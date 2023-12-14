import sys
import ezdxf
import matplotlib.pyplot as plt
from matplotlib.patches import * 

def DXF_convet_PNG():
    try:
        # Tomar las rutas desde los argumentos de la línea de comandos
        ruta_dxf = sys.argv[1]
        ruta_imagen = sys.argv[2]
        DPI = int(sys.argv[3])
        Ancho_Linea = float(sys.argv[4])

        # Leer el archivo DXF
        doc = ezdxf.readfile(ruta_dxf)

        # Crear un nuevo dibujo de Matplotlib
        fig, ax = plt.subplots()

        # Recorrer todas las entidades en los modelospace
        msp = doc.modelspace()

        for entidad in msp:
            capa = str(entidad.dxf.linetype).lower()
            print(f"{capa}")

            if capa=='continuous':
                Color='BLACK'
            else:
                Color='GREEN'

            if entidad.dxftype() == 'LINE':
                # Dibujar una línea desde el punto inicial al final
                plt.plot([entidad.dxf.start[0], entidad.dxf.end[0]], [entidad.dxf.start[1], entidad.dxf.end[1]], color=Color, antialiased=True, linewidth=Ancho_Linea)
            elif entidad.dxftype() == 'CIRCLE':
                # Dibujar un círculo
                circulo = Circle((entidad.dxf.center[0], entidad.dxf.center[1]), entidad.dxf.radius, fill=False, color=Color, antialiased=True, linewidth=Ancho_Linea)
                ax.add_patch(circulo)
            elif entidad.dxftype() == 'ARC':
                # Dibujar un arco
                arco = Arc((entidad.dxf.center[0], entidad.dxf.center[1]), 2*entidad.dxf.radius, 2*entidad.dxf.radius, theta1=entidad.dxf.start_angle, theta2=entidad.dxf.end_angle, fill=False, color=Color, antialiased=True, linewidth=Ancho_Linea)
                ax.add_patch(arco)
            elif entidad.dxftype() in 'LWPOLYLINE':
                # Dibujar una polilínea
                puntos = [punto for punto in entidad]
                plt.plot(*zip(*puntos), color=Color, antialiased=True, linewidth=Ancho_Linea)

        # Ajustar los límites de la gráfica para que incluyan todas las entidades
        ax.axis('equal')
        
        # Eliminar las barras de las gráficas
        plt.box(False)
        
        # Eliminar los valores de los ejes
        plt.xticks([])
        plt.yticks([])

        # Ajustar los márgenes
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

        # Guardar la figura como imagen
        plt.savefig(ruta_imagen, dpi=DPI, bbox_inches='tight', pad_inches=0)

        print(f"Proceso terminado correctamente")
    except Exception as e:
        print(f"Ha ocurrido un error: {e}")
        return None

DXF_convet_PNG()
