# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(801, 504)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralWidget)
        self.horizontalLayout.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget = QtWidgets.QWidget(self.centralWidget)
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.userinfo = QtWidgets.QGroupBox(self.widget)
        self.userinfo.setToolTipDuration(3)
        self.userinfo.setAutoFillBackground(False)
        self.userinfo.setStyleSheet("QGroupBox { \n"
"     border: 2px solid gray; \n"
"     border-radius: 3px; \n"
" } ")
        self.userinfo.setFlat(False)
        self.userinfo.setCheckable(False)
        self.userinfo.setObjectName("userinfo")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.userinfo)
        self.verticalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.widget_2 = QtWidgets.QWidget(self.userinfo)
        self.widget_2.setObjectName("widget_2")
        self.gridLayout = QtWidgets.QGridLayout(self.widget_2)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.avatar = QtWidgets.QLabel(self.widget_2)
        self.avatar.setStyleSheet("avatar{\n"
"background-color : blue\n"
"}")
        self.avatar.setText("")
        self.avatar.setObjectName("avatar")
        self.gridLayout.addWidget(self.avatar, 0, 0, 1, 1, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.dname = QtWidgets.QLabel(self.widget_2)
        self.dname.setStyleSheet("email{\n"
"background-color : blue\n"
"}")
        self.dname.setText("")
        self.dname.setObjectName("dname")
        self.gridLayout.addWidget(self.dname, 2, 0, 1, 1)
        self.nickname = QtWidgets.QLabel(self.widget_2)
        self.nickname.setText("")
        self.nickname.setObjectName("nickname")
        self.gridLayout.addWidget(self.nickname, 3, 0, 1, 1)
        self.email = QtWidgets.QLabel(self.widget_2)
        self.email.setText("")
        self.email.setObjectName("email")
        self.gridLayout.addWidget(self.email, 1, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.widget_2)
        self.verticalLayout.addWidget(self.userinfo)
        self.horizontalLayout.addWidget(self.widget)
        self.widget_3 = QtWidgets.QWidget(self.centralWidget)
        self.widget_3.setObjectName("widget_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget_3)
        self.verticalLayout_3.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.groupBox = QtWidgets.QGroupBox(self.widget_3)
        self.groupBox.setStyleSheet("QGroupBox { \n"
"     border: 2px solid gray; \n"
"     border-radius: 3px; \n"
" }")
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_7.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_7.setSpacing(6)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.widget_6 = QtWidgets.QWidget(self.groupBox)
        self.widget_6.setObjectName("widget_6")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget_6)
        self.horizontalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.groupBox_2 = QtWidgets.QGroupBox(self.widget_6)
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_4.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.btn_load_contacts = QtWidgets.QPushButton(self.groupBox_2)
        self.btn_load_contacts.setObjectName("btn_load_contacts")
        self.horizontalLayout_4.addWidget(self.btn_load_contacts)
        self.btn_save_contacts = QtWidgets.QPushButton(self.groupBox_2)
        self.btn_save_contacts.setObjectName("btn_save_contacts")
        self.horizontalLayout_4.addWidget(self.btn_save_contacts)
        self.horizontalLayout_2.addWidget(self.groupBox_2)
        self.chck_groups = QtWidgets.QCheckBox(self.widget_6)
        self.chck_groups.setObjectName("chck_groups")
        self.horizontalLayout_2.addWidget(self.chck_groups)
        self.btn_refresh_contact = QtWidgets.QToolButton(self.widget_6)
        self.btn_refresh_contact.setObjectName("btn_refresh_contact")
        self.horizontalLayout_2.addWidget(self.btn_refresh_contact)
        self.verticalLayout_7.addWidget(self.widget_6)
        self.contacts_table = QtWidgets.QTableView(self.groupBox)
        self.contacts_table.setObjectName("contacts_table")
        self.verticalLayout_7.addWidget(self.contacts_table)
        self.verticalLayout_3.addWidget(self.groupBox)
        self.widget_5 = QtWidgets.QWidget(self.widget_3)
        self.widget_5.setObjectName("widget_5")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.widget_5)
        self.verticalLayout_5.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_5.setSpacing(6)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.widget_7 = QtWidgets.QWidget(self.widget_5)
        self.widget_7.setObjectName("widget_7")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widget_7)
        self.horizontalLayout_3.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.btn_bold = QtWidgets.QToolButton(self.widget_7)
        self.btn_bold.setStyleSheet("")
        self.btn_bold.setObjectName("btn_bold")
        self.horizontalLayout_3.addWidget(self.btn_bold)
        self.btn_italic = QtWidgets.QToolButton(self.widget_7)
        self.btn_italic.setStyleSheet("")
        self.btn_italic.setObjectName("btn_italic")
        self.horizontalLayout_3.addWidget(self.btn_italic)
        self.btn_savetemplate = QtWidgets.QPushButton(self.widget_7)
        self.btn_savetemplate.setObjectName("btn_savetemplate")
        self.horizontalLayout_3.addWidget(self.btn_savetemplate)
        self.btn_templates = QtWidgets.QPushButton(self.widget_7)
        self.btn_templates.setObjectName("btn_templates")
        self.horizontalLayout_3.addWidget(self.btn_templates)
        self.verticalLayout_5.addWidget(self.widget_7)
        self.txt_msg = QtWidgets.QPlainTextEdit(self.widget_5)
        self.txt_msg.setObjectName("txt_msg")
        self.verticalLayout_5.addWidget(self.txt_msg)
        self.verticalLayout_3.addWidget(self.widget_5)
        self.horizontalLayout.addWidget(self.widget_3)
        self.widget_8 = QtWidgets.QWidget(self.centralWidget)
        self.widget_8.setObjectName("widget_8")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.widget_8)
        self.verticalLayout_6.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_6.setSpacing(6)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.table_log = QtWidgets.QTableView(self.widget_8)
        self.table_log.setObjectName("table_log")
        self.verticalLayout_6.addWidget(self.table_log)
        self.btn_send = QtWidgets.QPushButton(self.widget_8)
        self.btn_send.setObjectName("btn_send")
        self.verticalLayout_6.addWidget(self.btn_send)
        self.horizontalLayout.addWidget(self.widget_8)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 801, 21))
        self.menuBar.setObjectName("menuBar")
        self.menuMore = QtWidgets.QMenu(self.menuBar)
        self.menuMore.setObjectName("menuMore")
        self.menuHelp = QtWidgets.QMenu(self.menuBar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuAccount = QtWidgets.QMenu(self.menuBar)
        self.menuAccount.setObjectName("menuAccount")
        MainWindow.setMenuBar(self.menuBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.actionSetup_Access_Token = QtWidgets.QAction(MainWindow)
        self.actionSetup_Access_Token.setObjectName("actionSetup_Access_Token")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.action_About = QtWidgets.QAction(MainWindow)
        self.action_About.setObjectName("action_About")
        self.actionRemove_Account = QtWidgets.QAction(MainWindow)
        self.actionRemove_Account.setObjectName("actionRemove_Account")
        self.actionClear_Logs = QtWidgets.QAction(MainWindow)
        self.actionClear_Logs.setObjectName("actionClear_Logs")
        self.actionExport = QtWidgets.QAction(MainWindow)
        self.actionExport.setObjectName("actionExport")
        self.actionImport = QtWidgets.QAction(MainWindow)
        self.actionImport.setObjectName("actionImport")
        self.menuMore.addAction(self.actionSetup_Access_Token)
        self.menuMore.addAction(self.actionClear_Logs)
        self.menuHelp.addAction(self.action_About)
        self.menuAccount.addAction(self.actionRemove_Account)
        self.menuAccount.addAction(self.actionExport)
        self.menuAccount.addAction(self.actionImport)
        self.menuBar.addAction(self.menuMore.menuAction())
        self.menuBar.addAction(self.menuAccount.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "TeamsExt"))
        self.userinfo.setTitle(_translate("MainWindow", "User Info"))
        self.groupBox.setTitle(_translate("MainWindow", "Contacts"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Favorites"))
        self.btn_load_contacts.setText(_translate("MainWindow", "Load"))
        self.btn_save_contacts.setText(_translate("MainWindow", "Save"))
        self.chck_groups.setText(_translate("MainWindow", "Display All"))
        self.btn_refresh_contact.setText(_translate("MainWindow", "Re"))
        self.btn_bold.setText(_translate("MainWindow", "Bold"))
        self.btn_italic.setText(_translate("MainWindow", "Italic"))
        self.btn_savetemplate.setText(_translate("MainWindow", "Save"))
        self.btn_templates.setText(_translate("MainWindow", "Load"))
        self.btn_send.setText(_translate("MainWindow", "Send"))
        self.menuMore.setTitle(_translate("MainWindow", "Tools"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.menuAccount.setTitle(_translate("MainWindow", "Account"))
        self.actionSetup_Access_Token.setText(_translate("MainWindow", "Setup Access Token"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.action_About.setText(_translate("MainWindow", "About"))
        self.actionRemove_Account.setText(_translate("MainWindow", "Remove"))
        self.actionClear_Logs.setText(_translate("MainWindow", "Clear Logs"))
        self.actionExport.setText(_translate("MainWindow", "Export"))
        self.actionImport.setText(_translate("MainWindow", "Import"))

