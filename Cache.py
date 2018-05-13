import ReplacementAlgorithm


class Cache:

    def __init__(self, slots, size, alg="lru"):
        """
        :param slots: Number of slots; specifies the -way associativity of the cache
        :param size: Total number of slots in the cache
        :param alg: String that determines algorithm type. Used by ReplacementAlgorithm. Default is LRU
        """
        self._slots = slots
        self._size = size
        self._sets = int(size/slots)
        self._hits = 0
        self._misses = 0

        self._repl_alg = ReplacementAlgorithm.ReplacementAlgorithm(alg, self._sets)
        self._cache = [list() for _ in range(self._sets)]

    def put(self, key, value):
        """
        Stores data as a 2-item list [tag, value].
        Tag is calculated by hashing combination of key and value.
        Use update to update an entry with an existing key.
        :param key: Key to use for cache access
        :param value: Value to store in cache
        """
        set_num = self._get_set_num(key)
        tag = self._custom_hash((self._custom_hash(key), self._custom_hash(value)))

        if len(self._cache[set_num]) < self._slots:
            # set has space, append to set
            self._cache[set_num].append([tag, value])
            self._repl_alg.update_alg_struct(set_num, tag)
        else:
            # set is full, evict based on algorithm
            evict_i = self._repl_alg.get_index_to_evict(self._cache[set_num], set_num, self._slots)
            old_tag = self._cache[set_num][evict_i][0]
            self._cache[set_num][evict_i] = [tag, value]
            self._repl_alg.update_alg_struct_on_evict(set_num, old_tag, tag)

    def update(self, key, new_value):
        """
        Updates an existing entry in the cache.
        Tag is calculated by hashing a combination of key and old_value
        :param key: Specifies which entry to be replaced
        :param new_value: Value to store in entry, replacing old_value
        :return: Set number the value was stored in, or -1 if key was not found
        """
        set_num = self._get_set_num(key)
        old_value = self.get(key)

        if old_value is None:
            return -1

        old_tag = self._custom_hash((self._custom_hash(key), self._custom_hash(old_value)))
        new_tag = self._custom_hash((self._custom_hash(key), self._custom_hash(new_value)))

        for entry in self._cache[set_num]:
            if entry[0] == old_tag:
                entry[0] = new_tag
                entry[1] = new_value
                self._repl_alg.update_alg_struct_on_evict(set_num, old_tag, new_tag)
                return set_num

    def get(self, key):
        """
        Gets value in cache given key
        :return: Value corresponding to key, or None if no matching key
        """
        set_num = self._get_set_num(key)

        for entry in self._cache[set_num]:
            tag = self._custom_hash((self._custom_hash(key), self._custom_hash(entry[1])))

            if entry[0] == tag:
                self._hits += 1
                self._repl_alg.update_alg_struct(set_num, tag)
                return entry[1]

        self._misses += 1
        return None

    def remove(self, key):
        """
        Removes entry from cache given key
        :return: Value corresponding to key if successful, or None if no matching key
        """
        set_num = self._get_set_num(key)

        for i in range(len(self._cache[set_num])):
            tag = self._custom_hash((self._custom_hash(key), self._custom_hash(self._cache[set_num][i][1])))

            if self._cache[set_num][i][0] == tag:
                self._repl_alg.update_alg_struct_on_remove(set_num, tag)
                return self._cache[set_num].pop(i)[1]

        return None

    def clear(self):
        """
        Clears entire cache, removing all entries
        """
        for cache_set in self._cache:
            cache_set.clear()

        self._repl_alg.clear_alg_struct()
        self._hits = 0
        self._misses = 0

    def get_hits(self):
        """
        :return: Number of cache hits
        """
        return self._hits

    def get_misses(self):
        """
        :return: Number of cache misses
        """
        return self._misses

    def _custom_hash(self, key):
        """
        Recursive hash function that handles keys that are lists, sets, dicts
        """
        if type(key) is list:
            return self._custom_hash(tuple(key))
        elif type(key) is set:
            return self._custom_hash(frozenset(key))
        elif type(key) is dict:
            return self._custom_hash(frozenset(key.items()))
        else:
            return hash(key)

    def _get_set_num(self, key):
        """
        :return: Set index number given key
        """
        return self._custom_hash(key) % self._sets
