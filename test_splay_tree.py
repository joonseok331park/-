import random
from splay_tree_skeleton import SplayTree # Assuming file is in the same directory or PYTHONPATH

def test_splay_empty_tree():
    print("--- Testing SplayTree Empty Tree ---")
    tree = SplayTree()
    assert tree._size == 0, "Empty tree size should be 0"
    assert tree._root is None, "Empty tree root should be None"
    
    # Search on empty tree
    res_node = tree.search(10)
    assert res_node is None, "Search on empty tree should return None"
    assert tree._root is None, "Root should still be None after search on empty tree"
    
    tree.delete(10) # Should not error
    assert tree._size == 0, "Size after delete on empty tree should be 0"
    assert tree._root is None, "Root after delete on empty tree should be None"
    print("SplayTree Empty Tree tests passed.")

def test_splay_insertion_basic_and_splay_on_insert_search():
    print("--- Testing SplayTree Basic Insertion, Splay on Insert/Search ---")
    tree = SplayTree()
    elements = [10, 5, 15, 3, 7, 12, 17, 6]
    
    for i, el in enumerate(elements):
        tree.insert(el)
        assert tree._size == i + 1, f"Size should be {i+1} after inserting {el}"
        assert tree._root is not None, f"Root should not be None after inserting {el}"
        assert tree._root._element == el, f"Root should be {el} after inserting {el}"

    assert tree._size == len(elements), f"Final size should be {len(elements)}"

    # Test search and splay on search
    search_order = random.sample(elements, len(elements))
    for el in search_order:
        node = tree.search(el)
        assert node is not None, f"Element {el} should be found"
        assert node._element == el, f"Found node should have element {el}"
        assert tree._root is not None, f"Root should not be None after searching {el}"
        assert tree._root._element == el, f"Root should be {el} after searching for {el}"
        
    # Search for non-existent element
    tree.search(100) # Should splay the closest leaf (17 in this case if elements are as above)
    assert tree._root is not None, "Root should not be None after searching non-existent"
    # The actual root after searching non-existent depends on the last accessed node. 
    # For [10, 5, 15, 3, 7, 12, 17, 6], searching 100 likely splays 17.
    # For simplicity, we just check it's not None. More specific check is hard without knowing exact last path.
    
    tree.search(1) # Should splay 3 (if 3 is a leaf after previous ops)
    assert tree._root is not None
    print("SplayTree Basic Insertion and Splay on Insert/Search tests passed.")

def test_splay_insert_existing():
    print("--- Testing SplayTree Insert Existing Element ---")
    tree = SplayTree()
    elements = [10, 5, 15]
    for el in elements:
        tree.insert(el) # Root becomes el
    
    initial_size = tree._size
    tree.insert(10) # Insert existing 10
    assert tree._size == initial_size, "Size should not change when inserting existing element 10"
    assert tree._root is not None and tree._root._element == 10, "Root should be 10 after inserting existing 10"
    
    tree.insert(5) # Insert existing 5
    assert tree._size == initial_size, "Size should not change when inserting existing element 5"
    assert tree._root is not None and tree._root._element == 5, "Root should be 5 after inserting existing 5"
    print("SplayTree Insert Existing Element tests passed.")

def test_splay_deletion():
    print("--- Testing SplayTree Deletion ---")
    tree = SplayTree()
    elements = [10, 5, 15, 3, 7, 12, 17, 6, 8]
    for el in elements:
        tree.insert(el)
    
    # tree.display(); print("Initial for delete")

    # Delete 3 (a leaf after splaying it or its parent)
    tree.delete(3)
    # tree.display(); print(f"After del 3, root: {tree._root._element if tree._root else None}")
    assert tree.search(3) is None, "Deleted element 3 should not be found (search will splay parent)"
    if tree._root : assert tree._root._element != 3, "Root should not be 3 after deleting 3"
    assert tree._size == len(elements) - 1, "Size error after deleting 3"

    # Delete 7 (internal node, requires splay, then join)
    tree.delete(7)
    # tree.display(); print(f"After del 7, root: {tree._root._element if tree._root else None}")
    assert tree.search(7) is None
    if tree._root : assert tree._root._element != 7, "Root should not be 7 after deleting 7"
    assert tree._size == len(elements) - 2

    # Delete 10 (original root, likely not root anymore before this delete)
    tree.delete(10)
    # tree.display(); print(f"After del 10, root: {tree._root._element if tree._root else None}")
    assert tree.search(10) is None
    if tree._root : assert tree._root._element != 10, "Root should not be 10 after deleting 10"
    assert tree._size == len(elements) - 3
    
    # Check some remaining elements
    assert tree.search(5) is not None
    assert tree._root._element == 5 # Splayed 5
    assert tree.search(15) is not None
    assert tree._root._element == 15 # Splayed 15

    print("SplayTree Deletion tests passed.")


