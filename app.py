import graph_editor, graph

class App:

    def __init__(self):
        self.graph = graph.Graph()
        self.graphEditor = graph_editor.Graph_Editor(self.graph)

    def update(self):
        self.graphEditor.update()

    def mouse_down(self, pos, button):
        if button == 1:
            self.graphEditor.l_down(pos)
        if button == 3:
            self.graphEditor.r_down(pos)

    def mouse_up(self, pos, button):
        if button == 1:
            self.graphEditor.l_up()
        if button == 3:
            self.graphEditor.r_up(pos)

    def mouse_move(self, pos):
        self.graphEditor.mouse_move(pos)

    def key_down(self, key):
        self.graphEditor.key_down(key)
        if key == 13:
            print(self.graph.nodes)

    def display(self, screen):
        self.graphEditor.display(screen)