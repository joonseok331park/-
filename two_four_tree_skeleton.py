class TwoFourTree():
    class _Node:
        """Lightweight, nonpublic class for storing a node."""
        __slots__ = '_parent', '_keys', '_children' # streamline memory usage

        def __init__(self, parent=None, keys=[], children=[]):
            self._parent = parent
            self._keys = keys
            self._children = children

    def __init__(self):
        """Create an initially empty binary tree."""
        self._root = None
        self._size = 0

    def search(self, element):
        ## IMPLEMENT HERE

    def insert(self, element):
        ## IMPLEMENT HERE

    def delete(self, element):
        ## IMPLEMENT HERE

    def display(self):
        self._display(self._root, 0)

    def _display(self, node, depth):
        if node == None:
            return
        
        label = ''
        if node == self._root:
            label += '  <- root'
        
        print(f'{"    "*depth}* {node._keys}{label}')
        
        if node._children:
            for child in node._children:
                self._display(child, depth + 1)

    def search(self, element):
        current_node = self._root
        while current_node is not None:
            found_in_node = False
            # Iterate through keys to find element or determine next child
            for i, key_in_node in enumerate(current_node._keys):
                if element == key_in_node:
                    return (current_node, i) # Element found
                
                if element < key_in_node:
                    # If element is smaller, and this is an internal node, descend to child[i]
                    if current_node._children: # Check if it's an internal node
                        if i < len(current_node._children):
                            current_node = current_node._children[i]
                            found_in_node = True # Indicates we've moved to a child
                            break 
                        else: # Should not happen in a valid 2-4 tree (num_children = num_keys + 1)
                            return None # Or raise error, indicates malformed tree
                    else: # Leaf node, element not found (and smaller than current key)
                        return None 
            
            if found_in_node: # If we descended to a child, continue the outer while loop
                continue

            # If element is larger than all keys in the node (or node was empty)
            if not found_in_node: # Only if we didn't descend already
                if current_node._children: # Internal node
                    if len(current_node._children) > len(current_node._keys): # Must have a last child
                        current_node = current_node._children[len(current_node._keys)]
                    else: # Leaf node (or malformed internal if no last child)
                        # If it's a leaf, and we are here, element > all keys in leaf, so not found
                        return None
                else: # Leaf node, and element > all keys
                    return None
        
        return None # Element not found (e.g., tree is empty or fell through logic)

    def insert(self, element):
        # 1. Handle Empty Tree
        if self._root is None:
            self._root = self._Node(keys=[element])
            self._size = 1
            return

        # 2. Find Leaf for Insertion (or node containing element)
        current_node = self._root
        path_to_leaf = [] # Not strictly needed for inlining, but helps conceptualize
        
        while True:
            path_to_leaf.append(current_node) # Keep track for potential splits
            # Check if element exists
            for key_in_node in current_node._keys:
                if element == key_in_node:
                    return # Element already exists

            if not current_node._children: # Leaf node found
                break

            # Descend to the correct child
            found_child_path = False
            for i, key_in_node in enumerate(current_node._keys):
                if element < key_in_node:
                    current_node = current_node._children[i]
                    found_child_path = True
                    break
            if not found_child_path: # Element is greater than all keys
                current_node = current_node._children[len(current_node._keys)]
        
        # 3. Insert Element in Leaf (current_node is the leaf)
        current_node._keys.append(element)
        current_node._keys.sort()
        self._size += 1

        # 4. Inlined Overflow Handling (Splitting Loop)
        # node_to_check starts as the leaf where insertion happened
        node_to_check = current_node 

        while len(node_to_check._keys) > 3: # Max 3 keys allowed in a 2-4 tree node
            # Overflow detected
            
            # Middle key for 2-4 tree with 4 keys [k0,k1,k2,k3] is k1 (index 1) to go up.
            # Left node gets k0. Right node gets k2, k3.
            # Or, middle key k2 (index 2) goes up. Left node k0,k1. Right node k3. (Textbook version)
            # Let's use: middle key at index 1 (k1) goes up. k0 stays. k2, k3 go to new sibling.
            # This simplifies child distribution: first 2 children with k0, last 2 with k2,k3.
            
            # Using CLRS/Sedgewick approach: 4-node (3 keys) splits into two 2-nodes, middle key goes up.
            # If node has [k0, k1, k2, k3] -> k1 goes up. Left child [k0]. Right child [k2, k3].
            # Children distribution: children [c0,c1,c2,c3,c4]
            # Original node: keys=[k0], children=[c0,c1]
            # New sibling: keys=[k2,k3], children=[c2,c3,c4]
            # This seems more standard. Let's use this. Middle key is keys[1] of the 4 keys.
            
            # If we have 4 keys: k0, k1, k2, k3
            middle_key_val = node_to_check._keys[1] # k1 goes up
            
            new_sibling_node = self._Node(parent=node_to_check._parent)
            new_sibling_node._keys = node_to_check._keys[2:] # k2, k3

            # Original node keeps k0
            node_to_check._keys = [node_to_check._keys[0]] 
            
            if node_to_check._children: # If it's an internal node, distribute children
                # Original node keeps first 2 children (for key k0)
                # New sibling gets last 3 children (for keys k2, k3)
                # This means original node had 5 children with 4 keys, which is wrong.
                # A node with N keys has N+1 children. If 4 keys, 5 children.
                # Children: c0 c1 c2 c3 c4
                # k0 k1 k2 k3
                # Node1: keys=[k0], children=[c0,c1]
                # Key up: k1
                # Node2: keys=[k2,k3], children=[c2,c3,c4]
                
                new_sibling_node._children = node_to_check._children[2:]
                for child in new_sibling_node._children:
                    child._parent = new_sibling_node
                
                node_to_check._children = node_to_check._children[0:2]
                # Children that remain with node_to_check already have correct parent.

            parent_of_split_node = node_to_check._parent

            if parent_of_split_node is None: # node_to_check was the root
                new_root_node = self._Node(keys=[middle_key_val])
                new_root_node._children = [node_to_check, new_sibling_node]
                node_to_check._parent = new_root_node
                new_sibling_node._parent = new_root_node
                self._root = new_root_node
                break # Tree height increased, overflow handled for root.
            else:
                # Insert middle_key_val into parent_of_split_node
                insert_idx = 0
                while insert_idx < len(parent_of_split_node._keys) and \
                      parent_of_split_node._keys[insert_idx] < middle_key_val:
                    insert_idx += 1
                parent_of_split_node._keys.insert(insert_idx, middle_key_val)
                
                # Insert new_sibling_node into parent_of_split_node's children
                parent_of_split_node._children.insert(insert_idx + 1, new_sibling_node)
                new_sibling_node._parent = parent_of_split_node # already set, but good for clarity

                node_to_check = parent_of_split_node # Move up to check parent for overflow
        
        # No return value for insert

    def delete(self, element):
        if self._root is None:
            return

        # --- 1 & 2. Find Node Containing Element and Path ---
        current_node = self._root
        parent_of_current = None 
        path_nodes_stack = [] # Stores (node, child_index_in_parent)

        target_node = None
        key_idx_in_target = -1

        while current_node is not None:
            # Determine child_idx for current_node relative to parent_of_current
            child_idx_for_path = -1
            if parent_of_current:
                for i, child in enumerate(parent_of_current._children):
                    if child == current_node:
                        child_idx_for_path = i
                        break
            path_nodes_stack.append({'node': current_node, 'parent': parent_of_current, 'child_idx': child_idx_for_path})

            found_key_in_current_node = False
            for i, k_val in enumerate(current_node._keys):
                if element == k_val:
                    target_node = current_node
                    key_idx_in_target = i
                    found_key_in_current_node = True # Element found
                    break 
                if element < k_val: # Potential descent path
                    if not current_node._children: # Leaf reached, element not found
                        target_node = None; break 
                    parent_of_current = current_node
                    current_node = current_node._children[i]
                    found_key_in_current_node = True # Indicates descent, not necessarily element found
                    break
            
            if target_node is not None and target_node._element == element : break # Element located
            if target_node is None and not current_node._children and not found_key_in_current_node : break # Leaf, element > all keys

            if not found_key_in_current_node: # Element > all keys in current_node
                if not current_node._children: # Leaf reached
                    target_node = None; break 
                parent_of_current = current_node
                current_node = current_node._children[len(current_node._keys)]
        
        if target_node is None or key_idx_in_target == -1 : # Element not found in tree
            return

        # --- 3. Handle Non-Leaf Deletion (Swap with Successor) ---
        node_for_actual_deletion = target_node
        element_to_delete_from_leaf = target_node._keys[key_idx_in_target] # Actual value

        if target_node._children: # target_node is internal
            # Find successor
            # Successor path starts from child right of the key_idx_in_target
            # Add internal target_node itself to path for successor finding, as it's parent of successor's initial subtree
            path_nodes_stack.append({'node': target_node._children[key_idx_in_target + 1], 
                                     'parent': target_node, 
                                     'child_idx': key_idx_in_target + 1})
            
            succ_node = target_node._children[key_idx_in_target + 1]
            succ_parent = target_node
            
            while succ_node._children: # Descend to the leftmost node
                succ_parent = succ_node
                # Need to record path to successor for potential underflow propagation
                path_nodes_stack.append({'node': succ_node._children[0], 
                                         'parent': succ_parent, 
                                         'child_idx': 0})
                succ_node = succ_node._children[0]
            
            # Swap element with successor's first key
            element_to_delete_from_leaf = succ_node._keys[0] # This is the value to remove from leaf
            target_node._keys[key_idx_in_target] = succ_node._keys[0] # Actual swap
            node_for_actual_deletion = succ_node # This is the leaf (or near-leaf) to delete from
            # Key to remove from this node is its first key (which is now element_to_delete_from_leaf)
            # The element to remove from node_for_actual_deletion._keys is element_to_delete_from_leaf
            # which is node_for_actual_deletion._keys[0]

        # --- 4. Delete Element from Leaf/Near-Leaf (`node_for_actual_deletion`) ---
        # Remove the specific element value that was identified for deletion from this node
        if element_to_delete_from_leaf in node_for_actual_deletion._keys:
             node_for_actual_deletion._keys.remove(element_to_delete_from_leaf)
        self._size -= 1

        # --- 5. Inlined Underflow Handling ---
        current_deficient_node = node_for_actual_deletion
        
        # Loop while current_deficient_node has too few keys (0 for non-root, or root becomes childless with 0 keys)
        while len(current_deficient_node._keys) < 1:
            # Pop current node's info from path; its parent is now top of stack (if path exists)
            if not path_nodes_stack or path_nodes_stack[-1]['node'] != current_deficient_node :
                # This implies path tracking error or current_deficient_node is root and path was not built for it.
                # If current_deficient_node is root, its parent is None.
                 if current_deficient_node != self._root: break # Should not happen if path tracking is correct
            
            # If current_deficient_node is root
            if current_deficient_node == self._root:
                if not current_deficient_node._keys and current_deficient_node._children:
                    # Root is empty, promote its only child
                    self._root = current_deficient_node._children[0]
                    self._root._parent = None
                    current_deficient_node._children = [] # Avoid cycles, old root discarded
                elif not current_deficient_node._keys and not current_deficient_node._children:
                    self._root = None # Tree becomes empty
                break # Underflow at root is handled

            # Pop current node from path to get its parent and its index in parent's children
            # The last entry in path_nodes_stack is current_deficient_node itself if path was built to it
            # If path was built to original target_node, and then extended for successor,
            # path_nodes_stack top is node_for_actual_deletion.
            
            # We need parent of current_deficient_node.
            # The path_nodes_stack stores {'node': N, 'parent': P, 'child_idx': I}
            # The last element on stack is current_deficient_node. Its 'parent' and 'child_idx' are relevant.
            
            path_entry_for_deficient = None
            # Find current_deficient_node in path_stack to get its parent and child_idx
            # This is inefficient; parent should be directly accessible or passed down.
            # For inlining, let's assume current_deficient_node._parent is correct.
            parent_node = current_deficient_node._parent
            if parent_node is None: # Should have been caught by root check
                 break

            child_idx_in_parent = -1
            for i, child in enumerate(parent_node._children):
                if child == current_deficient_node:
                    child_idx_in_parent = i
                    break
            if child_idx_in_parent == -1: break # Should not happen

            # Try Redistribution with Left Sibling
            can_redistribute = False
            if child_idx_in_parent > 0:
                left_sibling = parent_node._children[child_idx_in_parent - 1]
                if len(left_sibling._keys) > 1: # Left sibling can give a key
                    # Move key from parent down to current_deficient_node (prepend)
                    current_deficient_node._keys.insert(0, parent_node._keys[child_idx_in_parent - 1])
                    # Move key from left_sibling up to parent
                    parent_node._keys[child_idx_in_parent - 1] = left_sibling._keys.pop() # Last key
                    # Move child pointer if internal node
                    if left_sibling._children:
                        moved_child = left_sibling._children.pop()
                        moved_child._parent = current_deficient_node
                        current_deficient_node._children.insert(0, moved_child)
                    can_redistribute = True
            
            if not can_redistribute and child_idx_in_parent < len(parent_node._keys): # len(parent_node._children) -1
                # Try Redistribution with Right Sibling
                if child_idx_in_parent + 1 < len(parent_node._children): # Check if right sibling exists
                    right_sibling = parent_node._children[child_idx_in_parent + 1]
                    if len(right_sibling._keys) > 1: # Right sibling can give a key
                        # Move key from parent down to current_deficient_node (append)
                        current_deficient_node._keys.append(parent_node._keys[child_idx_in_parent])
                        # Move key from right_sibling up to parent
                        parent_node._keys[child_idx_in_parent] = right_sibling._keys.pop(0) # First key
                        # Move child pointer if internal node
                        if right_sibling._children:
                            moved_child = right_sibling._children.pop(0)
                            moved_child._parent = current_deficient_node
                            current_deficient_node._children.append(moved_child)
                        can_redistribute = True

            if can_redistribute:
                break # Underflow resolved by redistribution

            # Else (Merge required)
            if child_idx_in_parent > 0: # Merge with left sibling
                left_sibling = parent_node._children[child_idx_in_parent - 1]
                # Pull key from parent into left_sibling
                key_from_parent = parent_node._keys.pop(child_idx_in_parent - 1)
                left_sibling._keys.append(key_from_parent)
                # Move keys and children from current_deficient_node to left_sibling
                left_sibling._keys.extend(current_deficient_node._keys)
                if current_deficient_node._children:
                    left_sibling._children.extend(current_deficient_node._children)
                    for child in current_deficient_node._children: # Re-parent children
                        child._parent = left_sibling
                
                # Remove current_deficient_node from parent's children
                parent_node._children.pop(child_idx_in_parent)
                current_deficient_node = parent_node # Move up to check parent
            
            elif child_idx_in_parent < len(parent_node._children) -1 : # Merge with right sibling (current is leftmost)
                right_sibling = parent_node._children[child_idx_in_parent + 1]
                 # Pull key from parent into current_deficient_node (or conceptually into merged node which is right_sibling)
                key_from_parent = parent_node._keys.pop(child_idx_in_parent) # Key between current and right sibling
                
                # Merge current_deficient_node into right_sibling
                # Prepend parent key and current_deficient_node's keys to right_sibling
                right_sibling._keys = current_deficient_node._keys + [key_from_parent] + right_sibling._keys
                if current_deficient_node._children: # If internal, move children
                    # Prepend current_deficient_node's children to right_sibling's children
                    right_sibling._children = current_deficient_node._children + right_sibling._children
                    for child in current_deficient_node._children: # Re-parent
                        child._parent = right_sibling
                
                # Remove current_deficient_node from parent's children
                parent_node._children.pop(child_idx_in_parent)
                current_deficient_node = parent_node # Move up
            else: # Should not happen if logic is correct (e.g. single child of root underflows)
                break
        
        # Final check for root if loop terminated due to current_deficient_node becoming root
        if current_deficient_node == self._root and not current_deficient_node._keys:
            if current_deficient_node._children:
                self._root = current_deficient_node._children[0]
                self._root._parent = None
            else: # Root is empty and no children
                self._root = None
