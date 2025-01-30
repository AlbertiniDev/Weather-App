import os, json
from pathlib import Path

def ruta_adjunto(archivo):
    '''
    Esta función recibe un nombre de archivo y retorna la ruta absoluta 
    del archivo correspondiente en el directorio de assets. 
    Si el archivo no está en las rutas predefinidas, lanza un ValueError.
    '''
    # Rutas para imagenes de la aplicación
    directorioScript = os.path.dirname(os.path.abspath(__file__))
    rutasRelativas = {
        "clear": "assets/clear_sky.png",
        "few_clouds": "assets/few_clouds.png",
        "scattered_clouds": "assets/scattered_clouds.png",
        "broken_clouds": "assets/broken_clouds.png",
        "shower_rain": "assets/shower_rain.png",
        "rain": "assets/rain.png",
        "thunderstorm": "assets/thunderstorm.png",
        "snow": "assets/snow.png",
        "mist": "assets/mist.png",
        "lista_climas" : "assets/lista_climas.json",
    }
    if archivo in rutasRelativas:
        rutaAbsoluta = os.path.join(directorioScript, rutasRelativas[archivo])
        return rutaAbsoluta
    else:
        raise ValueError(f"No se ha podido obtener la ruta de la imagen {archivo} en las rutas predefinidas")
    
def guardar_cadena_climas(lista_climas):
    '''
    Esta función guarda una lista de climas en un archivo JSON.
    '''
    archivoClimas = Path(ruta_adjunto("lista_climas"))
    climas = json.dumps(lista_climas, indent=4)
    archivoClimas.write_text(climas)

def abrir_cadena_climas(lista_climas):
    '''
    Esta función abre el archivo JSON de climas y carga su contenido en una lista.
    Si el archivo no existe, lo crea y guarda la lista de climas actual en él.
    '''
    archivoClimas = Path(ruta_adjunto("lista_climas"))
    try:
        contenido = archivoClimas.read_text()
    except FileNotFoundError:
        guardar_cadena_climas(lista_climas)
    else:
        climas = json.loads(contenido)
        for clima in climas:
            lista_climas.append(clima)