import shelve
import urllib as urllib

from PyQt5.QtCore import pyqtSignal, QThread, QAbstractTableModel, Qt
from PyQt5.QtGui import QPixmap, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QMessageBox
from Loadingdialog import Ui_Dialog as loadingui
import Messagestemplate as msg_template
from aiohttp.web_response import json_response

import Mainwindow as maingui
import AuthDialog as adiag
from PyQt5 import QtWidgets, QtCore, QtGui
import sys

import json
import requests
import user_info as user
import dbhelper as db
import contact as ctct

stored_accesstoken = ""

headers = {"Authorization": "Bearer " + stored_accesstoken,
           "Content-Type": "application/json; charset=utf-8"}

windows = []

current_user = ""

contact_table_Headers = ["Title", "Select", "Type"]
log_table_headers = ["Contacts", "Date", "Messsage"]


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
        self.dialog = QtWidgets.QDialog()
        self.windowObj = windowObj
        self.setupUi(self.windowObj)
        self.windowObj.show()
        # self.authchange.clicked.connect(self.getuserinfo)
        self.setupuserinfo()
        self.actionSetup_Access_Token.triggered.connect(self.getuserinfo)
        self.getlocalcontacts("success")
        self.refreshcontact.clicked.connect(self.getteamscontacts)
        self.chck_groups.toggled.connect(self.getlocalcontacts)
        self.btn_templates.clicked.connect(self.getmessagetemplate)
        self.btn_savetemplate.clicked.connect(self.savetemplate)
        self.btn_send.clicked.connect(self.send_msg)
        self.btn_bold.clicked.connect(self.boldselection)
        self.btn_italic.clicked.connect(self.italicselection)
        self.txt_msg.setPlaceholderText("Enter Your Message")
        # self.action_About.triggered.connect(lambda: self.displaypopup('fooData'))
        self.action_About.triggered.connect(lambda: self.displaypopup("Thank you for using this tool, it was created "
                                                                      "by me (Ziad Kiwan) as an individual contribution, and does not have"
                                                                      " any link to Cisco.\nif you have any problems or suggetions please contact me on my email: ziad_kiwan_1992@hotmail.com \nThank you! "))
        self.load_log_table("success")
        retrieveauth()
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
        messageid = db.insert_log(recipients, "Sending.....")
        self.load_log_table("success")
        self.work = sendmessages(ids=recipients, message=message, messageid=messageid)
        self.work.sig_error.connect(self.load_log_table)
        self.work.sig_success.connect(self.load_log_table)
        self.work.start()

    def load_log_table(self, message):
        result = db.load_log()
        self.model = QStandardItemModel(self.contacts_table)
        # self.contacts_table.itemChanged.connect(self.itemChanged)
        self.table_log.setModel(self.model)
        for value in result:
            row = []
            for item in value:
                cell = QStandardItem(item)
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
        # self.contacts_table.doubleClicked.connect(self.updateselect)

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
        MessagestemplateUI = Msg_templateclass(mainui=self, templateobj=Messagestemplatewindow)
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
                i = 0
                for item in value:
                    if i == 1:
                        cell = QStandardItem()
                        cell.setCheckable(True)
                        if "no" in item:
                            cell.setCheckState(False)
                        else:
                            cell.setCheckState(True)
                    else:
                        cell = QStandardItem(item)
                        cell.setFlags(QtCore.Qt.ItemIsEnabled)

                    row.append(cell)
                    i += 1
                self.model.appendRow(row)
            # item = QtGui.QStandardItem("Click me")
            # item.setCheckable(True)
            # self.contacts_table.appendRow(item)
            self.contacts_table.model().setHorizontalHeaderLabels(contact_table_Headers)
            header = self.contacts_table.horizontalHeader()
            header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
            header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
            # self.contacts_table.doubleClicked.connect(self.updateselect)
        except Exception as e:
            print(e)

    # def updateselect(self, mi):
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

    def open_Loading_dialog(self):
        self.dialog.ui = loadingui()
        self.dialog.ui.setupUi(self.dialog)
        self.dialog.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.dialog.exec_()
        # self.dialog.show()

    def close_Loading_dialog(self):
        if self.dialog.isActiveWindow():
            self.dialog.accept()


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
    def __init__(self, mainui, templateobj):
        self.mainui = mainui
        self.TemplateObj = templateobj
        self.setupUi(self.TemplateObj)
        self.TemplateObj.show()
        self.loadmessages()
        # self.table_template.dataChanged.connect(self.updatetable)
        self.model.dataChanged.connect(self.dataChanged)
        self.table_template.doubleClicked.connect(self.select_template)
        self.table_template.setWordWrap(True)
        self.table_template.resizeRowsToContents()
        # self.buttonBox.accepted.connect(self.accept)

    def select_template(self, index):
        msg = self.model.data(self.model.index(index.row(), 1))
        self.mainui.txt_msg.setPlainText(msg)
        self.TemplateObj.close()

    def dataChanged(self, index):
        msg = self.model.data(index)
        id = self.model.data(self.model.index(index.row(), 0))
        db.update_text(id, msg)

    def loadmessages(self):
        try:
            result = db.get_all_msg_templates()
            # print(result)
            self.model = QStandardItemModel(self.table_template)
            # self.contacts_table.itemChanged.connect(self.itemChanged)
            self.table_template.setModel(self.model)
            for value in result:
                row1 = []
                # print(value)
                i = 0
                for item in value:
                    cell = QStandardItem(str(item))
                    if i == 0:
                        cell.setFlags(QtCore.Qt.ItemIsEnabled)
                    row1.append(cell)
                    i += 1
                self.model.appendRow(row1)

            # item = QtGui.QStandardItem("Click me")
            # item.setCheckable(True)
            # self.contacts_table.appendRow(item)
            header = self.table_template.horizontalHeader()
            if self.table_template.model().rowCount() != 0:
                header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
                header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        except Exception as e:
            print(e)


class Authdialog(adiag.Ui_Dialog):

    def __init__(self, mainui, dialogobj):
        self.mainui = mainui
        self.DialogObj = dialogobj
        self.setupUi(self.DialogObj)
        self.DialogObj.show()
        self.buttonBox.accepted.connect(self.accept)

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
    access_token = ""
    sig_error = pyqtSignal(str)
    sig_success = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        QThread.__init__(self)
        # self.signal = QtCore.SIGNAL("signal")
        self.Init(*args, **kwargs)

    def Init(self, access_token):
        self.access_token = access_token

    def run(self):
        try:
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
            storeauth(access_token=self.access_token)
            self.sig_success.emit("success")
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


class loadcontacts(QtCore.QThread):
    access_token = ""

    sig_error = pyqtSignal(str)
    sig_success = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        QThread.__init__(self)
        # self.signal = QtCore.SIGNAL("signal")

    def run(self):
        try:
            resp = requests.get("https://api.ciscospark.com/v1/rooms", headers=headers, verify=False)
            json_response = resp.json()
        except Exception as e:
            print(e)
        # print(json_response['errors'])
        if 'errors' in json_response:
            error_message = json_response.get("errors")[0].get('description')
            # print(error_message)
            self.sig_error.emit(error_message)
        else:
            # print(json_response)
            for contact in json_response['items']:
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
