import os
import time
from urllib.request import urlretrieve


def download_iso(distro, version):
    url_map = {
        (
            "Ubuntu",
            "24.04 LTS with GNOME",
        ): "https://releases.ubuntu.com/24.04/ubuntu-24.04.3-desktop-amd64.iso"
    }

    url = url_map.get((distro, version))
    if not url:
        raise ValueError(f"Aucune URL définie pour {distro} {version}")

    filename = f"{distro.lower()}-{version.replace(' ', '_')}.iso"
    start = time.time()

    def reporthook(block_num, block_size, total_size):
        downloaded = block_num * block_size
        if total_size > 0:
            percent = downloaded / total_size * 100
            elapsed = time.time() - start
            speed = downloaded / 1024 / elapsed if elapsed > 0 else 0
            print(
                f"\r{percent:.2f}% téléchargé - {elapsed:.1f}s - {speed:.1f} Ko/s",
                end="",
            )
        else:
            print(f"\r{downloaded} octets téléchargés", end="")

    if os.path.exists(filename):
        print("Le fichier ISO est déjà présent :", filename)
    else:
        urlretrieve(url, filename, reporthook)
        print("\nTéléchargement terminé :", filename)

    return filename
