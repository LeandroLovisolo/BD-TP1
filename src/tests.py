#!/usr/bin/env python2

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
        with self.connector as c:
            c.execute('SELECT id, nombre FROM facultad')
            row = c.fetchone()
            self.assertIsNotNone(row)
            self.assertEquals(row[0], 1)
            self.assertEquals(row[1], api.NOMBRE_FACULTAD)

    def test_empadronar_alumno(self):
        dni = 123
        nombre = 'Alumno'

        self.model.empadronar_alumno(dni, nombre)
        with self.connector as c:
            # Verificar que se haya creado la entrada en la tabla empadronado
            c.execute('SELECT nombre, tipo FROM empadronado WHERE dni = ?', (dni,))
            row = c.fetchone()
            self.assertIsNotNone(row)
            self.assertEquals(row[0], nombre)
            self.assertEquals(row[1], api.TIPO_ESTUDIANTE)

            # Verificar que se haya creado la entrada en la tabla estudiante
            c.execute('SELECT * FROM estudiante WHERE dni = ?', (dni,))
            row = c.fetchone()
            self.assertIsNotNone(row)

    def test_empadronar_graduado(self):
        dni = 123
        nombre = 'Graduado'

        self.model.empadronar_graduado(dni, nombre)
        with self.connector as c:
            # Verificar que se haya creado la entrada en la tabla empadronado
            c.execute('SELECT nombre, tipo FROM empadronado WHERE dni = ?', (dni,))
            row = c.fetchone()
            self.assertIsNotNone(row)
            self.assertEquals(row[0], nombre)
            self.assertEquals(row[1], api.TIPO_GRADUADO)

            # Verificar que se haya creado la entrada en la tabla graduado
            c.execute('SELECT tipo FROM graduado WHERE dni = ?', (dni,))
            row = c.fetchone()
            self.assertIsNotNone(row)
            self.assertEquals(row[0], api.TIPO_GRADUADO_UBA)

            # Verificar que se haya creado la entrada en la tabla graduado_uba
            c.execute('SELECT * FROM graduado_uba WHERE dni = ?', (dni,))
            row = c.fetchone()
            self.assertIsNotNone(row)

    def test_empadronar_profesor(self):
        dni = 123
        nombre = 'Profesor'

        self.model.empadronar_profesor(dni, nombre)
        with self.connector as c:
            # Verificar que se haya creado la entrada en la tabla empadronado
            c.execute('SELECT nombre, tipo FROM empadronado WHERE dni = ?', (dni,))
            row = c.fetchone()
            self.assertIsNotNone(row)
            self.assertEquals(row[0], nombre)
            self.assertEquals(row[1], api.TIPO_PROFESOR)

            # Verificar que se haya creado la entrada en la tabla profesor
            c.execute('SELECT nacionalidad_universidad, tipo FROM profesor WHERE dni = ?', (dni,))
            row = c.fetchone()
            self.assertIsNotNone(row)
            self.assertEquals(row[0], api.NACIONALIDAD_UNIVERSIDAD_PROFESOR)
            self.assertEquals(row[1], api.TIPO_PROFESOR_REGULAR)

            # Verificar que se haya creado la entrada en la tabla profesor_regular
            c.execute('SELECT * FROM profesor_regular WHERE dni = ?', (dni,))
            row = c.fetchone()
            self.assertIsNotNone(row)

if __name__ == '__main__':
    unittest.main()
