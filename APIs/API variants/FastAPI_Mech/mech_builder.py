from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Данные о частях меха
bodies = {
    "strider": {"hp": 50, "durability": 30, "weight": 20, "speed": 40},
    "walker": {"hp": 70, "durability": 50, "weight": 30, "speed": 30},
    "glider": {"hp": 40, "durability": 20, "weight": 10, "speed": 60},
}

engines = {
    "light": {"hp": 0, "durability": 10, "weight": 5, "speed": 20},
    "medium": {"hp": 0, "durability": 20, "weight": 10, "speed": 15},
    "heavy": {"hp": 0, "durability": 30, "weight": 20, "speed": 10},
}

weapons = {
    "cannon": {"hp": 0, "durability": 10, "weight": 15, "speed": -5},
    "laser": {"hp": 0, "durability": 5, "weight": 10, "speed": 0},
    "missile": {"hp": 0, "durability": 8, "weight": 12, "speed": -2},
}

reactors = {
    "standard": {"hp": 10, "durability": 10, "weight": 10, "speed": 0},
    "enhanced": {"hp": 20, "durability": 5, "weight": 8, "speed": 5},
    "ultra": {"hp": 30, "durability": 0, "weight": 12, "speed": 10},
}

armors = {
    "light": {"hp": 20, "durability": 15, "weight": 5, "speed": 10},
    "medium": {"hp": 40, "durability": 30, "weight": 15, "speed": 5},
    "heavy": {"hp": 60, "durability": 50, "weight": 25, "speed": -5},
}


def assemble_mech(body, engine, weapon, reactor, armor):
    """Функция для расчета итоговых параметров меха."""
    # Начальные параметры
    total_hp, total_durability, total_weight, total_speed = 100, 100, 0, 0

    # Добавление параметров от каждой части
    for part in (bodies[body], engines[engine], weapons[weapon], reactors[reactor], armors[armor]):
        total_hp += part["hp"]
        total_durability += part["durability"]
        total_weight += part["weight"]
        total_speed += part["speed"]

    return {
        "hp": total_hp,
        "durability": total_durability,
        "weight": total_weight,
        "speed": total_speed
    }


@app.get("/")
def get_mech_builder(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "bodies": bodies,
        "engines": engines,
        "weapons": weapons,
        "reactors": reactors,
        "armors": armors
    })


@app.post("/assemble")
def post_assemble(
        request: Request,
        body: str = Form(...),
        engine: str = Form(...),
        weapon: str = Form(...),
        reactor: str = Form(...),
        armor: str = Form(...)
):
    result = assemble_mech(body, engine, weapon, reactor, armor)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "bodies": bodies,
        "engines": engines,
        "weapons": weapons,
        "reactors": reactors,
        "armors": armors,
        "result": result
    })


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=5000)
