import os
import tkinter as tk
import traceback
from os.path import expanduser
from tkinter import *
from tkinter import ttk, messagebox, filedialog
from tkinter.filedialog import askdirectory, askopenfilename

from pathlib import Path

from update_tool.crypto import sign_file
from update_tool.data import zip_from_folder, UpdateObject


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        # Variables for UI
        self.path_text = None
        self.path_key_text = None
        self.passphrase_text = StringVar()

        self.path_update = None
        self.path_key = None

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

        fname = askdirectory(initialdir=expanduser("~"),
                             title="Choisissez un dossier")

        if fname:
            self.path_text.set("Dossier chargé : {}".format(fname))
            self.path_update = fname
            self.master.update()

    def load_private_key(self):
        """
        Displays a window which asks for the private key's location
        """

        fname = askopenfilename(initialdir=expanduser("~"), title="Choisissez un dossier")

        if fname:
            self.path_key_text.set("Dossier chargé : {}".format(fname))
            self.path_key = fname
            self.master.update()

    def create_update(self):
        """
        Begins the update creation procedure
        """
        if self.path_update is None or self.path_key is None:
            messagebox.showwarning(
                "Valeurs incorrectes",
                "Le dossier de mise à jour ou la clé privée sont manquantes."
            )
            return

        path_folder = Path(self.path_update)
        path_key = Path(self.path_key)

        if not path_folder.is_dir():
            messagebox.showwarning(
                "Valeurs incorrectes",
                "Le dossier de mise à jour n'est pas un dossier valide."
            )
            return

        if not path_key.is_file():
            messagebox.showwarning(
                "Valeurs incorrectes",
                "La clé privée de DG2R n'est pas un fichier valide."
            )
            return

        try:
            zipfile = zip_from_folder(str(path_folder))
            signed_zip = sign_file(zipfile.getvalue(), str(path_key), self.passphrase_text.get())

            f = filedialog.asksaveasfilename(defaultextension=".dg2r", filetypes=[("Fichier de mise à jour", ".dg2r")],
                                             initialfile="UPDATE.dg2r")

            to_save = UpdateObject(zipfile.getvalue(), signed_zip, self.commands_text.get("1.0", 'end-1c'),
                                   self.extract_folder.get(), self.autostart.get())
            to_save.save(f)

            messagebox.showinfo("Fichier créé !", "Fichier de mise à jour créé avec succès ! Mettez le sur une clé USB")

        except Exception as e:
            traceback.print_exc()
            messagebox.showerror(
                "Création de mise à jour échouée",
                str(e)
            )
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
