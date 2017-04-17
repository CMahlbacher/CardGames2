#Team Crab

from Linked_List import Linked_List

class Deque:

    def __init__(self):
        self._list = Linked_List()

    def __str__(self):
        return str(self._list)

    def __len__(self):
        return len(self._list)

    def push_front(self, val):
        
        if len(self._list) == 0:
            self._list.append_element(val)
        
        else:
            self._list.insert_element_at(val, 0)
        pass

    def pop_front(self):
        if len(self) <= 0:
            return None
        return self._list.remove_element_at(0)
        pass

    def peek_front(self):
        if len(self) <= 0:
            return None
        return self._list.get_element_at(0)
        pass

    def push_back(self, val):
        self._list.append_element(val)
        pass

    def pop_back(self):
        if len(self) <= 0:
            return None
        return self._list.remove_element_at(len(self._list) - 1)
        pass

    def peek_back(self):
        if len(self) <= 0:
            return None
        return self._list.get_element_at(len(self._list) - 1)
        pass
    
    def isEmpty(self):
        return len(self) == 0

if __name__ == '__main__':
    pass #Unit tests make this unnecessary