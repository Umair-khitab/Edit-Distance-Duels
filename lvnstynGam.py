# -*- coding: utf-8 -*-
"""
Created on Tue Dec  2 15:51:37 2025

@author: khita
"""

# -*- coding: utf-8 -*-
"""
Neon / Glass Levenshtein Distance UI (Blue Neon theme NG-1)
Author: adapted for user
"""

import tkinter as tk
from tkinter import ttk

# -------------------------
# NEON THEME (NG-1: Blue Neon)
# -------------------------
NEON_BG = "#071124"         # deep midnight background
PANEL_BG = "#0b1624"        # slightly lighter panel
GLASS_BG = "#08111a"        # cell base (glass)
NEON_BLUE = "#39C6FF"       # neon blue letters / insert glow
NEON_CYAN = "#6EF1FF"       # cyan glow accents
NEON_RED = "#FF4D6D"        # red indices, sub glow
NEON_GREEN = "#7CFF89"      # match glow
NEON_YELLOW = "#FFD56B"     # delete glow
CELL_BORDER = "#17313f"     # subtle border color
CELL_SIZE_W = 6
CELL_SIZE_H = 2

# -------------------------
# Tooltip (glass-style)
# -------------------------
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
        # compute position near widget
        try:
            bbox = self.widget.bbox("insert")
            if bbox:
                x, y, cx, cy = bbox
            else:
                x, y, cx, cy = 0, 0, 0, 0
        except Exception:
            x, y, cx, cy = 0, 0, 0, 0
        x = x + self.widget.winfo_rootx() + 20
        y = y + self.widget.winfo_rooty() + 20

        tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        tw.configure(bg="#09151b")  # glass background

        lbl = tk.Label(tw,
                       text=self.text,
                       justify="left",
                       bg="#09151b",
                       fg="#BFEFFF",
                       relief="solid",
                       bd=0,
                       font=("Consolas", 9))
        lbl.pack(ipadx=6, ipady=4)
        self.tipwindow = tw

    def hide_tip(self, event=None):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

