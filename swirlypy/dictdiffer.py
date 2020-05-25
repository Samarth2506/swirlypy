# DictDiffer code borrowed from StackOverflow:
# http://stackoverflow.com/a/1165552/1550074
from swirlypy import *
class DictDiffer(object):
    """
Calculate the difference between two dictionaries as:
(1) items added
(2) items removed
(3) keys same in both but changed values
(4) keys same in both and unchanged values
"""
    def __init__(self, new, old):
        self.new, self.old = new, old
        self.set_current, self.set_past = set(new.keys()), set(old.keys())
        self.intersect = self.set_current.intersection(self.set_past)
    def added(self):
        return self.set_current - self.intersect
    def removed(self):
        return self.set_past - self.intersect
    def changed(self):
        # print(self.old)
        # print(self.new)
        changed = []
        for o in self.intersect:
            # print(o)
            # print(self.new[o])
            if isinstance(self.new[o], pd.DataFrame):
                if not self.old[o].equals(self.new[o]):
                    changed.append(o)
            elif isinstance(self.new[o], (np.ndarray, np.generic)):
                if not np.array_equal(self.old[o],self.new[o]):
                    changed.append(o)
                # changed = [o for o in self.intersect if not np.array_equal(self.old[o],self.new[o])]
            else:
                if self.old[o] != self.new[o]:
                    changed.append(o)
                # changed = [o for o in self.intersect if self.old[o] != self.new[o]]
        return set(changed)
        # return set(o for o in self.intersect if self.old[o] != self.new[o])

    def unchanged(self):
        unchanged = []
        for o in self.intersect:
            # print(o)
            # print(self.new[o])
            if isinstance(self.new[o], pd.DataFrame):
                if self.old[o].equals(self.new[o]):
                    unchanged.append(o)
            elif isinstance(self.new[o], (np.ndarray, np.generic)):
                if np.array_equal(self.old[o],self.new[o]):
                    unchanged.append(o)
                # changed = [o for o in self.intersect if not np.array_equal(self.old[o],self.new[o])]
            else:
                if self.old[o] != self.new[o]:
                    unchanged.append(o)
                # changed = [o 
        return set(unchanged)
        # return set(o for o in self.intersect if self.old[o] == self.new[o])
