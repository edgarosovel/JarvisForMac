import os
from DictionaryServices import *
from Cocoa import NSSpeechRecognizer, NSObject
import CoreFoundation as CF
import time
import subprocess
from random import randint
import speech_recognition as sr

temp_vol=None
NOMBRE="Jarvis"

#time.monotonic()

#os.system("open /Applications/Microsoft\ Word.app")
#osascript -e 'tell application "Safari" to open location "http://www.facebook.com"'
#osascript -e 'tell application "iTunes" to play'
#osascript -e 'tell application "iTunes" to pause'
#osascript -e 'tell application "iTunes" to next track'
#osascript -e 'tell application "iTunes" to previous track'
#osascript -e 'tell application "iTunes" to quit'
#osascript -e 'tell application "Unity" to launch'
#osascript -e 'set volume output volume x' x[0,100]
#osascript -e 'output volume of (get volume settings)'
#'tell application "iTunes" to get name of current track'
#activate application "Firefox"
#repeat 100 times
#    tell application "System Events" to keystroke "a" using command down
#    delay (random number from 0.5 to 5)
#end repeat

########################################
#FUNCIONES
def ejecutar_comando(cmd): #Executes cmd in terminal
    return os.system(cmd) #return 0 if succesful

def decir(string): #Speak text to speech
    if(string=="di"): #para el verbo 'di'
        global comando
        string = ""
        for i in range(1, len(comando)):
            string+=(str(comando[i])+" ")
    ejecutar_comando("say "+string)

def abrir_aplicacion(programa_url): #Open app
    global programa
    cmd = ejecutar_comando("open "+programa_url)
    if(cmd==0):
        decir(escoger_afirmacion_aleatoria())
        decir("abriendo "+programa)
    else:
        decir("Comando erroneo")

def applescript(cmd): #Execute osax (applescript)
    ejecutar_comando("osascript -e "+cmd)

def escoger_afirmacion_aleatoria(): #Gets random reply
    return respuestas[randint(0,len(respuestas)-1)]
 
def reset(): #Resets variables to ask a command again
    global verbo
    global programa
    global cmd
    global contenido
    global index
    global senial
    global senial_encontrada
    senial_encontrada=False
    index=None
    senial=None
    contenido=None
    verbo=None
    programa=None
    cmd=None

def obtener_volumen(): #Gets system volume
    stdout = subprocess.Popen("osascript -e 'output volume of (get volume settings)'", shell=True, stdout=subprocess.PIPE).stdout
    volumen = int(stdout.read()) #gets value echoed from terminal
    return volumen

def subir_volumen(a):
    vol = obtener_volumen()
    vol+=25
    set_volumen(vol)
    
def bajar_volumen(a):
    vol=obtener_volumen()
    vol-=25
    set_volumen(vol)

def set_volumen(volumen): #sets volume
    global temp_vol
    global comando
    if volumen=="set":
        volumen = revisar_si_hay_volumen(comando)
        if(volumen is None):
            decir("Número de volumen no especificado")
            return
    elif volumen=="0":
        global temp_vol
        temp_vol = obtener_volumen()
    elif volumen=="temp":
        volumen = temp_vol
    applescript("'set volume output volume "+str(volumen)+"'")
    if volumen>=100:
        decir("volumen al máximo")
    else:
        decir("volumen en "+str(volumen))
    #esperar 4 segundos si quiere incrementar o disminuir

def tell_application_to(aplicacion, accion): 
    applescript("'tell application \""+aplicacion+"\" to "+accion+"'")

def tell_itunes_to(accion):
    tell_application_to("itunes", accion)
    if(accion in ("play", "next track")):
        decir_la_cancion()      

def pausar_itunes(a):
    tell_itunes_to("pause")

def adelantar_itunes(a):
    tell_itunes_to("next track")
    decir_la_cancion()

def decir_la_cancion():
    decir("reproduciendo "+obtener_nombre_itunes())

