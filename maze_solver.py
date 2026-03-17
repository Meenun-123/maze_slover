import pygame
import sys
from collections import deque

WINDOW_TITLE  = "Maze Solver – BFS Visualizer (DAA Mini Project)"
CELL_SIZE     = 32
COLS, ROWS    = 20, 20
SIDEBAR_W     = 260
WIN_W         = COLS * CELL_SIZE + SIDEBAR_W
WIN_H         = ROWS * CELL_SIZE

FPS           = 60
BFS_DELAY     = 18         

C_BG          = (18,  18,  28)
C_GRID_LINE   = (40,  40,  60)
C_WALL        = (20,  20,  30)
C_OPEN        = (245, 245, 255)
C_START       = (50,  200, 100)
C_END         = (220, 60,  60)
C_VISITED     = (80,  140, 220)
C_PATH        = (255, 210, 50)
C_SIDEBAR     = (24,  24,  40)
C_TEXT        = (200, 200, 230)
C_ACCENT      = (100, 160, 255)
C_BORDER      = (60,  60,  100)


OPEN  = 0
WALL  = 1
START = 2
END   = 3
DEFAULT_MAZE = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,2,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,1],
    [1,0,1,1,0,1,0,1,1,1,1,1,0,1,0,1,0,1,0,1],
    [1,0,1,0,0,0,0,1,0,0,0,1,0,1,0,0,0,1,0,1],
    [1,0,1,0,1,1,0,1,0,1,0,1,0,1,1,1,1,1,0,1],
    [1,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,0,1,0,1,1,1,1,1,1,1,1,0,1,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,1],
    [1,0,1,1,1,1,1,1,0,1,1,1,0,1,1,1,0,1,0,1],
    [1,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,0,0,1,1,1,0,1,1,1,1,1,1,1,0,1],
    [1,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,1,0,1],
    [1,0,1,0,1,1,1,1,0,1,1,1,1,1,0,1,0,1,0,1],
    [1,0,1,0,0,0,0,1,0,0,0,0,0,1,0,1,0,0,0,1],
    [1,0,1,1,1,1,0,1,1,1,1,1,0,1,0,1,1,1,0,1],
    [1,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,1,0,1],
    [1,1,1,0,0,1,1,1,1,1,1,1,0,1,1,1,0,1,0,1],
    [1,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,1,0,1],
    [1,0,1,0,0,0,1,0,1,1,0,0,1,1,1,1,0,0,3,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

def create_grid():
    """Deep-copy of the default maze so we can reset cleanly."""
    return [row[:] for row in DEFAULT_MAZE]


def find_cell(grid, kind):
    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c] == kind:
                return (r, c)
    return None


def bfs_solver(grid):
    """
    Generator – yields one step at a time so the caller can animate.
    Yields: ('visit', (r,c))  or  ('path', [(r,c), ...])  or  ('done', None)
    """
    start = find_cell(grid, START)
    end   = find_cell(grid, END)
    if not start or not end:
        yield ('done', None)
        return

    queue   = deque([start])
    visited = {start}
    parent  = {start: None}

    while queue:
        current = queue.popleft()

        if current == end:
            # Reconstruct path
            path, node = [], current
            while node is not None:
                path.append(node)
                node = parent[node]
            path.reverse()
            yield ('path', path)
            yield ('done', None)
            return

        r, c = current
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < ROWS and 0 <= nc < COLS:
                if (nr, nc) not in visited and grid[nr][nc] != WALL:
                    visited.add((nr, nc))
                    parent[(nr, nc)] = current
                    queue.append((nr, nc))

        if current != start:
            yield ('visit', current)

    
    yield ('done', None)


def cell_rect(r, c):
    return pygame.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)


def draw_grid(surface, grid, visited_cells, path_cells):
    for r in range(ROWS):
        for c in range(COLS):
            rect = cell_rect(r, c)
            val  = grid[r][c]

            if (r, c) in path_cells:
                colour = C_PATH
            elif (r, c) in visited_cells:
                colour = C_VISITED
            elif val == WALL:
                colour = C_WALL
            elif val == START:
                colour = C_START
            elif val == END:
                colour = C_END
            else:
                colour = C_OPEN

            pygame.draw.rect(surface, colour, rect)
            pygame.draw.rect(surface, C_GRID_LINE, rect, 1)


