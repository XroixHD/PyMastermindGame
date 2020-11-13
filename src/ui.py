import math
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox

from src.config import Config, get_file_path
from src.mastermind import Mastermind


class Root(tk.Tk):
    """ The root / main window
    """

    def __init__(self):
        """ Initialize and declare all needed attributes and create widgets
        """
        super().__init__()

        self.title("Mastermind")
        self.geometry("500x500")
        self.resizable(False, False)

        # Config
        self.config = Config(self)

        # Mastermind
        self.mastermind = Mastermind.from_config(self, self.config)
        print("Secret Code:", self.mastermind.secret_code)

        # TODO: Remake dynamic size
        # padding = -9 + round(500 / (self.mastermind.len * 20))

        # Themed Tkinter settings + Style
        self.font = "Sans Serif"
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.style.configure("TButton", font=(self.font, 12), background="#ffffff", padding=[-6, 20, -5, 20])

        # Widgets
        # Title
        self.title_frame = tk.Frame(self, bg="#ffffff")

        # History stuff
        self.history_button = None
        self.history_window = HistoryWindow(self)

        # Answer
        self.answer_frame = tk.Frame(self, bg="#ffffff")
        self.answer_labels = {}
        self.answers_images = {
            0: tk.PhotoImage(file=get_file_path("../res/true.png")).subsample(5, 5),
            1: tk.PhotoImage(file=get_file_path("../res/blank.png")).subsample(5, 5),
            2: tk.PhotoImage(file=get_file_path("../res/false.png")).subsample(5, 5)
        }

        # Preview
        self.output_frame = tk.Frame(self, bg="#ffffff")
        self.color_labels = {}

        # Controls for user
        # Color buttons
        self.input_frame = tk.Frame(self, bg="#ffffff")
        self.color_buttons = {}

        # Control buttons
        self.continue_image = tk.PhotoImage(file=get_file_path("../res/continue.png")).subsample(5, 5)
        self.continue_button = None
        self.clear_image = tk.PhotoImage(file=get_file_path("../res/clear.png")).subsample(5, 5)
        self.clear_button = None

        # Create content
        self.create_widgets()

        # Save state
        self.config.save_state()

    def create_widgets(self):
        # Title frame
        tk.Label(self.title_frame, text="Mastermind", font=("Sans Serif", "45"), bg="#ffffff").pack(pady=10)

        self.history_button = tk.Button(self.title_frame, text="Open History", bg="#ffffff")
        self.history_button.bind("<Button-1>", self.button_history_invoke)
        self.history_button.pack(expand=False, ipadx=50, pady=20)

        self.title_frame.pack(expand=False, fill="both")

        # Answer frame
        self.answer_frame.pack(expand=True, fill="both")

        for i in range(self.mastermind.len):
            self.answer_labels.update({
                i: tk.Label(self.answer_frame, bg="#ffffff", relief="flat", image=self.answers_images[1])
            })
            self.answer_labels[i].pack(side="left", expand=True, fill="x", ipadx=0, ipady=0, padx=20, pady=0)

        # Output frame
        self.output_frame.pack(expand=True, fill="both")

        for i, color_name in enumerate(self.mastermind.COLORS):
            self.color_labels.update({
                color_name: tk.Label(self.output_frame, bg="#a1a1a1", relief="sunken")
            })
            self.color_labels[color_name].pack(side="left", expand=True, fill="x", ipadx=30, ipady=20, padx=10, pady=0)

        # Input frame
        self.input_frame.columnconfigure(2, weight=0)
        self.input_frame.rowconfigure(1, weight=1)

        tk.Label(self.input_frame, text="Controls:", font=(self.font, 14), bg="#ffffff").grid(column=0, row=0, pady=15)

        self.continue_button = tk.Button(self.input_frame, image=self.continue_image, bg="#ffffff", state="disabled")
        self.continue_button.bind("<Button-1>", self.button_continue_invoke)
        self.continue_button.grid(column=1, row=0)

        self.clear_button = tk.Button(self.input_frame, image=self.clear_image, bg="#ffffff")
        self.clear_button.bind("<Button-1>", self.button_clear_invoke)
        self.clear_button.grid(column=2, row=0)

        for i, color_name in enumerate(self.mastermind.COLORS):
            self.color_buttons.update({
                color_name: ttk.Button(self.input_frame, text=color_name, style="TButton")
            })
            setattr(self.color_buttons[color_name], "name", color_name)
            self.color_buttons[color_name].bind("<Button-1>", self.button_color_invoke)
            self.color_buttons[color_name].grid(column=i, row=1, sticky="news", ipady=1)

        self.input_frame.pack(side="bottom", fill="x")

    def reset_ui(self):
        """ Reactivates input color buttons & labels and resets answer display
        """
        # Activate input color buttons & labels
        for button_name in self.color_buttons:
            self.color_buttons[button_name].configure(state="normal")
            self.color_labels[button_name].configure(background="#a1a1a1")

        # Resets answer display
        for answer_index in self.answer_labels:
            self.answer_labels[answer_index].configure(image=self.answers_images[1])

    def button_history_invoke(self, e: tk.EventType):
        """ Open history
        """
        self.history_window.deiconify()

    def button_color_invoke(self, e: tk.EventType):
        """ Choose a color
        :param e: the event
        """
        if str(e.widget["state"]) == "disabled":
            return

        answers = []

        # Invoke press command from mastermind
        index = self.mastermind.press(e.widget.name)

        # If a round is finished
        if index + 1 == self.mastermind.len:
            # Check the code and get answers
            answers = self.mastermind.evaluate()

            # Deactivate color input buttons
            for button_name in self.color_buttons:
                self.color_buttons[button_name].configure(state="disabled")

            # Set answer display
            for answer_index in self.answer_labels:
                self.answer_labels[answer_index].configure(image=self.answers_images[answers[answer_index]])

            # Save history
            self.config.save_state()

            # Render history
            self.history_window.update_canvas(rerender=False)

            # Activate continue button
            self.continue_button.configure(state="normal")

            print(f"[Round] {self.mastermind.history[-1]['answer']}")

        # Change color of color button
        self.color_labels[self.mastermind.COLORS[index]].configure(
            background=self.mastermind.COLOR_CODES[e.widget.name])

        # If answers were all correct -> finish game
        if answers and all((x == 0 for x in answers)):
            print("Hooray you got it right!")

            if messagebox.askyesno("Hooray", f"You got it right! \nIt took you {math.floor(self.mastermind._i / self.mastermind.len)} rounds! \nDo you want to play again?"):
                # Clear root
                self.reset_ui()

                # Clear history ui
                self.history_window.clear_canvas()

                # Clear state
                self.mastermind.clear()
                self.config.save_state()
                print("New Secret Code:", self.mastermind.secret_code)

                # Update history window
                self.history_window.update_canvas(rerender=True)

            else:
                exit(0)

    def button_continue_invoke(self, e: tk.EventType, *, ignore=False):
        """ Continue button
        :param e: event obj
        :param ignore: if to ignore widget state check
        """
        # Return
        if not ignore and str(e.widget["state"]) == "disabled":
            return

        self.reset_ui()

        # Deactivate this button again
        e.widget.configure(state="disabled")

    def button_clear_invoke(self, e: tk.EventType, *, ignore=False):
        """ Continue button
        :param e: event obj
        :param ignore: if to ignore the user question
        """
        if ignore or messagebox.askyesno("Question", "Do you really want to clear this session?"):
            # Clear root ui
            self.reset_ui()

            # Clear history ui
            self.history_window.clear_canvas()

            # Clear state
            self.mastermind.clear()
            self.config.save_state()

            print("New Secret Code:", self.mastermind.secret_code)

            self.history_window.update_canvas(rerender=True)

        e.widget["state"] = "normal"