def buscar_en_web(link_pag):
    global programa
    global comando
    string=""
    ya=False
    if(programa in busquedas):
        splt = busquedas[programa].split("|")
        string = splt[0].replace("%23","#")
        for i in range(1, len(comando)):
            if ya:
                string+=(str(comando[i])+splt[1])
            if(comando[i]==programa):
                ya=True
        abrir_aplicacion(link_pag+string)
        decir("Estos son los resultados para su búsqueda")
    else:
        decir("No se puede buscar en ese programa")
    
def atrasar_itunes(a):
    tell_itunes_to("previous track")

def reproducir_itunes(a):
    tell_itunes_to("play")

def cerrar_aplicacion(app):
    tell_application_to(app, "quit")

def obtener_nombre_itunes():
    stdout = subprocess.Popen("osascript -e 'tell app \"itunes\" to get name of current track'", shell=True, stdout=subprocess.PIPE).stdout
    nombre = str(stdout.read()).replace("b'","").replace("\\n'","").replace("(","").replace(")","").replace("&","y") #gets value echoed from terminal
    stdout = subprocess.Popen("osascript -e 'tell app \"itunes\" to get artist of current track'", shell=True, stdout=subprocess.PIPE).stdout
    artista = str(stdout.read()).replace("b'","").replace("\\n'","").replace("(","").replace(")","").replace("&","y") #gets value echoed from terminal
    string =str(nombre)+" de "+str(artista)
    return string

def revisar_si_hay_verbo(comando): #Checks if there's a primary command
    for x in comando:
        if x in verbos:
            #cortar el string comando
            return str(x)

def revisar_si_hay_programa(comando): #Checks if there's a secondary command
    for x in comando:
        if x in programas:
            #cortar el string comando
            return str(x)

def operacion(a):
    global comando
    op=obtener_operacion(comando)
    string=""
    for x in op:
        if x in ("entre", "sobre"):
            x="/"
        if x in ("por","x","X","×"):
            x="*"
        if x in ("mas","más"):
            x="+"
        if x =="menos":
            x="-"
        string+=x
        try:
            res="El resultado es "+str(eval(string))
        except ZeroDivisionError:
            res="Estás tratando de dividir entre cero. Si mee haces dividir entre cero mi chip podría explotar como un Gálaxy Nout 7, y no queremos eso, ¿verdád?" 
        except:
            res="Operacion no soportada"
    decir(res)
    
def get_hora(a):
    hora = str(time.strftime("%I"))
    if hora[0]=="0":
        hora=hora.replace("0","")
    minutos = str(time.strftime("%M"))
    if minutos[0]=="0":
        minutos=minutos.replace("0","")
    if(hora=="1"):
        string="Es la "
    else:
        string="Son las "
    decir(string+hora+" "+minutos+" "+time.strftime("%p"))

def get_fecha(a):
    dia = time.strftime("%A")
    num = time.strftime("%d")
    if num[0]=="0":
        num=num.replace("0","")    
    mes = time.strftime("%B")
    string = "Hoy es "+dias[dia]+" "+num+" de "+meses[mes]
    decir(string)

def revisar_si_hay_volumen(comando):
    encontrado=False
    for x in comando:
        if encontrado:
            return int(x)
        if x in ("a","en"):
            encontrado = True
    return None

def obtener_operacion(comando):
    encontrado=False
    lista=[]
    for x in comando:
        if encontrado:
            lista.append(x)
        if x == "es":
            encontrado=True
    return lista

def significado_de_palabra(a):
    global comando
    resultado=None
    if str(a) == "significado":
        try:
            palabra = comando[comando.index('de')+1]
        except:
            palabra=""
    else:
        try:
            palabra = comando[comando.index('significa')+1]
        except:
            palabra = ""
    rango = (0, len(palabra))
    resultado = DCSCopyTextDefinition(None, palabra, rango)
    if resultado==None:
        respuesta = "La palabra "+palabra+"no se encontró en el diccionario" 
    else:
        inicio = len(palabra)
        try:
            inicio = resultado.index('1')+1
        except:
            pass
        try:
            final = resultado.index(':')
        except:
            try:
                final = resultado.index('.')
            except:
                final= None
        if final is None:
            respuesta = resultado[inicio:len(resultado)-1]
        else:
            respuesta = resultado[inicio:final]
    decir(respuesta)

