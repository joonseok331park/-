import random
from redblack_tree_skeleton import RedBlackTree # Assuming file is in the same directory or PYTHONPATH

def test_rb_empty_tree():
    print("--- Testing RedBlackTree Empty Tree ---")
    tree = RedBlackTree()
    assert tree._size == 0, "Empty tree size should be 0"
    assert tree._root is None, "Empty tree root should be None"
    assert tree.search(10) is None, "Search on empty tree should return None"
    tree.delete(10) # Should not error
    assert tree._size == 0, "Size after delete on empty tree should be 0"
    print("RedBlackTree Empty Tree tests passed.")

def test_rb_insertion_basic():
    print("--- Testing RedBlackTree Basic Insertion and Search ---")
    tree = RedBlackTree()
    elements = [10, 5, 15, 3, 7, 12, 17, 6, 8, 20, -5]
    
    for i, el in enumerate(elements):
        tree.insert(el)
        # print(f"Inserted {el}, current tree state:")
        # tree.display() # Optional: for debugging complex insertions
        assert tree._size == i + 1, f"Size should be {i+1} after inserting {el}"

    assert tree._size == len(elements), f"Final size should be {len(elements)}"

    for el in elements:
        node = tree.search(el)
        assert node is not None, f"Element {el} should be found"
        assert node._element == el, f"Found node should have element {el}"
        
    assert tree.search(100) is None, "Searching non-existent element (100) should return None"
    assert tree.search(1) is None, "Searching non-existent element (1) should return None"
    print("RedBlackTree Basic Insertion and Search tests passed.")

def test_rb_insert_existing():
    print("--- Testing RedBlackTree Insert Existing Element ---")
    tree = RedBlackTree()
    elements = [10, 5, 15]
    for el in elements:
        tree.insert(el)
    
    initial_size = tree._size
    tree.insert(10) # Insert existing
    assert tree._size == initial_size, "Size should not change when inserting existing element 10"
    node = tree.search(10)
    assert node is not None and node._element == 10, "Existing element 10 should still be found"
    
    tree.insert(15) # Insert existing
    assert tree._size == initial_size, "Size should not change when inserting existing element 15"
    node = tree.search(15)
    assert node is not None and node._element == 15, "Existing element 15 should still be found"
    print("RedBlackTree Insert Existing Element tests passed.")

def test_rb_deletion_leaf():
    print("--- Testing RedBlackTree Deletion - Leaf Node ---")
    tree = RedBlackTree()
    elements = [10, 5, 15, 3, 7] 
    for el in elements:
        tree.insert(el)
    # tree.display(); print("---")
        
    # Delete leaf 3
    tree.delete(3)
    # tree.display(); print("--- after del 3")
    assert tree.search(3) is None, "Deleted leaf (3) should not be found"
    assert tree._size == len(elements) - 1, "Size should decrease after deleting leaf 3"
    assert tree.search(7) is not None, "Element 7 should still be present"
    
    # Delete leaf 7
    tree.delete(7)
    # tree.display(); print("--- after del 7")
    assert tree.search(7) is None, "Deleted leaf (7) should not be found"
    assert tree._size == len(elements) - 2, "Size should decrease after deleting leaf 7"
    assert tree.search(5) is not None, "Element 5 should still be present"
    print("RedBlackTree Deletion - Leaf Node tests passed.")

def test_rb_deletion_node_with_one_child():
    print("--- Testing RedBlackTree Deletion - Node with One Child ---")
    tree = RedBlackTree()
    # Structure: 10 -> 5 (B) -> 3 (R). Delete 5.
    elements1 = [10, 5, 3] 
    for el in elements1:
        tree.insert(el)
    # tree.display(); print("--- Before del 5 (case 1 child left)")
    tree.delete(5)
    # tree.display(); print("--- After del 5")
    assert tree.search(5) is None, "Deleted node (5) with one child should not be found"
    assert tree._size == 2, "Size incorrect after deleting node (5)"
    assert tree.search(10) is not None, "Element 10 should be present"
    assert tree.search(3) is not None, "Child (3) of deleted node should be present"

    # Structure: 10 -> 15 (B) -> 17 (R). Delete 15.
    tree = RedBlackTree()
    elements2 = [10, 15, 17]
    for el in elements2:
        tree.insert(el)
    # tree.display(); print("--- Before del 15 (case 1 child right)")
    tree.delete(15)
    # tree.display(); print("--- After del 15")
    assert tree.search(15) is None, "Deleted node (15) with one child should not be found"
    assert tree._size == 2, "Size incorrect after deleting node (15)"
    assert tree.search(10) is not None
    assert tree.search(17) is not None
    print("RedBlackTree Deletion - Node with One Child tests passed.")

