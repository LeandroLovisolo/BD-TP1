#!/usr/bin/env python2
# coding: utf-8

import unittest
import tp_api as api

class TestModel(unittest.TestCase):

    def setUp(self):
        # Crear una base en memoria y crear las tablas
        self.connector = api.bd_connector()
        self.connector.connect(bd=':memory:')
        f = open('../db/facultad.sql', 'r')
        self.connector.conn.executescript(f.read())

        # El modelo ahora usa la base en memoria en lugar del archivo facultad.db
        self.model = api.model_test(self.connector)

    def test_crear_facultad_por_defecto(self):
        self.model.empadronar_alumno(123, 'Alumno')
        self.assertSelectEquals('SELECT id, nombre FROM facultad', (),
                                [1, api.NOMBRE_FACULTAD])

    def test_empadronar_alumno(self):
        dni = 123
        nombre = 'Alumno'
        self.model.empadronar_alumno(dni, nombre)

        # Verificar que se haya creado la entrada en la tabla empadronado
        self.assertSelectEquals('SELECT nombre, tipo FROM empadronado WHERE dni = ?', (dni,),
                                [nombre, api.TIPO_ESTUDIANTE])

        # Verificar que se haya creado la entrada en la tabla estudiante
        self.assertSelectIsNotEmpty('SELECT * FROM estudiante WHERE dni = ?', (dni,))

    def test_empadronar_graduado(self):
        dni = 123
        nombre = 'Graduado'
        self.model.empadronar_graduado(dni, nombre)

        # Verificar que se haya creado la entrada en la tabla empadronado
        self.assertSelectEquals('SELECT nombre, tipo FROM empadronado WHERE dni = ?', (dni,),
                                [nombre, api.TIPO_GRADUADO])

        # Verificar que se haya creado la entrada en la tabla graduado
        self.assertSelectEquals('SELECT tipo FROM graduado WHERE dni = ?', (dni,),
                                [api.TIPO_GRADUADO_UBA])

        # Verificar que se haya creado la entrada en la tabla graduado_uba
        self.assertSelectIsNotEmpty('SELECT * FROM graduado_uba WHERE dni = ?', (dni,))

    def test_empadronar_profesor(self):
        dni = 123
        nombre = 'Profesor'

        self.model.empadronar_profesor(dni, nombre)

        # Verificar que se haya creado la entrada en la tabla empadronado
        self.assertSelectEquals('SELECT nombre, tipo FROM empadronado WHERE dni = ?', (dni,),
                                [nombre, api.TIPO_PROFESOR])

        # Verificar que se haya creado la entrada en la tabla profesor
        self.assertSelectEquals('SELECT nacionalidad_universidad, tipo FROM profesor WHERE dni = ?', (dni,),
                                [api.NACIONALIDAD_UNIVERSIDAD_PROFESOR, api.TIPO_PROFESOR_REGULAR])

        # Verificar que se haya creado la entrada en la tabla profesor_regular
        self.assertSelectIsNotEmpty('SELECT * FROM profesor_regular WHERE dni = ?', (dni,))

    # Ejecuta la consulta y verifica que el conjunto de filas devuelto sea no-vacío
    def assertSelectIsNotEmpty(self, query, parameters):
        with self.connector as c:
            c.execute(query, parameters)
            row = c.fetchone()
            self.assertIsNotNone(row)

    # Ejecuta la consulta y verifica que la primera fila devuelta coincida con la fila recibida por parámetro
    def assertSelectEquals(self, query, parameters, expected_row):
        with self.connector as c:
            c.execute(query, parameters)
            row = c.fetchone()
            self.assertIsNotNone(row)
            for i in range(0, len(expected_row)):
                self.assertEquals(row[i], expected_row[i])

if __name__ == '__main__':
    unittest.main()
