import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog as fd
from PIL import Image, ImageTk
import requests
from datetime import datetime
from data_analysis import mostrar_analisis
import rute_script as rs

class WeatherApp:
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("El Tiempo")
        self.raiz.geometry("800x600")
        self.lista_climas = []
        rs.abrir_cadena_climas(self.lista_climas)

        # Ruta de las imágenes de fondo
        self.ruta_fondo_dia = "assets/day_background.png"
        self.ruta_fondo_noche = "assets/night_background.png"

        # Intenta cargar el ícono personalizado para la ventana
        try:
            self.raiz.iconbitmap("assets/weather_icon.ico")
        except:
            print("El archivo 'weather_icon.ico' no se encontró. Usando icono por defecto.")

        # Cargar imágenes de fondo
        self.fondo_dia = Image.open(self.ruta_fondo_dia)
        self.fondo_noche = Image.open(self.ruta_fondo_noche)
        self.fondo_actual = ImageTk.PhotoImage(self.fondo_dia)

        self.fondo_label = tk.Label(self.raiz, image=self.fondo_actual)
        self.fondo_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.frame = tk.Frame(self.raiz, bg="#f0f0f0", bd=5)
        self.frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor="n")

        self.entry_ciudad = tk.Entry(self.frame, font=("Comic Sans MS", 14))
        self.entry_ciudad.place(relwidth=0.65, relheight=1)
        self.entry_ciudad.bind("<Return>", self.get_tiempo)  # Asociar el botón de "Intro" a la función get_weather

        self.boton_buscar = tk.Button(self.frame, text="Buscar", font=("Comic Sans MS", 14), command=self.get_tiempo)
        self.boton_buscar.place(relx=0.7, relheight=1, relwidth=0.3)

        self.resultado_frame = tk.Frame(self.raiz, bg="#4d4d4d", bd=10)
        self.resultado_frame.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.6, anchor="n")

        self.temperatura_label = tk.Label(self.resultado_frame, text="", font=("Comic Sans MS", 14), bg="#4d4d4d", fg="white")
        self.temperatura_label.grid(row=0, column=0, padx=10, pady=5)

        self.humedad_label = tk.Label(self.resultado_frame, text="", font=("Comic Sans MS", 14), bg="#4d4d4d", fg="white")
        self.humedad_label.grid(row=1, column=0, padx=10, pady=5)

        self.presion_label = tk.Label(self.resultado_frame, text="", font=("Comic Sans MS", 14), bg="#4d4d4d", fg="white")
        self.presion_label.grid(row=2, column=0, padx=10, pady=5)

        self.descripcion_label = tk.Label(self.resultado_frame, text="", font=("Comic Sans MS", 14), bg="#4d4d4d", fg="white")
        self.descripcion_label.grid(row=3, column=0, padx=10, pady=5)

        # Botón para mostrar análisis
        self.boton_analisis = tk.Button(self.raiz, text="Mostrar análisis", font=("Comic Sans MS", 14), command=self.show_analysis_handler)
        self.boton_analisis.place(relx=0.5, rely=0.9, anchor="s")

        # Menú
        self.menu = tk.Menu(self.raiz)
        self.raiz.config(menu=self.menu)

        self.menu_archivo = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Archivo", menu=self.menu_archivo)
        self.menu_archivo.add_command(label="Guardar como", command=self.guardar_como)
        self.menu_archivo.add_separator()
        self.menu_archivo.add_command(label="Salir", command=self.raiz.quit)

        # Variables de estado
        self.tiempo_data = None

        # Diccionario para mapear descripciones de clima a nombres de archivos de imagen
        self.tiempo_imagenes = {
            "clear sky": "clear_sky.png",
            "few clouds": "few_clouds.png",
            "scattered clouds": "scattered_clouds.png",
            "broken clouds": "broken_clouds.png",
            "shower rain": "shower_rain.png",
            "rain": "rain.png",
            "thunderstorm": "thunderstorm.png",
            "snow": "snow.png",
            "mist": "mist.png"
        }

        # Eventos para redimensionar
        self.raiz.bind("<Configure>", self.escalar_fondo)

    def escalar_fondo(self, event):
        # Redimensionar la imagen de fondo para ajustarse a la ventana
        if event.widget == self.raiz:
            ancho = event.width
            alto = event.height
            if 6 <= datetime.now().hour < 18:
                imagen_fondo = self.fondo_dia.resize((ancho, alto), Image.Resampling.LANCZOS)
            else:
                imagen_fondo = self.fondo_noche.resize((ancho, alto), Image.Resampling.LANCZOS)
            self.fondo_actual = ImageTk.PhotoImage(imagen_fondo)
            self.fondo_label.config(image=self.fondo_actual)

    def get_tiempo(self, event=None):
        self.ciudad = self.entry_ciudad.get()
        self.entry_ciudad.delete(0, tk.END)  # Borrar automáticamente el contenido del campo de entrada
        api_llave = "a4edcd1842aee9e45faa29a822c4c68a"  # Clave de API de OpenWeather
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={self.ciudad}&appid={api_llave}&units=metric&lang=es"
        respuesta = requests.get(url)
        if respuesta.status_code == 200:
            data = respuesta.json()
            self.tiempo_data = data  # Guardar los datos para el análisis posterior
            self.mostrar_tiempo(data)  # Muestra los datos del clima si la solicitud fue exitosa
        else:
            messagebox.showerror("Error", f"No se pudo obtener el clima para {self.ciudad}. Por favor, verifica el nombre de la ciudad e intenta nuevamente.")

    def mostrar_tiempo(self, data):
        try:
            principal = data['list'][0]['main']

            # Get datos iniciales
            temperatura = principal['temp']
            humedad = principal['humidity']
            presion = principal['pressure']
            descripcion = data['list'][0]['weather'][0]['description']

            # Set datos temporales de la busqueda actual
            self.temp_temperatura = temperatura
            self.temp_humedad = humedad
            self.temp_presion = presion
            self.temp_descripcion = descripcion

            if descripcion not in self.lista_climas:
                self.lista_climas.append(descripcion)
                rs.guardar_cadena_climas(self.lista_climas)

            self.temperatura_label.config(text=f"Temperatura: {temperatura}°C")
            self.humedad_label.config(text=f"Humedad: {humedad}%")
            self.presion_label.config(text=f"Presión: {presion} hPa")
            self.descripcion_label.config(text=f"Descripción: {descripcion}")

            # Cargar imagen del clima según la descripción
            print(descripcion)
            self.seleccionar_imagen(descripcion)

            # Actualiza la imagen de fondo según la hora del día
            if 6 <= datetime.now().hour < 18:
                ruta_imagen_fondo = self.ruta_fondo_dia
            else:
                ruta_imagen_fondo = self.ruta_fondo_noche

            imagen_fondo = Image.open(ruta_imagen_fondo)
            imagen_fondo = imagen_fondo.resize((self.raiz.winfo_width(), self.raiz.winfo_height()))
            self.fondo_actual = ImageTk.PhotoImage(imagen_fondo)
            self.fondo_label.config(image=self.fondo_actual)
            self.fondo_label.image = self.fondo_actual

        except KeyError as e:
            messagebox.showerror("Error", f"Error al procesar los datos: {e}")

    def show_analysis_handler(self):
        if self.tiempo_data:
            mostrar_analisis(self.tiempo_data)
        else:
            messagebox.showerror("Error", "No hay datos para mostrar el análisis.")

    def seleccionar_imagen(self, tipo_clima):
        if tipo_clima == "cielo claro":
            self.imagen_clima = self.cargar_imagen(rs.ruta_adjunto('clear'), (150, 150))
        if tipo_clima == "nubes" or tipo_clima == "algo de nubes":
            self.imagen_clima = self.cargar_imagen(rs.ruta_adjunto('few_clouds'), (150, 150))
        if tipo_clima == "nubes dispersas":
            self.imagen_clima = self.cargar_imagen(rs.ruta_adjunto('scattered_clouds'), (150, 150))
        if tipo_clima == "muy nuboso":
            self.imagen_clima = self.cargar_imagen(rs.ruta_adjunto('broken_clouds'), (150, 150))
        if tipo_clima == "lluvia ligera" or tipo_clima == "lluvia moderada":
            self.imagen_clima = self.cargar_imagen(rs.ruta_adjunto('rain'), (150, 150))
        if tipo_clima == "lluvia de gran intensidad":
            self.imagen_clima = self.cargar_imagen(rs.ruta_adjunto('shower_rain'), (150, 150))
        if tipo_clima == "nieve":
            self.imagen_clima = self.cargar_imagen(rs.ruta_adjunto('snow'), (150, 150))
        print(type(self.imagen_clima))
        self.imagen_label = tk.Label(self.resultado_frame, image=self.imagen_clima, bg="#4d4d4d")
        self.imagen_label.place(x=290, y=7)
        


    def cargar_imagen(self, ruta, size):
        '''
            Funcion para cargar una imagen, con la ruta de entrada y su tamaño en (x,y) en pixeles
            Se devolverá una instancia de la libreria PhotoImage con la ruta de la imagen ya reescalada
        '''
        imagen = Image.open(ruta)
        imagen = imagen.resize(size)
        return ImageTk.PhotoImage(imagen)    
    
    def guardar_como(self):
        rutaArchivo = fd.asksaveasfile(
            title="Guardar resultados del tiempo",
            initialdir='.',
            defaultextension='.txt',
            filetypes=[
                ('Archivos txt','*.txt'),('Todos los archivos','*.*')
            ]
        )
        rutaArchivo.write(
            f"Localización: {self.ciudad.title()}\n"
            f"Temperatura: {self.temp_temperatura} ºC\n"
            f"Humedad: {self.temp_humedad} %\n"
            f"Presion: {self.temp_presion} hPa\n"
            f"Descripcion: {self.temp_descripcion.capitalize()}"         
            )