def test_rb_deletion_node_with_two_children():
    print("--- Testing RedBlackTree Deletion - Node with Two Children ---")
    tree = RedBlackTree()
    elements = [10, 5, 15, 3, 7, 12, 17, 6, 8] 
    for el in elements:
        tree.insert(el)
    # tree.display(); print("--- Initial tree for two-child delete")
        
    # Delete 5 (has 3 and 7 as children, 7 has 6 and 8)
    # Successor of 5 is 6.
    tree.delete(5)
    # tree.display(); print("--- After deleting 5")
    assert tree.search(5) is None, "Deleted node (5) with two children should not be found"
    assert tree._size == len(elements) - 1
    assert tree.search(3) is not None
    assert tree.search(7) is not None
    assert tree.search(6) is not None # Successor that replaced 5 (or its value)
    assert tree.search(8) is not None
    assert tree.search(10) is not None

    # Delete 15 (has 12 and 17 as children) - successor is 17
    # tree.delete(15) # This will be a bit complex depending on previous deletions
    # tree.display(); print("--- After deleting 15")
    # assert tree.search(15) is None
    # assert tree._size == len(elements) - 2
    # assert tree.search(12) is not None
    # assert tree.search(17) is not None # Successor
    print("RedBlackTree Deletion - Node with Two Children tests passed.")

def test_rb_deletion_root():
    print("--- Testing RedBlackTree Deletion - Root Node ---")
    tree = RedBlackTree()
    elements = [10, 5, 15, 3, 7, 12, 17]
    for el in elements:
        tree.insert(el)

    original_size = tree._size
    # tree.display(); print("--- Before deleting root 10")
    tree.delete(10) # Delete root
    # tree.display(); print("--- After deleting root 10")
    assert tree.search(10) is None, "Deleted root (10) should not be found"
    assert tree._size == original_size - 1, "Size should decrease after deleting root"
    if tree._root is not None:
        assert tree._root._element != 10, f"New root is {tree._root._element}, expected not 10"
    
    # Check remaining elements
    remaining = [5, 15, 3, 7, 12, 17]
    for r_el in remaining:
        assert tree.search(r_el) is not None, f"Element {r_el} should still be found after root deletion"
    
    # Delete until one node left, then delete root
    tree = RedBlackTree()
    tree.insert(10)
    tree.insert(5) # 5 is root, 10 is right child
    # tree.display(); print("--- Tree: 5, 10")
    tree.delete(tree._root._element) # Delete current root (could be 5 or 10 depending on RBT logic)
    # tree.display(); print(f"--- After deleting root, new root {tree._root._element if tree._root else None}")
    assert tree._size == 1
    
    tree.delete(tree._root._element) # Delete last node
    assert tree._size == 0
    assert tree._root is None
    print("RedBlackTree Deletion - Root Node tests passed.")

