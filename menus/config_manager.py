import json
import os

import questionary
from rich.console import Console
from rich.panel import Panel

from menus.distributions import choose_distribution

console = Console()
CONFIG_DIR = "configs"


def ensure_config_dir():
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)


def list_configs():
    ensure_config_dir()
    return [
        f.replace(".json", "") for f in os.listdir(CONFIG_DIR) if f.endswith(".json")
    ]


def config_manager():
    console.clear()
    console.print(
        Panel(
            "Configuration Manager\n"
            "Choose to create a new config or manage existing ones",
            border_style="grey37",
            title="CONFIG MANAGER",
            expand=False,
        )
    )

    choice = questionary.select(
        "Select an option",
        choices=["Create new config", "Load existing config", "Exit"],
        qmark="[*]",
        pointer=">",
    ).ask()

    if choice == "Create new config":
        while True:
            name = questionary.text("Enter a name for this config :", qmark="[>]").ask()
            if not name:
                console.print("[red]You must enter a name.[/red]")
                continue

            path = os.path.join(CONFIG_DIR, f"{name}.json")
            if os.path.exists(path):
                console.print(
                    f"[red][*] Config '{name}' already exists. Choose another name.[/red]"
                )
                continue

            distro, version = choose_distribution()
            if not distro or not version:
                return None, None, None

            with open(path, "w") as f:
                json.dump({"distro": distro, "version": version}, f, indent=2)

            console.print(f"[green]Config '{name}' saved successfully.[/green]")
            return name, distro, version

    elif choice == "Load existing config":
        configs = list_configs()
        if not configs:
            console.print("[yellow]No configs found[/yellow]")
            return config_manager()

        configs.append("Back")
        name = questionary.select(
            "Select a config", choices=configs, qmark="[*]", pointer=">"
        ).ask()

        if name == "Back" or not name:
            return config_manager()

        action = questionary.select(
            f"What do you want to do with '{name}'?",
            choices=["Modify", "Delete", "Use", "Back"],
            qmark="[*]",
            pointer=">",
        ).ask()

        if action == "Modify":
            distro, version = choose_distribution()
            path = os.path.join(CONFIG_DIR, f"{name}.json")
            with open(path, "w") as f:
                json.dump({"distro": distro, "version": version}, f, indent=2)
            return name, distro, version

        elif action == "Delete":
            os.remove(os.path.join(CONFIG_DIR, f"{name}.json"))
            console.print(f"[red]Config '{name}' deleted.[/red]")
            return config_manager()

        elif action == "Use":
            with open(os.path.join(CONFIG_DIR, f"{name}.json")) as f:
                data = json.load(f)
            return name, data.get("distro"), data.get("version")

        elif action == "Back":
            return config_manager()

    elif choice == "Exit":
        return None, None, None

    return None, None, None
