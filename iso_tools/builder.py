import os

import pycdlib


def build_iso(output_iso="recompiled.iso"):
    if os.path.exists(output_iso):
        print("Le fichier ISO recompilé est déjà présent :", output_iso)
        return output_iso

    print("Création du nouvel ISO...")

    new_iso = pycdlib.PyCdlib()
    new_iso.new(interchange_level=3, vol_ident="MYISO")

    new_iso.write(output_iso)
    new_iso.close()

    return output_iso
