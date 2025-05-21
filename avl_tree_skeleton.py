class AVLTree():
    class _Node:
        """Lightweight, nonpublic class for storing a node."""
        __slots__ = '_element', '_parent', '_left', '_right', '_height' # streamline memory usage

        def __init__(self, element, parent=None, left=None, right=None):
            self._element = element
            self._parent = parent
            self._left = left
            self._right = right
            self._height = 0

        def left_height(self):
            return self._left._height if self._left != None else 0

        def right_height(self):
            return self._right._height if self._right != None else 0

        def set_height(self, new_height):
            self._height = new_height


    def __init__(self):
        """Create an initially empty binary tree."""
        self._root = None
        self._size = 0

    def search(self, element):
        curr = self._root
        while curr != None:
            if curr._element == element:
                return curr
            elif curr._element < element:
                curr = curr._right
            else:
                curr = curr._left
        return None

    def _update_height(self, node):
        node._height = 1 + max(node.left_height(), node.right_height())

    def _balance_factor(self, node):
        return node.left_height() - node.right_height()

    def _rotate_left(self, x):
        y = x._right
        x._right = y._left
        if y._left:
            y._left._parent = x
        y._parent = x._parent
        if not x._parent:
            self._root = y
        elif x == x._parent._left:
            x._parent._left = y
        else:
            x._parent._right = y
        y._left = x
        x._parent = y
        self._update_height(x)
        self._update_height(y)
        return y

    def _rotate_right(self, y):
        x = y._left
        y._left = x._right
        if x._right:
            x._right._parent = y
        x._parent = y._parent
        if not y._parent:
            self._root = x
        elif y == y._parent._right:
            y._parent._right = x
        else:
            y._parent._left = x
        x._right = y
        y._parent = x
        self._update_height(y)
        self._update_height(x)
        return x

    def _rebalance(self, node):
        while node:
            self._update_height(node)
            balance = self._balance_factor(node)

            if balance > 1:  # Left heavy
                if self._balance_factor(node._left) < 0:  # Left-Right case
                    node._left = self._rotate_left(node._left)
                node = self._rotate_right(node)  # Left-Left case
            elif balance < -1:  # Right heavy
                if self._balance_factor(node._right) > 0:  # Right-Left case
                    node._right = self._rotate_right(node._right)
                node = self._rotate_left(node)  # Right-Right case
            
            # Special handling for root after rotation
            if node._parent is None:
                self._root = node

            node = node._parent


    def insert(self, element):
        if not self._root:
            self._root = self._Node(element)
            self._size = 1
            return

        curr = self._root
        parent = None
        while curr:
            parent = curr
            if element < curr._element:
                curr = curr._left
            elif element > curr._element:
                curr = curr._right
            else:
                return  # Element already exists

        new_node = self._Node(element, parent)
        if element < parent._element:
            parent._left = new_node
        else:
            parent._right = new_node
        
        self._size += 1
        self._rebalance(new_node._parent)

    def _delete_node(self, node_to_delete):
        if node_to_delete is None:
            return # Should not happen if search is correct

        parent = node_to_delete._parent
        # Case 1: Node has no children (leaf node)
        if not node_to_delete._left and not node_to_delete._right:
            if parent:
                if parent._left == node_to_delete:
                    parent._left = None
                else:
                    parent._right = None
                self._rebalance(parent)
            else: # Deleting the root
                self._root = None
            
        # Case 2: Node has one child
        elif not node_to_delete._left or not node_to_delete._right:
            child = node_to_delete._left if node_to_delete._left else node_to_delete._right
            if parent:
                if parent._left == node_to_delete:
                    parent._left = child
                else:
                    parent._right = child
                child._parent = parent
                self._rebalance(parent)
            else: # Deleting the root
                self._root = child
                child._parent = None
                self._rebalance(child) # Rebalance from the new root if it exists

        # Case 3: Node has two children
        else:
            successor = node_to_delete._right
            while successor._left:
                successor = successor._left
            
            node_to_delete._element = successor._element # Replace data
            # Now delete the successor, which has at most one right child
            self._delete_node(successor) # Recursive call, rebalancing will be handled there
            return # Avoid double rebalancing or size decrement

        self._size -= 1


    def delete(self, element):
        node_to_delete = self.search(element)
        if node_to_delete:
            self._delete_node(node_to_delete)
        # Rebalancing is handled within _delete_node


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
        print(f'{"    "*depth}* {node._element}({node._height}){label}')
        if node._left != None:
            self._display(node._left, depth+1)