import os
import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
from tkinter.filedialog import askdirectory, askopenfilename


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        # Variables for UI
        self.path_text = None
        self.path_key_text = None
        self.passphrase_text = None

        self.commands = StringVar(master, "midori -a /usr/local/share/app/index.html -e Fullscreen")
        self.extract_folder = StringVar(master, "/usr/local/share/app")
        self.autostart = StringVar(master, "/home/DG2R/.config/lxsession/LXDE/autostart")

        self.create_widgets()


    def create_widgets(self):
        """
        Create the widgets of the main interface
        """

        Label(self.master, text="DG2R Update Tool", font=("fixedsys", 17)) \
            .grid(row=0, sticky=W+N+E+S, columnspan=4, padx=15, pady=15)

        ttk.Separator(self.master).grid(row=1, columnspan=4, sticky=E + W, pady=10)

        Label(self.master, text="Selectionnez le dossier à téléverser", font="bold")\
            .grid(row=2, columnspan=4, sticky=W)

        Button(self.master, text="Parcourir", command=self.load_folder).grid(row=3, column=0, sticky=W)
        self.path_text = StringVar(self.master, "Aucun fichier sélectionné")
        Label(self.master, textvariable=self.path_text).grid(row=3, column=1, columnspan=3, sticky=W)

        ttk.Separator(self.master).grid(row=4, columnspan=4, sticky=E + W, pady=10)

        Label(self.master, text="Sélectionnez votre clé privée", font="bold") \
            .grid(row=5, columnspan=4, sticky=W)

        Button(self.master, text="Parcourir", command=self.load_private_key).grid(row=6, column=0, sticky=W)
        self.path_text = StringVar(self.master, "Aucun fichier sélectionné")
        Label(self.master, textvariable=self.path_text).grid(row=6, column=1, columnspan=3, sticky=W)

        Label(self.master, text="Passphrase :").grid(row=7, column=0, sticky=W + E)
        Entry(self.master).grid(row=7, column=1, columnspan=3, sticky=W + E, textvariable=self.passphrase_text)

        ttk.Separator(self.master).grid(row=4, columnspan=4, sticky=E + W, pady=10)

        Label(self.master, text="Commandes au démarrage") \
            .grid(row=5, columnspan=4, sticky=W)
        Text(self.master, textvariable=self.commands).grid(row=7, column=1, columnspan=3, rowspan=2, sticky=W + E)

    def load_folder(self):
        """
        Charge un fichier de données afin de démarrer le plot
        """

        fname = askdirectory(initialdir=(os.path.dirname(os.path.realpath(__file__))
                                         if self.path_text is None else self.path_text.get()),
                             title="Choisissez un dossier")

        if fname:
            self.path_text.set("Dossier chargé : {}".format(fname))
            self.master.update()


    def load_private_key(self):
        """
        Charge un fichier de données afin de démarrer le plot
        """

        fname = askopenfilename(initialdir=os.path.dirname(os.path.realpath(__file__)), title="Choisissez un dossier")

        if fname:
            self.path_key_text.set("Dossier chargé : {}".format(fname))
            self.master.update()



def launch_gui():
    """
    Method launching the GUI
    """
    root = tk.Tk()
    root.wm_title("DG2R Update Tool")

    root.grid_columnconfigure(1, weight=1)

    app = Application(master=root)

    def on_close():
        if messagebox.askokcancel("Quitter", "Voulez-vous vraiment quitter l'application ?"):
            root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)

    app.mainloop()

# Oui
