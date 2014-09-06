# -*- coding: utf-8 -*-
'''
Created on 2014-08-26 15:11
@summary: Base de Datos - 2 Cuatrimestre 2014 - TP1 API
'''

# Clase para generar conexiones con la BD y ejecutar queries
# se da un ejemplo incompleto con el motor SQLite, pueden  adaptarlo
# a cualquiera de los motores permitidos

class bd_connector():
	import sqlite3
	
	# Funcion que crea la conexion con su BD
	def connect(self, port,username,password,bd="bd",host="localhost"):
		self.conn = sqlite3.connect(bd)
	
	# Funcion que ejecuta queries sin esperar resultado y las comitea
	def query_without_result(self,aQuery):
		c = conn.cursor()
		c.exequte(aQuery)
		conn.commit()

# Clase para testear una subparte del modelo realizado. La subparte a
# testear corresponde a lo referido en una sola facultad. Es por eso
# que el set de funciones son pocas

class model_test():
	
	# Funciones para empadronar personas
	def empadronar_alumno(self, dni): pass
	def empadronar_graduado(self, dni, nombre):	pass
	def empadronar_profesor(self, dni,nombre):	pass
	
	# Funcion que afilia a una persona (dni_afiliante) a una agrupacion (id_agrupacion)
	def afiliar_a_agrupacion(self, dni_afiliante, id_agrupacion): pass

	# Funciones para setear la cantidad de votos que obtuvo cada candidato a consejero en la votacion con fecha=fecha
	def set_cant_votos_cantidato_a_consejero(self, dni_candidato, cantidad_de_votos, fecha): pass
	
	# Funcion que determina como esta compuesto el consejo directivo en la fecha=fecha
	def composicion_consejo(self,fecha): pass
	
	# Funcion que emite un voto de un consejero (dni_votador) para un candidato (dni_candidato) de decano en la fecha=fecha
	def set_voto_para_decano(self,dni_consejero_votador, dni_candidato,cantidad_de_votos,fecha): pass
	
	
	
	
