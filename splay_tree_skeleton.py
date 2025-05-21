class SplayTree():
    class _Node:
        """Lightweight, nonpublic class for storing a node."""
        __slots__ = '_element', '_parent', '_left', '_right' # streamline memory usage

        def __init__(self, element, parent=None, left=None, right=None):
            self._element = element
            self._parent = parent
            self._left = left
            self._right = right

    def __init__(self):
        """Create an initially empty binary tree."""
        self._root = None
        self._size = 0

    def search(self, element):
        if self._root is None:
            return None

        current = self._root
        last_accessed = None
        found_node = None

        # BST-like search
        while current is not None:
            last_accessed = current
            if element == current._element:
                found_node = current
                break
            elif element < current._element:
                current = current._left
            else:
                current = current._right
        
        # Node to splay is either the found_node or the last_accessed node
        node_to_splay = found_node if found_node is not None else last_accessed

        if node_to_splay is None: # Should not happen if root was not None
            return None

        # --- Inlined Splay Logic ---
        while node_to_splay._parent is not None: # While node_to_splay is not the root
            parent = node_to_splay._parent
            grandparent = parent._parent

            # --- Inlined Rotation Logic ---
            if grandparent is None: # Parent is root (Zig case)
                if node_to_splay == parent._left:
                    # Rotate right (Zag based on child's perspective, or Zig on parent)
                    #   Original 'y' in rotate_right is parent
                    #   Original 'x' in rotate_right is node_to_splay
                    parent._left = node_to_splay._right
                    if node_to_splay._right is not None:
                        node_to_splay._right._parent = parent
                    node_to_splay._parent = parent._parent # None
                    # Parent's parent is already None (root)
                    node_to_splay._right = parent
                    parent._parent = node_to_splay
                else: # node_to_splay == parent._right
                    # Rotate left (Zig based on child's perspective, or Zag on parent)
                    #   Original 'x' in rotate_left is parent
                    #   Original 'y' in rotate_left is node_to_splay
                    parent._right = node_to_splay._left
                    if node_to_splay._left is not None:
                        node_to_splay._left._parent = parent
                    node_to_splay._parent = parent._parent # None
                    # Parent's parent is already None (root)
                    node_to_splay._left = parent
                    parent._parent = node_to_splay
                # self._root will be set after loop
            
            else: # Node_to_splay has a grandparent (Zig-Zig or Zig-Zag)
                # Link grandparent to node_to_splay's future position
                node_to_splay._parent = grandparent._parent
                if grandparent._parent is not None:
                    if grandparent == grandparent._parent._left:
                        grandparent._parent._left = node_to_splay
                    else:
                        grandparent._parent._right = node_to_splay
                
                if node_to_splay == parent._left:
                    if parent == grandparent._left: # Zig-Zig (left-left)
                        # Rotate parent around grandparent (rotate right on grandparent)
                        grandparent._left = parent._right
                        if parent._right is not None:
                            parent._right._parent = grandparent
                        parent._right = grandparent
                        grandparent._parent = parent
                        # Rotate node_to_splay around new parent (parent) (rotate right on parent)
                        parent._left = node_to_splay._right
                        if node_to_splay._right is not None:
                            node_to_splay._right._parent = parent
                        node_to_splay._right = parent
                        parent._parent = node_to_splay
                    else: # Zig-Zag (right-left)
                        # Rotate node_to_splay around parent (rotate right on parent)
                        parent._left = node_to_splay._right
                        if node_to_splay._right is not None:
                            node_to_splay._right._parent = parent
                        node_to_splay._right = parent
                        parent._parent = node_to_splay
                        # Rotate node_to_splay around new parent (grandparent) (rotate left on grandparent)
                        grandparent._right = node_to_splay._left # node_to_splay is now parent of original parent
                        if node_to_splay._left is not None:
                            node_to_splay._left._parent = grandparent
                        node_to_splay._left = grandparent
                        grandparent._parent = node_to_splay
                else: # node_to_splay == parent._right
                    if parent == grandparent._right: # Zig-Zig (right-right)
                        # Rotate parent around grandparent (rotate left on grandparent)
                        grandparent._right = parent._left
                        if parent._left is not None:
                            parent._left._parent = grandparent
                        parent._left = grandparent
                        grandparent._parent = parent
                        # Rotate node_to_splay around new parent (parent) (rotate left on parent)
                        parent._right = node_to_splay._left
                        if node_to_splay._left is not None:
                            node_to_splay._left._parent = parent
                        node_to_splay._left = parent
                        parent._parent = node_to_splay
                    else: # Zig-Zag (left-right)
                        # Rotate node_to_splay around parent (rotate left on parent)
                        parent._right = node_to_splay._left
                        if node_to_splay._left is not None:
                            node_to_splay._left._parent = parent
                        node_to_splay._left = parent
                        parent._parent = node_to_splay
                        # Rotate node_to_splay around new parent (grandparent) (rotate right on grandparent)
                        grandparent._left = node_to_splay._right # node_to_splay is now parent of original parent
                        if node_to_splay._right is not None:
                            node_to_splay._right._parent = grandparent
                        node_to_splay._right = grandparent
                        grandparent._parent = node_to_splay
            
            if node_to_splay._parent is None: # node_to_splay became root
                self._root = node_to_splay
        
        if self._root != node_to_splay : # Ensure root is updated if loop didn't set it (e.g. splaying original root)
             self._root = node_to_splay
             if node_to_splay is not None : node_to_splay._parent = None # Ensure new root's parent is None


        return found_node


    def insert(self, element):
        # 1. Handle empty tree
        if self._root is None:
            self._root = self._Node(element)
            self._size = 1
            return

        # 2. BST-like search to find node to splay
        current = self._root
        last_accessed = None
        while current is not None:
            last_accessed = current
            if element == current._element:
                break 
            elif element < current._element:
                current = current._left
            else:
                current = current._right
        
        node_to_splay = last_accessed # Splay the last accessed node

        # 3. Inline Splay Logic for node_to_splay
        if node_to_splay is not None:
            while node_to_splay._parent is not None:
                parent = node_to_splay._parent
                grandparent = parent._parent

                if grandparent is None: # Zig case
                    # Update root before splay if parent is root
                    # self._root = node_to_splay # (will be set at end of splay)
                    if node_to_splay == parent._left: # Rotate right on parent
                        parent._left = node_to_splay._right
                        if node_to_splay._right is not None:
                            node_to_splay._right._parent = parent
                        node_to_splay._right = parent
                    else: # Rotate left on parent
                        parent._right = node_to_splay._left
                        if node_to_splay._left is not None:
                            node_to_splay._left._parent = parent
                        node_to_splay._left = parent
                    
                    node_to_splay._parent = None # New root
                    parent._parent = node_to_splay
                    # self._root = node_to_splay # Set at the end of splay
                
                else: # Zig-Zig or Zig-Zag
                    # Common step: Link node_to_splay to grandparent's original parent
                    node_to_splay._parent = grandparent._parent
                    if grandparent._parent is not None:
                        if grandparent == grandparent._parent._left:
                            grandparent._parent._left = node_to_splay
                        else:
                            grandparent._parent._right = node_to_splay
                    
                    if node_to_splay == parent._left:
                        if parent == grandparent._left: # Zig-Zig (left-left)
                            # Rotate parent around grandparent (right rotation on grandparent)
                            grandparent._left = parent._right
                            if parent._right is not None: parent._right._parent = grandparent
                            parent._right = grandparent
                            grandparent._parent = parent
                            # Rotate node_to_splay around new parent (parent) (right rotation on parent)
                            parent._left = node_to_splay._right
                            if node_to_splay._right is not None: node_to_splay._right._parent = parent
                            node_to_splay._right = parent
                            parent._parent = node_to_splay
                        else: # Zig-Zag (right-left)
                            # Rotate node_to_splay around parent (right rotation on parent)
                            parent._left = node_to_splay._right
                            if node_to_splay._right is not None: node_to_splay._right._parent = parent
                            node_to_splay._right = parent
                            parent._parent = node_to_splay 
                            # Rotate node_to_splay around new parent (grandparent) (left rotation on grandparent)
                            grandparent._right = node_to_splay._left 
                            if node_to_splay._left is not None: node_to_splay._left._parent = grandparent
                            node_to_splay._left = grandparent
                            grandparent._parent = node_to_splay
                    else: # node_to_splay == parent._right
                        if parent == grandparent._right: # Zig-Zig (right-right)
                            # Rotate parent around grandparent (left rotation on grandparent)
                            grandparent._right = parent._left
                            if parent._left is not None: parent._left._parent = grandparent
                            parent._left = grandparent
                            grandparent._parent = parent
                            # Rotate node_to_splay around new parent (parent) (left rotation on parent)
                            parent._right = node_to_splay._left
                            if node_to_splay._left is not None: node_to_splay._left._parent = parent
                            node_to_splay._left = parent
                            parent._parent = node_to_splay
                        else: # Zig-Zag (left-right)
                            # Rotate node_to_splay around parent (left rotation on parent)
                            parent._right = node_to_splay._left
                            if node_to_splay._left is not None: node_to_splay._left._parent = parent
                            node_to_splay._left = parent
                            parent._parent = node_to_splay
                            # Rotate node_to_splay around new parent (grandparent) (right rotation on grandparent)
                            grandparent._left = node_to_splay._right
                            if node_to_splay._right is not None: node_to_splay._right._parent = grandparent
                            node_to_splay._right = grandparent
                            grandparent._parent = node_to_splay
                
                if node_to_splay._parent is None: # node_to_splay became root
                    self._root = node_to_splay

            if self._root != node_to_splay: # Ensure root is updated
                self._root = node_to_splay
                if node_to_splay is not None: node_to_splay._parent = None


        # After splaying, node_to_splay is self._root
        # 4. If element already exists
        if self._root is not None and self._root._element == element:
            return # Element exists, splayed, do nothing more for insert

        # 5. Element not found, insert new node
        new_node = self._Node(element)
        self._size += 1

        if self._root is None: # Should have been caught by first check, but for safety after splay of empty/single tree
            self._root = new_node
            return

        # Current self._root is the splayed node (closest to element)
        if element < self._root._element:
            new_node._right = self._root
            new_node._left = self._root._left
            if self._root._left is not None:
                self._root._left._parent = new_node
            self._root._parent = new_node
            self._root._left = None
        else: # element > self._root._element
            new_node._left = self._root
            new_node._right = self._root._right
            if self._root._right is not None:
                self._root._right._parent = new_node
            self._root._parent = new_node
            self._root._right = None
        
        self._root = new_node # New node becomes the root
        self._root._parent = None


    def delete(self, element):
        if self._root is None:
            return

        # 1. Search for the element and splay it (or the last accessed node)
        # --- Inlined Search and Splay Logic (from search method) ---
        current_s = self._root
        last_accessed_s = None
        node_to_splay_s = None # Renamed to avoid conflict with splay logic variables
        
        while current_s is not None:
            last_accessed_s = current_s
            if element == current_s._element:
                node_to_splay_s = current_s
                break
            elif element < current_s._element:
                current_s = current_s._left
            else:
                current_s = current_s._right
        
        if node_to_splay_s is None: # Element not found, splay last accessed
            node_to_splay_s = last_accessed_s
        
        if node_to_splay_s is not None: # Perform splay if a node was identified
            while node_to_splay_s._parent is not None:
                parent_s = node_to_splay_s._parent
                grandparent_s = parent_s._parent
                if grandparent_s is None: # Zig
                    if node_to_splay_s == parent_s._left: # Rotate right on parent_s
                        parent_s._left = node_to_splay_s._right
                        if node_to_splay_s._right is not None: node_to_splay_s._right._parent = parent_s
                        node_to_splay_s._right = parent_s
                    else: # Rotate left on parent_s
                        parent_s._right = node_to_splay_s._left
                        if node_to_splay_s._left is not None: node_to_splay_s._left._parent = parent_s
                        node_to_splay_s._left = parent_s
                    node_to_splay_s._parent = None
                    parent_s._parent = node_to_splay_s
                else: # Zig-Zig or Zig-Zag
                    node_to_splay_s._parent = grandparent_s._parent
                    if grandparent_s._parent is not None:
                        if grandparent_s == grandparent_s._parent._left: grandparent_s._parent._left = node_to_splay_s
                        else: grandparent_s._parent._right = node_to_splay_s
                    
                    if node_to_splay_s == parent_s._left:
                        if parent_s == grandparent_s._left: # Zig-Zig (left-left)
                            grandparent_s._left = parent_s._right
                            if parent_s._right is not None: parent_s._right._parent = grandparent_s
                            parent_s._right = grandparent_s
                            grandparent_s._parent = parent_s
                            parent_s._left = node_to_splay_s._right
                            if node_to_splay_s._right is not None: node_to_splay_s._right._parent = parent_s
                            node_to_splay_s._right = parent_s
                            parent_s._parent = node_to_splay_s
                        else: # Zig-Zag (right-left)
                            parent_s._left = node_to_splay_s._right
                            if node_to_splay_s._right is not None: node_to_splay_s._right._parent = parent_s
                            node_to_splay_s._right = parent_s
                            parent_s._parent = node_to_splay_s
                            grandparent_s._right = node_to_splay_s._left
                            if node_to_splay_s._left is not None: node_to_splay_s._left._parent = grandparent_s
                            node_to_splay_s._left = grandparent_s
                            grandparent_s._parent = node_to_splay_s
                    else: # node_to_splay_s == parent_s._right
                        if parent_s == grandparent_s._right: # Zig-Zig (right-right)
                            grandparent_s._right = parent_s._left
                            if parent_s._left is not None: parent_s._left._parent = grandparent_s
                            parent_s._left = grandparent_s
                            grandparent_s._parent = parent_s
                            parent_s._right = node_to_splay_s._left
                            if node_to_splay_s._left is not None: node_to_splay_s._left._parent = parent_s
                            node_to_splay_s._left = parent_s
                            parent_s._parent = node_to_splay_s
                        else: # Zig-Zag (left-right)
                            parent_s._right = node_to_splay_s._left
                            if node_to_splay_s._left is not None: node_to_splay_s._left._parent = parent_s
                            node_to_splay_s._left = parent_s
                            parent_s._parent = node_to_splay_s
                            grandparent_s._left = node_to_splay_s._right
                            if node_to_splay_s._right is not None: node_to_splay_s._right._parent = grandparent_s
                            node_to_splay_s._right = grandparent_s
                            grandparent_s._parent = node_to_splay_s
                if node_to_splay_s._parent is None: self._root = node_to_splay_s
            if self._root != node_to_splay_s: 
                self._root = node_to_splay_s
                if node_to_splay_s is not None: node_to_splay_s._parent = None
        # --- End of Inlined Search and Splay Logic ---

        # 2. Check if element is at the root
        if self._root is None or self._root._element != element:
            return # Element not found or not splayed to root

        # 3. Element is at the root, proceed with deletion
        deleted_node_actual = self._root # Keep track for size decrement
        
        left_subtree = self._root._left
        right_subtree = self._root._right

        if left_subtree is not None:
            left_subtree._parent = None # Disconnect
        if right_subtree is not None:
            right_subtree._parent = None # Disconnect

        if left_subtree is None:
            self._root = right_subtree
            # if self._root is not None: self._root._parent = None (already done)
        else:
            self._root = left_subtree # Make left_subtree the temporary root
            # self._root._parent = None (already done)

            # Find max in L (current self._root)
            max_in_L_node = self._root
            while max_in_L_node._right is not None:
                max_in_L_node = max_in_L_node._right
            
            # Splay max_in_L_node to the root of the current tree (L)
            if max_in_L_node != self._root : # Only splay if it's not already the root of L
                # --- Inlined Splay Logic for max_in_L_node ---
                # (Here, self._root is the root of L, not the overall tree root yet)
                # Parent of max_in_L_node cannot be None unless max_in_L_node is self._root (root of L)
                while max_in_L_node._parent is not None: # Splay within the context of L
                    parent_l = max_in_L_node._parent
                    grandparent_l = parent_l._parent # Grandparent within L

                    # Common step for Zig-Zig/Zig-Zag: connect max_in_L_node to grandparent_l's original parent
                    # This new parent will be None if grandparent_l was the root of L.
                    max_in_L_node._parent = grandparent_l._parent if grandparent_l else None 
                                                                    # grandparent_l could be None if parent_l is root of L
                    
                    if grandparent_l is None: # Zig Case (parent_l is root of L)
                        if max_in_L_node == parent_l._left: # Rotate right on parent_l
                            parent_l._left = max_in_L_node._right
                            if max_in_L_node._right is not None: max_in_L_node._right._parent = parent_l
                            max_in_L_node._right = parent_l
                        else: # Rotate left on parent_l
                            parent_l._right = max_in_L_node._left
                            if max_in_L_node._left is not None: max_in_L_node._left._parent = parent_l
                            max_in_L_node._left = parent_l
                        # max_in_L_node._parent is already set (to None in this Zig case)
                        parent_l._parent = max_in_L_node
                    else: # Zig-Zig or Zig-Zag
                        # Link to grandparent_l's original parent (if exists)
                        if grandparent_l._parent is not None:
                            if grandparent_l == grandparent_l._parent._left: grandparent_l._parent._left = max_in_L_node
                            else: grandparent_l._parent._right = max_in_L_node
                        # else max_in_L_node will become root of L (parent is None)

                        if max_in_L_node == parent_l._left:
                            if parent_l == grandparent_l._left: # Zig-Zig (left-left)
                                grandparent_l._left = parent_l._right
                                if parent_l._right is not None: parent_l._right._parent = grandparent_l
                                parent_l._right = grandparent_l
                                grandparent_l._parent = parent_l
                                parent_l._left = max_in_L_node._right
                                if max_in_L_node._right is not None: max_in_L_node._right._parent = parent_l
                                max_in_L_node._right = parent_l
                                parent_l._parent = max_in_L_node
                            else: # Zig-Zag (right-left)
                                parent_l._left = max_in_L_node._right
                                if max_in_L_node._right is not None: max_in_L_node._right._parent = parent_l
                                max_in_L_node._right = parent_l
                                parent_l._parent = max_in_L_node
                                grandparent_l._right = max_in_L_node._left
                                if max_in_L_node._left is not None: max_in_L_node._left._parent = grandparent_l
                                max_in_L_node._left = grandparent_l
                                grandparent_l._parent = max_in_L_node
                        else: # max_in_L_node == parent_l._right
                            if parent_l == grandparent_l._right: # Zig-Zig (right-right)
                                grandparent_l._right = parent_l._left
                                if parent_l._left is not None: parent_l._left._parent = grandparent_l
                                parent_l._left = grandparent_l
                                grandparent_l._parent = parent_l
                                parent_l._right = max_in_L_node._left
                                if max_in_L_node._left is not None: max_in_L_node._left._parent = parent_l
                                max_in_L_node._left = parent_l
                                parent_l._parent = max_in_L_node
                            else: # Zig-Zag (left-right)
                                parent_l._right = max_in_L_node._left
                                if max_in_L_node._left is not None: max_in_L_node._left._parent = parent_l
                                max_in_L_node._left = parent_l
                                parent_l._parent = max_in_L_node
                                grandparent_l._left = max_in_L_node._right
                                if max_in_L_node._right is not None: max_in_L_node._right._parent = grandparent_l
                                max_in_L_node._right = grandparent_l
                                grandparent_l._parent = max_in_L_node
                    
                    if max_in_L_node._parent is None: # max_in_L_node became root of L
                        self._root = max_in_L_node # Update self._root to new root of L
                # --- End of Inlined Splay Logic for max_in_L_node ---
                if self._root != max_in_L_node: # Ensure L's root is updated
                    self._root = max_in_L_node 
                    if max_in_L_node is not None: max_in_L_node._parent = None # New root of L has no parent

            # After splaying max_in_L_node, it is self._root (root of L)
            # Its right child should be None. Now attach R.
            self._root._right = right_subtree
            if right_subtree is not None:
                right_subtree._parent = self._root
        
        # 4. Decrement size
        self._size -= 1
        if self._size == 0: # Tree became empty
            self._root = None # Explicitly set root to None


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
