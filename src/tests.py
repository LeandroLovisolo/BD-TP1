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

    def test_empadronar_alumno(self):
        dni = 1234
        nombre = 'Alumno'

        self.model.empadronar_alumno(dni, nombre)
        with self.connector as c:
            c.execute('SELECT dni, tipo FROM empadronado WHERE dni = ?', (dni,))
            row = c.fetchone()
            self.assertIsNotNone(row)
            self.assertEquals(row[1], api.TIPO_ESTUDIANTE)


if __name__ == '__main__':
    unittest.main()
