import pygame

class Box:

    def __init__(self, x: int, y: int, width: int, height: int, colour: tuple, rounding: int = 0, outlineThickness=0):
        self.pos = pygame.math.Vector2(x, y)
        self.dimensions = pygame.math.Vector2(width, height)
        self.rect = pygame.Rect(x, y, width, height)
        self.colour = colour
        self.rounding = rounding
        self.outlineThickness = outlineThickness

    def get_centre(self):
        return (self.pos.x + (self.dimensions.x / 2), self.pos.y + (self.dimensions.y / 2))
    
    def pos_is_in(self, point):
        return self.rect.collidepoint(point[0], point[1])

    def display(self, screen):
        pygame.draw.rect(screen, self.colour, self.rect, self.outlineThickness, self.rounding)

class Circle:

    def __init__(self, x:int, y:int, radius:int, colour:tuple, hollowRadius=0, visible=True):
        self.pos = pygame.math.Vector2(x, y)
        self.radius = radius
        self.colour = colour
        self.hollowRadius = hollowRadius
        self.visible = visible

    def set_pos(self, x, y):
        self.pos = pygame.math.Vector2(x, y)
        
    def display(self, screen):
        if not self.visible:
            return
        pygame.draw.circle(screen, self.colour, self.pos, self.radius, int(self.radius - self.hollowRadius))

class Text:

    def __init__(self, x:int, y:int, text:str, textColour:tuple, fontSize:float, anchor='tl', maxWidth=0):
        self.pos = pygame.math.Vector2(x, y)
        self.text = text
        self.textColour = textColour
        self.fontSize = fontSize
        self.anchor = anchor
        self.maxWidth = maxWidth
        self.textObj = self.get_text()
        self.rect = self.get_rect()
        self.fit_text()

    def get_text(self):
        font = pygame.font.Font('_Roboto-Bold.ttf', self.fontSize)
        textObj = font.render(self.text, True, self.textColour)
        return textObj

    def get_rect(self):
        textRect = self.textObj.get_rect()
        anchorOffsets = {
            'tl' : (0, 0),
            'l' : (0, textRect.height / 2),
            'bl' : (0, textRect.height),
            'tc' : (textRect.width / 2, 0),
            'c' : (textRect.width / 2, textRect.height / 2),
            'bc' : (textRect.width / 2, textRect.height),
            'tr' : (textRect.width, 0),
            'r' : (textRect.width, textRect.height / 2),
            'br' : (textRect.width, textRect.height)
        }
        offset = anchorOffsets[self.anchor]
        textRect.topleft = (self.pos.x - offset[0], self.pos.y - offset[1])
        return textRect

    def fit_text(self):
        if self.maxWidth == 0:
            return
        while self.rect.width >= self.maxWidth:
            self.fontSize-=1
            self.textObj = self.get_text()
            self.rect = self.get_rect()

    def set_text(self, text):
        self.text = text
        self.textObj = self.get_text()
        self.rect = self.get_rect()
        self.fit_text() 

    def set_pos(self, x, y):
        self.pos = pygame.math.Vector2(x, y)
        self.textObj = self.get_text()
        self.rect = self.get_rect()

    def display(self, screen):
        screen.blit(self.textObj, self.rect)

class Button(Box):

    def __init__(self, x, y, width, height, colour, text, textColour, fontSize, function, enabled=True):
        super().__init__(x, y, width, height, colour, rounding=20)
        self.text = Text(self.get_centre()[0], self.get_centre()[1], text, textColour, fontSize, 'c')
        self.function = function
        self.enabled = enabled

    def check_press(self, mousePos):
        if not self.enabled:
            return False
        return self.rect.collidepoint(mousePos)
    
    def set_enabled(self, enabled):
        self.enabled = enabled

    def display(self, screen):
        if not self.enabled:
            return
        super().display(screen)
        self.text.display(screen)


class TextBox(Box):

    selectedColour = (232, 255, 106)

    def __init__(self, x, y, width, height, colour, text, textColour, fontSize, enabled=True):
        super().__init__(x, y, width, height, colour, rounding=20)
        self.text = text
        self.textObj = Text(x + 15, int(y + height/2), text, textColour, fontSize, 'l')
        self.enabled = enabled
        self.targetEdge = None

    def check_press(self, mousePos):
        if not self.enabled:
            return False
        return self.rect.collidepoint(mousePos)
    
    def backspace(self):
        if len(self.text) == 1:
            self.set_text('0')
            return 0
        self.set_text(self.text[0:-1])
        return int(self.text)

    def char_input(self, char:str):
        if not char.isdigit() or len(self.text) == 5:
            return int(self.text)
        self.set_text((self.text + char).lstrip('0'))
        return int(self.text)

    def set_enabled(self, enabled, targetEdge=None):
        self.enabled = enabled
        self.targetEdge = targetEdge
        if targetEdge is None:
            return
        self.set_text(targetEdge.lengthText.text)
        

    def set_text(self, text):
        self.text = text
        self.textObj.set_text(text)
        self.targetEdge.set_length(text)

    def display(self, screen):
        if not self.enabled:
            return
        super().display(screen)
        self.textObj.display(screen)

