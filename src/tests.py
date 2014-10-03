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
            # Verificar que se haya creado la entrada en la tabla empadronado
            c.execute('SELECT dni, nombre, tipo FROM empadronado WHERE dni = ?', (dni,))
            row = c.fetchone()
            self.assertIsNotNone(row)
            self.assertEquals(row[1], nombre)
            self.assertEquals(row[2], api.TIPO_ESTUDIANTE)

            # Verificar que se haya creado la entrada en la tabla estudiante
            c.execute('SELECT dni FROM estudiante WHERE dni = ?', (dni,))
            row = c.fetchone()
            self.assertIsNotNone(row)

if __name__ == '__main__':
    unittest.main()
