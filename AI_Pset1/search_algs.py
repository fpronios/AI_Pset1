import sys
import copy
import time
import math
import heapq
import argparse

FINFINITY = 5000
USAGE = "python puzzle8.py [bfs|idfs|astar|idastar]"

HARD_START =[2, 5, None, 
        1, 4, 8, 
        7, 3, 6]

GOAL = [1, 2, 3, 
        4, 5, 6, 
        7, 8, None]

EASY_START = [1, 2, 3, 
        4, None, 5, 
        7, 8, 6]

MIDDLE_START = [4, None, 1, 
         5, 8, 2, 
         7, 6, 3]

START_DICT = {"easy": EASY_START,
        "hard": HARD_START,
        "middle": MIDDLE_START}


class Node(object):
    def __init__(self, value):
        self.value = value
        self.cost = None
        self.total_cost = None
        self.parent = None

    def __repr__(self):
        return str(self.value)

    #XXX overwritten <=
    # heapq is faster than sorted
    
    def __le__(self, other):
        return self.total_cost <= other.total_cost


class PuzzleSearch(object):

    def __init__(self, start, goal):
        self.start = start
        self.goal = goal
        self.nodes = []
        self.maxnodes = 0
        self.maxelapsed = 0
        self.maxdepth = 0

    def _position_by_value(self, node, value):
        cells = int(math.sqrt(len(node)))
        row_idx = node.index(value) / cells
        col_idx = node.index(value) % cells
        return row_idx, col_idx

    def _move_left(self, node):
        row_idx, col_idx = self._position_by_value(node, None)
        cells = int(math.sqrt(len(node)))
        if col_idx != 0:
            newnode = copy.deepcopy(node)
            idx_old = cells * row_idx + col_idx
            idx_new = cells * row_idx + col_idx-1
            new_val = node[idx_new]
            newnode[idx_old] = new_val
            newnode[idx_new] = None
            return newnode

    def _move_right(self, node):
        row_idx, col_idx = self._position_by_value(node, None)
        cells = int(math.sqrt(len(node)))
        max_col = cells-1
        if col_idx != max_col:
            newnode = copy.deepcopy(node)
            idx_old = cells * row_idx + col_idx
            idx_new = cells * row_idx + col_idx+1
            new_val = node[idx_new]
            newnode[idx_old] = new_val
            newnode[idx_new] = None
            return newnode

    def _move_up(self, node):
        row_idx, col_idx = self._position_by_value(node, None)
        cells = int(math.sqrt(len(node)))
        if row_idx != 0:
            newnode = copy.deepcopy(node)
            idx_old = cells * row_idx + col_idx
            idx_new = cells * (row_idx-1) + col_idx
            new_val = node[idx_new]
            newnode[idx_old] = new_val
            newnode[idx_new] = None
            return newnode

    def _move_down(self, node):
        row_idx, col_idx = self._position_by_value(node, None)
        cells = int(math.sqrt(len(node)))
        max_row = cells-1
        if row_idx != max_row:
            newnode = copy.deepcopy(node)
            idx_old = cells * row_idx + col_idx
            idx_new = cells * (row_idx+1) + col_idx
            new_val = node[idx_new]
            newnode[idx_old] = new_val
            newnode[idx_new] = None
            return newnode

    def get_children(self, node):
        tmp_nodes = []
        new_node_list = []
        tmp_nodes.append(self._move_down(node))
        tmp_nodes.append(self._move_up(node))
        tmp_nodes.append(self._move_left(node))
        tmp_nodes.append(self._move_right(node))
        for new in tmp_nodes:
            if new:
                new_node_list.append(new)
        return new_node_list

    def _heuristic_manhatten(self, node, goal):
        """
        Example:
        N | 1 | 2
        3 | 4 | 5
        6 | 7 | 8
        1 | 2 | 5
        3 | 4 | 8
        6 | 7 | N
        == 0 + 1 + 1 + 0 + 0 + 1 + 0 + 0 + 1 = 4
        """
        ret = 0
        for i in node:
            # exclude None
            if not i:
                continue
            row_idx, col_idx = self._position_by_value(node, i)
            row_idx_goal, col_idx_goal = self._position_by_value(goal, i)
            ret += abs(row_idx_goal - row_idx) + abs(col_idx_goal - col_idx)
        return ret

    def _dfs_heuristic(self, node, limit):
        newlimit = FINFINITY
        node_list = [node]
        minimum = FINFINITY

        while node_list:
            node = node_list.pop(0)
            if node.total_cost > limit:
                return node, node.total_cost
            if node.value == self.goal.value:
                return node, node.total_cost

            tmp = self.get_children(node.value)
            tmp_nodes = []
            for i in tmp:
                obj_node = Node(i)
                obj_node.parent = node
                obj_node.cost = self._heuristic_manhatten(i, self.goal.value)
                obj_node.total_cost = obj_node.cost + node.total_cost
                tmp_nodes.append(obj_node)
                if newlimit < minimum:
                    minimum = newlimit
                node_list = node_list + tmp_nodes
                    
        return None, newlimit

    def _dfs_heuristic_rec(self, node, limit, depth):
        depth +=1
        if node.total_cost > limit:
            return node, node.total_cost
        if node.value == self.goal.value:
            return node, node.total_cost
        tmp = self.get_children(node.value)
        minimum = FINFINITY
        for i in tmp:
            obj_node = Node(i)
            obj_node.parent = node
            obj_node.cost = self._heuristic_manhatten(i, self.goal.value)
            obj_node.total_cost = obj_node.cost + node.total_cost
            self.maxnodes += 1
            ret, newlimit = self._dfs_heuristic_rec(obj_node, limit, depth)
            if ret.value == self.goal.value:
                return ret, ret.total_cost
            if newlimit < minimum:
                minimum = newlimit
        return node, minimum

    def idastar(self):
        self.start.cost = self._heuristic_manhatten(self.start.value, 
                self.goal.value)
        self.start.total_cost = 0
        limit = self.start.cost
        loops = 0
        node = None
        depth = 0
        while limit < FINFINITY:
            loops +=1
            # TODO as a while loop
            # node, tmp_limit = self._dfs_heuristic(self.start, limit)
            node, tmp_limit = self._dfs_heuristic_rec(self.start, limit, depth)
            limit = tmp_limit + 1
            if node.value == self.goal.value:
                print("Max nodes %s loops %s" % (
                        self.maxnodes, loops))
                break
        return node

    def astar(self, node_list=None):
        ret = None
        if not node_list:
            self.start.cost = self._heuristic_manhatten(self.start.value, 
                    self.goal.value)
            self.start.total_cost  = 0
            node_list = []
            heapq.heapify(node_list)
            heapq.heappush(node_list, self.start)
            visited = []

        loops = 0
        
        while node_list:
            loops +=1
            node = heapq.heappop(node_list)

            if node.value == self.goal.value:
                print("Max nodes %s loops %s" % (
                    self.maxnodes, loops))
                return node
            tmp = self.get_children(node.value)
            for i in tmp:
                if i not in visited:
                    self.maxnodes += 1
                    visited.append(i)
                    obj_node = Node(i)
                    obj_node.parent = node
                    obj_node.cost = self._heuristic_manhatten(i, self.goal.value)
                    obj_node.total_cost = obj_node.cost + node.total_cost
                    heapq.heappush(node_list, obj_node)
        return ret

    def _dfs(self, node, deep, limit, visited):
        if node.value == self.goal.value:
            return node
        tmp = self.get_children(node.value)
        new_node_list = []
        for i in tmp:
            #remove cycles of 2 
            if i not in visited:
                visited.append(i)
                obj_node = Node(i)
                obj_node.parent = node
                new_node_list.append(obj_node)
        while new_node_list and deep < limit:
            parent = new_node_list.pop(0)
            ret = self._dfs(parent, deep + 1, limit, visited)
            if ret:
                if ret.value == self.goal.value:
                    return ret
        return None

    def idfs(self):
        limit = 0
        ret = None
        while True:
            visited = []
            ret = self._dfs(self.start, 0, limit, visited)
            limit +=1
            #print limit
            if ret:
                break
        return ret

    def bfs(self):
        visited = []
        ret = self._bfs([self.start], visited)
        return ret

    def _bfs(self, node_list, visited):
        new_node_list = []
        for node in node_list:
            if node.value == self.goal.value:
                return node
            tmp = self.get_children(node.value)
            for i in tmp:
                #remove cycles of 2 
                if i not in visited:
                    visited.append(i)
                    obj_node = Node(i)
                    obj_node.parent = node
                    new_node_list.append(obj_node)
        if new_node_list:
            ret = self._bfs(new_node_list, visited)
        return ret
    
    def rep_node(self, node):
        ret = ""
        cells = int(math.sqrt(len(node)))
        for count, val in enumerate(node):
            if not val:
                val = "N"
            if (count + 1) % cells > 0:
                ret += " %s |" % val 
            else:
                ret += " %s\n" % val 
        return ret

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Search 8-Puzzle Solver')

    parser.add_argument('-a', action="store", dest="algo", default="astar",
            help="Select between idastar, astar, bfs, idfs")
    parser.add_argument('-d', action="store", dest="difficulty", default="hard",
            help="Select between easy, middle, hard")
    parser.add_argument('-c', action="store", dest="count", type=int, 
            default=1, help="Set runs count")
    result = parser.parse_args()

    if result.algo not in ("astar", "idastar", "bfs", "idfs", "test"):
        print result.help()
        sys.exit()

    if result.difficulty not in ("middle", "easy", "hard"):
        print result.help()
        sys.exit()

    if result.algo in ("astar", "idastar", "bfs", "idfs"):
        START = START_DICT.get(result.difficulty) 
        puzzle = PuzzleSearch(Node(START), Node(GOAL))
        for i in range(result.count):
            start = time.time()
            func = getattr(puzzle, result.algo)
            res = func()
            elapsed = (time.time() - start)
            print("%s - RESULT in %.4f: \n" % (result.algo.upper(), (elapsed)))
        
        node = res
        count = 0
        while True:
            count +=1
            if not node:
                break
            print puzzle.rep_node(node.value)
            print "cost: %s total_cost: %s\n" % (node.cost, node.total_cost)
            node = node.parent
        print "nodes %s\n" % count

    if result.algo == "test":
        print "TEST MOVE"
        START = START_DICT.get("easy") 
        puzzle = PuzzleSearch(START, GOAL)
        print puzzle.rep_node(START)
        print "right: \n", puzzle.rep_node(puzzle._move_right(START))
        print "left: \n", puzzle.rep_node(puzzle._move_left(START))
        print "down: \n", puzzle.rep_node(puzzle._move_down(START))
        print "up: \n", puzzle.rep_node(puzzle._move_up(START))
        
        print "\nTEST MANHATTEN"
        G = [None, 1, 2, 
             3, 4, 5, 
             6 ,7 ,8]
        print puzzle.rep_node(G)
        S = [1, 2, 5, 
             3, 4, 8, 
             6, 7,None]
        print puzzle.rep_node(S)
        print "Result: %s" % puzzle._heuristic_manhatten(S, G)
        print "1 + 1 + 0 + 0 + 1 + 0 + 0 + 1 = 4"