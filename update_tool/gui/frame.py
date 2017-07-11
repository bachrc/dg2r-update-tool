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

        self.commands_default = "midori -a /usr/local/share/app/index.html -e Fullscreen"
        self.commands_text = None

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
        self.path_key_text = StringVar(self.master, "Aucun fichier sélectionné")
        Label(self.master, textvariable=self.path_key_text).grid(row=6, column=1, columnspan=3, sticky=W)

        Label(self.master, text="Passphrase :").grid(row=7, column=0, sticky=W + E)
        Entry(self.master, textvariable=self.passphrase_text).grid(row=7, column=1, columnspan=3, sticky=W + E)

        ttk.Separator(self.master).grid(row=8, columnspan=4, sticky=E + W, pady=10)

        Label(self.master, text="Commandes au démarrage") \
            .grid(row=9, columnspan=4, sticky=W)
        self.commands_text: Text = Text(self.master, height=3, width=60, wrap=NONE)
        self.commands_text.insert(INSERT, self.commands_default)
        self.commands_text.grid(row=10, column=0, columnspan=4, rowspan=3, sticky=W + E)

        Label(self.master, text="Dossier d'extraction").grid(row=13, column=0, sticky=W, pady=10)
        Entry(self.master, textvariable=self.extract_folder).grid(row=13, column=1, sticky=W + E)

        Label(self.master, text="Chemin du fichier d'autodémarrage").grid(row=14, column=0, sticky=W, pady=10)
        Entry(self.master, textvariable=self.autostart).grid(row=14, column=1, columnspan=3, sticky=W + E)

        ttk.Separator(self.master).grid(row=15, columnspan=4, sticky=E + W, pady=10)

        Button(self.master, text="Créer le fichier de mise à jour",
               command=self.create_update).grid(row=16, columnspan=4, sticky=W + E)

    def load_folder(self):
        """
        Displays a window which asks for the application folder
        """

        fname = askdirectory(initialdir=(os.path.dirname(os.path.realpath(__file__))
                                         if self.path_text is None else self.path_text.get()),
                             title="Choisissez un dossier")

        if fname:
            self.path_text.set("Dossier chargé : {}".format(fname))
            self.master.update()

    def load_private_key(self):
        """
        Displays a window which asks for the private key's location
        """

        fname = askopenfilename(initialdir=os.path.dirname(os.path.realpath(__file__)), title="Choisissez un dossier")

        if fname:
            self.path_key_text.set("Dossier chargé : {}".format(fname))
            self.master.update()

    def create_update(self):
        """
        Begins the update creation procedure
        """
        return


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
