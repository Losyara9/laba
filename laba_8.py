import psycopg2
import sys
from PyQt5.QtWidgets import (QApplication, QWidget,
                             QTabWidget, QAbstractScrollArea,
                             QVBoxLayout, QHBoxLayout,
                             QTableWidget, QGroupBox,
                             QTableWidgetItem, QPushButton, QMessageBox)


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self._connect_to_db()

        self.setWindowTitle("Shedule")
        self.setWindowTitle("Subjects")
        self.setWindowTitle("Teachers")

        self.vbox = QVBoxLayout(self)

        self.tabs = QTabWidget(self)
        self.vbox.addWidget(self.tabs)

        self._create_shedule_tab()
        self._create_teacher_tab()
        self._create_subject_tab()

    def _connect_to_db(self):
        self.conn = psycopg2.connect(database="exxel",
                                     user="postgres",
                                     password="123",
                                     host="localhost",
                                     port="5432")

        self.cursor = self.conn.cursor()

    def _create_teacher_tab(self):
        self.teacher_tab = QWidget()
        self.tabs.addTab(self.teacher_tab, "Teachers")

        self.teacher_gbox = QGroupBox("Teachers")

        self.svbox = QVBoxLayout()
        self.shbox1 = QHBoxLayout()
        self.shbox2 = QHBoxLayout()

        self.svbox.addLayout(self.shbox1)
        self.svbox.addLayout(self.shbox2)

        self.shbox1.addWidget(self.teacher_gbox)

        self._get_teacher()
        self.update_shedule_button = QPushButton("Update")
        self.shbox2.addWidget(self.update_shedule_button)
        self.update_shedule_button.clicked.connect(self._update_teacher)

        self.teacher_tab.setLayout(self.svbox)

        self.teacher_tab.setLayout(self.svbox)

    def _get_teacher(self):
        self.teacher_table = QTableWidget()
        self.teacher_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.teacher_table.setColumnCount(4)
        self.teacher_table.setHorizontalHeaderLabels(["ID", "NAME", "", ""])

        self._update_teacher()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.teacher_table)
        self.teacher_gbox.setLayout(self.mvbox)

    def _update_teacher(self):
        self.cursor.execute("SELECT * FROM teacher ORDER BY id")
        teachers = list(self.cursor.fetchall())

        self.teacher_table.setRowCount(len(teachers) + 1)

        for i, r in enumerate(teachers):
            r = list(r)
            joinButton = QPushButton("Join")
            delButton = QPushButton("Delete")

            self.teacher_table.setItem(i, 0,
                                      QTableWidgetItem(str(r[0])))

            self.teacher_table.setItem(i, 1,
                                      QTableWidgetItem(str(r[1])))

            self.teacher_table.setCellWidget(i, 2, joinButton)

            self.teacher_table.setCellWidget(i, 3, delButton)

            joinButton.clicked.connect(lambda ch, num=i: self._change_teacher(num))
            delButton.clicked.connect(lambda ch, num=i: self._del_teacher(num))

        self.teacher_table.resizeRowsToContents()

    def _create_subject_tab(self):
        self.subject_tab = QWidget()
        self.tabs.addTab(self.subject_tab, "Subjects")

        self.subject_gbox = QGroupBox("Subjects")

        self.svbox = QVBoxLayout()
        self.shbox1 = QHBoxLayout()
        self.shbox2 = QHBoxLayout()

        self.svbox.addLayout(self.shbox1)
        self.svbox.addLayout(self.shbox2)

        self.shbox1.addWidget(self.subject_gbox)

        self._get_subject()
        self.update_shedule_button = QPushButton("Update")
        self.shbox2.addWidget(self.update_shedule_button)
        self.update_shedule_button.clicked.connect(self._update_subject_table)

        self.subject_tab.setLayout(self.svbox)

        self.subject_tab.setLayout(self.svbox)

    def _get_subject(self):
        self.subject_table = QTableWidget()
        self.subject_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.subject_table.setColumnCount(4)
        self.subject_table.setHorizontalHeaderLabels(["ID", "NAME", "", ""])

        self._update_subject_table()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.subject_table)
        self.subject_gbox.setLayout(self.mvbox)

    def _update_subject_table(self):
        self.cursor.execute("SELECT * FROM subject ORDER BY id")
        subjects = list(self.cursor.fetchall())

        self.subject_table.setRowCount(len(subjects) + 1)

        for i, r in enumerate(subjects):
            r = list(r)
            joinButton = QPushButton("Join")
            delButton = QPushButton("Delete")

            self.subject_table.setItem(i, 0,
                                        QTableWidgetItem(str(r[0])))

            self.subject_table.setItem(i, 1,
                                        QTableWidgetItem(str(r[1])))

            self.subject_table.setCellWidget(i, 2, joinButton)

            self.subject_table.setCellWidget(i, 3, delButton)

            joinButton.clicked.connect(lambda ch, num=i: self.change_subject(num))
            delButton.clicked.connect(lambda ch, num=i: self._del_subject(num))

        self.subject_table.resizeRowsToContents()


    def _create_shedule_tab(self):
        self.shedule_tab = QTabWidget()
        self.tabs.addTab(self.shedule_tab, "Timetable")

        self.monday_gbox = QGroupBox("Monday")
        self.tuesday_gbox = QGroupBox("Tuesday")
        self.wednesday_gbox = QGroupBox("Wednesday")
        self.thursday_gbox = QGroupBox("Thursday")
        self.friday_gbox = QGroupBox("Friday")

        self.svbox = QVBoxLayout()
        self.shbox1 = QHBoxLayout()
        self.shbox2 = QHBoxLayout()

        self.svbox.addLayout(self.shbox1)
        self.svbox.addLayout(self.shbox2)

        self.shbox1.addWidget(self.monday_gbox)
        self.shbox1.addWidget(self.tuesday_gbox)
        self.shbox1.addWidget(self.wednesday_gbox)
        self.shbox1.addWidget(self.thursday_gbox)
        self.shbox1.addWidget(self.friday_gbox)

        self._create_monday_table()
        self._create_tuesday_table()
        self._create_wednesday_table()
        self._create_thursday_table()
        self._create_friday_table()

        self.update_shedule_button = QPushButton("Update")
        self.shbox2.addWidget(self.update_shedule_button)
        self.update_shedule_button.clicked.connect(self._update_shedule)

        self.shedule_tab.setLayout(self.svbox)

    def _create_monday_table(self):
        self.monday_table = QTableWidget()
        self.monday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.monday_table.setColumnCount(7)
        self.monday_table.setHorizontalHeaderLabels(["Subject", "Time", "Class", "Teacher", 'Week number', ' ', ' '])

        self._update_monday_table()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.monday_table)
        self.monday_gbox.setLayout(self.mvbox)

    def _update_monday_table(self):
        self.cursor.execute("SELECT * FROM select_day('Понедельник')")
        records = list(self.cursor.fetchall())

        self.monday_table.setRowCount(len(records) + 1)

        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Join")
            delButton = QPushButton("Delete")

            self.monday_table.setItem(i, 0,
                                      QTableWidgetItem(str(r[0])))
            self.monday_table.setItem(i, 1,
                                      QTableWidgetItem(str(r[1])))
            self.monday_table.setItem(i, 2,
                                      QTableWidgetItem(str(r[2])))
            self.monday_table.setItem(i, 3,
                                      QTableWidgetItem(str(r[3])))
            self.monday_table.setItem(i, 4,
                                      QTableWidgetItem(str(r[4])))

            self.monday_table.setCellWidget(i, 5, joinButton)

            self.monday_table.setCellWidget(i, 6, delButton)

            joinButton.clicked.connect(lambda ch, num=i: self._change_day_from_table(num, records))
            delButton.clicked.connect(lambda ch, num=i: self._del_lesson(num, records))

        self.monday_table.resizeRowsToContents()

    def _create_tuesday_table(self):
        self.tuesday_table = QTableWidget()
        self.tuesday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.tuesday_table.setColumnCount(7)
        self.tuesday_table.setHorizontalHeaderLabels(["Subject", "Time", "Class", "Teacher", 'Week number', ' ', ' '])

        self._update_tuesday_table()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.tuesday_table)
        self.tuesday_gbox.setLayout(self.mvbox)

    def _update_tuesday_table(self):
        self.cursor.execute("SELECT * FROM select_day('Вторник')")
        records = list(self.cursor.fetchall())

        self.tuesday_table.setRowCount(len(records) + 1)

        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Join")
            delButton = QPushButton("Delete")

            self.tuesday_table.setItem(i, 0,
                                      QTableWidgetItem(str(r[0])))
            self.tuesday_table.setItem(i, 1,
                                      QTableWidgetItem(str(r[1])))
            self.tuesday_table.setItem(i, 2,
                                      QTableWidgetItem(str(r[2])))
            self.tuesday_table.setItem(i, 3,
                                      QTableWidgetItem(str(r[3])))
            self.tuesday_table.setItem(i, 4,
                                      QTableWidgetItem(str(r[4])))

            self.tuesday_table.setCellWidget(i, 5, joinButton)

            self.tuesday_table.setCellWidget(i, 6, delButton)

            joinButton.clicked.connect(lambda ch, num=i: self._change_day_from_table_1(num, records))
            delButton.clicked.connect(lambda ch, num=i: self._del_lesson_1(num, records))

        self.tuesday_table.resizeRowsToContents()

    def _create_wednesday_table(self):
        self.wednesday_table = QTableWidget()
        self.wednesday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.wednesday_table.setColumnCount(7)
        self.wednesday_table.setHorizontalHeaderLabels(["Subject", "Time", "Class", "Teacher", 'Week number', ' ', ' '])

        self._update_wednesday_table()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.wednesday_table)
        self.wednesday_gbox.setLayout(self.mvbox)

    def _update_wednesday_table(self):
        self.cursor.execute("SELECT * FROM select_day('Среда')")
        records = list(self.cursor.fetchall())

        self.wednesday_table.setRowCount(len(records) + 1)

        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Join")
            delButton = QPushButton("Delete")

            self.wednesday_table.setItem(i, 0,
                                      QTableWidgetItem(str(r[0])))
            self.wednesday_table.setItem(i, 1,
                                      QTableWidgetItem(str(r[1])))
            self.wednesday_table.setItem(i, 2,
                                      QTableWidgetItem(str(r[2])))
            self.wednesday_table.setItem(i, 3,
                                      QTableWidgetItem(str(r[3])))
            self.wednesday_table.setItem(i, 4,
                                      QTableWidgetItem(str(r[4])))

            self.wednesday_table.setCellWidget(i, 5, joinButton)

            self.wednesday_table.setCellWidget(i, 6, delButton)

            joinButton.clicked.connect(lambda ch, num=i: self._change_day_from_table_2(num, records))
            delButton.clicked.connect(lambda ch, num=i: self._del_lesson_2(num, records))

        self.wednesday_table.resizeRowsToContents()

    def _create_thursday_table(self):
        self.thursday_table = QTableWidget()
        self.thursday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.thursday_table.setColumnCount(7)
        self.thursday_table.setHorizontalHeaderLabels(["Subject", "Time", "Class", "Teacher", 'Week number', ' ', ' '])

        self._update_thursday_table()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.thursday_table)
        self.thursday_gbox.setLayout(self.mvbox)

    def _update_thursday_table(self):
        self.cursor.execute("SELECT * FROM select_day('Четверг')")
        records = list(self.cursor.fetchall())

        self.thursday_table.setRowCount(len(records) + 1)

        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Join")
            delButton = QPushButton("Delete")

            self.thursday_table.setItem(i, 0,
                                      QTableWidgetItem(str(r[0])))
            self.thursday_table.setItem(i, 1,
                                      QTableWidgetItem(str(r[1])))
            self.thursday_table.setItem(i, 2,
                                      QTableWidgetItem(str(r[2])))
            self.thursday_table.setItem(i, 3,
                                      QTableWidgetItem(str(r[3])))
            self.thursday_table.setItem(i, 4,
                                      QTableWidgetItem(str(r[4])))

            self.thursday_table.setCellWidget(i, 5, joinButton)

            self.thursday_table.setCellWidget(i, 6, delButton)

            joinButton.clicked.connect(lambda ch, num=i: self._change_day_from_table_3(num, records))
            delButton.clicked.connect(lambda ch, num=i: self._del_lesson_3(num, records))

        self.thursday_table.resizeRowsToContents()

    def _create_friday_table(self):
        self.friday_table = QTableWidget()
        self.friday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.friday_table.setColumnCount(7)
        self.friday_table.setHorizontalHeaderLabels(["Subject", "Time", "Class", "Teacher", 'Week number', ' ', ' '])

        self._update_friday_table()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.friday_table)
        self.friday_gbox.setLayout(self.mvbox)

    def _update_friday_table(self):
        self.cursor.execute("SELECT * FROM select_day('Пятница')")
        records = list(self.cursor.fetchall())

        self.friday_table.setRowCount(len(records) + 1)

        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Join")
            delButton = QPushButton("Delete")

            self.friday_table.setItem(i, 0,
                                      QTableWidgetItem(str(r[0])))
            self.friday_table.setItem(i, 1,
                                      QTableWidgetItem(str(r[1])))
            self.friday_table.setItem(i, 2,
                                      QTableWidgetItem(str(r[2])))
            self.friday_table.setItem(i, 3,
                                      QTableWidgetItem(str(r[3])))
            self.friday_table.setItem(i, 4,
                                      QTableWidgetItem(str(r[4])))

            self.friday_table.setCellWidget(i, 5, joinButton)

            self.friday_table.setCellWidget(i, 6, delButton)

            joinButton.clicked.connect(lambda ch, num=i: self._change_day_from_table_4(num, records))
            delButton.clicked.connect(lambda ch, num=i: self._del_lesson_4(num, records))

        self.friday_table.resizeRowsToContents()

    def _del_lesson(self, rowNum, records):
        row = list()
        day: int
        for i in range(self.monday_table.columnCount()):
            try:
                row.append(self.monday_table.item(rowNum, i).text())
            except:
                row.append(None)
        for record in records:
            if row[3] == record[3]:
                day = record[4]
                break
        self.cursor.execute("CALL update_day(%s, %s, %s)", (10, '', day))

    def _del_lesson_1(self, rowNum, records):
        row = list()
        day: int
        for i in range(self.tuesday_table.columnCount()):
            try:
                row.append(self.tuesday_table.item(rowNum, i).text())
            except:
                row.append(None)
        for record in records:
            if row[3] == record[3]:
                day = record[4]
                break
        self.cursor.execute("CALL update_day(%s, %s, %s)", (10, '', day))

    def _del_lesson_2(self, rowNum, records):
        row = list()
        day: int
        for i in range(self.wednesday_table.columnCount()):
            try:
                row.append(self.wednesday_table.item(rowNum, i).text())
            except:
                row.append(None)
        for record in records:
            if row[3] == record[3]:
                day = record[4]
                break
        self.cursor.execute("CALL update_day(%s, %s, %s)", (10, '', day))

    def _del_lesson_3(self, rowNum, records):
        row = list()
        day: int
        for i in range(self.thursday_table.columnCount()):
            try:
                row.append(self.thursday_table.item(rowNum, i).text())
            except:
                row.append(None)
        for record in records:
            if row[3] == record[3]:
                day = record[4]
                break
        self.cursor.execute("CALL update_day(%s, %s, %s)", (10, '', day))

    def _del_lesson_4(self, rowNum, records):
        row = list()
        day: int
        for i in range(self.friday_table.columnCount()):
            try:
                row.append(self.friday_table.item(rowNum, i).text())
            except:
                row.append(None)
        for record in records:
            if row[3] == record[3]:
                day = record[4]
                break
        self.cursor.execute("CALL update_day(%s, %s, %s)", (10, '', day))


    def _del_teacher(self, rowNum):
        row = list()
        for i in range(self.teacher_table.columnCount()):
            try:
                row.append(self.teacher_table.item(rowNum, i).text())
            except:
                row.append(None)
        print(row)
        self.cursor.execute("DELETE FROM teacher WHERE id=%s", (row[0],))
        self.conn.commit()

    def _del_subject(self, rowNum):
        row = list()
        for i in range(self.subject_table.columnCount()):
            try:
                row.append(self.subject_table.item(rowNum, i).text())
            except:
                row.append(None)
        print(row)
        self.cursor.execute("DELETE FROM subject WHERE id=%s", (row[0],))
        self.conn.commit()

    def _change_teacher(self, rowNum):
        row = list()
        for i in range(self.teacher_table.columnCount()):
            try:
                row.append(self.teacher_table.item(rowNum, i).text())
            except:
                row.append(None)
        try:
            self.cursor.execute("CALL update_teacher(%s, %s)", (row[0], row[1]))
            self.conn.commit()
            QMessageBox.about(self, "Success", "Fields are transformed")
        except:
            self.conn.commit()
            QMessageBox.about(self, "Error", "Enter all fields")

    def change_subject(self, rowNum):
        row = list()
        for i in range(self.subject_table.columnCount()):
            try:
                row.append(self.subject_table.item(rowNum, i).text())
            except:
                row.append(None)
        try:
            self.cursor.execute("CALL update_subject(%s, %s)", (row[0], row[1]))
            self.conn.commit()
            QMessageBox.about(self, "Success", "Fields are transformed")
        except:
            self.conn.commit()
            QMessageBox.about(self, "Error", "Enter all fields")

    def _change_day_from_table(self, rowNum, records):
        row = list()
        day: int
        for i in range(self.monday_table.columnCount()):
            try:
                row.append(self.monday_table.item(rowNum, i).text())
            except:
                row.append(None)
        for record in records:

            if row[3] == record[3]:
                day = record[4]
                break
        sub_id: int
        self.cursor.execute("SELECT * FROM subject")
        check = list(self.cursor.fetchall())
        subject = []
        for _, sub in check:
            subject.append(sub)  # заполнение списка с предметами
        if row[0] not in subject:
            QMessageBox.about(self, "ERROR", "Нет такого предмета")
            return
        elif row[0] in subject:  # проверка на наличие предмета
            for num, sub in check:  # сравнение предмета с его id
                if sub == row[0]:
                    sub_id = num
                    break
        try:
            self.cursor.execute("CALL update_day(%s, %s, %s)", (sub_id, row[1], day))
            self.conn.commit()
            QMessageBox.about(self, "Success", "Fields are transformed")
        except:
            self.conn.commit()
            QMessageBox.about(self, "Error", "Enter all fields")

    def _change_day_from_table_1(self, rowNum, records):
        row = list()
        day: int
        for i in range(self.tuesday_table.columnCount()):
            try:
                row.append(self.tuesday_table.item(rowNum, i).text())
            except:
                row.append(None)
        for record in records:

            if row[3] == record[3]:
                day = record[4]
                break
        sub_id: int
        self.cursor.execute("SELECT * FROM subject")
        check = list(self.cursor.fetchall())
        subject = []
        for _, sub in check:
            subject.append(sub)  # заполнение списка с предметами
        if row[0] not in subject:
            QMessageBox.about(self, "ERROR", "Нет такого предмета")
            return
        elif row[0] in subject:  # проверка на наличие предмета
            for num, sub in check:  # сравнение предмета с его id
                if sub == row[0]:
                    sub_id = num
                    break
        try:
            self.cursor.execute("CALL update_day(%s, %s, %s)", (sub_id, row[1], day))
            self.conn.commit()
            QMessageBox.about(self, "Success", "Fields are transformed")
        except:
            self.conn.commit()
            QMessageBox.about(self, "Error", "Enter all fields")

    def _change_day_from_table_2(self, rowNum, records):
        row = list()
        day: int
        for i in range(self.wednesday_table.columnCount()):
            try:
                row.append(self.wednesday_table.item(rowNum, i).text())
            except:
                row.append(None)
        for record in records:

            if row[3] == record[3]:
                day = record[4]
                break
        sub_id: int
        self.cursor.execute("SELECT * FROM subject")
        check = list(self.cursor.fetchall())
        subject = []
        for _, sub in check:
            subject.append(sub)  # заполнение списка с предметами
        if row[0] not in subject:
            QMessageBox.about(self, "ERROR", "Нет такого предмета")
            return
        elif row[0] in subject:  # проверка на наличие предмета
            for num, sub in check:  # сравнение предмета с его id
                if sub == row[0]:
                    sub_id = num
                    break
        try:
            self.cursor.execute("CALL update_day(%s, %s, %s)", (sub_id, row[1], day))
            self.conn.commit()
            QMessageBox.about(self, "Success", "Fields are transformed")
        except:
            self.conn.commit()
            QMessageBox.about(self, "Error", "Enter all fields")

    def _change_day_from_table_3(self, rowNum, records):
        row = list()
        day: int
        for i in range(self.thursday_table.columnCount()):
            try:
                row.append(self.thursday_table.item(rowNum, i).text())
            except:
                row.append(None)
        for record in records:

            if row[3] == record[3]:
                day = record[4]
                break
        sub_id: int
        self.cursor.execute("SELECT * FROM subject")
        check = list(self.cursor.fetchall())
        subject = []
        for _, sub in check:
            subject.append(sub)  # заполнение списка с предметами
        if row[0] not in subject:
            QMessageBox.about(self, "ERROR", "Нет такого предмета")
            return
        elif row[0] in subject:  # проверка на наличие предмета
            for num, sub in check:  # сравнение предмета с его id
                if sub == row[0]:
                    sub_id = num
                    break
        try:
            self.cursor.execute("CALL update_day(%s, %s, %s)", (sub_id, row[1], day))
            self.conn.commit()
            QMessageBox.about(self, "Success", "Fields are transformed")
        except:
            self.conn.commit()
            QMessageBox.about(self, "Error", "Enter all fields")

    def _change_day_from_table_4(self, rowNum, records):
        row = list()
        day: int
        for i in range(self.friday_table.columnCount()):
            try:
                row.append(self.friday_table.item(rowNum, i).text())
            except:
                row.append(None)
        for record in records:

            if row[3] == record[3]:
                day = record[4]
                break
        sub_id: int
        self.cursor.execute("SELECT * FROM subject")
        check = list(self.cursor.fetchall())
        subject = []
        for _, sub in check:
            subject.append(sub)  # заполнение списка с предметами
        if row[0] not in subject:
            QMessageBox.about(self, "ERROR", "Нет такого предмета")
            return
        elif row[0] in subject:  # проверка на наличие предмета
            for num, sub in check:  # сравнение предмета с его id
                if sub == row[0]:
                    sub_id = num
                    break
        try:
            self.cursor.execute("CALL update_day(%s, %s, %s)", (sub_id, row[1], day))
            self.conn.commit()
            QMessageBox.about(self, "Success", "Fields are transformed")
        except:
            self.conn.commit()
            QMessageBox.about(self, "Error", "Enter all fields")


    def _update_shedule(self):
        self._update_monday_table()
        self._update_tuesday_table()
        self._update_wednesday_table()
        self._update_thursday_table()
        self._update_friday_table()
        self._update_subject_table()
        self._update_teachers()


app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())
