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

NACIMIENTO_DEFAULT = '01/01/2000'
TODAY = time.strftime("%d/%m/%Y")

ID_FACULTAD_DEFAULT = 1

# Valores de la columna 'tipo' de la tabla 'empadronado'
TIPO_ESTUDIANTE = 0
TIPO_GRADUADO   = 1
TIPO_PROFESOR   = 2

class bd_connector():
    # Funcion que crea la conexion con su BD
    def connect(self, port='', username='', password='', bd='bd', host='localhost'):
        self.conn = sqlite3.connect(bd)
    
    # Funcion que ejecuta queries sin esperar resultado y las comitea
    def query_without_result(self, aQuery):
        c = self.conn.cursor()
        c.execute(aQuery)
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

    def execute_query(self, query):
        print query
        self.connector.query_without_result(query)

    def crear_empadronado(self, dni, nombre, tipo):
        query_empadronado = "INSERT INTO empadronado (dni, nombre, fecha_de_nacimiento, id_facultad, tipo) VALUES (\"%s\", \"%s\", \"%s\", %s, %s)"%(dni, nombre, NACIMIENTO_DEFAULT, ID_FACULTAD_DEFAULT, str(tipo))
        self.execute_query(query_empadronado)

    #Tipos de empadronado: 0 = estudiante, 1 = graduado, 2 = profesor
    # Funciones para empadronar personas
    def empadronar_alumno(self, dni, nombre): 
        tipo = 0
        self.crear_empadronado(dni, nombre, tipo)
        query_alumno = "INSERT INTO estudiante (dni, fecha_inscripcion) VALUES (\"%s\", \"%s\")" % (dni, TODAY)
        self.execute_query(query_alumno)

    #tipo de graduado 0 = UBA, 1 = otras
    def empadronar_graduado(self, dni, nombre):
        tipo = 1
        self.crear_empadronado(dni, nombre, tipo)
        query_graduado = "INSERT INTO graduado (dni, tipo) VALUES (\"%s\", %s)" % (dni, TIPO_GRADUADO)
        self.execute_query(query_graduado)

        query_graduado_UBA = "INSERT INTO graduado_uba (dni) VALUES (\"%s\")" % (dni)
        self.execute_query(query_graduado_UBA)

    #tipo de profesor 0 = regular, 1 = adjunto
    def empadronar_profesor(self, dni,nombre):  
        tipo = 2
        self.crear_empadronado(dni, nombre, tipo)
        query_graduado = "INSERT INTO profesor (dni, tipo) VALUES (\"%s\", %s)" % (dni, TIPO_GRADUADO)
        self.execute_query(query_graduado)

        query_graduado_regular = "INSERT INTO profesor_regular (dni) VALUES (\"%s\")" % (dni)
        self.execute_query(query_graduado_regular)
    
    # Funcion que afilia a una persona (dni_afiliante) a una agrupacion (id_agrupacion)
    def afiliar_a_agrupacion(self, dni_afiliante, id_agrupacion): pass

    # Funciones para setear la cantidad de votos que obtuvo cada candidato a consejero en la votacion con fecha=fecha
    def set_cant_votos_cantidato_a_consejero(self, dni_candidato, cantidad_de_votos, fecha): pass
    
    # Funcion que determina como esta compuesto el consejo directivo en la fecha=fecha
    def composicion_consejo(self,fecha): pass
    
    # Funcion que emite un voto de un consejero (dni_votador) para un candidato (dni_candidato) de decano en la fecha=fecha
    def set_voto_para_decano(self,dni_consejero_votador, dni_candidato,cantidad_de_votos,fecha): pass
