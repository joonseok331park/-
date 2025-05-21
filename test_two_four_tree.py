import random
from two_four_tree_skeleton import TwoFourTree # Assuming file is in the same directory or PYTHONPATH

def test_24_empty_tree():
    print("--- Testing TwoFourTree Empty Tree ---")
    tree = TwoFourTree()
    assert tree._size == 0, "Empty tree size should be 0"
    assert tree._root is None, "Empty tree root should be None"
    assert tree.search(10) is None, "Search on empty tree should return None"
    tree.delete(10) # Should not error
    assert tree._size == 0, "Size after delete on empty tree should be 0"
    print("TwoFourTree Empty Tree tests passed.")

def test_24_insertion_basic():
    print("--- Testing TwoFourTree Basic Insertion and Search ---")
    tree = TwoFourTree()
    # Elements chosen to trigger some splits potentially
    elements = [10, 20, 5, 15, 25, 3, 7, 12, 17, 22, 27, 1, 4, 6, 8] 
    
    for i, el in enumerate(elements):
        tree.insert(el)
        # print(f"Inserted {el}, current tree:")
        # tree.display() # Optional for debugging
        assert tree._size == i + 1, f"Size should be {i+1} after inserting {el}"

    assert tree._size == len(elements), f"Final size should be {len(elements)}"

    for el in elements:
        search_result = tree.search(el)
        assert search_result is not None, f"Element {el} should be found"
        node, key_idx = search_result
        assert node._keys[key_idx] == el, f"Found node should have element {el} at index {key_idx}"
        
    assert tree.search(100) is None, "Searching non-existent element (100) should return None"
    assert tree.search(0) is None, "Searching non-existent element (0) should return None"
    print("TwoFourTree Basic Insertion and Search tests passed.")

def test_24_insert_existing():
    print("--- Testing TwoFourTree Insert Existing Element ---")
    tree = TwoFourTree()
    elements = [10, 5, 15, 20, 30]
    for el in elements:
        tree.insert(el)
    
    initial_size = tree._size
    tree.insert(10) # Insert existing
    assert tree._size == initial_size, "Size should not change when inserting existing element 10"
    res_10 = tree.search(10)
    assert res_10 is not None and res_10[0]._keys[res_10[1]] == 10, "Existing element 10 should still be found"
    
    tree.insert(30) # Insert existing
    assert tree._size == initial_size, "Size should not change when inserting existing element 30"
    res_30 = tree.search(30)
    assert res_30 is not None and res_30[0]._keys[res_30[1]] == 30, "Existing element 30 should still be found"
    print("TwoFourTree Insert Existing Element tests passed.")

def test_24_deletion_simple_cases(): # Covers leaf and some internal without major underflow
    print("--- Testing TwoFourTree Deletion - Simple Cases (Leaf/Internal no major underflow) ---")
    tree = TwoFourTree()
    # Build a relatively balanced tree first
    base_elements = [50, 25, 75, 10, 30, 60, 80, 5, 15, 28, 40, 55, 65, 78, 90]
    for el in base_elements:
        tree.insert(el)
    
    initial_size = tree._size
    # tree.display(); print("--- Initial for simple delete ---")

    # Delete a leaf (e.g., 5)
    tree.delete(5)
    # tree.display(); print("--- After del 5 ---")
    assert tree.search(5) is None, "Deleted leaf (5) should not be found"
    assert tree._size == initial_size - 1, "Size error after deleting leaf 5"
    assert tree.search(10) is not None, "Element 10 should still be present"

    # Delete an internal node's key that might be replaced by successor/predecessor from a leaf
    # e.g., delete 10 (successor 15 from leaf)
    tree.delete(10)
    # tree.display(); print("--- After del 10 ---")
    assert tree.search(10) is None, "Deleted internal (10) should not be found"
    assert tree._size == initial_size - 2, "Size error after deleting internal 10"
    assert tree.search(15) is not None, "Successor (15) should be present"
    assert tree.search(25) is not None, "Element 25 should still be present"
    
    # Delete another leaf (e.g., 90)
    tree.delete(90)
    # tree.display(); print("--- After del 90 ---")
    assert tree.search(90) is None, "Deleted leaf (90) should not be found"
    assert tree._size == initial_size - 3, "Size error after deleting leaf 90"
    assert tree.search(80) is not None

    print("TwoFourTree Deletion - Simple Cases tests passed.")


