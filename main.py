from rich.console import Console
from rich.panel import Panel

from iso_tools.builder import build_iso
from iso_tools.downloader import download_iso
from iso_tools.extractor import extract_iso, extract_squashfs
from menus.config_manager import config_manager

console = Console()


def main():
    banner_text = (
        "[bold white][*] Abyss is currently in version [blue]v1.0[/blue][/bold white]\n"
        "[bold white][*] Documentation : [green]https://(soon)[/green][/bold white]"
    )
    console.print(
        Panel(
            banner_text,
            title="[bold blue]ABYSS[/bold blue]",
            border_style="grey37",
            expand=False,
        )
    )

    console.print(
        "\n[bold white][>] Press [blue]Enter[/blue] to start the configuration manager...[/bold white]"
    )
    input()

    # récupération de la config
    config_name, distro, version = config_manager()

    if not distro or not version:
        console.print("[red][*] Exiting[/red]")
        return

    console.print(
        f"[bold white]Selected configuration:[/bold white] [blue]{distro}[/blue] [green]{version}[/green]"
    )

    # téléchargement
    filename = download_iso(distro, version)

    # extraction
    extract_iso(filename)

    # custom
    extract_squashfs("iso_extracted/CASPER/MINIMAL_STANDARD.SQUASHFS")

    # recompilation de l'iso
    iso_name = f"{config_name}.iso"
    build_iso(iso_name)
    console.print(f"[green][*] ISO recompilé : {iso_name}[/green]")
    console.print("[red][*] Le programme n'est pas encore fonctionnel [/red]")


if __name__ == "__main__":
    main()
