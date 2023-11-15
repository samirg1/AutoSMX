from typing import Generic, TypeVar, Self


_T = TypeVar("_T")


class _MRUListNode(Generic[_T]):
    def __init__(self, value: _T, previous: Self | None = None, next: Self | None = None) -> None:
        self.value = value
        self.previous = previous
        self.next = next


class MRUList(Generic[_T]):
    def __init__(self) -> None:
        self.nodes: dict[_T, _MRUListNode[_T]] = {}
        self.head: _MRUListNode[_T] | None = None

    def add(self, value: _T) -> None:
        if value in self.nodes:
            self.remove(value)        

        if self.head is None:
            self.head = _MRUListNode(value)
            self.nodes[value] = self.head
            return
        
        temp = self.head
        self.head = _MRUListNode(value, None, temp)
        self.nodes[value] = self.head
        temp.previous = self.head
        
    def remove(self, value: _T) -> None:
        node = self.nodes[value]
        
        assert self.head
        if value == self.head.value:
            self.head = node.next
            if self.head is not None:
                self.head.previous = None
            del self.nodes[value]
            return
        
        assert node.previous
        node.previous.next = node.next
        if node.next:
            node.next.previous = node.previous
        del self.nodes[value]

    def __iter__(self) -> Self:
        self._current = self.head
        return self
    
    def __next__(self) -> _T:
        if self._current is None:
            raise StopIteration
        
        temp = self._current.value
        self._current = self._current.next
        return temp
    
    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, MRUList):
            return self.nodes == __value.nodes  # type: ignore
        return NotImplemented
    
    def __len__(self) -> int:
        return len(self.nodes)

    def __repr__(self) -> str:
        return f"MRUList({' -> '.join(str(value) for value in self)})"
