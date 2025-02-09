from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from pydantic import BaseModel
from typing import List, Optional
from contextlib import asynccontextmanager

DATABASE_URL = "sqlite:///character_assembly.db"
Base = declarative_base()
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Faction(Base):
    __tablename__ = "factions"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    health = Column(Float, nullable=False)
    damage = Column(Float, nullable=False)
    speed = Column(Float, nullable=False)
    armors = relationship("Armor", back_populates="faction")
    weapons = relationship("Weapon", back_populates="faction")
    modifications = relationship("Modification", back_populates="faction")
    characters = relationship("Character", back_populates="faction")

class Armor(Base):
    __tablename__ = "armors"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True) 
    name = Column(String, nullable=False)
    faction_id = Column(Integer, ForeignKey("factions.id"))
    health_bonus = Column(Float, default=0.0)
    damage_bonus = Column(Float, default=0.0)
    speed_bonus = Column(Float, default=0.0)
    faction = relationship("Faction", back_populates="armors")


class Weapon(Base):
    __tablename__ = "weapons"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    faction_id = Column(Integer, ForeignKey("factions.id"))
    damage_bonus = Column(Float, default=0.0)
    speed_bonus = Column(Float, default=0.0)
    faction = relationship("Faction", back_populates="weapons")

class Modification(Base):
    __tablename__ = "modifications"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    faction_id = Column(Integer, ForeignKey("factions.id"))
    health_bonus = Column(Float, default=0.0)
    damage_bonus = Column(Float, default=0.0)
    speed_bonus = Column(Float, default=0.0)
    faction = relationship("Faction", back_populates="modifications")

class Character(Base):
    __tablename__ = "characters"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    faction_id = Column(Integer, ForeignKey("factions.id"))
    armor_id = Column(Integer, ForeignKey("armors.id"), nullable=True)
    weapon_id = Column(Integer, ForeignKey("weapons.id"), nullable=True)
    modification_id = Column(Integer, ForeignKey("modifications.id"), nullable=True)
    health = Column(Float, nullable=False)
    damage = Column(Float, nullable=False)
    speed = Column(Float, nullable=False)
    faction = relationship("Faction", back_populates="characters")

def initialize_database():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        default_factions = [
            {"id": 1, "name": "Империум", "health": 100.0, "damage": 20.0, "speed": 10.0},
            {"id": 2, "name": "Хаос", "health": 120.0, "damage": 25.0, "speed": 8.0},
            {"id": 3, "name": "Эльдар", "health": 80.0, "damage": 15.0, "speed": 20.0},
            {"id": 4, "name": "Орк", "health": 150.0, "damage": 30.0, "speed": 5.0},
            {"id": 5, "name": "Некрон", "health": 200.0, "damage": 10.0, "speed": 5.0},
            {"id": 6, "name": "Тиранид", "health": 90.0, "damage": 35.0, "speed": 15.0},
            {"id": 7, "name": "Тау", "health": 70.0, "damage": 20.0, "speed": 18.0}
        ]

        for faction_data in default_factions:
            faction = db.query(Faction).filter(Faction.id == faction_data["id"]).first()
            if not faction:
                new_faction = Faction(**faction_data)
                db.add(new_faction)

        db.commit()
    finally:
        db.close()

class FactionSchema(BaseModel):
    id: Optional[int]
    name: str
    health: float
    damage: float
    speed: float

    class Config:
        from_attributes = True

class ArmorSchema(BaseModel):
    id: Optional[int] = None
    name: str
    faction_id: int
    health_bonus: float = 0.0
    damage_bonus: float = 0.0
    speed_bonus: float = 0.0

    class Config:
        from_attributes = True

class WeaponSchema(BaseModel):
    id: Optional[int] = None
    name: str
    faction_id: int
    damage_bonus: float = 0.0
    speed_bonus: float = 0.0

    class Config:
        from_attributes = True

class ModificationSchema(BaseModel):
    id: Optional[int] = None
    name: str
    faction_id: int
    health_bonus: float = 0.0
    damage_bonus: float = 0.0
    speed_bonus: float = 0.0

    class Config:
        from_attributes = True

