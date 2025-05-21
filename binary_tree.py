class BinarySearchTree():
    class _Node:
        """Lightweight, nonpublic class for storing a node."""
        __slots__ = '_element', '_parent', '_left', '_right' # streamline memory usage

        def __init__(self, element, parent=None, left=None, right=None):
            self._element = element
            self._parent = parent
            self._left = left
            self._right = right

    def __init__(self):
        """Create an initially empty binary search tree."""
        self._root = None
        self._size = 0

    def search(self, element):
        node = self._root
        while node is not None:
            if element == node._element:
                return node
            elif element < node._element:
                node = node._left
            else:
                node = node._right
        return None

    def insert(self, element):
        if self._root is None:
            self._root = self._Node(element)
            self._size = 1
            return

        node = self._root
        while True:
            if element < node._element:
                if node._left is None:
                    node._left = self._Node(element, parent=node)
                    break
                node = node._left
            elif element > node._element:
                if node._right is None:
                    node._right = self._Node(element, parent=node)
                    break
                node = node._right
            else:
                break
        self._size += 1

    def delete(self, element):
        node = self.search(element)
        if node is None:
            return

        if node._left is not None and node._right is not None:
            successor = self._find_successor(node)
            node._element = successor._element
            node = successor

        child = node._left if node._left else node._right
        if child is not None:
            child._parent = node._parent
        if node._parent is None:
            self._root = child
        elif node == node._parent._left:
            node._parent._left = child
        else:
            node._parent._right = child

        self._size -= 1

    def _find_successor(self, current_node):
        return self._go_left(current_node._right)

    def _go_left(self, node):
        while node._left is not None:
            node = node._left
        return node

    def display(self):
        self._display(self._root, 0)

    def _display(self, node, depth):
        if node == None:
            return

        if node._right != None:
            self._display(node._right, depth+1)
        label = ''
        if node == self._root:
            label += '  <- root'
        print(f'{"    "*depth}* {node._element}{label}')
        if node._left != None:
            self._display(node._left, depth+1)