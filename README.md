#Jarvis para Mac
Asistente personal al estilo Siri.

Todo empezó porque cada vez que ponía una película o serie en Netflix en mi computadora que siempre conecto a mi televisión, me daba flojera volverme a levantarme de la comodidad de mi cama para subirle el volumen o para cambiar el contenido que estaba viendo. Es por eso que pensé que sería una gran idea tener un programa que respondiera a comandos de voz para que ejecute funciones hechas a la medida. Y así es como nació Jarvis.

#Flujo del sistema
Consta de un programa construido en Python 3.4 que incluye una variedad de librerías y APIs que permiten reconocer lo que el usuario dicta a la máquina, para que esta a su vez lo ejecute. El flujo del sistema es simple: al iniciar el programa de inmediato se pone a escuchar en busca de una palabra clave que el usuario pude cambiar a placer. En mi caso dejé la palabra “Jarvis”, haciendo referencia a la inteligencia artificial construida por el genio “Tony Stark”, de la famosa historieta “Iron Man”, la cual le funge como asistente personal. Una vez que el programa detecta que el usuario ha dicho la palabra, el programa reproduce un mensaje que aviso al usuario que ya puede empezar a dictar la orden que se desee que ejecute. Una vez que el usuario da la orden, el sistema actúa dependiendo a las palabras clave que encuentre en dicha frase.

#Librerías y API's usadas:
Os (operative system)– Como bien se sabe, una computadora puede ser controlada práctimante solo desde la consola. Esta librería nos permite la ejecución de comandos de consola desde el programa.
DictionaryServices – Librería propia de sistemas operativos MacOSm la cual nos permite obtener el significado de una palabra.
Cocoa – Nos permite accesar a diversas herramientas y funciones de MacOS, como el reconocimiento de voz pre-instalado en cada Macbook.
Subprocess . librería que nos ofrece más opciones de sistema. En este caso se utilizó para obtener datos desde la consola, como el volumen actual de la computadora.
Speech_recognition – Librería que consta de una variedad de APIs para conectar con servicios de reconocimintos de voz (voz a texto).

La idea era usar una librería que sirviera sin una conexión forzosa a internet, pero desgraciadamente las que existen actualmente, o son muy deficientes, o son de paga. Por eso la última opción fue ocupar el reconocimiento de voz de Google, el cual es uno de los mejores al momento, pero ocupa una conexión estable a internet. 

#Tareas que el sistema puede ejecutar
1.	Abrir los programas listados.
2.	Cerrar los programas listados.
3.	Realizar búsquedas en Google.
4.	Realizar búsquedas en Youtube.
5.	Realizar búsquedas en Netflix.
6.	Subir el volumen.
7.	Bajar el volumen.
8.	Asignar el volumen entre un número dado entre 0 y 100.
9.	Reproducir canciones en iTunes.
10.	Adelantar y atrasar canciones en iTunes.
11.	Pausar canciones de iTunes.
12.	Dar la fecha.
13.	Dar la hora.
14.	Dar el significado de palabras.
15.	Realizar operaciones aritméticas básicas (multiplicación, división, suma y resta, respetando el orden de los operadores).
16.	Decir cualquier frase.
