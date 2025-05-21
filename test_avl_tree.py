import random
from avl_tree_skeleton import AVLTree # Assuming avl_tree_skeleton.py is in the same directory or PYTHONPATH

def test_avl_empty_tree():
    print("--- Testing AVL Empty Tree ---")
    tree = AVLTree()
    assert tree._size == 0, "Empty tree size should be 0"
    assert tree._root is None, "Empty tree root should be None"
    assert tree.search(10) is None, "Search on empty tree should return None"
    tree.delete(10) # Should not error
    assert tree._size == 0, "Size after delete on empty tree should be 0"
    print("AVL Empty Tree tests passed.")

def test_avl_insertion_basic():
    print("--- Testing AVL Basic Insertion and Search ---")
    tree = AVLTree()
    elements = [10, 5, 15, 3, 7, 12, 17, 6]
    
    for i, el in enumerate(elements):
        tree.insert(el)
        assert tree._size == i + 1, f"Size should be {i+1} after inserting {el}"

    assert tree._size == len(elements), f"Final size should be {len(elements)}"

    for el in elements:
        node = tree.search(el)
        assert node is not None, f"Element {el} should be found"
        assert node._element == el, f"Found node should have element {el}"
        
    assert tree.search(100) is None, "Searching non-existent element (100) should return None"
    assert tree.search(1) is None, "Searching non-existent element (1) should return None"
    print("AVL Basic Insertion and Search tests passed.")

def test_avl_insert_existing():
    print("--- Testing AVL Insert Existing Element ---")
    tree = AVLTree()
    elements = [10, 5, 15]
    for el in elements:
        tree.insert(el)
    
    initial_size = tree._size
    tree.insert(10) # Insert existing
    assert tree._size == initial_size, "Size should not change when inserting existing element"
    node = tree.search(10)
    assert node is not None and node._element == 10, "Existing element 10 should still be found"
    
    tree.insert(5) # Insert existing
    assert tree._size == initial_size, "Size should not change when inserting existing element 5"
    node = tree.search(5)
    assert node is not None and node._element == 5, "Existing element 5 should still be found"
    print("AVL Insert Existing Element tests passed.")

def test_avl_deletion_leaf():
    print("--- Testing AVL Deletion - Leaf Node ---")
    tree = AVLTree()
    elements = [10, 5, 15, 3]
    for el in elements:
        tree.insert(el) # 3 is a leaf
        
    tree.delete(3)
    assert tree.search(3) is None, "Deleted leaf (3) should not be found"
    assert tree._size == len(elements) - 1, "Size should decrease after deleting leaf"
    assert tree.search(10) is not None, "Element 10 should still be present"
    assert tree.search(5) is not None, "Element 5 should still be present"
    print("AVL Deletion - Leaf Node tests passed.")

def test_avl_deletion_node_with_one_child():
    print("--- Testing AVL Deletion - Node with One Child ---")
    tree = AVLTree()
    # Structure: 10 -> 5 -> 3. Delete 5.
    elements1 = [10, 5, 3] 
    for el in elements1:
        tree.insert(el)
    tree.delete(5)
    assert tree.search(5) is None, "Deleted node (5) with one child should not be found"
    assert tree._size == 2, "Size incorrect after deleting node (5)"
    assert tree.search(10) is not None, "Element 10 should be present"
    assert tree.search(3) is not None, "Child (3) of deleted node should be present"

    # Structure: 10 -> 15 -> 17. Delete 15.
    tree = AVLTree()
    elements2 = [10, 15, 17]
    for el in elements2:
        tree.insert(el)
    tree.delete(15)
    assert tree.search(15) is None, "Deleted node (15) with one child should not be found"
    assert tree._size == 2, "Size incorrect after deleting node (15)"
    assert tree.search(10) is not None
    assert tree.search(17) is not None
    print("AVL Deletion - Node with One Child tests passed.")

def test_avl_deletion_node_with_two_children():
    print("--- Testing AVL Deletion - Node with Two Children ---")
    tree = AVLTree()
    elements = [10, 5, 15, 3, 7, 12, 17] # Delete 5 (has 3 and 7 as children)
    for el in elements:
        tree.insert(el)
        
    tree.delete(5)
    assert tree.search(5) is None, "Deleted node (5) with two children should not be found"
    assert tree._size == len(elements) - 1
    assert tree.search(3) is not None
    assert tree.search(7) is not None
    assert tree.search(10) is not None

    # Delete 15 (has 12 and 17 as children)
    tree.delete(15)
    assert tree.search(15) is None
    assert tree._size == len(elements) - 2
    assert tree.search(12) is not None
    assert tree.search(17) is not None
    print("AVL Deletion - Node with Two Children tests passed.")

