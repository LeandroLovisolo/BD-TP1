# coding: utf-8

import sqlite3

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

# Valores de la columna 'tipo' de la tabla 'consejero_directivo'
TIPO_CONSEJERO_DIRECTIVO_CLAUSTRO_ESTUDIANTES = TIPO_ESTUDIANTE
TIPO_CONSEJERO_DIRECTIVO_CLAUSTRO_GRADUADOS   = TIPO_GRADUADO
TIPO_CONSEJERO_DIRECTIVO_CLAUSTRO_PROFESORES  = TIPO_PROFESOR

# Valores de la columna 'tipo' de la tabla 'consejero_superior'
TIPO_CONSEJERO_SUPERIOR_CLAUSTRO_ESTUDIANTES = TIPO_ESTUDIANTE
TIPO_CONSEJERO_SUPERIOR_CLAUSTRO_GRADUADOS   = TIPO_GRADUADO
TIPO_CONSEJERO_SUPERIOR_CLAUSTRO_PROFESORES  = TIPO_PROFESOR

# Valor por defecto para la columna 'nombre' de la tabla 'facultad'
NOMBRE_FACULTAD = 'Facultad de Ciencias Exactas y Naturales'

# Valor por defecto para la columna 'nacionalidad_universidad' de la tabla 'profesor'
NACIONALIDAD_UNIVERSIDAD_PROFESOR = 'Argentina'

