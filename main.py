import psycopg2
import sys

from PyQt5.QtWidgets import (QApplication, QWidget,
                             QTabWidget, QAbstractScrollArea,
                             QVBoxLayout, QHBoxLayout,
                             QTableWidget, QGroupBox,
                             QTableWidgetItem, QPushButton, QMessageBox)


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow,self).__init__()

        self._connect_to_db()

        self.setWindowTitle("Timetable")

        self.vbox=QVBoxLayout(self)

        self.tabs=QTabWidget(self)
        self.vbox.addWidget(self.tabs)

        self._create_timetable_tab()
        self._create_teachers_tab()
        self._create_subjects_tab()
        

    def _connect_to_db(self):
        self.conn=psycopg2.connect(database="timetable_db",
                                     user="postgres",
                                     password="25lol25lol25",
                                     host="localhost",
                                     port="5432")

        self.cursor=self.conn.cursor()


    def _create_timetable_tab(self):
        self.timetable_tab=QWidget()
        self.tabs.addTab(self.timetable_tab,"Timetable")
        self.svbox=QVBoxLayout()
        days=['Понедельник','Вторник','Среда','Четверг','Пятница']
        for i in range(len(days)):
            # f'{}' - форматированный строковый литерал
            # setattr функция устанавливающая значение атрибута указанного объекта по его имени
            # f'shbox{i} - имя атрибута
            # getattribute - вызывается всегда для реализации доступа к атрибутам для экземпляров класса
            # getattr - позволяет получить значение атрибута объекта по его имени
            setattr(self,f'{days[i]}_gbox',QGroupBox(days[i]))
            setattr(self,f'shbox{i}',QHBoxLayout())
            self.svbox.__getattribute__('addLayout')(getattr(self, f'shbox{i}'))
            getattr(self, f'shbox{i}').__getattribute__('addWidget')(getattr(self, f'{days[i]}_gbox'))
            self.__getattribute__('_create_day_table')(f'{days[i]}')

        self.shbox5=QHBoxLayout()
        self.svbox.addLayout(self.shbox5)
        
        self.update_timetable_button=QPushButton("Update")
        
        self.shbox5.addWidget(self.update_timetable_button)
        self.update_timetable_button.clicked.connect(self._update_timetable)

        self.timetable_tab.setLayout(self.svbox)


    def _create_teachers_tab(self):
        self.teachers_tab=QWidget()
        self.tabs.addTab(self.teachers_tab,"Teachers")

        self.teachers_gbox=QGroupBox("Teachers")

        self.svbox=QVBoxLayout()
        self.shbox1=QHBoxLayout()
        self.shbox2=QHBoxLayout()

        self.svbox.addLayout(self.shbox1)
        self.svbox.addLayout(self.shbox2)

        self.shbox1.addWidget(self.teachers_gbox)

        self._create_teachers_table()

        self.update_timetable_button=QPushButton("Update")
        self.shbox2.addWidget(self.update_timetable_button)
        self.update_timetable_button.clicked.connect(self._update_timetable)

        self.teachers_tab.setLayout(self.svbox)
        

    def _create_subjects_tab(self):
        self.subjects_tab=QWidget()
        self.tabs.addTab(self.subjects_tab,"Subjects")

        self.subjects_gbox=QGroupBox("Subjects")

        self.svbox=QVBoxLayout()
        self.shbox1=QHBoxLayout()
        self.shbox2=QHBoxLayout()

        self.svbox.addLayout(self.shbox1)
        self.svbox.addLayout(self.shbox2)

        self.shbox1.addWidget(self.subjects_gbox)

        self._create_subjects_table()

        self.update_timetable_button=QPushButton("Update")
        self.shbox2.addWidget(self.update_timetable_button)
        self.update_timetable_button.clicked.connect(self._update_timetable)

        self.subjects_tab.setLayout(self.svbox)


    def _create_day_table(self, day):
        setattr(self, f'day_table_{day}', QTableWidget())
        getattr(self, f'day_table_{day}').setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        getattr(self, f'day_table_{day}').setColumnCount(7)
        getattr(self, f'day_table_{day}').setHorizontalHeaderLabels(["id","Day","Subject","Room","Time","Join","Delete"])

        self._update_day_table(day)

        self.mvbox=QVBoxLayout()
        self.mvbox.addWidget(getattr(self, f'day_table_{day}'))
        
        getattr(self, f'{day}_gbox').setLayout(self.mvbox)


    def _create_teachers_table(self):
        self.teachers_table=QTableWidget()
        self.teachers_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.teachers_table.setColumnCount(5)
        self.teachers_table.setHorizontalHeaderLabels(["id","Full_Name","Subject","Join","Delete"])

        self._update_teachers_table()

        self.mvbox=QVBoxLayout()
        self.mvbox.addWidget(self.teachers_table)
        self.teachers_gbox.setLayout(self.mvbox)


    def _create_subjects_table(self):
        self.subjects_table=QTableWidget()
        self.subjects_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.subjects_table.setColumnCount(3)
        self.subjects_table.setHorizontalHeaderLabels(["Name","Join","Delete"])

        self._update_subjects_table()

        self.mvbox=QVBoxLayout()
        self.mvbox.addWidget(self.subjects_table)
        self.subjects_gbox.setLayout(self.mvbox)


    def _update_day_table(self, day):
        getattr(self, f'day_table_{str(day)}').setRowCount(0)
        self.cursor.execute(f"SELECT * FROM timetable_tab WHERE day='{str(day)}'")
        records=list(self.cursor.fetchall())

        getattr(self, f'day_table_{day}').setRowCount(len(records) + 1)

        for i, r in enumerate(records):
            r=list(r)
            
            joinButton=QPushButton("Join")
            deleteButton=QPushButton("Delete")
            insertButton=QPushButton("Insert")
            
            getattr(self, f'day_table_{day}').setItem(i, 0, QTableWidgetItem(str(r[0])))
            getattr(self, f'day_table_{day}').setItem(i, 1, QTableWidgetItem(str(r[1])))
            getattr(self, f'day_table_{day}').setItem(i, 2, QTableWidgetItem(str(r[2])))
            getattr(self, f'day_table_{day}').setItem(i, 3, QTableWidgetItem(str(r[3])))
            getattr(self, f'day_table_{day}').setItem(i, 4, QTableWidgetItem(str(r[4])))
        
            getattr(self, f'day_table_{day}').setCellWidget(i, 5, joinButton)
            getattr(self, f'day_table_{day}').setCellWidget(i, 6, deleteButton)
            getattr(self, f'day_table_{day}').setCellWidget(len(records), 5, insertButton)

            joinButton.clicked.connect(lambda ch, num=i, day=day: self._change_day_from_table(num, day))
            deleteButton.clicked.connect(lambda ch, id_to_delete=r[0], num=i: self._delete_day_from_table(id_to_delete, num, day))
            insertButton.clicked.connect(lambda ch, num=i + 1: self._insert_day_from_table(num, day))

            getattr(self, f'day_table_{day}').resizeRowsToContents()

        if len(records)==0:
            insertButton=QPushButton("Введите первую запись")
            getattr(self, f'day_table_{day}').setCellWidget(len(records), 5, insertButton)
            insertButton.clicked.connect(lambda ch, num=0: self._insert_day_from_table(num, day))

            getattr(self, f'day_table_{day}').resizeRowsToContents()


    def _update_teachers_table(self):
        self.teachers_table.removeRow(0)
        self.cursor.execute("SELECT * FROM teachers_tab")
        records=list(self.cursor.fetchall())
        self.teachers_table.setRowCount(len(records) + 1)

        for i, r in enumerate(records):
            r=list(r)
            
            joinButton=QPushButton("Join")
            deleteButton=QPushButton("Delete")
            insertButton=QPushButton("Insert")
            
            self.teachers_table.setItem(i, 0, QTableWidgetItem(str(r[0])))
            self.teachers_table.setItem(i, 1, QTableWidgetItem(str(r[1])))
            self.teachers_table.setItem(i, 2, QTableWidgetItem(str(r[2])))
            
            self.teachers_table.setCellWidget(i, 3, joinButton)
            self.teachers_table.setCellWidget(i, 4, deleteButton)
            self.teachers_table.setCellWidget(len(records), 3, insertButton)
            
            joinButton.clicked.connect(lambda ch, num=i: self._change_teachers_from_table(num))
            deleteButton.clicked.connect(lambda ch, id_to_delete=r[0], num=i: self._delete_teachers_from_table(id_to_delete, num))
            insertButton.clicked.connect(lambda ch, num=i + 1: self._insert_teachers_from_table(num))

            self.teachers_table.resizeRowsToContents()

        if len(records)==0:
            insertButton=QPushButton("Введите первую запись")
            self.teachers_table.setCellWidget(len(records), 3, insertButton)
            insertButton.clicked.connect(lambda ch, num=0: self._insert_teachers_from_table(num))

            self.teachers_table.resizeRowsToContents()


    def _update_subjects_table(self):
        self.subjects_table.removeRow(0)
        self.cursor.execute("SELECT * FROM subjects_tab")
        records=list(self.cursor.fetchall())
        self.subjects_table.setRowCount(len(records) + 1)

        for i, r in enumerate(records):
            r=list(r)
            
            joinButton = QPushButton("Join")
            deleteButton = QPushButton("Delete")
            insertButton = QPushButton("Insert")
            
            self.subjects_table.setItem(i, 0, QTableWidgetItem(str(r[0])))
            
            self.subjects_table.setCellWidget(i, 1, joinButton)
            self.subjects_table.setCellWidget(i, 2, deleteButton)
            self.subjects_table.setCellWidget(len(records), 1, insertButton)
            
            joinButton.clicked.connect(lambda ch, num=i: self._change_subjects_from_table(num))
            deleteButton.clicked.connect(lambda ch, id_to_delete=r[0], num=i: self._delete_subjects_from_table(id_to_delete, num))
            insertButton.clicked.connect(lambda ch, num=i + 1: self._insert_subjects_from_table(num))

            self.subjects_table.resizeRowsToContents()

        if len(records)==0:
            insertButton=QPushButton("Введите первую запись")
            self.subjects_table.setCellWidget(len(records), 2, insertButton)
            insertButton.clicked.connect(lambda ch, num=0: self._insert_subjects_from_table(num))

            self.subjects_table.resizeRowsToContents()


    def _change_day_from_table(self, rowNum, day):
        row=list()
        for i in range(getattr(self, f'day_table_{day}').columnCount()):
            try:
                row.append(getattr(self, f'day_table_{day}').item(rowNum, i).text())
            except:
                row.append(None)
        #print(rowNum)
        #print(row[0])
        try:
            self.cursor.execute(f"UPDATE timetable_tab SET (day,subject,room,time) = ('{row[1]}','{row[2]}','{row[3]}','{row[4]}') WHERE id={row[0]};")
            self.conn.commit()
        except:
            QMessageBox.about(self, "Ошибка", "Заполните поля корректно!")


    def _change_teachers_from_table(self, rowNum):
        row=list()
        for i in range(self.teachers_table.columnCount()):
            try:
                row.append(self.teachers_table.item(rowNum, i).text())
            except:
                row.append(None)
        #rowch=rowNum+1
        try:
            #self.cursor.execute("UPDATE teachers_tab SET subject='" + str(row[1]) + "', full_name='" + row[0] + "' WHERE id='" + str(rowch) + "'")
            self.cursor.execute("UPDATE teachers_tab SET subject='" + str(row[2]) + "', full_name='" + str(row[1]) + "' where id='" + str(row[0]) + "'")
            self.conn.commit()
        except:
            QMessageBox.about(self, "Ошибка", "Заполните поля корректно!")


    def _change_subjects_from_table(self, rowNum):
        row=list()
        for i in range(self.subjects_table.columnCount()):
            try:
                row.append(self.subjects_table.item(rowNum, i).text())
            except:
                row.append(None)        
        try:
            self.cursor.execute("UPDATE subjects_tab SET name='" + str(row[1]) + "' WHERE id='" + str(row[0]) + "'")
            self.conn.commit()
        except:
            QMessageBox.about(self, "Ошибка", "Заполните поля корректно!")


    def _delete_day_from_table(self, delete, rowNum, day):
        try:
            self.cursor.execute("DELETE FROM timetable_tab WHERE id=" + str(delete) + ";")
            self.conn.commit()
        except:
            QMessageBox.about(self, "Ошибка", "Не существует!")
        getattr(self, f'day_table_{day}').removeRow(rowNum)
        self._update_day_table(day)
        

    def _delete_subjects_from_table(self, delete, rowNum):
        try:
            self.cursor.execute("DELETE FROM subjects_tab WHERE name='" + str(delete) + "';")
            self.conn.commit()
        except:
            QMessageBox.about(self, "Ошибка", "Не существует!")
        self.subjects_table.removeRow(rowNum)
        self._update_subjects_table()
        

    def _delete_teachers_from_table(self, delete, rowNum):
        rowdel=rowNum+1
        print(rowNum)
        try:
            self.cursor.execute("DELETE FROM teachers_tab WHERE id='" + str(delete) + "';")
            self.conn.commit()
        except:
            QMessageBox.about(self, "Ошибка", "Не существует!")
        self.teachers_table.removeRow(rowNum)
        self._update_teachers_table()
        

    def _insert_day_from_table(self, rowNum, day):
        row=list()
        for i in range(getattr(self, f'day_table_{day}').columnCount()):
            try:
                row.append(getattr(self, f'day_table_{day}').item(rowNum, i).text())
            except:
                row.append(None)
        try:
            self.cursor.execute(f"INSERT INTO timetable_tab VALUES ({str(row[0])},'{str(row[1])}','{str(row[2])}','{str(row[3])}','{str(row[4])}');")
            self.conn.commit()
        except:
            QMessageBox.about(self, "Ошибка", "Заполните поля корректно!")


    def _insert_teachers_from_table(self, rowNum):
        row=list()
        for i in range(self.teachers_table.columnCount()):
            try:
                row.append(self.teachers_table.item(rowNum, i).text())
            except:
                row.append(None)
        try:
            self.cursor.execute("INSERT INTO teachers_tab VALUES ('" + str(row[0]) + "', '" + str(row[1]) + "', '" + str(row[2]) + "');")
            self.conn.commit()

        except:
            QMessageBox.about(self, "Ошибка", "Заполните поля корректно!")


    def _insert_subjects_from_table(self, rowNum):
        row=list()
        for i in range(self.subjects_table.columnCount()):
            try:
                row.append(self.subjects_table.item(rowNum, i).text())
            except:
                row.append(None)
        try:
            self.cursor.execute("INSERT INTO subjects_tab VALUES ('" + str(row[0]) + "');")
            self.conn.commit()
        except:
            QMessageBox.about(self, "Ошибка", "Заполните поля корректно!")
            

    def _update_timetable(self):
        days=['Понедельник','Вторник','Среда','Четверг','Пятница']
        for day in days:
            self._update_day_table(day)
            self._update_teachers_table()
            self._update_subjects_table()


app=QApplication(sys.argv)
win=MainWindow()
win.show()
sys.exit(app.exec_())
