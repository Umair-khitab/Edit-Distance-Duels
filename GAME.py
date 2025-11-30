# -*- coding: utf-8 -*-
"""
Created on Sun Nov 30 22:47:44 2025

@author: khita
"""

import tkinter as tk
from tkinter import ttk

# Tooltip helper class
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        widget.bind("<Enter>", self.show_tip)
        widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert") if self.widget.bbox("insert") else (0,0,0,0)
        x = x + self.widget.winfo_rootx() + 25
        y = y + self.widget.winfo_rooty() + 20
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify="left",
                         background="#ffffe0", relief="solid", borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(ipadx=4)

    def hide_tip(self, event=None):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

class LevenshteinGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Levenshtein Distance Game")

        # Input fields
        self.s1_var = tk.StringVar(value="hello")
        self.s2_var = tk.StringVar(value="yellow")

        frm = ttk.Frame(root, padding=10)
        frm.pack(fill="x")

        ttk.Label(frm, text="String A").grid(row=0, column=0)
        ttk.Entry(frm, textvariable=self.s1_var).grid(row=0, column=1)

        ttk.Label(frm, text="String B").grid(row=1, column=0)
        ttk.Entry(frm, textvariable=self.s2_var).grid(row=1, column=1)

        ttk.Button(frm, text="Build Grid", command=self.build).grid(row=0, column=2, rowspan=2, padx=5)
        ttk.Button(frm, text="Step", command=self.step).grid(row=0, column=3, rowspan=2, padx=5)
        ttk.Button(frm, text="Solve", command=self.solve).grid(row=0, column=4, rowspan=2, padx=5)

        # Status labels
        self.distance_label = ttk.Label(root, text="Edit distance: –")
        self.distance_label.pack()
        self.ratio_label = ttk.Label(root, text="Similarity ratio: –")
        self.ratio_label.pack()
        self.attack_label = ttk.Label(root, text="Attack power: –")
        self.attack_label.pack()

        # Grid frame
        self.grid_frame = ttk.Frame(root, padding=10)
        self.grid_frame.pack()

        self.A = ""
        self.B = ""
        self.DP = []
        self.OP = []
        self.filled_i = 0
        self.filled_j = 0

    def build(self):
        self.A = self.s1_var.get()
        self.B = self.s2_var.get()
        n, m = len(self.A), len(self.B)

        # Reset
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        self.DP = [[0]*(m+1) for _ in range(n+1)]
        self.OP = [[""]*(m+1) for _ in range(n+1)]

        # Base cases
        for i in range(n+1):
            self.DP[i][0] = i
        for j in range(m+1):
            self.DP[0][j] = j

        # Headers
        tk.Label(self.grid_frame, text="", width=4).grid(row=0, column=0)
        for j in range(m):
            tk.Label(self.grid_frame, text=self.B[j], width=4, fg="gray").grid(row=0, column=j+1)
        for i in range(n):
            tk.Label(self.grid_frame, text=self.A[i], width=4, fg="gray").grid(row=i+1, column=0)

        # Initial grid
        for i in range(n+1):
            for j in range(m+1):
                val = self.DP[i][j]
                lbl = tk.Label(self.grid_frame, text=str(val), width=4, height=2, borderwidth=1, relief="solid")
                lbl.grid(row=i+1, column=j+1)
                lbl._coords = (i, j)
                ToolTip(lbl, f"Base case DP[{i}][{j}] = {val}")
        self.filled_i, self.filled_j = 1, 1
        self.distance_label.config(text="Edit distance: –")
        self.ratio_label.config(text="Similarity ratio: –")
        self.attack_label.config(text="Attack power: –")

    def paint_cell(self, i, j, val, op):
        for widget in self.grid_frame.winfo_children():
            if hasattr(widget, "_coords") and widget._coords == (i, j):
                widget.config(text=str(val), bg=self.color_for(op))

                charA = self.A[i-1] if i > 0 else "∅"
                charB = self.B[j-1] if j > 0 else "∅"

                if op == "match":
                    tip_text = f"🟩 Match: '{charA}' = '{charB}'\nDP[{i}][{j}] = {val}"
                elif op == "sub":
                    tip_text = f"🔴 Replacement: '{charA}' → '{charB}'\nDP[{i}][{j}] = {val}"
                elif op == "ins":
                    tip_text = f"🔵 Insertion: add '{charB}'\nDP[{i}][{j}] = {val}"
                elif op == "del":
                    tip_text = f"🟡 Deletion: remove '{charA}'\nDP[{i}][{j}] = {val}"
                else:
                    tip_text = f"DP[{i}][{j}] = {val}"

                ToolTip(widget, tip_text)

    def color_for(self, op):
        return {
            "match": "lightgreen",
            "sub": "red",
            "ins": "lightblue",
            "del": "yellow"
        }.get(op, "white")

    def step(self):
        n, m = len(self.A), len(self.B)
        if self.filled_i > n: return False
        i, j = self.filled_i, self.filled_j

        cost = 0 if self.A[i-1] == self.B[j-1] else 1
        del_cost = self.DP[i-1][j] + 1
        ins_cost = self.DP[i][j-1] + 1
        sub_cost = self.DP[i-1][j-1] + cost

        val = min(del_cost, ins_cost, sub_cost)
        self.DP[i][j] = val

        if val == sub_cost:
            op = "match" if cost == 0 else "sub"
        elif val == ins_cost:
            op = "ins"
        else:
            op = "del"
        self.OP[i][j] = op
        self.paint_cell(i, j, val, op)

        if self.filled_j < m:
            self.filled_j += 1
        else:
            self.filled_j = 1
            self.filled_i += 1

        if self.filled_i > n:
            self.finalize()
        return True

    def solve(self):
        while self.step():
            pass

    def finalize(self):
        n, m = len(self.A), len(self.B)
        dist = self.DP[n][m]
        self.distance_label.config(text=f"Edit distance: {dist}")
        ratio = (n + m - dist) / max(1, (n + m))
        self.ratio_label.config(text=f"Similarity ratio: {ratio*100:.1f}%")
        denom = max(1, max(n, m))
        power = max(0, round((1 - dist/denom)*100))
        self.attack_label.config(text=f"Attack power: {power} ⚔️")
        self.draw_path()

    def draw_path(self):
        """Highlight optimal path from bottom-right to top-left."""
        n, m = len(self.A), len(self.B)
        i, j = n, m
        while i >= 0 and j >= 0:
            for widget in self.grid_frame.winfo_children():
                if hasattr(widget, "_coords") and widget._coords == (i, j):
                    widget.config(relief="ridge", bd=3, fg="black", bg="white")
            if i == 0 and j == 0:
                break
            # ✅ fixed line
            op = self.OP[i][j] if i >= 0 and j >= 0 else ""
            if op in ("match", "sub"):
                i -= 1; j -= 1
            elif op == "del":
                i -= 1
            elif op == "ins":
                j -= 1
            else:
                break


