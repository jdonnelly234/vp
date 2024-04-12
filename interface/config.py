# config.py

# Window configurations
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

# Heading font
TITLE_FONT = ("Helvetica", 20, "bold")
TITLE_COLOUR = "white"
COMPLEXITY_SUBTITLE_FONT = ("Helvetica", 14)
COMPLEXITY_PLACEHOLDER_FONT = ("Helvetica", 14, "italic")
COMPLEXITY_PLACEHOLDER_COLOUR = "grey"

VISUALISER_GUIDE_TEXT = "The graph visualiser allows you to construct the minimum spanning tree (MST) of a graph in an iterative manner using Prim's algorithm. You can create, generate or import a graph directly through the user interface using the menus, buttons and drawable canvas in the centre of the screen.\n\n" + "1. Click the middle canvas to create new nodes.\n\n" + "2. Use the menus on the left to create edges, delete nodes/edges, and use other features like graph importing and graph resetting.\n\n" + "3. Select a source node in the top right, and click Run Prim's to start Prim's algorithm on your graph.\n\n" + "4. Use the Next Step button in the bottom right to progress Prim's on your graph until your MST is complete.\n\n" + "5. Continue editing your graphs dimensions or use the Reset Graph button to start again."

COMPLEXITY_GUIDE_TEXT = "The complexity analyser allows you to see the time complexity of Prim's algorithm for a series of complete graphs. You can specify the maximum number of nodes and the size of the step interval between plotted points.\n\n" + "1. Select No. of Comparisons/Execution Time in the top left to specify the complexity metrics you want to collect.\n\n" + "2. Use the sliders to specify the maximum number of nodes and the step interval for the chart data.\n\n" + "3. Click the Analyse button to start the analysis.\n\n" + "4. After a short while, the generated chart will display the time complexity of Prim's algorithm for the series of complete graphs. Complexity data will be displayed below the sliders.\n\n" + "5. Change the slider parameters and click the Analyse button again to see how the time complexity and complexity metrics change."

FAQ_TEXT = "Q: What is a complete graph?\n\n" + "A complete graph is a graph where there is an edge between every pair of nodes. In a complete graph with n nodes, there are n(n-1)/2 edges.\n\n" +  "Q: What formats can I import a graph in?\n\n" + "You can import a graph in JSON format. The JSON file should contain a list of nodes, where each node has a valid alphabetical identifier (eg. A, B, C...) and valid x/y coordiantes for the canvas (Canvas width is 600 and height is 700) and a list of edges, where each edge is listed with a start and end node and a weight.\n\n" + "Q: What format are exported graphs in?\n\n" + "Exported graphs are in the same JSON format as imported graphs. You can save the JSON file and import it back into the graph visualiser at a later time.\n\n"


# Color configurations
FRAME_FG_COLOR = "#2b2828"
FRAME_BG_COLOR = "#2b2828"
CANVAS_BG_COLOR = "white"
BUTTON_FG_COLOR = "#4D85AC"
BUTTON_BG_COLOR = FRAME_FG_COLOR
ANALYSER_FRAME_COLOR = "#464141"
