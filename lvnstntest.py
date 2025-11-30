# -*- coding: utf-8 -*-
"""
Created on Sun Nov 30 23:42:05 2025

@author: khita
"""

def levenshtein_dp(a: str, b: str):
    n, m = len(a), len(b)
    dp = [[0]*(m+1) for _ in range(n+1)]
    op = [[""]*(m+1) for _ in range(n+1)]

    # Base cases
    for i in range(n+1):
        dp[i][0] = i
        op[i][0] = "del" if i > 0 else ""
    for j in range(m+1):
        dp[0][j] = j
        op[0][j] = "ins" if j > 0 else ""

    # Fill DP
    for i in range(1, n+1):
        for j in range(1, m+1):
            cost = 0 if a[i-1] == b[j-1] else 1
            del_cost = dp[i-1][j] + 1
            ins_cost = dp[i][j-1] + 1
            sub_cost = dp[i-1][j-1] + cost

            best = min(del_cost, ins_cost, sub_cost)
            dp[i][j] = best

            if best == sub_cost:
                op[i][j] = "match" if cost == 0 else "sub"
            elif best == ins_cost:
                op[i][j] = "ins"
            else:
                op[i][j] = "del"

    return dp, op

def backtrack_path(op, a, b):
    """Return list of (i,j) coordinates on optimal path from (n,m) to (0,0)."""
    path = []
    i, j = len(a), len(b)
    while i >= 0 and j >= 0:
        path.append((i, j))
        if i == 0 and j == 0:
            break
        curr = op[i][j] if i >= 0 and j >= 0 else ""
        if curr in ("match", "sub"):
            i -= 1; j -= 1
        elif curr == "del":
            i -= 1
        elif curr == "ins":
            j -= 1
        else:
            # Fallback for any unexpected blank (shouldn't happen with proper base cases)
            if i > 0: i -= 1
            elif j > 0: j -= 1
            else: break
    return path

def print_matrix(a: str, b: str, dp, op, path):
    n, m = len(a), len(b)
    path_set = set(path)

    # Header row
    header = ["    "] + [f"  {ch} " for ch in b]
    print("".join(header))

    # Grid with left header
    for i in range(n+1):
        left = "   " if i == 0 else f" {a[i-1]} "
        row_cells = []
        for j in range(m+1):
            val = dp[i][j]
            in_path = (i, j) in path_set
            # Mark path cells with brackets; others plain
            cell = f"[{val:2d}]" if in_path else f" {val:2d} "
            row_cells.append(cell)
        print(left + "".join(row_cells))

    # Optional: operation legend per cell (compact)
    print("\nOperation grid (M=match, S=sub, I=ins, D=del):")
    print("".join(["    "] + [f"  {ch} " for ch in b]))
    for i in range(n+1):
        left = "   " if i == 0 else f" {a[i-1]} "
        row_ops = []
        for j in range(m+1):
            o = op[i][j]
            mark = {
                "match": "M", "sub": "S", "ins": "I", "del": "D", "": "."
            }[o]
            row_ops.append(f"  {mark} ")
        print(left + "".join(row_ops))

def summary(a: str, b: str, dp):
    n, m = len(a), len(b)
    dist = dp[n][m]
    ratio = (n + m - dist) / max(1, (n + m))  # same as your web version
    attack = max(0, round((1 - dist / max(1, max(n, m))) * 100))
    print("\nSummary:")
    print(f"- String A: '{a}' (n={len(a)})")
    print(f"- String B: '{b}' (m={len(b)})")
    print(f"- Edit distance: {dist}")
    print(f"- Similarity ratio: {ratio*100:.1f}%")
    print(f"- Attack power: {attack} ⚔️")

if __name__ == "__main__":
    A = "hello"
    B = "yellow"

    dp, op = levenshtein_dp(A, B)
    path = backtrack_path(op, A, B)
    print_matrix(A, B, dp, op, path)
    summary(A, B, dp)
