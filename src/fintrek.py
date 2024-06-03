import sys
import os

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import (
    QLabel, QVBoxLayout, QDialog, QGroupBox, QGridLayout, QMenuBar, QTabWidget)
from PyQt5.QtCore import Qt

import com_ui
import fintrek_config as config


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.app_name = com_ui.UIProperties.get_app_name()
        self.app_description = com_ui.UIProperties.get_app_description()
        self.version = com_ui.UIProperties.get_version()
        self.developer = com_ui.UIProperties.get_developer_name()
        self.setWindowTitle(f"{self.app_name} || Version {self.version}")
        self.setWindowIcon(com_ui.UIProperties.get_app_icon())
        self.setFixedSize(
            com_ui.UIProperties.get_app_width(),
            com_ui.UIProperties.get_app_height())

        with open(config.APP_STYLE, "r", encoding="UTF-8") as stylesheet:
            self.setStyleSheet(stylesheet.read())
        self.tab_manager = TabManager()
        self.setMenuBar(self.menu_bar())
        self.setCentralWidget(self.tab_manager)

    def menu_bar(self) -> QMenuBar:
        menubar = QMenuBar(self)

        file_menu = menubar.addMenu("File")

        db_action = file_menu.addAction("Database...")
        db_action.triggered.connect(
            DBInfoDialog(self).exec_)

        exit_action = file_menu.addAction("Exit")
        exit_action.triggered.connect(self.exit_app)

        help_menu = menubar.addMenu("Help")

        about_action = help_menu.addAction("About")
        about_action.triggered.connect(self.about_info)

        return menubar

    def about_info(self):
        msg_box = com_ui.CommonUI.message_box(
            self,
            title = "About Fintrek",
            text = self.app_description,
            info_text = f"""Version: v{self.version}
            \nDeveloped by: {self.developer}""")
        msg_box.exec_()

    def exit_app(self):
        self.close()

class DBInfoDialog(QDialog):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setWindowTitle("Database Information")
        self.setFixedSize(300, 200)

        self.db_name = str()
        self.db_user = str()
        self.db_pass = str()
        self.db_host = str()
        self.db_port = str()

        self.get_db_info()
        self.initiate_ui()

    def initiate_ui(self):
        main_layout = QVBoxLayout()

        db_info_group = self.db_info_group()
        db_info_submit = com_ui.CommonUI.push_button(
            self,
            "Submit",
            self.submit_db_info)
        main_layout.addWidget(db_info_group)
        main_layout.addWidget(db_info_submit)

        self.setLayout(main_layout)

    def db_info_group(self) -> QGroupBox:
        db_info_group = QGroupBox()
        layout = QGridLayout()

        self.db_name_label = QLabel("Database Name:")
        layout.addWidget(self.db_name_label, 0, 0)

        self.db_name_input = com_ui.CommonUI.line_edit(
            self,
            "",
            "Database Name",
            self.set_db_name)
        layout.addWidget(self.db_name_input, 0, 1)

        self.db_user_label = QLabel("Database User:")
        layout.addWidget(self.db_user_label, 1, 0)

        self.db_user_input = com_ui.CommonUI.line_edit(
            self,
            "",
            "Database User",
            self.set_db_user)
        layout.addWidget(self.db_user_input, 1, 1)

        self.db_pass_label = QLabel("Database Password:")
        layout.addWidget(self.db_pass_label, 2, 0)

        self.db_pass_input = com_ui.CommonUI.line_edit(
            self,
            "",
            "Database Password",
            self.set_db_pass)
        layout.addWidget(self.db_pass_input, 2, 1)

        self.db_host_label = QLabel("Database Host:")
        layout.addWidget(self.db_host_label, 3, 0)

        self.db_host_input = com_ui.CommonUI.line_edit(
            self,
            "",
            "Database Host",
            self.set_db_host)
        layout.addWidget(self.db_host_input, 3, 1)

        self.db_port_label = QLabel("Database Port:")
        layout.addWidget(self.db_port_label, 4, 0)

        self.db_port_input = com_ui.CommonUI.line_edit(
            self,
            "",
            "Database Port",
            self.set_db_port)
        layout.addWidget(self.db_port_input, 4, 1)

        db_info_group.setLayout(layout)
        return db_info_group

    def set_db_name(self, db_name):
        self.db_name = db_name

    def set_db_user(self, db_user):
        self.db_user = db_user

    def set_db_pass(self, db_pass):
        self.db_pass = db_pass

    def set_db_host(self, db_host):
        self.db_host = db_host

    def set_db_port(self, db_port):
        self.db_port = db_port

    def get_db_info(self):
        if not os.path.exists(f"{config.APP_LOCAL_PATH}/.env"):
            print("Environment file not found. Please create an environment file.")

        with open(f"{config.APP_LOCAL_PATH}/.env", "r") as env_file:
            env_contents = env_file.readlines()

            for line in env_contents:
                if "DB_NAME" in line:
                    self.db_name = line.split("=")[1].strip()
                elif "DB_USER" in line:
                    self.db_user = line.split("=")[1].strip()
                elif "DB_PASS" in line:
                    self.db_pass = line.split("=")[1].strip()
                elif "DB_HOST" in line:
                    self.db_host = line.split("=")[1].strip()
                elif "DB_PORT" in line:
                    self.db_port = line.split("=")[1].strip()

    def submit_db_info(self):
        env_setup_list = [
            f"DB_NAME={self.db_name}\n",
            f"DB_USER={self.db_user}\n",
            f"DB_PASS={self.db_pass}\n",
            f"DB_HOST={self.db_host}\n",
            f"DB_PORT={self.db_port}\n"
        ]

        with open(f"{config.APP_LOCAL_PATH}/.env", "w") as env_file:
            env_file.writelines(env_setup_list)


