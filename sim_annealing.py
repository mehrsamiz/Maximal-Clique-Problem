import networkx as nx
import random
import math

def generate_random_graph(num_nodes, probability):
    """
    Generate a random graph using the Erdős–Rényi model.
    """
    return nx.erdos_renyi_graph(num_nodes, probability)

def is_clique(graph, nodes):
    """
    Check if a set of nodes forms a clique in the graph.
    """
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            if not graph.has_edge(nodes[i], nodes[j]):
                return False
    return True

def acceptance_probability(delta, temperature, degree):
    """
    Calculate acceptance probability using degree-based acceptance function.
    """
    if delta < 0:
        return 1.0
    return math.exp(-delta / (temperature * (1 + degree)))

def find_neighbors(graph, current_clique):
    """
    Generate a neighboring solution by adding or removing a node.
    """
    new_clique = current_clique.copy()
    if random.random() < 0.5 and new_clique:
        # Remove a random node
        new_clique.remove(random.choice(new_clique))
    else:
        # Add a random node
        remaining_nodes = list(set(graph.nodes) - set(new_clique))
        if remaining_nodes:
            new_node = random.choice(remaining_nodes)
            new_clique.append(new_node)
    return new_clique

def evaluate_clique(graph, clique):
    """
    Evaluate the quality of a clique based on size and validity.
    """
    return len(clique) if is_clique(graph, clique) else 0

def simulated_annealing(graph, initial_temp=100, alpha=0.95, stopping_temp=0.001, max_steps=1000):
    """
    ISA Algorithm to find the Maximum Clique.
    """
    # Initial solution
    current_clique = random.sample(list(graph.nodes), random.randint(1, len(graph.nodes)))
    current_fitness = evaluate_clique(graph, current_clique)

    best_clique = current_clique.copy()
    best_fitness = current_fitness

    temperature = initial_temp
    step = 0

    while temperature > stopping_temp and step < max_steps:
        # Generate a neighbor
        neighbor_clique = find_neighbors(graph, current_clique)
        neighbor_fitness = evaluate_clique(graph, neighbor_clique)

        # Calculate degree for acceptance function
        degree = sum(graph.degree[node] for node in neighbor_clique) / len(neighbor_clique) if neighbor_clique else 0

        # Determine acceptance probability
        delta = neighbor_fitness - current_fitness
        prob = acceptance_probability(delta, temperature, degree)

        # Accept or reject the new solution
        if random.random() < prob:
            current_clique = neighbor_clique
            current_fitness = neighbor_fitness

        # Update best solution if necessary
        if current_fitness > best_fitness:
            best_clique = current_clique.copy()
            best_fitness = current_fitness

        # Reduce temperature
        temperature *= alpha
        step += 1

    return best_clique

# Main program
if __name__ == "__main__":
    # Generate a random graph
    num_nodes = 50
    probability = 0.3
    graph = generate_random_graph(num_nodes, probability)

    # Run the ISA algorithm
    max_clique = simulated_annealing(graph)

    # Output results
    print(f"Maximum Clique Size: {len(max_clique)}")
    print(f"Nodes in Maximum Clique: {max_clique}")