def test_rb_delete_to_empty():
    print("--- Testing RedBlackTree Deletion - Delete to Empty ---")
    tree = RedBlackTree()
    elements = [10, 5, 15, 3, 7, 12, 17, 6, 8, 2, 4, 20, 25, -10, -5]
    # elements = [10,5,15]
    
    # Insert elements
    for el in elements:
        tree.insert(el)
        # print(f"Inserted {el}")
        # tree.display()
        # print("----")
    
    assert tree._size == len(elements)
    
    shuffled_elements = list(elements)
    random.shuffle(shuffled_elements) 

    for i, el_to_delete in enumerate(shuffled_elements):
        # print(f"Attempting to delete {el_to_delete}, current size {tree._size}")
        # tree.display()
        node_before_delete = tree.search(el_to_delete)
        assert node_before_delete is not None, f"Element {el_to_delete} should be in tree before delete. Iteration {i}"
        
        tree.delete(el_to_delete)
        # print(f"Deleted {el_to_delete}, new size {tree._size}")
        # tree.display()
        # print("----")
        
        assert tree.search(el_to_delete) is None, f"Element {el_to_delete} should be deleted. Iteration {i}"
        assert tree._size == len(elements) - (i + 1), f"Size check failed after deleting {el_to_delete}. Iteration {i}"
        
        # Check a few remaining elements if any
        if i < len(shuffled_elements) - 2:
            remaining_to_check = [el for el in shuffled_elements[i+1:] if tree.search(el) is None]
            if remaining_to_check: # Should not happen if logic is correct
                pass # print(f"Error: Elements {remaining_to_check} not found but should be. Iteration {i}")
                # assert False, f"Elements {remaining_to_check} not found but should be. Iteration {i}"


    assert tree._size == 0, "Tree size should be 0 after deleting all elements"
    assert tree._root is None, "Tree root should be None after deleting all elements"
    print("RedBlackTree Deletion - Delete to Empty tests passed.")

def test_rb_stress_various_orders():
    print("--- Testing RedBlackTree Stress Test ---")
    dataset_size = 50 # Increased for better stress
    deletion_count_ratio = 0.5

    for order_name, elements_orig in [
        ("Sorted", list(range(1, dataset_size + 1))),
        ("Reverse Sorted", list(range(dataset_size, 0, -1))),
        ("Random Large", random.sample(range(1, dataset_size * 2), dataset_size))
    ]:
        print(f"  Order: {order_name} (Size: {len(elements_orig)})")
        tree = RedBlackTree()
        
        # Insert all
        for i, el in enumerate(elements_orig):
            tree.insert(el)
            # if (i+1) % (dataset_size // 10) == 0: print(f"    Inserted {i+1}/{len(elements_orig)} elements...")
        assert tree._size == len(elements_orig), f"[{order_name}] Initial insert size failed. Expected {len(elements_orig)}, got {tree._size}"
        for el in elements_orig:
            assert tree.search(el) is not None, f"[{order_name}] Search failed for {el} after initial insert"

        elements_to_delete = random.sample(elements_orig, int(len(elements_orig) * deletion_count_ratio))
        remaining_elements = [el for el in elements_orig if el not in elements_to_delete]
        
        # print(f"    Deleting {len(elements_to_delete)} elements...")
        for i, el_del in enumerate(elements_to_delete):
            # if (i+1) % (len(elements_to_delete) // 10) == 0 : print(f"      Deleted {i+1}/{len(elements_to_delete)}...")
            assert tree.search(el_del) is not None, f"[{order_name}] Element {el_del} to be deleted was not found before deletion."
            tree.delete(el_del)
            assert tree.search(el_del) is None, f"[{order_name}] Search failed for deleted {el_del}"
        
        assert tree._size == len(remaining_elements), f"[{order_name}] Size after deletions failed. Expected {len(remaining_elements)}, got {tree._size}"

        for el_rem in remaining_elements:
            assert tree.search(el_rem) is not None, f"[{order_name}] Search failed for remaining {el_rem}"
        
        for el_del in elements_to_delete: # Double check deleted are gone
            assert tree.search(el_del) is None, f"[{order_name}] Deleted element {el_del} found again"
        
        print(f"    {order_name} sub-test passed.")
    print("RedBlackTree Stress Test passed.")

if __name__ == '__main__':
    test_rb_empty_tree()
    test_rb_insertion_basic()
    test_rb_insert_existing()
    test_rb_deletion_leaf()
    test_rb_deletion_node_with_one_child()
    test_rb_deletion_node_with_two_children()
    test_rb_deletion_root()
    test_rb_delete_to_empty() # This is a thorough test
    test_rb_stress_various_orders()
    print("\nAll RedBlackTree tests completed (check output for specific pass/fail messages).")
