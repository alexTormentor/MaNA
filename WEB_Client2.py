from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests

app = Flask(__name__)

API_BASE_URL = "http://localhost:8000" 


@app.route('/')
def index():
    return render_template('client2_index.html')


@app.route("/create-armor", methods=["GET", "POST"])
def create_armor():
    error_message = None
    if request.method == "POST":
        name = request.form.get("name")
        faction_id = request.form.get("faction_id")
        health_bonus = request.form.get("health_bonus", 0.0, type=float)
        damage_bonus = request.form.get("damage_bonus", 0.0, type=float)
        speed_bonus = request.form.get("speed_bonus", 0.0, type=float)

        armor_data = {
            "name": name,
            "faction_id": int(faction_id),
            "health_bonus": health_bonus,
            "damage_bonus": damage_bonus,
            "speed_bonus": speed_bonus,
        }

        try:
            response = requests.post(f"{API_BASE_URL}/armors", json=armor_data)
            if response.status_code == 200:
                return redirect(url_for("create_armor"))
            else:
                error_message = response.json().get('detail', 'Unknown error')
        except requests.RequestException as e:
            error_message = f"Failed to connect to API: {str(e)}"

    return render_template("client2_create_armor.html", error_message=error_message)


@app.route("/create-weapon", methods=["GET", "POST"])
def create_weapon():
    error_message = None
    if request.method == "POST":
        name = request.form.get("name")
        faction_id = request.form.get("faction_id")
        damage_bonus = request.form.get("damage_bonus", 0.0, type=float)
        speed_bonus = request.form.get("speed_bonus", 0.0, type=float)

        weapon_data = {
            "name": name,
            "faction_id": int(faction_id),
            "damage_bonus": damage_bonus,
            "speed_bonus": speed_bonus,
        }

        try:
            response = requests.post(f"{API_BASE_URL}/weapons", json=weapon_data)
            if response.status_code == 200:
                return redirect(url_for("create_weapon"))
            else:
                error_message = response.json().get('detail', 'Unknown error')
        except requests.RequestException as e:
            error_message = f"Failed to connect to API: {str(e)}"

    return render_template("client2_create_weapon.html", error_message=error_message)


@app.route("/create-modification", methods=["GET", "POST"])
def create_modification():
    error_message = None
    if request.method == "POST":
        name = request.form.get("name")
        faction_id = request.form.get("faction_id")
        health_bonus = request.form.get("health_bonus", 0.0, type=float)
        damage_bonus = request.form.get("damage_bonus", 0.0, type=float)
        speed_bonus = request.form.get("speed_bonus", 0.0, type=float)

        modification_data = {
            "name": name,
            "faction_id": int(faction_id),
            "health_bonus": health_bonus,
            "damage_bonus": damage_bonus,
            "speed_bonus": speed_bonus,
        }

        try:
            response = requests.post(f"{API_BASE_URL}/modifications", json=modification_data)
            if response.status_code == 200:
                return redirect(url_for("create_modification"))
            else:
                error_message = response.json().get('detail', 'Unknown error')
        except requests.RequestException as e:
            error_message = f"Failed to connect to API: {str(e)}"

    return render_template("client2_create_modification.html", error_message=error_message)



@app.route("/armors", methods=["GET"])
def get_armors():
    armors = []
    factions = []
    error_message = None

    try:
        # Запрос всех бронь с API
        response_armors = requests.get(f"{API_BASE_URL}/armors")
        if response_armors.status_code == 200:
            armors = response_armors.json()
        else:
            error_message = response_armors.json().get('detail', 'Unknown error')

        # Запрос всех фракций с API
        response_factions = requests.get(f"{API_BASE_URL}/factions")
        if response_factions.status_code == 200:
            factions = response_factions.json()
        else:
            error_message = response_factions.json().get('detail', 'Unknown error')
    except requests.RequestException as e:
        error_message = f"Failed to connect to API: {str(e)}"

    factions_dict = {faction['id']: faction['name'] for faction in factions}

    return render_template("client2_armors.html", armors=armors, factions_dict=factions_dict, error_message=error_message)


@app.route("/weapons", methods=["GET"])
def get_weapons():
    weapons = []
    factions = []
    error_message = None

    try:
        response_weapons = requests.get(f"{API_BASE_URL}/weapons")
        if response_weapons.status_code == 200:
            weapons = response_weapons.json()
        else:
            error_message = response_weapons.json().get('detail', 'Unknown error')

        response_factions = requests.get(f"{API_BASE_URL}/factions")
        if response_factions.status_code == 200:
            factions = response_factions.json()
        else:
            error_message = response_factions.json().get('detail', 'Unknown error')
    except requests.RequestException as e:
        error_message = f"Failed to connect to API: {str(e)}"

    factions_dict = {faction['id']: faction['name'] for faction in factions}

    return render_template("client2_weapons.html", weapons=weapons, factions_dict=factions_dict, error_message=error_message)


