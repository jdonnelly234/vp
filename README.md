# Visualising Prim's 

This repository contains the development code and test suites for 'Visualising Prim's' (VP), a Prim's algorithm educational tool. VP is a standalone application (written in Python), that allows users to draw/generate graphs using their mouse in tandem with drop down-menus. Drawn graphs can then be ran through Prim's algorithm, and VP highlights nodes and edges that are within the minimum spanning tree of the drawn graphs. VP also offers textual captions to accomodate graph highlighting, including an L-table representation that updates accurately as the algorithm progresses. Users have full control of the execution of the algorithm through the use of a Python generator function, making VP a highly dynamic and effective tool in teaching Prim's algorithm.

VP also includes a complexity analyser, which generates large complete graphs (up to 4000 nodes), then runs Prim's algorithm on them. During it's execution, Prim's collects complexity metrics related to the performance of the algorithm, mainly execution time and the number of comparisons of edge weights the algorithm performs, and plots these on a chart that is directly embedded within the UI, alongside a theoretical fitted complexity curve.


## Visuals
### VP's Graph Visualiser
![VP's Graph Visualiser](interface/images/VP%20graph%20visualiser.png)
### VP's Complexity Analyser
![VP's Complexity Analyser](interface/images/VP%20complexity%20analyser.png)


## Installation
The 'src' directory contains executable versions of VP for Windows and Mac, created using pyinstaller, which can be ran on your machine to directly access the application. Simply pull this repository and navigate to the 'src' directory on your local machine to find the VP executable files for your OS.


## Structure
The code for building the VP application is located entirely within the 'interface' directory. Testing related files are located within the 'test' directory. The 'complexityAnalysisFiles' directory includes implementations of Prim's algorithm in Python, C++, Rust, Java and Go that were created during development but were ultimately unused in the final implementation. The 'testImportFiles' directory includes JSON files that can be used in tandem with the Import and Export functionalities of VP's graph visualiser. Meeting minutes can be found within the 'Minutes' directory


## Authors and acknowledgment
VP was developed by Computer Science student, James Donnelly, as the core of his final year dissertation in the School of Electronics, Electrical Engineering and Computer Science at Queen's University, Belfast. Special acknowledgement is given to the projects supervisor, Dr Peter Kilpatrick, who played an important role in clarifying the direction of the project through his expertise in algorithms and algorithmic teaching. 


