# -*- coding: utf-8 -*-
'''
Created on 2014-08-26 15:11
@summary: Base de Datos - 2 Cuatrimestre 2014 - TP1 API
'''
import time
import sqlite3

# Clase para generar conexiones con la BD y ejecutar queries
# se da un ejemplo incompleto con el motor SQLite, pueden  adaptarlo
# a cualquiera de los motores permitidos

# Valores de la columna 'tipo' de la tabla 'empadronado'
TIPO_ESTUDIANTE = 0
TIPO_GRADUADO   = 1
TIPO_PROFESOR   = 2

# Valores de la columna 'tipo' de la tabla 'graduado'
TIPO_GRADUADO_UBA              = 0
TIPO_GRADUADO_OTRA_UNIVERSIDAD = 1

# Valores de la columna 'tipo' de la tabla 'profesor'
TIPO_PROFESOR_REGULAR = 0
TIPO_PROFESOR_ADJUNTO = 1

# Valor por defecto para la columna 'nombre' de la tabla 'facultad'
NOMBRE_FACULTAD = 'Facultad de Ciencias Exactas y Naturales'

# Valor por defecto para la columna 'nacionalidad_universidad' de la tabla 'profesor'
NACIONALIDAD_UNIVERSIDAD_PROFESOR = 'Argentina'

class bd_connector():
    # Funcion que crea la conexion con su BD
    def connect(self, port='', username='', password='', bd='bd', host='localhost'):
        self.conn = sqlite3.connect(bd)
    
    # Funcion que ejecuta queries sin esperar resultado y las comitea
    def query_without_result(self, query, parameters=()):
        c = self.conn.cursor()
        c.execute(query, parameters)
        self.conn.commit()

    def __enter__(self):
        self.cur = self.conn.cursor()
        return self.cur

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None and exc_value is None and traceback is None:
            self.conn.commit()

    def __del__(self):
        self.conn.close()

# Clase para testear una subparte del modelo realizado. La subparte a
# testear corresponde a lo referido en una sola facultad. Es por eso
# que el set de funciones son pocas

class model_test():

    # Permite usar un conector distinto (ej.: a una base en memoria) desde los tests
    def __init__(self, connector=None):
        if connector is None:
            self.connector = bd_connector()
            self.connector.connect('../db/facultad')
        else:
            self.connector = connector

    def execute_query(self, query, parameters=()):
        print query
        self.connector.query_without_result(query, parameters)

    def empadronar_alumno(self, dni, nombre): 
        self.insertar_empadronado(dni, nombre, TIPO_ESTUDIANTE)
        self.execute_query('''INSERT INTO estudiante (dni, fecha_inscripcion)
                              VALUES (?, strftime('%s', 'now'))''', (dni,))

    def empadronar_graduado(self, dni, nombre):
        self.insertar_empadronado(dni, nombre, TIPO_GRADUADO)
        self.execute_query('''INSERT INTO graduado (dni, tipo)
                              VALUES (?, ?)''', (dni, TIPO_GRADUADO_UBA))
        self.execute_query('''INSERT INTO graduado_uba (dni)
                              VALUES (?)''', (dni,))

    def empadronar_profesor(self, dni,nombre):  
        self.insertar_empadronado(dni, nombre, TIPO_PROFESOR)
        self.execute_query('''INSERT INTO profesor (dni, nacionalidad_universidad, tipo)
                              VALUES (?, ?, ?)''', (dni, NACIONALIDAD_UNIVERSIDAD_PROFESOR, TIPO_PROFESOR_REGULAR))
        self.execute_query('''INSERT INTO profesor_regular (dni)
                              VALUES (?)''', (dni,))
    
    # Funcion que afilia a una persona (dni_afiliante) a una agrupacion (id_agrupacion)
    def afiliar_a_agrupacion(self, dni_afiliante, id_agrupacion): pass

    # Funciones para setear la cantidad de votos que obtuvo cada candidato a consejero en la votacion con fecha=fecha
    def set_cant_votos_cantidato_a_consejero(self, dni_candidato, cantidad_de_votos, fecha): pass
    
    # Funcion que determina como esta compuesto el consejo directivo en la fecha=fecha
    def composicion_consejo(self,fecha): pass
    
    # Funcion que emite un voto de un consejero (dni_votador) para un candidato (dni_candidato) de decano en la fecha=fecha
    def set_voto_para_decano(self,dni_consejero_votador, dni_candidato,cantidad_de_votos,fecha): pass


    ###############################################################################
    # Funciones privadas (no deben ser consumidas por fuera de la API)            #
    ###############################################################################

    def obtener_id_facultad_por_defecto(self):
        with self.connector as c:
            c.execute('SELECT id FROM facultad WHERE nombre = ?', (NOMBRE_FACULTAD,))
            row = c.fetchone()
            if row is None:
                c.execute('INSERT INTO facultad (nombre) VALUES (?)', (NOMBRE_FACULTAD,))
                id = c.lastrowid
            else:
                id = row[0]
        return id

    def insertar_empadronado(self, dni, nombre, tipo):
        id_facultad = self.obtener_id_facultad_por_defecto()
        self.execute_query('''INSERT INTO empadronado (dni, nombre, id_facultad, tipo)
                              VALUES (?, ?, ?, ?)''', (dni, nombre, id_facultad, tipo))