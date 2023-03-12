import UI, enum

class Editor_States(enum.Enum):

    idle = 1 
    selectedNode = 2 #node pressed but unsure if dragging or editing
    draggingNode = 3
    editingNode = 4
    drawingEdge = 5
    editingEdge = 6

class Graph_Editor:

    nextNodeId = 1

    def __init__(self, graph):
        self.graph = graph
        self.state = Editor_States.idle
        self.nodes = []
        self.edges = []
        self.l_pressPos = (0, 0)
        self.l_wasPressed = False
        self.r_wasPressed = False
        self.targetItem = None
        self.bg = UI.Box(20, 20, 1160, 550, (150, 150, 150, 255), 20)
        self.addNode_button = UI.Button(1080, 40, 80, 80, (37, 193, 22), '+', (200, 200, 200, 255), 60, self.add_node)
        self.remove_button = UI.Button(1080, 140, 80, 80, (232, 65, 65), '-', (200, 200, 200, 255), 60, self.remove_selected_item, enabled=False)
        self.edgeEditor_textBox = UI.TextBox(915, 40, 150, 80, (80, 80, 80), '', (220, 220, 220), 40)
        self.buttons = [self.addNode_button, self.remove_button]
    
    def update(self):
        for node in self.nodes:
            node.set_editing(False)
        for edge in self.edges:
            edge.set_editing(False)
        self.remove_button.set_enabled(False)
        self.edgeEditor_textBox.set_enabled(False)

        if self.state in [Editor_States.editingEdge, Editor_States.editingNode]:
            self.targetItem.set_editing(True)
            self.remove_button.set_enabled(True)

        if self.state == Editor_States.editingEdge:
            self.edgeEditor_textBox.set_enabled(True, self.targetItem)

        if self.state == Editor_States.idle:
            if self.targetItem is not None:
                self.targetItem = None

    def l_down(self, mousePos):
        for node in self.nodes:
            if node.check_press(mousePos):
                self.targetItem = node
                self.nodes.remove(node) #move to end of list so renders on top
                self.nodes.append(node)
                self.state = Editor_States.selectedNode
                return
        for edge in self.edges:
            if edge.check_press(mousePos):
                self.targetItem = edge
                self.state = Editor_States.editingEdge
                return
        for button in self.buttons:
            if button.check_press(mousePos):
                button.function()
        self.state = Editor_States.idle

    def l_up(self):
        if self.state == Editor_States.draggingNode:
            self.state = Editor_States.idle
            self.targetItem.set_valid(True)
            self.targetItem.move_to_last_valid()
            
        if self.state == Editor_States.selectedNode:
            self.state = Editor_States.editingNode
    
    def r_down(self, mousePos):
        for node in self.nodes:
            if node.check_press(mousePos):
                self.edges.append(UI.Drawing_Edge(node))
                self.state = Editor_States.drawingEdge
                return
        self.state = Editor_States.idle
    
    def r_up(self, mousePos):
        if self.state == Editor_States.drawingEdge:
            edge = self.edges.pop()
            for node in self.nodes:
                if node.check_press(mousePos) and node != edge.node:
                    self.add_edge(edge.node, node)
        self.state = Editor_States.idle

    def mouse_move(self, mousePos):
        if not self.bg.pos_is_in(mousePos):
            return
        if self.state == Editor_States.selectedNode:
            self.state = Editor_States.draggingNode
        if self.state == Editor_States.draggingNode:
            for node in self.nodes:
                if node != self.targetItem:
                    if node.check_nodeCollision(mousePos):
                        self.targetItem.set_valid(False)
                        self.targetItem.set_pos(mousePos[0], mousePos[1])
                        return
            self.targetItem.set_valid(True)
            self.targetItem.set_pos(mousePos[0], mousePos[1])
        if self.state == Editor_States.drawingEdge:
            for node in self.nodes:
                if node.check_press(mousePos) and node != self.edges[-1].node:
                    self.edges[-1].update(node.get_pos(), True)
                    return
            self.edges[-1].update(mousePos, False)
        
    def key_down(self, key):
        if self.state != Editor_States.editingEdge:
            return
        num = key - 48
        if key == 8:
            length = self.edgeEditor_textBox.backspace()
        elif key in range(48, 58):
            length = self.edgeEditor_textBox.char_input(str(key - 48))
        elif key in range(1073741913, 1073741923):
            if key == 1073741922: key = 1073741912
            length = self.edgeEditor_textBox.char_input(str(key - 1073741912))
        self.graph.edit_edge(self.targetItem.node1.id, self.targetItem.node2.id, length)

    def add_node(self):
        collision = True
        pos = (600, 245)
        steps = [(0, 15), (30, 0), (0, -15), (-30, 0)]
        stepIndex = 0
        repeats = 1
        while collision:
            for _ in range(repeats):
                pos = (pos[0] + steps[stepIndex][0], pos[1] + steps[stepIndex][1])
                if not self.bg.pos_is_in(pos):
                    return
                collision = False
                for node in self.nodes:
                    if node.check_nodeCollision(pos):
                        collision = True
                if not collision: break
            repeats += stepIndex % 2
            stepIndex = (stepIndex + 1) % 4

        self.graph.add_node(self.nextNodeId)
        self.nodes.append(UI.Node(pos[0], pos[1], self.nextNodeId))
        self.nextNodeId += 1

    def add_edge(self, sourceNode, endNode):
        for edges in self.graph.nodes[sourceNode.id]:
            if edges[0] == endNode.id:
                return
        self.graph.add_edge(sourceNode.id, endNode.id, 0)
        self.edges.append(UI.Static_Edge(sourceNode, endNode))

    def remove_selected_item(self):
        if type(self.targetItem) == UI.Node:
            self.remove_selected_node()
            return
        self.remove_edge()
    
    def remove_selected_node(self):
        selectedNode = self.targetItem
        self.targetItem = None
        for edgeNodes in list(map(lambda x : (x.node1, x.node2, x), self.edges)):
            if selectedNode in edgeNodes:
                self.remove_edge(edgeNodes[2])
        num = selectedNode.displayNum
        self.graph.remove_node(selectedNode.id)
        self.nodes.remove(selectedNode)
        for node in self.nodes:
            if node.displayNum > num:
                node.set_text(str(node.displayNum - 1))

    def remove_edge(self, edge=None):
        if edge is None:
            edge = self.targetItem
        self.graph.remove_edge(edge.node1.id, edge.node2.id)
        self.edges.remove(edge)

    def display(self, screen):
        self.bg.display(screen)
        for button in self.buttons:
            button.display(screen)
        for edge in self.edges:
            edge.display(screen)
        for node in self.nodes:
            node.display(screen)
        self.edgeEditor_textBox.display(screen)