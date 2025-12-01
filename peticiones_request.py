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
    try:
        print(f"Verificando conexión con {url_base}...")
        respuesta = requests.get(url_base, timeout=timeout)
        
        if respuesta.status_code == 200:
            print("Conexión exitosa con la aplicación Flask")
            return True
        else:
            print(f"Error de conexión: Código {respuesta.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("No se pudo conectar con la aplicación Flask")
        print("  Asegúrate de que la aplicación esté ejecutándose")
        return False
    except Exception as e:
        print(f"Error inesperado: {e}")
        return False

def hacer_peticion_entrenamiento(url_base: str, datos: dict, numero_peticion: int) -> bool:
    try:
        url_entrenamiento = urljoin(url_base, '/train')
        
        print(f"\n[{numero_peticion}] Enviando petición de entrenamiento...")
        print(f"   Dataset: {datos['dataset']}")
        print(f"   Modelo: {datos['model']}")
        
        respuesta = requests.post(url_entrenamiento, data=datos, timeout=60)  # Aumentado timeout
        
        if respuesta.status_code == 200:
            print(f"   Petición {numero_peticion} exitosa")
            return True
        else:
            print(f"   Error en petición {numero_peticion}: Código {respuesta.status_code}")
            return False
            
    except Exception as e:
        print(f"   Error inesperado en petición {numero_peticion}: {e}")
        return False

def ejecutar_pruebas_completas(url_base: str):
    print("INICIANDO PRUEBAS AUTOMÁTICAS DE ENTRENAMIENTO")
    print("=" * 60)
    
    # Simplificar pruebas para evitar saturación
    datasets = ['iris', 'wine', 'breast_cancer']
    modelos = ['RandomForest']
    
    contador_exitos = 0
    contador_total = 0
    
    for i, dataset in enumerate(datasets, 1):
        for modelo in modelos:
            datos = {
                'dataset': dataset,
                'model': modelo,
                'train_size': 0.7,
                'test_size': 0.3
            }
            
            exito = hacer_peticion_entrenamiento(url_base, datos, i)
            
            if exito:
                contador_exitos += 1
            contador_total += 1
            
            time.sleep(3)  # Mayor pausa entre peticiones
    
    print("\n" + "=" * 60)
    print("RESUMEN DE PRUEBAS")
    print("=" * 60)
    print(f"Peticiones exitosas: {contador_exitos}/{contador_total}")
    print(f"Tasa de éxito: {(contador_exitos/contador_total)*100:.1f}%")

def main():
    IP_ALPINE = "localhost"  # Cambiar a localhost para pruebas locales
    PUERTO = "5000"
    URL_BASE = f"http://{IP_ALPINE}:{PUERTO}"
    
    print("CLIENTE DE PRUEBAS AUTOMÁTICAS PARA PROYECTO FLASK")
    print("=" * 60)
    print(f"URL objetivo: {URL_BASE}")
    print("-" * 60)
    
    if not verificar_conexion(URL_BASE):
        print("\nNo se pudo establecer conexión.")
        return
    
    ejecutar_pruebas_completas(URL_BASE)
    
    print("\n" + "=" * 60)
    print("PRUEBAS COMPLETADAS")
    print("=" * 60)

if __name__ == "__main__":
    main()