def salir(a):
    global salir
    salir=True
    decir("Cerrando programa. Hasta luego")

class SpeechRecognizer (NSObject):
    def init(self):
        commands = [ NOMBRE, "a","e","i","o","u" ]
        self.recognizer = NSSpeechRecognizer.alloc().init()
        self.recognizer.blocksOtherRecognizers()
        self.recognizer.setCommands_(commands)
        self.recognizer.startListening()
        self.recognizer.setDelegate_(self)

    def speechRecognizer_didRecognizeCommand_(self, recognizer, command):
        global senial
        senial = command
        self.recognizer.stopListening()
        CF.CFRunLoopStop(CF.CFRunLoopGetCurrent())

def esperar_senial():
    speech = SpeechRecognizer.alloc().init()
    CF.CFRunLoopRun()
    if senial is NOMBRE:
        return True
    else:
        return False

def google_speech_recognition():
    result=None
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("····Escuchando····")
        decir("Escuchando")
        audio = r.listen(source)
        try:
                # for testing purposes, we're just using the default API key
                # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
                # instead of `r.recognize_google(audio)`
            result = str(r.recognize_google(audio, language='es-US')).lower()
        except sr.UnknownValueError:
            result = "di No comprendí lo que dijo"
        except sr.RequestError as e:
            result = "di Error al conectar con el reconocimiento de voz de gugol"
        except:
            result = "di Error"
        print(result)
        return result

    

########################################
#DICCIONARIOS
verbos = { #Dictionary of primary commands
    'nada': decir,
    'pon' : {'open':abrir_aplicacion, 'tell_itunes':tell_itunes_to, 'set_vol':set_volumen},
    'poner' : {'open':abrir_aplicacion, 'tell_itunes':tell_itunes_to, 'set_vol':set_volumen},
    'di' : decir,
    'abre' : abrir_aplicacion,
    'significa' : significado_de_palabra,
    'abrir' : abrir_aplicacion,
    'cierra' : cerrar_aplicacion,
    'sierra' : cerrar_aplicacion,
    'cerrar' : cerrar_aplicacion,
    'es' : {'hora':get_hora,'fecha':get_fecha, 'operacion':operacion, 'significado':significado_de_palabra},
    'son':get_hora,
    'reproduce' : tell_itunes_to,
    'hablar': set_volumen,
    'busca':buscar_en_web,
    'buscar':buscar_en_web,
    #volumen
    'súbele' : subir_volumen,
    'subele' : subir_volumen,
    'bájale' : bajar_volumen,
    'bajale' : bajar_volumen,
    'subir' : subir_volumen,
    'bajar' : bajar_volumen,
    'sube' : subir_volumen,
    'baja' : bajar_volumen,
    'silencio' : set_volumen,
    'callate' : set_volumen,
    'cállate' : set_volumen,
    #canciones
    'pausa' : pausar_itunes,
    'quita' : pausar_itunes,
    'quitar' : pausar_itunes,
    'pausar' : pausar_itunes,
    'siguiente' : adelantar_itunes,
    'regresa' : atrasar_itunes,
    'continúa' : reproducir_itunes,
    'continua' : reproducir_itunes,
    'play' : reproducir_itunes,
    #
    'salir' : salir,
    }
                     
