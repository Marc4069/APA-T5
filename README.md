# Sonido estéreo y ficheros WAVE

## Nom i cognoms

> [!Important]
> Introduzca a continuación su nombre y apellidos:
>
> Marc Nieto Muñoz

## Aviso Importante

> [!Caution]
> 
> El objetivo de esta tarea es manejar la lectura y escritura de ficheros binarios. Para ello, sólo se
> permite el uso de las funciones de la biblioteca `struct`. Aunque existen distintas bibliotecas que
> permiten manejar los ficheros WAVE de una manera más eficiente y sencilla, su uso está prohibido.
>
> ¿Quiere saber más?, consulte con el profesorado.

## Fecha de entrega: 24 de mayo a medianoche

## El formato WAVE

El formato WAVE es uno de los más extendidos para el almacenamiento y transmisión
de señales de audio. En el fondo, se trata de un tipo particular de fichero
[RIFF](https://en.wikipedia.org/wiki/Resource_Interchange_File_Format) (*Resource
Interchange File Format*), utilizado no sólo para señales de audio sino también para señales de
otros tipos, como las imágenes estáticas o en movimiento, o secuencias MIDI (aunque, en el caso
del MIDI, con pequeñas diferencias que los hacen incompatibles).

La base de los ficheros RIFF es el uso de *cachos* (*chunks*, en inglés). Cada cacho,
o subcacho, está encabezado por una cadena de cuatro caracteres ASCII, que indica el tipo del cacho,
seguido por un entero sin signo de cuatro bytes, que indica el tamaño en bytes de lo que queda de
cacho sin contar la cadena inicial y el propio tamaño. A continuación, y en función del tipo de
cacho, se colocan los datos que lo forman.

Todo fichero RIFF incluye un primer cacho que lo identifica como tal y que empieza por la cadena
`'RIFF'`. A continuación, después del tamaño del cacho y en otra cadena de cuatro caracteres,
se indica el tipo concreto de información que contiene el fichero. En el caso concreto de los
ficheros de audio WAVE, esta cadena es igual a `'WAVE'`, y el cacho debe contener dos
*subcachos*: el primero, de nombre `'fmt '`, proporciona la información de cómo está
codificada la señal. Por ejemplo, si es PCM lineal, ADPCM, etc., o si es monofónica o estéreo. El
segundo subcacho, de nombre `'data'`, incluye las muestras de la señal.

