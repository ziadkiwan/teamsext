import os
import shelve
import urllib as urllib
import zipfile
from datetime import time, datetime
from itertools import islice

from PyQt5.QtCore import pyqtSignal, QThread, QAbstractTableModel, Qt, QVariant, QUrl
from PyQt5.QtGui import QPixmap, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QMessageBox, QInputDialog, QLineEdit, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView

from Loadingdialog import Ui_Dialog as loadingui
import Messagestemplate as msg_template

import Mainwindow as maingui
import AuthDialog as adiag
from PyQt5 import QtWidgets, QtCore, QtGui
import sys

import app_config as app_cfg

import json
import requests
import user_info as user
import dbhelper as db
import contact as ctct

version = "0.4.2"

stored_accesstoken = ""

headers = {"Authorization": "Bearer " + stored_accesstoken,
           "Content-Type": "application/json; charset=utf-8"}

windows = []

current_user = ""

contact_table_Headers = ["Title", "Select", "Type"]
log_table_headers = ["Contacts", "Date", "Message"]
message_templates_table_header = ["Id", "Message", "Select", "Remove"]
favorites_table_header = ["Name", "Contacts", "Select", "Remove"]

redirect_url = "https://github.com/ziadkiwan/teamsext"

app_integration_url = "https://api.ciscospark.com/v1/authorize?client_id=Cd0541422a182f5e0e00344e3ea8f7fca7ddfecb5b8e56b7776c2cb8759210ca3&response_type=code&redirect_uri=https%3A%2F%2Fgithub.com%2Fziadkiwan%2Fteamsext&scope=spark-compliance%3Amemberships_read%20spark-admin%3Aresource_groups_read%20spark%3Aall%20spark-compliance%3Amemberships_write%20spark-admin%3Apeople_write%20spark-admin%3Aroles_read%20spark-admin%3Aorganizations_read%20spark-admin%3Aresource_group_memberships_read%20spark-admin%3Aresource_group_memberships_write%20spark-compliance%3Arooms_read%20spark-compliance%3Ateam_memberships_read%20spark-compliance%3Amessages_write%20spark-compliance%3Ateam_memberships_write%20spark%3Akms%20spark-compliance%3Ateams_read%20spark-compliance%3Amessages_read%20spark-admin%3Apeople_read&state=set_state_here"


# class ContactsTableModel(QAbstractTableModel):
#     def __init__(self, parent, mylist, header, *args):
#         QAbstractTableModel.__init__(self, parent, *args)
#         self.mylist = mylist
#         self.header = header
#
#     def rowCount(self, parent):
#         return len(self.mylist)
#
#     def columnCount(self, parent):
#         if self.mylist:
#             return len(self.mylist[0])
#         else:
#             return 0
#
#     def data(self, index, role=QtCore.Qt.DisplayRole):
#         if not index.isValid():
#             return None
#         # elif role == Qt.EditRole:
#         #     return self.mylist[index.row()][index.column()]
#         elif role != Qt.DisplayRole:
#             return None
#         # if "no" in self.mylist[index.row()][1] and column == 1:
#         #     return QtCore.QVariant(QtCore.Qt.Unchecked)
#         # else:
#         #     return QtCore.QVariant(QtCore.Qt.Checked)
#         # print(row,column)
#         return self.mylist[index.row()][index.column()]
#
#     def headerData(self, col, orientation, role):
#         if orientation == Qt.Horizontal and role == Qt.DisplayRole:
#             return self.header[col]
#         return None
#
#     def setData(self, index, value, role=Qt.EditRole):
#         if index.isValid():
#             row = index.row()
#             col = index.column()
#             self.mylist[row][col] = value
#             self.dataChanged.emit(index, index, (Qt.DisplayRole,))
#             return True
#         return False