def test_24_deletion_triggering_merge_or_redistribution():
    print("--- Testing TwoFourTree Deletion - Triggering Merge/Redistribution ---")
    # This test is harder to set up perfectly without seeing the tree structure
    # We aim to delete elements that would likely cause underflow and restructuring
    tree = TwoFourTree()
    elements = list(range(1, 21)) # 1 to 20
    for el in elements:
        tree.insert(el)
    
    initial_size = tree._size
    # tree.display(); print("--- Initial for merge/redistribute test ---")

    # Deleting elements that are likely to cause nodes to have minimum keys,
    # potentially leading to merge or redistribution.
    # E.g., delete elements from sparse parts of the tree or consecutive elements.
    elements_to_delete = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19] # Delete many small/odd numbers
    
    count_deleted = 0
    for el_del in elements_to_delete:
        if tree.search(el_del) is not None: # Make sure it's there before deleting
            tree.delete(el_del)
            count_deleted += 1
            assert tree.search(el_del) is None, f"Deleted element {el_del} should not be found"
            # tree.display(); print(f"--- After del {el_del} ---")
        else:
            print(f"Warning: Element {el_del} not found before attempted deletion in merge test.")

    assert tree._size == initial_size - count_deleted, "Size error after deletions in merge/redistribute test"
    
    # Check some remaining elements
    remaining_elements = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
    for el_rem in remaining_elements:
        assert tree.search(el_rem) is not None, f"Remaining element {el_rem} not found"

    print("TwoFourTree Deletion - Triggering Merge/Redistribution tests passed (verify by absence of errors).")


def test_24_deletion_root():
    print("--- Testing TwoFourTree Deletion - Root ---")
    tree = TwoFourTree()
    elements = [10, 5, 15, 3, 7, 12, 17] # A small tree
    for el in elements:
        tree.insert(el)
    initial_size = tree._size
    
    # tree.display(); print("--- Before deleting root ---")
    # Find current root's first key to delete
    if tree._root and tree._root._keys:
        root_key_to_delete = tree._root._keys[0]
        tree.delete(root_key_to_delete)
        # tree.display(); print(f"--- After deleting root key {root_key_to_delete} ---")
        assert tree.search(root_key_to_delete) is None, f"Deleted root key {root_key_to_delete} should not be found"
        assert tree._size == initial_size - 1, "Size error after deleting a root key"
        if tree._root and tree._root._keys: # If tree not empty
             assert root_key_to_delete not in tree._root._keys, "Old root key should not be in new root's keys"
    else:
        print("Skipping root deletion as root is empty or None initially in test_24_deletion_root setup.")

    # Delete until one node left, then delete its key(s)
    tree = TwoFourTree()
    tree.insert(10)
    tree.insert(5) # e.g. root [5,10] or [5] then child [10] etc.
    tree.insert(15) # Root might be [10] with children [5] and [15] or [5,10,15]
    
    # tree.display(); print(f"--- Tree before deleting all from root test ---")
    if tree.search(10): tree.delete(10)
    if tree.search(5): tree.delete(5)
    if tree.search(15): tree.delete(15)
    
    assert tree._size == 0
    assert tree._root is None or not tree._root._keys # Root might be an empty node before becoming None
    if tree._root is None and tree._size !=0 : # if root becomes None, size must be 0
        assert tree._size == 0 

    print("TwoFourTree Deletion - Root tests passed.")


