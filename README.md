# MazeTrace: A BFS-Based Shortest Path Visualizer

> A graphical maze solver that visualizes the Breadth First Search algorithm in real time, built with Python and pygame as a DAA Mini Project.

---

## Abstract

This project presents the design and development of a graphical maze solver visualizer using the Python programming language. The application enables users to observe the complete solving process of a predefined maze through an interactive desktop interface and instantly visualize how the Breadth First Search algorithm finds the shortest path between a start node and an end node. By combining Python's straightforward programming model with the pygame library's real time rendering framework, the project demonstrates that algorithm visualization is not limited to theoretical explanation but is fully capable of powering interactive, step by step educational software tools.

---

## Features

- 20x20 grid maze with clean cell rendering
- Predefined maze loads automatically on startup
- Step by step BFS animation showing exploration in real time
- Shortest path reconstruction and display
- Live status panel showing algorithm state and path length
- Keyboard controls for a smooth interactive experience

---

## Color Legend

| Color | Meaning |
|-------|---------|
| 🟢 Green | Start node |
| 🔴 Red | End node |
| ⬛ Black | Wall |
| ⬜ White | Open path |
| 🔵 Blue | BFS visited cells |
| 🟡 Yellow | Shortest path |

---

## Controls

| Key | Action |
|-----|--------|
| `SPACE` | Start solving the maze |
| `R` | Reset the maze |
| `ESC` | Quit the application |

---

## Tech Stack

- **Language:** Python 3
- **Library:** pygame
- **Algorithm:** Breadth First Search (BFS)

---

## Installation

**Step 1 — Clone the repository**
```bash
git clone https://github.com/your-username/mazetrace.git
cd mazetrace
```

**Step 2 — Install pygame**
```bash
pip install pygame
```

**Step 3 — Run the program**
```bash
python3 maze_solver.py
```

---

## How It Works

The maze is represented as a 20x20 grid where each cell is categorized as either an open path, a wall, a start node, or an end node. When the solver is executed, the BFS algorithm begins from the start node and explores all neighboring cells in a queue based order, ensuring that the shortest possible path is always discovered first. The exploration process is animated step by step, with visited cells highlighted in blue and the final shortest path marked in yellow.

The application is built with a clear separation between the maze representation layer, the BFS algorithm layer, and the pygame rendering layer. This ensures that the algorithm logic remains clean and traceable while the visualization layer handles all display and user interaction concerns.

---

## Project Structure

```
mazetrace/
│
└── maze_solver.py       # Main application file
```

---

## Algorithm

The BFS algorithm guarantees the shortest path in an unweighted grid. It works by:

1. Starting from the start node and adding it to a queue
2. Exploring all valid neighboring cells level by level
3. Tracking visited nodes to avoid revisiting
4. Recording the parent of each visited node
5. Reconstructing the shortest path from end to start using the parent map once the end node is reached

---

## Course Info

- **Subject:** Design and Analysis of Algorithms (DAA)
- **Project Title:** MazeTrace: A BFS-Based Shortest Path Visualizer
- **Language:** Python 3
- **Platform:** Kali Linux / Any OS with Python 3 and pygame

---

## License

This project is open source and available under the [MIT License](LICENSE).
