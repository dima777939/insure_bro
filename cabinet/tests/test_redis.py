from cabinet.redis_data import RedisData
from cabinet.tests.test_data import DataTestList


class RedisTest(DataTestList):
    """
    Тесты для Redis
    """

    def setUp(self):
        self.redis_db = RedisData()

    def test_connections(self):
        """
        Тест подключения
        """
        conn = self.redis_db._r.ping()
        self.assertTrue(conn)

    def test_incr_key(self):
        """
        Тест увеличения значения ключа
        """
        self.redis_db.incr_key("test_key", "1")
        self.redis_db.incr_key("test_key", "1")
        self.assertEqual(self.redis_db._r.get("test_key:1"), "2")

    def test_del_key(self):
        """
        Тест удаления ключа
        """
        self.redis_db.delete_product_key("test_key", "1")
        self.assertIsNone(self.redis_db._r.get("test_key:1"))

