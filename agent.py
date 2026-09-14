from collections import deque
import heapq


class SearchAgent:
    def __init__(self):
        self.plan = []
        self.active_algo = 'BFS'

    def manhattan_distance(self, pos, goal):
        return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

    def bfs_search(self, start_pos, goal_pos, walls, grid_size):
        queue = deque()
        reached = set()

        start_pos = tuple(start_pos)
        goal_pos = tuple(goal_pos)
        walls = set(tuple(wall) for wall in walls)

        width, height = grid_size

        queue.append((start_pos, []))
        reached.add(start_pos)

        directions = [
            ('Up', (0, 1)),
            ('Down', (0, -1)),
            ('Left', (-1, 0)),
            ('Right', (1, 0))
        ]

        while queue:
            current_pos, path = queue.popleft()

            if current_pos == goal_pos:
                return path

            for action, (dx, dy) in directions:
                new_pos = (
                    current_pos[0] + dx,
                    current_pos[1] + dy
                )

                if not (
                    0 <= new_pos[0] < width
                    and 0 <= new_pos[1] < height
                ):
                    continue

                if new_pos in walls:
                    continue

                if new_pos in reached:
                    continue

                reached.add(new_pos)

                new_path = path + [action]

                queue.append(
                    (new_pos, new_path)
                )

        return []

    def dfs_search(self, start_pos, goal_pos, walls, grid_size):
        stack = []
        reached = set()

        start_pos = tuple(start_pos)
        goal_pos = tuple(goal_pos)
        walls = set(tuple(wall) for wall in walls)

        width, height = grid_size

        stack.append((start_pos, []))
        reached.add(start_pos)

        directions = [
            ('Up', (0, 1)),
            ('Down', (0, -1)),
            ('Left', (-1, 0)),
            ('Right', (1, 0))
        ]

        while stack:
            current_pos, path = stack.pop()

            if current_pos == goal_pos:
                return path

            for action, (dx, dy) in reversed(directions):
                new_pos = (
                    current_pos[0] + dx,
                    current_pos[1] + dy
                )

                if not (
                    0 <= new_pos[0] < width
                    and 0 <= new_pos[1] < height
                ):
                    continue

                if new_pos in walls:
                    continue

                if new_pos in reached:
                    continue

                reached.add(new_pos)

                new_path = path + [action]

                stack.append(
                    (new_pos, new_path)
                )

        return []

    def ucs_search(self, start_pos, goal_pos, walls, grid_size):
        priority_queue = []
        reached = set()

        start_pos = tuple(start_pos)
        goal_pos = tuple(goal_pos)
        walls = set(tuple(wall) for wall in walls)

        width, height = grid_size

        heapq.heappush(
            priority_queue,
            (0, start_pos, [])
        )

        directions = [
            ('Up', (0, 1)),
            ('Down', (0, -1)),
            ('Left', (-1, 0)),
            ('Right', (1, 0))
        ]

        while priority_queue:
            cost, current_pos, path = heapq.heappop(
                priority_queue
            )

            if current_pos in reached:
                continue

            reached.add(current_pos)

            if current_pos == goal_pos:
                return path

            for action, (dx, dy) in directions:
                new_pos = (
                    current_pos[0] + dx,
                    current_pos[1] + dy
                )

                if not (
                    0 <= new_pos[0] < width
                    and 0 <= new_pos[1] < height
                ):
                    continue

                if new_pos in walls:
                    continue

                if new_pos in reached:
                    continue

                new_cost = cost + 1
                new_path = path + [action]

                heapq.heappush(
                    priority_queue,
                    (
                        new_cost,
                        new_pos,
                        new_path
                    )
                )

        return []

    def sense_and_act(self, percept):
        if not self.plan:

            current_pos = tuple(
                percept['agent_pos']
            )

            food_positions = percept.get(
                'all_food',
                []
            )

            if not food_positions:
                return 'Stay'

            goal_pos = min(
                food_positions,
                key=lambda food:
                self.manhattan_distance(
                    current_pos,
                    food
                )
            )

            walls = percept['walls']
            grid_size = percept['grid_size']

            if self.active_algo == 'BFS':

                self.plan = self.bfs_search(
                    current_pos,
                    goal_pos,
                    walls,
                    grid_size
                )

            elif self.active_algo == 'DFS':

                self.plan = self.dfs_search(
                    current_pos,
                    goal_pos,
                    walls,
                    grid_size
                )

            elif self.active_algo == 'UCS':

                self.plan = self.ucs_search(
                    current_pos,
                    goal_pos,
                    walls,
                    grid_size
                )

        if self.plan:
            return self.plan.pop(0)

        return 'Stay'