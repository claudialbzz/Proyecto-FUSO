#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# =============================================================================
# ARCHIVO: peticiones_request.py
# DESCRIPCIÓN: Script para realizar peticiones automáticas al servicio Flask
#              y descargar las imágenes generadas por el entrenamiento
# USO: python peticiones_request.py
# AUTOR: Claudia Maria Lopez Bombin Y Gonzalo Velasco Lucas
# FECHA: Noviembre 2025
# =============================================================================

import requests
import os
import time
from urllib.parse import urljoin

def verificar_conexion(url_base: str, timeout: int = 10) -> bool:
    """
    Verifica que la aplicación Flask esté funcionando y accesible.
    
    Args:
        url_base (str): URL base de la aplicación Flask
        timeout (int): Tiempo máximo de espera para la conexión
        
    Returns:
        bool: True si la conexión es exitosa, False en caso contrario
    """
    try:
        print(f"Verificando conexión con {url_base}...")
        respuesta = requests.get(url_base, timeout=timeout)
        
        if respuesta.status_code == 200:
            print("✓ Conexión exitosa con la aplicación Flask")
            return True
        else:
            print(f"✗ Error de conexión: Código {respuesta.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("✗ No se pudo conectar con la aplicación Flask")
        print("  Asegúrate de que la aplicación esté ejecutándose")
        return False
    except requests.exceptions.Timeout:
        print("✗ Timeout al intentar conectar")
        return False
    except Exception as e:
        print(f"✗ Error inesperado: {e}")
        return False

def hacer_peticion_entrenamiento(url_base: str, datos: dict, numero_peticion: int) -> bool:
    """
    Realiza una petición POST al endpoint de entrenamiento y descarga la imagen resultante.
    
    Args:
        url_base (str): URL base de la aplicación
        datos (dict): Datos para la petición de entrenamiento
        numero_peticion (int): Número de petición para logging
        
    Returns:
        bool: True si la petición fue exitosa, False en caso contrario
    """
    try:
        # Construir URL completa del endpoint de entrenamiento
        url_entrenamiento = urljoin(url_base, '/train')
        
        print(f"\n[{numero_peticion}] Enviando petición de entrenamiento...")
        print(f"   Dataset: {datos['dataset']}")
        print(f"   Modelo: {datos['model']}")
        print(f"   Train size: {datos['train_size']}")
        print(f"   Test size: {datos['test_size']}")
        
        # Realizar petición POST con los datos del formulario
        respuesta = requests.post(url_entrenamiento, data=datos, timeout=30)
        
        if respuesta.status_code == 200:
            print(f"   ✓ Petición {numero_peticion} exitosa")
            
            # Descargar la imagen generada
            nombre_imagen = f"{datos['dataset']}Tr{datos['train_size']}Tst{datos['test_size']}.png"
            url_imagen = urljoin(url_base, f'/static/{nombre_imagen}')
            
            return descargar_imagen(url_imagen, nombre_imagen, numero_peticion)
        else:
            print(f"   ✗ Error en petición {numero_peticion}: Código {respuesta.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print(f"   ✗ Timeout en petición {numero_peticion}")
        return False
    except Exception as e:
        print(f"   ✗ Error inesperado en petición {numero_peticion}: {e}")
        return False

def descargar_imagen(url_imagen: str, nombre_archivo: str, numero_peticion: int) -> bool:
    """
    Descarga una imagen desde la URL especificada.
    
    Args:
        url_imagen (str): URL completa de la imagen a descargar
        nombre_archivo (str): Nombre del archivo para guardar
        numero_peticion (int): Número de petición para logging
        
    Returns:
        bool: True si la descarga fue exitosa, False en caso contrario
    """
    try:
        # Intentar descargar la imagen
        respuesta_imagen = requests.get(url_imagen, timeout=15)
        
        if respuesta_imagen.status_code == 200:
            # Asegurarse de que el directorio de descargas existe
            directorio_descargas = "descargas_train"
            os.makedirs(directorio_descargas, exist_ok=True)
            
            # Guardar la imagen
            ruta_completa = os.path.join(directorio_descargas, nombre_archivo)
            with open(ruta_completa, 'wb') as archivo:
                archivo.write(respuesta_imagen.content)
            
            # Obtener tamaño del archivo para logging
            tamaño = os.path.getsize(ruta_completa)
            print(f"   ✓ Imagen descargada: {nombre_archivo} ({tamaño:,} bytes)")
            return True
        else:
            print(f"   ✗ Error descargando imagen: Código {respuesta_imagen.status_code}")
            return False
            
    except Exception as e:
        print(f"   ✗ Error descargando imagen: {e}")
        return False

def ejecutar_pruebas_completas(url_base: str):
    """
    Ejecuta todas las pruebas automáticas de entrenamiento con diferentes parámetros.
    
    Args:
        url_base (str): URL base de la aplicación Flask
    """
    print("INICIANDO PRUEBAS AUTOMÁTICAS DE ENTRENAMIENTO")
    print("=" * 60)
    
    # Configuración de las pruebas
    datasets = ['iris', 'wine', 'breast_cancer']
    modelos = ['RandomForest', 'SVM', 'LogisticRegression']
    
    # Combinaciones de train_size y test_size (deben sumar 1.0)
    tamanios_entrenamiento = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    tamanios_prueba = [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]
    
    contador_exitos = 0
    contador_total = 0
    
    # Probar diferentes combinaciones de parámetros
    for i, (train_size, test_size) in enumerate(zip(tamanios_entrenamiento, tamanios_prueba), 1):
        for dataset in datasets[:1]:  # Probar solo con iris para no saturar
            for modelo in modelos[:1]:  # Probar solo con RandomForest para no saturar
                
                # Preparar datos para la petición
                datos = {
                    'dataset': dataset,
                    'model': modelo,
                    'train_size': train_size,
                    'test_size': test_size
                }
                
                # Realizar petición
                exito = hacer_peticion_entrenamiento(url_base, datos, i)
                
                if exito:
                    contador_exitos += 1
                contador_total += 1
                
                # Pequeña pausa entre peticiones para no sobrecargar el servidor
                time.sleep(2)
    
    # Mostrar resumen final
    print("\n" + "=" * 60)
    print("RESUMEN DE PRUEBAS")
    print("=" * 60)
    print(f"Peticiones exitosas: {contador_exitos}/{contador_total}")
    print(f"Tasa de éxito: {(contador_exitos/contador_total)*100:.1f}%")
    print(f"Imágenes descargadas en: {os.path.abspath('descargas_train')}")

def main():
    """
    Función principal del script.
    """
    # Configuración - CAMBIAR POR LA IP REAL DE TU MÁQUINA ALPINE
    IP_ALPINE = "192.168.1.100"  # ← IMPORTANTE: Cambiar por IP real
    PUERTO = "5000"
    URL_BASE = f"http://{IP_ALPINE}:{PUERTO}"
    
    print("CLIENTE DE PRUEBAS AUTOMÁTICAS PARA PROYECTO FLASK")
    print("=" * 60)
    print(f"URL objetivo: {URL_BASE}")
    print("Este script realizará peticiones automáticas al servicio /train")
    print("y descargará las imágenes generadas por el entrenamiento.")
    print("-" * 60)
    
    # Verificar conexión antes de empezar
    if not verificar_conexion(URL_BASE):
        print("\nNo se pudo establecer conexión. Verifica:")
        print("1. Que la aplicación Flask esté ejecutándose")
        print("2. Que la IP y puerto sean correctos")
        print("3. Que no haya problemas de firewall/red")
        return
    
    # Ejecutar pruebas
    ejecutar_pruebas_completas(URL_BASE)
    
    print("\n" + "=" * 60)
    print("PRUEBAS COMPLETADAS")
    print("=" * 60)

if __name__ == "__main__":
    main()