class HistoryWindow(tk.Toplevel):
    """ The history window which shows the history of guessed codes
    """

    def __init__(self, root, **kw):
        """ Initialize
        :param root: the root window
        """
        super().__init__(root, **kw)
        self.root = root

        self.protocol("WM_DELETE_WINDOW", self.withdraw)
        self.title("Mastermind History")
        self.geometry("500x250")
        self.resizable(False, True)

        self.font = self.root.font

        self.tree = None
        self.canvas = None
        self.scrollbar = None

        # List of lists for each history and their ids
        # last index is text id
        self.canvas_objs = []

        self.create_widgets()
        self.withdraw()

    def create_widgets(self):
        """ Create widgets
        """
        self.canvas = tk.Canvas(self, bg='#FFFFFF', width=480, height=1000)

        self.scrollbar = ttk.Scrollbar(self, orient="vertical")
        self.scrollbar.config(command=self.canvas.yview)

        self.canvas.config(width=480, height=1000)
        self.canvas.config(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.update_canvas(rerender=True)

    def update_canvas(self, rerender=False):
        """ Update history window
        :param rerender: If to rerender ALL, if False than only render new
        """

        size = 40
        pad_x = 0
        pad_y = 10
        base_x = 0
        base_y = 0
        pad_base_y = (len(self.canvas_objs)) * (size + pad_y) * (not rerender)

        # For reach code in history
        # If rerender False, than only in new history
        for i, d in enumerate(self.root.mastermind.history[len(self.canvas_objs) * int(not rerender):]):
            base_y = pad_base_y + i * (size + pad_y)
            temp_l = []

            # For each color in code
            for color_i, color_name in enumerate(d["code"].split(";")):
                base_x = color_i * (size + pad_x)

                temp_l.append(self.canvas.create_rectangle(base_x, base_y, base_x + size, base_y + size,
                                                           fill=self.root.mastermind.COLOR_CODES[color_name]))

            temp_l.append(self.canvas.create_text(round(base_x + ((500 - base_x) / 2) + 25), round(base_y + 40 / 2),
                                                  text=d["answer"],
                                                  font=(self.font, 14)))

            self.canvas_objs.append(temp_l)

            # Set canvas size (without last padding)
        self.canvas.configure(scrollregion=(0, 0, 500, base_y + size))

    def clear_canvas(self):
        """ Clear canvas
        """
        self.canvas.delete("all")
        self.canvas_objs = []

    def create_widgets_old(self):
        """ Create widgets
        """
        self.tree = ttk.Treeview(self, columns=("Answer",))
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)

        self.tree.configure(yscroll=self.scrollbar.set)
        self.tree.column("#0", width=166)
        self.tree.heading("#0", text="Code", anchor="w")
        self.tree.column("#1", width=166)
        self.tree.heading("#1", text="Answer", anchor="w")

        root_node = self.tree.insert('', 'end', text="1:", open=True)

        history = self.root.mastermind.history
        for i in history:
            self.tree.insert(root_node, 'end', text=i["code"], values=(i["answer"],), open=False)

        self.tree.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
