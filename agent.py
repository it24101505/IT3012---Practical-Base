class SimpleReflexAgent:
    """
    Simple Reflex Agent.

    Uses only the current percept.
    It does not maintain internal memory.
    """

    def sense_and_act(self, percept):

        # IF food_here THEN Eat
        if percept["food_here"]:
            return "Eat"

        # IF wall_ahead THEN TurnLeft
        if percept["wall_ahead"]:
            return "TurnLeft"

        # ELSE MoveForward
        return "MoveForward"


class ModelBasedAgent:
    """
    Model-Based Agent.

    Maintains an internal state consisting of:
    - estimated position
    - current direction
    - previously visited states
    - last action

    The agent uses its internal memory together with
    the current percept to choose an action.
    """

    def __init__(self):

        # Internal memory
        self.visited_cells = set()

        # Last action performed
        self.last_action = None

        # Agent's internal estimate of its position
        self.internal_position = [0, 0]

        # Agent's internal estimate of its direction
        self.direction = "Right"

    def sense_and_act(self, percept):

        # =========================================================
        # UPDATE INTERNAL STATE
        # =========================================================

        current_state = (
            tuple(self.internal_position),
            self.direction
        )

        self.visited_cells.add(current_state)

        # =========================================================
        # RULE 1
        # IF food is here THEN Eat
        # =========================================================

        if percept["food_here"]:

            action = "Eat"

            self.last_action = action

            return action

        # =========================================================
        # RULE 2
        # IF wall ahead AND left is blocked THEN TurnRight
        # =========================================================

        if percept["wall_ahead"]:

            if percept["left_blocked"]:

                action = "TurnRight"

            # =====================================================
            # RULE 3
            # IF wall ahead AND left is free THEN TurnLeft
            # =====================================================

            else:

                action = "TurnLeft"

        # =========================================================
        # RULE 4
        # IF no wall ahead THEN MoveForward
        # =========================================================

        else:

            action = "MoveForward"

        # =========================================================
        # UPDATE INTERNAL MODEL
        # =========================================================

        self.update_internal_model(action, percept)

        # Remember last action
        self.last_action = action

        return action

    def update_internal_model(self, action, percept):
        """
        Update the internal state after selecting an action.

        This represents the agent's internal transition model.
        """

        # ---------------------------------------------------------
        # Turn Left
        # ---------------------------------------------------------

        if action == "TurnLeft":

            if self.direction == "Right":
                self.direction = "Up"

            elif self.direction == "Up":
                self.direction = "Left"

            elif self.direction == "Left":
                self.direction = "Down"

            elif self.direction == "Down":
                self.direction = "Right"

        # ---------------------------------------------------------
        # Turn Right
        # ---------------------------------------------------------

        elif action == "TurnRight":

            if self.direction == "Right":
                self.direction = "Down"

            elif self.direction == "Down":
                self.direction = "Left"

            elif self.direction == "Left":
                self.direction = "Up"

            elif self.direction == "Up":
                self.direction = "Right"

        # ---------------------------------------------------------
        # Move Forward
        # ---------------------------------------------------------

        elif action == "MoveForward":

            # Only update the estimated position when
            # the percept indicates that the path ahead is free.

            if not percept["wall_ahead"]:

                if self.direction == "Right":
                    self.internal_position[0] += 1

                elif self.direction == "Left":
                    self.internal_position[0] -= 1

                elif self.direction == "Up":
                    self.internal_position[1] += 1

                elif self.direction == "Down":
                    self.internal_position[1] -= 1


class SearchAgent:
    """
    Compatibility class for Practical 03.

    This class is retained so that the previous practical
    does not break when switching between branches.
    """

    def __init__(self):

        self.plan = []

        self.active_algo = "BFS"

    def sense_and_act(self, percept):

        return "Stay"