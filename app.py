import sys
import threading
import pyqtgraph as pg
from data_import import data_importer
from data_import import data_importer_noopt
from optimiser_cpsat import ac6_opti
import winsound

from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton)

from main_window_ui import Ui_MainWindow



class AreaSearchWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Area Search")
        # Temperature vs time plot
        self.plot_graph = pg.plot()
        self.plot_graph.showGrid(x=True, y=True)
        self.plot_graph.setTitle("Target vs Weight")
        layout = QVBoxLayout()
        layout.addWidget(self.plot_graph)
        new_button = QPushButton()
        new_button.setText("Run Area search")
        new_button.clicked.connect(self.button_clicked)
        layout.addWidget(new_button)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def button_clicked(self):
        # I'm only doing weight stuff today, idc.
        # Both of the below call on the instance that's created at the end, not the general class, but should be fine
        self.curr_select = win.get_current_selection_opti()
        self.opti_data_ref = win.opti_data
        weight_limit_list = []
        selection_list = []
        if hasattr(self, 'line'):
            self.line.clear()
        if self.curr_select[14] == 1 and self.curr_select[15] != "":
            self.curr_select[15] = int(self.curr_select[15])
            baseval = self.curr_select[15] - 5000
            for modifier in range(0, 11):
                self.curr_select[15] = baseval + modifier * 1000
                weight_limit_list.append(self.curr_select[15])
                try:
                    selection_list.append(ac6_opti(self.opti_data_ref, self.curr_select)[6])
                except IndexError:
                    selection_list.append(0)
                    print(f"No solution found for weight limit of {self.curr_select[15]}")
            self.line = self.plot_graph.plot(weight_limit_list, selection_list)
        else:
            print("Please input a relevant weight limit and enable the restriction")
            threading.Thread(
                target=lambda: winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
            ).start()



