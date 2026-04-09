import tkinter as tk
from tkinter import ttk, messagebox
import heapq
import networkx as nx
import matplotlib.pyplot as plt

# ---------------------------
# Campus Graph Dataset
# ---------------------------
CAMPUS_GRAPH = {
    'A': {'B': 4, 'C': 2, 'J': 7},
    'B': {'A': 4, 'C': 1, 'D': 5, 'E': 6},
    'C': {'A': 2, 'B': 1, 'D': 8, 'F': 3},
    'D': {'B': 5, 'C': 8, 'E': 2, 'G': 4},
    'E': {'B': 6, 'D': 2, 'F': 5, 'H': 3},
    'F': {'C': 3, 'E': 5, 'G': 2, 'I': 6},
    'G': {'D': 4, 'F': 2, 'H': 5, 'I': 3},
    'H': {'E': 3, 'G': 5, 'I': 4, 'J': 6},
    'I': {'F': 6, 'G': 3, 'H': 4, 'J': 2},
    'J': {'A': 7, 'H': 6, 'I': 2}
}

BASE_FARE = 20  # fare per unit distance

# ---------------------------------------------------
# Dijkstra’s Algorithm (Shortest Path)
# ---------------------------------------------------
def dijkstra(graph, start):
    dist = {node: float('inf') for node in graph}
    prev = {node: None for node in graph}
    dist[start] = 0
    pq = [(0, start)]
    while pq:
        d, node = heapq.heappop(pq)
        if d > dist[node]:
            continue
        for neigh, w in graph[node].items():
            new_d = d + w
            if new_d < dist[neigh]:
                dist[neigh] = new_d
                prev[neigh] = node
                heapq.heappush(pq, (new_d, neigh))
    return dist, prev

def shortest_path(graph, start, end):
    dist, prev = dijkstra(graph, start)
    path, current = [], end
    while current:
        path.append(current)
        current = prev[current]
    path.reverse()
    return dist[end], path

# ---------------------------------------------------
# Prim’s Algorithm (Minimum Spanning Tree)
# ---------------------------------------------------
def prim_mst(graph, start='A'):
    visited, edges, total = set(), [], 0
    pq = [(0, start, None)]
    while pq:
        w, node, parent = heapq.heappop(pq)
        if node in visited:
            continue
        visited.add(node)
        if parent:
            edges.append((parent, node, w))
            total += w
        for neigh, wt in graph[node].items():
            if neigh not in visited:
                heapq.heappush(pq, (wt, neigh, node))
    return total, edges

# ---------------------------------------------------
# Binary Search (case-insensitive)
# ---------------------------------------------------
def binary_search(arr, target):
    target_upper = target.upper()
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        mid_name = arr[mid][0].upper()
        if mid_name == target_upper:
            return arr[mid]
        elif mid_name < target_upper:
            lo = mid + 1
        else:
            hi = mid - 1
    return None

# ---------------------------------------------------
# GUI Functions
# ---------------------------------------------------
def show_optimal_route():
    pickup = pickup_var.get()
    drop = drop_var.get()
    if not pickup or not drop:
        messagebox.showwarning("Input Error", "Please select both pickup and drop locations.")
        return
    dist, path = shortest_path(CAMPUS_GRAPH, pickup, drop)
    fare = dist * BASE_FARE
    result_text.set(f"Optimal Route: {' → '.join(path)}\n"
                    f"Total Distance: {dist} units\n"
                    f"Estimated Fare: ₹{fare}")

