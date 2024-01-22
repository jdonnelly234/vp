# For edge objects
class Edge:
    def __init__(self, start_node, end_node, weight):
        self.start_node = start_node    # Start node of the edge
        self.end_node = end_node    # End node of the edge
        self.weight = weight    # Weight of the edge
        self.line_id = None  # To store the ID of the line on the canvas
        self.text_id = None  # To store the ID of the text label for the weight
        self.midpoint_id = None  # For the midpoint oval
        self.is_mst_edge = False  # Attribute to mark if the edge is part of the MST for toggling button