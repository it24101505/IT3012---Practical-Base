import random
import tkinter as tk

from agent import SimpleReflexAgent, ModelBasedAgent


class VisualGridHuntGame:
    def __init__(self, width=12, height=12, num_food=8, custom_walls=None):

        self.width = width
        self.height = height

        # Actual environment state
        self.agent_pos = [0, 0]
        self.agent_direction = "Right"

        # ----------------------------------------------------------
        # Walls
        # ----------------------------------------------------------

        if custom_walls is not None:
            self.walls = set(custom_walls)
        else:
            self.walls = {
                (2, 2),
                (2, 3),
                (5, 5),
                (6, 5),
                (3, 7)
            }

        # ----------------------------------------------------------
        # Food
        # ----------------------------------------------------------

        self.food_positions = set()

        while len(self.food_positions) < num_food:

            fx = random.randint(0, self.width - 1)
            fy = random.randint(0, self.height - 1)

            if (
                (fx, fy) != (0, 0)
                and (fx, fy) not in self.walls
            ):
                self.food_positions.add((fx, fy))

        self.score = 0
        self.steps = 0

    # ==============================================================
    # PARTIALLY OBSERVABLE PERCEPT
    # ==============================================================

    def get_percept(self):
        """
        Returns only local information.

        The agent does NOT receive:
        - exact global position
        - complete grid
        - complete wall layout

        It receives:
        - wall_ahead
        - food_here
        - left_blocked
        """

        x, y = self.agent_pos

        # ----------------------------------------------------------
        # Position directly ahead
        # ----------------------------------------------------------

        if self.agent_direction == "Right":
            forward = (x + 1, y)

        elif self.agent_direction == "Left":
            forward = (x - 1, y)

        elif self.agent_direction == "Up":
            forward = (x, y + 1)

        else:
            forward = (x, y - 1)

        # ----------------------------------------------------------
        # Position to the left
        # ----------------------------------------------------------

        if self.agent_direction == "Right":
            left = (x, y + 1)

        elif self.agent_direction == "Left":
            left = (x, y - 1)

        elif self.agent_direction == "Up":
            left = (x - 1, y)

        else:
            left = (x + 1, y)

        # ----------------------------------------------------------
        # Check boundaries
        # ----------------------------------------------------------

        forward_outside = not (
            0 <= forward[0] < self.width
            and 0 <= forward[1] < self.height
        )

        left_outside = not (
            0 <= left[0] < self.width
            and 0 <= left[1] < self.height
        )

        # ----------------------------------------------------------
        # Local percept
        # ----------------------------------------------------------

        wall_ahead = (
            forward_outside
            or forward in self.walls
        )

        left_blocked = (
            left_outside
            or left in self.walls
        )

        food_here = (
            tuple(self.agent_pos)
            in self.food_positions
        )

        return {
            "wall_ahead": wall_ahead,
            "food_here": food_here,
            "left_blocked": left_blocked
        }

    # ==============================================================
    # EXECUTE ACTION
    # ==============================================================

    def execute_action(self, action):

        self.steps += 1

        # ----------------------------------------------------------
        # Eat
        # ----------------------------------------------------------

        if action == "Eat":

            current_position = tuple(self.agent_pos)

            if current_position in self.food_positions:

                self.food_positions.remove(
                    current_position
                )

                self.score += 20

            return

        # ----------------------------------------------------------
        # Turn Left
        # ----------------------------------------------------------

        if action == "TurnLeft":

            if self.agent_direction == "Right":
                self.agent_direction = "Up"

            elif self.agent_direction == "Up":
                self.agent_direction = "Left"

            elif self.agent_direction == "Left":
                self.agent_direction = "Down"

            else:
                self.agent_direction = "Right"

            return

        # ----------------------------------------------------------
        # Turn Right
        # ----------------------------------------------------------

        if action == "TurnRight":

            if self.agent_direction == "Right":
                self.agent_direction = "Down"

            elif self.agent_direction == "Down":
                self.agent_direction = "Left"

            elif self.agent_direction == "Left":
                self.agent_direction = "Up"

            else:
                self.agent_direction = "Right"

            return

        # ----------------------------------------------------------
        # Move Forward
        # ----------------------------------------------------------

        if action == "MoveForward":

            new_pos = list(self.agent_pos)

            if self.agent_direction == "Right":
                new_pos[0] += 1

            elif self.agent_direction == "Left":
                new_pos[0] -= 1

            elif self.agent_direction == "Up":
                new_pos[1] += 1

            elif self.agent_direction == "Down":
                new_pos[1] -= 1

            # Boundary collision
            if not (
                0 <= new_pos[0] < self.width
                and 0 <= new_pos[1] < self.height
            ):

                self.score -= 5
                return

            # Wall collision
            if tuple(new_pos) in self.walls:

                self.score -= 5
                return

            # Move
            self.agent_pos = new_pos

            # Automatically collect food
            if tuple(self.agent_pos) in self.food_positions:

                self.food_positions.remove(
                    tuple(self.agent_pos)
                )

                self.score += 20

    # ==============================================================
    # CHECK GAME END
    # ==============================================================

    def is_done(self):

        return (
            len(self.food_positions) == 0
            or self.steps >= 100
        )


