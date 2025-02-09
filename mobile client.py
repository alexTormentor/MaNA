import requests
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup

API_URL = "http://127.0.0.1:8000"

class MyApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        self.main_menu()
        return self.layout

    def main_menu(self):
        """Главное меню с кнопками для создания брони или оружия"""
        self.layout.clear_widgets()

        label = Label(text="Выберите действие:")
        add_armor_btn = Button(text="Добавить броню")
        add_weapon_btn = Button(text="Добавить оружие")
        add_modification_btn = Button(text="Добавить модификацию")
        add_character_btn = Button(text="Добавить персонажа")
        view_armors_btn = Button(text="Просмотреть список брони")
        view_weapons_btn = Button(text="Просмотреть список оружия")
        view_modifications_btn = Button(text="Просмотреть список модификаций")
        view_characters_btn = Button(text="Просмотреть список персонажей")

        add_armor_btn.bind(on_press=self.add_armor_form)
        add_weapon_btn.bind(on_press=self.add_weapon_form)
        add_modification_btn.bind(on_press=self.add_modification_form)
        add_character_btn.bind(on_press=self.add_character_form)
        view_armors_btn.bind(on_press=self.view_armors)
        view_weapons_btn.bind(on_press=self.view_weapons)
        view_modifications_btn.bind(on_press=self.view_modifications)
        view_characters_btn.bind(on_press=self.view_characters)

        self.layout.add_widget(label)
        self.layout.add_widget(add_armor_btn)
        self.layout.add_widget(add_weapon_btn)
        self.layout.add_widget(add_modification_btn)
        self.layout.add_widget(add_character_btn)
        self.layout.add_widget(view_armors_btn)
        self.layout.add_widget(view_weapons_btn)
        self.layout.add_widget(view_modifications_btn)
        self.layout.add_widget(view_characters_btn)

    def add_armor_form(self, instance):
        """Форма для добавления брони"""
        self.layout.clear_widgets()

        label = Label(text="Добавить броню")

        response = requests.get(f"{API_URL}/factions")
        factions = response.json()

        dropdown = DropDown()
        for faction in factions:
            btn = Button(text=faction['name'], size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            dropdown.add_widget(btn)

        faction_button = Button(text='Выберите фракцию')
        faction_button.bind(on_release=dropdown.open)
        dropdown.bind(on_select=lambda instance, x: setattr(faction_button, 'text', x))

        name_input = TextInput(hint_text="Название брони")
        health_bonus_input = TextInput(hint_text="Бонус к здоровью", input_filter='float')
        damage_bonus_input = TextInput(hint_text="Бонус к урону", input_filter='float')
        speed_bonus_input = TextInput(hint_text="Бонус к скорости", input_filter='float')

        submit_btn = Button(text="Создать броню")
        submit_btn.bind(on_press=lambda instance: self.create_armor(
            name_input.text,
            faction_button.text,
            health_bonus_input.text,
            damage_bonus_input.text,
            speed_bonus_input.text
        ))

        back_btn = Button(text="Назад")
        back_btn.bind(on_press=lambda instance: self.main_menu())

        self.layout.add_widget(back_btn)
        self.layout.add_widget(label)
        self.layout.add_widget(faction_button)
        self.layout.add_widget(name_input)
        self.layout.add_widget(health_bonus_input)
        self.layout.add_widget(damage_bonus_input)
        self.layout.add_widget(speed_bonus_input)
        self.layout.add_widget(submit_btn)

    def create_armor(self, name, faction_name, health_bonus, damage_bonus, speed_bonus):
        """Отправка данных для создания брони"""
        try:
            # Получаем ID фракции по имени
            response = requests.get(f"{API_URL}/factions")
            factions = response.json()
            faction_id = next(faction['id'] for faction in factions if faction['name'] == faction_name)

            payload = {
                "name": name,
                "faction_id": faction_id,
                "health_bonus": float(health_bonus),
                "damage_bonus": float(damage_bonus),
                "speed_bonus": float(speed_bonus)
            }

            response = requests.post(f"{API_URL}/armors", json=payload)
            if response.status_code == 200:
                self.show_popup("Успех", "Броня успешно добавлена!")
            else:
                self.show_popup("Ошибка", "Не удалось создать броню.")
        except Exception as e:
            self.show_popup("Ошибка", f"Произошла ошибка: {str(e)}")

    def add_weapon_form(self, instance):
        """Форма для добавления оружия"""
        self.layout.clear_widgets()

        label = Label(text="Добавить оружие")

        # Получаем фракции с сервера для выпадающего списка
        response = requests.get(f"{API_URL}/factions")
        factions = response.json()

        dropdown = DropDown()
        for faction in factions:
            btn = Button(text=faction['name'], size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            dropdown.add_widget(btn)

        faction_button = Button(text='Выберите фракцию')
        faction_button.bind(on_release=dropdown.open)
        dropdown.bind(on_select=lambda instance, x: setattr(faction_button, 'text', x))

        name_input = TextInput(hint_text="Название оружия")
        damage_bonus_input = TextInput(hint_text="Бонус к урону", input_filter='float')
        speed_bonus_input = TextInput(hint_text="Бонус к скорости", input_filter='float')

        submit_btn = Button(text="Создать оружие")
        submit_btn.bind(on_press=lambda instance: self.create_weapon(
            name_input.text,
            faction_button.text,
            damage_bonus_input.text,
            speed_bonus_input.text
        ))

        back_btn = Button(text="Назад")
        back_btn.bind(on_press=lambda instance: self.main_menu())

        self.layout.add_widget(back_btn)
        self.layout.add_widget(label)
        self.layout.add_widget(faction_button)
        self.layout.add_widget(name_input)
        self.layout.add_widget(damage_bonus_input)
        self.layout.add_widget(speed_bonus_input)
        self.layout.add_widget(submit_btn)

    def create_weapon(self, name, faction_name, damage_bonus, speed_bonus):
        """Отправка данных для создания оружия"""
        try:
            response = requests.get(f"{API_URL}/factions")
            factions = response.json()
            faction_id = next(faction['id'] for faction in factions if faction['name'] == faction_name)
            payload = {
                "name": name,
                "faction_id": faction_id,
                "damage_bonus": float(damage_bonus),
                "speed_bonus": float(speed_bonus)
            }

            response = requests.post(f"{API_URL}/weapons", json=payload)
            if response.status_code == 200:
                self.show_popup("Успех", "Оружие успешно добавлено!")
            else:
                self.show_popup("Ошибка", "Не удалось создать оружие.")
        except Exception as e:
            self.show_popup("Ошибка", f"Произошла ошибка: {str(e)}")

    def add_modification_form(self, instance):
        """Форма для добавления мода"""
        self.layout.clear_widgets()

        label = Label(text="Добавить модификацию")
        response = requests.get(f"{API_URL}/factions")
        modifications = response.json()

        dropdown = DropDown()
        for modification in modifications:
            btn = Button(text=modification['name'], size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            dropdown.add_widget(btn)

        modification_button = Button(text='Выберите фракцию')
        modification_button.bind(on_release=dropdown.open)
        dropdown.bind(on_select=lambda instance, x: setattr(modification_button, 'text', x))

        name_input = TextInput(hint_text="Название модификации")
        health_bonus_input = TextInput(hint_text="Бонус к здоровью", input_filter='float')
        damage_bonus_input = TextInput(hint_text="Бонус к урону", input_filter='float')
        speed_bonus_input = TextInput(hint_text="Бонус к скорости", input_filter='float')

        submit_btn = Button(text="Создать модификацию")
        submit_btn.bind(on_press=lambda instance: self.create_modification(
            name_input.text,
            modification_button.text,
            health_bonus_input.text,
            damage_bonus_input.text,
            speed_bonus_input.text
        ))

        back_btn = Button(text="Назад")
        back_btn.bind(on_press=lambda instance: self.main_menu())

        self.layout.add_widget(back_btn)
        self.layout.add_widget(label)
        self.layout.add_widget(modification_button)
        self.layout.add_widget(name_input)
        self.layout.add_widget(health_bonus_input)
        self.layout.add_widget(damage_bonus_input)
        self.layout.add_widget(speed_bonus_input)
        self.layout.add_widget(submit_btn)

    def create_modification(self, name, faction_name, health_bonus, damage_bonus, speed_bonus):
        """Отправка данных для создания"""
        try:
            response = requests.get(f"{API_URL}/factions")
            factions = response.json()
            faction_id = next(faction['id'] for faction in factions if faction['name'] == faction_name)
            payload = {
                "name": name,
                "faction_id": faction_id,
                "health_bonus": float(health_bonus),
                "damage_bonus": float(damage_bonus),
                "speed_bonus": float(speed_bonus)
            }

            response = requests.post(f"{API_URL}/modifications", json=payload)
            if response.status_code == 200:
                self.show_popup("Успех", "Модификация успешно добавлена!")
            else:
                self.show_popup("Ошибка", "Не удалось создать модификацию.")
        except Exception as e:
            self.show_popup("Ошибка", f"Произошла ошибка: {str(e)}")

    def add_character_form(self, instance):
        """Форма для добавления персонажа"""
        self.layout.clear_widgets()

        label = Label(text="Добавить персонажа")
        response = requests.get(f"{API_URL}/factions")
        factions = response.json()

        dropdown_faction = DropDown()
        for faction in factions:
            btn = Button(text=faction['name'], size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: dropdown_faction.select(btn.text))
            dropdown_faction.add_widget(btn)

        faction_button = Button(text='Выберите фракцию')
        faction_button.bind(on_release=dropdown_faction.open)
        dropdown_faction.bind(on_select=lambda instance, x: setattr(faction_button, 'text', x))

        name_input = TextInput(hint_text="Имя персонажа")
        response_armor = requests.get(f"{API_URL}/armors")
        armors = response_armor.json()
        dropdown_armor = DropDown()
        for armor in armors:
            btn = Button(text=armor['name'], size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: dropdown_armor.select(btn.text))
            dropdown_armor.add_widget(btn)

        armor_button = Button(text='Выберите броню')
        armor_button.bind(on_release=dropdown_armor.open)
        dropdown_armor.bind(on_select=lambda instance, x: setattr(armor_button, 'text', x))

        response_weapon = requests.get(f"{API_URL}/weapons")
        weapons = response_weapon.json()
        dropdown_weapon = DropDown()
        for weapon in weapons:
            btn = Button(text=weapon['name'], size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: dropdown_weapon.select(btn.text))
            dropdown_weapon.add_widget(btn)

        weapon_button = Button(text='Выберите оружие')
        weapon_button.bind(on_release=dropdown_weapon.open)
        dropdown_weapon.bind(on_select=lambda instance, x: setattr(weapon_button, 'text', x))

        response_modification = requests.get(f"{API_URL}/modifications")
        modifications = response_modification.json()
        dropdown_modification = DropDown()
        for mod in modifications:
            btn = Button(text=mod['name'], size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: dropdown_modification.select(btn.text))
            dropdown_modification.add_widget(btn)

        modification_button = Button(text='Выберите модификацию')
        modification_button.bind(on_release=dropdown_modification.open)
        dropdown_modification.bind(on_select=lambda instance, x: setattr(modification_button, 'text', x))

        submit_btn = Button(text="Создать персонажа")
        submit_btn.bind(on_press=lambda instance: self.create_character(
            name_input.text,
            faction_button.text,
            armor_button.text,
            weapon_button.text,
            modification_button.text
        ))

        back_btn = Button(text="Назад")
        back_btn.bind(on_press=lambda instance: self.main_menu())

        self.layout.add_widget(back_btn)
        self.layout.add_widget(label)
        self.layout.add_widget(faction_button)
        self.layout.add_widget(name_input)
        self.layout.add_widget(armor_button)
        self.layout.add_widget(weapon_button)
        self.layout.add_widget(modification_button)
        self.layout.add_widget(submit_btn)

    def create_character(self, name, faction_name, armor_name, weapon_name, modification_name):
        """Отправка данных для создания персонажа"""
        try:
            response = requests.get(f"{API_URL}/factions")
            factions = response.json()
            faction_id = next(faction['id'] for faction in factions if faction['name'] == faction_name)

            response_armor = requests.get(f"{API_URL}/armors")
            armors = response_armor.json()
            armor_id = next((armor['id'] for armor in armors if armor['name'] == armor_name), None)

            response_weapon = requests.get(f"{API_URL}/weapons")
            weapons = response_weapon.json()
            weapon_id = next((weapon['id'] for weapon in weapons if weapon['name'] == weapon_name), None)

            response_modification = requests.get(f"{API_URL}/modifications")
            modifications = response_modification.json()
            modification_id = next((mod['id'] for mod in modifications if mod['name'] == modification_name), None)

            if armor_id:
                armor_faction = next(armor['faction_id'] for armor in armors if armor['id'] == armor_id)
                if armor_faction != faction_id:
                    self.show_popup("Ошибка", "Броня не принадлежит выбранной фракции!")
                    return

            if weapon_id:
                weapon_faction = next(weapon['faction_id'] for weapon in weapons if weapon['id'] == weapon_id)
                if weapon_faction != faction_id:
                    self.show_popup("Ошибка", "Оружие не принадлежит выбранной фракции!")
                    return

            if modification_id:
                mod_faction = next(mod['faction_id'] for mod in modifications if mod['id'] == modification_id)
                if mod_faction != faction_id:
                    self.show_popup("Ошибка", "Модификация не принадлежит выбранной фракции!")
                    return

            # Отправка данных для создания персонажа
            payload = {
                "name": name,
                "faction_id": faction_id,
                "armor_id": armor_id,
                "weapon_id": weapon_id,
                "modification_id": modification_id,
                "health": 100,  # Это можно адаптировать, вычисляя характеристики
                "damage": 50,  # Также можно вычислить на основе компонентов
                "speed": 30  # Аналогично
            }

            response = requests.post(f"{API_URL}/characters", json=payload)
            if response.status_code == 200:
                self.show_popup("Успех", "Персонаж успешно создан!")
            else:
                self.show_popup("Ошибка", f"Не удалось создать персонажа: {response.json()['detail']}")
        except Exception as e:
            self.show_popup("Ошибка", f"Произошла ошибка: {str(e)}")

    def view_armors(self, instance):
        """Просмотр списка брони с улучшенной таблицей и именем фракции"""
        self.layout.clear_widgets()

        # Запрос на получение списка брони
        response = requests.get(f"{API_URL}/armors")
        armors = response.json()

        # Запрос на получение фракций для отображения их имен
        factions_response = requests.get(f"{API_URL}/factions")
        factions = {faction['id']: faction['name'] for faction in factions_response.json()}

        grid = GridLayout(cols=5, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))

        grid.add_widget(Label(text="Название", bold=True))
        grid.add_widget(Label(text="Фракция", bold=True))
        grid.add_widget(Label(text="Здоровье", bold=True))
        grid.add_widget(Label(text="Урон", bold=True))
        grid.add_widget(Label(text="Скорость", bold=True))

        for armor in armors:
            faction_name = factions.get(armor['faction_id'], "Неизвестно")
            grid.add_widget(Label(text=armor['name']))
            grid.add_widget(Label(text=faction_name))
            grid.add_widget(Label(text=str(armor['health_bonus'])))
            grid.add_widget(Label(text=str(armor['damage_bonus'])))
            grid.add_widget(Label(text=str(armor['speed_bonus'])))

        scroll_view = ScrollView(size_hint=(1, None), size=(600, 300))
        scroll_view.add_widget(grid)

        back_btn = Button(text="Назад")
        back_btn.bind(on_press=lambda instance: self.main_menu())

        self.layout.add_widget(back_btn)
        self.layout.add_widget(scroll_view)

    def view_weapons(self, instance):
        """Просмотр списка оружия"""
        self.layout.clear_widgets()
        response = requests.get(f"{API_URL}/weapons")
        weapons = response.json()

        factions_response = requests.get(f"{API_URL}/factions")
        factions = {faction['id']: faction['name'] for faction in factions_response.json()}

        grid = GridLayout(cols=4, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))

        grid.add_widget(Label(text="Название", bold=True))
        grid.add_widget(Label(text="Фракция", bold=True))
        grid.add_widget(Label(text="Урон", bold=True))
        grid.add_widget(Label(text="Скорость", bold=True))

        for weapon in weapons:
            faction_name = factions.get(weapon['faction_id'], "Неизвестно")
            grid.add_widget(Label(text=weapon['name']))
            grid.add_widget(Label(text=faction_name))
            grid.add_widget(Label(text=str(weapon['damage_bonus'])))
            grid.add_widget(Label(text=str(weapon['speed_bonus'])))

        scroll_view = ScrollView(size_hint=(1, None), size=(600, 300))
        scroll_view.add_widget(grid)

        back_btn = Button(text="Назад")
        back_btn.bind(on_press=lambda instance: self.main_menu())

        self.layout.add_widget(back_btn)
        self.layout.add_widget(scroll_view)

    def view_modifications(self, instance):
        """Просмотр списка брони с улучшенной таблицей и именем фракции"""
        self.layout.clear_widgets()

        response = requests.get(f"{API_URL}/modifications")
        modifications = response.json()

        factions_response = requests.get(f"{API_URL}/factions")
        factions = {faction['id']: faction['name'] for faction in factions_response.json()}

        grid = GridLayout(cols=5, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))

        grid.add_widget(Label(text="Название", bold=True))
        grid.add_widget(Label(text="Фракция", bold=True))
        grid.add_widget(Label(text="Здоровье", bold=True))
        grid.add_widget(Label(text="Урон", bold=True))
        grid.add_widget(Label(text="Скорость", bold=True))

        for modification in modifications:
            faction_name = factions.get(modification['faction_id'], "Неизвестно")
            grid.add_widget(Label(text=modification['name']))
            grid.add_widget(Label(text=faction_name))
            grid.add_widget(Label(text=str(modification['health_bonus'])))
            grid.add_widget(Label(text=str(modification['damage_bonus'])))
            grid.add_widget(Label(text=str(modification['speed_bonus'])))

        scroll_view = ScrollView(size_hint=(1, None), size=(600, 300))
        scroll_view.add_widget(grid)

        back_btn = Button(text="Назад")
        back_btn.bind(on_press=lambda instance: self.main_menu())

        self.layout.add_widget(back_btn)
        self.layout.add_widget(scroll_view)

    def view_characters(self, instance):
        """Просмотр списка персонажей"""
        self.layout.clear_widgets()

        response = requests.get(f"{API_URL}/characters")
        characters = response.json()

        factions_response = requests.get(f"{API_URL}/factions")
        factions = {faction['id']: faction['name'] for faction in factions_response.json()}
        armors_response = requests.get(f"{API_URL}/armors")
        armors = {armor['id']: armor['name'] for armor in armors_response.json()}
        weapons_response = requests.get(f"{API_URL}/weapons")
        weapons = {weapon['id']: weapon['name'] for weapon in weapons_response.json()}
        modifications_response = requests.get(f"{API_URL}/modifications")
        modifications = {modification['id']: modification['name'] for modification in modifications_response.json()}

        grid = GridLayout(cols=8, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))

        grid.add_widget(Label(text="Персонаж", bold=True))
        grid.add_widget(Label(text="Фракция", bold=True))
        grid.add_widget(Label(text="Здоровье", bold=True))
        grid.add_widget(Label(text="Урон", bold=True))
        grid.add_widget(Label(text="Скорость", bold=True))
        grid.add_widget(Label(text="Броня", bold=True))
        grid.add_widget(Label(text="Оружие", bold=True))
        grid.add_widget(Label(text="Модификация", bold=True))

        for character in characters:
            faction_name = factions.get(character['faction_id'], "Неизвестно")
            weapon_name = weapons.get(character['weapon_id'], "Неизвестно")
            armor_name = armors.get(character['armor_id'], "Неизвестно")
            modification_name = modifications.get(character['modification_id'], "Неизвестно")
            grid.add_widget(Label(text=character['name']))
            grid.add_widget(Label(text=faction_name))
            grid.add_widget(Label(text=str(character['health'])))
            grid.add_widget(Label(text=str(character['damage'])))
            grid.add_widget(Label(text=str(character['speed'])))
            grid.add_widget(Label(text=armor_name))
            grid.add_widget(Label(text=weapon_name))
            grid.add_widget(Label(text=modification_name))

        scroll_view = ScrollView(size_hint=(1, None), size=(600, 300))
        scroll_view.add_widget(grid)

        back_btn = Button(text="Назад")
        back_btn.bind(on_press=lambda instance: self.main_menu())

        self.layout.add_widget(back_btn)
        self.layout.add_widget(scroll_view)

    def show_popup(self, title, message):
        """Показать всплывающее окно"""
        popup = Popup(title=title, content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()


if __name__ == "__main__":
    MyApp().run()
