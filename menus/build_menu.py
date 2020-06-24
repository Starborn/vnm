import configparser
import json
from pathlib import Path
from typing import Text
import xml.etree.ElementTree as et


def add_menu(name: Text, icon: Text) -> None:
    print(f"Adding submenu for '{name}'")
    # Generate `.directory` file
    entry = configparser.ConfigParser()
    entry["Desktop Entry"] = {
        "Name": name.capitalize(),
        "Comment": name.capitalize(),
        "Icon": icon,
        "Type": "Directory",
    }
    directories_path = "/usr/share/desktop-directories"
    directory_name = f"vnm-{name.lower().replace(' ', '-')}.directory"
    with open(Path(f"{directories_path}/{directory_name}"), "w",) as directory_file:
        entry.write(directory_file)
    # Add entry to `.menu` file
    menu_path = Path("/etc/xdg/menus/vnm-applications.menu")
    tree = et.ElementTree(file=str(menu_path))
    root = tree.getroot()
    menu = root.findall("./Menu")[0]
    sub = et.SubElement(menu, "Menu")
    name = et.SubElement(sub, "Name")
    name.text = name.capitalize()
    dir = et.SubElement(sub, "Directory")
    dir.text = directory_name
    include = et.SubElement(sub, "Include")
    a = et.SubElement(include, "And")
    cat = et.SubElement(a, "Category")
    cat.text = name.replace(" ", "-")
    tree.write("/etc/xdg/menus/vnm-applications.menu")


def add_app(
    name: Text,
    version: Text,
    icon: Text,
    exec: Text,
    comment: Text,
    category: Text,
    terminal: bool = True,
) -> None:
    entry = configparser.ConfigParser()
    entry["Desktop Entry"] = {
        "Name": name.capitalize(),
        "GenericName": name.capitalize(),
        "Comment": comment,
        "Exec": exec,
        "Icon": icon,
        "Type": "Application",
        "Categories": category,
        "Terminal": str(terminal).lower(),
    }
    applications_path = "/usr/share/applications"
    with open(
        Path(f"{applications_path}/vnm-{name.lower().replace(' ', '-')}.desktop"), "w",
    ) as desktop_file:
        entry.write(desktop_file)


if __name__ == "__main__":
    # Read applications file
    with open(Path("./apps.json"), "r") as json_file:
        menu_entries = json.load(json_file)

    for menu_name, menu_data in menu_entries.items():
        # Add submenu
        add_menu(menu_name, menu_data["icon"])
        for app_name, app_data in menu_data.get("apps", {}):
            # Add application
            add_app(app_name, category=menu_name.replace(" ", "-"), **app_data)