# ==================================================================
# GUI
# ==================================================================

class GridGameGUI:

    def __init__(self, root, width=12, height=12, num_food=8):

        self.root = root

        self.root.title(
            "IT3012 - Practical 02 - Agent Architectures"
        )

        # ----------------------------------------------------------
        # Environment
        # ----------------------------------------------------------

        self.env = VisualGridHuntGame(
            width=width,
            height=height,
            num_food=num_food
        )

        # ----------------------------------------------------------
        # SELECT AGENT
        #
        # Change to "SIMPLE" if you want to test Simple Reflex.
        # Change to "MODEL" to test Model-Based Agent.
        # ----------------------------------------------------------

        self.agent_type = "MODEL"

        if self.agent_type == "SIMPLE":

            self.agent = SimpleReflexAgent()

        else:

            self.agent = ModelBasedAgent()

        # ----------------------------------------------------------
        # Canvas
        # ----------------------------------------------------------

        self.cell_size = 45

        canvas_width = (
            self.env.width
            * self.cell_size
        )

        canvas_height = (
            self.env.height
            * self.cell_size
        )

        self.canvas = tk.Canvas(
            root,
            width=canvas_width,
            height=canvas_height,
            bg="white"
        )

        self.canvas.pack()

        # ----------------------------------------------------------
        # Information label
        # ----------------------------------------------------------

        self.label = tk.Label(
            root,
            text=(
                f"Agent: {self.agent_type}"
                f" | Direction: "
                f"{self.env.agent_direction}"
                f" | Score: 0"
                f" | Steps: 0"
            ),
            font=("Arial", 13)
        )

        self.label.pack(
            pady=10
        )

        # ----------------------------------------------------------
        # Start button
        # ----------------------------------------------------------

        self.button = tk.Button(
            root,
            text="Start Simulation",
            command=self.run_loop,
            font=("Arial", 12)
        )

        self.button.pack(
            pady=5
        )

        # Draw initial grid
        self.draw_grid()

    # ==============================================================
    # DRAW GRID
    # ==============================================================

    def draw_grid(self):

        self.canvas.delete("all")

        # ----------------------------------------------------------
        # Draw grid
        # ----------------------------------------------------------

        for x in range(self.env.width):

            for y in range(self.env.height):

                x1 = (
                    x
                    * self.cell_size
                )

                y1 = (
                    self.env.height
                    - 1
                    - y
                ) * self.cell_size

                x2 = (
                    x1
                    + self.cell_size
                )

                y2 = (
                    y1
                    + self.cell_size
                )

                fill_color = "white"

                if (x, y) in self.env.walls:

                    fill_color = "gray"

                self.canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill=fill_color,
                    outline="black"
                )

        # ----------------------------------------------------------
        # Draw food
        # ----------------------------------------------------------

        for fx, fy in self.env.food_positions:

            x1 = (
                fx
                * self.cell_size
                + 12
            )

            y1 = (
                (
                    self.env.height
                    - 1
                    - fy
                )
                * self.cell_size
                + 12
            )

            x2 = (
                fx
                * self.cell_size
                + self.cell_size
                - 12
            )

            y2 = (
                (
                    self.env.height
                    - 1
                    - fy
                )
                * self.cell_size
                + self.cell_size
                - 12
            )

            self.canvas.create_oval(
                x1,
                y1,
                x2,
                y2,
                fill="orange"
            )

        # ----------------------------------------------------------
        # Draw agent
        # ----------------------------------------------------------

        ax, ay = self.env.agent_pos

        x1 = (
            ax
            * self.cell_size
            + 5
        )

        y1 = (
            (
                self.env.height
                - 1
                - ay
            )
            * self.cell_size
            + 5
        )

        x2 = (
            ax
            * self.cell_size
            + self.cell_size
            - 5
        )

        y2 = (
            (
                self.env.height
                - 1
                - ay
            )
            * self.cell_size
            + self.cell_size
            - 5
        )

        self.canvas.create_oval(
            x1,
            y1,
            x2,
            y2,
            fill="blue"
        )

        # ----------------------------------------------------------
        # Direction text
        # ----------------------------------------------------------

        self.canvas.create_text(
            (
                ax
                * self.cell_size
                + self.cell_size / 2
            ),
            (
                (
                    self.env.height
                    - 1
                    - ay
                )
                * self.cell_size
                + self.cell_size / 2
            ),
            text=self.env.agent_direction,
            fill="white",
            font=("Arial", 8, "bold")
        )

    # ==============================================================
    # RUN SIMULATION
    # ==============================================================

    def run_loop(self):

        self.button.config(
            state="disabled"
        )

        def step():

            if not self.env.is_done():

                # --------------------------------------------------
                # 1. Get partial percept
                # --------------------------------------------------

                percept = self.env.get_percept()

                # --------------------------------------------------
                # 2. Agent decides action
                # --------------------------------------------------

                action = self.agent.sense_and_act(
                    percept
                )

                # --------------------------------------------------
                # 3. Execute action
                # --------------------------------------------------

                self.env.execute_action(
                    action
                )

                # --------------------------------------------------
                # 4. Redraw
                # --------------------------------------------------

                self.draw_grid()

                # --------------------------------------------------
                # 5. Display memory
                # --------------------------------------------------

                memory_text = ""

                if self.agent_type == "MODEL":

                    memory_count = len(
                        getattr(
                            self.agent,
                            "visited_cells",
                            set()
                        )
                    )

                    memory_text = (
                        f" | Memory: {memory_count}"
                    )

                # --------------------------------------------------
                # Update information
                # --------------------------------------------------

                self.label.config(
                    text=(
                        f"Agent: {self.agent_type}"
                        f" | Action: {action}"
                        f" | Direction: "
                        f"{self.env.agent_direction}"
                        f" | Score: {self.env.score}"
                        f" | Steps: {self.env.steps}"
                        f"{memory_text}"
                    )
                )

                # Continue simulation
                self.root.after(
                    300,
                    step
                )

            else:

                # --------------------------------------------------
                # Simulation finished
                # --------------------------------------------------

                self.label.config(
                    text=(
                        f"Finished!"
                        f" | Agent: {self.agent_type}"
                        f" | Score: {self.env.score}"
                        f" | Steps: {self.env.steps}"
                    )
                )

                self.button.config(
                    state="normal"
                )

        step()


# ==================================================================
# MAIN
# ==================================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = GridGameGUI(
        root,
        width=12,
        height=12,
        num_food=8
    )

    root.mainloop()