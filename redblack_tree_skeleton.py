class RedBlackTree():
    class _Node:
        RED = 0
        BLACK = 1
        """Lightweight, nonpublic class for storing a node."""
        __slots__ = '_element', '_parent', '_left', '_right', '_color' # streamline memory usage

        def __init__(self, element, parent=None, left=None, right=None, color=RED):
            self._element = element
            self._parent = parent
            self._left = left
            self._right = right
            self._color = color

    def __init__(self):
        """Create an initially empty binary tree."""
        self._root = None
        self._size = 0

    def search(self, element):
        curr = self._root
        while curr is not None:
            if curr._element == element:
                return curr
            elif curr._element < element:
                curr = curr._right
            else:
                curr = curr._left
        return None

    def insert(self, element):
        # 1. Handle insertion into an empty tree
        if self._root is None:
            self._root = self._Node(element, color=self._Node.BLACK)
            self._size = 1
            return

        # 2. Standard BST insertion
        bst_parent_node = None
        current_node = self._root
        while current_node is not None:
            bst_parent_node = current_node
            if element < current_node._element:
                current_node = current_node._left
            elif element > current_node._element:
                current_node = current_node._right
            else:
                return  # Element already exists, do nothing

        new_node = self._Node(element, parent=bst_parent_node, color=self._Node.RED)
        if bst_parent_node is None: # Should be caught by root check, but as a safeguard
             self._root = new_node # new_node is RED here, will be fixed
        elif new_node._element < bst_parent_node._element:
            bst_parent_node._left = new_node
        else:
            bst_parent_node._right = new_node
        
        # 3. Increment size
        self._size += 1

        # 4. Inline Fixup Logic (formerly _insert_fixup)
        fixup_node = new_node
        while fixup_node != self._root and fixup_node._parent._color == self._Node.RED:
            parent = fixup_node._parent
            grandparent = parent._parent 
            
            # This check should not be needed if tree properties are maintained,
            # as a RED parent implies a BLACK grandparent (root is black or fixup ensures)
            if grandparent is None: 
                break 

            if parent == grandparent._left:
                uncle = grandparent._right
                # Case 1: Uncle is RED
                if uncle is not None and uncle._color == self._Node.RED:
                    parent._color = self._Node.BLACK
                    uncle._color = self._Node.BLACK
                    grandparent._color = self._Node.RED
                    fixup_node = grandparent
                # Case 2: Uncle is BLACK (or None)
                else:
                    # Case 2a: fixup_node is right child (LR zig-zag)
                    if fixup_node == parent._right:
                        fixup_node = parent
                        # Inlined _rotate_left(fixup_node)
                        #   Original 'x' in rotate_left is fixup_node (parent)
                        #   Original 'y' in rotate_left is y_rot (child)
                        y_rot = fixup_node._right 
                        fixup_node._right = y_rot._left
                        if y_rot._left is not None:
                            y_rot._left._parent = fixup_node
                        y_rot._parent = fixup_node._parent
                        if fixup_node._parent is None:
                            self._root = y_rot
                        elif fixup_node == fixup_node._parent._left:
                            fixup_node._parent._left = y_rot
                        else:
                            fixup_node._parent._right = y_rot
                        y_rot._left = fixup_node
                        fixup_node._parent = y_rot
                        # After rotation, fixup_node is now y_rot. The original parent of fixup_node is now fixup_node.left
                        # The new parent of fixup_node (which was fixup_node.right) is y_rot
                        # The new parent for the next step is y_rot._parent, which is original grandparent
                        parent = fixup_node._parent # parent is now y_rot

                    # Case 2b: fixup_node is left child (LL straight line)
                    parent._color = self._Node.BLACK
                    if grandparent is not None: # Grandparent must exist if parent is RED and not root
                        grandparent._color = self._Node.RED
                        # Inlined _rotate_right(grandparent)
                        #   Original 'y' in rotate_right is grandparent
                        #   Original 'x' in rotate_right is x_rot (parent)
                        x_rot = grandparent._left # This is `parent`
                        grandparent._left = x_rot._right
                        if x_rot._right is not None:
                            x_rot._right._parent = grandparent
                        x_rot._parent = grandparent._parent
                        if grandparent._parent is None:
                            self._root = x_rot
                        elif grandparent == grandparent._parent._right:
                            grandparent._parent._right = x_rot
                        else:
                            grandparent._parent._left = x_rot
                        x_rot._right = grandparent
                        grandparent._parent = x_rot
            else: # Symmetric: parent == grandparent._right
                uncle = grandparent._left
                # Case 1: Uncle is RED
                if uncle is not None and uncle._color == self._Node.RED:
                    parent._color = self._Node.BLACK
                    uncle._color = self._Node.BLACK
                    grandparent._color = self._Node.RED
                    fixup_node = grandparent
                # Case 2: Uncle is BLACK (or None)
                else:
                    # Case 2a: fixup_node is left child (RL zig-zag)
                    if fixup_node == parent._left:
                        fixup_node = parent
                        # Inlined _rotate_right(fixup_node)
                        #   Original 'y' in rotate_right is fixup_node (parent)
                        #   Original 'x' in rotate_right is x_rot (child)
                        x_rot = fixup_node._left
                        fixup_node._left = x_rot._right
                        if x_rot._right is not None:
                            x_rot._right._parent = fixup_node
                        x_rot._parent = fixup_node._parent
                        if fixup_node._parent is None:
                            self._root = x_rot
                        elif fixup_node == fixup_node._parent._right:
                            fixup_node._parent._right = x_rot
                        else:
                            fixup_node._parent._left = x_rot
                        x_rot._right = fixup_node
                        fixup_node._parent = x_rot
                        parent = fixup_node._parent # parent is now x_rot

                    # Case 2b: fixup_node is right child (RR straight line)
                    parent._color = self._Node.BLACK
                    if grandparent is not None: # Grandparent must exist
                        grandparent._color = self._Node.RED
                        # Inlined _rotate_left(grandparent)
                        #   Original 'x' in rotate_left is grandparent
                        #   Original 'y' in rotate_left is y_rot (parent)
                        y_rot = grandparent._right # This is `parent`
                        grandparent._right = y_rot._left
                        if y_rot._left is not None:
                            y_rot._left._parent = grandparent
                        y_rot._parent = grandparent._parent
                        if grandparent._parent is None:
                            self._root = y_rot
                        elif grandparent == grandparent._parent._left:
                            grandparent._parent._left = y_rot
                        else:
                            grandparent._parent._right = y_rot
                        y_rot._left = grandparent
                        grandparent._parent = y_rot
            
            # Ensure fixup_node._parent is not None before accessing grandparent in next iteration
            if fixup_node == self._root: # Moved to root
                break
        
        # 5. Ensure root is BLACK
        if self._root is not None:
            self._root._color = self._Node.BLACK

    def delete(self, element):
        # --- Inlined Search Logic ---
        node_to_delete_z = self._root
        while node_to_delete_z is not None:
            if node_to_delete_z._element == element:
                break 
            elif node_to_delete_z._element < element:
                node_to_delete_z = node_to_delete_z._right
            else:
                node_to_delete_z = node_to_delete_z._left
        
        if node_to_delete_z is None:
            return # Element not found

        # --- Deletion Logic ---
        # y is the node to be actually spliced out from the tree.
        # It's either node_to_delete_z itself or its in-order successor.
        y = node_to_delete_z
        y_original_color = y._color
        
        # x is the child of y that will replace y in the tree.
        # x_parent is the parent of x's position after y is spliced.
        # x_is_left_child indicates if x's position is a left child of x_parent.
        x = None
        x_parent = None
        x_is_left_child = False # Default, will be updated

        if node_to_delete_z._left is None: # z has no left child or at most one (right) child
            x = node_to_delete_z._right
            x_parent = node_to_delete_z._parent
            # Inlined _transplant(node_to_delete_z, x)
            if node_to_delete_z._parent is None:
                self._root = x
            elif node_to_delete_z == node_to_delete_z._parent._left:
                node_to_delete_z._parent._left = x
                x_is_left_child = True
            else:
                node_to_delete_z._parent._right = x
                x_is_left_child = False
            if x is not None:
                x._parent = node_to_delete_z._parent
            
        elif node_to_delete_z._right is None: # z has only a left child
            x = node_to_delete_z._left
            x_parent = node_to_delete_z._parent
            # Inlined _transplant(node_to_delete_z, x)
            if node_to_delete_z._parent is None:
                self._root = x
            elif node_to_delete_z == node_to_delete_z._parent._left:
                node_to_delete_z._parent._left = x
                x_is_left_child = True
            else:
                node_to_delete_z._parent._right = x
                x_is_left_child = False
            if x is not None:
                x._parent = node_to_delete_z._parent

        else: # z has two children
            # Find in-order successor y (formerly _minimum in z's right subtree)
            y = node_to_delete_z._right
            while y._left is not None:
                y = y._left
            
            y_original_color = y._color
            x = y._right # x is the right child of successor y (y has no left child)

            if y._parent == node_to_delete_z: 
                # Successor y is direct child of z.
                # x_parent for fixup will be y itself, as x is y's child.
                x_parent = y 
                if x is not None:
                    x._parent = y # x's parent is y (which will move into z's spot)
                # x_is_left_child determined by x relative to y (it's y's right child)
                # This will be set before fixup call based on x_parent._left == x
            else:
                # Successor y is not a direct child of z.
                # x_parent for fixup is y's original parent.
                x_parent = y._parent
                # Inlined _transplant(y, x) - y is replaced by its child x
                # (y is y._parent's child, we need to know which one for x_is_left_child)
                if y == y._parent._left:
                    y._parent._left = x
                    # x_is_left_child = True; (relative to y._parent)
                else:
                    y._parent._right = x
                    # x_is_left_child = False; (relative to y._parent)
                if x is not None:
                    x._parent = y._parent
            
            # Now, y replaces node_to_delete_z
            # Inlined _transplant(node_to_delete_z, y)
            if node_to_delete_z._parent is None:
                self._root = y
            elif node_to_delete_z == node_to_delete_z._parent._left:
                node_to_delete_z._parent._left = y
            else:
                node_to_delete_z._parent._right = y
            y._parent = node_to_delete_z._parent

            y._left = node_to_delete_z._left
            if y._left is not None:
                y._left._parent = y
            
            # If y was NOT direct child of z, y's original right child (x) has already been transplanted.
            # We also need to connect y to z's original right subtree (excluding y itself).
            if y != node_to_delete_z._right: # y was not direct child
                # x (y's original right child) is already in y's old spot.
                # y needs to adopt z's right child.
                # However, y._right was already set to x (or x was set as child of y_parent)
                # The node y takes z's right child.
                # If y had a right child x, that x is now child of y._parent.
                # y itself now needs to point to z._right.
                # This part of logic for y taking z's children is complex.
                # Standard CLRS: y._right = z._right; y._right._parent = y;
                # But if y *was* z._right, y._right is already x.
                # The `x_parent` setting logic for fixup depends on where x ends up.

                # Let's trace x_parent carefully for fixup:
                # if y._parent was node_to_delete_z: x_parent = y (fixup is for child of y)
                # else: x_parent = y._parent (fixup is for child of y's original parent)
                # This `x_parent` is correct.
                 y._right = node_to_delete_z._right # y takes z's right subtree
                 if y._right is not None: y._right._parent = y # update parent
            else: # y was z's direct right child. x_parent is y.
                  # y._right is already x (y's original right child).
                  pass


            y._color = node_to_delete_z._color # y takes z's color

        # --- Decrement Size ---
        if node_to_delete_z is not None : # if a node was found and processed
            self._size -= 1

        # --- Inline Fixup Logic (if y's original color was BLACK) ---
        if y_original_color == self._Node.BLACK:
            # Determine x_is_left_child for the fixup loop based on x_parent
            # This must be done carefully after all transplants.
            if x_parent is not None: # If x_parent is None, x is root or tree became empty
                if x == x_parent._left:
                    x_is_left_child = True
                else: # x could be None, or x_parent._right == x
                    x_is_left_child = False
            
            # Loop for fixup (formerly _delete_fixup)
            # `x` is the node with extra blackness (can be None)
            # `x_parent` is its parent
            # `x_is_left_child` indicates if x's position is left of `x_parent`
            while x != self._root and (x is None or x._color == self._Node.BLACK):
                if x_parent is None: # Should not happen if x is not root
                    break

                if x_is_left_child:
                    sibling_w = x_parent._right
                    
                    # Case 1: Sibling w is RED
                    if sibling_w is not None and sibling_w._color == self._Node.RED:
                        sibling_w._color = self._Node.BLACK
                        x_parent._color = self._Node.RED
                        # Inlined _rotate_left(x_parent)
                        rot_y = x_parent._right # This is sibling_w
                        x_parent._right = rot_y._left
                        if rot_y._left is not None: rot_y._left._parent = x_parent
                        rot_y._parent = x_parent._parent
                        if x_parent._parent is None: self._root = rot_y
                        elif x_parent == x_parent._parent._left: x_parent._parent._left = rot_y
                        else: x_parent._parent._right = rot_y
                        rot_y._left = x_parent
                        x_parent._parent = rot_y
                        sibling_w = x_parent._right # New sibling, must be BLACK

                    # Sibling w is BLACK (or None, treated as BLACK)
                    # Check sibling's children's colors (None children are BLACK)
                    s_left_is_red = (sibling_w is not None and sibling_w._left is not None and 
                                     sibling_w._left._color == self._Node.RED)
                    s_right_is_red = (sibling_w is not None and sibling_w._right is not None and 
                                      sibling_w._right._color == self._Node.RED)

                    # Case 2: Sibling w is BLACK, and both of w's children are BLACK
                    if not s_left_is_red and not s_right_is_red:
                        if sibling_w is not None: sibling_w._color = self._Node.RED
                        x = x_parent # Move extra black up
                        if x is not None: # Update x_parent and x_is_left_child for next iteration
                            x_parent = x._parent
                            if x_parent is not None: x_is_left_child = (x == x_parent._left)
                            else: break # x is root
                        else: break # x became None
                    else:
                        # Case 3: Sibling w is BLACK, w's left child is RED, w's right child is BLACK
                        if not s_right_is_red: # (and s_left_is_red must be true)
                            if sibling_w._left is not None: sibling_w._left._color = self._Node.BLACK
                            if sibling_w is not None: sibling_w._color = self._Node.RED
                            # Inlined _rotate_right(sibling_w)
                            rot_x = sibling_w._left
                            sibling_w._left = rot_x._right
                            if rot_x._right is not None: rot_x._right._parent = sibling_w
                            rot_x._parent = sibling_w._parent
                            if sibling_w._parent is None: self._root = rot_x
                            elif sibling_w == sibling_w._parent._right: sibling_w._parent._right = rot_x
                            else: sibling_w._parent._left = rot_x
                            rot_x._right = sibling_w
                            sibling_w._parent = rot_x
                            sibling_w = x_parent._right # New sibling
                            # Update s_right_is_red for Case 4, sibling properties changed
                            s_right_is_red = (sibling_w is not None and sibling_w._right is not None and 
                                             sibling_w._right._color == self._Node.RED)


                        # Case 4: Sibling w is BLACK, w's right child is RED
                        if sibling_w is not None: sibling_w._color = x_parent._color
                        x_parent._color = self._Node.BLACK
                        if sibling_w._right is not None: sibling_w._right._color = self._Node.BLACK
                        # Inlined _rotate_left(x_parent)
                        rot_y = x_parent._right # This is sibling_w
                        x_parent._right = rot_y._left
                        if rot_y._left is not None: rot_y._left._parent = x_parent
                        rot_y._parent = x_parent._parent
                        if x_parent._parent is None: self._root = rot_y
                        elif x_parent == x_parent._parent._left: x_parent._parent._left = rot_y
                        else: x_parent._parent._right = rot_y
                        rot_y._left = x_parent
                        x_parent._parent = rot_y
                        x = self._root # Fixup complete
                else: # Symmetric: x_is_left_child is False (x is right child)
                    sibling_w = x_parent._left

                    # Case 1: Sibling w is RED
                    if sibling_w is not None and sibling_w._color == self._Node.RED:
                        sibling_w._color = self._Node.BLACK
                        x_parent._color = self._Node.RED
                        # Inlined _rotate_right(x_parent)
                        rot_x = x_parent._left # This is sibling_w
                        x_parent._left = rot_x._right
                        if rot_x._right is not None: rot_x._right._parent = x_parent
                        rot_x._parent = x_parent._parent
                        if x_parent._parent is None: self._root = rot_x
                        elif x_parent == x_parent._parent._right: x_parent._parent._right = rot_x
                        else: x_parent._parent._left = rot_x
                        rot_x._right = x_parent
                        x_parent._parent = rot_x
                        sibling_w = x_parent._left # New sibling

                    s_left_is_red = (sibling_w is not None and sibling_w._left is not None and 
                                     sibling_w._left._color == self._Node.RED)
                    s_right_is_red = (sibling_w is not None and sibling_w._right is not None and 
                                      sibling_w._right._color == self._Node.RED)

                    # Case 2: Sibling w is BLACK, and both of w's children are BLACK
                    if not s_left_is_red and not s_right_is_red:
                        if sibling_w is not None: sibling_w._color = self._Node.RED
                        x = x_parent
                        if x is not None: # Update x_parent and x_is_left_child for next iteration
                            x_parent = x._parent
                            if x_parent is not None: x_is_left_child = (x == x_parent._left)
                            else: break # x is root
                        else: break # x became None
                    else:
                        # Case 3: Sibling w is BLACK, w's right child is RED, w's left child is BLACK
                        if not s_left_is_red: # (and s_right_is_red must be true)
                            if sibling_w._right is not None: sibling_w._right._color = self._Node.BLACK
                            if sibling_w is not None: sibling_w._color = self._Node.RED
                            # Inlined _rotate_left(sibling_w)
                            rot_y = sibling_w._right
                            sibling_w._right = rot_y._left
                            if rot_y._left is not None: rot_y._left._parent = sibling_w
                            rot_y._parent = sibling_w._parent
                            if sibling_w._parent is None: self._root = rot_y
                            elif sibling_w == sibling_w._parent._left: sibling_w._parent._left = rot_y
                            else: sibling_w._parent._right = rot_y
                            rot_y._left = sibling_w
                            sibling_w._parent = rot_y
                            sibling_w = x_parent._left # New sibling
                            # Update s_left_is_red for Case 4
                            s_left_is_red = (sibling_w is not None and sibling_w._left is not None and 
                                             sibling_w._left._color == self._Node.RED)

                        # Case 4: Sibling w is BLACK, w's left child is RED
                        if sibling_w is not None: sibling_w._color = x_parent._color
                        x_parent._color = self._Node.BLACK
                        if sibling_w._left is not None: sibling_w._left._color = self._Node.BLACK
                        # Inlined _rotate_right(x_parent)
                        rot_x = x_parent._left # This is sibling_w
                        x_parent._left = rot_x._right
                        if rot_x._right is not None: rot_x._right._parent = x_parent
                        rot_x._parent = x_parent._parent
                        if x_parent._parent is None: self._root = rot_x
                        elif x_parent == x_parent._parent._right: x_parent._parent._right = rot_x
                        else: x_parent._parent._left = rot_x
                        rot_x._right = x_parent
                        x_parent._parent = rot_x
                        x = self._root # Fixup complete
            
            # After one iteration of fixup, if x is not self.root, update x_parent and x_is_left_child
            if x != self._root and x is not None:
                x_parent = x._parent
                if x_parent is not None:
                    x_is_left_child = (x == x_parent._left)
                else: # x became root or its parent became None (should not happen if x is not root)
                    break 
            elif x is None and x_parent is None: # x is None and has no parent (e.g. empty tree after delete)
                 break


        # Ensure x (which could be root after fixup) is black
        if x is not None: 
            x._color = self._Node.BLACK
        # Final check on root color, critical if x is None and tree is not empty
        elif self._root is not None: 
             self._root._color = self._Node.BLACK

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

        if node._color == self._Node.RED:
            colorstr = 'R'
        else:
            colorstr = 'B'
        print(f'{"    "*depth}* {node._element}({colorstr}){label}')
        if node._left != None:
            self._display(node._left, depth+1)