@app.route("/modifications", methods=["GET"])
def get_modifications():
    modifications = []
    factions = []
    error_message = None

    try:
        response_modifications = requests.get(f"{API_BASE_URL}/modifications")
        if response_modifications.status_code == 200:
            modifications = response_modifications.json()
        else:
            error_message = response_modifications.json().get('detail', 'Unknown error')

        response_factions = requests.get(f"{API_BASE_URL}/factions")
        if response_factions.status_code == 200:
            factions = response_factions.json()
        else:
            error_message = response_factions.json().get('detail', 'Unknown error')
    except requests.RequestException as e:
        error_message = f"Failed to connect to API: {str(e)}"

    factions_dict = {faction['id']: faction['name'] for faction in factions}

    return render_template("client2_modifications.html", modifications=modifications, factions_dict=factions_dict, error_message=error_message)


@app.route("/create-character", methods=["GET", "POST"])
def create_character():
    error_message = None
    factions = []
    armors = []
    weapons = []
    modifications = []

    if request.method == "POST":
        name = request.form.get("name")
        faction_id = request.form.get("faction_id")
        armor_id = request.form.get("armor_id")
        weapon_id = request.form.get("weapon_id")
        modification_id = request.form.get("modification_id")

        health_bonus = request.form.get("health_bonus", 0.0, type=float)
        damage_bonus = request.form.get("damage_bonus", 0.0, type=float)
        speed_bonus = request.form.get("speed_bonus", 0.0, type=float)

        character_data = {
            "name": name,
            "faction_id": int(faction_id),
            "armor_id": int(armor_id) if armor_id else None,
            "weapon_id": int(weapon_id) if weapon_id else None,
            "modification_id": int(modification_id) if modification_id else None,
            "health": health_bonus,
            "damage": damage_bonus,
            "speed": speed_bonus,
        }

        try:
            response = requests.post(f"{API_BASE_URL}/characters", json=character_data)
            if response.status_code == 200:
                return redirect(url_for("create_character"))
            else:
                error_message = response.json().get('detail', 'Unknown error')
        except requests.RequestException as e:
            error_message = f"Failed to connect to API: {str(e)}"

    try:
        response_factions = requests.get(f"{API_BASE_URL}/factions")
        if response_factions.status_code == 200:
            factions = response_factions.json()
    except requests.RequestException as e:
        error_message = f"Failed to fetch factions: {str(e)}"

    return render_template("client2_create_character.html", error_message=error_message, factions=factions)


@app.route("/get-armors-by-faction/<int:faction_id>", methods=["GET"])
def get_armors_by_faction(faction_id):
    armors = []
    try:
        response = requests.get(f"{API_BASE_URL}/armors")
        if response.status_code == 200:
            armors = [armor for armor in response.json() if armor["faction_id"] == faction_id]
    except requests.RequestException as e:
        return jsonify({"error": f"Failed to fetch armors: {str(e)}"}), 500
    return jsonify(armors)


@app.route("/get-weapons-by-faction/<int:faction_id>", methods=["GET"])
def get_weapons_by_faction(faction_id):
    weapons = []
    try:
        response = requests.get(f"{API_BASE_URL}/weapons")
        if response.status_code == 200:
            weapons = [weapon for weapon in response.json() if weapon["faction_id"] == faction_id]
    except requests.RequestException as e:
        return jsonify({"error": f"Failed to fetch weapons: {str(e)}"}), 500
    return jsonify(weapons)


@app.route("/get-modifications-by-faction/<int:faction_id>", methods=["GET"])
def get_modifications_by_faction(faction_id):
    modifications = []
    try:
        response = requests.get(f"{API_BASE_URL}/modifications")
        if response.status_code == 200:
            modifications = [mod for mod in response.json() if mod["faction_id"] == faction_id]
    except requests.RequestException as e:
        return jsonify({"error": f"Failed to fetch modifications: {str(e)}"}), 500
    return jsonify(modifications)


@app.route("/view-characters", methods=["GET"])
def view_characters():
    characters = []
    factions = []
    error_message = None

    try:
        response_characters = requests.get(f"{API_BASE_URL}/characters")
        if response_characters.status_code == 200:
            characters = response_characters.json()

        response_factions = requests.get(f"{API_BASE_URL}/factions")
        if response_factions.status_code == 200:
            factions = response_factions.json()

        response_armors = requests.get(f"{API_BASE_URL}/armors")
        if response_armors.status_code == 200:
            armors = response_armors.json()

        response_weapons = requests.get(f"{API_BASE_URL}/weapons")
        if response_weapons.status_code == 200:
            weapons = response_weapons.json()

        response_modifications = requests.get(f"{API_BASE_URL}/modifications")
        if response_modifications.status_code == 200:
            modifications = response_modifications.json()
    except requests.RequestException as e:
        error_message = f"Failed to fetch data: {str(e)}"
        return render_template("client2_view_characters.html", error_message=error_message)

    factions_dict = {faction['id']: faction['name'] for faction in factions}
    armors_dict = {armor['id']: armor['name'] for armor in armors}
    weapons_dict = {weapon['id']: weapon['name'] for weapon in weapons}
    modifications_dict = {modification['id']: modification['name'] for modification in modifications}


    return render_template("client2_view_characters.html", characters=characters, factions_dict=factions_dict, armors_dict=armors_dict,
                           weapons_dict=weapons_dict, modifications_dict=modifications_dict, error_message=error_message)




if __name__ == "__main__":
    app.run(debug=True)
