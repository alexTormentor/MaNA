from flask import Flask, render_template, request

app = Flask(__name__)

# Данные о частях меха с новыми категориями и параметрами
bodies = {
    "strider": {"hp": 50, "durability": 30, "weight": 20, "speed": 40, "energy": 10},
    "walker": {"hp": 70, "durability": 50, "weight": 30, "speed": 30, "energy": 15},
    "glider": {"hp": 40, "durability": 20, "weight": 10, "speed": 60, "energy": 8},
}

engines = {
    "light": {"hp": 0, "durability": 10, "weight": 5, "speed": 20, "energy_use": 5},
    "medium": {"hp": 0, "durability": 20, "weight": 10, "speed": 15, "energy_use": 10},
    "heavy": {"hp": 0, "durability": 30, "weight": 20, "speed": 10, "energy_use": 15},
}

weapons = {
    "cannon": {"hp": 0, "durability": 10, "weight": 15, "speed": -5, "damage": 20, "energy_use": 7},
    "laser": {"hp": 0, "durability": 5, "weight": 10, "speed": 0, "damage": 15, "energy_use": 10},
    "missile": {"hp": 0, "durability": 8, "weight": 12, "speed": -2, "damage": 25, "energy_use": 12},
}

reactors = {
    "standard": {"hp": 10, "durability": 10, "weight": 10, "speed": 0, "energy": 20},
    "enhanced": {"hp": 20, "durability": 5, "weight": 8, "speed": 5, "energy": 30},
    "ultra": {"hp": 30, "durability": 0, "weight": 12, "speed": 10, "energy": 50},
}

armors = {
    "light": {"hp": 20, "durability": 15, "weight": 5, "speed": 10, "damage_resist": 5},
    "medium": {"hp": 40, "durability": 30, "weight": 15, "speed": 5, "damage_resist": 10},
    "heavy": {"hp": 60, "durability": 50, "weight": 25, "speed": -5, "damage_resist": 15},
}

shields = {
    "basic": {"durability": 20, "weight": 5, "energy_use": 10, "shield_strength": 30},
    "advanced": {"durability": 30, "weight": 8, "energy_use": 15, "shield_strength": 50},
    "elite": {"durability": 40, "weight": 10, "energy_use": 20, "shield_strength": 70},
}

modules = {
    "speed_booster": {"weight": 5, "speed": 10, "energy_use": 5},
    "armor_plating": {"weight": 10, "hp": 20, "durability": 15},
    "targeting_system": {"weight": 3, "damage": 10, "energy_use": 7},
}


def assemble_mech(body, engine, weapon, reactor, armor, shield, module):
    """Функция для расчета итоговых параметров меха с новыми расчетами и проверками."""
    total_hp, total_durability, total_weight, total_speed = 100, 100, 0, 0
    total_damage, total_shield, total_energy, total_energy_use = 0, 0, 0, 0

    # Расчет параметров меха
    for part in (
    bodies[body], engines[engine], weapons[weapon], reactors[reactor], armors[armor], shields[shield], modules[module]):
        total_hp += part.get("hp", 0)
        total_durability += part.get("durability", 0)
        total_weight += part.get("weight", 0)
        total_speed += part.get("speed", 0)
        total_damage += part.get("damage", 0)
        total_shield += part.get("shield_strength", 0)
        total_energy += part.get("energy", 0)
        total_energy_use += part.get("energy_use", 0)

    # Проверка энергопотребления
    if total_energy < total_energy_use:
        return {"error": "Недостаточно энергии для поддержки всех систем"}

    # Ограничения по весу
    max_weight = 100
    if total_weight > max_weight:
        return {"error": "Перегрузка: вес меха превышает допустимый предел"}

    return {
        "hp": total_hp,
        "durability": total_durability,
        "weight": total_weight,
        "speed": total_speed,
        "damage": total_damage,
        "shield": total_shield,
        "energy_balance": total_energy - total_energy_use,
    }


@app.route("/", methods=["GET", "POST"])
def mech_builder():
    result = None
    if request.method == "POST":
        body = request.form["body"]
        engine = request.form["engine"]
        weapon = request.form["weapon"]
        reactor = request.form["reactor"]
        armor = request.form["armor"]
        shield = request.form["shield"]
        module = request.form["module"]

        # Рассчитываем параметры меха
        result = assemble_mech(body, engine, weapon, reactor, armor, shield, module)

    return render_template("index.html", bodies=bodies, engines=engines, weapons=weapons,
                           reactors=reactors, armors=armors, shields=shields, modules=modules, result=result)


if __name__ == "__main__":
    app.run(debug=True)