def test_avl_deletion_root():
    print("--- Testing AVL Deletion - Root Node ---")
    tree = AVLTree()
    elements = [10, 5, 15, 3, 7, 12, 17]
    for el in elements:
        tree.insert(el)

    # Delete root (10)
    original_size = tree._size
    tree.delete(10)
    assert tree.search(10) is None, "Deleted root (10) should not be found"
    assert tree._size == original_size - 1, "Size should decrease after deleting root"
    if tree._root is not None: # New root should not be 10
        assert tree._root._element != 10, f"New root is {tree._root._element}, expected not 10"
    assert tree.search(5) is not None
    assert tree.search(15) is not None
    assert tree.search(3) is not None
    
    # Delete until one node left, then delete root
    tree = AVLTree()
    tree.insert(10)
    tree.insert(5)
    tree.delete(10) # Delete root (10), 5 becomes root
    assert tree._size == 1
    assert tree._root is not None and tree._root._element == 5
    tree.delete(5) # Delete last node (root)
    assert tree._size == 0
    assert tree._root is None
    print("AVL Deletion - Root Node tests passed.")

def test_avl_delete_to_empty():
    print("--- Testing AVL Deletion - Delete to Empty ---")
    tree = AVLTree()
    elements = [10, 5, 15, 3, 7, 12, 17, 6, 8, 2, 4]
    random.shuffle(elements) # Delete in random order
    
    for el in elements:
        tree.insert(el)
    
    assert tree._size == len(elements)

    for i, el in enumerate(elements):
        tree.delete(el)
        assert tree.search(el) is None, f"Element {el} should be deleted"
        assert tree._size == len(elements) - (i + 1), f"Size check failed after deleting {el}"
        # Check a few remaining elements if any
        if i < len(elements) - 2:
            assert tree.search(elements[i+1]) is not None, f"Remaining element {elements[i+1]} not found"


    assert tree._size == 0, "Tree size should be 0 after deleting all elements"
    assert tree._root is None, "Tree root should be None after deleting all elements"
    print("AVL Deletion - Delete to Empty tests passed.")

def test_avl_stress_various_orders():
    print("--- Testing AVL Stress Test ---")
    for order_name, elements in [
        ("Sorted", list(range(1, 31))),
        ("Reverse Sorted", list(range(30, 0, -1))),
        ("Random Small", random.sample(range(1, 101), 30))
    ]:
        print(f"  Order: {order_name}")
        tree = AVLTree()
        for el in elements:
            tree.insert(el)
        assert tree._size == len(elements), f"[{order_name}] Initial insert size failed"
        for el in elements:
            assert tree.search(el) is not None, f"[{order_name}] Search failed for {el} after initial insert"

        elements_to_delete = random.sample(elements, len(elements) // 2)
        remaining_elements = [el for el in elements if el not in elements_to_delete]

        for el_del in elements_to_delete:
            tree.delete(el_del)
            assert tree.search(el_del) is None, f"[{order_name}] Search failed for deleted {el_del}"
        
        assert tree._size == len(remaining_elements), f"[{order_name}] Size after deletions failed"

        for el_rem in remaining_elements:
            assert tree.search(el_rem) is not None, f"[{order_name}] Search failed for remaining {el_rem}"
        
        for el_del in elements_to_delete: # Double check deleted are gone
            assert tree.search(el_del) is None, f"[{order_name}] Deleted element {el_del} found again"

    print("AVL Stress Test passed.")

if __name__ == '__main__':
    test_avl_empty_tree()
    test_avl_insertion_basic()
    test_avl_insert_existing()
    test_avl_deletion_leaf()
    test_avl_deletion_node_with_one_child()
    test_avl_deletion_node_with_two_children()
    test_avl_deletion_root()
    test_avl_delete_to_empty()
    test_avl_stress_various_orders()
    print("\nAll AVL tests completed (check output for specific pass/fail messages).")
