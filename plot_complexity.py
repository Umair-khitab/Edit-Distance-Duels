# -*- coding: utf-8 -*-
"""
Created on Mon Dec  1 02:35:42 2025

@author: khita
"""

# plot_complexity.py
import matplotlib.pyplot as plt

# Example benchmark results (you can replace with actual data from benchmark_complexity.py)
matrix_sizes = [3*3, 6*7, 6*5, 9*6, 13*13]        # n × m
runtimes = [0.2, 0.4, 1.1, 2.8, 7.3]              # Avg runtime (ms)

# Optional: Labels for each test case
cases_labels = ["cat-cut", "kitten-sitting", "abcdef-azced", "algorithm-rhythm", "transformation-transportation"]

plt.figure(figsize=(8, 5))
plt.plot(matrix_sizes, runtimes, marker='o', linewidth=2)

# Annotate points
for i, label in enumerate(cases_labels):
    plt.text(matrix_sizes[i] * 1.02, runtimes[i] * 0.97, label, fontsize=9)

plt.xlabel("DP Matrix Size (n × m)")
plt.ylabel("Average Runtime (ms)")
plt.title("Edit Distance Complexity: DP Matrix Size vs Time")
plt.grid(True)
plt.tight_layout()
plt.show()
