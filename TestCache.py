import unittest
import Cache
import Student


class TestCache(unittest.TestCase):

    def test_new_cache_is_empty(self):
        sa_cache = Cache.Cache(2, 8)
        self.assertIsNone(sa_cache.get("a_key"))

    def test_put(self):
        sa_cache = Cache.Cache(2, 8)
        data = (3, 5)
        sa_cache.put(data[0], data[1])
        tag = sa_cache._custom_hash(tuple([sa_cache._custom_hash(data[0]), sa_cache._custom_hash(data[1])]))
        self.assertIn([tag, data[1]], [[entry[0], entry[1]] for entry in sa_cache._cache[sa_cache._get_set_num(data[0])]])

        data2 = (-62, 172)
        sa_cache.put(data2[0], data2[1])
        tag2 = sa_cache._custom_hash(tuple([sa_cache._custom_hash(data2[0]), sa_cache._custom_hash(data2[1])]))
        self.assertIn([tag, data[1]], [[entry[0], entry[1]] for entry in sa_cache._cache[sa_cache._get_set_num(data[0])]])
        self.assertIn([tag2, data2[1]], [[entry[0], entry[1]] for entry in sa_cache._cache[sa_cache._get_set_num(data2[0])]])

    def test_get_invalid_key(self):
        sa_cache = Cache.Cache(2, 8)
        data = (55, -27)
        self.assertIsNone(sa_cache.get(data[0]))

    def test_get(self):
        sa_cache = Cache.Cache(2, 8)
        data = (1, 20)
        sa_cache.put(data[0], data[1])
        self.assertEqual(data[1], sa_cache.get(data[0]))

    def test_update(self):
        sa_cache = Cache.Cache(2, 8)
        data_old = (222, 793914)
        sa_cache.put(data_old[0], data_old[1])

        data_new = (data_old[0], 804697)
        sa_cache.update(data_new[0], data_new[1])
        self.assertEqual(data_new[1], sa_cache.get(data_new[0]))

    def test_remove_invalid_key(self):
        sa_cache = Cache.Cache(2, 8)
        data = (55129, 3)
        self.assertIsNone(sa_cache.remove(data[0]))

    def test_remove(self):
        sa_cache = Cache.Cache(2, 8)
        data = (3901, 7123)
        sa_cache.put(data[0], data[1])
        self.assertEqual(data[1], sa_cache.remove(data[0]))
        self.assertIsNone(sa_cache.remove(data[0]))

        for entry in sa_cache._cache:
            self.assertFalse(entry)

    def test_clear(self):
        sa_cache = Cache.Cache(2, 8)
        sa_cache.clear()
        for entry in sa_cache._cache:
            self.assertFalse(entry)

        data = [(x, x**2) for x in range(12)]
        for i in range(12):
            sa_cache.put(data[i][0], data[i][1])
        sa_cache.clear()
        for entry in sa_cache._cache:
            self.assertFalse(entry)

    def test_cache_replacement_LRU(self):
        sa_cache = Cache.Cache(2, 8, "lru")
        data = [(x, x**2) for x in range(11)]
        collision = dict()
        for i in range(8, 11):
            collision[data[i][0]] = []

        for i in range(8):
            sa_cache.put(data[i][0], data[i][1])

            for j in range(8, 11):
                if sa_cache._get_set_num(data[i][0]) == sa_cache._get_set_num(data[j][0]):
                    collision[data[j][0]].append(data[i][0])
        sa_cache.put(data[8][0], data[8][1])

        self.assertIsNone(sa_cache.get(collision[data[8][0]][0]))
        self.assertEqual(data[8][1], sa_cache.get(data[8][0]))

        # update timestamp by accessing through get, check if it is not replaced
        sa_cache.get(collision[data[9][0]][0])
        sa_cache.put(data[9][0], data[9][1])
        self.assertIsNotNone(sa_cache.get(collision[data[9][0]][0]))
        self.assertEqual(data[9][1], sa_cache.get(data[9][0]))

        # update timestamp by accessing through update, check if it is not replaced
        sa_cache.get(collision[data[10][0]][0])
        sa_cache.put(data[10][0], data[10][1])
        self.assertIsNotNone(sa_cache.get(collision[data[10][0]][0]))
        self.assertEqual(data[10][1], sa_cache.get(data[10][0]))

    def test_cache_replacement_MRU(self):
        sa_cache = Cache.Cache(2, 8, "mru")
        data = [(x, x**2) for x in range(11)]
        collision = dict()
        for i in range(8, 11):
            collision[data[i][0]] = []

        for i in range(8):
            sa_cache.put(data[i][0], data[i][1])

            for j in range(8, 11):
                if sa_cache._get_set_num(data[i][0]) == sa_cache._get_set_num(data[j][0]):
                    collision[data[j][0]].append(data[i][0])
        sa_cache.put(data[8][0], data[8][1])

        self.assertIsNone(sa_cache.get(collision[data[8][0]][-1]))
        self.assertEqual(data[8][1], sa_cache.get(data[8][0]))

        # update timestamp by accessing through get, check if it is replaced
        sa_cache.get(collision[data[9][0]][0])
        sa_cache.put(data[9][0], data[9][1])
        self.assertIsNone(sa_cache.get(collision[data[9][0]][0]))
        self.assertEqual(data[9][1], sa_cache.get(data[9][0]))

        # update timestamp by accessing through update, check if it is replaced
        sa_cache.get(collision[data[10][0]][0])
        sa_cache.put(data[10][0], data[10][1])
        self.assertIsNone(sa_cache.get(collision[data[10][0]][0]))
        self.assertEqual(data[10][1], sa_cache.get(data[10][0]))

    def test_custom_alg(self):
        sa_cache = Cache.Cache(2, 8, "fifo")
        data = [(x, x**2) for x in range(11)]
        collision = dict()
        for i in range(8, 11):
            collision[data[i][0]] = []

        for i in range(8):
            sa_cache.put(data[i][0], data[i][1])

            for j in range(8, 11):
                if sa_cache._get_set_num(data[i][0]) == sa_cache._get_set_num(data[j][0]):
                    collision[data[j][0]].append(data[i][0])
        sa_cache.put(data[8][0], data[8][1])

        self.assertIsNone(sa_cache.get(collision[data[8][0]][0]))
        self.assertEqual(data[8][1], sa_cache.get(data[8][0]))

        # update timestamp by accessing through get, check if it is replaced
        sa_cache.get(collision[data[9][0]][0])
        sa_cache.put(data[9][0], data[9][1])
        self.assertIsNone(sa_cache.get(collision[data[9][0]][0]))
        self.assertEqual(data[9][1], sa_cache.get(data[9][0]))

        # update timestamp by accessing through update, check if it is replaced
        sa_cache.get(collision[data[10][0]][0])
        sa_cache.put(data[10][0], data[10][1])
        self.assertIsNone(sa_cache.get(collision[data[10][0]][0]))
        self.assertEqual(data[10][1], sa_cache.get(data[10][0]))

    def test_different_n(self):
        # lru
        sa_cache_2way = Cache.Cache(2, 16)
        sa_cache_4way = Cache.Cache(4, 16)

        data = [(x, x**2) for x in range(100)]
        for i in range(100):
            sa_cache_2way.put(data[i][0], data[i][1])
        for i in range(100):
            sa_cache_4way.put(data[i][0], data[i][1])

        self.assertIn(2, [len(sa_cache_2way._cache[set_num]) for set_num in range(8)])
        self.assertIn(4, [len(sa_cache_4way._cache[set_num]) for set_num in range(4)])

        # mru
        sa_cache_3way = Cache.Cache(3, 15, "mru")
        sa_cache_5way = Cache.Cache(5, 15, "mru")

        data = [(x, x**2) for x in range(100)]
        for i in range(100):
            sa_cache_3way.put(data[i][0], data[i][1])
        for i in range(100):
            sa_cache_5way.put(data[i][0], data[i][1])

        self.assertIn(3, [len(sa_cache_3way._cache[set_num]) for set_num in range(5)])
        self.assertIn(5, [len(sa_cache_5way._cache[set_num]) for set_num in range(3)])

    def test_hits(self):
        # lru
        sa_cache = Cache.Cache(2, 8)
        data = [(x, x**2) for x in range(12)]

        for i in range(8):
            sa_cache.put(data[i][0], data[i][1])

        for i in range(8):
            sa_cache.get(data[i][0])
            self.assertEqual(i+1, sa_cache.get_hits())

        for i in range(8, 12):
            sa_cache.put(data[i][0], data[i][1])

        for i in range(0, 4):
            sa_cache.get(data[i][0])
            self.assertEqual(i+1, sa_cache.get_misses())

        # mru
        sa_cache = Cache.Cache(2, 8, "mru")

        for i in range(8):
            sa_cache.put(data[i][0], data[i][1])

        for i in range(8):
            sa_cache.get(data[i][0])
            self.assertEqual(i+1, sa_cache.get_hits())

        for i in range(8, 12):
            sa_cache.put(data[i][0], data[i][1])

        for i in range(4, 8):
            sa_cache.get(data[i][0])
            self.assertEqual(i-3, sa_cache.get_misses())

    def test_built_in_types(self):
        sa_cache = Cache.Cache(2, 8)

        # test put & get
        sa_cache.put("Username", "johanan_lai1997")
        self.assertEqual("johanan_lai1997", sa_cache.get("Username"))

        sa_cache.put("Save password", False)
        self.assertFalse(sa_cache.get("Save password"))

        sa_cache.put("Login attempts", 3)
        self.assertEqual(3, sa_cache.get("Login attempts"))

        sa_cache.put(200, 500)
        self.assertEqual(500, sa_cache.get(200))

        # test remove
        sa_cache.remove("Login attempts")
        self.assertIsNone(sa_cache.get("Login attempts"))

        self.assertEqual(500, sa_cache.remove(200))
        self.assertIsNone(sa_cache.get(200))

        sa_cache.remove("Username")
        sa_cache.remove("Save password")
        self.assertIsNone(sa_cache.get("Username"))
        self.assertIsNone(sa_cache.get("Save password"))

        # test clear
        for entry in sa_cache._cache:
            self.assertFalse(entry)

        sa_cache.put("Username", "johanan_lai1997")
        sa_cache.put("Save password", False)
        sa_cache.put("Login attempts", 3)
        sa_cache.put(200, 500)

        sa_cache.clear()
        for entry in sa_cache._cache:
            self.assertFalse(entry)

        # test update
        sa_cache.put("Prompt on quit", True)
        self.assertTrue(sa_cache.get("Prompt on quit"))
        sa_cache.update("Prompt on quit", False)
        self.assertFalse(sa_cache.get("Prompt on quit"))

        # test replacement
        sa_cache2 = Cache.Cache(2, 2)
        sa_cache2.put("string1", 10923)
        self.assertEqual(10923, sa_cache2.get("string1"))

        sa_cache2.put("string2", False)
        self.assertEqual(10923, sa_cache2.get("string1"))
        self.assertFalse(sa_cache2.get("string2"))

        sa_cache2.get("string1")
        sa_cache2.put(1000, "hello world")
        self.assertEqual("hello world", sa_cache2.get(1000))
        self.assertIsNone(sa_cache2.get("string2"))

    def test_nested_types(self):
        sa_cache = Cache.Cache(2, 8)

        # test put & get
        username_list = ["johanan_lai1997", "johananlai1997", "admin"]
        sa_cache.put("Usernames", username_list)
        self.assertEqual(username_list, sa_cache.get("Usernames"))

        sa_cache.put("Save password", False)
        self.assertFalse(sa_cache.get("Save password"))

        login_attempts = {"johanan_lai1997": 3, "johananlai1997": 0, "admin": 13291836}
        sa_cache.put("Login attempts", login_attempts)
        self.assertEqual(login_attempts, sa_cache.get("Login attempts"))

        key_set = {200, 100, 300}
        sa_cache.put(key_set, 500)
        self.assertEqual(500, sa_cache.get(key_set))

        # test remove
        sa_cache.remove("Login attempts")
        self.assertIsNone(sa_cache.get("Login attempts"))

        self.assertEqual(500, sa_cache.remove(key_set))
        self.assertIsNone(sa_cache.get(key_set))

        sa_cache.remove("Usernames")
        sa_cache.remove("Save password")
        self.assertIsNone(sa_cache.get("Usernames"))
        self.assertIsNone(sa_cache.get("Save password"))

        # test clear
        for entry in sa_cache._cache:
            self.assertFalse(entry)

        sa_cache.put("Usernames", username_list)
        sa_cache.put("Save password", False)
        sa_cache.put("Login attempts", login_attempts)
        sa_cache.put(key_set, 500)

        sa_cache.clear()
        for entry in sa_cache._cache:
            self.assertFalse(entry)

        # test update
        sa_cache.put(username_list, key_set)
        self.assertEqual(key_set, sa_cache.get(username_list))
        sa_cache.update(username_list, login_attempts)
        self.assertEqual(login_attempts, sa_cache.get(username_list))

        # test replacement
        sa_cache2 = Cache.Cache(2, 2)
        data1_key = {True, 100, False, "string1"}
        sa_cache2.put(data1_key, 10923)
        self.assertEqual(10923, sa_cache2.get(data1_key))

        data2_key = {"Root": True, "Filepos": 100, "Open": False, -44: "string1"}
        sa_cache2.put(data2_key, username_list)
        self.assertEqual(10923, sa_cache2.get(data1_key))
        self.assertEqual(username_list, sa_cache2.get(data2_key))

        sa_cache2.get(data1_key)
        sa_cache2.put(1000, "hello world")
        self.assertEqual("hello world", sa_cache2.get(1000))
        self.assertIsNone(sa_cache2.get(data2_key))

    def test_class_types(self):
        sa_cache = Cache.Cache(2, 8)

        # test put & get
        student1 = Student.Student("Johanan Lai", 48406488, ("UCI", "Computer Science"))
        sa_cache.put(student1, 123)
        self.assertEqual(123, sa_cache.get(student1))

        sa_cache.put("johananl", student1)
        self.assertEqual(student1, sa_cache.get("johananl"))

        login_attempts = {"johanan_lai1997": 3, "johananlai1997": 0, "admin": 13291836}
        sa_cache.put("Login attempts", student1)
        self.assertEqual(student1, sa_cache.get("Login attempts"))

        key_set = {200, 100, 300}
        sa_cache.put(key_set, 500)
        self.assertEqual(500, sa_cache.get(key_set))

        # test remove
        sa_cache.remove("Login attempts")
        self.assertIsNone(sa_cache.get("Login attempts"))

        self.assertEqual(500, sa_cache.remove(key_set))
        self.assertIsNone(sa_cache.get(key_set))

        sa_cache.remove(student1)
        sa_cache.remove("johananl")
        self.assertIsNone(sa_cache.get(student1))
        self.assertIsNone(sa_cache.get("johananl"))

        # test clear
        for entry in sa_cache._cache:
            self.assertFalse(entry)

        sa_cache.put(student1, 123)
        sa_cache.put("johananl", student1)
        sa_cache.put("Login attempts", login_attempts)
        sa_cache.put(key_set, 500)

        sa_cache.clear()
        for entry in sa_cache._cache:
            self.assertFalse(entry)

        # test update
        sa_cache.put("johananl", key_set)
        self.assertEqual(key_set, sa_cache.get("johananl"))
        sa_cache.update("johananl", student1)
        self.assertEqual(student1, sa_cache.get("johananl"))

        # test replacement
        sa_cache2 = Cache.Cache(2, 2)
        data1_key = {True, 100, False, "string1"}
        sa_cache2.put(data1_key, student1)
        self.assertEqual(student1, sa_cache2.get(data1_key))

        data2_value = {"Root": True, "Filepos": 100, "Open": False, -44: "string1"}
        sa_cache2.put(student1, data2_value)
        self.assertEqual(student1, sa_cache2.get(data1_key))
        self.assertEqual(data2_value, sa_cache2.get(student1))

        sa_cache2.get(data1_key)
        sa_cache2.put(1000, "hello world")
        self.assertEqual("hello world", sa_cache2.get(1000))
        self.assertIsNone(sa_cache2.get(student1))

if __name__ == "__main__":
    unittest.main()
