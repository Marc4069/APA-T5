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