# -------------------------
# Levenshtein Game
# -------------------------
class LevenshteinGame:
    def __init__(self, root):
        self.root = root
        root.title("Levenshtein — Neon Grid")
        root.configure(bg=NEON_BG)
        self.frame = ttk.Frame(root)
        self.frame.pack(padx=12, pady=12)

        # input variables with 10-char limit
        self.s1_var = tk.StringVar(value="hello")
        self.s2_var = tk.StringVar(value="yellow")
        self.s1_var.trace_add("write", self.limit_length)
        self.s2_var.trace_add("write", self.limit_length)

        # top controls panel (glass-like)
        ctrl = tk.Frame(root, bg=PANEL_BG, padx=10, pady=10)
        ctrl.pack(fill="x", padx=12, pady=(12,6))

        tk.Label(ctrl, text="String A", bg=PANEL_BG, fg=NEON_CYAN, font=("Consolas", 10)).grid(row=0, column=0, sticky="w")
        tk.Entry(ctrl, textvariable=self.s1_var, width=14, font=("Consolas", 10),
                 relief="flat", bg="#071620", fg=NEON_BLUE, insertbackground=NEON_BLUE).grid(row=0, column=1, padx=6)

        tk.Label(ctrl, text="String B", bg=PANEL_BG, fg=NEON_CYAN, font=("Consolas", 10)).grid(row=1, column=0, sticky="w")
        tk.Entry(ctrl, textvariable=self.s2_var, width=14, font=("Consolas", 10),
                 relief="flat", bg="#071620", fg=NEON_BLUE, insertbackground=NEON_BLUE).grid(row=1, column=1, padx=6)

        bld = tk.Button(ctrl, text="Build Grid", command=self.build, bg="#091a22", fg=NEON_CYAN,
                        activebackground="#062026", relief="ridge", bd=1, font=("Consolas", 10))
        bld.grid(row=0, column=2, rowspan=2, padx=8)

        step_btn = tk.Button(ctrl, text="Step", command=self.step, bg="#091a22", fg=NEON_CYAN,
                             activebackground="#062026", relief="ridge", bd=1, font=("Consolas", 10))
        step_btn.grid(row=0, column=3, rowspan=2, padx=6)

        solve_btn = tk.Button(ctrl, text="Solve", command=self.solve, bg="#091a22", fg=NEON_CYAN,
                              activebackground="#062026", relief="ridge", bd=1, font=("Consolas", 10))
        solve_btn.grid(row=0, column=4, rowspan=2, padx=6)

        swap_btn = tk.Button(ctrl, text="Swap", command=self.swap_strings, bg="#091a22", fg=NEON_CYAN,
                             relief="ridge", bd=1, font=("Consolas", 10))
        swap_btn.grid(row=0, column=5, rowspan=2, padx=6)

        # status labels
        status = tk.Frame(root, bg=NEON_BG)
        status.pack(fill="x", padx=12)
        self.distance_label = tk.Label(status, text="Edit distance: –", bg=NEON_BG, fg="#BFEFFF", font=("Consolas", 10))
        self.distance_label.pack(side="left", padx=(0,12))
        self.ratio_label = tk.Label(status, text="Similarity ratio: –", bg=NEON_BG, fg="#BFEFFF", font=("Consolas", 10))
        self.ratio_label.pack(side="left", padx=(0,12))
        self.attack_label = tk.Label(status, text="Attack power: –", bg=NEON_BG, fg="#BFEFFF", font=("Consolas", 10))
        self.attack_label.pack(side="left", padx=(0,12))

        # grid frame
        self.grid_frame = tk.Frame(root, bg=NEON_BG, padx=8, pady=8)
        self.grid_frame.pack(padx=12, pady=(6,12))

        # DP state
        self.A = ""
        self.B = ""
        self.DP = []
        self.OP = []
        self.filled_i = 0
        self.filled_j = 0
        self.cells = {}  # map (i,j)->label

        # initial build
        self.build()

    def limit_length(self, *args):
        a = self.s1_var.get()[:10]
        b = self.s2_var.get()[:10]
        if self.s1_var.get() != a:
            self.s1_var.set(a)
        if self.s2_var.get() != b:
            self.s2_var.set(b)

    def swap_strings(self):
        a = self.s1_var.get()
        b = self.s2_var.get()
        self.s1_var.set(b)
        self.s2_var.set(a)
        self.build()

    def clear_grid_widgets(self):
        for child in self.grid_frame.winfo_children():
            child.destroy()
        self.cells.clear()

    def build(self):
        # read strings (already limited)
        self.A = self.s1_var.get()
        self.B = self.s2_var.get()
        n, m = len(self.A), len(self.B)

        # reset
        self.clear_grid_widgets()
        self.DP = [[0] * (m + 1) for _ in range(n + 1)]
        self.OP = [[""] * (m + 1) for _ in range(n + 1)]

        # base cases
        for i in range(n + 1):
            self.DP[i][0] = i
        for j in range(m + 1):
            self.DP[0][j] = j

        # header spacing top-left corner
        corner = tk.Label(self.grid_frame, text="", width=CELL_SIZE_W, height=CELL_SIZE_H,
                          bg=NEON_BG, fg=NEON_CYAN, font=("Consolas", 10))
        corner.grid(row=0, column=0, padx=2, pady=2)

        # top headers (B)
        for j in range(m):
            lbl = tk.Label(self.grid_frame, text=self.B[j], width=CELL_SIZE_W, height=CELL_SIZE_H,
                           bg=GLASS_BG, fg=NEON_BLUE, font=("Consolas", 12, "bold"),
                           bd=1, relief="solid", highlightthickness=2, highlightbackground=CELL_BORDER)
            lbl.grid(row=0, column=j + 1, padx=2, pady=2)
            # neon effect via border highlight color (simulate glow)
            lbl.configure(highlightbackground=NEON_CYAN)

        # left headers (A)
        for i in range(n):
            lbl = tk.Label(self.grid_frame, text=self.A[i], width=CELL_SIZE_W, height=CELL_SIZE_H,
                           bg=GLASS_BG, fg=NEON_BLUE, font=("Consolas", 12, "bold"),
                           bd=1, relief="solid", highlightthickness=2, highlightbackground=CELL_BORDER)
            lbl.grid(row=i + 1, column=0, padx=2, pady=2)
            lbl.configure(highlightbackground=NEON_CYAN)

        # index numerals (red) for top row and left column base-case numbers
        for j in range(m + 1):
            val = self.DP[0][j]
            lbl = tk.Label(self.grid_frame, text=str(val), width=CELL_SIZE_W, height=CELL_SIZE_H,
                           bg=GLASS_BG, fg=NEON_RED, font=("Consolas", 10, "bold"),
                           bd=1, relief="solid")
            lbl.grid(row=1, column=j + 1, padx=2, pady=2)
            self.cells[(0, j)] = lbl
            ToolTip(lbl, f"DP[0][{j}] = {val}")

        for i in range(1, len(self.DP)):
            val = self.DP[i][0]
            lbl = tk.Label(self.grid_frame, text=str(val), width=CELL_SIZE_W, height=CELL_SIZE_H,
                           bg=GLASS_BG, fg=NEON_RED, font=("Consolas", 10, "bold"),
                           bd=1, relief="solid")
            lbl.grid(row=i + 1, column=1, padx=2, pady=2)
            self.cells[(i, 0)] = lbl
            ToolTip(lbl, f"DP[{i}][0] = {val}")

        # inner cells
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                val = self.DP[i][j]
                lbl = tk.Label(self.grid_frame, text=str(val), width=CELL_SIZE_W, height=CELL_SIZE_H,
                               bg=GLASS_BG, fg="#BFEFFF", font=("Consolas", 10),
                               bd=1, relief="solid", highlightthickness=1, highlightbackground=CELL_BORDER)
                lbl.grid(row=i + 1, column=j + 1, padx=2, pady=2)
                lbl._coords = (i, j)
                self.cells[(i, j)] = lbl
                ToolTip(lbl, f"DP[{i}][{j}] = {val}")

        # reset step indices
        self.filled_i, self.filled_j = 1, 1
        self.distance_label.config(text="Edit distance: –")
        self.ratio_label.config(text="Similarity ratio: –")
        self.attack_label.config(text="Attack power: –")

    # choose neon pulse color for op
    def op_color(self, op):
        return {
            "match": NEON_GREEN,
            "sub": NEON_RED,
            "ins": NEON_BLUE,
            "del": NEON_YELLOW
        }.get(op, NEON_CYAN)

    # animate a cell pulse then set text/background
    def paint_cell(self, i, j, val, op):
        lbl = self.cells.get((i, j))
        if not lbl:
            return
        glow = self.op_color(op)

        # pulse: set glow background briefly then return to glass with colored highlight
        def pulse_step1():
            lbl.config(text=str(val), bg=glow, fg="#071124", font=("Consolas", 10, "bold"))
        def pulse_step2():
            lbl.config(bg=GLASS_BG, fg="#BFEFFF", font=("Consolas", 10))
            # highlight border to simulate glow
            lbl.configure(highlightbackground=glow, highlightthickness=2)
            # update tooltip text
            charA = self.A[i-1] if i > 0 else "∅"
            charB = self.B[j-1] if j > 0 else "∅"
            if op == "match":
                tip = f"Match: '{charA}' = '{charB}'  DP[{i}][{j}]={val}"
            elif op == "sub":
                tip = f"Replace: '{charA}'→'{charB}'  DP[{i}][{j}]={val}"
            elif op == "ins":
                tip = f"Insert: '{charB}'  DP[{i}][{j}]={val}"
            elif op == "del":
                tip = f"Delete: '{charA}'  DP[{i}][{j}]={val}"
            else:
                tip = f"DP[{i}][{j}]={val}"
            ToolTip(lbl, tip)

        # start pulse
        pulse_step1()
        # after short delay, revert to glass look with neon highlight
        self.root.after(260, pulse_step2)

    def step(self):
        n, m = len(self.A), len(self.B)
        if self.filled_i > n:
            return False

        i, j = self.filled_i, self.filled_j
        # compute costs safely if indices valid
        cost = 0 if self.A[i - 1] == self.B[j - 1] else 1
        del_cost = self.DP[i - 1][j] + 1
        ins_cost = self.DP[i][j - 1] + 1
        sub_cost = self.DP[i - 1][j - 1] + cost

        val = min(del_cost, ins_cost, sub_cost)
        self.DP[i][j] = val

        if val == sub_cost:
            op = "match" if cost == 0 else "sub"
        elif val == ins_cost:
            op = "ins"
        else:
            op = "del"
        self.OP[i][j] = op

        # animate cell
        self.paint_cell(i, j, val, op)

        # advance indices
        if self.filled_j < m:
            self.filled_j += 1
        else:
            self.filled_j = 1
            self.filled_i += 1

        if self.filled_i > n:
            self.finalize()
        return True

    def solve(self):
        # compute all remaining steps without long GUI blocking (use after)
        def work():
            if self.step():
                self.root.after(30, work)
        work()

    def finalize(self):
        n, m = len(self.A), len(self.B)
        dist = self.DP[n][m]
        self.distance_label.config(text=f"Edit distance: {dist}")
        ratio = (n + m - dist) / max(1, (n + m))
        self.ratio_label.config(text=f"Similarity ratio: {ratio*100:.1f}%")
        denom = max(1, max(n, m))
        power = max(0, round((1 - dist/denom)*100))
        self.attack_label.config(text=f"Attack power: {power} ⚔️")
        # draw path after small delay to allow final pulses to finish
        self.root.after(350, self.draw_path)

    def draw_path(self):
        # highlight the optimal path with a strong neon outline
        n, m = len(self.A), len(self.B)
        i, j = n, m
        while i >= 0 and j >= 0:
            lbl = self.cells.get((i, j))
            if lbl:
                # strong border and slight fill
                lbl.config(bg="#041018", fg=NEON_CYAN, font=("Consolas", 10, "bold"))
                lbl.configure(highlightbackground=NEON_CYAN, highlightthickness=3)
            if i == 0 and j == 0:
                break
            op = self.OP[i][j] if i >= 0 and j >= 0 else ""
            if op in ("match", "sub"):
                i -= 1; j -= 1
            elif op == "del":
                i -= 1
            elif op == "ins":
                j -= 1
            else:
                # fallback to diagonal if missing op
                i -= 1; j -= 1

# -------------------------------
# START PROGRAM
# -------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    # use a monospace-friendly font if available
    try:
        root.option_add("*Font", "Consolas 10")
    except Exception:
        pass
    app = LevenshteinGame(root)
    root.mainloop()
