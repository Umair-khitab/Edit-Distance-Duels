# Edit-Distance-Duels
A game-based implementation of the Edit Distance (Levenshtein) algorithm using Dynamic Programming and Tkinter.
Project Overview

Edit Distance Duels is an educational word battle game where players visualize how the Edit Distance algorithm transforms one word into another using insertion, deletion, and substitution operations.

Each operation is color-animated in a Dynamic Programming (DP) matrix, making complex algorithm execution interactive and understandable.

🟢 Less edits = more attack power → stronger hit in battle!

🎯 Learning Objectives

Understand Dynamic Programming through visualization

Learn how Edit Distance algorithm works step-by-step

Explore time & space complexity practically

Apply algorithmic logic in game mechanics

Demonstrate performance impacts and algorithm visualization

🛠️ Tech Stack
Component	Technology
Programming Language	Python
GUI Library	Tkinter
Algorithm	Edit Distance (Levenshtein) – Dynamic Programming
Visualization	Grid-based Tkinter animation
Documentation Format	APA 6
📂 Folder Structure
EditDistanceDuels/
│── code/
│   ├── game.py             # Tkinter-based interface
│   ├── edit_distance.py    # Algorithm and step tracing
│
│── docs/
│   ├── steps.md            # Algorithm pseudocode & execution steps
│   ├── complexity.md       # Phase 3 analysis
│
│── REPORT.pdf              # Final APA-standard report
│── README.md               # Project setup and summary  

🚀 How to Run
pip install tk
python code/game.py


💡 Note: Tkinter is included with most Python installations. If missing, install manually using pip install tk.

🎨 Visualization Legend
Operation	DP Cell Color
🟢 Match	Green
🔵 Insert	Blue
🟡 Delete	Yellow
🔴 Substitute	Red
📊 Example Gameplay Flow

1️⃣ Enter two words
2️⃣ DP matrix fills dynamically
3️⃣ Each step is highlighted with operation color
4️⃣ Final edit distance calculated
5️⃣ Attack power = max(1, 10 - edit_distance)
6️⃣ Duel results displayed

🎬 Algorithm → Visualization → Game Action → Learning

📈 Algorithm Complexity
Complexity Type	Value
Time	O(n × m)
Space	O(n × m)
Optimized Space	O(min(n, m)) (not used due to visualization needs)

🔹 Word length limited to ≤10 characters for real-time performance.

🧠 Real-World Applications

✔ Spell Checking (Google, MS Word)
✔ DNA Sequence Analysis
✔ NLP & Chatbots (auto-correction)
✔ Plagiarism Detection
✔ Cybersecurity (password similarity detection)

📌 Future Enhancements

⏩ Auto-play animation mode

⌨ Graphical word input (text box)

🔉 Sound/audio effects

🧑‍🤝‍🧑 Multiplayer mode

📊 Export gameplay history for analysis

👨‍💻 Author
Name	Roll No	Course	Instructor
Your Name	Your Roll No	Analysis of Algorithms	Instructor Name
📚 References

Cormen et al. (2009). Introduction to Algorithms. MIT Press.

Levenshtein, V. (1966). Binary codes capable of correcting deletions, insertions, and reversals.

Gusfield, D. (1997). Algorithms on Strings, Trees and Sequences.

Jurafsky & Martin (2008). Speech and Language Processing.

🙌 Acknowledgement

This project was developed as part of the Analysis of Algorithms course, following the structured 5-phase development process, including algorithm study, implementation, performance analysis, real-world impact, and report presentation.

🎉 Final Notes

“Turning theory into experience — one algorithm at a time.”
⭐ If you like this project or found it educational, feel free to star ⭐ the repo!
