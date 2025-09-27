import cv2
import pyzbar.pyzbar as pyzbar
from data.Alumnos import AlumnoData
from datetime import datetime, timedelta

from data.historial import Historial


def scan():
    """
    Escanea códigos QR y de barras utilizando pyzbar y OpenCV.
    Imprime en la terminal los códigos detectados, asegurándose de no
    imprimir el mismo código repetidamente.
    """
    # (0) para la cámara principal
    cap = cv2.VideoCapture(0) 
    now = datetime.now()
    last_detected_data = None
    horaEntrada = "19:05:00" 
    days = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
    horarios_salida = {
         "1A": {
            "Lunes":"23:05:00",
            "Martes":"23:05:00",
            "Miercoles":"23:05:00",
            "Jueves":"23:05:00",
            "Viernes":"23:05:00",
            "Sabado":"23:05:00",
            "Domingo":"19:10:00",},
         "1B": {
            "Lunes":"23:05:00",
            "Martes":"23:05:00",
            "Miercoles":"23:05:00",
            "Jueves":"23:05:00",
            "Viernes":"23:05:00",
            "Sabado":"23:05:00",
            "Domingo":"19:10:00",},
          "1C": {
            "Lunes":"23:05:00",
            "Martes":"23:05:00",
            "Miercoles":"23:05:00",
            "Jueves":"8:30:00",
            "viernes":"23:05:00",
            "Sabado":"23:05:00",
            "Domingo":"19:10:00",},
          "1D": {
            "Lunes":"23:05:00",
            "Martes":"23:05:00",
            "Miercoles":"23:05:00",
            "Jueves":"23:05:00",
            "Viernes":"23:05:00",
            "Sabado":"23:05:00",
            "Domingo":"19:10:00",
          } 



         }
   
    
   

    if not cap.isOpened():
        print("Error: No se pudo abrir la cámara.")
        return
  
    print("Escaneando códigos QR y de barras. Presione 'q' para salir.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: No se pudo leer el frame de la cámara.")
            break

        # Convierte la imagen a escala de grises para un mejor rendimiento
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Encuentra los códigos de barras en la imagen
        barcodes = pyzbar.decode(gray)

        # Itera sobre los códigos de barras detectados
        for barcode in barcodes:
            # Obtiene los datos del código de barras
            barcode_data = barcode.data.decode("utf-8")

            # Verifica si el código detectado es diferente al último
             # Verifica si el código detectado es diferente al último
            if barcode_data != last_detected_data:
                print("Nuevo código detectado.")
                print(barcode_data)
                now = datetime.now()
                dia_semana = days[now.weekday()]
                print(dia_semana + "  day")
                

                hora_actual = now.time() # Ejemplo: horaEntrada = "08:00:00"
                hora_entrada = datetime.strptime(horaEntrada.strip(), "%H:%M:%S").time()
                hora_limite = datetime.strptime("19:10:00", "%H:%M:%S").time()
                
                
                
                if hora_actual < hora_limite:  # Antes de las 19:05 se registra entrada
                    print("Antes de las 19:05 se registra entrada.")
                    if hora_actual <= hora_entrada:
                        print("se registró entrada normal")
                        print(f"Código detectado: Tipo = {barcode.type}, Datos = {barcode_data}")
                        AlumnoData.RegistrarScam(barcode_data, "Presente" )
                    else:
                        print("se registró entrada tarde")
                        
                        print(f"Código detectado: Tipo = {barcode.type}, Datos = {barcode_data}")
                        AlumnoData.RegistrarScam(barcode_data,"llegada Tarde")
                else:  # Después de las 19:05 se registra salida
                    print("Después de las 19:05 se registra salida.")
                    Alumno = Historial.BuscarNIE(barcode_data)
                    if Alumno and isinstance(Alumno, (list, tuple)) and len(Alumno) > 0:
                        alumno_data = Alumno[0]  # Primer resultado de la consulta
                        if len(alumno_data) > 1:
                            seccion = alumno_data[1]
                            if seccion in horarios_salida:
                                horaSalida = horarios_salida[seccion][dia_semana]
                                hora_salida_dt = datetime.strptime(horaSalida.strip(), "%H:%M:%S")
                                hora_actual_dt = datetime.combine(now.date(), hora_actual)
                                rango_final = hora_salida_dt + timedelta(minutes=10)

                                if hora_salida_dt <= hora_actual_dt <= rango_final:
                                    print("se registro salida")
                                    AlumnoData.RegistrarScam(barcode_data, "salida")
                                elif hora_actual_dt > rango_final:
                                    print("se registro salida tarde")
                                    AlumnoData.RegistrarScam(barcode_data, "salida Tarde")
                                else:
                                    print("Salió antes de la hora de salida")
                                    # Puedes registrar como "salida anticipada" o ignorar
                        else:
                            print("El resultado de alumno no tiene suficientes datos.")
                    else:
                        print("No se encontró el alumno o los datos están incompletos.")
            
            
            last_detected_data = barcode_data
            # Dibuja un recuadro alrededor del código de barras
            (x, y, w, h) = barcode.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2) 
            
            # Pone el texto con el tipo y los datos del código
            cv2.putText(frame, barcode_data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Muestra el frame con los recuadros
        cv2.imshow("Escáner de Códigos", frame)

        # Sale del bucle si se presiona 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Libera la cámara y cierra todas las ventanas
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    scan()