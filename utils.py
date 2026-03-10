from tkinter import BooleanVar


def create_enemy_info_box(description:str = "Error", location:str = "", type:str = "", health:int= -1, shield:int= 0, holy_shield:int= 0,
                          damage:int= -1,movement:int= -1, luck:int= -1) -> str:

    real_health = health if health != -1 else ""
    real_shield = shield if shield != 0 else ""
    real_holy_shield = holy_shield if holy_shield != 0 else ""
    real_damage = damage if damage != -1 else ""
    real_movement = movement if movement != -1 else ""
    real_luck = luck if luck != -1 else ""

    infobox = f"""{{{{Infobox/Enemy
| Description = {description}
| Location = {location}
| Type = {type}
| Health = {real_health}
| Shield = {real_shield}
| HolyShield = {real_holy_shield}
| Damage = {real_damage}
| Movement = {real_movement}
| Luck = {real_luck}
}}}}"""
    return infobox

def find_entity_in_gon(gon_file, entity) -> bool:
    with open(gon_file, 'r') as file:
        content = file.read()
    found = entity in content
    print(f" {found} {entity} in {gon_file}")
    return found


