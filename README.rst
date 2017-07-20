================
DG2R Update Tool
================

This tool is supposed to help people creating update packages which installs automatically the update package on a Linux
when an USB key is plugged in.

Install
=======

To use this tool, you need to have Python 3.5 or newer.

In order to install it, you'll have to traditionnaly install it with the ``setup.py``.

.. code-block:: bash

    sudo python3 setup.py install

You now can launch the gui anywhere by typing ``dg2r_update_tool``.

Usage
=====

When the software displays, you must put multiple values in order to create your update :

Update folder
    You must select the folder containing your app

Private key
    This private key is used to verify the zip file, to ensure that the update is coming from you.

Startup commands
    This textbox includes the commands launched at the Armadillo start. In the default commands, ``midori`` is launched
    in fullscreen with the ``index.html`` file located under ``/usr/local/share/app``.

Destination folder
    Because, yes, unbelievable, you can choose the destination folder for the extraction. The default configured one
    is ``/usr/local/share/app``, but you can change it according to your needs. It must be a destination where the
    Armadillo default user have write permissions, or else the update will fail, because he couldn't write it.

Autostart file
    Because there's a file with the autostart instruction, you'll need to inquire the file's location. By default, the
    autostart file is correct, but if you need it to change, you can do it.