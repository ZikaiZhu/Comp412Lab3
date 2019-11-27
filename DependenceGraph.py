from collections import defaultdict
class DependenceGraph:
    def __init__(self):
        self.opindex = None
        self.next = set()
        self.operation = None
        self.parent = set()
        self.done_next = set()
        self.priority = 0
        self.edge_weights = defaultdict(int)

    def __lt__(self, other):
        return self.get_operation().get_index() > other.get_operation().get_index()

    def set_opindex(self, num):
        self.opindex = num

    def get_opindex(self):
        return self.opindex

    def add_next(self, next_node):
        self.next.add(next_node)

    def get_next(self):
        return self.next

    def get_operation(self):
        return self.operation

    def set_operation(self, op):
        self.operation = op

    def add_parent(self, parent_node):
        self.parent.add(parent_node)

    def get_parent(self):
        return self.parent

    def set_priority(self, num):
        self.priority = num

    def get_priority(self):
        return self.priority

    def set_edge_weights(self, to_node, number):
        self.edge_weights[to_node] = max(self.edge_weights[to_node], number)

    def get_edge_weights(self):
        return self.edge_weights

    def add_done_set(self, node):
        self.done_next.add(node)

    def get_done_set(self):
        return self.done_next

    def set_prio_from_root(self):
        # first compute all connected nodes
        node_list = set()
        stack = []
        stack.append(self)
        while stack:
            cur = stack.pop()
            node_list.add(cur)
            if cur.get_next():
                for item in cur.get_next():
                    stack.append(item)
        visited = {}
        for node in node_list:
            #print(node.get_operation().get_index())
            visited[node] = False
        #print ("Done an iteration")
        new_stack = []
        for n in node_list:
            if not visited[n]:
                n.topologicalSortUtil(n, visited, new_stack)
        for node in node_list:
            node.set_priority(float("-inf"))
        self.set_priority(0)
        while new_stack:
            u = new_stack.pop(0)
            if u.get_priority() != float("-inf"):
                if u.get_next():
                    for i in u.get_next():
                        #print (u.get_operation().get_index(), i.get_operation().get_index(), u.get_edge_weights()[i])
                        i.set_priority(max(i.get_priority(), u.get_priority() + u.get_edge_weights()[i]))



    def topologicalSortUtil(self, node, visited, stack):
        visited[node] = True
        if node.get_next():
            for item in node.get_next():
                if not visited[item]:
                    item.topologicalSortUtil(item, visited, stack)
        stack.insert(0, node)

    def is_ready(self):
        return self.done_next == self.next

    def fully_tell_done(self):
        for parent in self.get_parent():
            parent.add_done_set(self)

    def serialization_tell_done(self):
        for parent in self.get_parent():
            if parent.get_edge_weights()[self] == 1:
                parent.add_done_set(self)
