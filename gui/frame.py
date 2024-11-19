from tkinter import *
class My_frame(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        #to Access parent variables
        self.parent = parent

        #put the here on screen
        self.pack(pady=20)

        #create buttons
        self.next_button = Button(self, text="Next Step", command=parent.next_step)
        self.next_button.pack(side=LEFT)

        self.prev_button = Button(self, text="Previous Step", command=parent.prev_step)
        self.prev_button.pack(side=LEFT)

        self.fast_forward_button = Button(self, text="Fast Forward", command=parent.fast_forward)
        self.fast_forward_button.pack(side=LEFT)

        #create Canvas
        self.canvas = Canvas(self, width=1000, height=1000, bg="white")
        self.canvas.pack()
        #Bind option to canvas
        self.canvas.bind("<Button-1>", self.add_node_or_edge)

        # Menü Bar oben
        self.menu_bar = Menu(parent)
        parent.config(menu=self.menu_bar)

        # Optionen Menu
        self.options_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Options", menu=self.options_menu)
        self.debug_mode_var = BooleanVar(value=False)
        # Add commands to the "Options" menu
        self.options_menu.add_command(label="Setting", command=self.open_settings)
        self.options_menu.add_separator()
        self.options_menu.add_command(label="Quit", command=parent.quit)
        self.options_menu.add_checkbutton(label="Toggle Debug mode", variable=self.debug_mode_var, command=self.toggle_debug_mode)

        # Graph optionen Menu
        self.graph_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Graph", menu=self.graph_menu)
        self.graph_menu.add_command(label="Load Default Graph", command=self.load_default_graph)
        self.graph_menu.add_command(label="Clear Graph", command=parent.clear_graph)

        # Creation menu
        self.creation_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Create", menu=self.creation_menu)

        #display current mode with  checkmark
        self.node_mode_var = BooleanVar(value=False)  # Default: Node mode is off
        self.edge_mode_var = BooleanVar(value=False)

        self.creation_menu.add_checkbutton(label="Add Node", variable=self.node_mode_var,
                                           command=self.toggle_node_creation_mode)
        self.creation_menu.add_checkbutton(label="Add Edge", variable=self.edge_mode_var,
                                           command=self.toggle_edge_creation_mode)
        self.creation_menu.add_separator()
        self.creation_menu.add_checkbutton(label="Bidirectional", command=self.toggle_bidirectional_mode)



    def add_node_or_edge(self, event):
        if self.parent.node_creation_mode == True:
            if self.parent.debug:
                print("Node_Event triggered by Mouse clicked at", event.x, event.y)
        if self.parent.edge_creation_mode == True:
            if self.parent.debug:
                print("Edge_Event triggered by Mouse clicked at", event.x, event.y)

    def toggle_debug_mode(self):
        self.parent.debug = self.debug_mode_var.get()
        print("Debug mode is now", "on" if self.parent.debug else "off")

    def shutdown(self):
        if self.parent.debug:
            print("Shutting down...")

    def open_settings(self):
        if self.parent.debug:
            print("Opening settings...")

    def load_default_graph(self):
        if self.parent.debug:
            print("Loading default graph...")

    def clear_graph(self):
        if self.parent.debug:
            print("Clearing graph...")

    def toggle_node_creation_mode(self):
        if self.parent.debug:
            print("Toggling node creation mode...")
        self.parent.node_creation_mode = True
        self.parent.edge_creation_mode = False
        self.node_mode_var.set(True)  # Check the node mode
        self.edge_mode_var.set(False)  # Uncheck edge mode

    def toggle_edge_creation_mode(self):
        if self.parent.debug:
            print("Toggling Edge creation mode...")
        self.parent.node_creation_mode = False
        self.parent.edge_creation_mode = True
        self.node_mode_var.set(False)  # Uncheck node mode
        self.edge_mode_var.set(True)  # Check the edge mode

    def toggle_bidirectional_mode(self):
        if self.parent.debug:
            print("Toggling bidirectional mode...")