class CharacterSchema(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    faction_id: int
    armor_id: Optional[int] = None
    weapon_id: Optional[int] = None
    modification_id: Optional[int] = None
    health: Optional[float] = None
    damage: Optional[float] = None
    speed: Optional[float] = None

    class Config:
        from_attributes = True

@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()
    yield

app = FastAPI(lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.get("/factions", response_model=List[FactionSchema], tags=["Factions"])
def get_all_factions(db=Depends(get_db)):
    return db.query(Faction).all()

@app.get("/characters", response_model=List[CharacterSchema], tags=["Characters"])
def get_all_characters(db=Depends(get_db)):
    return db.query(Character).all()

@app.get("/armors", response_model=List[ArmorSchema], tags=["Components"])
def get_all_armors(db=Depends(get_db)):
    return db.query(Armor).all()

@app.get("/weapons", response_model=List[WeaponSchema], tags=["Components"])
def get_all_weapons(db=Depends(get_db)):
    return db.query(Weapon).all()

@app.get("/modifications", response_model=List[ModificationSchema], tags=["Components"])
def get_all_modifications(db=Depends(get_db)):
    return db.query(Modification).all()

@app.get("/calculate_character_parameters", response_model=CharacterSchema, tags=["Characters"])
def calculate_character_parameters(faction_id: int, armor_id: int = None, weapon_id: int = None, modification_id: int = None, db=Depends(get_db)):
    faction = db.query(Faction).filter(Faction.id == faction_id).first()
    if not faction:
        raise HTTPException(status_code=404, detail="Faction not found")

    armor = db.query(Armor).filter(Armor.id == armor_id).first() if armor_id else None
    weapon = db.query(Weapon).filter(Weapon.id == weapon_id).first() if weapon_id else None
    modification = db.query(Modification).filter(Modification.id == modification_id).first() if modification_id else None

    if (armor_id and not armor) or (weapon_id and not weapon) or (modification_id and not modification):
        raise HTTPException(status_code=400, detail="One or more components do not exist")

    if armor and armor.faction_id != faction_id:
        raise HTTPException(status_code=400, detail="Armor does not belong to the correct faction")
    if weapon and weapon.faction_id != faction_id:
        raise HTTPException(status_code=400, detail="Weapon does not belong to the correct faction")
    if modification and modification.faction_id != faction_id:
        raise HTTPException(status_code=400, detail="Modification does not belong to the correct faction")

    health = faction.health + (armor.health_bonus if armor else 0) + (modification.health_bonus if modification else 0)
    damage = faction.damage + (weapon.damage_bonus if weapon else 0) + (modification.damage_bonus if modification else 0)
    speed = faction.speed + (armor.speed_bonus if armor else 0) + (weapon.speed_bonus if weapon else 0)

    if health <= 0 or damage <= 0 or speed <= 0:
        raise HTTPException(status_code=400, detail="Character stats are unbalanced")

    calculated_character = Character(
        faction_id=faction_id,
        armor_id=armor_id,
        weapon_id=weapon_id,
        modification_id=modification_id,
        health=health,
        damage=damage,
        speed=speed
    )
    return calculated_character


@app.post("/armors", response_model=ArmorSchema, tags=["Components"])
def create_armor(armor: ArmorSchema, db=Depends(get_db)):
    print(armor.dict()) 
    faction = db.query(Faction).filter(Faction.id == armor.faction_id).first()
    if not faction:
        raise HTTPException(status_code=404, detail="Faction not found")

    new_armor = Armor(
        name=armor.name,
        faction_id=armor.faction_id,
        health_bonus=armor.health_bonus,
        damage_bonus=armor.damage_bonus,
        speed_bonus=armor.speed_bonus
    )

    db.add(new_armor)
    db.commit()
    db.refresh(new_armor)

    return new_armor



@app.post("/weapons", response_model=WeaponSchema, tags=["Components"])
def create_weapon(weapon: WeaponSchema, db=Depends(get_db)):
    faction = db.query(Faction).filter(Faction.id == weapon.faction_id).first()
    if not faction:
        raise HTTPException(status_code=404, detail="Faction not found")

    new_weapon = Weapon(
        name=weapon.name, 
        faction_id=weapon.faction_id,
        damage_bonus=weapon.damage_bonus,
        speed_bonus=weapon.speed_bonus
    )
    db.add(new_weapon)
    db.commit()
    db.refresh(new_weapon)
    return new_weapon

@app.post("/modifications", response_model=ModificationSchema, tags=["Components"])
def create_modification(modification: ModificationSchema, db=Depends(get_db)):
    faction = db.query(Faction).filter(Faction.id == modification.faction_id).first()
    if not faction:
        raise HTTPException(status_code=404, detail="Faction not found")
    new_modification = Modification(
        name=modification.name,  
        faction_id=modification.faction_id,
        health_bonus=modification.health_bonus,
        damage_bonus=modification.damage_bonus,
        speed_bonus=modification.speed_bonus
    )
    db.add(new_modification)
    db.commit()
    db.refresh(new_modification)
    return new_modification

@app.post("/characters", response_model=CharacterSchema, tags=["Characters"])
def create_character(character: CharacterSchema, db=Depends(get_db)):
    faction = db.query(Faction).filter(Faction.id == character.faction_id).first()
    if not faction:
        raise HTTPException(status_code=404, detail="Faction not found")

    # Проверяем существование каждого компонента
    armor = db.query(Armor).filter(Armor.id == character.armor_id).first() if character.armor_id else None
    weapon = db.query(Weapon).filter(Weapon.id == character.weapon_id).first() if character.weapon_id else None
    modification = db.query(Modification).filter(Modification.id == character.modification_id).first() if character.modification_id else None

    # Если хотя бы одного компонента нет в базе данных, отклоняем создание
    if (character.armor_id and not armor) or (character.weapon_id and not weapon) or (character.modification_id and not modification):
        raise HTTPException(status_code=400, detail="One or more components do not exist")

    # Проверяем фракцию для каждого компонента
    if armor and armor.faction_id != character.faction_id:
        raise HTTPException(status_code=400, detail="Armor does not belong to the correct faction")
    if weapon and weapon.faction_id != character.faction_id:
        raise HTTPException(status_code=400, detail="Weapon does not belong to the correct faction")
    if modification and modification.faction_id != character.faction_id:
        raise HTTPException(status_code=400, detail="Modification does not belong to the correct faction")

    # Вычисляем характеристики персонажа с учетом компонентов
    health = faction.health + (armor.health_bonus if armor else 0) + (modification.health_bonus if modification else 0)
    damage = faction.damage + (weapon.damage_bonus if weapon else 0) + (modification.damage_bonus if modification else 0)
    speed = faction.speed + (armor.speed_bonus if armor else 0) + (weapon.speed_bonus if weapon else 0)

    if health <= 0 or damage <= 0 or speed <= 0:
        raise HTTPException(status_code=400, detail="Character stats are unbalanced")

    new_character = Character(
        name=character.name,
        faction_id=character.faction_id,
        armor_id=character.armor_id,
        weapon_id=character.weapon_id,
        modification_id=character.modification_id,
        health=health,
        damage=damage,
        speed=speed
    )
    db.add(new_character)
    db.commit()
    db.refresh(new_character)
    return new_character




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)