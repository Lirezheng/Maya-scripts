import pprint

from maya import cmds

import pyGUI
import imp
imp.reload(pyGUI)

from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui


class ControllerLibraryUI(QtWidgets.QDialog):

    def __init__(self):
        #初始化所有父类的部分
        super(ControllerLibraryUI, self).__init__()

        self.setWindowTitle('MyUI')
        self.library = pyGUI.ControllerLibrary()
        self.buildUI()
        self.populate()

    def buildUI(self):
        layout = QtWidgets.QVBoxLayout(self)

        saveWidget = QtWidgets.QWidget()
        saveLayout = QtWidgets.QHBoxLayout(saveWidget)
        layout.addWidget(saveWidget)

        self.saveNameField = QtWidgets.QLineEdit()
        saveBtn = QtWidgets.QPushButton('Save')
        saveBtn.clicked.connect(self.save)
        saveLayout.addWidget(self.saveNameField)
        saveLayout.addWidget(saveBtn)

        size = 64
        buffer = 12
        self.listWidget = QtWidgets.QListWidget()
        self.listWidget.setViewMode((QtWidgets.QListWidget.IconMode))
        self.listWidget.setIconSize(QtCore.QSize(size,size))
        self.listWidget.setResizeMode(QtWidgets.QListWidget.Adjust)
        self.listWidget.setGridSize(QtCore.QSize(size+buffer,size+buffer))
        layout.addWidget(self.listWidget)

        btnWidget = QtWidgets.QWidget()
        btnLayout = QtWidgets.QHBoxLayout(btnWidget)
        layout.addWidget(btnWidget)

        importBtn = QtWidgets.QPushButton('import')
        refreshBtn = QtWidgets.QPushButton('refresh')
        closeBtn = QtWidgets.QPushButton('close')
        importBtn.clicked.connect(self.load)
        refreshBtn.clicked.connect(self.populate)
        closeBtn.clicked.connect(self.close)

        btnLayout.addWidget(importBtn)
        btnLayout.addWidget(refreshBtn)
        btnLayout.addWidget(closeBtn)

    def populate(self):
        self.listWidget.clear()
       #由于library继承自字典，所以他有items()方法，返回可遍历的键值元组
        self.library.find()

        for name,info in self.library.items():
            item = QtWidgets.QListWidgetItem(name)
            self.listWidget.addItem(item)

            #在List中放入文件的缩率图
            screenshot = info.get('screenshot')
            #找到路径
            if screenshot:
                icon = QtGui.QIcon(screenshot)
                item.setIcon(icon)
            item.setToolTip(pprint.pformat(info))

    def load(self):
        currentItem = self.listWidget.currentItem()
        if not currentItem:
            return
        else:
            name = currentItem.text()
            self.library.load(name)
    def save(self):
        name = self.saveNameField.text()

        #移除开头和结尾的空格，判断是否为空
        if not name.strip():
            cmds.warning("must give a name")

        self.library.save(name)
        self.populate()
        self.saveNameField.setText('')
ui = ControllerLibraryUI()
ui.show()