###


class Node:

    size = 30
    colour = (44, 74, 178, 255)
    invalidColour = (210, 77, 77, 100)
    selectedColour = (232, 255, 106)
    textColour = (200, 200, 200)
    fontSize = 30
    count = 0

    def __init__(self, x, y, id):
        Node.count += 1
        self.valid = True
        self.editing = False
        self.displayNum = Node.count
        self.id = id
        self.circle = Circle(x, y, self.size, self.colour)
        self.lastValidPos = pygame.Vector2(x, y)
        self.highlight = Circle(x, y, self.size * 1.1, self.selectedColour, self.size, False)
        self.text = Text(x, y, str(self.displayNum), self.textColour, self.fontSize, anchor='c', maxWidth=self.size*1.7)
        

    def __del__(self):
        Node.count -= 1

    def check_press(self, mousePos):
        vector = pygame.math.Vector2(mousePos[0] - self.circle.pos.x, mousePos[1] - self.circle.pos.y)
        return vector.magnitude() < self.size
    
    def check_nodeCollision(self, pos):
        vector = pygame.math.Vector2(pos[0] - self.circle.pos.x, pos[1] - self.circle.pos.y)
        return vector.magnitude() < 2.8*self.size

    def set_pos(self, x, y):
        self.circle.set_pos(x, y)
        self.highlight.set_pos(x, y)
        self.text.set_pos(x, y)
        if self.valid: self.lastValidPos = pygame.Vector2(x, y)

    def set_text(self, text:str):
        self.displayNum = int(text)
        if not text.isnumeric():
            return
        self.text.set_text(text)

    def set_valid(self, valid):
        self.valid = valid
        if self.valid:
            self.circle.colour = self.colour
        else:
            self.circle.colour = self.invalidColour

    def set_editing(self, editing):
        self.editing = editing
        self.highlight.visible = editing

    def get_pos(self):
        return self.circle.pos
    
    def move_to_last_valid(self):
        self.set_pos(self.lastValidPos.x, self.lastValidPos.y)

    def display(self, screen):
        self.circle.display(screen)
        self.highlight.display(screen)
        self.text.display(screen)

class Drawing_Edge:

    colour = (95, 190, 170, 100)
    invalidColour = (210, 77, 77, 100)
    thickness = 8
    
    def __init__(self, node):
        self.node = node
        self.sourcePos = pygame.Vector2(node.circle.pos.x, node.circle.pos.y)
        self.displayColour = self.colour
        self.update((node.circle.pos.x, node.circle.pos.y), False)

    def update(self, mousePos, valid):
        self.endPos = pygame.Vector2(mousePos[0], mousePos[1])
        if valid: self.displayColour = self.colour
        else: self.displayColour = self.invalidColour

    def set_editing(self, x):
        return

    def display(self, screen: pygame.Surface):
        pygame.draw.line(screen, self.displayColour, self.sourcePos, self.endPos, self.thickness)

class Static_Edge:
   
    colour = (75, 152, 152, 160)
    selectedColour = (176, 228, 177)
    textColour = (30, 30, 30)
    thickness = 8

    def __init__(self, node1, node2):
        self.node1 = node1
        self.node2 = node2
        self.editing = False
        self.lengthText = Text(0, 0, '0', self.textColour, 20, anchor='c')

    def check_press(self, mousePos):
        m = pygame.math.Vector2(mousePos[0], mousePos[1])
        p1 = self.node1.get_pos()
        p2 = self.node2.get_pos()
        if m.x < min(p1.x, p2.x) or m.x > max(p1.x, p2.x): return False
        if m.y < min(p1.y, p2.y) or m.y > max(p1.y, p2.y): return False
        v1 = pygame.math.Vector2(p2.x - p1.x, p2.y - p1.y)  #vector between two node points
        v2 = v1.rotate(90)  #perpendicular vector to v1, gives shortest distance when passing through m
        mu = ( (v1.y * (m.x - p1.x)) - (v1.x * (m.y - p1.y)) ) / ( (v1.x * v2.y) - (v1.y * v2.x) )  #constant multiplier for v2 which gives vector from m to point of intersection of v1 and v2
        return (mu * v2).magnitude() < 6

    def set_editing(self, editing):
        self.editing = editing

    def set_length(self, length):
        self.lengthText.set_text(length)

    def display(self, screen):
        if self.editing:
            colour = self.selectedColour
        else:
            colour = self.colour
        pygame.draw.line(screen, colour, self.node1.circle.pos, self.node2.circle.pos, self.thickness)
        p1 = self.node1.get_pos()
        p2 = self.node2.get_pos()
        mid = p1 + 0.5 * (p2 - p1)
        self.lengthText.set_pos(int(mid.x), int(mid.y))
        self.lengthText.display(screen)
