import pandas as pd
from ortools.sat.python import cp_model
from data_import import data_importer

def ac6_opti(input_data, selection_list):

    frame_data = input_data[0]
    num_pieces = input_data[1]
    head_range = input_data[2]
    body_range = input_data[3]
    hand_range = input_data[4]
    legs_range = input_data[5]
    gen_range = input_data[6]
    boost_range = input_data[7]

    # Non-opti weight and en load restrictions
    weapon_weight = int(selection_list[0])
    weapon_en_load = int(selection_list[1])
    # Part forcing
    head_enforce = selection_list[2]
    head_enforce_no = selection_list[3]
    core_enforce = selection_list[4]
    core_enforce_no = selection_list[5] + max(head_range) + 1
    arms_enforce = selection_list[6]
    arms_enforce_no = selection_list[7] + max(body_range) + 1
    legs_enforce = selection_list[8]
    legs_enforce_no = selection_list[9] + max(hand_range) + 1
    gen_enforce = selection_list[10]
    gen_enforce_no = selection_list[11] + max(legs_range) + 1
    boost_enforce = selection_list[12]
    boost_enforce_no = selection_list[13] + max(gen_range) + 1

    # Optimisation constraints
    weight_enforce = selection_list[14]
    if selection_list[15] == "":
        selection_list[15] = 0
    weight_enforce_no = int(selection_list[15])
    en_recharge_enforce = selection_list[16]
    if selection_list[17] == "":
        selection_list[17] = 0
    en_recharge_enforce_no = int(selection_list[17])
    ap_min_enforce = selection_list[18]
    if selection_list[19] == "":
        selection_list[19] = 0
    ap_min_enforce_no = int(selection_list[19])
    as_min_enforce = selection_list[20]
    if selection_list[21] == "":
        selection_list[21] = 0
    as_min_enforce_no = int(selection_list[21])
    en_cap_min_enforce = selection_list[22]
    if selection_list[23] == "":
        selection_list[23] = 0
    en_cap_min_enforce_no = int(selection_list[23])
    energy_spec_enforce = selection_list[24]
    if selection_list[25] == "":
        selection_list[25] = 0
    energy_spec_enforce_no = int(selection_list[25])
    recoil_enforce = selection_list[26]
    if selection_list[27] == "":
        selection_list[27] = 0
    recoil_enforce_no = int(selection_list[27])
    tracking_enforce = selection_list[28]
    if selection_list[29] == "":
        selection_list[29] = 0
    tracking_enforce_no = int(selection_list[29])
    melee_spec_enforce = selection_list[30]
    if selection_list[31] == "":
        selection_list[31] = 0
    melee_spec_enforce_no = int(selection_list[31])
    load_override = selection_list[32]

    opti_target = selection_list[33]
    arm_weapon_weight = selection_list[34]
    leg_type_force = selection_list[35]
    # Nov 24 update
    gen_type_force = selection_list[36]
    sys_rec_enforce = selection_list[37]
    if selection_list[38] == "":
        selection_list[38] = 0
    sys_rec_enforce_no = int(selection_list[38])
    boost_spd_enforce = selection_list[39]
    if selection_list[40] == "":
        selection_list[40] = 0
    boost_spd_enforce_no = int(selection_list[40])
    ab_spd_enforce = selection_list[41]
    if selection_list[42] == "":
        selection_list[42] = 0
    ab_spd_enforce_no = int(selection_list[42])
    travel_spd_enforce = selection_list[43]
    if selection_list[44] == "":
        selection_list[44] = 0
    travel_spd_enforce_no = int(selection_list[44])
    hover_spd_enforce = selection_list[45]
    if selection_list[46] == "":
        selection_list[46] = 0
    hover_spd_enforce_no = int(selection_list[46])

    model = cp_model.CpModel()
    data_pd = pd.DataFrame.from_records(frame_data)

    # Remove NaN entries
    data_pd = data_pd.fillna(0)

    # Destringing the input
    column_list = list(data_pd.columns)
    for column_name in column_list:
        data_pd[column_name] = data_pd[column_name].astype(int, errors='ignore')

    # Create optimiser variable - as I understand, this is p much a vector
    x = model.NewBoolVarSeries(name="x", index = data_pd.index)

    # Exactly 6 parts, one of each type
    for unused_name, types in data_pd.groupby("Part type"):
        model.AddExactlyOne(x[types.index])

    # Enforced part selection
    if head_enforce:
        model.Add(x[head_enforce_no] == 1)
    if core_enforce:
        model.Add(x[core_enforce_no] == 1)
    if arms_enforce:
        model.Add(x[arms_enforce_no] == 1)
    if legs_enforce:
        model.Add(x[legs_enforce_no] == 1)
    if gen_enforce:
        model.Add(x[gen_enforce_no] == 1)
    if boost_enforce:
        model.Add(x[boost_enforce_no] == 1)

    # Optimiser optional restrictions:
    # Manual weight restriction
    if weight_enforce:
        model.Add(data_pd["Weight"].dot(x) + weapon_weight <= weight_enforce_no)
    # AP Minimum
    if ap_min_enforce:
        model.Add(data_pd["AP"].dot(x) >= ap_min_enforce_no)
    # AS Minimum
    if as_min_enforce:
        model.Add(as_min_enforce_no <= data_pd['Attitude Stability'].dot(x))
    # EN Capacity Minimum
    if en_cap_min_enforce:
        model.Add(data_pd["EN Capacity"].dot(x) >= en_cap_min_enforce_no)
    # Energy FA Spec Minimum
    if energy_spec_enforce:
        model.Add(data_pd["Energy Firearm Spec."].dot(x) >= energy_spec_enforce_no)
    # Recoil Minimum
    if recoil_enforce:
        model.Add(data_pd["Recoil Control"].dot(x) >= recoil_enforce_no)
    # FA Spec Minimum
    if tracking_enforce:
        model.Add(data_pd["Target Tracking"].dot(x) >= tracking_enforce_no)
    # Melee Spec Minimum
    if melee_spec_enforce:
        model.Add(data_pd["Melee Specialization"].dot(x) >= melee_spec_enforce_no)

    # Enforced leg type:
    if leg_type_force == "Biped":
        model.Add(sum(x[min(legs_range):max(legs_range) - 8]) == 1)
    elif leg_type_force == "Reverse Joint":
        model.Add(sum(x[max(legs_range) - 8:max(legs_range) - 5]) == 1)
    elif leg_type_force == "Quad":
        model.Add(sum(x[max(legs_range)-5:max(legs_range)-2]) == 1)
    elif leg_type_force == "Tank":
        model.Add(sum(x[max(legs_range)-2:max(legs_range)+1]) == 1)

    # Enforced Generator type:
    if gen_type_force == "Normal":
        model.Add(sum(x[min(gen_range):max(gen_range) - 1]) == 1)
    elif gen_type_force == "Coral":
        model.Add(sum(x[max(gen_range) - 1:max(gen_range) + 1]) == 1)

    # Leg load limit
    if load_override is False:
        leg_weight = model.NewIntVar(1, 49800, 'leg_weight')
        model.Add(leg_weight == data_pd.loc[data_pd["Part type"] == "Legs", "Weight"].dot(x.iloc[min(legs_range):max(legs_range) + 1]))
        model.Add(data_pd["Weight"].dot(x) - leg_weight + weapon_weight <= data_pd["Load Limit"].dot(x))

    # Arm load limit
    arm_load_limit = model.NewIntVar(0, 25000, 'arm_load_limit')
    model.Add(arm_load_limit == data_pd["Arms Load Limit"].dot(x))
    model.Add(arm_load_limit >= arm_weapon_weight)
    # EN Load Limit
    raw_output = model.NewIntVarFromDomain(cp_model.Domain.FromValues(data_pd['EN Output']), 'raw_output')
    core_adj = model.NewIntVarFromDomain(cp_model.Domain.FromValues(data_pd['Generator Output Adj.']), 'core_adj')
    adj_output = model.NewIntVar(2340*83, 4430*126, 'adj_output')
    model.AddMultiplicationEquality(adj_output, [raw_output, core_adj])

    # Output as calculated must be larger than EN Load
    model.Add((data_pd["EN Load"].dot(x) + weapon_en_load) * 100 <= adj_output)
    # Tie down output as calculated to the actually selected pieces:
    model.Add(data_pd["EN Output"].dot(x) == raw_output)
    model.Add(data_pd['Generator Output Adj.'].dot(x) == core_adj)

    # Free EN Minimum
    if en_recharge_enforce:
        model.Add(((4166 * (adj_output - (data_pd["EN Load"].dot(x) + weapon_en_load) * 100)) + 1500) >= en_recharge_enforce_no * 100000)
    # 4.166 * (en_load_max - en_load) + 1500

    # Restrict Tank legs and Boosters to only work together
    # Yes I'm hard coding it. Sue me.
    model.Add(x.iloc[max(legs_range)-2] == x.iloc[max(boost_range)-2])
    model.Add(x.iloc[max(legs_range)-1] == x.iloc[max(boost_range)-1])
    model.Add(x.iloc[max(legs_range)] == x.iloc[max(boost_range)])

    # Effective HP target - groundwork
    total_ap = model.NewIntVar(5720000, 18680000, 'total_ap')
    kinetic_def = model.NewIntVar(892, 1421, 'kinetic_def')
    energy_def = model.NewIntVar(0, 2000, 'energy_def')
    explosive_def = model.NewIntVar(0, 2000, 'explosive_def')
    # Tie this to the real variables:
    model.Add(data_pd["AP"].dot(x) * 1000 == total_ap)

    model.Add(data_pd["Anti-Kinetic Defense"].dot(x) == kinetic_def)
    kinetic_red = model.NewIntVar(500, 5000, 'kinetic_red') # CARE! Do NOT include 0
    kinetic_ehp = model.NewIntVar(0, 330000, 'kinetic_ehp')
    model.Add(kinetic_red == 2000 - kinetic_def)
    model.AddDivisionEquality(kinetic_ehp, total_ap, kinetic_red)

    model.Add(data_pd["Anti-Energy Defense"].dot(x) == energy_def)
    energy_red = model.NewIntVar(1, 5000, 'energy_red')
    energy_ehp = model.NewIntVar(0, 500000, 'energy_ehp')
    model.Add(energy_red == 2000 - energy_def)
    model.AddDivisionEquality(energy_ehp, total_ap, energy_red)

    model.Add(data_pd["Anti-Explosive Defense"].dot(x) == explosive_def)
    explosive_red = model.NewIntVar(1, 5000, 'explosive_red')
    explosive_ehp = model.NewIntVar(0, 500000, 'explosive_ehp')
    model.Add(explosive_red == 2000 - explosive_def)
    model.AddDivisionEquality(explosive_ehp, total_ap, explosive_red)

    overall_ehp = model.NewIntVar(1, 500000000, 'overall_ehp')
    sum_of_ehp = model.NewIntVar(0, 2000000000, 'sum_of_ehp')
    model.Add(sum_of_ehp == kinetic_ehp + energy_ehp + explosive_ehp + data_pd["AP"].dot(x))
    model.AddDivisionEquality(overall_ehp, sum_of_ehp, 4)

    # Speed implementation

    # Define constraint variables for the different types of speed
    # Need to do this in terms of thrust since optimiser only supports integers and no rounding methods in its constraints
    # ...Actually, need to scale the values up intensely. Base thrust goes up to ~8k, then increase by a factor of
    # roundabout 100*1/10*10^5*10^6 -> 10^12? Should work. So domain goes from 4*10^15 to 9*10^15
    # Define constraint variable for weight
    # Define constraint bool variables for the weight breakpoints:
    # Boost Speed, QB speed, and Melee Lunge Speed: 40k, 50k, 62.5k, 75k, 80k (diff multipliers though)
    # AB Speed: 40k, 50k, 75k, 100k
    # Tetrapod Hover Speed: 70k, 90k, 100k, 110k
    # Tank travel speed: 50k, 75k, 100k, 110k
    # Fortaleza tank travel speed: 50k, 62.5k, 75k, 100k

    # So in total want 40k, 50k, 62.5k, 70k, 75k, 80k, 90k, 100k, 110k, 120k, 150k
    if boost_spd_enforce or ab_spd_enforce or hover_spd_enforce or travel_spd_enforce:
        wb_under40 = model.NewBoolVar('wb_under40')
        model.Add(data_pd["Weight"].dot(x) + weapon_weight <= 40000).OnlyEnforceIf(wb_under40)
        model.Add(data_pd["Weight"].dot(x) + weapon_weight > 40000).OnlyEnforceIf(wb_under40.Not())

        wb_under50 = model.NewBoolVar('wb_under50')
        model.Add(data_pd["Weight"].dot(x) + weapon_weight <= 50000).OnlyEnforceIf(wb_under50)
        model.Add(data_pd["Weight"].dot(x) + weapon_weight > 50000).OnlyEnforceIf(wb_under50.Not())

        wb_under62 = model.NewBoolVar('wb_under62')
        model.Add(data_pd["Weight"].dot(x) + weapon_weight <= 62500).OnlyEnforceIf(wb_under62)
        model.Add(data_pd["Weight"].dot(x) + weapon_weight > 62500).OnlyEnforceIf(wb_under62.Not())

        wb_under70 = model.NewBoolVar('wb_under70')
        model.Add(data_pd["Weight"].dot(x) + weapon_weight <= 70000).OnlyEnforceIf(wb_under70)
        model.Add(data_pd["Weight"].dot(x) + weapon_weight > 70000).OnlyEnforceIf(wb_under70.Not())

        wb_under75 = model.NewBoolVar('wb_under75')
        model.Add(data_pd["Weight"].dot(x) + weapon_weight <= 75000).OnlyEnforceIf(wb_under75)
        model.Add(data_pd["Weight"].dot(x) + weapon_weight > 75000).OnlyEnforceIf(wb_under75.Not())

        wb_under80 = model.NewBoolVar('wb_under80')
        model.Add(data_pd["Weight"].dot(x) + weapon_weight <= 80000).OnlyEnforceIf(wb_under80)
        model.Add(data_pd["Weight"].dot(x) + weapon_weight > 80000).OnlyEnforceIf(wb_under80.Not())

        wb_under90 = model.NewBoolVar('wb_under90')
        model.Add(data_pd["Weight"].dot(x) + weapon_weight <= 90000).OnlyEnforceIf(wb_under90)
        model.Add(data_pd["Weight"].dot(x) + weapon_weight > 90000).OnlyEnforceIf(wb_under90.Not())

        wb_under100 = model.NewBoolVar('wb_under100')
        model.Add(data_pd["Weight"].dot(x) + weapon_weight <= 100000).OnlyEnforceIf(wb_under100)
        model.Add(data_pd["Weight"].dot(x) + weapon_weight > 100000).OnlyEnforceIf(wb_under100.Not())

        wb_under110 = model.NewBoolVar('wb_under110')
        model.Add(data_pd["Weight"].dot(x) + weapon_weight <= 110000).OnlyEnforceIf(wb_under110)
        model.Add(data_pd["Weight"].dot(x) + weapon_weight > 110000).OnlyEnforceIf(wb_under110.Not())

        wb_under120 = model.NewBoolVar('wb_under120')
        model.Add(data_pd["Weight"].dot(x) + weapon_weight <= 120000).OnlyEnforceIf(wb_under120)
        model.Add(data_pd["Weight"].dot(x) + weapon_weight > 120000).OnlyEnforceIf(wb_under120.Not())

        wb_under150 = model.NewBoolVar('wb_under150')
        model.Add(data_pd["Weight"].dot(x) + weapon_weight <= 150000).OnlyEnforceIf(wb_under150)
        model.Add(data_pd["Weight"].dot(x) + weapon_weight > 150000).OnlyEnforceIf(wb_under150.Not())

    # I think the issue is that I need to do this via multiplication constraints?
    # So define a speed multi variable that is tied to weight based on multiplication
    # And then add linear constraint of boost_spd_enforce_no >= base speed * multiplier?

    # Big issue: conditional enforcement via .OnlyEnforceIf does *not* work for multiplicative constraints.
    base_speed = model.NewIntVar(0, 410, 'base_speed')
    model.Add(data_pd['Base Speed'].dot(x) == base_speed)
    ab_base_speed = model.NewIntVar(0, 630, 'ab_base_speed')
    model.Add(data_pd['AB Base Speed'].dot(x) == ab_base_speed)
    hover_base_speed = model.NewIntVar(0, 390, 'hover_base_speed')
    model.Add(data_pd['Tetrapod Hover Speed'].dot(x) == hover_base_speed)
    tank_base_speed = model.NewIntVar(0, 430, 'tank_base_speed')
    model.Add(data_pd['High-Speed Perf.'].dot(x) == tank_base_speed)
    total_weight = model.NewIntVar(0, 1000000, 'total_weight')
    model.Add(data_pd["Weight"].dot(x) + weapon_weight == total_weight)

    if boost_spd_enforce:
        model.Add(boost_spd_enforce_no <= base_speed).OnlyEnforceIf(wb_under40)

        speed_mod_1 = model.NewIntVar(0, 100000000000000, 'speed_mod_1')
        speed_boost_1 = model.NewIntVar(0, 100000000000000, 'speed_boost_1')
        model.Add(speed_mod_1 == (1 * 10**10 - (total_weight - 40000) * 33333))
        model.AddMultiplicationEquality(speed_boost_1, base_speed, speed_mod_1)
        model.Add(boost_spd_enforce_no * 10**10 <= speed_boost_1).OnlyEnforceIf(wb_under62, wb_under40.Not())

        speed_mod_2 = model.NewIntVar(0, 100000000000000, 'speed_mod_2')
        speed_boost_2 = model.NewIntVar(0, 100000000000000, 'speed_boost_2')
        model.Add(speed_mod_2 == (925 * 10**3 - (total_weight - 62500) * 6))
        model.AddMultiplicationEquality(speed_boost_2, base_speed, speed_mod_2)
        model.Add(boost_spd_enforce_no * 10 ** 6 <= speed_boost_2).OnlyEnforceIf(wb_under75, wb_under62.Not())

        speed_mod_3 = model.NewIntVar(0, 100000000000000, 'speed_mod_3')
        speed_boost_3 = model.NewIntVar(0, 100000000000000, 'speed_boost_3')
        model.Add(speed_mod_3 == (850 * 10**3 - (total_weight - 75000) * 15))
        model.AddMultiplicationEquality(speed_boost_3, base_speed, speed_mod_3)
        model.Add(boost_spd_enforce_no * 10 ** 6 <= speed_boost_3).OnlyEnforceIf(wb_under80, wb_under75.Not())

        speed_mod_3 = model.NewIntVar(0, 100000000000000, 'speed_mod_3')
        speed_boost_3 = model.NewIntVar(0, 100000000000000, 'speed_boost_3')
        model.Add(speed_mod_3 == (775 * 10 ** 6 - (total_weight - 80000) * 3125))
        model.AddMultiplicationEquality(speed_boost_3, base_speed, speed_mod_3)
        model.Add(boost_spd_enforce_no * 10 ** 9 <= speed_boost_3).OnlyEnforceIf(wb_under120, wb_under80.Not())

        model.Add(boost_spd_enforce_no * 100 <= 65 * base_speed).OnlyEnforceIf(wb_under120.Not())

    if ab_spd_enforce:
        model.Add(ab_spd_enforce_no <= ab_base_speed).OnlyEnforceIf(wb_under40)

        ab_speed_mod_1 = model.NewIntVar(0, 100000000000000, 'ab_speed_mod_1')
        ab_speed_boost_1 = model.NewIntVar(0, 100000000000000, 'ab_speed_boost_1')
        model.Add(ab_speed_mod_1 == (1 * 10 ** 6 - (total_weight - 40000) * 5))
        model.AddMultiplicationEquality(ab_speed_boost_1, ab_base_speed, ab_speed_mod_1)
        model.Add(ab_spd_enforce_no * 10 ** 6 <= ab_speed_boost_1).OnlyEnforceIf(wb_under50, wb_under40.Not())

        ab_speed_mod_2 = model.NewIntVar(0, 100000000000000, 'ab_speed_mod_2')
        ab_speed_boost_2 = model.NewIntVar(0, 100000000000000, 'ab_speed_boost_2')
        model.Add(ab_speed_mod_2 == (950 * 10 ** 3 - (total_weight - 50000) * 2))
        model.AddMultiplicationEquality(ab_speed_boost_2, ab_base_speed, ab_speed_mod_2)
        model.Add(ab_spd_enforce_no * 10 ** 6 <= ab_speed_boost_2).OnlyEnforceIf(wb_under75, wb_under50.Not())

        ab_speed_mod_3 = model.NewIntVar(0, 100000000000000, 'ab_speed_mod_3')
        ab_speed_boost_3 = model.NewIntVar(0, 100000000000000, 'ab_speed_boost_3')
        model.Add(ab_speed_mod_3 == (900 * 10 ** 3 - (total_weight - 75000) * 8))
        model.AddMultiplicationEquality(ab_speed_boost_3, ab_base_speed, ab_speed_mod_3)
        model.Add(ab_spd_enforce_no * 10 ** 6 <= ab_speed_boost_3).OnlyEnforceIf(wb_under100, wb_under75.Not())

        ab_speed_mod_4 = model.NewIntVar(0, 100000000000000, 'ab_speed_mod_4')
        ab_speed_boost_4 = model.NewIntVar(0, 100000000000000, 'ab_speed_boost_4')
        model.Add(ab_speed_mod_4 == (700 * 10 ** 3 - (total_weight - 100000) * 3))
        model.AddMultiplicationEquality(ab_speed_boost_4, ab_base_speed, ab_speed_mod_4)
        model.Add(ab_spd_enforce_no * 10 ** 6 <= ab_speed_boost_4).OnlyEnforceIf(wb_under100.Not())

    if hover_spd_enforce:
        model.Add(hover_spd_enforce_no <= hover_base_speed).OnlyEnforceIf(wb_under70)

        hover_speed_mod_1 = model.NewIntVar(0, 100000000000000, 'hover_speed_mod_1')
        hover_speed_boost_1 = model.NewIntVar(0, 100000000000000, 'hover_speed_boost_1')
        model.Add(hover_speed_mod_1 == (1 * 10 ** 6 - (total_weight - 70000) * 5))
        model.AddMultiplicationEquality(hover_speed_boost_1, hover_base_speed, hover_speed_mod_1)
        model.Add(hover_spd_enforce_no * 10 ** 6 <= hover_speed_boost_1).OnlyEnforceIf(wb_under100, wb_under70.Not())

        hover_speed_mod_2 = model.NewIntVar(0, 100000000000000, 'hover_speed_mod_2')
        hover_speed_boost_2 = model.NewIntVar(0, 100000000000000, 'hover_speed_boost_2')
        model.Add(hover_speed_mod_2 == (850 * 10 ** 3 - (total_weight - 100000) * 10))
        model.AddMultiplicationEquality(hover_speed_boost_2, hover_base_speed, hover_speed_mod_2)
        model.Add(hover_spd_enforce_no * 10 ** 6 <= hover_speed_boost_2).OnlyEnforceIf(wb_under110, wb_under100.Not())

        hover_speed_mod_3 = model.NewIntVar(0, 100000000000000, 'hover_speed_mod_3')
        hover_speed_boost_3 = model.NewIntVar(0, 100000000000000, 'hover_speed_boost_3')
        model.Add(hover_speed_mod_3 == (750 * 10 ** 3 - (total_weight - 110000) * 5))
        model.AddMultiplicationEquality(hover_speed_boost_3, hover_base_speed, hover_speed_mod_3)
        model.Add(hover_spd_enforce_no * 10 ** 6 <= hover_speed_boost_3).OnlyEnforceIf(wb_under120, wb_under110.Not())

        model.Add(hover_spd_enforce_no * 100 <= 70 * hover_base_speed).OnlyEnforceIf(wb_under120.Not())

    if travel_spd_enforce:
        # Need to use different modifiers for wheelchair tank vs the other two tanks
        fortaleza = model.NewBoolVar('fortaleza')
        model.Add(x.iloc[max(legs_range)] == 1).OnlyEnforceIf(fortaleza)
        model.Add(x.iloc[max(legs_range)] != 1).OnlyEnforceIf(fortaleza.Not())

        model.Add(travel_spd_enforce_no <= tank_base_speed).OnlyEnforceIf(wb_under50, fortaleza.Not())

        tank_speed_mod_1 = model.NewIntVar(0, 100000000000000, 'tank_speed_mod_1')
        tank_speed_boost_1 = model.NewIntVar(0, 100000000000000, 'tank_speed_boost_1')
        model.Add(tank_speed_mod_1 == (1 * 10 ** 6 - (total_weight - 50000) * 4))
        model.AddMultiplicationEquality(tank_speed_boost_1, tank_base_speed, tank_speed_mod_1)
        model.Add(travel_spd_enforce_no * 10 ** 6 <= tank_speed_boost_1).OnlyEnforceIf(wb_under75, wb_under50.Not(), fortaleza.Not())

        tank_speed_mod_2 = model.NewIntVar(0, 100000000000000, 'tank_speed_mod_2')
        tank_speed_boost_2 = model.NewIntVar(0, 100000000000000, 'tank_speed_boost_2')
        model.Add(tank_speed_mod_2 == (900 * 10 ** 3 - (total_weight - 75000) * 2))
        model.AddMultiplicationEquality(tank_speed_boost_2, tank_base_speed, tank_speed_mod_2)
        model.Add(travel_spd_enforce_no * 10 ** 6 <= tank_speed_boost_2).OnlyEnforceIf(wb_under100, wb_under75.Not(), fortaleza.Not())

        tank_speed_mod_3 = model.NewIntVar(0, 100000000000000, 'tank_speed_mod_3')
        tank_speed_boost_3 = model.NewIntVar(0, 100000000000000, 'tank_speed_boost_3')
        model.Add(tank_speed_mod_3 == (850 * 10 ** 4 - (total_weight - 100000) * 25))
        model.AddMultiplicationEquality(tank_speed_boost_3, tank_base_speed, tank_speed_mod_3)
        model.Add(travel_spd_enforce_no * 10 ** 7 <= tank_speed_boost_3).OnlyEnforceIf(wb_under110, wb_under100.Not(), fortaleza.Not())

        tank_speed_mod_4 = model.NewIntVar(0, 100000000000000, 'tank_speed_mod_4')
        tank_speed_boost_4 = model.NewIntVar(0, 100000000000000, 'tank_speed_boost_4')
        model.Add(tank_speed_mod_4 == (800 * 10 ** 3 - (total_weight - 110000) * 5))
        model.AddMultiplicationEquality(tank_speed_boost_4, tank_base_speed, tank_speed_mod_4)
        model.Add(travel_spd_enforce_no * 10 ** 6 <= tank_speed_boost_4).OnlyEnforceIf(wb_under120, wb_under110.Not(), fortaleza.Not())

        model.Add(travel_spd_enforce_no * 100 <= 70 * tank_base_speed).OnlyEnforceIf(wb_under120.Not(), fortaleza.Not())

        model.Add(travel_spd_enforce_no <= tank_base_speed).OnlyEnforceIf(wb_under50, fortaleza)

        fortaleza_speed_mod_1 = model.NewIntVar(0, 100000000000000, 'fortaleza_speed_mod_1')
        fortaleza_speed_boost_1 = model.NewIntVar(0, 100000000000000, 'fortaleza_speed_boost_1')
        model.Add(fortaleza_speed_mod_1 == (1 * 10 ** 7 - (total_weight - 50000) * 48))
        model.AddMultiplicationEquality(fortaleza_speed_boost_1, tank_base_speed, fortaleza_speed_mod_1)
        model.Add(travel_spd_enforce_no * 10 ** 7 <= fortaleza_speed_boost_1).OnlyEnforceIf(wb_under62, wb_under50.Not(), fortaleza)

        fortaleza_speed_mod_2 = model.NewIntVar(0, 100000000000000, 'fortaleza_speed_mod_2')
        fortaleza_speed_boost_2 = model.NewIntVar(0, 100000000000000, 'fortaleza_speed_boost_2')
        model.Add(fortaleza_speed_mod_2 == (940 * 10 ** 4 - (total_weight - 62500) * 64))
        model.AddMultiplicationEquality(fortaleza_speed_boost_2, tank_base_speed, fortaleza_speed_mod_2)
        model.Add(travel_spd_enforce_no * 10 ** 7 <= fortaleza_speed_boost_2).OnlyEnforceIf(wb_under75, wb_under62.Not(), fortaleza)

        fortaleza_speed_mod_3 = model.NewIntVar(0, 100000000000000, 'fortaleza_speed_mod_3')
        fortaleza_speed_boost_3 = model.NewIntVar(0, 100000000000000, 'fortaleza_speed_boost_3')
        model.Add(fortaleza_speed_mod_3 == (860 * 10 ** 4 - (total_weight - 75000) * 44))
        model.AddMultiplicationEquality(fortaleza_speed_boost_3, tank_base_speed, fortaleza_speed_mod_3)
        model.Add(travel_spd_enforce_no * 10 ** 7 <= fortaleza_speed_boost_3).OnlyEnforceIf(wb_under100, wb_under75.Not(), fortaleza)

        fortaleza_speed_mod_4 = model.NewIntVar(0, 100000000000000, 'fortaleza_speed_mod_4')
        fortaleza_speed_boost_4 = model.NewIntVar(0, 100000000000000, 'fortaleza_speed_boost_4')
        model.Add(fortaleza_speed_mod_4 == (750 * 10 ** 3 - (total_weight - 110000) * 3))
        model.AddMultiplicationEquality(fortaleza_speed_boost_4, tank_base_speed, fortaleza_speed_mod_4)
        model.Add(travel_spd_enforce_no * 10 ** 6 <= fortaleza_speed_boost_4).OnlyEnforceIf(wb_under150, wb_under100.Not(), fortaleza)

        model.Add(travel_spd_enforce_no * 100 <= 60 * tank_base_speed).OnlyEnforceIf(wb_under150.Not(), fortaleza)


    # (1 - (weight - 40000) * (30/9) * 10**(-6))
    # Create objective function
    if opti_target == 0:
        model.Maximize(overall_ehp)
    elif opti_target == 1:
        model.Maximize(kinetic_ehp)
    elif opti_target == 2:
        model.Maximize(energy_ehp)
    elif opti_target == 3:
        model.Maximize(explosive_ehp)
    elif opti_target == 4:
        model.Maximize(data_pd["AP"].dot(x))
    elif opti_target == 5:
        model.Maximize(data_pd['Attitude Stability'].dot(x))
    elif opti_target == 6:
        model.Minimize(data_pd['Weight'].dot(x))
    elif opti_target == 7:
        model.Maximize(data_pd['Weight'].dot(x))


    # Instantiate model
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # Print solution.
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print(f"Target = {solver.ObjectiveValue()}")
        selected = data_pd.loc[solver.BooleanValues(x).loc[lambda x: x].index]
        opti_list = list(selected.index)
        opti_list.append(solver.ObjectiveValue())
        for unused_index, row in selected.iterrows():
            print(f"{row['Part type']}: {row['Part name']}")
        print("\n")
    else:
        print("No solution found.")
        opti_list = "Error"

    return opti_list

if __name__ == "__main__":
    data = data_importer()[0]
    opti_output = ac6_opti(data)
    print(opti_output)
    print(type(opti_output))