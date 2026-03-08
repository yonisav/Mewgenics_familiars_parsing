import csv
import utils

GON_FILES_ARRAY = ['familiars.gon', 'enemies.gon',  'cat_enemies.gon', 'small_enemies.gon', 'cat_minibosses.gon',
                   'minibosses.gon', 'bosses.gon']

class Familiar:
    def __init__(self,name:str = "Error", description:str = "Error", health:int= -1, shield:int= 0, holy_shield:int= 0,
                          damage:int= -1,movement:int= -1, luck:int= -1):
        self.name = name
        self.display_name = ""
        self.desc = description
        self.location = "Summon"
        self.health = health
        self.shield = shield
        self.holy_shield = holy_shield
        self.damage = damage
        self.movement = movement
        self.luck = luck
        self.is_interesting = False

    def __str__(self):
        rep_str = self.display_name + "\n"
        rep_str += utils.create_enemy_info_box(self.desc, self.location, self.health, self.shield, self.holy_shield, self.damage,
                                         self.movement, self.luck) +"\n"
        return rep_str

#Create a library of only the interesting familiars to avoid extra parsing later
#Interesting is anything with a different name, description or stats
def create_interesting_dictionary(familiar_file):
    is_interesting = False
    interesting_dictionary = {}
    enemy_name = ""
    field_name = ""
    level = 0
    with open('Familiars.gon', mode='r', encoding='utf-8') as f_in:
        for line in f_in:
            line = line.strip()
            if line == '':
                continue
            split_line = line.split(" ")
            if "{" in line:
                if level == 0:
                    enemy_name = split_line[0]
                elif level == 1:
                    field_name = split_line[0]
                level += 1
            elif "}" in line:
                level -= 1
            if level == 2:
                if field_name == "stats":
                    interesting_dictionary[enemy_name] = True
                    continue
                elif field_name == "graphics":
                    if split_line[0] == "name":
                        # get name from csv
                        interesting_dictionary[enemy_name] = True
                    elif split_line[0] == "tooltip":
                        # get tooltip from csv
                        interesting_dictionary[enemy_name] = True
                elif field_name == "properties":
                    if split_line[0] == "health":
                        interesting_dictionary[enemy_name] = True
                    elif split_line[0] == "shield":
                        interesting_dictionary[enemy_name] = True
                    elif split_line[0] == "movement":
                        interesting_dictionary[enemy_name] = True
                    else:
                        continue
                else:
                    continue
    return interesting_dictionary


def parse_enemy_info_recu(familiar, unit_lookup, interest) -> bool:
    found = False

    for file in GON_FILES_ARRAY:
        field_name = ""
        fam = familiar
        level = 0
        with open(file, mode='r', encoding='utf-8') as f_in:
            for line in f_in:
                line = line.strip()
                if line == '':
                    continue
                if "}" in line:
                    level -= 1
                    if found and level == 0:
                        return True
                    continue
                split_line = line.split(" ")
                if level == 0:
                    if "{" in line:
                        if interest == split_line[0]:
                            found = True
                if found:
                    if level == 1:
                        if split_line[1] == "{":
                            field_name = split_line[0]
                        # if fam is variant recursively look for the father info
                        elif split_line[0] == "variant_of":
                            parse_enemy_info_recu(familiar, unit_lookup, split_line[1])
                    elif level == 2:
                        if field_name == "stats":
                            is_interesting = True
                            if split_line[0] == "strength":
                                fam.damage = int(split_line[1])
                            elif split_line[0] == "constitution":
                                fam.health = int(split_line[1])
                            elif split_line[0] == "speed":
                                fam.movement = int(split_line[1])
                            elif split_line[0] == "luck":
                                fam.luck = int(split_line[1])

                        elif field_name == "graphics":
                            if split_line[0] == "name":
                                # get name from csv
                                fam.display_name = unit_lookup.get(split_line[1].strip('"'), fam.display_name)
                                key = split_line[1].replace("NAME", "DESC").strip('"')
                                fam.desc = unit_lookup.get(key, "")
                                print(f"{fam.display_name=}, {fam.desc=}, {split_line[1].strip('"')=}")
                            elif split_line[0] == "tooltip":
                                # get tooltip from csv
                                fam.desc = unit_lookup.get(split_line[1].strip('"'), "")
                                #print(f"{fam.display_name=}, {fam.desc=}, {split_line[1].strip('"')=}")
                        elif field_name == "properties":
                            if split_line[0] == "health":
                                fam.health = int(split_line[1])
                            elif split_line[0] == "shield":
                                fam.shield = int(split_line[1])
                            elif split_line[0] == "movement":
                                fam.movement = int(split_line[1])
                # After level processing is  done increase level
                if "{" in line:
                    level += 1
    return found


def generate_formatted_item_list():

    field_name = ""
    fam = Familiar(name="")
    level = 0
    familiar_dic  = {}

    # Load CSV data into a lookup dictionary
    unit_lookup = {}
    with open("units.csv", mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header row
        for row in reader:
            if len(row) >= 2:
                unit_lookup[row[0]] = row[1]
    with open("additions.csv", mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header row
        for row in reader:
            if len(row) >= 2:
                unit_lookup[row[0]] = row[1]

    print(unit_lookup)

    familiar_dic = create_interesting_dictionary('Familiars.gon')
    print(familiar_dic)

    with open('wiki_format_familiars.txt', 'w', encoding='utf-8') as f_out:
        for item in familiar_dic:
            fam = Familiar(name=item)
            parse_enemy_info_recu(fam, unit_lookup, item)
            f_out.write(str(fam)+"\n")


# Run the process
generate_formatted_item_list()