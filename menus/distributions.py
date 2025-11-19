import questionary
from rich.console import Console

console = Console()


def choose_distribution():
    distro = questionary.select(
        "Select your distribution",
        choices=["Ubuntu", "Other", "Other", "Other"],
        qmark="[*]",
        pointer=">",
    ).ask()

    # Ubuntu
    if distro == "Ubuntu":
        version = questionary.select(
            "Select Ubuntu version",
            choices=["24.04 LTS"],
            qmark="[*]",
            pointer=">",
        ).ask()

        de = questionary.select(
            "Select Desktop Environment (DE)",
            choices=["GNOME"],
            qmark="[*]",
            pointer=">",
        ).ask()

        return distro, f"{version} with {de}"

    # other distribution

    return distro, None
