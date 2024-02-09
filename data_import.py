import csv
from os import path

def data_importer():
    bundle_dir = path.abspath(path.dirname(__file__))

    path_to_heads = path.join(bundle_dir, 'AC6 - Trimmed down - HEADS.csv')
    file = open(path_to_heads, "r")
    head_data = list(csv.DictReader(file, delimiter=","))
    file.close()

    path_to_cores = path.join(bundle_dir, 'AC6 - Trimmed down - CORES.csv')
    file = open(path_to_cores, "r")
    body_data = list(csv.DictReader(file, delimiter=","))
    file.close()

    path_to_legs = path.join(bundle_dir, 'AC6 - Trimmed down - LEGS.csv')
    file = open(path_to_legs, "r")
    legs_data = list(csv.DictReader(file, delimiter=","))
    file.close()

    path_to_arms = path.join(bundle_dir, 'AC6 - Trimmed down - ARMS.csv')
    file = open(path_to_arms, "r")
    hand_data = list(csv.DictReader(file, delimiter=","))
    file.close()

    path_to_gens = path.join(bundle_dir, 'AC6 - Trimmed down - GENERATORS.csv')
    file = open(path_to_gens, "r")
    gen_data = list(csv.DictReader(file, delimiter=","))
    file.close()

    path_to_boosters = path.join(bundle_dir, 'AC6 - Trimmed down - BOOSTERS.csv')
    file = open(path_to_boosters, "r")
    boost_data = list(csv.DictReader(file, delimiter=","))
    file.close()

    gap1 = len(head_data)
    gap2 = len(head_data) + len(body_data)
    gap3 = len(head_data) + len(body_data) + len(hand_data)
    gap4 = len(head_data) + len(body_data) + len(hand_data) + len(legs_data)
    gap5 = gap4 + len(gen_data)
    gap6 = gap5 + len(boost_data)

    head_range = [n for n in range(0, gap1)]
    body_range = [n for n in range(gap1, gap2)]
    hand_range = [n for n in range(gap2, gap3)]
    legs_range = [n for n in range(gap3, gap4)]
    gen_range = [n for n in range(gap4, gap5)]
    boost_range = [n for n in range(gap5, gap6)]

    # Tag the different types for selection purposes later:
    for i in head_data:
        i["Part type"] = "Head"
    for i in body_data:
        i["Part type"] = "Core"
    for i in hand_data:
        i["Part type"] = "Arms"
    for i in legs_data:
        i["Part type"] = "Legs"
    for i in gen_data:
        i["Part type"] = "Generator"
    for i in boost_data:
        i["Part type"] = "Booster"

    frame_data = head_data + body_data + hand_data + legs_data + gen_data + boost_data

    num_pieces = len(frame_data)

    return [[frame_data, num_pieces, head_range, body_range,
            hand_range, legs_range, gen_range, boost_range],
            [head_data, body_data, hand_data, legs_data, gen_data, boost_data]]


def data_importer_noopt():
    bundle_dir = path.abspath(path.dirname(__file__))

    path_to_weapons = path.join(bundle_dir, 'AC6 - Trimmed down - ARM WEAPONS.csv')
    file = open(path_to_weapons, "r")
    weapon_data = list(csv.DictReader(file, delimiter=","))
    file.close()

    path_to_back_weapons = path.join(bundle_dir, 'AC6 - Trimmed down - BACK WEAPONS.csv')
    file = open(path_to_back_weapons, "r")
    back_data = list(csv.DictReader(file, delimiter=","))
    file.close()

    path_to_fcs = path.join(bundle_dir, 'AC6 - Trimmed down - FCS.csv')
    file = open(path_to_fcs, "r")
    fcs_data = list(csv.DictReader(file, delimiter=","))
    file.close()

    for i in weapon_data:
        i["Part type"] = "Arm Weapon"
    for i in back_data:
        i["Part type"] = "Back Weapon"
    for i in fcs_data:
        i["Part type"] = "FCS"

    return [weapon_data, back_data, fcs_data]
