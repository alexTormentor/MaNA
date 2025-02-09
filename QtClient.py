import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit, QComboBox, QTableWidget, QTableWidgetItem
)
import httpx

API_URL = "http://localhost:8000"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Character Manager")

        layout = QVBoxLayout()

        self.create_character_button = QPushButton("Create Character")
        self.create_character_button.clicked.connect(self.open_create_character)
        layout.addWidget(self.create_character_button)

        self.create_armor_button = QPushButton("Create Armor")
        self.create_armor_button.clicked.connect(self.open_create_armor)
        layout.addWidget(self.create_armor_button)

        self.create_weapon_button = QPushButton("Create Weapon")
        self.create_weapon_button.clicked.connect(self.open_create_weapon)
        layout.addWidget(self.create_weapon_button)

        self.create_modification_button = QPushButton("Create Modification")
        self.create_modification_button.clicked.connect(self.open_create_modification)
        layout.addWidget(self.create_modification_button)

        self.view_characters_button = QPushButton("View Characters")
        self.view_characters_button.clicked.connect(self.open_view_characters)
        layout.addWidget(self.view_characters_button)



        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def open_create_character(self):
        self.create_character_window = CreateCharacterWindow()
        self.create_character_window.show()

    def open_create_armor(self):
        self.create_armor_window = CreateArmorWindow()
        self.create_armor_window.show()

    def open_create_weapon(self):
        self.create_weapon_window = CreateWeaponWindow()
        self.create_weapon_window.show()

    def open_create_modification(self):
        self.create_modification_window = CreateModificationWindow()
        self.create_modification_window.show()

    def open_view_characters(self):
        self.view_characters_window = ViewCharactersWindow()
        self.view_characters_window.show()


class CreateCharacterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Create Character")

        layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Character Name")
        layout.addWidget(QLabel("Name:"))
        layout.addWidget(self.name_input)

        self.faction_select = QComboBox()
        layout.addWidget(QLabel("Faction:"))
        layout.addWidget(self.faction_select)
        self.load_factions()

        self.armor_select = QComboBox()
        layout.addWidget(QLabel("Armor:"))
        layout.addWidget(self.armor_select)
        self.load_armors()

        self.weapon_select = QComboBox()
        layout.addWidget(QLabel("Weapon:"))
        layout.addWidget(self.weapon_select)
        self.load_weapons()

        self.modification_select = QComboBox()
        layout.addWidget(QLabel("Modification:"))
        layout.addWidget(self.modification_select)
        self.load_modifications()

        self.health_input = QLineEdit()
        self.health_input.setPlaceholderText("Health")
        layout.addWidget(QLabel("Health:"))
        layout.addWidget(self.health_input)

        self.damage_input = QLineEdit()
        self.damage_input.setPlaceholderText("Damage")
        layout.addWidget(QLabel("Damage:"))
        layout.addWidget(self.damage_input)

        self.speed_input = QLineEdit()
        self.speed_input.setPlaceholderText("Speed")
        layout.addWidget(QLabel("Speed:"))
        layout.addWidget(self.speed_input)

        self.submit_button = QPushButton("Create Character")
        self.submit_button.clicked.connect(self.create_character)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def load_factions(self):
        try:
            response = httpx.get(f"{API_URL}/factions")
            factions = response.json()
            for faction in factions:
                self.faction_select.addItem(faction['name'], faction['id'])
        except Exception as e:
            print(f"Error loading factions: {e}")

    def load_armors(self):
        try:
            response = httpx.get(f"{API_URL}/armors")
            armors = response.json()
            for armor in armors:
                self.armor_select.addItem(armor['name'], armor['id'])
        except Exception as e:
            print(f"Error loading armors: {e}")

    def load_weapons(self):
        try:
            response = httpx.get(f"{API_URL}/weapons")
            weapons = response.json()
            for weapon in weapons:
                self.weapon_select.addItem(weapon['name'], weapon['id'])
        except Exception as e:
            print(f"Error loading weapons: {e}")

    def load_modifications(self):
        try:
            response = httpx.get(f"{API_URL}/modifications")
            modifications = response.json()
            for mod in modifications:
                self.modification_select.addItem(mod['name'], mod['id'])
        except Exception as e:
            print(f"Error loading modifications: {e}")

    def create_character(self):
        try:
            data = {
                "name": self.name_input.text(),
                "faction_id": self.faction_select.currentData(),
                "armor_id": self.armor_select.currentData() if self.armor_select.currentData() else None,
                "weapon_id": self.weapon_select.currentData() if self.weapon_select.currentData() else None,
                "modification_id": self.modification_select.currentData() if self.modification_select.currentData() else None,
                "health": float(self.health_input.text() or 0),
                "damage": float(self.damage_input.text() or 0),
                "speed": float(self.speed_input.text() or 0)
            }

            response = httpx.post(f"{API_URL}/characters", json=data)
            if response.status_code == 200:
                print("Character created successfully!")
                self.close()
            else:
                print(f"Failed to create character: {response.json()}")
        except Exception as e:
            print(f"Error creating character: {e}")


class CreateArmorWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Create Armor")

        layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Armor Name")
        layout.addWidget(QLabel("Name:"))
        layout.addWidget(self.name_input)

        self.faction_select = QComboBox()
        layout.addWidget(QLabel("Faction:"))
        layout.addWidget(self.faction_select)
        self.load_factions()

        self.health_bonus_input = QLineEdit()
        self.health_bonus_input.setPlaceholderText("Health Bonus")
        layout.addWidget(QLabel("Health Bonus:"))
        layout.addWidget(self.health_bonus_input)

        self.damage_bonus_input = QLineEdit()
        self.damage_bonus_input.setPlaceholderText("Damage Bonus")
        layout.addWidget(QLabel("Damage Bonus:"))
        layout.addWidget(self.damage_bonus_input)

        self.speed_bonus_input = QLineEdit()
        self.speed_bonus_input.setPlaceholderText("Speed Bonus")
        layout.addWidget(QLabel("Speed Bonus:"))
        layout.addWidget(self.speed_bonus_input)

        self.submit_button = QPushButton("Create Armor")
        self.submit_button.clicked.connect(self.create_armor)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def load_factions(self):
        try:
            response = httpx.get(f"{API_URL}/factions")
            factions = response.json()
            for faction in factions:
                self.faction_select.addItem(faction['name'], faction['id'])
        except Exception as e:
            print(f"Error loading factions: {e}")

    def create_armor(self):
        try:
            data = {
                "name": self.name_input.text(),
                "faction_id": self.faction_select.currentData(),
                "health_bonus": float(self.health_bonus_input.text() or 0),
                "damage_bonus": float(self.damage_bonus_input.text() or 0),
                "speed_bonus": float(self.speed_bonus_input.text() or 0)
            }

            response = httpx.post(f"{API_URL}/armors", json=data)

            if response.status_code == 200:
                print("Armor created successfully!")
            else:
                print(f"Failed to create armor: {response.json()}")
        except Exception as e:
            print(f"Error creating armor: {e}")



class CreateWeaponWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Create Weapon")

        layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Weapon Name")
        layout.addWidget(QLabel("Name:"))
        layout.addWidget(self.name_input)

        self.faction_select = QComboBox()
        layout.addWidget(QLabel("Faction:"))
        layout.addWidget(self.faction_select)
        self.load_factions()

        self.damage_bonus_input = QLineEdit()
        self.damage_bonus_input.setPlaceholderText("Damage Bonus")
        layout.addWidget(QLabel("Damage Bonus:"))
        layout.addWidget(self.damage_bonus_input)

        self.speed_bonus_input = QLineEdit()
        self.speed_bonus_input.setPlaceholderText("Speed Bonus")
        layout.addWidget(QLabel("Speed Bonus:"))
        layout.addWidget(self.speed_bonus_input)

        self.submit_button = QPushButton("Create Weapon")
        self.submit_button.clicked.connect(self.create_weapon)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def load_factions(self):
        try:
            response = httpx.get(f"{API_URL}/factions")
            factions = response.json()
            for faction in factions:
                self.faction_select.addItem(faction['name'], faction['id'])
        except Exception as e:
            print(f"Error loading factions: {e}")

    def create_weapon(self):
        try:
            data = {
                "name": self.name_input.text(),
                "faction_id": self.faction_select.currentData(),
                "damage_bonus": float(self.damage_bonus_input.text() or 0),
                "speed_bonus": float(self.speed_bonus_input.text() or 0)
            }

            response = httpx.post(f"{API_URL}/weapons", json=data)

            if response.status_code == 200:
                print("Weapon created successfully!")
            else:
                print(f"Failed to create weapon: {response.json()}")
        except Exception as e:
            print(f"Error creating weapon: {e}")


class CreateModificationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Create Modification")

        layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Modification Name")
        layout.addWidget(QLabel("Name:"))
        layout.addWidget(self.name_input)

        self.faction_select = QComboBox()
        layout.addWidget(QLabel("Faction:"))
        layout.addWidget(self.faction_select)
        self.load_factions()

        self.health_bonus_input = QLineEdit()
        self.health_bonus_input.setPlaceholderText("Health Bonus")
        layout.addWidget(QLabel("Health Bonus:"))
        layout.addWidget(self.health_bonus_input)

        self.damage_bonus_input = QLineEdit()
        self.damage_bonus_input.setPlaceholderText("Damage Bonus")
        layout.addWidget(QLabel("Damage Bonus:"))
        layout.addWidget(self.damage_bonus_input)

        self.speed_bonus_input = QLineEdit()
        self.speed_bonus_input.setPlaceholderText("Speed Bonus")
        layout.addWidget(QLabel("Speed Bonus:"))
        layout.addWidget(self.speed_bonus_input)

        self.submit_button = QPushButton("Create Modification")
        self.submit_button.clicked.connect(self.create_modification)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def load_factions(self):
        try:
            response = httpx.get(f"{API_URL}/factions")
            factions = response.json()
            for faction in factions:
                self.faction_select.addItem(faction['name'], faction['id'])
        except Exception as e:
            print(f"Error loading factions: {e}")

    def create_modification(self):
        try:
            data = {
                "name": self.name_input.text(),
                "faction_id": self.faction_select.currentData(),
                "health_bonus": float(self.health_bonus_input.text() or 0),
                "damage_bonus": float(self.damage_bonus_input.text() or 0),
                "speed_bonus": float(self.speed_bonus_input.text() or 0)
            }

            response = httpx.post(f"{API_URL}/modifications", json=data)

            if response.status_code == 200:
                print("Modification created successfully!")
            else:
                print(f"Failed to create modification: {response.json()}")
        except Exception as e:
            print(f"Error creating modification: {e}")


class ViewCharactersWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("View Characters")

        layout = QVBoxLayout()

        self.characters_table = QTableWidget()
        self.characters_table.setColumnCount(5) 
        self.characters_table.setHorizontalHeaderLabels(["Name", "Faction", "Health", "Damage", "Speed"])

        layout.addWidget(self.characters_table)

        self.load_button = QPushButton("Load Characters")
        self.load_button.clicked.connect(self.load_characters)
        layout.addWidget(self.load_button)

        self.setLayout(layout)

    def load_characters(self):
        try:
            response = httpx.get(f"{API_URL}/characters")
            characters = response.json()

            if not isinstance(characters, list):
                print("Unexpected response format:", characters)
                return

            self.characters_table.setRowCount(0)

            for row, character in enumerate(characters):
                self.characters_table.insertRow(row)
                self.characters_table.setItem(row, 0, QTableWidgetItem(character['name']))
                self.characters_table.setItem(row, 1, QTableWidgetItem(
                    str(character['faction_id'])))  
                self.characters_table.setItem(row, 2, QTableWidgetItem(str(character['health'])))
                self.characters_table.setItem(row, 3, QTableWidgetItem(str(character['damage'])))
                self.characters_table.setItem(row, 4, QTableWidgetItem(str(character['speed'])))
        except Exception as e:
            print(f"Error loading characters: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