# Clase para generar conexiones con la BD y ejecutar queries
# se da un ejemplo incompleto con el motor SQLite, pueden  adaptarlo
# a cualquiera de los motores permitidos
class bd_connector():

    # Funcion que crea la conexion con su BD
    def connect(self, port='', username='', password='', bd='bd', host='localhost'):
        self.conn = sqlite3.connect(bd)
    
    # Funcion que ejecuta queries sin esperar resultado y las comitea
    def query_without_result(self, query, parameters=()):
        with self as c:
            c.execute(query, parameters)

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
        if connector is not None:
            self.connector = connector
        else:
            self.connector = bd_connector()
            self.connector.connect('../db/facultad')

    def execute_query(self, query, parameters=()):
        self.connector.query_without_result(query, parameters)

    ################################################################################
    # Padrón electoral                                                             #
    ################################################################################

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
    
    ################################################################################
    # Consejo directivo                                                            #
    ################################################################################

    # Crea una agrupación y devuelve el ID que le fue asignado
    def crear_agrupacion_politica(self, nombre):
        with self.connector as c:
            c.execute('INSERT INTO agrupacion_politica (nombre) VALUES (?)', (nombre,))
            return c.lastrowid

    def registrar_votos_eleccion_consejo_directivo(self, id_agrupacion_politica, periodo, votos_recibidos):
        self.execute_query('INSERT OR IGNORE INTO calendario_electoral (periodo) VALUES (?)', (periodo,))
        self.execute_query('''INSERT INTO agrupacion_politica_se_presenta_durante_calendario_electoral
                              (id_agrupacion_politica, periodo, votos_recibidos)
                              VALUES (?, ?, ?)''', (id_agrupacion_politica, periodo, votos_recibidos))

    def crear_consejero_directivo(self, dni, periodo, id_agrupacion_politica):
        claustro = self.obtener_claustro(dni)
        tabla_claustro = self.obtener_tabla_consejero_directivo_dado_un_claustro(claustro)
        self.execute_query('''INSERT INTO consejero_directivo (dni, periodo, id_agrupacion_politica, tipo)
                              VALUES (?, ?, ?, ?)''', (dni, periodo, id_agrupacion_politica, claustro))
        self.execute_query('INSERT INTO %s (dni, periodo) VALUES (?, ?)' % tabla_claustro, (dni, periodo))

    ################################################################################
    # Decano                                                                       #
    ################################################################################

    def crear_decano(self, dni, periodo):
        self.execute_query('INSERT INTO decano (dni, periodo) VALUES (?, ?)', (dni, periodo))

    def registrar_voto_a_decano(self, dni_decano, periodo_decano, dni_consejero_directivo, periodo_consejero_directivo):
        self.execute_query('''INSERT INTO voto_a_decano
                              (dni_decano, periodo_decano, dni_consejero_directivo, periodo_consejero_directivo)
                              VALUES (?, ?, ?, ?)''',
                           (dni_decano, periodo_decano, dni_consejero_directivo, periodo_consejero_directivo))

    ################################################################################
    # Consejo superior                                                             #
    ################################################################################

    def crear_consejero_superior(self, dni, periodo):
        claustro = self.obtener_claustro(dni)
        tabla_claustro = self.obtener_tabla_consejero_superior_dado_un_claustro(claustro)
        self.execute_query('''INSERT INTO consejero_superior (dni, periodo, tipo)
                              VALUES (?, ?, ?)''', (dni, periodo, claustro))
        self.execute_query('INSERT INTO %s (dni, periodo) VALUES (?, ?)' % tabla_claustro, (dni, periodo))

    def registrar_voto_a_consejero_superior(self, dni_consejero_superior, periodo_consejero_superior, dni_consejero_directivo, periodo_consejero_directivo):
        self.execute_query('''INSERT INTO voto_a_consejero_superior
                              (dni_consejero_superior, periodo_consejero_superior, dni_consejero_directivo, periodo_consejero_directivo)
                              VALUES (?, ?, ?, ?)''',
                           (dni_consejero_superior, periodo_consejero_superior, dni_consejero_directivo, periodo_consejero_directivo))

    ################################################################################
    # Rector                                                                       #
    ################################################################################

    def crear_rector(self, dni, periodo):
        self.execute_query('INSERT INTO rector (dni, periodo) VALUES (?, ?)', (dni, periodo))        

    def registrar_voto_de_consejero_directivo_a_rector(self, dni_rector, periodo_rector, dni_consejero_directivo, periodo_consejero_directivo):
        self.execute_query('''INSERT INTO rector_fue_votado_por_consejero_directivo
                              (dni_rector, periodo_rector, dni_consejero_directivo, periodo_consejero_directivo)
                              VALUES (?, ?, ?, ?)''',
                           (dni_rector, periodo_rector, dni_consejero_directivo, periodo_consejero_directivo))

    def registrar_voto_de_consejero_superior_a_rector(self, dni_rector, periodo_rector, dni_consejero_superior, periodo_consejero_superior):
        self.execute_query('''INSERT INTO rector_fue_votado_por_consejero_superior
                              (dni_rector, periodo_rector, dni_consejero_superior, periodo_consejero_superior)
                              VALUES (?, ?, ?, ?)''',
                           (dni_rector, periodo_rector, dni_consejero_superior, periodo_consejero_superior))

    def registrar_voto_de_decano_a_rector(self, dni_rector, periodo_rector, dni_decano, periodo_decano):
        self.execute_query('''INSERT INTO rector_fue_votado_por_decano
                              (dni_rector, periodo_rector, dni_decano, periodo_decano)
                              VALUES (?, ?, ?, ?)''',
                           (dni_rector, periodo_rector, dni_decano, periodo_decano))

    ###############################################################################
    # Funciones requeridas por la cátedra aún no implementadas                    #
    ###############################################################################

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

    def obtener_claustro(self, dni):
        with self.connector as c:
            c.execute('SELECT tipo FROM empadronado WHERE dni = ?', (dni,))
            row = c.fetchone()
            assert row is not None, 'El DNI %d no está empadronado.' % dni
            return row[0]

    def obtener_tabla_consejero_directivo_dado_un_claustro(self, claustro):
        if claustro == TIPO_CONSEJERO_DIRECTIVO_CLAUSTRO_ESTUDIANTES:
            return 'consejero_directivo_claustro_estudiantes'
        if claustro == TIPO_CONSEJERO_DIRECTIVO_CLAUSTRO_GRADUADOS:
            return 'consejero_directivo_claustro_graduados'
        if claustro == TIPO_CONSEJERO_DIRECTIVO_CLAUSTRO_PROFESORES:
            return 'consejero_directivo_claustro_profesores'
        raise Error('Claustro inválido')

    def obtener_tabla_consejero_superior_dado_un_claustro(self, claustro):
        if claustro == TIPO_CONSEJERO_SUPERIOR_CLAUSTRO_ESTUDIANTES:
            return 'consejero_superior_claustro_estudiantes'
        if claustro == TIPO_CONSEJERO_SUPERIOR_CLAUSTRO_GRADUADOS:
            return 'consejero_superior_claustro_graduados'
        if claustro == TIPO_CONSEJERO_SUPERIOR_CLAUSTRO_PROFESORES:
            return 'consejero_superior_claustro_profesores'
        raise Error('Claustro inválido')