# --- 🟢 UPDATED FUNCTION WITH GRAPH VISUALIZATION ---
def show_campus_map():
    total, edges = prim_mst(CAMPUS_GRAPH)

    # Create a graph using NetworkX
    G = nx.Graph()
    for node, neighbors in CAMPUS_GRAPH.items():
        for neigh, weight in neighbors.items():
            G.add_edge(node, neigh, weight=weight)

    pos = nx.spring_layout(G, seed=42)  # layout for visual consistency

    # Draw all edges in light gray
    nx.draw_networkx_edges(G, pos, edge_color='lightgray', width=1.5)

    # Highlight MST edges in a different color
    mst_edges = [(u, v) for u, v, w in edges]
    nx.draw_networkx_edges(G, pos, edgelist=mst_edges, edge_color='green', width=2.5)

    # Draw nodes and labels
    nx.draw_networkx_nodes(G, pos, node_color="#3498db", node_size=800)
    nx.draw_networkx_labels(G, pos, font_color='white', font_size=10, font_weight='bold')

    # Draw edge weights
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=9)

    plt.title(f"Campus Connectivity (MST Highlighted)\nTotal Connection Cost: {total}", fontsize=12)
    plt.axis('off')
    plt.show()

# ---------------------------------------------------
# Search Function
# ---------------------------------------------------
def search_route():
    routes = [
        ('A-J', 15),
        ('A-C', 2),
        ('B-F', 10),
        ('C-I', 12),
        ('D-H', 8)
    ]
    routes.sort(key=lambda x: x[0].upper())
    target = search_var.get().strip()
    if not target:
        messagebox.showwarning("Search Error", "Please enter a route to search.")
        return
    result = binary_search(routes, target)
    if result:
        messagebox.showinfo("Route Found", f"Route: {result[0]}\nDistance: {result[1]} units")
    else:
        available = "\n".join([f"{r[0]} - {r[1]} units" for r in routes])
        messagebox.showinfo("Route Not Found", f"No such route.\nAvailable Routes:\n{available}")

# ---------------------------------------------------
# GUI Setup
# ---------------------------------------------------
root = tk.Tk()
root.title("Campus Shuttle Route Optimizer")
root.geometry("650x400")
root.configure(bg="#f0f4f7")

title_label = tk.Label(root, text="🚍 Campus Shuttle Route Optimizer", 
                       font=("Arial", 18, "bold"), bg="#f0f4f7", fg="#2c3e50")
title_label.pack(pady=10)

frame = tk.Frame(root, bg="#f0f4f7")
frame.pack(pady=10)

tk.Label(frame, text="Pickup Location:", font=("Arial", 12), bg="#f0f4f7").grid(row=0, column=0, padx=10, pady=5)
pickup_var = tk.StringVar()
pickup_combo = ttk.Combobox(frame, textvariable=pickup_var, values=list(CAMPUS_GRAPH.keys()), width=5, state="readonly")
pickup_combo.grid(row=0, column=1, padx=5)

tk.Label(frame, text="Drop Location:", font=("Arial", 12), bg="#f0f4f7").grid(row=0, column=2, padx=10, pady=5)
drop_var = tk.StringVar()
drop_combo = ttk.Combobox(frame, textvariable=drop_var, values=list(CAMPUS_GRAPH.keys()), width=5, state="readonly")
drop_combo.grid(row=0, column=3, padx=5)

# Buttons
button_frame = tk.Frame(root, bg="#f0f4f7")
button_frame.pack(pady=10)

ttk.Button(button_frame, text="Show Optimal Route", command=show_optimal_route).grid(row=0, column=0, padx=10)
ttk.Button(button_frame, text="View Campus Map (MST)", command=show_campus_map).grid(row=0, column=1, padx=10)

# Search section
search_frame = tk.Frame(root, bg="#f0f4f7")
search_frame.pack(pady=10)
tk.Label(search_frame, text="Search Route (e.g. A-J):", font=("Arial", 12), bg="#f0f4f7").grid(row=0, column=0, padx=10)
search_var = tk.StringVar()
tk.Entry(search_frame, textvariable=search_var, width=10).grid(row=0, column=1, padx=5)
ttk.Button(search_frame, text="Search", command=search_route).grid(row=0, column=2, padx=10)

# Result area
result_text = tk.StringVar()
result_label = tk.Label(root, textvariable=result_text, font=("Arial", 12), bg="#f0f4f7", fg="#1a5276", justify="left")
result_label.pack(pady=20)

ttk.Button(root, text="Exit", command=root.destroy).pack(pady=10)

root.mainloop()