class Window(QMainWindow, Ui_MainWindow):
    add_data = data_importer_noopt()
    imported_data = data_importer()
    opti_data = imported_data[0]
    list_data = imported_data[1]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.w = None
        self.setupUi(self)
        self.setWindowTitle("Armored Core VI - Optimizer")
        self.populate_lists(self.list_data, self.add_data)
        self.connectSignalSlots()
        # Starting off with custom weight fields hidden:
        self.as_weight.hide()
        self.ehp_weight.hide()
        self.as_weight_label.hide()
        self.ehp_weight_label.hide()
        # Default values for custom weights:
        self.as_weight.setText("8")
        self.ehp_weight.setText("1")

    def list_maker(self, add_data):
        weapon_list_l = add_data[0]
        weapon_list_r = []
        for i in range(0, len(add_data[0])):
            if add_data[0][i]["Weapon Type"] != "Melee":
                weapon_list_r.append(add_data[0][i])
        back_list_l = add_data[1] + add_data[0]
        back_list_r = []
        for i in range(0, len(add_data[1])):
            if add_data[1][i]["Weapon Type"] != "Shield":
                back_list_r.append(add_data[1][i])
        back_list_r = back_list_r + weapon_list_r
        fcs_list = add_data[2]
        option_list = [weapon_list_r, weapon_list_l, back_list_r, back_list_l, fcs_list]

        return option_list

    def get_current_selection_stats(self):
        selection_list = []
        selection_list.append(self.RightArm.currentIndex())
        selection_list.append(self.LeftArm.currentIndex())
        selection_list.append(self.RightBack.currentIndex())
        selection_list.append(self.LeftBack.currentIndex())
        selection_list.append(self.FCS.currentIndex())
        selection_list.append(self.Head_Select.currentIndex())
        selection_list.append(self.Core_Select.currentIndex())
        selection_list.append(self.Arms_Select.currentIndex())
        selection_list.append(self.Legs_Select.currentIndex())
        selection_list.append(self.Gen.currentIndex())
        selection_list.append(self.Boost.currentIndex())
        return selection_list

    def get_current_selection_opti(self):
        selection_list = []

        data_list = self.get_current_selection_stats()
        option_list = self.list_maker(self.add_data)
        weight = int(option_list[0][data_list[0]]["Weight"]) + int(option_list[1][data_list[1]]["Weight"]) + int(option_list[2][data_list[2]]["Weight"]) + int(option_list[3][data_list[3]]["Weight"]) + int(option_list[4][data_list[4]]["Weight"])
        en_load = int(option_list[0][data_list[0]]["EN Load"]) + int(option_list[1][data_list[1]]["EN Load"]) + int(option_list[2][data_list[2]]["EN Load"]) + int(option_list[3][data_list[3]]["EN Load"]) + int(option_list[4][data_list[4]]["EN Load"])
        selection_list.append(weight)
        selection_list.append(en_load)

        selection_list.append(self.ForceHead.isChecked())
        selection_list.append(self.Head_Select.currentIndex())
        selection_list.append(self.ForceCore.isChecked())
        selection_list.append(self.Core_Select.currentIndex())
        selection_list.append(self.ForceArms.isChecked())
        selection_list.append(self.Arms_Select.currentIndex())
        selection_list.append(self.ForceLegs.isChecked())
        selection_list.append(self.Legs_Select.currentIndex())
        selection_list.append(self.ForceGen.isChecked())
        selection_list.append(self.Gen.currentIndex())
        selection_list.append(self.ForceBoost.isChecked())
        selection_list.append(self.Boost.currentIndex())

        selection_list.append(self.WeightMax.isChecked())
        selection_list.append(self.WeightMax_line.text())
        selection_list.append(self.ENRecMin.isChecked())
        selection_list.append(self.ENRecMin_line.text())
        selection_list.append(self.APMin.isChecked())
        selection_list.append(self.APMin_line.text())
        selection_list.append(self.ASMin.isChecked())
        selection_list.append(self.ASMin_line.text())
        selection_list.append(self.ENCapMin.isChecked())
        selection_list.append(self.ENCapMin_line.text())
        selection_list.append(self.EnergyFASpec.isChecked())
        selection_list.append(self.EnergyFASpecMin_line.text())
        selection_list.append(self.RecoilMin.isChecked())
        selection_list.append(self.RecoilMin_line.text())
        selection_list.append(self.TargetTrackMin.isChecked())
        selection_list.append(self.TargetTrackMin_line.text())
        selection_list.append(self.MeleeSpecMin.isChecked())
        selection_list.append(self.MeleeSpecMin_line.text())
        selection_list.append(self.LoadOverride.isChecked())

        selection_list.append(self.OptiTargetSelect.currentIndex())
        # Adding arm load (of weapons)
        arm_weight = int(option_list[0][data_list[0]]["Weight"]) + int(option_list[1][data_list[1]]["Weight"])
        selection_list.append(arm_weight)
        # Adding leg type selection
        selection_list.append(self.LegTypeSelect.currentText())
        # Adding new opti targets (update Nov 24)
        selection_list.append(self.GenTypeSelect.currentText())
        selection_list.append(self.SysRecMin.isChecked())
        selection_list.append(self.SysRecMin_line.text())
        selection_list.append(self.BoostSpdMin.isChecked())
        selection_list.append(self.BoostSpdMin_line.text())
        selection_list.append(self.ABSpdMin.isChecked())
        selection_list.append(self.ABSpdMin_line.text())
        selection_list.append(self.TravelSpdMin.isChecked())
        selection_list.append(self.TravelSpdMin_line.text())
        selection_list.append(self.HoverSpdMin.isChecked())
        selection_list.append(self.HoverSpdMin_line.text())
        # Adding custom target weights:
        selection_list.append(self.ehp_weight.text())
        selection_list.append(self.as_weight.text())

        return selection_list

    def set_stats(self):
        # First list is the indices of current selections
        current_selected = self.get_current_selection_stats()
        # Second list is the extra lists for weapons, that are partially used.
        option_list = self.list_maker(self.add_data)
        # All the other stuff is saved in the class above, under self.list_data
        # Meaning: All the stuff below takes the full lists of equipment (from list-data or option_list) and selects the
        # relevant item by picking the element equal to the selection (from current_selected), and the data point is
        # called with the dict key of the name of the statistic
        weight = int(option_list[0][current_selected[0]]["Weight"]) + int(
            option_list[1][current_selected[1]]["Weight"]) + int(
            option_list[2][current_selected[2]]["Weight"]) + int(option_list[3][current_selected[3]]["Weight"]) + int(
            option_list[4][current_selected[4]]["Weight"]) + int(
            self.list_data[0][current_selected[5]]["Weight"]) + int(
            self.list_data[1][current_selected[6]]["Weight"]) + int(
            self.list_data[2][current_selected[7]]["Weight"]) + int(
            self.list_data[3][current_selected[8]]["Weight"]) + int(
            self.list_data[4][current_selected[9]]["Weight"]) + int(self.list_data[5][current_selected[10]]["Weight"])
        en_load = int(option_list[0][current_selected[0]]["EN Load"]) + int(option_list[1][current_selected[1]]["EN Load"]) + int(
            option_list[2][current_selected[2]]["EN Load"]) + int(option_list[3][current_selected[3]]["EN Load"]) + int(
            option_list[4][current_selected[4]]["EN Load"]) + int(
            self.list_data[0][current_selected[5]]["EN Load"]) + int(
            self.list_data[1][current_selected[6]]["EN Load"]) + int(
            self.list_data[2][current_selected[7]]["EN Load"]) + int(
            self.list_data[3][current_selected[8]]["EN Load"]) + int(self.list_data[5][current_selected[10]]["EN Load"])
        en_load_max = int(int(self.list_data[1][current_selected[6]]["Generator Output Adj."]) / 100 * int(self.list_data[4][current_selected[9]]["EN Output"]))
        en_capacity = int(self.list_data[4][current_selected[9]]["EN Capacity"])
        en_recharge = int(4.166 * (en_load_max - en_load) + 1500)
        recharge_delay = float(float(self.list_data[4][current_selected[9]]["EN Recharge Delay"]) * (200 - int(self.list_data[1][current_selected[6]]["Generator Supply Adj"])) / 100)
        recharge_delay_red = float(float(self.list_data[4][current_selected[9]]["Supply Recovery Delay"]) * (200 - int(self.list_data[1][current_selected[6]]["Generator Supply Adj"])) / 100)
        ap = int(self.list_data[0][current_selected[5]]["AP"]) + int(
            self.list_data[1][current_selected[6]]["AP"]) + int(
            self.list_data[2][current_selected[7]]["AP"]) + int(
            self.list_data[3][current_selected[8]]["AP"])
        attitude = int(self.list_data[0][current_selected[5]]["Attitude Stability"]) + int(
            self.list_data[1][current_selected[6]]["Attitude Stability"]) + int(
            self.list_data[3][current_selected[8]]["Attitude Stability"])
        kinetic_def = int(self.list_data[0][current_selected[5]]["Anti-Kinetic Defense"]) + int(
            self.list_data[1][current_selected[6]]["Anti-Kinetic Defense"]) + int(
            self.list_data[2][current_selected[7]]["Anti-Kinetic Defense"]) + int(
            self.list_data[3][current_selected[8]]["Anti-Kinetic Defense"])
        kinetic_ehp = ap / ((2000 - kinetic_def) / 1000)
        energy_def = int(self.list_data[0][current_selected[5]]["Anti-Energy Defense"]) + int(
            self.list_data[1][current_selected[6]]["Anti-Energy Defense"]) + int(
            self.list_data[2][current_selected[7]]["Anti-Energy Defense"]) + int(
            self.list_data[3][current_selected[8]]["Anti-Energy Defense"])
        energy_ehp = ap / ((2000 - energy_def)/1000)
        explosive_def = int(self.list_data[0][current_selected[5]]["Anti-Explosive Defense"]) + int(
            self.list_data[1][current_selected[6]]["Anti-Explosive Defense"]) + int(
            self.list_data[2][current_selected[7]]["Anti-Explosive Defense"]) + int(
            self.list_data[3][current_selected[8]]["Anti-Explosive Defense"])
        explosive_ehp = ap / ((2000 - explosive_def)/1000)
        overall_ehp = (ap + kinetic_ehp + energy_ehp + explosive_ehp) / 4
        if option_list[0][current_selected[0]]["Recoil"] == "" or option_list[0][current_selected[0]]["Rapid Fire"] == "":
            recoil_right = "Unclear"
        else:
            recoil_right = str(float(option_list[0][current_selected[0]]["Recoil"]) * float(option_list[0][current_selected[0]]["Rapid Fire"]))
        if option_list[1][current_selected[1]]["Recoil"] == "" or option_list[1][current_selected[1]]["Rapid Fire"] == "":
            recoil_left = "Unclear"
        else:
            recoil_left = str(float(option_list[1][current_selected[1]]["Recoil"]) * float(option_list[1][current_selected[1]]["Rapid Fire"]))
        energy_spec = int(self.list_data[4][current_selected[9]]["Energy Firearm Spec."])
        melee_spec = int(self.list_data[2][current_selected[7]]["Melee Specialization"])
        target_tracking = int(self.list_data[2][current_selected[7]]["Target Tracking"])
        recoil_control = int(self.list_data[2][current_selected[7]]["Recoil Control"])
        sys_recovery = int(self.list_data[0][current_selected[5]]["System Recovery"])
        jump_height = int(self.list_data[3][current_selected[8]]["Jump Height"])
        jump_dist = int(self.list_data[3][current_selected[8]]["Jump Distance"])
        lock_close = (90 - (9 / 10 * float(option_list[4][current_selected[4]]["Close-Range Assist"]))) * (100 / float(self.list_data[2][current_selected[7]]["Target Tracking"]))
        lock_mid = (90 - (9 / 10 * float(option_list[4][current_selected[4]]["Medium-Range Assist"]))) * (
                    100 / float(self.list_data[2][current_selected[7]]["Target Tracking"]))
        lock_far = (90 - (9 / 10 * float(option_list[4][current_selected[4]]["Long-Range Assist"]))) * (
                    100 / float(self.list_data[2][current_selected[7]]["Target Tracking"]))
        qb_cost = (float(self.list_data[5][current_selected[10]]["QB EN Consumption"]) / (float(self.list_data[1][current_selected[6]]["Booster Efficiency Adj."]) / 100))
        ab_cost = (float(self.list_data[5][current_selected[10]]["AB EN Consumption"]) / (float(self.list_data[1][current_selected[6]]["Booster Efficiency Adj."]) / 100))

        # Boost Speed:
        if weight <= 40000:
            weight_multi = 1
        elif weight <= 62500:
            weight_multi = (1 - (weight - 40000) * (30/9) * 10**(-6))
        elif weight <= 75000:
            weight_multi = (0.925 - (weight - 62500) * 0.000006)
        elif weight <= 80000:
            weight_multi = (0.85 - (weight - 75000) * 0.000015)
        elif weight <= 120000:
            weight_multi = (0.775 - (weight - 80000) * 0.000003125)
        else:
            weight_multi = 0.65

        boost_speed = round(int(self.list_data[5][current_selected[10]]["Thrust"]) * 0.06 * weight_multi)

        if weight <= 40000:
            qb_weight_multi = 1
        elif weight <= 62500:
            qb_weight_multi = (1 - (weight - 40000) * (40/9) * 10**(-6))
        elif weight <= 75000:
            qb_weight_multi = (0.9 - (weight - 62500) * 0.000004)
        elif weight <= 80000:
            qb_weight_multi = (0.85 - (weight - 75000) * 0.00001)
        elif weight <= 120000:
            qb_weight_multi = (0.8 - (weight - 80000) * 0.0000025)
        else:
            qb_weight_multi = 0.7

        ascent_speed = round(int(self.list_data[5][current_selected[10]]["Upward Thrust"]) * 0.06 * qb_weight_multi)
        qb_speed = round(int(self.list_data[5][current_selected[10]]["QB Thrust"]) * 0.06 * qb_weight_multi)

        if weight <= 40000:
            melee_lunge_speed = round(int(self.list_data[5][current_selected[10]]["Melee Attack Thrust"]) * 0.06)
        elif weight <= 62500:
            melee_lunge_speed = round(int(self.list_data[5][current_selected[10]]["Melee Attack Thrust"]) * 0.06 * (1 - (weight - 40000) * (20/9) * 10**(-6)))
        elif weight <= 75000:
            melee_lunge_speed = round(int(self.list_data[5][current_selected[10]]["Melee Attack Thrust"]) * 0.06 * (0.925 - (weight - 62500) * 0.000008))
        elif weight <= 80000:
            melee_lunge_speed = round(int(self.list_data[5][current_selected[10]]["Melee Attack Thrust"]) * 0.06 * (0.85 - (weight - 75000) * 0.00002))
        elif weight <= 120000:
            melee_lunge_speed = round(int(self.list_data[5][current_selected[10]]["Melee Attack Thrust"]) * 0.06 * (0.775 - (weight - 80000) * 0.0000025))
        else:
            melee_lunge_speed = round(int(self.list_data[5][current_selected[10]]["Melee Attack Thrust"]) * 0.06 * 0.65)

        if weight <= 40000:
            ab_speed = round(int(self.list_data[5][current_selected[10]]["AB Thrust"]) * 0.06)
        elif weight <= 50000:
            ab_speed = round(int(self.list_data[5][current_selected[10]]["AB Thrust"]) * 0.06 * (1 - (weight - 40000) * 0.000005))
        elif weight <= 75000:
            ab_speed = round(int(self.list_data[5][current_selected[10]]["AB Thrust"]) * 0.06 * (0.95 - (weight - 50000) * 0.000002))
        elif weight <= 100000:
            ab_speed = round(int(self.list_data[5][current_selected[10]]["AB Thrust"]) * 0.06 * (0.9 - (weight - 75000) * 0.000008))
        else:
            ab_speed = round(int(self.list_data[5][current_selected[10]]["AB Thrust"]) * 0.06 * (0.7 - (weight - 100000) * 0.000003))

        if weight <= 70000:
            hover_speed = round(int(self.list_data[3][current_selected[8]]["Tetrapod Hover Speed"]))
        elif weight <= 90000:
            hover_speed = round(int(self.list_data[3][current_selected[8]]["Tetrapod Hover Speed"]) * (1 - (weight - 70000) * 0.000005))
        elif weight <= 100000:
            hover_speed = round(int(self.list_data[3][current_selected[8]]["Tetrapod Hover Speed"]) * (0.9 - (weight - 90000) * 0.000005))
        elif weight <= 110000:
            hover_speed = round(int(self.list_data[3][current_selected[8]]["Tetrapod Hover Speed"]) * (0.85 - (weight - 100000) * 0.00001))
        elif weight <= 120000:
            hover_speed = round(int(self.list_data[3][current_selected[8]]["Tetrapod Hover Speed"]) * (0.75 - (weight - 110000) * 0.000005))
        else:
            hover_speed = round(int(self.list_data[3][current_selected[8]]["Tetrapod Hover Speed"]) * 0.7)

        if weight <= 50000:
            tank_travel_multi = 1
        elif weight <= 75000:
            tank_travel_multi = 1 - (weight - 50000) * 0.000004
        elif weight <= 100000:
            tank_travel_multi = 0.9 - (weight - 75000) * 0.000002
        elif weight <= 110000:
            tank_travel_multi = 0.85 - (weight - 100000) * 0.0000025
        elif weight <= 120000:
            tank_travel_multi = 0.8 - (weight - 110000) * 0.000005
        else:
            tank_travel_multi = 0.7

        tank_speed = round(int(self.list_data[5][current_selected[10]]["High-Speed Perf."]) * tank_travel_multi)

        if weight <= 50000:
            fortaleza_travel_multi = 1
        elif weight <= 62500:
            fortaleza_travel_multi = 1 - (weight - 50000) * 0.0000048
        elif weight <= 75000:
            fortaleza_travel_multi = 0.94 - (weight - 62500) * 0.0000064
        elif weight <= 100000:
            fortaleza_travel_multi = 0.86 - (weight - 75000) * 0.0000044
        elif weight <= 150000:
            fortaleza_travel_multi = 0.75 - (weight - 100000) * 0.000003
        else:
            fortaleza_travel_multi = 0.6

        fortaleza_tank_speed = round(int(self.list_data[5][current_selected[10]]["High-Speed Perf."]) * fortaleza_travel_multi)

        self.out_AP.setText(str(ap))
        self.out_Attitude.setText(str(attitude))
        self.out_Weight.setText(str(weight))
        self.out_EN.setText(str(en_load) + " / " + str(en_load_max))
        self.out_EN_Cap.setText(str(en_capacity))
        self.out_ENRecharge.setText(str(en_recharge))
        self.out_RechargeDelay.setText(str(round(recharge_delay, 2)) + " seconds")
        self.out_RechargeDelayRed.setText(str(round(recharge_delay_red, 2)) + " seconds")
        self.out_Kinetic.setText(str(round(kinetic_ehp)))
        self.out_Energy.setText(str(round(energy_ehp)))
        self.out_Explosive.setText(str(round(explosive_ehp)))
        self.out_OverallEHP.setText(str(round(overall_ehp)))
        self.out_RecoilRight.setText(recoil_right)
        self.out_RecoilLeft.setText(recoil_left)
        self.out_EnergySpec.setText(str(energy_spec))
        self.out_MeleeSpec.setText(str(melee_spec))
        self.out_RecoilCont.setText(str(recoil_control))
        self.out_TargetTracking.setText(str(target_tracking))
        self.out_SysRec.setText(str(sys_recovery))
        self.out_JumpHeight.setText(str(jump_height))
        self.out_JumpDist.setText(str(jump_dist))
        self.out_LockClose.setText(str(round(lock_close / 60, 3)) + " seconds")
        self.out_LockMid.setText(str(round(lock_mid / 60, 3)) + " seconds")
        self.out_LockFar.setText(str(round(lock_far / 60, 3)) + " seconds")
        self.out_BoostSpd.setText(str(boost_speed))
        self.out_AscentSpd.setText(str(ascent_speed))
        self.out_MeleeSpd.setText(str(melee_lunge_speed))
        self.out_QBCost.setText(str(round(qb_cost)) + " / " + str(round(en_capacity / qb_cost, 2)) + " boosts")
        self.out_ABSpd.setText(str(ab_speed))
        self.out_ABCost.setText(str(round(ab_cost)) + " / " + str(round(en_capacity / ab_cost, 2)) + " seconds")
        self.out_TetraSpd.setText(str(hover_speed))
        self.out_TankSpd.setText(str(tank_speed))
        if current_selected[10] == 14:
            self.out_TankSpd.setText(str(fortaleza_tank_speed))

        return


    def run_optimiser(self):
        self.opti_list = ac6_opti(self.opti_data, self.get_current_selection_opti())
        if self.opti_list == "Error":
            threading.Thread(
                target=lambda: winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
            ).start()
        else:
            # Head
            self.out_Head.setText(self.list_data[0][self.opti_list[0]]["Part name"])
            self.Head_Select.setCurrentIndex(self.opti_list[0])
            # Core
            self.opti_list[1] = self.opti_list[1] - len(self.list_data[0])
            self.out_Core.setText(self.list_data[1][self.opti_list[1]]["Part name"])
            self.Core_Select.setCurrentIndex(self.opti_list[1])
            # Arms
            self.opti_list[2] = self.opti_list[2] - len(self.list_data[0]) - len(self.list_data[1])
            self.out_Arms.setText(str(self.list_data[2][self.opti_list[2]]["Part name"]))
            self.Arms_Select.setCurrentIndex(self.opti_list[2])
            # Legs
            self.opti_list[3] = self.opti_list[3] - len(self.list_data[0]) - len(self.list_data[1]) - len(self.list_data[2])
            self.out_Legs.setText(str(self.list_data[3][self.opti_list[3]]["Part name"]))
            self.Legs_Select.setCurrentIndex(self.opti_list[3])
            # Gen
            self.opti_list[4] = self.opti_list[4] - len(self.list_data[0]) - len(self.list_data[1]) - len(
                self.list_data[2]) - len(self.list_data[3])
            self.out_Gen.setText(str(self.list_data[4][self.opti_list[4]]["Part name"]))
            self.Gen.setCurrentIndex(self.opti_list[4])
            # Boosters
            self.opti_list[5] = self.opti_list[5] - len(self.list_data[0]) - len(self.list_data[1]) - len(
                self.list_data[2]) - len(self.list_data[3]) - len(self.list_data[4])
            self.out_Boost.setText(str(self.list_data[5][self.opti_list[5]]["Part name"]))
            self.Boost.setCurrentIndex(self.opti_list[5])

            self.set_stats()

            return self.opti_list

    def show_custom_fields(self):
        target = self.OptiTargetSelect.currentIndex()
        if target == 8:
            self.ehp_weight.show()
            self.as_weight.show()
            self.as_weight_label.show()
            self.ehp_weight_label.show()

    def connectSignalSlots(self):
        self.actionExit.triggered.connect(self.close)
        self.actionOpti.triggered.connect(self.run_optimiser)
        self.RightArm.currentIndexChanged.connect(self.set_stats)
        self.LeftArm.currentIndexChanged.connect(self.set_stats)
        self.RightBack.currentIndexChanged.connect(self.set_stats)
        self.LeftBack.currentIndexChanged.connect(self.set_stats)
        self.FCS.currentIndexChanged.connect(self.set_stats)
        self.Head_Select.currentIndexChanged.connect(self.set_stats)
        self.Core_Select.currentIndexChanged.connect(self.set_stats)
        self.Arms_Select.currentIndexChanged.connect(self.set_stats)
        self.Legs_Select.currentIndexChanged.connect(self.set_stats)
        self.Gen.currentIndexChanged.connect(self.set_stats)
        self.Boost.currentIndexChanged.connect(self.set_stats)
        self.actionAreaSearch.triggered.connect(self.area_search_activate)
        self.actionCustomTarget.triggered.connect(self.show_custom_fields)

    def populate_lists(self, data, add_data):
        head_list = []
        for i in range(0, len(data[0])):
            head_list.append(data[0][i]["Part name"])
        self.Head_Select.addItems(head_list)

        core_list = []
        for i in range(0, len(data[1])):
            core_list.append(data[1][i]["Part name"])
        self.Core_Select.addItems(core_list)

        arms_list = []
        for i in range(0, len(data[2])):
            arms_list.append(data[2][i]["Part name"])
        self.Arms_Select.addItems(arms_list)

        legs_list = []
        for i in range(0, len(data[3])):
            legs_list.append(data[3][i]["Part name"])
        self.Legs_Select.addItems(legs_list)

        gen_list = []
        for i in range(0, len(data[4])):
            gen_list.append(data[4][i]["Part name"])
        self.Gen.addItems(gen_list)

        boost_list = []
        for i in range(0, len(data[5])):
            boost_list.append(data[5][i]["Part name"])
        self.Boost.addItems(boost_list)

        weapon_list_l = []
        for i in range(0, len(add_data[0])):
            weapon_list_l.append(add_data[0][i]["Part name"])
        self.LeftArm.addItems(weapon_list_l)

        weapon_list_r = []
        for i in range(0, len(add_data[0])):
            if add_data[0][i]["Weapon Type"] != "Melee":
                weapon_list_r.append(add_data[0][i]["Part name"])
        self.RightArm.addItems(weapon_list_r)

        back_list_l = []
        for i in range(0, len(add_data[1])):
            back_list_l.append(add_data[1][i]["Part name"])
        back_list_l = back_list_l + weapon_list_l
        self.LeftBack.addItems(back_list_l)

        back_list_r = []
        for i in range(0, len(add_data[1])):
            if add_data[1][i]["Weapon Type"] != "Shield":
                back_list_r.append(add_data[1][i]["Part name"])
        back_list_r = back_list_r + weapon_list_r
        self.RightBack.addItems(back_list_r)

        fcs_list = []
        for i in range(0, len(add_data[2])):
            fcs_list.append(add_data[2][i]["Part name"])
        self.FCS.addItems(fcs_list)

        self.CoreExp.addItems(["Pulse Armour", "Pulse Protection", "Assault Armour", "Terminal Armour"])

        self.OptiTargetSelect.addItems(["Maximise average EHP", "Maximise kinetic EHP", "Maximise energy EHP", "Maximise explosive EHP", "Maximise AP", "Maximise AS", "Minimise Weight", "Maximise Weight", "Custom EHP/AS mix"])
        self.LegTypeSelect.addItems(["Any", "Biped", "Reverse Joint", "Quad", "Tank"])
        self.GenTypeSelect.addItems(["Any", "Normal", "Coral"])

    def area_search_activate(self):
        if self.w is None:
            self.w = AreaSearchWindow()
        self.w.show()
        self.w.activateWindow()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    win.set_stats()
    sys.exit(app.exec())