Dispone de una descripción detallada del formato WAVE en la página
[WAVE PCM soundfile format](http://soundfile.sapp.org/doc/WaveFormat/) de Soundfile.

## Audio estéreo

La mayor parte de los animales, incluidos los del género *homo sapiens sapiens* sanos y completos,
están dotados de dos órganos que actúan como transductores acústico-sensoriales (es decir, tienen dos
*oídos*). Esta duplicidad orgánica permite al bicho, entre otras cosas, determinar la dirección de
origen del sonido. En el caso de la señal de música, además, la duplicidad proporciona una sensación
de *amplitud espacial*, de realismo y de confort acústico.

En un principio, los equipos de reproducción de audio no tenían en cuenta estos efectos y sólo permitían
almacenar y reproducir una única señal para los dos oídos. Es el llamado *sonido monofónico* o
*monoaural*. Una alternativa al sonido monofónico es el *estereofónico* o, simplemente, *estéreo*. En
él, se usan dos señales independientes, destinadas a ser reproducidas a ambos lados del oyente: los
llamados *canal izquierdo* (**L**) y *derecho* (**R**).

Aunque los primeros experimentos con sonido estereofónico datan de finales del siglo XIX, los primeros
equipos y grabaciones de este tipo no se popularizaron hasta los años 1950 y 1960. En aquel tiempo, la
gestión de los dos canales era muy rudimentaria. Por ejemplo, los instrumentos se repartían entre los
dos canales, con unos sonando exclusivamente a la izquierda y el resto a la derecha. Es el caso de las
primeras grabaciones en estéreo de los Beatles: las versiones en alemán de los singles *She loves you*
y *I want to hold your hand*. Así, en esta última (de la que dispone de un fichero en Atenea con sus
primeros treinta segundos, [Komm, gib mir deine Hand](wav/komm.wav)), la mayor parte de los instrumentos
suenan por el canal derecho, mientras que las voces y las características palmas lo hacen por el izquierdo.

Un problema habitual en los primeros años del sonido estereofónico, y aún vigente hoy en día, es que no
todos los equipos son capaces de reproducir los dos canales por separado. La solución comúnmente
adoptada consiste en no almacenar cada canal por separado, sino en la forma semisuma, $(L+R)/2$, y
semidiferencia, $(L-R)/2$, y de tal modo que los equipos monofónicos sólo accedan a la primera de ellas.
De este modo, estos equipos pueden reproducir una señal completa, formada por la suma de los dos
canales, y los estereofónicos pueden reconstruir los dos canales estéreo.

Por ejemplo, en la radio FM estéreo, la señal, de ancho de banda 15 kHz, se transmite del modo siguiente:

- En banda base, $0\le f\le 15$ kHz, se transmite la suma de los dos canales, $L+R$. Esta es la señal
  que son capaces de reproducir los equipos monofónicos.

- La señal diferencia, $L-R$, se transmite modulada en amplitud con una frecuencia de portadora
  $f_m = 38$ kHz.

  - Por tanto, ocupa la banda $23 \mathrm{kHz}\le f\le 53 \mathrm{kHz}$, que sólo es accedida por los
    equipos estéreo, y, en el caso de colarse en un reproductor monofónico, ocupa la banda no audible.

- También se emite una sinusoide de $19 \mathrm{kHz}$, denominada *señal piloto*, que se usa para
  demodular síncronamente la señal diferencia.

- Finalmente, la señal de audio estéreo puede acompañarse de otras señales de señalización y servicio en
  frecuencias entre $55.35 \mathrm{kHz}$ y $94 \mathrm{kHz}$.

En los discos fonográficos, la semisuma de las señales está grabada del mismo modo que se haría en una
grabación monofónica, es decir, en la profundidad del surco; mientras que la semidiferencia se graba en el
desplazamiento a izquierda y derecha de la aguja. El resultado es que un reproductor mono, que sólo atiende
a la profundidad del surco, reproduce casi correctamente la señal monofónica, mientras que un reproductor
estéreo es capaz de separar los dos canales. Es posible que algo de la información de la semisuma se cuele
en el reproductor mono, pero, como su amplitud es muy pequeña, se manifestará como un ruido muy débil,
apenas perceptible.

En general, todos estos sistemas se basan en garantizar que el reproductor mono recibe correctamente la
semisuma de canales y que, si algo de la semidiferencia se cuela en la reproducción, sea en forma de un
ruido inaudible.

## Tareas a realizar

Escriba el fichero `estereo.py` que incluirá las funciones que permitirán el manejo de los canales de una
señal estéreo y su codificación/decodificación para compatibilizar ésta con sistemas monofónicos.


### Manejo de los canales de una señal estéreo

En un fichero WAVE estéreo con señales de 16 bits, cada muestra de cada canal se codifica con un entero de
dos bytes. La señal se almacena en el *cacho* `'data'` alternando, para cada muestra de $x[n]$, el valor
del canal izquierdo y el derecho:

<img src="img/est%C3%A9reo.png" width="380px">

#### Función `estereo2mono(ficEste, ficMono, canal=2)`

La función lee el fichero `ficEste`, que debe contener una señal estéreo, y escribe el fichero `ficMono`,
con una señal monofónica. El tipo concreto de señal que se almacenará en `ficMono` depende del argumento
`canal`:

- `canal=0`: Se almacena el canal izquierdo $L$.
- `canal=1`: Se almacena el canal derecho $R$.
- `canal=2`: Se almacena la semisuma $(L+R)/2$. Ha de ser la opción por defecto.
- `canal=3`: Se almacena la semidiferencia $(L-R)/2$.

#### Función `mono2estereo(ficIzq, ficDer, ficEste)`

Lee los ficheros `ficIzq` y `ficDer`, que contienen las señales monofónicas correspondientes a los canales
izquierdo y derecho, respectivamente, y construye con ellas una señal estéreo que almacena en el fichero
`ficEste`.

### Codificación estéreo usando los bits menos significativos

En la línea de los sistemas usados para codificar la información estéreo en señales de radio FM o en los
surcos de los discos fonográficos, podemos usar enteros de 32 bits para almacenar los dos canales de 16 bits:

- En los 16 bits más significativos se almacena la semisuma de los dos canales.

- En los 16 bits menos significativos se almacena la semidiferencia.

Los sistemas monofónicos sólo son capaces de manejar la señal de 32 bits. Esta señal es prácticamente
idéntica a la señal semisuma, ya que la semisuma ocupa los 16 bits más significativos. La señal
semidiferencia aparece como un ruido añadido a la señal, pero, como su amplitud es $2^{16}$ veces más
pequeña, será prácticamente inaudible (la relación señal a ruido es del orden de 90 dB).

Los sistemas estéreo son capaces de aislar las dos partes de la señal y, con ellas, reconstruir los dos
canales izquierdo y derecho.

<img src="img/est%C3%A9reo_cod.png" width="510px">

#### Función `codEstereo(ficEste, ficCod)`

Lee el fichero `ficEste`, que contiene una señal estéreo codificada con PCM lineal de 16 bits, y
construye con ellas una señal codificada con 32 bits que permita su reproducción tanto por sistemas
monofónicos como por sistemas estéreo preparados para ello.

#### Función `decEstereo(ficCod, ficEste)`

Lee el fichero `ficCod` con una señal monofónica de 32 bits en la que los 16 bits más significativos
contienen la semisuma de los dos canales de una señal estéreo y los 16 bits menos significativos la
semidiferencia, y escribe el fichero `ficEste` con los dos canales por separado en el formato de los
ficheros WAVE estéreo.

### Entrega

#### Fichero `estereo.py`

- El fichero debe incluir una cadena de documentación que incluirá el nombre del alumno y una descripción
  del contenido del fichero.

- Es muy recomendable escribir, además, sendas funciones que *empaqueten* y *desempaqueten* las cabeceras
  de los ficheros WAVE a partir de los datos contenidos en ellas.

- Aparte de `struct`, no se puede importar o usar ningún módulo externo.

- Se deben evitar los bucles. Se valorará el uso, cuando sea necesario, de *comprensiones*.

- Los ficheros se deben abrir y cerrar usando gestores de contexto.

- Las funciones deberán comprobar que los ficheros de entrada tienen el formato correcto y, en caso
  contrario, elevar la excepción correspondiente.

- Los ficheros resultantes deben ser reproducibles correctamente usando cualquier reproductor estándar;
  por ejemplo, el Windows Media Player o similar. Es probable, muy probable, que tenga que modificar los
  datos de las cabeceras de los ficheros para conseguirlo.

- Se valorará lo pythónico de la solución; en concreto, su claridad y sencillez, y el uso de los estándares
  marcados por PEP-ocho.

#### Comprobación del funcionamiento

Es responsabilidad del alumno comprobar que las distintas funciones realizan su cometido de manera correcta.
Para ello, se recomienda usar la canción [Komm, gib mir deine Hand](wav/komm.wav), suminstrada al efecto.
De todos modos, recuerde que, aunque sea en alemán, se trata de los Beatles, así que procure no destrozar
innecesariamente la canción.
<img width="812" height="97" alt="comprobacion" src="https://github.com/user-attachments/assets/6808d34f-2696-40d3-9c1a-1b4c3bdee993" />
#### Código desarrollado

Inserte a continuación el código de los métodos desarrollados en esta tarea, usando los comandos necesarios
para que se realice el realce sintáctico en Python del mismo (no vale insertar una imagen o una captura de
pantalla, debe hacerse en formato *markdown*).
```python
"""
Autor: Marc Nieto Muñoz

Módulo especializado en la manipulación y procesamiento de señales de audio estéreo
y mono en formato WAVE de 16 y 32 bits mediante la librería estructurada de Python.
"""

import struct

def empaquetar_cabecera(num_channels, sample_rate, bits_sample, data_size):
    """
    Genera el bloque de bytes correspondiente a la cabecera estructurada de un archivo WAVE.
    
    Parámetros:
        num_channels: Cantidad de canales de audio (1 para mono, 2 para estéreo).
        sample_rate: Frecuencia de muestreo en Hz.
        bits_sample: Resolución de bits por muestra (ej. 16 o 32).
        data_size: Tamaño total en bytes de la sección de datos de audio.
    """
    byte_rate = sample_rate * num_channels * bits_sample // 8
    block_align = num_channels * bits_sample // 8
    riff_size = 36 + data_size # Suma de los bloques RIFF (12 bytes) y FMT (24 bytes)
    
    return (
        struct.pack('4sI4s', b'RIFF', riff_size, b'WAVE') +
        struct.pack('<4sIHHIIHH', b'fmt ', 16, 1, num_channels, 
                    sample_rate, byte_rate, block_align, bits_sample) +
        struct.pack('<4sI', b'data', data_size)
    )

def desempaquetar_cabecera(f):
    """
    Analiza y extrae las especificaciones técnicas de la cabecera de un archivo de audio.
    
    Retorna un diccionario con los metadatos esenciales del flujo WAVE o lanza una 
    excepción si el formato no es válido o compatible.
    """
    f.seek(0)
    riff, _, wave = struct.unpack('<4sI4s', f.read(12))
    if riff != b'RIFF' or wave != b'WAVE':
        raise TypeError('El archivo proporcionado no tiene un contenedor WAVE válido')
        
    data_offset = None
    data_size = None
    audio_format = None
    num_channels = None
    sample_rate = None
    bits_sample = None
    
    while True:
        cabecera = f.read(8)
        if len(cabecera) < 8:
            break
        chunk_id, chunk_size = struct.unpack('<4sI', cabecera)
        if chunk_id == b'fmt ':
            fmt_data = f.read(chunk_size)
            audio_format, num_channels, sample_rate, byte_rate, block_align, bits_sample = struct.unpack('<HHIIHH', fmt_data[:16])
        elif chunk_id == b'data':
            data_offset = f.tell()
            data_size = chunk_size
            f.seek(chunk_size, 1)
        else:
            f.seek(chunk_size, 1)
            
    if audio_format != 1 or bits_sample not in (16, 32):
        raise TypeError("Formato incompatible: se requiere codificación PCM lineal (16 o 32 bits)")
        
    return {
        'num_channels': num_channels,
        'sample_rate': sample_rate,
        'bits_sample': bits_sample,
        'data_offset': data_offset,
        'data_size': data_size
    }

 
def estereo2mono(ficEste, ficMono, canal=2):
    """
    Transforma un flujo de audio estéreo en una pista monofónica.
    
    Opciones del parámetro 'canal':
        0: Extrae únicamente el canal izquierdo.
        1: Extrae únicamente el canal derecho.
        2: Calcula el promedio (semisuma) de ambos canales.
        3: Calcula la semidiferencia espectral de los canales.
    """
    with open(ficEste, 'rb') as fpEstereo:
        info = desempaquetar_cabecera(fpEstereo)
        if info['num_channels'] != 2:
            raise TypeError("Operación cancelada: El archivo de origen debe ser estéreo")
        fpEstereo.seek(info['data_offset'])
        datos = fpEstereo.read(info['data_size'])

    muestras = struct.unpack('<' + 'h' * (info['data_size'] // 2), datos)
    pares = zip(muestras[::2], muestras[1::2]) # Separación en tuplas (izq, der)

    if canal == 0:
        salida = [l for l, r in pares]
    elif canal == 1:
        salida = [r for l, r in pares]
    elif canal == 2:
        salida = [((l + r) // 2) for l, r in pares]
    elif canal == 3:
        salida = [((l - r) // 2) for l, r in pares]
    else:
        raise TypeError('Identificador de canal incorrecto (use valores de 0 a 3)')
    
    datos_mono = struct.pack('<' + 'h' * len(salida), *salida)

    with open(ficMono, 'wb') as f:
        f.write(empaquetar_cabecera(1, info['sample_rate'], 16, len(datos_mono)))
        f.write(datos_mono)

def mono2estereo(ficIzq, ficDer, ficEste):
    """
    Fusiona dos fuentes de audio independientes (canal izquierdo y canal derecho)
    para consolidar un único archivo con señal estéreo.
    """
    with open(ficIzq, 'rb') as fpIzq:
        info_izq = desempaquetar_cabecera(fpIzq)
        if info_izq['num_channels'] != 1:
            raise TypeError("El archivo asignado a la izquierda no es monofónico")
        fpIzq.seek(info_izq['data_offset'])
        datos_izq = struct.unpack('<' + 'h' * (info_izq['data_size'] // 2), fpIzq.read(info_izq['data_size']))
    
    with open(ficDer, 'rb') as fpDer:
        info_der = desempaquetar_cabecera(fpDer)
        if info_der['num_channels'] != 1:
            raise TypeError("El archivo asignado a la derecha no es monofónico")
        fpDer.seek(info_der['data_offset'])
        datos_der = struct.unpack('<' + 'h' * (info_der['data_size'] // 2), fpDer.read(info_izq['data_size']))

    # Intercala las muestras de ambos canales en un único flujo estéreo
    datos_estereo = struct.pack('<' + 'h' * (2 * len(datos_izq)),
                                *sum(zip(datos_izq, datos_der), ()))
                                
    with open(ficEste, 'wb') as fpEste:
        fpEste.write(empaquetar_cabecera(2, info_izq['sample_rate'], 16, len(datos_estereo)))
        fpEste.write(datos_estereo)

def codEstereo(ficEste, ficCod):
    """
    Codifica un flujo estéreo estándar de 16 bits en una señal de 32 bits.
    
    Este proceso empaqueta la información MS (Mid/Side): la semisuma se almacena
    en los 16 bits superiores (compatibilidad mono) y la semidiferencia en los 
    16 bits inferiores.
    """
    with open(ficEste, 'rb') as fp:
        info = desempaquetar_cabecera(fp)
        if info['num_channels'] != 2:
            raise TypeError("Se requiere un archivo estéreo nativo para realizar la codificación")
        fp.seek(info['data_offset'])
        datos = struct.unpack('<' + 'h' * (info['data_size'] // 2), fp.read(info['data_size']))

    pares = zip(datos[::2], datos[1::2])
    # Desplazamiento bitwise para fusionar semisuma (High Word) y semidiferencia (Low Word)
    codificados = [((l + r) << 16) & 0xFFFF0000 | ((l - r) & 0xFFFF) for l, r in pares]

    datos_cod = struct.pack('<' + 'I' * len(codificados), *codificados)

    with open(ficCod, 'wb') as fpDos:
        fpDos.write(empaquetar_cabecera(1, info['sample_rate'], 32, len(datos_cod)))
        fpDos.write(datos_cod)

def decEstereo(ficCod, ficEste):
    """
    Decodifica una señal de 32 bits previamente combinada para restaurar y reconstruir
    los canales originales izquierdo y derecho en un formato estéreo estándar.
    """
    with open(ficCod, 'rb') as fpCod:
        info = desempaquetar_cabecera(fpCod)
        if info['bits_sample'] != 32:
            raise TypeError('El archivo origen no cumple con la resolución requerida de 32 bits')
        fpCod.seek(info['data_offset'])
        datos = struct.unpack('<' + 'I' * (info['data_size'] // 4), fpCod.read(info['data_size']))

        reconstruidos = []

        for cod in datos:
            # Segmentación de componentes mediante operaciones de máscara binaria
            suma = (cod >> 16) & 0xFFFF
            diff_raw = cod & 0xFFFF
            
            # Interpretación de los valores binarios como enteros de 16 bits con signo
            suma = struct.unpack('<h', struct.pack('<H', diff_raw))[0]
            diff = struct.unpack('<h', struct.pack('<H', diff_raw))[0]
            
            izq = (suma + diff) // 2
            der = (suma - diff) // 2
            
            # Recomposición de la estructura de canales entrelazados
            reconstruidos.append(int(izq)) 
            reconstruidos.append(int(der)) 

    datos_estereo = struct.pack('<' + 'h' * len(reconstruidos), *reconstruidos)

    with open(ficEste, 'wb') as fpEste:
         fpEste.write(empaquetar_cabecera(2, info['sample_rate'], 16, len(datos_estereo)))
         fpEste.write(datos_estereo)
         ```
##### Código de `estereo2mono()`

```python
def estereo2mono(ficEste, ficMono, canal=2):
    '''
    Convierte un archivo (ficEste) de estéreo a mono, el fichero mono resultante
    dependerá del argumento canal; 0 para canal izquierdo, 1 para canal derecho,
    2 para la semisuma y 3 para la semidiferencia.
    '''
    with open(ficEste, 'rb') as fpEstereo:
        info = desempaquetar_cabecera(fpEstereo)
        if info ['num_channels'] != 2:
            raise TypeError("El fichero no es estéreo")
        fpEstereo.seek(info['data_offset'])
        datos = fpEstereo.read(info['data_size'])

    muestras = struct.unpack('<' + 'h' * (info['data_size'] // 2), datos)
    pares = zip(muestras[::2], muestras[1::2]) #izquierda, derecha

    if canal == 0:
        salida = [l for l, r in pares]
    elif canal ==1:
        salida = [r for l, r in pares]
    elif canal == 2:
        salida = [((l+r) // 2) for l, r in pares]
    elif canal == 3:
        salida = [((l-r) // 2) for l, r in pares]
    else:
        raise TypeError('canal no válido')
    
    datos_mono = struct.pack('<' + 'h' * len(salida), *salida)

    with open(ficMono, 'wb') as f:
        f.write(empaquetar_cabecera(1, info['sample_rate'], 16, len(datos_mono)))
        f.write(datos_mono)
```
##### Código de `mono2estereo()`

```python
def mono2estereo(ficIzq, ficDer, ficEste):
    '''
    A partir de dos ficheros mono, uno que corresponde al canal izquierdo y otro al derecho, 
    crea un archivo estéreo
    '''
    with open(ficIzq, 'rb') as fpIzq:
        info_izq = desempaquetar_cabecera(fpIzq)
        if info_izq['num_channels'] !=1:
            raise TypeError("El fichero no es mono")
        fpIzq.seek(info_izq['data_offset'])
        datos_izq = struct.unpack('<' + 'h' * (info_izq['data_size'] // 2), fpIzq.read(info_izq['data_size']))
    
    with open(ficDer, 'rb') as fpDer:
        info_der = desempaquetar_cabecera(fpDer)
        if info_der['num_channels'] != 1:
            raise TypeError("El fichero no es mono")
        fpDer.seek(info_der['data_offset'])
        datos_der = struct.unpack('<' + 'h' * (info_der['data_size'] // 2), fpDer.read(info_izq['data_size']))

    datos_estereo = struct.pack('<' + 'h' * (2 * len(datos_izq)),
                                *sum(zip(datos_izq, datos_der), ()))
    with open(ficEste, 'wb') as fpEste:
        fpEste.write(empaquetar_cabecera(2, info_izq['sample_rate'], 16, len(datos_estereo)))
        fpEste.write(datos_estereo)
```
##### Código de `codEstereo()`
```python
def codEstereo(ficEste, ficCod):
    '''
    Lee el fichero ficEste, que contiene una señal estéreo codificada con PCM lineal de 16 bits,
    y construye con ellas una señal codificada con 32 bits que permita su reproducción
    tanto por sistemas monofónicos como por sistemas estéreo preparados para ello
    '''
    with open(ficEste, 'rb') as fp:
        info = desempaquetar_cabecera(fp)
        if info['num_channels'] != 2:
            raise TypeError("El fichero no es estéreo")
        fp.seek(info['data_offset'])
        datos = struct.unpack('<' + 'h' * (info['data_size'] // 2), fp.read(info['data_size']))

    pares = zip(datos[::2], datos[1::2])
    codificados = [((l + r) << 16) & 0xFFFF0000 | ((l - r) & 0xFFFF) for l, r in pares]

    datos_cod = struct.pack('<' + 'I' * len(codificados), *codificados)

    with open(ficCod, 'wb') as fpDos:
        fpDos.write(empaquetar_cabecera(1, info['sample_rate'], 32, len(datos_cod)))
        fpDos.write(datos_cod)
```
##### Código de `decEstereo()`
```python
def decEstereo(ficCod, ficEste):
    '''
    Lee el fichero ficCod con una señal monofónica de 32 bits en la que 
    los 16 bits más significativos contienen la semisuma de los 
    dos canales de una señal estéreo y los 16 bits menos significativos la semidiferencia,
    y escribe el fichero ficEste con los dos canales por separado en el formato de los ficheros WAVE estéreo
    '''
    with open(ficCod, 'rb') as fpCod:
        info = desempaquetar_cabecera(fpCod)
        if info['bits_sample'] != 32:
            raise TypeError('El fichero no está codificado en 32 bits')
        fpCod.seek(info['data_offset'])
        datos = struct.unpack('<' + 'I' * (info['data_size'] // 4), fpCod.read(info['data_size']))

        reconstruidos = []

        for cod in datos:
            suma = (cod >> 16) & 0xFFFF
            diff_raw = cod & 0xFFFF
            # diff y suma como entero con signo 16 bit
            suma = struct.unpack('<h', struct.pack('<H', diff_raw))[0]
            diff = struct.unpack('<h', struct.pack('<H', diff_raw))[0]
            izq = (suma + diff) // 2
            der = (suma - diff) // 2
            #reconstruir los canales
            reconstruidos.append(int(izq)) 
            reconstruidos.append(int(der)) 

    datos_estereo = struct.pack('<' + 'h' * len(reconstruidos), *reconstruidos)

    with open(ficEste, 'wb') as fpEste:
         fpEste.write(empaquetar_cabecera(2, info['sample_rate'], 16, len(datos_estereo)))
         fpEste.write(datos_estereo)
```

#### Subida del resultado al repositorio GitHub y *pull-request*

La entrega se formalizará mediante *pull request* al repositorio de la tarea.

El fichero `README.md` deberá respetar las reglas de los ficheros Markdown y visualizarse correctamente en
el repositorio, incluyendo el realce sintáctico del código fuente insertado.
