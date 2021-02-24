import unittest
from lambdas.handler import hello
from tests import *

class TestStringMethods(unittest.TestCase):

    def test_hello(self):
        resp = hello(api_gateway_event({}), None)
        self.assertEqual(resp, {'statusCode': 200, 'body': '{"message": "Go Serverless v1.0! Your function executed successfully!"}'})

if __name__ == '__main__':
    unittest.main()