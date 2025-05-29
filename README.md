# Maximum Clique Problem: Genetic Algorithm vs. Simulated Annealing

![Clique Visualization](docs/clique_visualization.png)

Implementation of two metaheuristic approaches to solve the NP-hard Maximum Clique Problem in graph theory.

##  Features

**Algorithms**:
- **Genetic Algorithm (GA)** with:
  - Roulette wheel selection
  - Single-point crossover
  - Degree-based mutation
  - Local optimization

- **Simulated Annealing (SA)** with:
  - Degree-weighted acceptance function
  - Geometric cooling schedule
  - Neighborhood search

**Graph Generation**:
- Erdős–Rényi random graphs via NetworkX
- Configurable node count (50-1000) and edge probability

**Metrics**:
- Clique size validation
- Runtime benchmarking
- Solution quality comparison

##  Installation

1. Clone repository:
   ```bash
   git clone https://github.com/yourusername/AI-Clique-Problem.git
   cd Maximal-Clique-Problem