class extendmain(maingui.Ui_MainWindow):
    def __init__(self, windowObj):
        self.selected_fav = ""
        self.dialog = QtWidgets.QDialog()
        self.windowObj = windowObj
        self.setupUi(self.windowObj)
        self.windowObj.show()
        # self.authchange.clicked.connect(self.getuserinfo)
        self.setupuserinfo()
        self.actionSetup_Access_Token.triggered.connect(self.getuserinfo)
        self.getlocalcontacts("success")
        self.sorttable(1)
        self.btn_refresh_contact.clicked.connect(self.getteamscontacts)
        self.chck_groups.toggled.connect(self.getlocalcontacts)
        self.btn_templates.clicked.connect(self.getmessagetemplate)
        self.btn_savetemplate.clicked.connect(self.savetemplate)
        self.btn_send.clicked.connect(self.send_msg)
        self.actionClear_Logs.triggered.connect(self.clearlogs)
        self.actionRemove_Account.triggered.connect(self.removeaccount)
        self.btn_bold.setIcon(QtGui.QIcon('imgs/bold.png'))
        self.btn_italic.setIcon(QtGui.QIcon('imgs/italic.png'))
        self.btn_send.setIcon(QtGui.QIcon('imgs/send.png'))
        self.btn_savetemplate.setIcon(QtGui.QIcon('imgs/save.png'))
        self.btn_templates.setIcon(QtGui.QIcon('imgs/load.png'))
        self.btn_save_contacts.setIcon(QtGui.QIcon('imgs/save.png'))
        self.btn_load_contacts.setIcon(QtGui.QIcon('imgs/load.png'))
        self.btn_refresh_contact.setIcon(QtGui.QIcon("imgs/refresh.png"))
        self.btn_add_group.setIcon(QtGui.QIcon("imgs/add_to_group.png"))
        self.btn_bold.clicked.connect(self.boldselection)
        self.btn_italic.clicked.connect(self.italicselection)
        self.txt_msg.setPlaceholderText("Enter Your Message")
        self.btn_save_contacts.clicked.connect(self.save_contacts)
        self.btn_send.setDisabled(True)
        self.actionSetup_Access_Token_2.triggered.connect(self.ordinaryway_access_token)
        # self.action_About.triggered.connect(lambda: self.displaypopup('fooData'))
        self.action_About.triggered.connect(lambda: self.displaypopup("""Thank you for using TeamsExt, created by Ziad Kiwan and Marc Khayat. This tool is provided "as is" and is neither supported nor backed by Cisco.
Source code and latest release can be found at https://github.com/ziadkiwan/teamsext/
For feedback and suggestions, please contact ziad_kiwan_1992@hotmail.com."""))
        self.load_log_table("success")
        self.btn_load_contacts.clicked.connect(self.load_contacts_table)
        retrieveauth()
        self.actionExport.triggered.connect(self.export_account)
        self.actionImport.triggered.connect(self.import_account)
        self.actionVersion.setText("Version: " + version)
        self.txt_msg.textChanged.connect(self.txt_msg_txt_chnaged)
        self.btn_add_group.clicked.connect(self.add_to_group)
        self.actionRefresh_Access_Token.triggered.connect(self.refresh_access_token)
        # self.createkey.clicked.connect(self.showCrkey)
        # self.importkey.clicked.connect(self.showimportdialog)
        # self.browsefile.clicked.connect(self.showfiledialog)
        # self.dec.clicked.connect(self.decrypytfile)
        # self.enc.clicked.connect(self.encryptfile)
        # global keytable
        # keytable = self.keys

    #   self.windowObj.connect(keytable, SIGNAL('customContextMenuRequested(const QPoint &)'), self.contextMenuEvent)
    #    keytable.setContextMenuPolicy(Qt.CustomContextMenu)
    #    keytable.customContextMenuRequested.connect(self.contextMenuEvent)
    #    windows.append(self)

    def refresh_access_token(self):
        self.loadinguser()
        self.work = refresh_token()
        self.work.sig_error.connect(self.error_refresh_profile)
        self.work.sig_success.connect(self.setupuserinfo)
        self.work.start()

    def error_refresh_profile(self, message):
        self.erroruser()
        self.displaypopup(message)

    def ordinaryway_access_token(self):
        self.browser = QWebEngineView()
        self.browser.setWindowTitle("Teams Authentication")
        self.browser.load(QUrl(app_integration_url))
        self.browser.titleChanged.connect(self.getwebtitle)
        self.browser.show()

    def getwebtitle(self, title):
        if "https://github.com/ziadkiwan/teamsext" in title:
            access_code = title[title.rfind('?') + 6:title.rfind('&')]
            self.work = getuserdetail(access_token=access_code, is_token=False)
            self.work.sig_error.connect(self.load_profile)
            self.work.sig_success.connect(self.load_profile)
            self.work.start()

    def load_profile(self, message):
        self.browser.close()
        if message != "success":
            self.displaypopup(message)
        else:
            self.setupuserinfo()
            retrieveauth()

    def add_to_group(self):
        nbofrows = self.contacts_table.model().rowCount()
        recipients = []
        if (nbofrows == 0):
            self.displaypopup("Contacts List is empty!")
            return
        for i in range(nbofrows):
            # cell = QStandardItem(self.contacts_table.model().data(self.contacts_table.model().index(i, 1)))
            try:
                if self.contacts_table.model().item(i,
                                                    1).checkState() == QtCore.Qt.Checked or self.contacts_table.model().item(
                    i, 1).checkState() == QtCore.Qt.PartiallyChecked:
                    contact_name_index = self.contacts_table.model().index(i, 0)
                    contact_type_index = self.contacts_table.model().index(i, 2)
                    contact_type = self.contacts_table.model().data(contact_type_index)
                    if contact_type == "group":
                        contact_name = self.contacts_table.model().data(contact_name_index)
                        contact_id = db.get_id_by_contact_name(contact_name)
                        recipients.append([contact_id[0][0], contact_name])
            except Exception as e:
                print(e)
        if len(recipients) == 0:
            self.displaypopup("No groups were selected!")
            return
        Add_to_group_window = QtWidgets.QDialog()
        Add_to_group_UI = Authdialog(mainui=self, dialogobj=Add_to_group_window, is_auth=False, recept=recipients)
        windows.append(Add_to_group_UI)

    def txt_msg_txt_chnaged(self):
        nbofrows = self.contacts_table.model().rowCount()
        nbofreceipt = 0;
        if (nbofrows == 0):
            self.btn_send.setDisabled(True)
            return
        for i in range(nbofrows):
            # cell = QStandardItem(self.contacts_table.model().data(self.contacts_table.model().index(i, 1)))
            try:
                if self.contacts_table.model().item(i,
                                                    1).checkState() == QtCore.Qt.Checked or self.contacts_table.model().item(
                    i, 1).checkState() == QtCore.Qt.PartiallyChecked:
                    nbofreceipt += 1
            except Exception as e:
                print(e)
        if nbofreceipt == 0:
            self.btn_send.setDisabled(True)
            return
        if self.txt_msg.toPlainText() == "":
            self.btn_send.setDisabled(True)
        else:
            self.btn_send.setDisabled(False)

    def import_account(self):
        try:
            currentpath = os.getcwd()
            name = QtWidgets.QFileDialog.getOpenFileName(self.windowObj, 'Import Account')
            if name[0] != '':
                archive = zipfile.ZipFile(name[0], 'r')
                # text, okPressed = QInputDialog.getText(self.windowObj, "TeamExt",
                #                                        "Please input the archive password, if you did not put a password press cancel",
                #                                        QLineEdit.Normal, "")
                # if okPressed and text != '':
                #     archive.extractall(path=currentpath,pwd=text.encode)
                # else:
                archive.extractall(path=currentpath)
                self.setupuserinfo()
                self.load_log_table("success")
                self.getlocalcontacts("success")
                retrieveauth()
        except zipfile.BadZipFile as ziperror:
            self.displaypopup(str(ziperror))
        except Exception as ex:
            print(ex)
            # self.displaypopup("Unexpected Error:" +ex))

    def export_account(self):
        try:
            name = QtWidgets.QFileDialog.getSaveFileName(self.windowObj, 'Save Account')
            if name[0] != '':
                zf = zipfile.ZipFile(name[0] + ".bak", "w")
                currentpath = os.getcwd()
                backup = True

                if not os.path.exists("data.db") and not os.path.exists("00000001.jpg"):
                    backup = False
                else:
                    zf.write("data.db")
                    zf.write("00000001.jpg")
                if not os.path.exists("config.bak") and not os.path.exists("config.dat") and not os.path.exists(
                        "config.dir"):
                    backup = False
                else:
                    zf.write("config.bak")
                    zf.write("config.dat")
                    zf.write("config.dir")

                # text, okPressed = QInputDialog.getText(self.windowObj, "TeamExt",
                #                                        "For Better Security input a password, press cancel to backup without password",
                #                                        QLineEdit.Normal, "")
                #
                # if okPressed and text != '':
                #     message += ", Password was set: " + text
                #     zf.setpassword(text.encode())
                zf.close()

                if backup:
                    message = "Backup Completed"
                else:
                    message = "Partial backup done."
                self.displaypopup(message)
        except Exception as e:
            print(e)

    def load_contacts_table(self):
        Messagestemplatewindow = QtWidgets.QMainWindow()
        MessagestemplateUI = Msg_templateclass(mainui=self, templateobj=Messagestemplatewindow, msg=False)
        windows.append(MessagestemplateUI)

    def save_contacts(self):
        nbofrows = self.contacts_table.model().rowCount()
        recipients = []
        if (nbofrows == 0):
            self.displaypopup("Contacts List is empty!")
            return
        for i in range(nbofrows):
            # cell = QStandardItem(self.contacts_table.model().data(self.contacts_table.model().index(i, 1)))
            try:
                if self.contacts_table.model().item(i,
                                                    1).checkState() == QtCore.Qt.Checked or self.contacts_table.model().item(
                    i, 1).checkState() == QtCore.Qt.PartiallyChecked:
                    contact_name_index = self.contacts_table.model().index(i, 0)
                    contact_name = self.contacts_table.model().data(contact_name_index)
                    contact_id = db.get_id_by_contact_name(contact_name)
                    recipients.append(contact_id[0][0])
            except Exception as e:
                print(e)
        if len(recipients) == 0:
            self.displaypopup("No contacts were selected!")
            return
        text, okPressed = QInputDialog.getText(self.windowObj, "TeamExt", "Input a name:", QLineEdit.Normal, "")
        if okPressed and text != '':
            db.insert_favorite(recipients, text)
            self.displaypopup("Saved Successfully")

    # Messagestemplatewindow = QtWidgets.QMainWindow()
    #     MessagestemplateUI = Msg_templateclass(mainui=self, templateobj=Messagestemplatewindow)
    #     windows.append(MessagestemplateUI)

    def removeaccount(self):
        try:
            buttonReply = QMessageBox.question(self.windowObj, 'TeamsExt',
                                               "Are you sure you want to remove your account?",
                                               QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if buttonReply == QMessageBox.Yes:
                if (os._exists("00000001.jpg")):
                    os.remove("00000001.jpg")
                db.clear_all_users()
                db.clear_all_contacts()
                db.clear_all_msgtemplates()
                db.clear_all_logs()
                db.delete_all_favorites()
                storeauth("removed")
                self.load_log_table("success")
                self.getlocalcontacts("success")
                self.setupuserinfo()
        except Exception as e:
            print(e)

    def clearlogs(self):
        db.clear_all_logs()
        self.load_log_table("success")

    def send_msg(self):
        nbofrows = self.contacts_table.model().rowCount()
        recipients = []
        message = str(self.txt_msg.toPlainText())
        if message == "":
            self.displaypopup("There is no message to send!")
            return
        if (nbofrows == 0):
            self.displaypopup("Contacts List is empty!")
            return
        for i in range(nbofrows):
            # cell = QStandardItem(self.contacts_table.model().data(self.contacts_table.model().index(i, 1)))
            try:
                if self.contacts_table.model().item(i,
                                                    1).checkState() == QtCore.Qt.Checked or self.contacts_table.model().item(
                    i, 1).checkState() == QtCore.Qt.PartiallyChecked:
                    contact_name_index = self.contacts_table.model().index(i, 0)
                    contact_name = self.contacts_table.model().data(contact_name_index)
                    contact_id = db.get_id_by_contact_name(contact_name)
                    recipients.append(contact_id[0][0])
            except Exception as e:
                print(e)
        if len(recipients) == 0:
            self.displaypopup("No contacts were selected!")
            return
        if self.selected_fav != "":
            messageid = db.insert_log(self.selected_fav, "Sending.....", False)
        else:
            messageid = db.insert_log(recipients, "Sending.....")
        self.load_log_table("success")
        self.work = sendmessages(ids=recipients, message=message, messageid=messageid)
        self.work.sig_error.connect(self.load_log_table)
        self.work.sig_success.connect(self.load_log_table)
        self.work.start()

    def nth_index(self, iterable, value, n):
        matches = (idx for idx, val in enumerate(iterable) if val == value)
        return next(islice(matches, n - 1, n), None)

    def load_log_table(self, message):
        result = db.load_log()
        self.model = QStandardItemModel(self.contacts_table)
        # self.contacts_table.itemChanged.connect(self.itemChanged)
        self.table_log.setModel(self.model)
        for value in result:
            row = []
            # for item in value:
            #     cell = QStandardItem(item)
            #     cell.setToolTip(item)
            #     cell.setFlags(QtCore.Qt.ItemIsEnabled)
            #     row.append(cell)
            cell = QStandardItem(value[0])
            cell.setToolTip(value[0])
            cell.setFlags(QtCore.Qt.ItemIsEnabled)
            row.append(cell)
            datetime_object = datetime.strptime(value[1], "%Y-%m-%d %H:%M:%S.%f")
            cell = QStandardItem(datetime_object.strftime("%Y-%m-%d %H:%M"))
            cell.setToolTip(value[1])
            cell.setFlags(QtCore.Qt.ItemIsEnabled)
            row.append(cell)
            newline_count = value[2].count("\n")
            if newline_count >= 2:
                idx = self.nth_index(value[2], '\n', 2)
                cell = QStandardItem(value[2][:idx] + "...")
            elif len(value[2]) >= 120:
                cell = QStandardItem(value[2][:119] + "...")
            else:
                cell = QStandardItem(value[2])
            cell.setToolTip(value[2])
            cell.setFlags(QtCore.Qt.ItemIsEnabled)
            row.append(cell)
            self.model.appendRow(row)
        # item = QtGui.QStandardItem("Click me")
        # item.setCheckable(True)
        # self.contacts_table.appendRow(item)
        self.table_log.model().setHorizontalHeaderLabels(log_table_headers)
        header = self.table_log.horizontalHeader()
        # header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        self.table_log.resizeRowsToContents()

    def boldselection(self):
        try:
            msg = self.txt_msg.toPlainText()
            # print(msg)
            cursor = self.txt_msg.textCursor()
            tobold_selection = "**" + msg[cursor.selectionStart():cursor.selectionEnd()] + "**"
            new_str = msg[:cursor.selectionStart()] + tobold_selection + msg[cursor.selectionEnd():]
            self.txt_msg.setPlainText(new_str)

        except Exception as e:
            print(e)

    def italicselection(self):
        try:
            msg = self.txt_msg.toPlainText()
            # print(msg)
            cursor = self.txt_msg.textCursor()
            tobold_selection = "_" + msg[cursor.selectionStart():cursor.selectionEnd()] + "_"
            new_str = msg[:cursor.selectionStart()] + tobold_selection + msg[cursor.selectionEnd():]
            self.txt_msg.setPlainText(new_str)

        except Exception as e:
            print(e)

    def savetemplate(self):
        message = self.txt_msg.toPlainText()
        if str(message) != "":
            result = db.save_template(message)
            self.displaypopup("Saved Successfully")

    def getmessagetemplate(self):
        Messagestemplatewindow = QtWidgets.QMainWindow()
        MessagestemplateUI = Msg_templateclass(mainui=self, templateobj=Messagestemplatewindow, msg=True)
        windows.append(MessagestemplateUI)

    def getuserinfo(self):
        UserInfoWindow = QtWidgets.QDialog()
        UserInfoUI = Authdialog(mainui=self, dialogobj=UserInfoWindow)
        windows.append(UserInfoUI)

    def setupuserinfo(self):
        result = db.select_user_info()
        if result is not None:
            global current_user
            current_user = result
            self.email.setText("Email: " + result.email)
            self.email.setMaximumHeight(20)
            pixmap = QPixmap(result.avatar)
            pixmap = pixmap.scaled(200, 200)
            self.avatar.setPixmap(pixmap)
            self.nickname.setText("Nickname: " + result.nickname)
            self.nickname.setMaximumHeight(20)
            self.dname.setText("Display Name: " + result.displayname)
            self.dname.setMaximumHeight(20)
        else:
            pixmap = QPixmap("imgs/empty.png")
            pixmap = pixmap.scaled(200, 200)
            self.avatar.setPixmap(pixmap)
            self.email.setText("No User")
            self.email.setMaximumHeight(20)
            self.nickname.setText("No User")
            self.nickname.setMaximumHeight(20)
            self.dname.setText("No User")
            self.dname.setMaximumHeight(20)

    def loadinguser(self):
        self.email.setText("Loading.....")
        self.email.setMaximumHeight(20)
        self.nickname.setText("Loading.....")
        self.nickname.setMaximumHeight(20)
        self.dname.setText("Loading.....")
        self.dname.setMaximumHeight(20)

    def erroruser(self):
        self.email.setText("ERROR")
        self.email.setMaximumHeight(20)
        self.nickname.setText("ERROR")
        self.nickname.setMaximumHeight(20)
        self.dname.setText("ERROR")
        self.dname.setMaximumHeight(20)

    def getteamscontacts(self):
        self.work = loadcontacts()
        self.work.sig_error.connect(self.displaypopup)
        self.work.sig_success.connect(self.getlocalcontacts)
        self.work.start()
        self.open_Loading_dialog()

    def displaypopup(self, message):
        try:
            self.close_Loading_dialog()
            infoBox = QMessageBox()
            infoBox.setWindowTitle("TeamsExt")
            # infoBox.setIcon(QMessageBox.Warning)
            # infoBox.setText("Error")
            infoBox.setInformativeText(message)
            infoBox.setStandardButtons(QMessageBox.Ok)
            infoBox.setEscapeButton(QMessageBox.Close)
            infoBox.exec_()
            windows.append(infoBox)
        except Exception as e:
            print(e)

    def getlocalcontacts(self, message):
        self.close_Loading_dialog()
        if self.chck_groups.isChecked():
            result = db.select_all_contacts()
        else:
            result = db.select_groups_contacts()
        try:
            # table_model = ContactsTableModel(parent=myapp, mylist=result, header=contact_table_Headers)
            # self.contacts_table.setModel(table_model)
            self.model = QStandardItemModel(self.contacts_table)
            # self.contacts_table.itemChanged.connect(self.itemChanged)
            self.contacts_table.setModel(self.model)
            for value in result:
                row = []
                for i, item in enumerate(value):
                    if i == 1:
                        cell = QStandardItem()
                        cell.setCheckable(True)
                        cell.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                        cell.setData(QVariant(Qt.Checked), Qt.CheckStateRole)
                        if "no" in item:
                            cell.setCheckState(False)
                        else:
                            cell.setCheckState(True)
                    else:
                        cell = QStandardItem(item)
                        cell.setFlags(QtCore.Qt.ItemIsEnabled)

                    row.append(cell)
                self.model.appendRow(row)
            # item = QtGui.QStandardItem("Click me")
            # item.setCheckable(True)
            # self.contacts_table.appendRow(item)
            self.contacts_table.model().setHorizontalHeaderLabels(contact_table_Headers)
            self.contacts_table.setSortingEnabled(True)
            # self.contacts_table.setFocusPolicy(QtCore.Qt.NoFocus)
            header = self.contacts_table.horizontalHeader()
            header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
            header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
            header.sectionClicked.connect(self.sorttable)
            self.contacts_table.model().dataChanged.connect(self.contacts_table_changed)

            # self.contacts_table.doubleClicked.connect(self.updateselect)
        except Exception as e:
            print(e)

    def contacts_table_changed(self, tLeft, bRight):
        self.selected_fav = ""
        nbofrows = self.contacts_table.model().rowCount()
        nbofreceipt = 0
        if (nbofrows == 0):
            self.btn_send.setDisabled(True)
            return
        for i in range(nbofrows):
            # cell = QStandardItem(self.contacts_table.model().data(self.contacts_table.model().index(i, 1)))
            try:
                if self.contacts_table.model().item(i,
                                                    1).checkState() == QtCore.Qt.Checked or self.contacts_table.model().item(
                    i, 1).checkState() == QtCore.Qt.PartiallyChecked:
                    nbofreceipt += 1
            except Exception as e:
                print(e)
        if nbofreceipt == 0:
            self.btn_send.setDisabled(True)
            return
        if self.txt_msg.toPlainText() != "":
            self.btn_send.setDisabled(False)
        #     try:
        #         row = mi.row()
        #         column = mi.column()
        #         model = self.contacts_table.model()
        #         index = model.index(row, 1)
        #         selected = model.data(index)
        #         if "no" in selected:
        #            model.setData(index, "yes")
        #          #    self.contacts_table.item(row, 1).setText("Yes")
        #         else:
        #             model.setData(index, "no")
        #
        #     except Exception as e:
        #         print(e)

    def sorttable(self, index):
        if index == 1:
            nbofrows = self.contacts_table.model().rowCount()
            recipients = []
            if (nbofrows == 0):
                return
            for i in range(nbofrows):
                # cell = QStandardItem(self.contacts_table.model().data(self.contacts_table.model().index(i, 1)))
                try:
                    if self.contacts_table.model().item(i,
                                                        1).checkState() == QtCore.Qt.Checked or self.contacts_table.model().item(
                        i, 1).checkState() == QtCore.Qt.PartiallyChecked:
                        contact_name_index = self.contacts_table.model().index(i, 0)
                        rowItems = self.contacts_table.model().takeRow(contact_name_index.row())
                        self.contacts_table.model().insertRow(0, rowItems)
                except Exception as e:
                    print(e)

    def open_Loading_dialog(self):
        self.dialog.ui = loadingui()
        self.dialog.ui.setupUi(self.dialog)
        self.dialog.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.dialog.exec_()
        # self.dialog.show()

    def close_Loading_dialog(self):
        if self.dialog.isActiveWindow():
            self.dialog.accept()


def storerefreshcode(code):
    with shelve.open('config', 'c') as shelf:
        shelf['access_code'] = code


def retreiverefreshcode():
    with shelve.open('config', 'c') as shelf:
        if (shelf):
            access_code = shelf['access_code']
            return access_code


def storeauth(access_token):
    with shelve.open('config', 'c') as shelf:
        global stored_accesstoken
        stored_accesstoken = access_token
        reloadheaders()
        shelf['access_token'] = access_token


def retrieveauth():
    with shelve.open('config', 'c') as shelf:
        if (shelf):
            access_token = shelf['access_token']
            global stored_accesstoken
            stored_accesstoken = access_token
            reloadheaders()


def reloadheaders():
    global headers
    headers = {"Authorization": "Bearer " + stored_accesstoken,
               "Content-Type": "application/json; charset=utf-8"}


class Msg_templateclass(msg_template.Ui_MainWindow):
    def __init__(self, mainui, templateobj, msg):
        self.mainui = mainui
        self.TemplateObj = templateobj
        self.setupUi(self.TemplateObj)
        self.TemplateObj.show()
        self.msg = msg
        if (self.msg):
            self.loadmessages()
        else:
            self.TemplateObj.setWindowTitle("Favorites")
            self.loadfavorites()
        # self.table_template.dataChanged.connect(self.updatetable)

        # self.buttonBox.accepted.connect(self.accept)

    def select_template(self):
        try:
            button = self.qbutton_select.sender()
            index = self.table_template.indexAt(button.pos())
            msg = self.model.data(self.model.index(index.row(), 1))
            self.mainui.txt_msg.setPlainText(msg)
            self.TemplateObj.close()
        except Exception as e:
            print(e)

    def select_favorite(self):
        try:
            button = self.qbutton_select.sender()
            index = self.table_template.indexAt(button.pos())
            name = self.model.data(self.model.index(index.row(), 0))
            ids = db.get_all_favorites_by_name(name)
            ids_clean = []
            for id in ids:
                ids_clean.append(id[0])
            db.update_contact_selected(ids_clean)
            self.mainui.selected_fav = name;
            self.mainui.getlocalcontacts("Success")
            self.mainui.sorttable(1)
            self.TemplateObj.close()
        except Exception as e:
            print(e)

    def delete_msg_template(self):
        try:
            button = self.qbutton_remove.sender()
            index = self.table_template.indexAt(button.pos())
            msg_id = self.model.data(self.model.index(index.row(), 0))
            db.delete_msg_template_by_id(msg_id)
            # self.model.removeRow(index.row()) this caused the Qtoolrefrence to go so i had to make a work around which is reload the whole table
            self.loadmessages()
        except Exception as e:
            print(e)

    def dataChanged(self, index):
        msg = self.model.data(index)
        id = self.model.data(self.model.index(index.row(), 0))
        db.update_text(id, msg)

    def delete_favorite(self):
        try:
            button = self.qbutton_remove.sender()
            index = self.table_template.indexAt(button.pos())
            name = self.model.data(self.model.index(index.row(), 0))
            db.delete_favorite_by_id(name)
            # self.model.removeRow(index.row()) this caused the Qtoolrefrence to go so i had to make a work around which is reload the whole table
            self.loadfavorites()
        except Exception as e:
            print(e)

    def loadmessages(self):

        try:
            result = db.get_all_msg_templates()
            # print(result)
            self.model = QStandardItemModel(self.table_template)
            # self.contacts_table.itemChanged.connect(self.itemChanged)
            self.table_template.setModel(self.model)
            for idx, value in enumerate(result):
                row1 = []
                # print(value)
                # for i,item in enumerate(value):
                #     cell = QStandardItem(str(item))
                #     if i == 0:
                #         cell.setFlags(QtCore.Qt.ItemIsEnabled)
                #     row1.append(cell)
                cell = QStandardItem(str(value[0]))
                cell.setFlags(QtCore.Qt.ItemIsEnabled)
                row1.append(cell)
                cell = QStandardItem(str(value[1]))
                row1.append(cell)
                cell = QStandardItem()
                row1.append(cell)
                cell = QStandardItem()
                row1.append(cell)
                self.model.appendRow(row1)
                self.qbutton_select = QtWidgets.QToolButton()
                self.qbutton_select.setIcon(QtGui.QIcon("imgs/select.png"))
                self.qbutton_select.clicked.connect(self.select_template)
                self.table_template.setIndexWidget(self.model.index(idx, 2), self.qbutton_select)
                self.qbutton_remove = QtWidgets.QToolButton()
                self.qbutton_remove.setIcon(QtGui.QIcon("imgs/remove.png"))
                self.qbutton_remove.clicked.connect(self.delete_msg_template)
                self.table_template.setIndexWidget(self.model.index(idx, 3), self.qbutton_remove)
            # item = QtGui.QStandardItem("Click me")
            # item.setCheckable(True)
            # self.contacts_table.appendRow(item)
            header = self.table_template.horizontalHeader()
            if self.table_template.model().rowCount() != 0:
                header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
                header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
                header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
                header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
            self.model.dataChanged.connect(self.dataChanged)
            # self.table_template.doubleClicked.connect(self.select_template)
            self.table_template.setWordWrap(True)
            self.table_template.resizeRowsToContents()
            self.table_template.model().setHorizontalHeaderLabels(message_templates_table_header)
            self.table_template.setColumnHidden(0, True)
        except Exception as e:
            print(e)

    def loadfavorites(self):
        all_favorites = db.get_all_favorites()
        contacts_list = []
        contacts_names = []

        for i in range(len(all_favorites)):
            # contacts_name.append(db.get_contact_name_from_id())
            if i != 0 and all_favorites[i - 1][0] != all_favorites[i][0]:
                contacts_list.append(contacts_names)
                contacts_names = []
                contact_temp = [db.get_contact_name_from_id(all_favorites[i][1])[0][0], all_favorites[i][0]]
                contacts_names.append(contact_temp)
            else:
                contact_temp = [db.get_contact_name_from_id(all_favorites[i][1])[0][0], all_favorites[i][0]]
                contacts_names.append(contact_temp)

            if i == len(all_favorites) - 1:
                contacts_list.append(contacts_names)
        self.model = QStandardItemModel(self.table_template)
        # self.contacts_table.itemChanged.connect(self.itemChanged)
        self.table_template.setModel(self.model)
        last_contact = []
        for contacts in contacts_list:
            contacts_str = ""
            for idx, contact in enumerate(contacts):
                if (len(contacts)) == 0:
                    contacts_str += contact[0]
                elif (len(contacts)) - 1 == idx:
                    contacts_str += contact[0]
                else:
                    contacts_str += contact[0] + ", "

            contacts_temp = [contacts[0][1], contacts_str]
            last_contact.append(contacts_temp)
        for idx, value in enumerate(last_contact):
            row1 = []
            # print(value)
            # for i,item in enumerate(value):
            #     cell = QStandardItem(str(item))
            #     if i == 0:
            #         cell.setFlags(QtCore.Qt.ItemIsEnabled)
            #     row1.append(cell)
            cell = QStandardItem(str(value[0]))
            cell.setFlags(QtCore.Qt.ItemIsEnabled)
            row1.append(cell)
            cell = QStandardItem(str(value[1]))
            cell.setFlags(QtCore.Qt.ItemIsEnabled)
            row1.append(cell)
            cell = QStandardItem()
            row1.append(cell)
            cell = QStandardItem()
            row1.append(cell)
            self.model.appendRow(row1)
            self.qbutton_select = QtWidgets.QToolButton()
            self.qbutton_select.setIcon(QtGui.QIcon("imgs/select.png"))
            self.qbutton_select.clicked.connect(self.select_favorite)
            self.table_template.setIndexWidget(self.model.index(idx, 2), self.qbutton_select)
            self.qbutton_remove = QtWidgets.QToolButton()
            self.qbutton_remove.setIcon(QtGui.QIcon("imgs/remove.png"))
            self.qbutton_remove.clicked.connect(self.delete_favorite)
            self.table_template.setIndexWidget(self.model.index(idx, 3), self.qbutton_remove)
        # item = QtGui.QStandardItem("Click me")
        # item.setCheckable(True)
        # self.contacts_table.appendRow(item)
        header = self.table_template.horizontalHeader()
        if self.table_template.model().rowCount() != 0:
            header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
            header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        # self.table_template.doubleClicked.connect(self.select_template)
        self.table_template.setWordWrap(True)
        self.table_template.resizeRowsToContents()
        self.table_template.model().setHorizontalHeaderLabels(favorites_table_header)


class Authdialog(adiag.Ui_Dialog):

    def __init__(self, mainui, dialogobj, is_auth=True, recept=None):
        self.mainui = mainui
        self.DialogObj = dialogobj
        self.is_auth = is_auth
        self.recept = recept
        self.setupUi(self.DialogObj)
        self.DialogObj.show()
        if not is_auth:
            self.label.setText("Enter email addresses, one per line:")
            self.buttonBox.accepted.connect(self.accept_mails)
            self.DialogObj.setWindowTitle("Add To Group")

        else:
            self.DialogObj.setWindowTitle("Authentication")
            self.buttonBox.accepted.connect(self.accept)

    def accept_mails(self):
        self.emails = self.txt_access.toPlainText()
        if str(self.emails) != "":
            self.work = add_to_groups(emails=self.emails, rooms=self.recept)
            # self.work.sig_error_add.connect(self.add_result)
            self.work.sig_success_add.connect(self.add_result)
            self.work.start()
            self.mainui.open_Loading_dialog()

    def add_result(self, message, failed_nb):
        self.mainui.close_Loading_dialog()
        emails = self.emails.split("\n")
        success_nb = (len(emails) * len(self.recept)) - failed_nb
        log_message = str(success_nb) + "/" + str(len(emails) * len(self.recept)) + " Users were added"
        # for idx,space in enumerate(self.recept):
        #     if idx == len(self.recept)-1:
        #         log_message += space[1]
        #     else:
        #         log_message += space[1]+", "
        idsonly = [x[0] for x in self.recept]
        inserted_nb = db.insert_log(idsonly, log_message)
        self.mainui.load_log_table("success")
        if message != "success":
            self.mainui.displaypopup(message)
            # self.popup_message(message)

    def accept(self):
        accesstoken = self.txt_access.toPlainText()
        if str(accesstoken) != "":
            # print(accesstoken)
            try:
                global stored_accesstoken
                stored_accesstoken = accesstoken
                reloadheaders()
                self.mainui.loadinguser()
                self.work = getuserdetail(access_token=accesstoken)
                self.work.sig_error.connect(self.popup_message)
                self.work.sig_success.connect(self.updateuser)
                self.work.start()
            except Exception as e:
                print(e)

    def popup_message(self, message):
        self.mainui.erroruser()
        infoBox = QMessageBox()
        infoBox.setIcon(QMessageBox.Warning)
        infoBox.setText("Error")
        infoBox.setWindowTitle("Error")
        infoBox.setInformativeText(message)
        infoBox.setStandardButtons(QMessageBox.Ok)
        infoBox.setEscapeButton(QMessageBox.Close)
        infoBox.exec_()
        windows.append(infoBox)

    def updateuser(self, message):
        print(message)
        self.mainui.setupuserinfo()


class getuserdetail(QtCore.QThread):
    sig_error = pyqtSignal(str)
    sig_success = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        QThread.__init__(self)
        # self.signal = QtCore.SIGNAL("signal")
        self.Init(*args, **kwargs)

    def Init(self, access_token, is_token=True):
        self.access_token = access_token
        self.is_token = is_token

    def run(self):
        access_resp = "errors"
        json_response = "errors"
        try:
            if not self.is_token:
                code_headers = {"Content-Type": "application/x-www-form-urlencoded; charset=utf-8"}
                # YOU NEED TO CREATE YOUR OWN CLIENT ID AND CLIENT SECRET!!!!!!!!!!!!!!!!!!!!!!
                params = {'code': self.access_token, 'grant_type': 'authorization_code', 'client_id': app_cfg.client_id,
                          'client_secret': app_cfg.client_secret, 'redirect_uri': redirect_url}
                access_request = requests.post("https://api.ciscospark.com/v1/access_token", params=params,
                                               headers=code_headers, verify=False)
                access_resp = access_request.json()
                if 'errors' in access_resp:
                    error_message = access_resp.get("errors")[0].get('description')
                    # print(error_message)
                    self.sig_error.emit(error_message)
                    return
                else:
                    storeauth(access_resp['access_token'])
                    storerefreshcode(access_resp['refresh_token'])
            resp = requests.get("https://api.ciscospark.com/v1/people/me", headers=headers, verify=False)
            json_response = resp.json()
        except Exception as e:
            print(e)
        # print(json_response['errors'])
        if 'errors' in json_response:
            error_message = json_response.get("errors")[0].get('description')
            # print(error_message)
            self.sig_error.emit(error_message)
        else:
            db.clear_all_users()
            photoname = '00000001.jpg'
            f = open(photoname, 'wb')
            with urllib.request.urlopen(json_response['avatar']) as url:
                picture = url.read()
            f.write(picture)
            f.close()
            global current_user
            current_user = user.user_info(id="new", email=json_response['emails'][0],
                                          displayname=json_response['displayName'],
                                          nickname=json_response['nickName'], avatar=photoname)
            last_id = db.insert_user_info(current_user)
            current_user.id = last_id
            if self.is_token:
                storeauth(access_token=self.access_token)
            self.sig_success.emit("success")
        # print(last_id)

        # self.completed.emit("hello")
        # gentable(self)


class refresh_token(QtCore.QThread):
    sig_error = pyqtSignal(str)
    sig_success = pyqtSignal()

    def __init__(self, *args, **kwargs):
        QThread.__init__(self)
        # self.signal = QtCore.SIGNAL("signal")

    def run(self):
        access_resp = "errors"
        json_response = "errors"
        try:
            # YOU NEED TO CREATE YOUR OWN CLIENT ID AND CLIENT SECRET!!!!!!!!!!!!!!!!!!!!!!
            code_headers = {"Content-Type": "application/x-www-form-urlencoded; charset=utf-8"}
            params = {'refresh_token': retreiverefreshcode(), 'grant_type': 'refresh_token',
                      'client_id': app_cfg.client_id,
                      'client_secret': app_cfg.client_secret}
            access_request = requests.post("https://api.ciscospark.com/v1/access_token", params=params,
                                           headers=code_headers, verify=False)
            access_resp = access_request.json()
            if 'errors' in access_resp:
                error_message = access_resp.get("errors")[0].get('description')
                # print(error_message)
                self.sig_error.emit(error_message)
                return
            else:
                storeauth(access_resp['access_token'])
            resp = requests.get("https://api.ciscospark.com/v1/people/me", headers=headers, verify=False)
            json_response = resp.json()
        except Exception as e:
            self.sig_error.emit(str(e))
        # print(json_response['errors'])
        if 'errors' in json_response:
            error_message = json_response.get("errors")[0].get('description')
            # print(error_message)
            self.sig_error.emit(error_message)
        else:
            db.clear_all_users()
            photoname = '00000001.jpg'
            f = open(photoname, 'wb')
            with urllib.request.urlopen(json_response['avatar']) as url:
                picture = url.read()
            f.write(picture)
            f.close()
            global current_user
            current_user = user.user_info(id="new", email=json_response['emails'][0],
                                          displayname=json_response['displayName'],
                                          nickname=json_response['nickName'], avatar=photoname)
            last_id = db.insert_user_info(current_user)
            current_user.id = last_id
            self.sig_success.emit()
        # print(last_id)

        # self.completed.emit("hello")
        # gentable(self)


class sendmessages(QtCore.QThread):
    sig_error = pyqtSignal(str)
    sig_success = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        QThread.__init__(self)
        # self.signal = QtCore.SIGNAL("signal")
        self.Init(*args, **kwargs)

    def Init(self, ids, message, messageid):
        self.ids = ids
        self.message = message
        self.messageid = messageid

    def run(self):
        try:
            for id in self.ids:
                #    print(id, self.message)
                data = {'roomId': id, "markdown": self.message}
                request = "https://api.ciscospark.com/v1/messages"
                resp = requests.post(url=request, json=data, headers=headers, verify=False)
                json_response = resp.json()
                # print(json_response['errors'])
                if 'errors' in json_response:
                    error_message = json_response.get("errors")[0].get('description')
                    db.updatetable(self.messageid, "ERROR: " + error_message)
                    self.sig_error.emit(error_message)
                else:
                    db.updatetable(self.messageid, self.message)
                    db.update_contact_selected(self.ids)
                    self.sig_success.emit("success")
        except Exception as e:
            print(e)
    # print(last_id)

    # self.completed.emit("hello")
    # gentable(self)


class add_to_groups(QtCore.QThread):
    # sig_error_add = pyqtSignal(str)
    sig_success_add = pyqtSignal(str, int)

    def __init__(self, *args, **kwargs):
        QThread.__init__(self)
        # self.signal = QtCore.SIGNAL("signal")
        self.Init(*args, **kwargs)

    def Init(self, emails, rooms):
        self.emails = emails
        self.rooms = rooms

    def run(self):
        message = "success"
        error_found = False
        error_message = ""
        failed_nb = 0
        try:
            self.emails = self.emails.split("\n")
            for roomDetails in self.rooms:
                for email in self.emails:
                    if email != "":
                        body_json = {
                            "roomId": roomDetails[0],
                            "personEmail": email.strip(),
                        }
                        resp = requests.post("https://api.ciscospark.com/v1/memberships",
                                             json.dumps(body_json), headers=headers, verify=False)
                        json_resp = resp.json()
                        if 'errors' in json_resp:
                            error_found = True
                            failed_nb += 1
                            error_message += json_resp.get("errors")[0].get('description') + " Room: " + roomDetails[
                                1] + " (" + email.strip() + ")" + "\n"
                            # print(error_message)
                            # self.sig_error.emit(error_message)

        except Exception as e:
            self.sig_success_add.emit(e, failed_nb)
        # print(json_response['errors'])
        if error_found:
            message = "Finished Successfully, but there were some errors!\n"
            message += error_message
        self.sig_success_add.emit(message, failed_nb)

        # print(last_id)

        # self.completed.emit("hello")
        # gentable(self)


class loadcontacts(QtCore.QThread):
    access_token = ""

    sig_error = pyqtSignal(str)
    sig_success = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        QThread.__init__(self)
        # self.signal = QtCore.SIGNAL("signal")

    def run(self):
        try:
            resp = requests.get("https://api.ciscospark.com/v1/rooms?type=direct", headers=headers, verify=False)
            all_response = resp.json()
            resp = requests.get("https://api.ciscospark.com/v1/rooms?type=group", headers=headers, verify=False)
            group_response = resp.json()
        except Exception as e:
            print(e)
        # print(json_response['errors'])
        if 'errors' in all_response or 'errors' in group_response:
            error_message = all_response.get("errors")[0].get('description')
            # print(error_message)
            self.sig_error.emit(error_message)
        else:
            # print(json_response)
            db.clear_all_contacts()
            for contact in all_response['items']:
                contact_import = ctct.contact(id=contact['id'], title=contact['title'], selected="no",
                                              type=contact['type'])
                db.insert_contact(contact_import)

            for contact in group_response['items']:
                contact_import = ctct.contact(id=contact['id'], title=contact['title'], selected="no",
                                              type=contact['type'])
                db.insert_contact(contact_import)

            self.sig_success.emit("success")

        # print(last_id)

        # self.completed.emit("hello")
        # gentable(self)


if __name__ == "__main__":
    myapp = QtWidgets.QApplication(sys.argv)
    MainWIndow = QtWidgets.QMainWindow()
    ui = extendmain(MainWIndow)
    # crMainWindow=QtGui.QMainWindow()
    # crKeys=crkeyExt(crMainWindow)
    # app = QtGui.QApplication(sys.argv)
    # MainWindow = QtGui.QMainWindow()
    # ui = Ui_MainWindow()
    # ui.setupUi(MainWindow)
    # MainWindow.show()
    sys.exit(myapp.exec_())