class TabManager(QTabWidget):
    def __init__(self) -> None:
        super().__init__()
        self.fin_overview_tab = FintrekOverviewUI()
        self.fin_table_tab = FintrekTableUI()
        self.addTab(self.fin_overview_tab, "Finances Overview")
        self.addTab(self.fin_table_tab, "Finances Table")

class FintrekOverviewUI(QDialog):
    def __init__(self) -> None:
        super().__init__()
        self.fintrek_instance = Fintrek(self)
        self.budget = "0.00"
        self.currency_type = "£"
        main_layout = self.setup_ui()
        self.setLayout(main_layout)

    def setup_ui(self):
        main_layout = QVBoxLayout()

        fin_overview_group = self.fin_overview_group()
        fin_insert_group = self.fin_insert_group()

        main_layout.addWidget(fin_overview_group)
        main_layout.addWidget(fin_insert_group)
        return main_layout

    def fin_overview_group(self) -> QGroupBox:
        fin_overview_group = QGroupBox()
        layout = QGridLayout()
        layout.setAlignment(Qt.AlignTop)

        self.budget_label = QLabel(
            f"Budget: {self.currency_type}{self.budget}")
        self.budget_label.setObjectName("budget_label")

        self.remainder_label = QLabel(
            f"Remainder: {self.currency_type}{self.fintrek_instance.get_remainder()}")
        self.remainder_label.setObjectName("remainder_label")

        layout.addWidget(self.budget_label, 0, 0)
        layout.addWidget(self.remainder_label, 1, 0)

        fin_overview_group.setLayout(layout)
        return fin_overview_group

    def fin_insert_group(self) -> QGroupBox:
        fin_insert_group = QGroupBox()
        fin_insert_group.setFlat(True)
        fin_insert_group.setStyleSheet("QGroupBox{border:0;}")
        layout = QGridLayout()

        self.transact_type_button = com_ui.CommonUI.dropdown_button(
            self,
            ["Expense", "Income"],
            self.fintrek_instance.set_transaction_type)
        layout.addWidget(self.transact_type_button, 0, 0, 1, 1)

        self.transact_amount_input = com_ui.CommonUI.line_edit(
            self,
            "",
            "Amount: eg. 100.00",
            self.fintrek_instance.set_transaction_amount)
        layout.addWidget(self.transact_amount_input, 1, 0)

        self.reason_input = com_ui.CommonUI.line_edit(
            self,
            "",
            "Reason: eg. Groceries",
            self.fintrek_instance.set_reason)
        layout.addWidget(self.reason_input, 1, 1)

        self.submit_button = com_ui.CommonUI.push_button(
            self, "Submit", self.fintrek_instance.submit_transaction)
        layout.addWidget(self.submit_button, 1, 2)

        fin_insert_group.setLayout(layout)
        return fin_insert_group

class FintrekTableUI(QDialog):
    def __init__(self) -> None:
        super().__init__()
        self.fintrek_instance = Fintrek(self)
        main_layout = self.setup_ui()
        self.setLayout(main_layout)

    def setup_ui(self):
        main_layout = QVBoxLayout()
        return main_layout

class Fintrek:
    def __init__(self, fintrek_ui) -> None:
        self.fintrek_ui = fintrek_ui
        self.transact_type = str()
        self.transact_amount = float()
        self.reason = str()

    def get_remainder(self) -> str:
        return "0.00"

    def set_transaction_type(self, transact_type) -> None:
        self.transact_type = transact_type

    def set_transaction_amount(self, amount) -> None:
        self.transact_amount = amount

    def set_reason(self, reason) -> None:
        self.reason = reason

    def submit_transaction(self):
        pass


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