def test_splay_delete_to_empty():
    print("--- Testing SplayTree Deletion - Delete to Empty ---")
    tree = SplayTree()
    elements = [10, 5, 15, 3, 7, 12, 17, 6, 8, 2, 4]
    # elements = [3,2,1] # Simpler case for debugging
    
    for el in elements:
        tree.insert(el)
    
    assert tree._size == len(elements)
    
    shuffled_elements = list(elements)
    random.shuffle(shuffled_elements) 

    for i, el_to_delete in enumerate(shuffled_elements):
        # print(f"Deleting {el_to_delete} (iteration {i+1}/{len(shuffled_elements)}), current size {tree._size}")
        # tree.display()
        
        # Search first to ensure it's there and splay it (or its parent if not found)
        # This is consistent with how delete works (splay, then operate)
        tree.search(el_to_delete) 
        if tree._root and tree._root._element == el_to_delete: # Check if it was actually found
            tree.delete(el_to_delete)
            assert tree.search(el_to_delete) is None, f"Element {el_to_delete} should be deleted. Iteration {i}"
            # After search(el_to_delete) is None, root will be parent of where el_to_delete was.
            assert tree._size == len(elements) - (i + 1), f"Size check failed after deleting {el_to_delete}. Iteration {i}"
        else:
            # This case should ideally not happen if elements contains unique items and they were all inserted.
            # It means search didn't bring the element to root, so it wasn't found.
            # This can happen if the element was already deleted in a previous iteration if elements had duplicates,
            # but the test uses a shuffled list of unique elements.
            # Or, if the search itself has an issue not splaying correctly.
            # print(f"Warning: Element {el_to_delete} not found at root before planned deletion. Current root: {tree._root._element if tree._root else 'None'}")
            # This means the element was already deleted due to a flaw in test logic or prior deletion
            # For now, we assume this means it's already considered "deleted" for this pass.
            # This part of the test needs careful thought if elements can be re-deleted.
            # The current loop deletes each element from `shuffled_elements` once.
            pass


    # Recalculate expected size based on unique elements successfully deleted
    # This is tricky because the assertion for size is inside the loop.
    # The final check is most important.
    final_expected_size = 0 # All unique elements should be deleted
    assert tree._size == final_expected_size, f"Tree size should be {final_expected_size} after deleting all. Got {tree._size}"
    if final_expected_size == 0:
        assert tree._root is None, "Tree root should be None after deleting all elements"
    print("SplayTree Deletion - Delete to Empty tests passed.")

def test_splay_stress_various_orders():
    print("--- Testing SplayTree Stress Test ---")
    dataset_size = 30 
    deletion_count_ratio = 0.5

    for order_name, elements_orig_list in [
        ("Sorted", list(range(1, dataset_size + 1))),
        ("Reverse Sorted", list(range(dataset_size, 0, -1))),
        ("Random", random.sample(range(1, dataset_size * 2), dataset_size))
    ]:
        print(f"  Order: {order_name} (Size: {len(elements_orig_list)})")
        tree = SplayTree()
        
        # Insert all
        for el in elements_orig_list:
            tree.insert(el)
            assert tree._root._element == el, f"[{order_name}] Root not {el} after insert"
        assert tree._size == len(elements_orig_list), f"[{order_name}] Initial insert size failed."
        
        # Search all and check splay
        search_check_order = random.sample(elements_orig_list, len(elements_orig_list))
        for el in search_check_order:
            node = tree.search(el)
            assert node is not None, f"[{order_name}] Search failed for {el} after initial insert"
            assert tree._root._element == el, f"[{order_name}] Root not {el} after search"

        elements_to_delete = random.sample(elements_orig_list, int(len(elements_orig_list) * deletion_count_ratio))
        remaining_elements = [el for el in elements_orig_list if el not in elements_to_delete]
        
        for el_del in elements_to_delete:
            tree.delete(el_del) # Splay happens inside delete
            # After delete, root is usually parent of deleted node, or joined subtree root
            # Search for deleted should return None and splay the parent/closest.
            assert tree.search(el_del) is None, f"[{order_name}] Search found deleted {el_del}"
        
        assert tree._size == len(remaining_elements), f"[{order_name}] Size after deletions failed."

        for el_rem in remaining_elements:
            node = tree.search(el_rem)
            assert node is not None, f"[{order_name}] Search failed for remaining {el_rem}"
            assert tree._root._element == el_rem, f"[{order_name}] Root not {el_rem} after searching remaining"
        
        print(f"    {order_name} sub-test passed.")
    print("SplayTree Stress Test passed.")

if __name__ == '__main__':
    test_splay_empty_tree()
    test_splay_insertion_basic_and_splay_on_insert_search()
    test_splay_insert_existing()
    test_splay_deletion()
    test_splay_delete_to_empty()
    test_splay_stress_various_orders()
    print("\nAll SplayTree tests completed (check output for specific pass/fail messages).")
