import unittest


class IntegrationTest(unittest.TestCase):
    def test_integration(self):
        from tests.main_routine import integration

        try:
            integration()
        except Exception:
            raise self.failureException()