def test_24_delete_to_empty():
    print("--- Testing TwoFourTree Deletion - Delete to Empty ---")
    tree = TwoFourTree()
    elements = [10, 5, 15, 3, 7, 12, 17, 6, 8, 2, 4, 1, 20, 30, 40, 50]
    
    for el in elements:
        tree.insert(el)
    
    assert tree._size == len(elements)
    
    shuffled_elements = list(elements)
    random.shuffle(shuffled_elements) 

    for i, el_to_delete in enumerate(shuffled_elements):
        # print(f"Deleting {el_to_delete} ({i+1}/{len(shuffled_elements)}), current size {tree._size}")
        # tree.display()
        if tree.search(el_to_delete) is not None: # Check if actually present
            tree.delete(el_to_delete)
            assert tree.search(el_to_delete) is None, f"Element {el_to_delete} should be deleted. Iteration {i}"
            # Size check is tricky if delete wasn't guaranteed (e.g. if element wasn't found)
            # The current logic relies on tree.search being accurate.
            # The size check below assumes element was indeed found and deleted.
            assert tree._size == len(elements) - (i + 1), f"Size check failed after deleting {el_to_delete}. Iteration {i}"
        else:
            # This implies element was already removed or test logic error
            print(f"Warning: Element {el_to_delete} not found before planned deletion in delete_to_empty. Iteration {i}")
            # Adjust expected size if element was not there to be deleted
            elements = [e for e in elements if e != el_to_delete] # Effectively reduce original set for next size checks

    # Final check after attempting to delete all unique original elements
    assert tree._size == 0, f"Tree size should be 0. Got {tree._size}"
    assert tree._root is None or (not tree._root._keys and not tree._root._children), "Tree root problematic after all deletions"
    print("TwoFourTree Deletion - Delete to Empty tests passed.")

def test_24_stress_various_orders():
    print("--- Testing TwoFourTree Stress Test ---")
    dataset_size = 50 
    deletion_count_ratio = 0.5

    for order_name, elements_orig_list in [
        ("Sorted", list(range(1, dataset_size + 1))),
        ("Reverse Sorted", list(range(dataset_size, 0, -1))),
        ("Random", random.sample(range(1, dataset_size * 2), dataset_size))
    ]:
        print(f"  Order: {order_name} (Size: {len(elements_orig_list)})")
        tree = TwoFourTree()
        
        for el in elements_orig_list:
            tree.insert(el)
        assert tree._size == len(elements_orig_list), f"[{order_name}] Initial insert size failed."
        
        for el in elements_orig_list: # Verify all inserted elements are searchable
            assert tree.search(el) is not None, f"[{order_name}] Search failed for {el} after initial insert"

        elements_to_delete = random.sample(elements_orig_list, int(len(elements_orig_list) * deletion_count_ratio))
        remaining_elements = [el for el in elements_orig_list if el not in elements_to_delete]
        
        deleted_count_in_test = 0
        for el_del in elements_to_delete:
            if tree.search(el_del) is not None: # Ensure it's there
                tree.delete(el_del)
                deleted_count_in_test+=1
            assert tree.search(el_del) is None, f"[{order_name}] Search found deleted {el_del}"
        
        assert tree._size == len(elements_orig_list) - deleted_count_in_test, f"[{order_name}] Size after deletions failed."

        for el_rem in remaining_elements:
            assert tree.search(el_rem) is not None, f"[{order_name}] Search failed for remaining {el_rem}"
        
        print(f"    {order_name} sub-test passed.")
    print("TwoFourTree Stress Test passed.")

if __name__ == '__main__':
    test_24_empty_tree()
    test_24_insertion_basic()
    test_24_insert_existing()
    test_24_deletion_simple_cases()
    test_24_deletion_triggering_merge_or_redistribution()
    test_24_deletion_root()
    test_24_delete_to_empty()
    test_24_stress_various_orders()
    print("\nAll TwoFourTree tests completed (check output for specific pass/fail messages).")
