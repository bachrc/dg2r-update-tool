import os
import zipfile


def zip_from_folder(folder_path):
    try:
        ziph = zipfile.ZipFile("UPDATE.zip", "w", zipfile.ZIP_DEFLATED)

        for root, dirs, files in os.walk(folder_path):
            for file in files:
                ziph.write(os.path.join(root, file))

        return ziph
    except:
        raise Exception("Erreur lors de la création de l'archive.")
