
import sqlite3
import matplotlib.pyplot as plt
import numpy as np

def generar_grafica():
    try:
        # Conectar a la base de datos
        db = sqlite3.connect('estudiates.db')
        cursor = db.cursor()

        # Obtener todas las secciones únicas
        cursor.execute("SELECT DISTINCT seccion FROM Registros")
        secciones = [row[0] for row in cursor.fetchall()]

        # Definir los motivos
        motivos = ['Presente', 'Expulsión', 'Retiro por Tutor o Padres', 'Emergencia o Salud']

        # Diccionario para almacenar los datos
        data = {motivo: [] for motivo in motivos}

        # Obtener los datos de la base de datos
        for seccion in secciones:
            for motivo in motivos:
                cursor.execute("""
                    SELECT COUNT(*)
                    FROM Asistencias a
                    JOIN Registros r ON a.NIE = r.NIE
                    WHERE r.seccion = ? AND a.motivo = ?
                """, (seccion, motivo))
                count = cursor.fetchone()[0]
                data[motivo].append(count)

        # Cerrar la conexión a la base de datos
        cursor.close()
        db.close()

        # Aplicar un estilo de Matplotlib más moderno
        plt.style.use('seaborn-v0_8-darkgrid') # O 'ggplot', 'fivethirtyeight', etc.

        # Crear la gráfica de barras
        x = np.arange(len(secciones))  # the label locations
        width = 0.2  # the width of the bars
        multiplier = 0

        fig, ax = plt.subplots(layout='constrained')

        for attribute, measurement in data.items():
            offset = width * multiplier
            rects = ax.bar(x + offset, measurement, width, label=attribute)
            ax.bar_label(rects, padding=3)
            multiplier += 1

        # Add some text for labels, title and axes ticks
        ax.set_ylabel('Cantidad de Estudiantes')
        ax.set_title('Asistencia de Estudiantes por Sección y Motivo')
        ax.set_xticks(x + width, secciones)
        ax.legend(loc='upper left', ncols=1)
        ax.set_ylim(0, max(max(data.values(), default=[0])) + 10)


        # Guardar la gráfica con mayor resolución
        plt.savefig('grafica_asistencia.png', dpi=300)
        print("Gráfica generada exitosamente como 'grafica_asistencia.png'")

    except sqlite3.Error as e:
        print(f"Error al conectar o consultar la base de datos: {e}")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

if __name__ == '__main__':
    generar_grafica()
