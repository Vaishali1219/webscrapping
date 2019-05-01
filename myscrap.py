# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'myscrap.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import sqlite3

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.url = QtWidgets.QLineEdit(self.centralwidget)
        self.url.setObjectName("url")
        self.horizontalLayout.addWidget(self.url)
        self.gdbtn = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.gdbtn.setFont(font)
        self.gdbtn.setObjectName("gdbtn")
        self.gdbtn.clicked.connect(self.loadData)
        self.horizontalLayout.addWidget(self.gdbtn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.table = QtWidgets.QTableWidget(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.table.setFont(font)
        self.table.setColumnCount(3)
        self.table.setObjectName("table")
        self.table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(2, item)
        self.verticalLayout.addWidget(self.table)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.cancelbtn = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.cancelbtn.setFont(font)
        self.cancelbtn.setObjectName("cancelbtn")
        self.horizontalLayout_2.addWidget(self.cancelbtn)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.cancelbtn.clicked.connect(self.table.clearContents)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Enter Url"))
        self.gdbtn.setText(_translate("MainWindow", "Get Data"))
        item = self.table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Slno"))
        item = self.table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Product_Name"))
        item = self.table.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Price"))
        self.cancelbtn.setText(_translate("MainWindow", "Cancel"))
        
    def loadData(self):
         my_url = self.url.text()
         uClient = uReq(my_url)
         page_html = uClient.read()
         uClient.close()
         page_soup = soup(page_html, "html.parser")
         containers = page_soup.findAll("div", attrs={'class':'_3O0U0u'})
         container = containers[0]
         filename = "products.csv"
         f = open(filename, "w")
         headers = "Product_Name, Pricing, Ratings\n"
         f.write(headers)
         MyWeb = sqlite3.connect('websr.db')
         curweb = MyWeb.cursor()
         for container in containers:
             product_name = container.div.img["alt"]
             price_container = container.findAll("div", attrs={"class" : "col col-5-12 _2o7WAb"})
             price = price_container[0].text.strip()
             trim_price = ''.join(price.split(','))
             rm_rupee = trim_price.split("₹")
             add_rs_price = "Rs." + rm_rupee[1]
             split_price = add_rs_price.split('E')
             final_price = split_price[0]
             curweb.execute("INSERT INTO web (Product_Name, Price) VALUES ('{}', '{}');".format(product_name, final_price))
             print(product_name.replace(",", "|") + "," + final_price + "\n")
             f.write(product_name.replace(",", "|") + "," + final_price + "\n")
         MyWeb.commit()
         MyWe = sqlite3.connect('websr.db')
         sql = "SELECT * from web;"
         result = MyWe.execute(sql)
         self.table.setRowCount(2)
         for row_number, row_data in enumerate(result):
             self.table.insertRow(row_number)
             for column_number, data in enumerate(row_data):
                 self.table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
         MyWe.close()




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
