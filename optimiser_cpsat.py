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
    en_min_enforce = selection_list[16]
    if selection_list[17] == "":
        selection_list[17] = 0
    en_min_enforce_no = int(selection_list[17])
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
    fa_spec_enforce = selection_list[28]
    if selection_list[29] == "":
        selection_list[29] = 0
    fa_spec_enforce_no = int(selection_list[29])
    melee_spec_enforce = selection_list[30]
    if selection_list[31] == "":
        selection_list[31] = 0
    melee_spec_enforce_no = int(selection_list[31])
    load_override = selection_list[32]

    opti_target = selection_list[33]
    arm_weapon_weight = selection_list[34]
    leg_type_force = selection_list[35]

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
    # Free EN Minimum
    if en_min_enforce:
        free_en_min = en_min_enforce_no
    else:
        free_en_min = 0
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
    if fa_spec_enforce:
        model.Add(data_pd["Firearm Specialization"].dot(x) >= fa_spec_enforce_no)
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

    # Leg load limit
    if load_override is False:
        leg_weight = model.NewIntVar(1, 49800, 'leg_weight')
        model.Add(leg_weight == data_pd.loc[data_pd["Part type"] == "Legs", "Weight"].dot(x.iloc[min(legs_range):max(legs_range) + 1]))
        model.Add(data_pd["Weight"].dot(x) - leg_weight + weapon_weight <= data_pd["Load Limit"].dot(x))
    # Arm load limit

    arm_load_limit = model.NewIntVar(0, 25000, 'arm_load_limit')
    # model.Add(arm_load_limit == data_pd.loc[data_pd["Part Type"] == "Arms", "Arms Load Limit"].dot(x.iloc[min(hand_range):max(hand_range) + 1]))
    model.Add(arm_load_limit == data_pd["Arms Load Limit"].dot(x))
    model.Add(arm_load_limit >= arm_weapon_weight)
    # EN Load Limit
    raw_output = model.NewIntVarFromDomain(cp_model.Domain.FromValues(data_pd['EN Output']), 'raw_output')
    core_adj = model.NewIntVarFromDomain(cp_model.Domain.FromValues(data_pd['Generator Output Adj.']), 'core_adj')
    adj_output = model.NewIntVar(2340*83, 4430*126, 'adj_output')
    model.AddMultiplicationEquality(adj_output, [raw_output, core_adj])

    # Output as calced must be larger than EN Load
    model.Add((data_pd["EN Load"].dot(x) + weapon_en_load + free_en_min) * 100 <= adj_output)
    # Tie down output as calced to the actually selected pieces:
    model.Add(data_pd["EN Output"].dot(x) == raw_output)
    model.Add(data_pd['Generator Output Adj.'].dot(x) == core_adj)

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