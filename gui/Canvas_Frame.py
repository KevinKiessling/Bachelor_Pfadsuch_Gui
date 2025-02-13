import os.path
import random
import string
import tkinter.simpledialog
from tkinter import *
import math
from tkinter import filedialog
import json
from tkinter import messagebox
from tkinter import ttk
from tkinter import colorchooser
from tkinter import Tk, Canvas, Frame, Scrollbar, Button
from tkinter import StringVar, OptionMenu
from tkinter import Toplevel, Label, Button, Checkbutton, BooleanVar
from tkinter import Toplevel, Button, Checkbutton, BooleanVar, Text, Frame, Scrollbar

import copy
class Canvas_Frame(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.shortest_paths_window = None
        self.parent = parent
        self.operation_history = []
        self.node_flags = {}
        self.dragging_node = None# Dictionary to manage node availability
        self.reset_node_ids()
        self.grid(row=0, column=0, sticky="nsew")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=1)
        self.grid_columnconfigure(5, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)


        self.button_frame = Frame(self)
        self.button_frame.grid(row=0, column=0, columnspan=6, pady=5, sticky="ew")
        self.button_frame.grid_columnconfigure(0, weight=1)  #
        self.button_frame.grid_columnconfigure(7, weight=1)

        self.prev_button = Button(self.button_frame, text="1 Schritt zurück", command=parent.prev_step)
        self.prev_button.grid(row=0, column=1, padx=5)

        self.next_button = Button(self.button_frame, text="1 Schritt vor", command=parent.next_step)
        self.next_button.grid(row=0, column=2, padx=5)

        self.pause_button = Button(self.button_frame, text="Pausieren", command=parent.pause)
        self.pause_button.grid(row=0, column=3, padx=5)

        self.fast_forward_button = Button(self.button_frame, text="Vorspulen", command=self.go_forward_button)
        self.fast_forward_button.grid(row=0, column=4, padx=5)

        self.starting_button = Button(
            self.button_frame, text="Algorithmus Starten", command=parent.start_algorithm, width=20
        )
        self.starting_button.grid(row=0, column=5, padx=5)

        self.shortest_paths_button = Button(
            self.button_frame, text="Kürzeste Pfade", command=self.open_shortest_paths, state=DISABLED, width=20
        )
        self.shortest_paths_button.grid(row=0, column=6, padx=5)


        self.canvas_frame = Frame(self, bd=2, relief="solid")
        self.canvas_frame.grid(row=1, column=0, padx=10, pady=5, columnspan=6, sticky="nsew")

        self.canvas = Canvas(self.canvas_frame, bg="white", width=1000, height=1000)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.canvas_frame.grid_rowconfigure(0, weight=1)
        self.canvas_frame.grid_columnconfigure(0, weight=1)


        #self.canvas.bind("<Button-1>", self.add_node)
        self.canvas.bind("<Button-3>", self.add_edge)
        self.canvas.bind("<Button-2>", self.remove_clicked_element)
        self.canvas.bind("<Control-Button-1>", self.remove_clicked_element)

        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.canvas.bind("<Double-1>", self.on_double_click)
        self.canvas_frame.bind("<Configure>", self.resize_canvas)

        self.focus_set()
        self.bind("<Right>", self.go_to_next_step)
        self.bind("<Left>", self.go_step_back)
        self.bind("<Up>", self.go_fast_forward)
        self.bind("<Down>", self.pause_fast_forward)
        self.bind("<Return>", self.start_alg)
        self.bind("<Control-z>", self.undo_last_operation)

        # Menü Bar oben
        self.menu_bar = Menu(parent)
        parent.config(menu=self.menu_bar)

        # Optionen Menü
        self.options_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Optionen", menu=self.options_menu)
        self.debug_mode_var = BooleanVar(value=True)
        self.options_menu.add_command(label="Einstellungen", command=self.open_settings)
        self.options_menu.add_separator()
        self.options_menu.add_command(label="Beenden", command=parent.quit)

        # Graph optionen Menu
        self.graph_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Graph-Funktionen", menu=self.graph_menu)
        self.graph_menu.add_command(label="Lade Standard Graph", command=parent.load_default_graph)
        self.graph_menu.add_command(label="Lösche Graph", command=parent.clear_graph)
        self.graph_menu.add_command(label="Importiere Graph", command=self.import_graph)
        self.graph_menu.add_command(label="Exportiere Graph", command=self.export_graph)

        # Algorithmen menü
        self.algorithm_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Algorithmen", menu=self.algorithm_menu)
        self.dijk_L = BooleanVar(value=False)
        self.dijk_PQ_lazy = BooleanVar(value=True)
        self.dijk_PQ = BooleanVar(value=False)
        self.algorithm_menu.add_checkbutton(label="Dijkstra mit Liste", variable=self.dijk_L , command=self.toggle_dijk_L)
        self.algorithm_menu.add_checkbutton(label="Dijkstra mit Priority Queue", variable=self.dijk_PQ,
                                            command=self.toggle_dijk_PQ)
        self.algorithm_menu.add_checkbutton(label="Dijkstra mit Priority Queue(Lazy Deletion)",
                                            variable=self.dijk_PQ_lazy, command=self.toggle_dijk_PQ_lazy)
        '''self.help = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Hilfe", menu=self.help)
        self.help.add_command(label="Tutorial", command=self.open_tutorial)'''
        self.original_positions = self.parent.node_positions.copy()

    def resize_canvas(self, event):
        if event.widget == self.canvas_frame:
            self.scale_node_positions(event.width, event.height)





    def reset_original_data(self):
        self.canvas.update_idletasks()
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if canvas_width > 1 and canvas_height > 1:
            self.original_width = canvas_width
            self.original_height = canvas_height
            self.original_positions = self.parent.node_positions.copy()
            self.original_radius = self.parent.node_rad

    def scale_node_positions(self, new_width, new_height):
        if new_width <= 1 or new_height <= 1:
            return

        if not hasattr(self, "original_width") or not hasattr(self, "original_height"):
            self.reset_original_data()
            return

        if self.original_width <= 1 or self.original_height <= 1:
            self.reset_original_data()
            if self.original_width <= 1 or self.original_height <= 1:
                return


        scale_x = new_width / self.original_width
        scale_y = new_height / self.original_height

        if new_width == self.original_width and new_height == self.original_height:
            return


        for node, (orig_x, orig_y) in self.original_positions.items():
            new_x = orig_x * scale_x
            new_y = orig_y * scale_y

            new_x = min(max(new_x, 0), new_width)
            new_y = min(max(new_y, 0), new_height)

            self.parent.node_positions[node] = (new_x, new_y)


        scale_factor = (scale_x + scale_y) / 2


        new_radius = self.original_radius * scale_factor
        self.parent.node_rad = new_radius


        original_font_size = 14
        new_font_size = original_font_size * scale_factor


        new_font_size = max(12, min(new_font_size, 25))
        self.parent.font_size_node_weight = int(new_font_size)
        print(self.parent.font_size_node_weight)

        self.parent.update_gui()


    def on_press(self, event):
        x, y = event.x, event.y
        clicked_node = self.get_node_at_position(x, y)

        if clicked_node:
            self.dragging_node = clicked_node
        else:
            self.add_node(event)

    def on_double_click(self, event):
        x, y = event.x, event.y
        clicked_node = self.get_node_at_position(x, y)

        if clicked_node:
            self.parent.set_starting_node(clicked_node)
            if self.parent.debug:
                print(f"Startknoten gesetzt auf {clicked_node}")
        else:
            if self.parent.debug:
                print("Kein Knoten unter Doppelklick gefunden!")
    def on_drag(self, event):
        if self.dragging_node is not None:

            self.parent.node_positions[self.dragging_node] = (event.x, event.y)
            self.reset_original_data()
            self.parent.reset()

    def on_release(self, event):
        if self.dragging_node is not None:
            #self.operation_history.append(("move_node", self.dragging_node, (event.x, event.y)))
            self.dragging_node = None
    # öffnet ein Fenster mit Buttons um die kürzesten Pfade zu zeichnen
    def open_shortest_paths(self):
        if hasattr(self, "shortest_paths_window") and self.shortest_paths_window is not None:
            if self.shortest_paths_window.winfo_exists():
                self.refresh_window_content()
                self.shortest_paths_window.lift()
                return
            else:
                self.shortest_paths_window = None

        self.shortest_paths_window = Tk()
        self.shortest_paths_window.geometry("200x300")
        self.shortest_paths_window.title("Kürzeste Pfade Zeichnen")
        self.shortest_paths_window.rowconfigure(0, weight=1)
        self.shortest_paths_window.columnconfigure(0, weight=1)

        container = Frame(self.shortest_paths_window)
        container.grid(row=0, column=0, sticky="nsew")

        canvas = Canvas(container)
        scrollbar = Scrollbar(container, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=0)
        container.grid_rowconfigure(0, weight=1)

        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        scrollable_frame = Frame(canvas)
        window_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        def update_scrollregion(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        scrollable_frame.bind("<Configure>", update_scrollregion)

        def resize_scrollable_frame(event):
            canvas.itemconfig(window_id, width=event.width)

        canvas.bind("<Configure>", resize_scrollable_frame)

        scrollable_frame.grid_columnconfigure(0, weight=1)

        for index, end_node in enumerate(self.parent.shortest_paths.keys()):
            if end_node == self.parent.start_node:
                continue
            button = Button(
                scrollable_frame,
                text=f"Kürzester Pfad zu {end_node}",
                command=lambda node=end_node: self.on_button_click(node, self.shortest_paths_window)
            )
            button.grid(row=index, column=0, sticky="ew", padx=5, pady=5)

        close_button = Button(self.shortest_paths_window, text="Close", command=self._on_window_close)
        close_button.grid(row=1, column=0, sticky="ew", pady=5)

        self.shortest_paths_window.protocol("WM_DELETE_WINDOW", lambda: self._on_window_close())

        #Besseres Scrollen auf Win/linux
        def on_mouse_wheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        self.shortest_paths_window.bind_all("<MouseWheel>", on_mouse_wheel)

    def refresh_window_content(self):

        scrollable_frame = self.shortest_paths_window.winfo_children()[0].winfo_children()[0].winfo_children()[
            0]
        for widget in scrollable_frame.winfo_children():
            widget.destroy()


        for index, end_node in enumerate(self.parent.shortest_paths.keys()):
            if end_node == self.parent.start_node:
                continue
            button = Button(
                scrollable_frame,
                text=f"Zeichne kürzesten Pfad zu {end_node}",
                command=lambda node=end_node: self.on_button_click(node, self.shortest_paths_window)
            )
            button.grid(row=index, column=0, sticky="ew", padx=5, pady=5)

    def _on_window_close(self):
        if hasattr(self, "shortest_paths_window"):
            self.shortest_paths_window.destroy()
            self.shortest_paths_window = None

    def on_button_click(self, end_node, path_window):

        path = self.parent.shortest_paths.get(end_node, [])

        if self.parent.current_step != -1 and self.parent.current_step >= len(self.parent.steps_finished_algorithm) - 1:
            self.parent.draw_graph_path(path)

        else:
            messagebox.showwarning("Path Not Found",
                                   f"No path to {end_node} exists or Algorithm not in State Algorithmus abgeschlossen.")

           # messagebox.showinfo("Path Drawn", f"Path to {end_node} has been drawn!")

    def open_tutorial(self):
        if self.parent.debug:
            print("Opening tutorial window")

        tutorial_window = Toplevel(self)
        tutorial_window.title("Tutorial")
        tutorial_window.geometry("700x600")
        tutorial_window.transient(self.parent)

        self.dont_show_again_var = BooleanVar()
        self.dont_show_again_var.set(self.parent.has_seen_tutorial)


        frame = Frame(tutorial_window)
        frame.pack(fill="both", expand=True, padx=10, pady=10)


        text_frame = Frame(frame)
        text_frame.pack(fill="both", expand=True, padx=10, pady=10)


        tutorial_text = Text(text_frame, wrap="word", width=80, height=20, padx=10, pady=10, bg="#f0f0f0",
                             state="disabled")
        tutorial_text.pack(side="left", fill="both", expand=True)


        scrollbar = Scrollbar(text_frame, command=tutorial_text.yview)
        scrollbar.pack(side="right", fill="y")


        tutorial_text.config(yscrollcommand=scrollbar.set)


        text_content = """
        Tutorial Übersicht:

        1. **Knotenerstellung** (Linksklick):
           - Klicken Sie auf den Canvas, um einen neuen Knoten zu erstellen. Der Knoten wird an der Position des Mauszeigers erzeugt.

        --------------------------------------------------------------------

        2. **Kantenerstellung** (Rechtsklick):
           - Klicken Sie zuerst mit der rechten Maustaste auf einen Knoten, um ihn als Startpunkt auszuwählen.
           - Klicken Sie mit der rechten Maustaste auf einen anderen Knoten, um eine Kante zwischen den beiden Knoten zu erstellen.
           - Ein Dialogfenster erscheint, um das Gewicht der Kante festzulegen. Falls zufälliger Kantengewichts Modus aktiviert ist,
             wird die Kante direkt mit einem Zufallsgewicht erstellt.

        --------------------------------------------------------------------

        3. **Knoten/Kantenlöschung** (Mittelklick):
           - Klicken Sie mit der mittleren Maustaste (Mausrad) oder STRG + Linksklick auf einen Knoten oder eine Kante, um diesen/diese von dem Canvas zu löschen.
       
        --------------------------------------------------------------------
       
        4. **Algorithmen**
            - Es sind 3 Varianten des Dijkstra Algorithmus implementiert, welche Schritt für Schritt durchlaufen werden können
       
        --------------------------------------------------------------------
       
        5. **Start der Algorithmen**
            - Entweder über die Buttons oben oder per Pfeiltaste rechts oder oben (Vorspulen)
       
        --------------------------------------------------------------------
       
        6. **Startknoten**(Doppel Linksklick)
            - Auswahl des Startknoten durch doppel Linksklick auf einen Knoten auf dem Canvas
            - Falls kein Startknoten gewählt wurde, wird beim Start nach einem Startknoten gefragt
       
        --------------------------------------------------------------------
       
        7. **Import/Export**
            - Es bestelt die möglichkeit einen Graph als .Json Datei zu importieren bzw. zu exportieren
        
        --------------------------------------------------------------------
        
        8. **Knotenlegende**
            - Buchstabe auf Knoten ist der Name des Knoten
            - Zahl unter dem Knoten ist die Distanz vom Startknoten zu diesem Knoten
            
        **Zusätzliche Funktionen:**
        - Knoten können gezogen und verschoben werden. 
        - Das Tutorial-Fenster wird einmal beim Start der App angezeigt. Später können Sie es bei Bedarf über die oberen Leiste aufrufen.

        --------------------------------------------------------------------
    
        Drücken Sie "Okay", um das Tutorial zu schließen.
        """


        tutorial_text.config(state="normal")
        tutorial_text.insert("1.0", text_content)
        tutorial_text.config(state="disabled")


        dont_show_again_check = Checkbutton(
            tutorial_window,
            text="Tutorial beim Start nicht zeigen",
            variable=self.dont_show_again_var
        )
        dont_show_again_check.pack(pady=10)

        def close_tutorial():
            if self.dont_show_again_var.get():
                self.parent.has_seen_tutorial = True
            else:
                self.parent.has_seen_tutorial = False

            self.parent.save_config()
            tutorial_window.destroy()


        cancel_button = Button(tutorial_window, text="Okay", command=close_tutorial)
        cancel_button.pack(pady=10)



    def undo_last_operation(self, event=None):
        if self.parent.debug:
            print(self.operation_history)
        if not self.operation_history:
            if self.parent.debug:
                print("Keine Operation im speicher")
            return

        last_operation = self.operation_history.pop()
        op_type, op_data = last_operation
        if op_type == "add_node":
            self.delete_note(op_data)
        elif op_type == "add_edge":
            node1, node2, _ = op_data
            if node1 in self.parent.graph and node2 in self.parent.graph[node1]:
                del self.parent.graph[node1][node2]
                if self.parent.debug:
                    print(f"Strg+z Kante von {node1} nach {node2} rückgängig gemacht")
        self.parent.reset()
        if self.parent.debug:
            print(self.operation_history)

    #Löscht Knoten oder Kante an Klick position,
    def remove_clicked_element(self, event):
        x, y = event.x, event.y
        if self.parent.debug:
            print("removal event at:", event.x, event.y)

        node = self.get_node_at_position(x, y)
        if node:
            if self.parent.debug:
                print("Knoten gelöscht")
            self._remove_from_history("add_node", node)
            self.delete_note(node)
            return

        kante = self.get_edge_at_coordinates(x, y)
        if kante:

            s, e = kante
            if e in self.parent.graph[s]:
                del self.parent.graph[s][e]
                if self.parent.debug:
                    print(f" Kante {s}, {e} gelöscht")
                self._remove_from_history("add_edge", (s, e))
                self.parent.reset()
                return
            else:
                if self.parent.debug:
                    print("Error, keine Kante gefunden")

    def _remove_from_history(self, op_type, item):
        if self.parent.debug:
            print(op_type)
            print(item)
        for i in range(len(self.operation_history)):
            operation = self.operation_history[i]
            if operation[0] == op_type:
                if op_type == "add_node" and operation[1] == item:
                    del self.operation_history[i]
                    break
                elif op_type == "add_edge" and (operation[1][0] == item[0] and operation[1][1] == item[1]):

                    del self.operation_history[i]
                    break
    #Löscht übergebenen Knoten
    def delete_note(self, node):
        if node in self.parent.graph:
            del self.parent.graph[node]


        for nb in self.parent.graph.values():
            if node in nb:
                del nb[node]
        if node in self.parent.node_positions:
            del self.parent.node_positions[node]
        self.parent.selected_nodes = []
        if self.parent.debug:
            print(f"Knoten {node} gelöscht")
        self.parent.reset()
        self.reset_original_data()
        self.update_avai_ids()

    #Öffnet Einstellungsmenu, welches den Debug mode, random mode und Animationspeed einstellen lässt und in der Config.json speichert.
    def open_settings(self):
        settings_window = Toplevel(self)
        settings_window.title("Einstellungen")
        settings_window.geometry("500x550")
        settings_window.transient(self.parent)


        notebook = ttk.Notebook(settings_window)
        notebook.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)


        scrollable_frame = Frame(notebook)
        notebook.add(scrollable_frame, text="Allgemeine Einstellungen")


        general_tab_canvas = Canvas(scrollable_frame)
        general_tab_canvas.grid(row=0, column=0, sticky="nsew")


        general_tab_scrollbar = ttk.Scrollbar(
            scrollable_frame, orient="vertical", command=general_tab_canvas.yview
        )
        general_tab_scrollbar.grid(row=0, column=1, sticky="ns")

        general_tab_canvas.configure(yscrollcommand=general_tab_scrollbar.set)
        general_tab_canvas.bind(
            "<Configure>", lambda e: general_tab_canvas.configure(scrollregion=general_tab_canvas.bbox("all"))
        )


        general_tab_frame = Frame(general_tab_canvas)
        general_tab_canvas.create_window((0, 0), window=general_tab_frame, anchor="nw")


        scrollable_frame.grid_rowconfigure(0, weight=1)
        scrollable_frame.grid_columnconfigure(0, weight=1)


        def on_mousewheel(event):

            general_tab_canvas.yview_scroll(-1 * (event.delta // 120), "units")


        general_tab_frame.bind("<Enter>", lambda e: settings_window.bind_all("<MouseWheel>", on_mousewheel))
        general_tab_frame.bind("<Leave>", lambda e: settings_window.unbind_all("<MouseWheel>"))


        '''debug_var = BooleanVar(value=self.parent.debug)
        debug_checkbox = Checkbutton(
            general_tab_frame,
            text="Debug Mode",
            variable=debug_var
        )
        debug_checkbox.pack(anchor="w", pady=10, padx=10)'''

        random_mode_var = BooleanVar(value=self.parent.random_edge_mode)
        random_checkbox_frame = Frame(general_tab_frame)
        random_checkbox_frame.pack(anchor="w", pady=10, padx=10)
        random_checkbox = Checkbutton(
            random_checkbox_frame,
            text="Zufälliges Kantengewicht",
            variable=random_mode_var
        )
        random_checkbox.grid(row=0, column=0)

        max_weight_var = IntVar(value=self.parent.max_edge_weight)

        def validate_input(new_val):
            return new_val == "" or new_val.isdigit()

        validate_command = settings_window.register(validate_input)

        max_weight_entry_field = Entry(random_checkbox_frame, textvariable=max_weight_var, width=10, validate="key",
                                       validatecommand=(validate_command, "%P"))
        max_weight_entry_field.grid(row=0, column=1)
        max_weight_label = Label(random_checkbox_frame, text="Maximales Gewicht (<100000)")
        max_weight_label.grid(row=0, column=2)

        def save_default_graph_to_parent():

            self.parent.default_graph_pos = json.loads(json.dumps(self.parent.node_positions))
            self.parent.default_graph = json.loads(json.dumps(self.parent.graph))
            if self.parent.debug:
                print("Default graph updated successfully.")

        save_cur_a_d_button = Button(
            general_tab_frame,
            text="Aktuellen Graphen als Standard Speichern",
            command=lambda: save_default_graph_to_parent()
        )
        save_cur_a_d_button.pack(anchor="w", pady=10, padx=10)




        Label(general_tab_frame, text="Animationsgeschwindigkeit (ms):").pack(pady=10)
        speed_var = IntVar(value=self.parent.animation_speed)
        speed_slider = ttk.Scale(
            general_tab_frame, from_=100, to=1000, orient="horizontal", length=300, variable=speed_var
        )
        speed_slider.pack(pady=10)
        speed_label = Label(general_tab_frame,
                            text=f"Aktuelle Verzögerung bei Vorspul Wiedergabe: {speed_var.get()} ms")
        speed_label.pack()

        def update_speed_label(*args):
            speed_label.config(text=f"Verzögerung bei Vorspul Wiedergabe: {speed_var.get()} ms")

        speed_var.trace_add("write", update_speed_label)

        Label(general_tab_frame, text="Font Größe:").pack(pady=10)
        font_var = IntVar(value=self.parent.font_size_pseudocode)
        font_slider = ttk.Scale(
            general_tab_frame, from_=8, to=25, orient="horizontal", length=300, variable=font_var
        )
        font_slider.pack(pady=10)
        font_label = Label(general_tab_frame, text=f"Aktuelle Font Größe: {font_var.get()}")
        font_label.pack()

        def update_font_label(*args):
            font_label.config(text=f"Aktuelle Font Größe: {font_var.get()}")

        font_var.trace_add("write", update_font_label)


        settings_window.grid_rowconfigure(0, weight=1)
        settings_window.grid_columnconfigure(0, weight=1)

        def apply_settings():
            #self.parent.debug = debug_var.get()
            self.parent.random_edge_mode = random_mode_var.get()
            self.parent.animation_speed = speed_var.get()
            self.parent.font_size_pseudocode = font_var.get()
            max_edge_weight = max_weight_var.get()

            if max_edge_weight < 0 or max_edge_weight >= 100000:

                messagebox.showerror("Ungültige Eingabe", "Maximales Kantengewicht muss <100000 sein")
                return
            self.parent.max_edge_weight = max_weight_var.get()

            self.parent.save_config()
            settings_window.destroy()


        # COLOR TAB
        default_colors = {
            "color_heap": "#d2cd6f",
            "color_d_v": "#559cec",
            "color_discovered_true": "orange",
            "color_discovered_false": "#00ff40",
            "color_edge_highlight": "#53e2ee",
            "color_shortest_path": "#ff4297"
        }

        color_tab = Frame(notebook)
        notebook.add(color_tab, text="Farb Einstellungen")

        def choose_color(element):
            color = colorchooser.askcolor()[1]
            if color:
                if element == 'color_heap':
                    self.parent.color_heap = color
                    color_heap_button.config(bg=color)
                elif element == 'color_d_v':
                    self.parent.color_d_v = color
                    color_d_v_button.config(bg=color)
                elif element == 'color_discovered_true':
                    self.parent.color_discovered_true = color
                    color_discovered_true_button.config(bg=color)
                elif element == 'color_discovered_false':
                    self.parent.color_discovered_false = color
                    color_discovered_false_button.config(bg=color)
                elif element == 'color_edge_highlight':
                    self.parent.color_edge_highlight = color
                    color_edge_highlight_button.config(bg=color)
                elif element == 'color_shortest_path':
                    self.parent.color_shortest_path = color
                    color_shortest_path_button.config(bg=color)


        def reset_colors():

            self.parent.color_heap = default_colors["color_heap"]
            self.parent.color_d_v = default_colors["color_d_v"]
            self.parent.color_discovered_true = default_colors["color_discovered_true"]
            self.parent.color_discovered_false = default_colors["color_discovered_false"]
            self.parent.color_edge_highlight = default_colors["color_edge_highlight"]
            self.parent.color_shortest_path = default_colors["color_shortest_path"]


            color_heap_button.config(bg=self.parent.color_heap)
            color_d_v_button.config(bg=self.parent.color_d_v)
            color_discovered_true_button.config(bg=self.parent.color_discovered_true)
            color_discovered_false_button.config(bg=self.parent.color_discovered_false)
            color_edge_highlight_button.config(bg=self.parent.color_edge_highlight)
            color_shortest_path_button.config(bg=self.parent.color_shortest_path)


        def create_color_button(frame, text, element):
            button = Button(frame, text="    ", width=5, command=lambda: choose_color(element))
            button.grid(row=0, column=0, padx=10)
            label = Label(frame, text=text)
            label.grid(row=0, column=1, padx=10)
            return button


        color_heap_button_frame = Frame(color_tab)
        color_heap_button = create_color_button(color_heap_button_frame, "Heap/List Farbe", 'color_heap')
        color_heap_button_frame.pack(pady=5)
        color_heap_button.config(bg=self.parent.color_heap)

        color_d_v_button_frame = Frame(color_tab)
        color_d_v_button = create_color_button(color_d_v_button_frame, "d[v] Farbe", 'color_d_v')
        color_d_v_button_frame.pack(pady=5)
        color_d_v_button.config(bg=self.parent.color_d_v)

        color_discovered_true_button_frame = Frame(color_tab)
        color_discovered_true_button = create_color_button(color_discovered_true_button_frame, "discovered[v] ← true",
                                                           'color_discovered_true')
        color_discovered_true_button_frame.pack(pady=5)
        color_discovered_true_button.config(bg=self.parent.color_discovered_true)

        color_discovered_false_button_frame = Frame(color_tab)
        color_discovered_false_button = create_color_button(color_discovered_false_button_frame,
                                                            "discovered[v] ← false", 'color_discovered_false')
        color_discovered_false_button_frame.pack(pady=5)
        color_discovered_false_button.config(bg=self.parent.color_discovered_false)

        color_edge_highlight_button_frame = Frame(color_tab)
        color_edge_highlight_button = create_color_button(color_edge_highlight_button_frame, "Hervorgehobene Kante",
                                                          'color_edge_highlight')
        color_edge_highlight_button_frame.pack(pady=5)
        color_edge_highlight_button.config(bg=self.parent.color_edge_highlight)

        color_shortest_path_button_frame = Frame(color_tab)
        color_shortest_path_button = create_color_button(color_shortest_path_button_frame, "Kürzester Pfad",
                                                         'color_shortest_path')
        color_shortest_path_button_frame.pack(pady=5)
        color_shortest_path_button.config(bg=self.parent.color_shortest_path)

        reset_button = Button(color_tab, text="Zurücksetzen", command=reset_colors)
        reset_button.pack(pady=20)

        button_frame = Frame(settings_window)
        button_frame.grid(row=1, column=0, sticky="ew", pady=10)

        apply_button = Button(button_frame, text="Anwenden", command=apply_settings)
        apply_button.grid(row=0, column=0, padx=10)

        cancel_button = Button(button_frame, text="Abbrechen", command=settings_window.destroy)
        cancel_button.grid(row=0, column=1, padx=10)

    # hilfsunktion um die parent funktion zu callen für die Keybinds
    def start_alg (self, event):
        if self.parent.debug:
            print("Beginne Algorithmus")
        self.parent.start_algorithm()
    def go_to_next_step(self, event):
        if self.parent.debug:
            print("1 Schritt vor")
        self.parent.next_step()
    def go_step_back(self, event):
        if self.parent.debug:
            print("1 Schritt zurück")
        self.parent.prev_step()

    def go_forward_button(self):
        if self.parent.debug:
            print("Vorspulen aktiviert")
        self.parent.fast_forward_paused = False
        self.parent.fast_forward()
    def go_fast_forward(self, event):
        if self.parent.debug:
            print("Vorspulen aktiviert")
        self.parent.fast_forward_paused = False
        self.parent.fast_forward()
    def pause_fast_forward(self, event):
        if self.parent.debug:
            print("Vorspulen pausiert")
        self.parent.pause()


    # gibt den aktuellen graphen auf der Konsole aus -> debug optionen
    def print_loaded_graph(self):
        if self.parent.debug:
            print("Aktuell geladener Graph: ")
        print(self.parent.graph)
        print(self.parent.node_positions)
        print(self.parent.steps_finished_algorithm)

    # select dijkstra mit List as algorithm
    def toggle_dijk_L(self):
        if self.parent.debug:
            print("Wechsel zu Dijkstram mit Liste")
        self.parent.selected_algorithm = "Dijkstra_List"
        self.parent.code_frame.set_algorithm("Dijkstra_List")
        self.parent.reset()
        self.dijk_L.set(True)
        self.dijk_PQ_lazy.set(False)
        self.dijk_PQ.set(False)

    #select dijkstra mit Pq as algorithm
    def toggle_dijk_PQ_lazy(self):
        if self.parent.debug:
            print("Wechsel zu Dijkstra mit Priority Queue (Lazy Deletion)")
        self.parent.selected_algorithm = "Dijkstra_PQ_lazy"
        self.parent.code_frame.set_algorithm("Dijkstra_PQ_lazy")
        self.parent.reset()
        self.dijk_L.set(False)
        self.dijk_PQ.set(False)
        self.dijk_PQ_lazy.set(True)
    def toggle_dijk_PQ(self):
        if self.parent.debug:
            print("Wechsel zu Dijkstra mit Priority Queue")
        self.parent.selected_algorithm = "Dijkstra_PQ"
        self.parent.code_frame.set_algorithm("Dijkstra_PQ")
        self.parent.reset()
        self.dijk_L.set(False)
        self.dijk_PQ.set(True)
        self.dijk_PQ_lazy.set(False)



    #Knoten hinzufügen
    def add_node(self, event):
        x, y = event.x, event.y
        clicked_node = self.get_node_at_position(x, y)
        self.parent.reset()

        if clicked_node:
            if self.parent.debug:
                print("Startknoten wählen statt neuer Knoten")
            self.parent.set_starting_node(clicked_node)
            return

        min_dis = self.parent.node_rad * 2
        for node, (c_x, c_y) in self.parent.node_positions.items():
            if math.hypot(c_x - x, c_y - y) < min_dis:
                if self.parent.debug:
                    print(f"Knoten ist zu nah an {node}, bitte etwas weiter entfernt einfügen")
                return

        new_node = self.get_next_id()
        self.parent.graph[new_node] = {}
        self.parent.node_positions[new_node] = (x, y)

        self.operation_history.append(("add_node", new_node))
        if self.parent.debug:
            print(f"Knoten {new_node} hinzugefügt an Position ({x}, {y})")
        self.reset_original_data()
        self.parent.selected_nodes = []
        self.parent.reset()
        self.update_avai_ids()


    def add_edge(self, event):

        x, y = event.x, event.y
        clicked_node = self.get_node_at_position(x, y)

        if clicked_node:

            self.parent.selected_nodes.append(clicked_node)

            if len(self.parent.selected_nodes) == 1:
                self.start_edge_simulation(clicked_node)

            elif len(self.parent.selected_nodes) == 2:
                self.finalize_edge(self.parent.selected_nodes[0], self.parent.selected_nodes[1])
            return

        clicked_edge = self.get_edge_at_coordinates(x, y)
        if clicked_edge:
            start, end = clicked_edge
            if self.parent.debug:
                print("clicked edge")
            current_weight = self.parent.graph[start][end]

            new_weight = None
            while new_weight is None or not (0 <= new_weight <= 99999):

                new_weight = tkinter.simpledialog.askinteger(
                    "Kantengewicht ändern",
                    f"Aktuelles Gewicht: {current_weight}\nNeues Gewicht eingeben (Maximal: 99999):",
                    initialvalue=current_weight
                )

                if new_weight is None:
                    return

                if not (0 <= new_weight <= 99999):
                    tkinter.messagebox.showerror(
                        "Ungültiges Gewicht",
                        "Das Kantengewicht muss zwischen 0 und 99999 liegen. Bitte erneut eingeben."
                    )


            if self.parent.debug:
                print(f"updating edge weight from {start} -> {end} to {new_weight}")
            self.parent.graph[start][end] = new_weight
            self.parent.update_gui()
            self.parent.reset()

    def start_edge_simulation(self, start_node):

        cx, cy = self.parent.node_positions[start_node]
        mx, my = self.canvas.winfo_pointerx(), self.canvas.winfo_pointery()


        dx, dy = mx - cx, my - cy
        length = math.sqrt(dx ** 2 + dy ** 2)

        if length > 0:

            start_x = cx + (dx / length) * 30
            start_y = cy + (dy / length) * 30
        else:

            start_x, start_y = cx, cy

        self.simulated_edge = self.canvas.create_line(start_x, start_y, start_x, start_y, dash=(8, 4), fill='gray', arrow="last", arrowshape=(10, 12, 5))
        self.canvas.bind("<Motion>", self.update_edge_simulation)
        self.canvas.bind("<Button-1>", self.cancel_edge)

    def update_edge_simulation(self, event):

        if hasattr(self, "simulated_edge") and self.parent.selected_nodes:
            try:
                cx, cy = self.parent.node_positions[self.parent.selected_nodes[0]]
                mx, my = event.x, event.y


                dx, dy = mx - cx, my - cy
                length = math.sqrt(dx ** 2 + dy ** 2)

                if length > 0:

                    start_x = cx + (dx / length) * 30
                    start_y = cy + (dy / length) * 30
                else:
                    start_x, start_y = cx, cy


                self.canvas.coords(self.simulated_edge, start_x, start_y, mx, my)
            except (KeyError, IndexError):

                self.cancel_edge()

    def finalize_edge(self, node1, node2):

        if hasattr(self, "simulated_edge"):
            self.canvas.delete(self.simulated_edge)
            del self.simulated_edge
            self.canvas.unbind("<Motion>")

        if node1 == node2:
            self.parent.selected_nodes.clear()
            self.parent.reset()
            return

        weight = self.ask_for_edge_weight()
        if weight is not None:
            self.add_or_update_edge(node1, node2, weight)
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.parent.selected_nodes.clear()

        self.parent.update_gui()
        self.parent.reset()

    def cancel_edge(self, event=None):

        if hasattr(self, "simulated_edge"):
            self.canvas.delete(self.simulated_edge)
            del self.simulated_edge
            self.canvas.bind("<ButtonPress-1>", self.on_press)

        self.parent.selected_nodes.clear()
        self.parent.reset()
    def ask_for_edge_weight(self):

        if self.parent.random_edge_mode:
            if self.parent.debug:
                print("Zufallsmodus -> zufälliges Gewicht.")
            return random.randint(0, self.parent.max_edge_weight)

        weight = None
        while weight is None or not (0 <= weight <= 99999):
            weight = tkinter.simpledialog.askinteger(
                "Kantengewicht Eingeben",
                "Kantengewicht Eingeben (Maximales Gewicht < 100000)"
            )
            if weight is None:
                self.parent.selected_nodes.clear()
                self.parent.reset()
                return None
            if not (0 <= weight <= 99999):
                tkinter.messagebox.showerror(
                    "Ungültiges Gewicht",
                    "Das Kantengewicht muss zwischen 0 und 99999 liegen."
                )
        return weight
     # Hilfsfunktion die einen Knoten returned der in einem Radius von 30px zu click coordinaten ist. Wird benötigt für die Erstellung von Kanten
    def get_node_at_position(self, x, y):

        for node, (nx, ny) in self.parent.node_positions.items():
            if math.hypot(nx - x, ny - y) <= self.parent.node_rad:
                return node
        return None

    def add_or_update_edge(self, node1, node2, weight):
        """Adds or updates an edge in the graph."""
        if node2 in self.parent.graph[node1]:
            if self.parent.debug:
                print(f"Updating existing edge {node1} -> {node2} with weight {weight}")
            self.parent.graph[node1][node2] = weight
            #self.operation_history.append(("update_edge", (node1, node2, weight)))
        elif node1 in self.parent.graph[node2]:
            if self.parent.debug:
                print(f"Replacing edge {node2} -> {node1} with {node1} -> {node2}")
            del self.parent.graph[node2][node1]
            self.parent.graph[node1][node2] = weight
            self.operation_history.append(("add_edge", (node1, node2, weight)))
        else:
            self.parent.graph[node1][node2] = weight
            self.operation_history.append(("add_edge", (node1, node2, weight)))
            if self.parent.debug:
                print(f"Added edge {node1} -> {node2} with weight {weight}")
    # hilfsfunktion die naheste kante zu 2 koordinaten findet, wird benötigt um Kanten zu löschen
    def get_edge_at_coordinates(self, x, y):
        nearest_edge = None
        min = float('inf')

        for node_s, neighbor in self.parent.graph.items():
            for node_e in neighbor:

                if node_s in self.parent.node_positions and node_e in self.parent.node_positions:
                    x1, y1 = self.parent.node_positions[node_s]
                    x2, y2 = self.parent.node_positions[node_e]
                    dis = self.distance_to_edge(x, y, x1, y1, x2, y2)

                    if dis < min and dis <=5:
                        min = dis
                        nearest_edge = (node_s, node_e)
        return nearest_edge

    # Berechnet die distanz von einem punkt zu einer Linie

    def distance_to_edge(self, x, y, x2, y2, x3, y3):
        if (x2, y2) == (x3, y3):
            return math.hypot(x - x2, y - y2)
        dx, dy = x3 - x2, y3 - y2
        t = ((x - x2) * dx + (y - y2) * dy) / (dx * dx + dy * dy)
        t = max(0, min(1, t))
        closest_x = x2 + t * dx
        closest_y = y2 + t * dy
        return math.hypot(x - closest_x, y - closest_y)

    # export funktion, Hier wird der Graph als .json file gespeichert. Default directory ist dafür der save_files ordner
    def export_graph(self):
        default_dir = os.path.join(os.getcwd(), "save_files")
        os.makedirs(default_dir, exist_ok=True)
        filepath = filedialog.asksaveasfilename(
            initialdir=default_dir,
            initialfile="Exported_Graph.json",
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
        )
        if not filepath:
            return
        try:
            data = {
                "graph": self.parent.graph,
                "node_position": self.parent.node_positions
            }
            with open(filepath, 'w') as file:
                json.dump(data, file, indent=4)
            print(f"exported to {filepath}")
        except Exception as e:
            print(f"Error:{e}")

    # import funktion, um einen Graphen als .json zu importieren
    def import_graph(self):
        default_dir = os.path.join(os.getcwd(), "save_files")
        os.makedirs(default_dir, exist_ok=True)
        filepath = filedialog.askopenfilename(
            title="Graph .json file zum Importieren auswählen",
            initialdir=default_dir,
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
        )
        if not filepath:
            return
        try:
            with open(filepath, 'r') as file:
                data = json.load(file)
            if "graph" in data and "node_position" in data:
                self.parent.graph = data["graph"]
                self.parent.node_positions = {node: tuple(pos) for node, pos in data["node_position"].items()}
                if self.parent.debug:
                    print(f" Graph von {filepath} wurde erfolgreich importiert")
                self.update_avai_ids()
                self.operation_history = []
                self.parent.reset()
            else:
                print("Fehlerhafte Input datei, Graph oder Node_Position nicht gefunden")
        except Exception as e:
            print(f"Importing error : {e}")

    def generate_node_ids(self):

        ids = []
        length = 1
        while len(ids) < 100:
            for i in range(26**length):
                name = ""
                current = i
                for _ in range(length):
                    name = chr(ord('A') + (current % 26)) + name
                    current //= 26
                ids.append(name)
            length += 1
        return ids[:100]

    def reset_node_ids(self):

        self.node_flags = {node_id: True for node_id in self.generate_node_ids()}

    def get_next_id(self):

        for node_id, is_available in sorted(self.node_flags.items(), key=lambda x: (len(x[0]), x[0])):
            if is_available:
                self.node_flags[node_id] = False
                return node_id
        raise ValueError("Keine verfügbaren Knoten-IDs mehr.")

    def set_node_availability(self, node_id, available):

        if node_id in self.node_flags:
            self.node_flags[node_id] = available
        else:
            raise ValueError(f"Node ID {node_id} does not exist.")

    def update_avai_ids(self):

        imported_nodes = self.parent.node_positions.keys()
        for node_id in self.node_flags:
            self.node_flags[node_id] = node_id not in imported_nodes
        if self.parent.debug:
            print(self.node_flags)