programas = { #Dictionary of secondary commands
    #redundantes
    'nada':"|okei",
    'di':"|di",
    'salir' : "|",
    'cállate' : "|0",
    'silencio' : "|0",
    'subele' : "|",
    'súbele' : "|",
    'bajale' : "|",
    'bájale' : "|",
    'play':"|",
    'significa':"|",
    #
    'siguiente' : "|next track", #redundante
    'regresa' : "|previous track", #redundante
    'pausar' : "|", #redundante
    'pausa' : "tell_itunes|pause",
    'otra' : "tell_itunes|next track",
    'canción' : "tell_itunes|play",
    'anterior' : "tell_itunes|previous track",
    'música' : "tell_itunes|play",
    'rola' : "tell_itunes|play",
    'rolita' : "tell_itunes|play",
    'hablar':"|temp",
    'hora': "hora|",
    'horas': "|",
    'dia':"fecha|",
    'día':"fecha|",
    'cuánto':"operacion|",
    'significado':"significado|significado",
    #
    'facebook': "open|https://www.facebook.com",
    'hotmail': "|https://www.outlook.com",
    'outlook': "|https://www.outlook.com",
    'correo': "|https://www.outlook.com",
    'gmail': "|https://mail.google.com",
    'twitter':"|/Applications/Twitter.app",
    'netflix':"open|http://www.netflix.com",
    'google':"|https://www.google.com.mx",
    'youtube':"open|https://www.youtube.com",
    #
    'ableton':"|/Applications/Ableton\ Live\ Suite.app",
    'illustrator':"|/Applications/Adobe\ Illustrator\ CC\ 2015/Adobe\ Illustrator\ CC\ 2015.app",
    'photoshop':"|/Applications/Adobe\ Photoshop\ CC\ 2014/Adobe\ Photoshop\ CC\ 2014.app",
    'store':"|/Applications/App\ Store.app",
    'blender':"|/Applications/Blender.app",
    'calendario':"|/Applications/Calendar.app",
    'evernote':"|/Applications/Evernote.app",
    'popcorn':"|/Applications/PopcornTime.app",
    'popcorntime':"|/Applications/PopcornTime.app",
    'sublime':"|/Applications/Sublime\ Text.app",
    'tor':"|/Applications/TorBrowser.app",
    'unity':"|/Applications/Unity/Unity.app",
    'word':"|/Applications/Microsoft\ Word.app",
    'excel':"|/Applications/Microsoft\ Excel.app",
    'itunes':"|/Applications/itunes.app",
    'safari':"|/Applications/safari.app",
    'mozilla':"|/Applications/firefox.app",
    'firefox':"|/Applications/firefox.app",
    'whats':"|/Applications/WhatsApp.app",
    'whatsapp':"|/Applications/WhatsApp.app",
    #
    'volumen':"set_vol|set"
    }

busquedas = {
    'google':"/#q=|+",
    'youtube':"/results?search_query=|+",
    'netflix':"/search/|%2520"
    }

verbo_respuestas = { #Conjugated replies
    'pon' : "poniendo",
    'abre' : "abriendo",
    'abrir' : "abriendo",
    }

dias = {
    'Monday':"Lunes",
    'Tuesday':"Martes",
    'Wednesday':"Miércoles",
    'Thursday':"Jueves",
    'Friday':"Viernes",
    'Saturday':"Sábado",
    'Sunday':"Domingo"
    }
meses = {
    'January':"Enero",
    'February':"Febrero",
    'March':"Marzo",
    'April':"Abril",
    'May':"Mayo",
    'June':"Junio",
    'July':"Julio",
    'August':"Agosto",
    'September':"Septiembre",
    'October':"Octubre",
    'November':"Noviembre",
    'December':"Diciembre"
    }

#Machine replies when executing a command                     
respuestas = ("a la orden", "en seguida", "por supuesto", "cómo ordene", "cómo guste", "con gusto","sí señor", "okei")


########################################
#PROGRAMA

index=None
contenido=None
senial=None
verbo=None
programa=None
salir = False
senial_encontrada=False
cmd=None
decir("Bienvenido. Para activarme solo diga "+NOMBRE+". Despúes diga el comando que desee que ejecute")

while not salir:
    reset()
    while not senial_encontrada:
        senial_encontrada=esperar_senial()
    comando = google_speech_recognition()
    comando = comando.split()
    verbo = revisar_si_hay_verbo(comando)
    if verbo is not None:
        programa = revisar_si_hay_programa(comando)
        if programa is not None:
            contenido = programas[programa].split("|")[1]
            if(callable(verbos[verbo])):
                verbos[verbo](contenido)
            else:
                index = programas[programa].split("|")[0]
                verbos[verbo][index](contenido)
        else:
            decir("Comando incompleto o desconcido.")   
    else:
        decir("No entendí el comando")
