# Knapsack Problem — Algorithmic Approaches

## Overview

This project implements and compares several algorithmic approaches for solving the **0/1 Knapsack Problem**.

The objective is to select a subset of items that maximizes the total value while respecting a given capacity constraint.

Several approaches are implemented in order to compare their principles, complexity and practical behavior:

* Greedy algorithm
* Brute-force search
* Dynamic programming
* Branch and Bound

The project also provides a graphical interface for interacting with the different algorithms.

## Problem Definition

Given a set of `n` items, each item has:

* a weight `wᵢ`
* a value `vᵢ`

and the knapsack has a maximum capacity `C`.

The objective is to maximize:

```text
Σ vᵢ xᵢ
```

subject to:

```text
Σ wᵢ xᵢ ≤ C

xᵢ ∈ {0, 1}
```

where `xᵢ = 1` means that item `i` is selected and `xᵢ = 0` means that it is not selected.

## Implemented Algorithms

### Greedy Algorithm

The greedy approach selects items according to a local criterion, such as the value-to-weight ratio.

It provides a fast solution, although it does not always guarantee the optimal solution for the 0/1 Knapsack Problem.

### Brute Force

The brute-force approach explores the possible combinations of items in order to identify the optimal solution.

It guarantees an optimal solution but has exponential time complexity.

### Dynamic Programming

The dynamic programming approach decomposes the problem into overlapping subproblems and stores previously computed results.

For a capacity `C` and `n` items, the classical approach uses a table defined by:

```text
DP[i][c] = maximum value obtainable
           using the first i items
           with capacity c
```

The method provides an exact solution with significantly better complexity than exhaustive enumeration.

### Branch and Bound

Branch and Bound explores the solution space as a search tree.

Branches that cannot produce a better solution than the current best solution are eliminated using an upper-bound estimation.

This reduces the number of combinations that need to be explored while still guaranteeing an optimal solution.

## Project Structure

```text
Knapsack-Problem-Algorithms/
├── ...
└── README.md
```

The source files contain the implementations of the different algorithms as well as the graphical interface.

## Comparison

The project makes it possible to compare the approaches according to several criteria:

| Algorithm           | Optimal solution | Main characteristic       |
| ------------------- | ---------------- | ------------------------- |
| Greedy              | Not guaranteed   | Fast heuristic approach   |
| Brute Force         | Yes              | Exhaustive search         |
| Dynamic Programming | Yes              | Uses subproblem structure |
| Branch and Bound    | Yes              | Prunes the search space   |

The practical performance depends on the number of items, the capacity and the characteristics of the generated instance.

## Graphical Interface

A graphical interface is provided to facilitate experimentation with the different approaches.

It allows the user to work with knapsack instances and execute the implemented algorithms.

## Technologies

* Python
* Algorithm design and analysis
* Dynamic programming
* Branch and Bound
* Combinatorial optimization
* Graphical user interface

## Objectives

This project was developed to study and compare different algorithmic strategies for solving an optimization problem.

It provides practical experience with:

* algorithm design;
* complexity analysis;
* exhaustive search;
* dynamic programming;
* search-space pruning;
* combinatorial optimization;
* comparative algorithm evaluation.

## Academic Context

Academic project focused on **Operations Research and Algorithmic Optimization**.

## Author

**Ismaël Lebange**

Master's student in Artificial Intelligence
