import heapq
import math


class SearchAgent:
    """A search-based agent that uses A* Search to find food."""

    def __init__(self, active_algo='AStar'):
        self.active_algo = active_algo
        self.plan = []

    def manhattan_distance(self, pos, goal):
        """
        Calculate Manhattan distance between two positions.

        Manhattan Distance = |x1 - x2| + |y1 - y2|
        """
        return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

    def euclidean_distance(self, pos, goal):
        """
        Calculate Euclidean distance between two positions.

        Euclidean Distance =
        sqrt((x1 - x2)^2 + (y1 - y2)^2)
        """
        return math.sqrt(
            (pos[0] - goal[0]) ** 2 +
            (pos[1] - goal[1]) ** 2
        )

    def astar_search(
        self,
        start_pos,
        goal_pos,
        walls,
        grid_size,
        heuristic_type='manhattan'
    ):
        """
        Perform A* Search from start position to goal position.

        A* evaluation:
        f(n) = g(n) + h(n)

        g(n) = cost from start to current node
        h(n) = estimated cost from current node to goal
        """

        priority_queue = []
        reached_states = set()

        width, height = grid_size

        if heuristic_type == 'euclidean':
            heuristic = self.euclidean_distance
        else:
            heuristic = self.manhattan_distance

        start_pos = tuple(start_pos)
        goal_pos = tuple(goal_pos)
        walls = set(tuple(wall) for wall in walls)

        # Initial node
        g_cost = 0
        h_cost = heuristic(start_pos, goal_pos)
        f_cost = g_cost + h_cost

        heapq.heappush(
            priority_queue,
            (
                f_cost,
                g_cost,
                start_pos,
                []
            )
        )

        # Four-way movement
        directions = [
            ('Up', (0, 1)),
            ('Down', (0, -1)),
            ('Left', (-1, 0)),
            ('Right', (1, 0))
        ]

        while priority_queue:

            f_cost, g_cost, current_pos, path_taken = heapq.heappop(
                priority_queue
            )

            # Goal reached
            if current_pos == goal_pos:
                return path_taken

            # Skip already explored states
            if current_pos in reached_states:
                continue

            reached_states.add(current_pos)

            # Explore neighbouring cells
            for action, (dx, dy) in directions:

                new_x = current_pos[0] + dx
                new_y = current_pos[1] + dy

                new_pos = (new_x, new_y)

                # Check boundaries
                if not (
                    0 <= new_x < width
                    and 0 <= new_y < height
                ):
                    continue

                # Check walls
                if new_pos in walls:
                    continue

                # Check already reached states
                if new_pos in reached_states:
                    continue

                # Calculate new costs
                new_g_cost = g_cost + 1
                new_h_cost = heuristic(new_pos, goal_pos)
                new_f_cost = new_g_cost + new_h_cost

                new_path = path_taken + [action]

                heapq.heappush(
                    priority_queue,
                    (
                        new_f_cost,
                        new_g_cost,
                        new_pos,
                        new_path
                    )
                )

        # No path found
        return []

    def sense_and_act(self, percept):
        """
        Select an action based on the current percept.
        """

        if self.active_algo == 'AStar':

            current_pos = tuple(percept['agent_pos'])

            food_positions = percept.get(
                'food_positions',
                []
            )

            # No food remaining
            if not food_positions:
                return 'Stay'

            # Find the closest food using Manhattan distance
            goal_pos = min(
                food_positions,
                key=lambda food: self.manhattan_distance(
                    current_pos,
                    food
                )
            )

            walls = set(
                tuple(wall)
                for wall in percept['walls']
            )

            grid_size = percept['grid_size']

            # Calculate A* path
            self.plan = self.astar_search(
                current_pos,
                goal_pos,
                walls,
                grid_size,
                heuristic_type='manhattan'
            )

            # Execute the next planned action
            if self.plan:
                return self.plan.pop(0)

        return 'Stay'


def test_heuristics():
    """
    Testing checkpoint for Practical 04.
    """

    agent = SearchAgent()

    start = (0, 0)
    goal = (3, 4)

    print(
        "Manhattan Distance:",
        agent.manhattan_distance(start, goal)
    )

    print(
        "Euclidean Distance:",
        agent.euclidean_distance(start, goal)
    )


if __name__ == "__main__":
    test_heuristics()