from tp_api import model_test as mt
import unittest

class TestModel(unittest.TestCase):
	def setUp(self):
		mt.empadronar_alumno("")


if __name__ == '__main__':
	unittest.main()