import datetime


class ReplacementAlgorithm:

    def __init__(self, alg, sets):
        """
        :param alg: String that determines algorithm type.
        timestamps: List of dict containing tags and their timestamps (datetime of last access)
        fifo_queue: Queue of tags; keeps track of entries were put into cache
        """
        self._alg = alg
        self._timestamps = [dict() for _ in range(sets)]
        self._fifo_queue = []
        # add more algorithm-related structures here

    def get_index_to_evict(self, cache_set, set_num, slots):
        """
        :param cache_set: Current working set inside cache to look through
        :param set_num: Index of cache set
        :param slots: Number of slots in cache_set
        :return: Index of entry to evict based on replacement algorithm
        """
        if self._alg == "lru":
            lru_tag = sorted(self._timestamps[set_num].items(), key=lambda kv: kv[1])[0][0]
            for i in range(slots):
                if cache_set[i][0] == lru_tag:
                    return i
        elif self._alg == "mru":
            mru_tag = sorted(self._timestamps[set_num].items(), key=lambda kv: kv[1], reverse=True)[0][0]
            for i in range(slots):
                if cache_set[i][0] == mru_tag:
                    return i
        elif self._alg == "fifo":
            for i in range(slots):
                if cache_set[i][0] == self._fifo_queue[0]:
                    self._fifo_queue.pop(0)
                    return i
        else:
            # add more algorithm cases before else
            return 0

    def update_alg_struct(self, set_num, tag):
        """
        Update all structures related to the algorithm after a put, e.g. a dict for priorities
        :param set_num: Index of cache set
        :param tag: Tag of key/value pair to add to alg struct
        """
        if self._alg in ["lru", "mru"]:
            self._timestamps[set_num][tag] = datetime.datetime.now()
        elif self._alg == "fifo":
            self._fifo_queue.append(tag)

    def update_alg_struct_on_evict(self, set_num, old_tag, new_tag):
        """
        Update all structures related to the algorithm after an update, e.g. a dict for priorities
        Remove all stored values pertaining to the old tag.
        :param set_num: Index of cache set
        :param old_tag: Tag of old key/value pair to remove from alg struct
        :param new_tag: Tag of new key/value pair to add to alg struct
        """
        if self._alg in ["lru", "mru"]:
            # remove old tag/timestamp value
            self._timestamps[set_num].pop(old_tag)

            # add new tag/timestamp value
            self._timestamps[set_num][new_tag] = datetime.datetime.now()
        elif self._alg == "fifo":
            self._fifo_queue.append(new_tag)

    def update_alg_struct_on_remove(self, set_num, tag):
        if self._alg in ["lru", "mru"]:
            self._timestamps[set_num].pop(tag)
        elif self._alg == "fifo":
            pass

    def clear_alg_struct(self):
        if self._alg in ["lru", "mru"]:
            for d in self._timestamps:
                d.clear()
        elif self._alg == "fifo":
            self._fifo_queue.clear()
