# config.py

# Color configurations
FRAME_FG_COLOR = "#2b2828"
FRAME_BG_COLOR = "#2b2828"
CANVAS_BG_COLOR = "white"

# Window configurations
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

# Heading font
TITLE_FONT = ("Helvetica", 20, "bold")
COMPLEXITY_SUBTITLE_FONT = ("Helvetica", 14)

VISUALISER_GUIDE_TEXT = ["The graph visualiser allows you to see the minimum spanning tree (MST) of a graph using Prim's algorithm. You can create, generate or import a graph directly through the user interface using the menus, buttons and drawable canvas in the centre of the screen.\n\n"
                        + "1. Click the middle canvas to create new nodes\n"
                        + "2. Use the menus on the left to create edges, delete nodes/edges, and use other features like graph importing and graph resetting.\n"
                        + "3. Select a source node in the top right, and click Run Prim's to start Prim's algorithm on your graph.\n"
                        + "4. Use the Next Step button in the bottom right to progress Prim's on your graph until your MST is complete.\n"
                        + "5. Continue editing your graphs dimensions or use the Reset Graph button to start again."]

COMPLEXITY_GUIDE_TEXT = ["The complexity analyser allows you to see the time complexity of Prim's algorithm for a complete graph. You can specify the number of nodes and the range of weights for the edges.\n\n"
                         + "1. Select Number of Comparisons/Execution Time in the top left to specify the y-axis you want.\n"
                         + "2. Use the sliders to specify the number of nodes and the step interval for the chart data.\n"
                         + "3. Click the Analyse button to start the analysis.\n"
                         + "4. The generated chart will display the time complexity of Prim's algorithm for the complete graph. Complexity data will be displayed below the sliders.\n"
                         + "5. Change the slider parameters and click the Analyse button again to see how the time complexity and complexity metrics change."]