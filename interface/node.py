# For node objects
class Node:
    def __init__(self, x, y, identifier):
        self.x = x  # x-coordinate of the node
        self.y = y  # y-coordinate of the node
        self.id = None  # To store the ID of the oval on the canvas
        self.text_id = None  # To store the ID of the text on the canvas
        self.identifier = identifier  # To store the identifier of the node