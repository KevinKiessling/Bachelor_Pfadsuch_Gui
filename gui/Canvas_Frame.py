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
from tkinter import Toplevel, Button, Checkbutton, BooleanVar, Text, Frame, Scrollbar, PhotoImage, LEFT
from idlelib.tooltip import Hovertip

import copy
class Canvas_Frame(Frame):
    """
    Linke seite der GUI
    """
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
        self.prev_icon = PhotoImage(file="icons/arrow-left.png")  # Replace with your icon path
        self.next_icon = PhotoImage(file="icons/arrow-right.png")  # Replace with your icon path
        self.pause_icon = PhotoImage(file="icons/pause.png")  # Replace with your icon path
        self.fast_forward_icon = PhotoImage(file="icons/fast-forward.png")  # Replace with your icon path
        self.start_icon = PhotoImage(file="icons/play.png")  # Replace with your icon path
        self.shortest_paths_icon = PhotoImage(file="icons/path.png")  # Replace with your icon path
        self.cancel_icon = PhotoImage(file="icons/cancel.png")
        self.button_frame = Frame(self)
        self.button_frame.grid(row=0, column=0, columnspan=7, pady=5, sticky="ew")
        #padding left/right
        self.button_frame.grid_columnconfigure(0, weight=1)  #
        self.button_frame.grid_columnconfigure(8, weight=1)

        self.prev_button = Button(self.button_frame, image=self.prev_icon, command=parent.prev_step)
        self.prev_button.grid(row=0, column=1, padx=5)
        Hovertip(self.prev_button, "1 Schritt zurück")

        self.next_button = Button(self.button_frame, image=self.next_icon, command=parent.next_step)
        self.next_button.grid(row=0, column=2, padx=5)
        Hovertip(self.next_button, "1 Schritt vor")

        self.pause_button = Button(self.button_frame, image=self.pause_icon, command=parent.pause, state=DISABLED)
        self.pause_button.grid(row=0, column=3, padx=5)
        Hovertip(self.pause_button, "Pausiert automatische Wiedergabe")

        self.fast_forward_button = Button(self.button_frame, image=self.fast_forward_icon, command=self.go_forward_button)
        self.fast_forward_button.grid(row=0, column=4, padx=5)
        Hovertip(self.fast_forward_button, "Startet automatische Wiedergabe")

        self.starting_button = Button(
            self.button_frame, image=self.start_icon, command=parent.start_algorithm, width=20
        )
        self.starting_button.grid(row=0, column=5, padx=5)
        Hovertip(self.starting_button, "Starte Algorithmus")

        self.shortest_paths_button = Button(
            self.button_frame, image=self.shortest_paths_icon, command=self.open_shortest_paths, state=DISABLED, width=20
        )
        self.shortest_paths_button.grid(row=0, column=6, padx=5)
        Hovertip(self.shortest_paths_button, "Öffne kürzeste Pfade Fenster")
        self.cancel_button = Button(self.button_frame, image=self.cancel_icon,
                                          command=self.cancel_button_method, state=DISABLED)
        self.cancel_button.grid(row=0, column=7, padx=5)
        Hovertip(self.cancel_button, "Abbruch")

        self.canvas_frame = Frame(self, bd=2, relief="solid")
        self.canvas_frame.grid(row=1, column=0, padx=10, pady=5, columnspan=6, sticky="nsew")

        self.canvas = Canvas(self.canvas_frame, bg="white", width=1000, height=1000)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.canvas_frame.grid_rowconfigure(0, weight=1)
        self.canvas_frame.grid_columnconfigure(0, weight=1)

        self.canvas_bindings = [
            ("<Button-3>", self.add_edge),
            ("<Button-2>", self.remove_clicked_element),
            ("<Control-Button-1>", self.remove_clicked_element),
            ("<ButtonPress-1>", self.on_press),
            ("<B1-Motion>", self.on_drag),
            ("<ButtonRelease-1>", self.on_release),
            ("<Double-1>", self.on_double_click),
        ]
        for event, callback in self.canvas_bindings:
            self.canvas.bind(event, callback)

        self.focus_set()
        self.bind("<Right>", self.go_to_next_step)
        self.bind("<Left>", self.go_step_back)
        self.bind("<Up>", self.go_fast_forward)
        self.bind("<Down>", self.pause_fast_forward)
        self.bind("<Return>", self.start_alg)
        self.bind("<Control-z>", self.undo_last_operation)
        self.bind("<Escape>", self.cancel_bind_method)
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
        self.menu_bar.add_cascade(label="Graph Funktionen", menu=self.graph_menu)
        self.graph_menu.add_command(label="Lade Standardgraph", command=parent.load_default_graph)
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
        self.help = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Hilfe", menu=self.help)
        self.help.add_command(label="Tutorial", command=self.open_tutorial)
        self.canvas_frame.bind("<Configure>", self.resize_canvas)
        self.initial_width = 1000
        self.initial_height = 1000
        self.canvas_width = self.initial_width
        self.canvas_height = self.initial_height

    def disable_canvas_interactions(self):
        """
        Entfernt alle Canvas Bindings, wird genutzt um diese Während der Ausführung eines Algorithmusses zu blockieren
        :return:
        """
        if self.parent.debug:
            print("Disabling graph interactions while algorithm is running")

        for event, _ in self.canvas_bindings:
            self.canvas.unbind(event)
    def enable_canvas_interactions(self):
        """
        Aktiviert die Canvas Bindings erneut um diese außerhalb eines Algorithmusses wieder zu aktivieren
        :return:
        """
        if self.parent.debug:
            print("Re-enabling graph interactions")
        # Rebind all canvas events
        for event, callback in self.canvas_bindings:
            self.canvas.bind(event, callback)
    def cancel_bind_method(self, event):
        """
        Esc- Bind um den Graphen zu resetten
        :param event: Event was diese Methode ausgelöst hat, in dem Fall esc
        :return:
        """
        self.parent.reset()
        self.close_shortest_path_window()
    def cancel_button_method(self):
        """
        Methode die den Button mit einer Funktion der Parent Klasse verbindet
        :return:
        """
        self.parent.reset()
        self.close_shortest_path_window()
    def close_shortest_path_window(self):
        """
        Schließt das kürzeste Pfade menu
        :return:
        """
        if hasattr(self, "shortest_paths_window") and self.shortest_paths_window is not None:
            if self.shortest_paths_window.winfo_exists():
                self.shortest_paths_window.destroy()
            self.shortest_paths_window = None
    def resize_canvas(self, event):
        """
        Methode um den Graphen zu skalieren
        :param event: Event was eine veränderung der Canvas Größe hervorgerufen hat
        :return:
        """

        new_width = event.width
        new_height = event.height

        if new_width == self.canvas_width and new_height == self.canvas_height:
            return

        scale_x = new_width / self.canvas_width
        scale_y = new_height / self.canvas_height

        self.scale_node_positions(scale_x, scale_y)

        self.scale_node_size_absolute(new_width, new_height)

        self.canvas_width = new_width
        self.canvas_height = new_height
        self.parent.update_gui()

    def scale_node_positions(self, scale_x, scale_y):
        """
        Skaliert die Knoten positionen.
        :param scale_x: Faktor für x
        :param scale_y: Faktor für y
        :return:
        """

        for node, (x, y) in self.parent.node_positions.items():
            new_x = x * scale_x
            new_y = y * scale_y
            self.parent.node_positions[node] = (new_x, new_y)

    def scale_node_size_absolute(self, new_width, new_height):
        """
        Skaliert die Knoten größe und schriftgröße der Knoten
        :param new_width: Neue Breite
        :param new_height: Neue Höhe
        :return:
        """

        scale_x = new_width / self.initial_width
        scale_y = new_height / self.initial_height
        average_scale = (scale_x + scale_y) / 2

        self.parent.node_rad = self.parent.node_rad_original * average_scale
        self.parent.font_size_edge_weight = int(self.parent.font_size_edge_weight_original * average_scale)
        self.parent.font_size_node_label = int(self.parent.font_size_node_label_original * average_scale)


    def on_press(self, event):
        """
        Event was mit dem Canvas verbunden ist, um das angeklickt Element zu erkennen
        :param event: Koordinaten des Mausklicks
        :return:
        """
        x, y = event.x, event.y
        clicked_node = self.get_node_at_position(x, y)

        if clicked_node:
            self.dragging_node = clicked_node
        else:
            self.add_node(event)

    def on_double_click(self, event):
        """
        Even um doppelklick zu erkennen
        :param event: Koordinaten
        :return:
        """
        x, y = event.x, event.y
        clicked_node = self.get_node_at_position(x, y)

        if clicked_node:
            if self.parent.start_node == clicked_node:
                self.parent.set_starting_node("")
                if self.parent.debug:
                    print(f"Startknoten {clicked_node} entfernt")
            else:
                self.parent.set_starting_node(clicked_node)
                if self.parent.debug:
                    print(f"Startknoten gesetzt auf {clicked_node}")
        else:
            if self.parent.debug:
                print("Kein Knoten unter Doppelklick gefunden!")
    def on_drag(self, event):
        """
        Event um maus Drag zu erkennen
        :param event: Koordinaten
        :return:
        """
        if self.dragging_node is not None:
            # Clamp x and y within canvas bounds
            x = max(self.parent.node_rad, min(event.x, self.canvas_width - self.parent.node_rad))
            y = max(self.parent.node_rad, min(event.y, self.canvas_height - self.parent.node_rad))

            self.parent.node_positions[self.dragging_node] = (x, y)
            self.parent.reset()

    def on_release(self, event):
        """
        Event um loslassen des Mausdrags zu erkennne
        :param event: Koordinaten
        :return:
        """
        if self.dragging_node is not None:
            #self.operation_history.append(("move_node", self.dragging_node, (event.x, event.y)))
            self.dragging_node = None
    # öffnet ein Fenster mit Buttons um die kürzesten Pfade zu zeichnen
    def open_shortest_paths(self):
        """
        Öffnet kürzeste Pfade Fenster
        :return:
        """
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
            """
            Updated die Scrollregion der Scrollbar
            :param event: Event was diese Funktion ausgelöst hat
            :return:
            """
            canvas.configure(scrollregion=canvas.bbox("all"))

        scrollable_frame.bind("<Configure>", update_scrollregion)

        def resize_scrollable_frame(event):
            """
            Skaliert den Scrollbar frame
            :param event: Event was diese Funktion ausgelöst hat
            :return:
            """
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
            """
            Verbessert das Scrollen auf anderen Plattformen
            :param event: mouserad scroll
            :return:
            """
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        self.shortest_paths_window.bind_all("<MouseWheel>", on_mouse_wheel)

    def refresh_window_content(self):
        """
        Methode des kürzeste Pfade menüs, um den Inhalt zu refreshen
        :return:
        """

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
        """
        Schließt kürzeste Pfade menu wenn Hauptfenster geschlossen wird
        :return:
        """
        if hasattr(self, "shortest_paths_window"):
            self.shortest_paths_window.destroy()
            self.shortest_paths_window = None

    def on_button_click(self, end_node, path_window):
        """
        Funktion um die Buttons im kürzeste Pfade Fenster mit Funktionen zu verbinden
        :param end_node: Endknoten
        :param path_window: aktuelles Fenster
        :return:
        """

        path = self.parent.shortest_paths.get(end_node, [])

        if self.parent.current_step != -1 and self.parent.current_step >= len(self.parent.steps_finished_algorithm) - 1:
            self.parent.draw_graph_path(path)

        else:
            messagebox.showwarning("Path Not Found",
                                   f"No path to {end_node} exists or Algorithm not in State Algorithmus abgeschlossen.")

           # messagebox.showinfo("Path Drawn", f"Path to {end_node} has been drawn!")

    def open_tutorial(self):
        """
        Öffnet ein Hilfsfenster, was eine Features des Programms erklärt
        :return:
        """

        tutorial_window = Toplevel(self.parent)
        tutorial_window.title("Tutorial")
        tutorial_window.geometry("850x650")

        custom_font = ("Arial", 12)

        notebook = ttk.Notebook(tutorial_window)
        notebook.pack(fill="both", expand=True)


        self._add_welcome_tab(notebook, custom_font)
        self._add_node_management_tab(notebook, custom_font)
        self._add_button_explanations_tab(notebook, custom_font)
        self._add_heap_description_tab(notebook, custom_font)

    def _add_welcome_tab(self, notebook, custom_font):
        """
        Willkommensfenster
        :param notebook: notbook tab
        :param custom_font: fontsize
        :return:
        """

        welcome_tab = ttk.Frame(notebook)
        notebook.add(welcome_tab, text="Übersicht")


        canvas_frame = Frame(welcome_tab)
        canvas_frame.pack(fill="both", expand=True)

        canvas = Canvas(canvas_frame)
        scrollbar = Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        content_frame = Frame(canvas)
        canvas.create_window((0, 0), window=content_frame, anchor="nw")


        def update_scrollregion(event=None):
            """
            Updated die Scrollregion des Fensters
            :param event: Scroll event
            :return:
            """
            canvas.configure(scrollregion=canvas.bbox("all"))


        content_frame.bind("<Configure>", update_scrollregion)


        def update_wraplength(event=None):
            new_width = content_frame.winfo_width() - 40
            for label in content_frame.winfo_children():
                if isinstance(label, Label):
                    label.config(wraplength=new_width)
            update_scrollregion()


        content_frame.bind("<Configure>", update_wraplength)


        Label(content_frame, text="Eine GUI zur Visualisierung von Pfadsuchalgorithmen", font=("Arial", 16, "bold")).pack(pady=(10, 5))

        intro_text = """
        Diese Anwendung dient der Erstellung, Bearbeitung und Visualisierung von Graphen sowie der Demonstration von Pfadsuchalgorithmen.
        """
        Label(content_frame, text=intro_text, justify="left", wraplength=750, font=custom_font).pack(padx=20,
                                                                                                     pady=(0, 10))


        Label(content_frame, text="Funktionen:", font=("Arial", 14, "bold")).pack(anchor="w", pady=(5, 0))
        Label(content_frame,
              text="- Graphen erstellen und bearbeiten:\n"
                   "  - Knoten und Kanten hinzufügen oder entfernen.\n"
                   "  - Kantengewichte festlegen.\n"
                   "  - Knoten per Drag-and-Drop verschieben.",
              justify="left", font=custom_font, wraplength=750).pack(anchor="w", pady=(0, 5))

        Label(content_frame,
              text="- Pfadsuchalgorithmen visualisieren:\n"
                   "  - Dijkstra-Algorithmus mit Priority Queue.\n"
                   "  - Dijkstra-Algorithmus mit Liste.\n"
                   "  - Dijkstra-Algorithmus mit Priority Queue und Lazy Deletion.",
              justify="left", font=custom_font, wraplength=750).pack(anchor="w", pady=(0, 5))

        Label(content_frame,
              text="- Graphen speichern und laden:\n"
                   "  - Graphen in einer Datei speichern.\n"
                   "  - Gespeicherte Graphen zur weiteren Bearbeitung laden.",
              justify="left", font=custom_font, wraplength=750).pack(anchor="w", pady=(0, 10))



        def _on_mousewheel(event):
            canvas.yview_scroll(-1 * (event.delta // 120), "units")

        def _bind_mousewheel(event):
            canvas.bind_all("<MouseWheel>", _on_mousewheel)

        def _unbind_mousewheel(event):
            canvas.unbind_all("<MouseWheel>")


        canvas.bind("<Enter>", _bind_mousewheel)
        canvas.bind("<Leave>", _unbind_mousewheel)


        def on_resize(event):
            """
            Skaliert das fenster mit der Fenstergröße
            :param event: Resize event
            :return:
            """
            canvas_width = event.width
            canvas.itemconfig(canvas_frame_window, width=canvas_width)
            update_wraplength()
            update_scrollregion()

        canvas_frame_window = canvas.create_window((0, 0), window=content_frame, anchor="nw",
                                                   width=canvas.winfo_width())
        canvas.bind("<Configure>", on_resize)
    def _add_node_management_tab(self, notebook, custom_font):
        """
        Fügt Graphen Aufbaue tab hinzu
        :param notebook: Notebook
        :param custom_font: font
        :return:
        """
        node_tab = ttk.Frame(notebook)
        notebook.add(node_tab, text="Graphen Aufbau")


        canvas_frame = Frame(node_tab)
        canvas_frame.pack(fill="both", expand=True)

        canvas = Canvas(canvas_frame)
        scrollbar = Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        content_frame = Frame(canvas)
        canvas.create_window((0, 0), window=content_frame, anchor="nw")


        def update_scrollregion(event=None):
            """
            Updated die Scrollregion des Fensters
            :param event:
            :return:
            """
            canvas.configure(scrollregion=canvas.bbox("all"))


        content_frame.bind("<Configure>", update_scrollregion)


        def update_wraplength(event=None):
            new_width = content_frame.winfo_width() - 40
            for label in content_frame.winfo_children():
                if isinstance(label, Label):
                    label.config(wraplength=new_width)
            update_scrollregion()


        content_frame.bind("<Configure>", update_wraplength)


        Label(content_frame, text="Knoten", font=("Arial", 14, "bold")).pack(anchor="w", pady=(10, 0))

        node_canvas = Canvas(content_frame, bg="white", height=200)
        node_canvas.pack(fill="both", expand=True, pady=5)

        def draw_single_node():
            """
            Zeichnet einen Knoten zur Hilfe
            :return:
            """

            node_canvas.delete("all")
            canvas_width = node_canvas.winfo_width()
            canvas_height = node_canvas.winfo_height()

            node_radius = 30
            x, y = canvas_width // 2, canvas_height // 2


            node_canvas.create_oval(x - node_radius, y - node_radius, x + node_radius, y + node_radius,
                                    fill="lightblue")
            node_canvas.create_text(x, y - 12, text="1", font=("Arial", 14, "bold"))
            node_canvas.create_text(x, y + 12, text="5", font=("Arial", 12))
            node_canvas.create_text(x + node_radius + 60, y - 12, text="Knoten Name", anchor="w", font=("Arial", 10))
            node_canvas.create_text(x + node_radius + 60, y + 12, text="Distanz vom Startknoten", anchor="w",
                                    font=("Arial", 10))

        node_canvas.bind("<Configure>", lambda e: draw_single_node())


        Label(content_frame, text="Knotenerstellung:", font=("Arial", 12, "bold")).pack(anchor="w", pady=(5, 0))
        Label(content_frame,
              text="- Linksklick zum Erstellen eines Knotens.",
              justify="left", font=custom_font, wraplength=400).pack(anchor="w", pady=(0, 5))

        Label(content_frame, text="Knoten Löschen:", font=("Arial", 12, "bold")).pack(anchor="w", pady=(5, 0))
        Label(content_frame,
              text="- Mittelklick oder Strg + Linksklick, um einen Knoten zu löschen.",
              justify="left", font=custom_font, wraplength=400).pack(anchor="w", pady=(0, 5))

        Label(content_frame, text="Knoten Bewegen:", font=("Arial", 12, "bold")).pack(anchor="w", pady=(5, 0))
        Label(content_frame,
              text="- Linksklick gedrückt halten, um Knoten zu verschieben.",
              justify="left", font=custom_font, wraplength=400).pack(anchor="w", pady=(0, 5))

        Label(content_frame, text="Startknoten Wählen:", font=("Arial", 12, "bold")).pack(anchor="w", pady=(5, 0))
        Label(content_frame,
              text="- Doppel-Linksklick auf einen Knoten, um diesen als Startknoten zu setzen.",
              justify="left", font=custom_font, wraplength=400).pack(anchor="w", pady=(0, 15))


        Label(content_frame, text="Kanten und Gewichte:", font=("Arial", 14, "bold")).pack(anchor="w", pady=(10, 0))

        edge_canvas = Canvas(content_frame, bg="white", height=200)
        edge_canvas.pack(fill="both", expand=True, pady=5)

        def draw_edge_example():
            """
            Zeichnet eine Kante zur Hilfe
            :return:
            """
            edge_canvas.delete("all")
            canvas_width = edge_canvas.winfo_width()
            canvas_height = edge_canvas.winfo_height()

            node_radius = 30
            y = canvas_height // 2

            x1 = canvas_width // 4
            x2 = canvas_width * 3 // 4

            middle_x, middle_y = (x1 + x2) / 2, y


            line_start_x = x1 + node_radius
            line_end_x = x2 - node_radius


            edge_canvas.create_line(line_start_x, y, middle_x - 50, middle_y, width=4, fill="black", smooth=True,
                                    splinesteps=500)
            edge_canvas.create_line(middle_x + 50, middle_y, line_end_x, y, width=4, arrow="last",
                                    arrowshape=(10, 12, 5),
                                    fill="black", smooth=True, splinesteps=500)
            edge_canvas.create_text(middle_x, middle_y, text="7", fill="black", font=("Arial", 12))


            for x, label, distance in [(x1, "1", "5"), (x2, "2", "∞")]:
                edge_canvas.create_oval(x - node_radius, y - node_radius, x + node_radius, y + node_radius,
                                        fill="lightblue")
                edge_canvas.create_text(x, y - 12, text=label, font=("Arial", 14, "bold"))
                edge_canvas.create_text(x, y + 12, text=distance, font=("Arial", 12))

        edge_canvas.bind("<Configure>", lambda e: draw_edge_example())


        Label(content_frame, text="Kantenerstellung:", font=("Arial", 12, "bold")).pack(anchor="w", pady=(5, 0))
        Label(content_frame,
              text="- Rechtsklick auf einen Knoten startet die Kantenerstellung.\n"
                   "- Rechtsklick auf einen anderen Knoten erstellt die Kante.",
              justify="left", font=custom_font, wraplength=400).pack(anchor="w", pady=(0, 5))

        Label(content_frame, text="Kantengewichte:", font=("Arial", 12, "bold")).pack(anchor="w", pady=(5, 0))
        Label(content_frame,
              text="- Während der Kantenerstellung wird der Nutzer nach einem Gewicht für die Kante gefragt.\n"
                   "- Falls die zufällige Gewichte Option aktiviert ist, wird ein zufälliges Gewicht verwendet.",
              justify="left", font=custom_font, wraplength=400).pack(anchor="w", pady=(0, 5))

        Label(content_frame, text="Kantenrichtung:", font=("Arial", 12, "bold")).pack(anchor="w", pady=(5, 0))
        Label(content_frame,
              text="- Der Pfeil am Ende der Kante zeigt die Richtung der Kante an.",
              justify="left", font=custom_font, wraplength=400).pack(anchor="w", pady=(0, 15))


        def _on_mousewheel(event):
            """
            Fügt Mousebinds hinzu
            :param event: mouseevent
            :return:
            """
            canvas.yview_scroll(-1 * (event.delta // 120), "units")

        def _bind_mousewheel(event):
            """
            Bindet wheel, solange maus in dem fenster ist
            :param event:
            :return:
            """
            canvas.bind_all("<MouseWheel>", _on_mousewheel)

        def _unbind_mousewheel(event):
            """
            Unbinded Mauswheel, falls sie das Fenster verlässt
            :param event:
            :return:
            """
            canvas.unbind_all("<MouseWheel>")


        canvas.bind("<Enter>", _bind_mousewheel)
        canvas.bind("<Leave>", _unbind_mousewheel)


        def on_resize(event):
            """
            Methode zur Skalierung des Fensters
            :param event: Resize event
            :return:
            """
            canvas_width = event.width
            canvas.itemconfig(canvas_frame_window, width=canvas_width)
            update_wraplength()
            update_scrollregion()

        canvas_frame_window = canvas.create_window((0, 0), window=content_frame, anchor="nw",
                                                   width=canvas.winfo_width())
        canvas.bind("<Configure>", on_resize)

    def _add_button_explanations_tab(self, notebook, custom_font):
        """
        Fügt einen Tab hinzu der die buttons erklärt
        :param notebook:
        :param custom_font:
        :return:
        """
        button_tab = ttk.Frame(notebook)
        notebook.add(button_tab, text="Schaltflächen Erklärungen")

        canvas_frame = Frame(button_tab)
        canvas_frame.pack(fill="both", expand=True)

        canvas = Canvas(canvas_frame)
        scrollbar = Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        content_frame = Frame(canvas)
        canvas.create_window((0, 0), window=content_frame, anchor="nw")

        def update_scrollregion(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))

        content_frame.bind("<Configure>", update_scrollregion)

        def update_wraplength(event=None):
            new_width = content_frame.winfo_width() - 40
            for label in content_frame.winfo_children():
                if isinstance(label, Label):
                    label.config(wraplength=new_width)
            update_scrollregion()

        content_frame.bind("<Configure>", update_wraplength)

        Label(content_frame, text="Schaltflächen und ihre Funktionen:", font=("Arial", 14, "bold")).pack(anchor="w",
                                                                                                         pady=(10, 0))


        prev_button = Button(content_frame, image=self.prev_icon)
        prev_button.pack(anchor="w", pady=(5, 0))
        Label(content_frame,
              text="- Geht einen Schritt im Algorithmus zurück.",
              justify="left", font=custom_font, wraplength=750).pack(anchor="w", pady=(0, 5))


        next_button = Button(content_frame, image=self.next_icon)
        next_button.pack(anchor="w", pady=(5, 0))
        Label(content_frame,
              text="- Geht einen Schritt im Algorithmus vorwärts.",
              justify="left", font=custom_font, wraplength=750).pack(anchor="w", pady=(0, 5))


        pause_button = Button(content_frame, image=self.pause_icon)
        pause_button.pack(anchor="w", pady=(5, 0))
        Label(content_frame,
              text="- Pausiert die Ausführung des Algorithmus.",
              justify="left", font=custom_font, wraplength=750).pack(anchor="w", pady=(0, 5))


        fast_forward_button = Button(content_frame, image=self.fast_forward_icon)
        fast_forward_button.pack(anchor="w", pady=(5, 0))
        Label(content_frame,
              text="- Startet die automatische Wiedergabe des Algorithmus.",
              justify="left", font=custom_font, wraplength=750).pack(anchor="w", pady=(0, 5))


        start_button = Button(content_frame, image=self.start_icon)
        start_button.pack(anchor="w", pady=(5, 0))
        Label(content_frame,
              text="- Startet den ausgewählten Algorithmus.",
              justify="left", font=custom_font, wraplength=750).pack(anchor="w", pady=(0, 5))


        shortest_paths_button = Button(content_frame, image=self.shortest_paths_icon)
        shortest_paths_button.pack(anchor="w", pady=(5, 0))
        Label(content_frame,
              text="- Zeigt die kürzesten Pfade an (verfügbar nach Abschluss des Algorithmus).",
              justify="left", font=custom_font, wraplength=750).pack(anchor="w", pady=(0, 5))


        cancel_button = Button(content_frame, image=self.cancel_icon)
        cancel_button.pack(anchor="w", pady=(5, 0))
        Label(content_frame,
              text="- Bricht die aktuelle Ausführung des Algorithmus ab.",
              justify="left", font=custom_font, wraplength=750).pack(anchor="w", pady=(0, 15))

        def _on_mousewheel(event):
            canvas.yview_scroll(-1 * (event.delta // 120), "units")

        def _bind_mousewheel(event):
            canvas.bind_all("<MouseWheel>", _on_mousewheel)

        def _unbind_mousewheel(event):
            canvas.unbind_all("<MouseWheel>")

        canvas.bind("<Enter>", _bind_mousewheel)
        canvas.bind("<Leave>", _unbind_mousewheel)

        def on_resize(event):
            canvas_width = event.width
            canvas.itemconfig(canvas_frame_window, width=canvas_width)
            update_wraplength()
            update_scrollregion()

        canvas_frame_window = canvas.create_window((0, 0), window=content_frame, anchor="nw",
                                                   width=canvas.winfo_width())
        canvas.bind("<Configure>", on_resize)

    def _add_heap_description_tab(self, notebook, custom_font):
        """
        Fügt einen Tab hinzu der den Heap erklärt
        :param notebook:
        :param custom_font:
        :return:
        """
        features_tab = ttk.Frame(notebook)
        notebook.add(features_tab, text="Heap Erklärungen")

        description_text = (
            "Der Heap wird als Binärbaum dargestellt. Jeder Knoten v hat die Form:\n"
            "(v, d[v])\n"
        )

        Label(features_tab, text=description_text, justify="left", wraplength=750, font=custom_font).pack(padx=20,
                                                                                                          pady=10)

        canvas_frame = ttk.Frame(features_tab)
        canvas_frame.pack(pady=10)

        example_canvas = Canvas(canvas_frame, width=400, height=250, bg="white")
        example_canvas.pack()

        example_priority_queue = [(1, 1), (3, 2), (5, 3), (4, 4), (6, 5), (7, 6)]

        def draw_example_priority_queue():
            """
            Zeichnet bespiel heap
            :return:
            """
            example_canvas.delete("all")

            if not example_priority_queue:
                return

            canvas_width = example_canvas.winfo_width()
            canvas_height = example_canvas.winfo_height()

            if canvas_width <= 1 or canvas_height <= 1:
                example_canvas.after(100, draw_example_priority_queue)
                return

            num_levels = math.floor(math.log2(len(example_priority_queue))) + 1
            nodes_on_widest_level = 2 ** (num_levels - 1)

            node_size_x = canvas_width / (nodes_on_widest_level * 2)
            node_size_y = canvas_height / (num_levels * 3)
            node_size = min(min(node_size_x, node_size_y), 35)

            font_size = max(1, int(node_size // 2))
            horizontal_spacing = canvas_width / (2 ** num_levels)
            vertical_spacing = canvas_height / (num_levels + 1)

            def draw_node(x, y, text):
                """
                Zeichnet Knoten
                :param x: x koordinate
                :param y: y koordinate
                :param text: Beschriftung
                :return:
                """
                color = "lightgrey"
                example_canvas.create_oval(
                    x - node_size, y - node_size, x + node_size, y + node_size, fill=color
                )
                example_canvas.create_text(x, y, text=text, font=("Arial", font_size), fill="black")

            def draw_tree(index, x, y, dx):
                """
                Zeichnet rekursiv den Heap als Baum
                :param index: aktueller index
                :param x: x koordinate
                :param y: y koordinate
                :param dx: offset
                :return:
                """
                if index >= len(example_priority_queue):
                    return

                node = example_priority_queue[index]
                draw_node(x, y, f"{node[1]}, {node[0]}")

                left_child_idx = 2 * index + 1
                right_child_idx = 2 * index + 2

                if left_child_idx < len(example_priority_queue):
                    left_x, left_y = x - dx, y + vertical_spacing
                    example_canvas.create_line(x, y + node_size, left_x, left_y - node_size)
                    draw_tree(left_child_idx, left_x, left_y, dx / 2)

                if right_child_idx < len(example_priority_queue):
                    right_x, right_y = x + dx, y + vertical_spacing
                    example_canvas.create_line(x, y + node_size, right_x, right_y - node_size)
                    draw_tree(right_child_idx, right_x, right_y, dx / 2)

            root_x = canvas_width // 2
            root_y = vertical_spacing
            initial_dx = canvas_width / 4

            draw_tree(0, root_x, root_y, initial_dx)

        draw_example_priority_queue()

    def undo_last_operation(self, event=None):
        """
        Strg+z Methode die Knoten erstellung/kanten erstellung rückgängig macht
        :param event: strg + z
        :return:
        """
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
        """
        Entfernt das element an geklickter Position
        :param event: klick koordinaten
        :return:
        """
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
        """
        Entfernt Tupel aus der History, wird für strg+ z genutzt
        :param op_type: Typ der Operation
        :param item: Item, was gelöscht wird
        :return:
        """
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
        """
        Löscht den Knoten
        :param node: Knoten der gelöscht werden soll
        :return:
        """
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
        self.update_avai_ids()

    #Öffnet Einstellungsmenu, welches den Debug mode, random mode und Animationspeed einstellen lässt und in der Config.json speichert.
    def open_settings(self):
        """
        Öffnet Einstellungsfenster
        :return:
        """
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
            """
            Mousewheel binds um scrolling zu ermöglichen
            :param event: mousewheel
            :return:
            """

            general_tab_canvas.yview_scroll(-1 * (event.delta // 120), "units")


        general_tab_frame.bind("<Enter>", lambda e: settings_window.bind_all("<MouseWheel>", on_mousewheel))
        general_tab_frame.bind("<Leave>", lambda e: settings_window.unbind_all("<MouseWheel>"))

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
            """
            Validiert das input, sodass keine invaliden Werte eingefügt werden können
            :param new_val: Objekt was validiert werden solll
            :return:
            """
            return new_val == "" or new_val.isdigit()

        validate_command = settings_window.register(validate_input)

        max_weight_entry_field = Entry(random_checkbox_frame, textvariable=max_weight_var, width=10, validate="key",
                                       validatecommand=(validate_command, "%P"))
        max_weight_entry_field.grid(row=0, column=1)
        max_weight_label = Label(random_checkbox_frame, text="Maximales Gewicht (<100000)")
        max_weight_label.grid(row=0, column=2)



        def save_default_graph_to_parent():
            """
            Speichert den aktuellen Graph als Standardgraph
            :return:
            """

            try:

                scale_x = 1000 / self.parent.gui_frame.canvas_width
                scale_y = 1000 / self.parent.gui_frame.canvas_height


                self.parent.default_graph_pos = {
                    node: (x * scale_x, y * scale_y) for node, (x, y) in self.parent.node_positions.items()
                }

                self.parent.default_graph = self.parent.graph.copy()

                if self.parent.debug:
                    print("Default graph updated successfully.")
            except Exception as e:
                print(f"Error saving default graph: {e}")

        save_cur_a_d_button = Button(
            general_tab_frame,
            text="Aktuellen Graphen als Standardgraph Speichern",
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
            """
            Updated den Text des Speedlabels, sodass es immer den aktuellen wert zeigt
            :param args:
            :return:
            """
            speed_label.config(text=f"Verzögerung bei Vorspul Wiedergabe: {speed_var.get()} ms")

        speed_var.trace_add("write", update_speed_label)

        Label(general_tab_frame, text="Font Größe:").pack(pady=10)
        font_var = IntVar(value=self.parent.font_size)
        font_slider = ttk.Scale(
            general_tab_frame, from_=8, to=25, orient="horizontal", length=300, variable=font_var
        )
        font_slider.pack(pady=10)
        font_label = Label(general_tab_frame, text=f"Aktuelle Font Größe: {font_var.get()}")
        font_label.pack()

        def update_font_label(*args):
            """
            Updated den Text des Fontlabels, sodass es immer den aktuellen wert zeigt
            :param args:
            :return:
            """
            font_label.config(text=f"Aktuelle Font Größe: {font_var.get()}")

        font_var.trace_add("write", update_font_label)


        settings_window.grid_rowconfigure(0, weight=1)
        settings_window.grid_columnconfigure(0, weight=1)

        def apply_settings():
            """
            Speichert die Variablen des Settingsfenster in der Hauptklasse
            :return:
            """
            self.parent.random_edge_mode = random_mode_var.get()
            self.parent.animation_speed = speed_var.get()
            self.parent.font_size = font_var.get()
            max_edge_weight = max_weight_var.get()

            if max_edge_weight < 0 or max_edge_weight >= 100000:

                messagebox.showerror("Ungültige Eingabe", "Maximales Kantengewicht muss <100000 sein")
                return
            self.parent.max_edge_weight = max_weight_var.get()

            self.parent.save_config()
            settings_window.destroy()
            self.parent.update_gui()


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
        notebook.add(color_tab, text="Farbeinstellungen")

        def choose_color(element):
            """
            Colourpicker, die mit den colour buttons verbunden ist.
            :param element:
            :return:
            """
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
            """
            Setzt die Farben auf Standardwerte zurück
            :return:
            """

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
            """
            Erstellt die Farbbuttons
            :param frame: Frame auf dem die Buttons sind
            :param text: Display text
            :param element: Name, um den Button zu steuern
            :return:
            """
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
        """
        start Algorithm Binding, nötig um die Parent Methode zu callen
        :param event: Canvas Bind
        :return:
        """
        if self.parent.debug:
            print("Beginne Algorithmus")

        self.parent.start_algorithm()
    def go_to_next_step(self, event):
        """
        1 Schritt vor Binding
        :param event: Canvas Bind
        :return:
        """
        if self.parent.debug:
            print("1 Schritt vor")

        self.parent.next_step()
    def go_step_back(self, event):
        """
        1 schritt zurück Binding
        :param event:
        :return:
        """
        if self.parent.debug:
            print("1 Schritt zurück")
        self.parent.prev_step()

    def go_forward_button(self):
        """
        Fast forward binding
        :return:
        """
        if self.parent.debug:
            print("Vorspulen aktiviert")
        self.parent.fast_forward_paused = False

        self.parent.fast_forward()
    def go_fast_forward(self, event):
        """
        2. Fast vorward Binding
        :param event:
        :return:
        """
        if self.parent.debug:
            print("Vorspulen aktiviert")
        self.parent.fast_forward_paused = False

        self.parent.fast_forward()
    def pause_fast_forward(self, event):
        """
        Pausiere fast forward Binding
        :param event:
        :return:
        """
        if self.parent.debug:
            print("Vorspulen pausiert")
        self.parent.pause()


    # gibt den aktuellen graphen auf der Konsole aus -> debug optionen
    def print_loaded_graph(self):
        """
        Debuf funktion die den aktuellen Graph auf der console ausgibt
        :return:
        """
        if self.parent.debug:
            print("Aktuell geladener Graph: ")
        print(self.parent.graph)
        print(self.parent.node_positions)
        print(self.parent.steps_finished_algorithm)

    # select dijkstra mit List as algorithm
    def toggle_dijk_L(self):
        """
        Binding mit der Algorithmusauswahl, hier wechsel zu Dijkstra mit Liste
        :return:
        """
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
        """
        Binding mit der Algorithmusauswahl, hier wechsel zu Dijkstra Lazy
        :return:
        """
        if self.parent.debug:
            print("Wechsel zu Dijkstra mit Priority Queue (Lazy Deletion)")
        self.parent.selected_algorithm = "Dijkstra_PQ_lazy"
        self.parent.code_frame.set_algorithm("Dijkstra_PQ_lazy")
        self.parent.reset()
        self.dijk_L.set(False)
        self.dijk_PQ.set(False)
        self.dijk_PQ_lazy.set(True)
    def toggle_dijk_PQ(self):
        """
        Binding mit der Algorithmusauswahl, hier wechsel zu Dijkstra mit PQ
        :return:
        """
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
        """
        Fügt knoten hinzu
        :param event: Koordinaten für den Knoten
        :return:
        """
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

        self.parent.selected_nodes = []
        self.parent.reset()
        self.update_avai_ids()


    def add_edge(self, event):
        """
        Wenn an dem Event ein Knoten ist, startet die Kanten erstellung, Klick auf 2. Knoten erstellt Kante. Klick auf
        Kante öffnet Kantengewichtanpassung.
        :param event: Koordinaten des klicks
        :return:
        """

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
        """
        Startet Kanten erstellungs Simulation
        :param start_node: Startknoten der Kante
        :return:
        """

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
        """
        Simuliert das Folgen der Maus von der simulierten Kante
        :param event: Koordinaten
        :return:
        """

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
        """
        Beendet die Kantenerstellung und erstellt die Kante
        :param node1: Startknoten
        :param node2: Zielknoten
        :return:
        """

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
        """
        Abbruch Binding der Kantenerstellung
        :param event: Linksklick
        :return:
        """

        if hasattr(self, "simulated_edge"):
            self.canvas.delete(self.simulated_edge)
            del self.simulated_edge
            self.canvas.bind("<ButtonPress-1>", self.on_press)

        self.parent.selected_nodes.clear()
        self.parent.reset()
    def ask_for_edge_weight(self):
        """
        Öffnet dialog, der den Nutzer auffordert ein Kantengewicht einzugeben, validiert außerdem die Eingabe, sodass nur int <99999 möglich ist
        :return:
        """

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
        """
        Gibt den Knoten an Position zurück
        :param x: x Koordinate
        :param y: y Koordinate
        :return: Knoten an Position x,y
        """

        for node, (nx, ny) in self.parent.node_positions.items():
            if math.hypot(nx - x, ny - y) <= 30:
                return node
        return None

    def add_or_update_edge(self, node1, node2, weight):
        """
        Erstellt Kante oder updated das Gewicht der Kante
        :param node1: Starknoten
        :param node2: Zielknoten
        :param weight: Gewicht
        :return:
        """

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
        """
        Gibt die Kante an Koordinaten zurück
        :param x: x Koordinate
        :param y: y Koordinate
        :return: Kante an Koordinate
        """
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



    def distance_to_edge(self, x, y, x2, y2, x3, y3):
        """
        Berechnet die Distanz von einem Punkt zu einer Linie
        :param x: x Koordinate
        :param y: y Koordinate
        :param x2: x Startknoten
        :param y2: y Startknoten
        :param x3: x Zielknoten
        :param y3: y Zielknoten
        :return: Distanz zur von einem Punkt zur Linie
        """
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
        """
        Öffnet Dateifenster, was dem Nutzer ermöglich den aktuellen Graphen als JSON zu speichern
        :return:
        """
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
            scale_x = 1000 / self.parent.gui_frame.canvas_width
            scale_y = 1000 / self.parent.gui_frame.canvas_height

            node_positions_upscaled = {
                node: (x * scale_x, y * scale_y) for node, (x, y) in self.parent.node_positions.items()
            }
            data = {
                "graph": self.parent.graph,
                "node_position": node_positions_upscaled
            }
            with open(filepath, 'w') as file:
                json.dump(data, file, indent=4)
            print(f"exported to {filepath}")
        except Exception as e:
            print(f"Error:{e}")

    # import funktion, um einen Graphen als .json zu importieren
    def import_graph(self):
        """
        Import einen Graphen im richtigen Format als JSON,
        :return:
        """
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
                graph = data["graph"]
                node_positions = data["node_position"]


                def is_valid_node_id(node_id):
                    return node_id.isdigit() and int(node_id) > 0

                valid_graph = all(
                    is_valid_node_id(node) and
                    all(is_valid_node_id(neighbor) and isinstance(weight, (int, float))
                        for neighbor, weight in neighbors.items())
                    for node, neighbors in graph.items()
                )

                valid_positions = all(
                    is_valid_node_id(node) and isinstance(pos, list) and len(pos) == 2
                    and all(isinstance(coord, (int, float)) for coord in pos)
                    for node, pos in node_positions.items()
                )

                if valid_graph and valid_positions:
                    max_x = max(x for x, y in node_positions.values())
                    max_y = max(y for x, y in node_positions.values())

                    if max_x > 1000 or max_y > 1000:
                        print("Fehlerhafte Input-Datei: Die Positionen des Graphen überschreiten das 1000x1000 Limit.")
                        return
                    self.parent.graph = graph
                    self.parent.node_positions = {node: tuple(pos) for node, pos in node_positions.items()}
                    if self.parent.debug:
                        print(f"Graph von {filepath} wurde erfolgreich importiert")
                    self.parent.scale_loaded_graph()
                    self.update_avai_ids()
                    self.operation_history = []
                    self.parent.reset()
                else:
                    print("Fehlerhafte Input-Datei: Knoten-IDs müssen numerisch sein und Positionen korrekt angegeben.")
            else:
                print("Fehlerhafte Input-Datei: 'graph' oder 'node_position' nicht gefunden")
        except Exception as e:
            print(f"Importing error: {e}")

    def generate_node_ids(self):
        """
        Erstellt die Liste von möglichen Knoten namen
        :return: Liste der Knotennamen
        """
        return [str(i) for i in range(1, 1000)]

    def reset_node_ids(self):
        """
        Setzt der verfügbaren Knotennamen zurück
        :return:
        """
        self.node_flags = {node_id: True for node_id in self.generate_node_ids()}

    def get_next_id(self):
        """
        Gibt den nächsten Knoten namen zurück
        :return: Knotenname für den nächsten Knoten
        """
        for node_id, is_available in sorted(self.node_flags.items(), key=lambda x: int(x[0])):
            if is_available:
                self.node_flags[node_id] = False
                return node_id
        raise ValueError("Keine verfügbaren Knoten-IDs mehr.")

    def set_node_availability(self, node_id, available):
        """
        Setzt den Knoten namen auf verfügbar
        :param node_id: Knotenname
        :param available: Verfügbar flag
        :return:
        """
        if node_id in self.node_flags:
            self.node_flags[node_id] = available
        else:
            raise ValueError(f"Node ID {node_id} does not exist.")

    def update_avai_ids(self):
        """
        Updated verfügbare Knoten, wird beim Import genutzt
        :return:
        """
        imported_nodes = self.parent.node_positions.keys()
        for node_id in self.node_flags:
            self.node_flags[node_id] = node_id not in imported_nodes
        if self.parent.debug:
            print(self.node_flags)