import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import time

from node import Node
from edge import Edge
from vp_complexity_gui import ComplexityGUI
from utils import *
from config import *

# Visualising Prim's main graph application class
class ComplexityAnalyser(ComplexityGUI):
    def __init__(self):
        super().__init__()