def draw_sidebar(surface, font_big, font_sm, state, path_len):
    x = COLS * CELL_SIZE
    sidebar = pygame.Rect(x, 0, SIDEBAR_W, WIN_H)
    pygame.draw.rect(surface, C_SIDEBAR, sidebar)
    pygame.draw.line(surface, C_BORDER, (x, 0), (x, WIN_H), 2)

    def txt(text, y, font=None, colour=C_TEXT, cx=None):
        font = font or font_sm
        surf = font.render(text, True, colour)
        if cx:
            surface.blit(surf, (cx - surf.get_width()//2, y))
        else:
            surface.blit(surf, (x + 16, y))

    cx = x + SIDEBAR_W // 2

    txt("BFS Maze Solver", 22, font_big, C_ACCENT, cx)
    txt("DAA Mini Project",  52, font_sm,  C_TEXT,   cx)

    pygame.draw.line(surface, C_BORDER, (x+16, 78), (x+SIDEBAR_W-16, 78), 1)

    legend = [
        (C_START,   "Start node"),
        (C_END,     "End node"),
        (C_WALL,    "Wall"),
        (C_OPEN,    "Open path"),
        (C_VISITED, "BFS visited"),
        (C_PATH,    "Shortest path"),
    ]
    ly = 92
    for colour, label in legend:
        pygame.draw.rect(surface, colour,   pygame.Rect(x+16, ly+2, 18, 18))
        pygame.draw.rect(surface, C_BORDER, pygame.Rect(x+16, ly+2, 18, 18), 1)
        surface.blit(font_sm.render(label, True, C_TEXT), (x+42, ly+2))
        ly += 26

    pygame.draw.line(surface, C_BORDER, (x+16, ly+6), (x+SIDEBAR_W-16, ly+6), 1)

  
    controls = [
        ("SPACE",  "Start / Pause"),
        ("R",      "Reset maze"),
        ("ESC",    "Quit"),
    ]
    cy = ly + 18
    txt("Controls", cy, font_sm, C_ACCENT)
    cy += 24
    for key, action in controls:
        ktxt = font_sm.render(f"[{key}]", True, C_PATH)
        surface.blit(ktxt, (x+16, cy))
        atxt = font_sm.render(action, True, C_TEXT)
        surface.blit(atxt, (x+16+ktxt.get_width()+6, cy))
        cy += 22

    pygame.draw.line(surface, C_BORDER, (x+16, cy+4), (x+SIDEBAR_W-16, cy+4), 1)

 
    cy += 16
    status_map = {
        'idle':    ("Ready",      C_TEXT),
        'running': ("Solving…",   C_ACCENT),
        'done':    ("Path Found!",C_START),
        'nopath':  ("No Path!",   C_END),
    }
    label, colour = status_map.get(state, ("?", C_TEXT))
    txt("Status:", cy, colour=C_TEXT)
    cy += 22
    txt(label, cy, font_big, colour, cx)

    if path_len and state == 'done':
        cy += 34
        txt(f"Path length: {path_len} cells", cy, colour=C_PATH, cx=cx)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIN_W, WIN_H))
    pygame.display.set_caption(WINDOW_TITLE)
    clock  = pygame.time.Clock()

    try:
        font_big = pygame.font.SysFont("segoeui",   20, bold=True)
        font_sm  = pygame.font.SysFont("segoeui",   16)
    except Exception:
        font_big = pygame.font.SysFont(None, 22, bold=True)
        font_sm  = pygame.font.SysFont(None, 17)

    grid          = create_grid()
    visited_cells = set()
    path_cells    = set()
    bfs_gen       = None
    state         = 'idle'  
    path_len      = 0
    last_step_ms  = 0

    running = True
    while running:
        now = pygame.time.get_ticks()

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                elif event.key == pygame.K_r:
                    grid          = create_grid()
                    visited_cells = set()
                    path_cells    = set()
                    bfs_gen       = None
                    state         = 'idle'
                    path_len      = 0

                elif event.key == pygame.K_SPACE:
                    if state in ('idle', 'done', 'nopath'):
                        # (re)start
                        visited_cells = set()
                        path_cells    = set()
                        bfs_gen       = bfs_solver(grid)
                        state         = 'running'
                        path_len      = 0
        if state == 'running' and bfs_gen and (now - last_step_ms) >= BFS_DELAY:
            last_step_ms = now
            try:
                event_type, data = next(bfs_gen)
                if event_type == 'visit':
                    visited_cells.add(data)
                elif event_type == 'path':
                    path_cells = set(data)
                    path_len   = len(data)
                    state      = 'done'
                elif event_type == 'done':
                    if state != 'done':
                        state = 'nopath'
            except StopIteration:
                if state != 'done':
                    state = 'nopath'

        screen.fill(C_BG)
        draw_grid(screen, grid, visited_cells, path_cells)
        draw_sidebar(screen, font_big, font_sm, state, path_len)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
