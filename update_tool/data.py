import io
import os
import zipfile
from contextlib import closing
import msgpack


def zip_from_folder(basedir):
    buffer = io.BytesIO()

    with closing(zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED)) as z:
        for root, dirs, files in os.walk(basedir):
            # NOTE: ignore empty directories
            for fn in files:
                absfn = os.path.join(root, fn)
                zfn = absfn[len(basedir)+len(os.sep):]  # XXX: relative path
                z.write(absfn, zfn)

    return buffer


class UpdateObject:
    def __init__(self, ziph, signature, startup, destination_folder, autostart_file):
        self.autostart_file = autostart_file
        self.destination_folder = destination_folder
        self.startup = startup
        self.zip = ziph
        self.signature = signature

    def save(self, target):
        payload = {
            "autostart_file": self.autostart_file,
            "destination_folder": self.destination_folder,
            "startup": self.startup,
            "zip": self.zip,
            "signature": self.signature
        }

        stream = open(target, "wb")
        msgpack.pack(payload, stream=stream)
