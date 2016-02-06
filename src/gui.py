import Tkinter as tk
import numpy as np
import matplotlib
matplotlib.use("TkAgg")

import matplotlib.pyplot as plt
import main
from utils import split
from transaction import get_cumulative_amount
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from tkFileDialog import askopenfilename

class Application(tk.Frame):

    def create_figure(self):
        self.figure = Figure(figsize=(5, 4), dpi=100)
        a = self.figure.add_subplot(111)
        t = np.arange(0.0, 3.0, 0.01)
        s = np.sin(2 * np.pi * t)
        a.plot(t, s)

    def fill_account_pane(self):
        for account in self.accounts:
            self.account_box.insert(tk.END, account)

    def draw_balance_plot(self):
        colors = ["b", "r"]
        if not hasattr(self, "history_plot"):
            self.history_plot = self.figure.add_subplot(111)
        self.history_plot.clear()
        for (index, (account, ts)) in enumerate(self.accounts.iteritems()):
            (dates, balances) = get_cumulative_amount(ts)
            self.history_plot.plot_date(dates, balances, colors[index] + "-")
        self.figure.canvas.draw()

    def open_file(self):
        path = askopenfilename()
        history = main.open_transaction_file(path)
        self.accounts = split(history, [lambda t: t.dest])
        self.fill_account_pane()
        self.draw_balance_plot()

    def create_layout(self):
        self.create_menu_bar()

        self.left = tk.Frame()
        self.left.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        self.account_box = tk.Listbox(self.left, selectmode=tk.EXTENDED)
        self.account_box.pack(fill=tk.BOTH, expand=True)

        self.right = tk.Frame()
        self.right.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        self.figure = plt.figure(figsize=(8, 8))

        self.canvas = FigureCanvasTkAgg(self.figure, master=self.right)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.canvas = FigureCanvasTkAgg(plt.figure(figsize=(4, 5)), master=self.right)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def create_menu_bar(self):
        menu_bar = tk.Menu(self.master)
        self.master.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff = 0)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.master = master
        self.create_figure()
        self.create_layout()

if __name__ == "__main__":
    root = tk.Tk()
    root.wm_title("Test")
    app = Application(root)
    app.mainloop()
    root.destroy()
