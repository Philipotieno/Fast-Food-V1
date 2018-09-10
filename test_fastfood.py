import unittest
from fastfood import *

class Test_fastfood(unittest.TestCase):

	def test_home(self):
		with app.test_client() as p:
			response = p.get('/api/v1/')
			self.assertEqual(response.status_code, 200)


	def test_register(self):
		with app.test_client() as h:
			response = h.get('/api/v1/register')
			self.assertEqual(response.status_code, 405)

	def test_login(self):
		with app.test_client() as i:
			response = i.get('/api/v1/login')
			self.assertEqual(response.status_code, 405)

	def test_make_order(self):
		with app.test_client() as h:
			response = h.get('/api/v1/make_order')


if __name__ == '__main__':
	unittest.main()