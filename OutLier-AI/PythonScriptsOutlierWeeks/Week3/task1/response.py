class Node:
    def __init__(self, value):
        self.value = value
        self.children = []

def add_child(parent, child):
    parent.children.append(child)

def search_graph(node, target, path):
    # Add the current node to the path
    path.append(node.value)
    
    # Check if the current node is the target
    if node.value == target:
        return path
    
    # Recursively search in children
    for child in node.children:
        result = search_graph(child, target, path)
        if result:  # If found in the child, return the path
            return result
    
    # If not found, remove the current node from the path
    path.pop()
    return None

def main():
    # Construct the graph based on the provided structure
    root = Node("Data Structures")
    
    linear = Node("Linear")
    non_linear = Node("Non-Linear")
    
    root.children.extend([linear, non_linear])
    
    # Linear data structures
    direct_access = Node("Direct Access")
    sequential_access = Node("Sequential Access")
    
    linear.children.extend([direct_access, sequential_access])
    
    # Direct Access types
    homogeneous = Node("Homogeneous")
    heterogeneous = Node("Heterogeneous")
    
    direct_access.children.extend([homogeneous, heterogeneous])
    
    # Homogeneous and Heterogeneous types
    array = Node("Array")
    record = Node("Record")
    
    homogeneous.children.append(array)
    heterogeneous.children.append(record)
    
    # Sequential Access types
    general = Node("General")
    lifo = Node("LIFO")
    fifo = Node("FIFO")
    
    sequential_access.children.extend([general, lifo, fifo])
    
    # General types
    list_node = Node("List")
    stack = Node("Stack")
    queue = Node("Queue")
    
    general.children.extend([list_node, stack, queue])
    
    # Non-Linear data structures
    sets = Node("Sets")
    trees = Node("Trees")
    tables = Node("Tables (Maps)")
    graphs = Node("Graphs")
    
    non_linear.children.extend([sets, trees, tables, graphs])
    
    # User input for search
    target = input("Enter the element to search for: ")
    
    # Search for the element
    path = []
    result = search_graph(root, target, path)
    
    if result:
        print("Path from root to the element:", " -> ".join(result))
    else:
        print("Not Found")

if __name__ == "__main__":
    main()