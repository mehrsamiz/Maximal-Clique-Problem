import networkx as nx
import random

def generate_random_graph(num_nodes, probability):
    """
    Generate a random graph using the Erdős–Rényi model.
    """
    return nx.erdos_renyi_graph(num_nodes, probability)

def preprocess_graph(graph):
    """
    Preprocess the graph by sorting nodes by degree in descending order.
    """
    sorted_nodes = sorted(graph.nodes, key=lambda x: graph.degree[x], reverse=True)
    return sorted_nodes

def fitness(clique, graph):
    """
    Calculate fitness based on the size of the clique and whether it's valid.
    """
    subgraph = graph.subgraph(clique)
    if nx.is_clique(subgraph):
        return len(clique)
    return 0

def is_clique(graph, nodes):
    """
    Check if a set of nodes forms a clique in the graph.
    """
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            if not graph.has_edge(nodes[i], nodes[j]):
                return False
    return True

def mutate(clique, graph):
    """
    Perform mutation by adding or removing a random node.
    """
    if random.random() < 0.5 and len(clique) > 0:  # Remove a random node
        clique.remove(random.choice(clique))
    else:  # Add a random neighbor node
        potential_nodes = list(set(graph.nodes) - set(clique))
        if potential_nodes:
            clique.append(random.choice(potential_nodes))
    return clique

def crossover(parent1, parent2):
    """
    Perform crossover by combining subsets of two parents.
    """
    midpoint = len(parent1) // 2
    child = parent1[:midpoint] + parent2[midpoint:]
    return list(set(child))  # Ensure unique nodes

def clique_extraction(chromosome, graph):
    """
    Extract a valid clique from a chromosome using a greedy approach.
    """
    clique = []
    for node in chromosome:
        if all(graph.has_edge(node, other) for other in clique):
            clique.append(node)
    return clique

def local_optimization(clique, graph):
    """
    Improve the clique by attempting to add more nodes.
    """
    for node in graph.nodes:
        if node not in clique and all(graph.has_edge(node, other) for other in clique):
            clique.append(node)
    return clique

def select_parents(population, fitness_values):
    """
    Select two parents using roulette wheel selection.
    """
    total_fitness = sum(fitness_values)
    if total_fitness == 0:
        return random.choice(population), random.choice(population)

    probs = [f / total_fitness for f in fitness_values]
    parent1 = random.choices(population, weights=probs, k=1)[0]
    parent2 = random.choices(population, weights=probs, k=1)[0]
    return parent1, parent2

def genetic_algorithm(graph, population_size=50, generations=100):
    """
    Genetic Algorithm for finding the maximum clique.
    """
    sorted_nodes = preprocess_graph(graph)

    # Initialize population with random subsets of sorted nodes
    population = [random.sample(sorted_nodes, random.randint(1, len(sorted_nodes))) for _ in range(population_size)]

    best_clique = []
    for generation in range(generations):
        # Evaluate fitness for each individual in the population
        fitness_values = []
        for individual in population:
            extracted_clique = clique_extraction(individual, graph)
            fitness_values.append(fitness(extracted_clique, graph))

        # Update the best clique found so far
        max_index = fitness_values.index(max(fitness_values))
        if fitness_values[max_index] > len(best_clique):
            best_clique = clique_extraction(population[max_index], graph)

        # Create a new population
        new_population = []
        for _ in range(population_size // 2):
            # Select parents
            parent1, parent2 = select_parents(population, fitness_values)

            # Perform crossover
            child1 = crossover(parent1, parent2)
            child2 = crossover(parent2, parent1)

            # Perform mutation
            child1 = mutate(child1, graph)
            child2 = mutate(child2, graph)

            # Apply local optimization
            child1 = local_optimization(child1, graph)
            child2 = local_optimization(child2, graph)

            # Add children to the new population
            new_population.extend([child1, child2])

        population = new_population

    return best_clique

# Main program
if __name__ == "__main__":
    # Generate a random graph
    num_nodes = 50
    probability = 0.3
    graph = generate_random_graph(num_nodes, probability)

    # Run the genetic algorithm
    max_clique = genetic_algorithm(graph)

    # Output results
    print(f"Maximum Clique Size: {len(max_clique)}")
    print(f"Nodes in Maximum Clique: {max_clique}")