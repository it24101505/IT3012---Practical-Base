import random
import tkinter as tk


class VisualGridHuntGame:
    """A flexible Pacman-style grid environment with support for configurable opponents and larger scales."""

    def __init__(self, width=10, height=10, num_food=10, num_opponents=2, custom_walls=None):
        self.width = width
        self.height = height
        self.agent_pos = [0, 0]

        if custom_walls is not None:
            self.walls = set(custom_walls)
        else:
            self.walls = {(2, 2), (2, 3), (5, 5), (6, 5), (3, 7)}

        self.food_positions = set()

        while len(self.food_positions) < num_food:
            fx = random.randint(0, self.width - 1)
            fy = random.randint(0, self.height - 1)

            if (fx, fy) != (0, 0) and (fx, fy) not in self.walls:
                self.food_positions.add((fx, fy))

        self.opponents = []

        while len(self.opponents) < num_opponents:
            ox = random.randint(0, self.width - 1)
            oy = random.randint(0, self.height - 1)

            if (
                (ox, oy) != (0, 0)
                and (ox, oy) not in self.walls
                and (ox, oy) not in self.food_positions
            ):
                self.opponents.append([ox, oy])

        self.score = 0
        self.steps = 0
        self.collision = False

        # Toxic trap generation
        self.toxic_traps = set()

        while len(self.toxic_traps) < 5:

            tx = random.randint(0, self.width - 1)
            ty = random.randint(0, self.height - 1)

            if (
                (tx, ty) != (0, 0)
                and (tx, ty) not in self.walls
                and (tx, ty) not in self.food_positions
                and [tx, ty] not in self.opponents
            ):
                self.toxic_traps.add((tx, ty))

    def get_percept(self) -> dict:

        x, y = self.agent_pos

        nearby_food = []
        nearby_opponents = []

        for fx, fy in self.food_positions:
            if abs(fx-x) <= 1 and abs(fy-y) <= 1:
                nearby_food.append((fx, fy))

        for ox, oy in self.opponents:
            if abs(ox-x) <= 1 and abs(oy-y) <= 1:
                nearby_opponents.append((ox, oy))

        return {
            "agent_pos": list(self.agent_pos),
            "nearby_food": nearby_food,
            "nearby_opponents": nearby_opponents,
            "smells_toxin": tuple(self.agent_pos) in self.toxic_traps,
            "collision": self.collision,
            "score": self.score,
            "remaining_food": len(self.food_positions),
            "steps": self.steps
        }

    # NEW INTELLIGENT AGENT FUNCTION
    def choose_action(self):

        possible_actions = [
            "Up",
            "Down",
            "Left",
            "Right"
        ]

        best_action = None
        best_score = -9999

        for action in possible_actions:

            new_pos = list(self.agent_pos)

            if action == "Up":
                new_pos[1] = min(self.height - 1, new_pos[1] + 1)

            elif action == "Down":
                new_pos[1] = max(0, new_pos[1] - 1)

            elif action == "Left":
                new_pos[0] = max(0, new_pos[0] - 1)

            elif action == "Right":
                new_pos[0] = min(self.width - 1, new_pos[0] + 1)

            score = 0

            # Avoid walls
            if tuple(new_pos) in self.walls:
                score -= 100

            # Avoid traps
            if tuple(new_pos) in self.toxic_traps:
                score -= 50

            # Move towards food
            for food in self.food_positions:

                distance = (
                    abs(food[0] - new_pos[0])
                    +
                    abs(food[1] - new_pos[1])
                )

                score += max(0, 20 - distance)

            # Avoid opponents
            for opponent in self.opponents:

                distance = (
                    abs(opponent[0] - new_pos[0])
                    +
                    abs(opponent[1] - new_pos[1])
                )

                if distance <= 1:
                    score -= 70

            if score > best_score:

                best_score = score
                best_action = action

        return best_action

    def execute_action(self, action: str):

        self.steps += 1

        new_pos = list(self.agent_pos)

        if action == "Up":
            new_pos[1] = min(self.height - 1, new_pos[1] + 1)

        elif action == "Down":
            new_pos[1] = max(0, new_pos[1] - 1)

        elif action == "Left":
            new_pos[0] = max(0, new_pos[0] - 1)

        elif action == "Right":
            new_pos[0] = min(self.width - 1, new_pos[0] + 1)

        if tuple(new_pos) in self.walls:

            self.score -= 5

        else:

            self.agent_pos = new_pos

        # Toxic trap penalty
        if tuple(self.agent_pos) in self.toxic_traps:

            self.score -= 15

        # Food collection
        if tuple(self.agent_pos) in self.food_positions:

            self.food_positions.remove(tuple(self.agent_pos))
            self.score += 20

        # Collision with opponent
        for op in self.opponents:

            if op == self.agent_pos:

                self.score -= 50
                self.collision = True

        # Move opponents randomly
        for op in self.opponents:

            possible_moves = []

            directions = {
                "Up": [op[0], op[1]+1],
                "Down": [op[0], op[1]-1],
                "Left": [op[0]-1, op[1]],
                "Right": [op[0]+1, op[1]],
                "Stay": op
            }

            for move_pos in directions.values():

                if (
                    0 <= move_pos[0] < self.width
                    and 0 <= move_pos[1] < self.height
                    and tuple(move_pos) not in self.walls
                ):
                    possible_moves.append(move_pos)

            if possible_moves:

                new_op = random.choice(possible_moves)

                op[0] = new_op[0]
                op[1] = new_op[1]

            if op == self.agent_pos:

                self.score -= 50
                self.collision = True

    def is_done(self):

        return (
            len(self.food_positions) == 0
            or self.steps >= 60
            or self.collision
        )


