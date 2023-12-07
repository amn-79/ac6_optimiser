import sys
from data_import import data_importer
from data_import import data_importer_noopt
from optimiser_cpsat import ac6_opti
import winsound

from PyQt6.QtWidgets import (QApplication, QMainWindow)

from main_window_ui import Ui_MainWindow


class Window(QMainWindow, Ui_MainWindow):
    add_data = data_importer_noopt()
    imported_data = data_importer()
    opti_data = imported_data[0]
    list_data = imported_data[1]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Armored Core VI - Optimizer")
        self.populate_lists(self.list_data, self.add_data)
        self.connectSignalSlots()

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
        selection_list.append(self.ENMin.isChecked())
        selection_list.append(self.ENMin_line.text())
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
        selection_list.append(self.FASpecMin.isChecked())
        selection_list.append(self.FASpecMin_line.text())
        selection_list.append(self.MeleeSpecMin.isChecked())
        selection_list.append(self.MeleeSpecMin_line.text())
        selection_list.append(self.LoadOverride.isChecked())

        selection_list.append(self.OptiTargetSelect.currentIndex())
        # Adding arm load (of weapons)
        arm_weight = int(option_list[0][data_list[0]]["Weight"]) + int(option_list[1][data_list[1]]["Weight"])
        selection_list.append(arm_weight)
        # Adding leg type selection
        selection_list.append(self.LegTypeSelect.currentText())

        return selection_list

    def set_stats(self):
        # First list is the indices of current selections
        current_selected = self.get_current_selection_stats()
        # Second list is the extra lists for weapons, that are partially used.
        option_list = self.list_maker(self.add_data)
        # All the other stuff is saved in the class above, under self.list_data
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
        firearm_spec = int(self.list_data[2][current_selected[7]]["Firearm Specialization"])

        self.out_AP.setText(str(ap))
        self.out_Attitude.setText(str(attitude))
        self.out_Weight.setText(str(weight))
        self.out_EN.setText(str(en_load) + " / " + str(en_load_max))
        self.out_EN_Cap.setText(str(en_capacity))
        self.out_Kinetic.setText(str(kinetic_ehp))
        self.out_Energy.setText(str(energy_ehp))
        self.out_Explosive.setText(str(explosive_ehp))
        self.out_RecoilRight.setText(recoil_right)
        self.out_RecoilLeft.setText(recoil_left)
        self.out_EnergySpec.setText(str(energy_spec))
        self.out_MeleeSpec.setText(str(melee_spec))
        self.out_FASpec.setText(str(firearm_spec))

        return


    def run_optimiser(self):
        self.opti_list = ac6_opti(self.opti_data, self.get_current_selection_opti())
        if self.opti_list == "Error":
            winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
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

        self.OptiTargetSelect.addItems(["Maximise average EHP", "Maximise kinetic EHP", "Maximise energy EHP", "Maximise explosive EHP", "Maximise AP", "Maximise AS", "Minimise Weight", "Maximise Weight"])
        self.LegTypeSelect.addItems(["Any", "Biped", "Reverse Joint", "Quad", "Tank"])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    win.set_stats()
    sys.exit(app.exec())
