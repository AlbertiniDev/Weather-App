import tkinter as tk
from weather_app import WeatherApp

def main():
    '''
    Punto de entrada principal de la aplicación.
    '''
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