class GridGameGUI:

    def __init__(self, root, width=10, height=10, num_food=12, num_opponents=2, walls=None):

        self.root = root
        self.root.title("IT3012 - Scalable Multi-Agent Grid Hunt")

        self.env = VisualGridHuntGame(
            width=width,
            height=height,
            num_food=num_food,
            num_opponents=num_opponents,
            custom_walls=walls
        )

        max_canvas_dim = 600

        self.cell_size = max(
            20,
            min(
                max_canvas_dim // self.env.width,
                max_canvas_dim // self.env.height
            )
        )

        canvas_w = self.env.width * self.cell_size
        canvas_h = self.env.height * self.cell_size

        self.canvas = tk.Canvas(
            root,
            width=canvas_w,
            height=canvas_h,
            bg="white"
        )

        self.canvas.pack()

        self.label = tk.Label(
            root,
            text="Score: 0 | Steps: 0",
            font=("Arial", 14)
        )

        self.label.pack(pady=10)

        self.btn = tk.Button(
            root,
            text="Start Simulation",
            command=self.run_loop,
            font=("Arial", 12)
        )

        self.btn.pack(pady=5)

        self.draw_grid()

    def draw_grid(self):

        self.canvas.delete("all")

        # Draw grid cells
        for x in range(self.env.width):

            for y in range(self.env.height):

                x1 = x * self.cell_size
                y1 = (self.env.height - 1 - y) * self.cell_size

                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                color = "white"

                if (x, y) in self.env.walls:

                    color = "gray"

                elif (x, y) in self.env.toxic_traps:

                    color = "purple"

                self.canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill=color,
                    outline="black"
                )

        # Draw food

        for fx, fy in self.env.food_positions:

            self.canvas.create_oval(
                fx*self.cell_size+10,
                (self.env.height-1-fy)*self.cell_size+10,
                fx*self.cell_size+self.cell_size-10,
                (self.env.height-1-fy)*self.cell_size+self.cell_size-10,
                fill="orange"
            )

        # Draw opponents

        for ox, oy in self.env.opponents:

            self.canvas.create_rectangle(
                ox*self.cell_size+10,
                (self.env.height-1-oy)*self.cell_size+10,
                ox*self.cell_size+self.cell_size-10,
                (self.env.height-1-oy)*self.cell_size+self.cell_size-10,
                fill="red"
            )

        # Draw agent

        ax, ay = self.env.agent_pos

        self.canvas.create_oval(
            ax*self.cell_size+5,
            (self.env.height-1-ay)*self.cell_size+5,
            ax*self.cell_size+self.cell_size-5,
            (self.env.height-1-ay)*self.cell_size+self.cell_size-5,
            fill="blue"
        )

    def run_loop(self):

        self.btn.config(state="disabled")

        def step():

            if not self.env.is_done():

                # CHANGED:
                # Random action replaced by intelligent agent

                action = self.env.choose_action()

                self.env.execute_action(action)

                self.draw_grid()

                self.label.config(
                    text=f"Score: {self.env.score} | Steps: {self.env.steps}"
                )

                self.root.after(250, step)

            else:

                self.label.config(
                    text=f"Game Finished! Score: {self.env.score}"
                )

                self.btn.config(state="normal")

        step()


if __name__ == "__main__":

    root = tk.Tk()

    app = GridGameGUI(
        root,
        width=12,
        height=12,
        num_food=15,
        num_opponents=2
    )

    root.mainloop()