import os
import subprocess

import pycdlib


def extract_iso(filename, output_dir="iso_extracted"):
    iso = pycdlib.PyCdlib()
    iso.open(filename)

    os.makedirs(output_dir, exist_ok=True)

    for dirpath, dirnames, filenames in iso.walk(iso_path="/"):
        rel_path = dirpath.lstrip("/")
        target_dir = os.path.join(output_dir, rel_path)
        os.makedirs(target_dir, exist_ok=True)

        for fname in filenames:
            iso_path = os.path.join(dirpath, fname)
            record = iso.get_record(iso_path=iso_path)
            if record.is_symlink():
                print(f"Ignoré (symlink) : {iso_path}")
                continue

            target_file = os.path.join(target_dir, fname.strip(";1"))
            with open(target_file, "wb") as f:
                iso.get_file_from_iso_fp(f, iso_path=iso_path)

    iso.close()
    print(f"Tous les fichiers ont été extraits dans {output_dir}")

    return output_dir


def extract_squashfs(squashfs_path, output_dir="iso_extracted/squashfs-root"):
    if os.path.exists(output_dir):
        print(f"[*] Le dossier {output_dir} existe déjà, suppression...")
        subprocess.run(["sudo", "rm", "-rf", output_dir], check=True)

    print(f"[*] Extraction de {squashfs_path} vers {output_dir}...")
    subprocess.run(["sudo", "unsquashfs", "-d", output_dir, squashfs_path], check=True)

    print("[*] Extraction terminée")
