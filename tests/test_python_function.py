import unittest
from lambdas.handler import hello
from tests import *
from lambdas.meter_reader import validate_location

class TestStringMethods(unittest.TestCase):

    def test_hello(self):
        resp = hello(api_gateway_event({}), None)
        self.assertEqual(resp, {'statusCode': 200, 'body': '{"message": "Go Serverless v1.0! Your function executed successfully!"}'})

    def test_validate_location(self):
        self.assertEqual(validate_location.validate_location('6.682696, 80.325955', '6.682721, 80.325954'), True )
        self.assertEqual(validate_location.validate_location('6.682696, 80.325955', '6.649145, 80.350719'), False )


if __name__ == '__main__':
    unittest.main()