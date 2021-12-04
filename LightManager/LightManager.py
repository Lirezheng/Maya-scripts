import os,time
import pymel.core as pm
from functools import partial
from PySide2 import QtGui, QtWidgets,QtCore
from PySide2.QtCore import Signal
from shiboken2 import wrapInstance
from maya import OpenMayaUI as omui
import json,logging

#灯光类型
lightTypes = {
    'pointLight':partial(pm.shadingNode,'pointLight',asLight = True),
    'spotLight':partial(pm.shadingNode,'pointLight',asLight = True),
    'directionalLight':partial(pm.shadingNode,'directionalLight',asLight = True),
    'ambientLight':partial(pm.shadingNode,'ambientLight',asLight = True),
    'areaLight': partial(pm.shadingNode,'areaLight',asLight = True),
    'volumeLight': partial(pm.shadingNode,'volumeLight',asLight = True)

}
#该函数用于返回maya主窗口包装的控件
def getMayaWin():
    win = omui.MQtUtil_mainWindow()
    ptr = wrapInstance(int(win),QtWidgets.QMainWindow)
    return ptr

#该函数用于获取dock包装控件
def getDock(name='lightManagerDock'):
    deleteDock(name)
    ctrl = pm.workspaceControl(name,dockToMainWindow=('right',0),label = 'light Manager')
    qtCtrl = omui.MQtUtil_findControl(ctrl)
    ptr = wrapInstance(int(qtCtrl),QtWidgets.QWidget)
    return ptr

#该函数用于删除dock
def deleteDock(name='lightManagerDock'):
    if pm.workspaceControl(name,query=True,exists =True):
        pm.deleteUI(name)



#灯光管理器
#该管理器可以创建和显示指定灯光，为选中的灯光进行分组，
#可方便地设置灯光的各种属性，并能保存指定灯光到json文件，也可以导入灯光json文件到场景中。
class lightManager(QtWidgets.QWidget):
    #是否需要Dock，可以手动设置
    def __init__(self,dock = True):

        if dock:
            #需要设置Dock，获取Dock包装成的控件
            parent = getDock()
            print("dock执行")
        else:
            print("普通执行")

            #不需要，删除Dock,设置父母为QDialog(Qwidget的子类),且其祖宗为Maya窗口
            try:
                deleteDock()
                print("运行成功")
            except:
                raise RuntimeError("初始化错误")
            finally:
                parent = QtWidgets.QDialog(parent = getMayaWin())
                #设置该Dialog的名字
                parent.setObjectName('light Manager')
                parent.setWindowTitle('lightManager')
                layout = QtWidgets.QVBoxLayout(parent)



        super(lightManager, self).__init__(parent = parent)


        self.buildUI()
        self.loadOrignLight()

        #如果dock为True，显然该dock为插件的父母；若dock为False，控件的父母为QDialog窗口
        self.parent().layout().addWidget(self)
        if not dock:
            parent.show()


    #该函数用于创建基本UI
    def buildUI(self):
        layout = QtWidgets.QGridLayout(self)

        #向ComboBox增加灯光项
        self.lightTypeCB = QtWidgets.QComboBox()
        for lightType in sorted(lightTypes):
            self.lightTypeCB.addItem(lightType,0,0)

        layout.addWidget(self.lightTypeCB, 0,0,2,2)

        #用于创建灯光
        createBtn = QtWidgets.QPushButton('创建')
        createBtn.clicked.connect(self.loadLight)
        layout.addWidget(createBtn,0,2)

        #用于指定灯光类型显示
        selectSameBtn = QtWidgets.QPushButton('指定类型显示')
        selectSameBtn.clicked.connect(self.showSelectedType)
        layout.addWidget(selectSameBtn,1,2)

        #用于输入组命名
        self.groupNameEditor = QtWidgets.QLineEdit()
        self.groupNameEditor.setPlaceholderText('此处输入组命名')
        self.groupNameEditor.textChanged.connect(self.changeEditName)

        #用于创建灯光组
        createGroupBtn = QtWidgets.QPushButton('选中分组')
        createGroupBtn.clicked.connect(self.addGroup)
        layout.addWidget(self.groupNameEditor,2,0,1,2)
        layout.addWidget(createGroupBtn,2,2)

        #再次创建一个垂直的布局，且该布局有个父类窗口
        scrollWidget = QtWidgets.QWidget() #未嵌入父类QWidget为窗口
        scrollWidget.setSizePolicy(QtWidgets.QSizePolicy.Maximum,QtWidgets.QSizePolicy.Maximum)
        self.scrollLayout = QtWidgets.QVBoxLayout(scrollWidget)

        #创建一个滚动区域
        scrollArea = QtWidgets.QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollArea.setWidget(scrollWidget)
        layout.addWidget(scrollArea,3,0,1,3)

        #用于保存功能
        saveBtn = QtWidgets.QPushButton('保存')
        saveBtn.setMaximumSize(70,50)
        saveBtn.clicked.connect(self.saveLight)
        layout.addWidget(saveBtn, 4, 0)

        #用于刷新，获得当前场景所有灯光
        refreshBtn = QtWidgets.QPushButton('刷新')
        refreshBtn.clicked.connect(self.loadOrignLight)
        layout.addWidget(refreshBtn, 4, 1)

        #用于导入json文件
        importBtn = QtWidgets.QPushButton('导入')
        importBtn.setMaximumSize(70, 50)
        importBtn.clicked.connect(self.importLight)
        layout.addWidget(importBtn, 4, 2)

    #该函数用于将选定灯光分成指定命名组
    def addGroup(self):
        try:
            pm.ungroup(self.groupName)
        except:
            logging.info('组名为新名字')
        finally:
            lightWidgets = self.findChildren(lightWidget)
            nameList = []

            for widget in lightWidgets:
                if widget.name.isChecked():
                    nameList.append(str(widget.light.getTransform()))
                    logging.info("oh %s被分到%s组" % (str(widget.light.getTransform()), self.groupName))
            print(self.groupName)
            pm.group(*nameList,n = self.groupName)

    #该函数用于获得编辑line中输入的字符
    def changeEditName(self):
        self.groupName = self.groupNameEditor.text()

    #该函数用于指定类型显示
    def showSelectedType(self):
        while self.scrollLayout.count():
            # takeAT会帮助widget设置parent为None
            widget = self.scrollLayout.takeAt(0).widget()
            if widget:
                widget.setVisible(True)
                widget.deleteLater()

        allLight = pm.ls(type='light')
        for light in allLight:
            if pm.objectType(light) == self.lightTypeCB.currentText():
                self.createLight(light)

    #该函数用于存储灯光属性到json文件中
    def saveLight(self):
        properties = {}

        lightWidgets = self.findChildren(lightWidget)
        for widget in lightWidgets:
            if widget.name.isChecked():
                light = widget.light
                transform = light.getTransform()
                properties[str(transform)] = {
                    'lightType':pm.objectType(light),
                    'translate':list(transform.translate.get()),
                    'rotation':list(transform.rotate.get()),
                    'scale':transform.getScale(),
                    'color':list(light.getColor()),
                    'intensity':light.getIntensity()
                }
        directory = self.getDirectory()
        lightFile = os.path.join(directory,'lightFile_%s.json'% time.strftime('%m-%d'))

        with open(lightFile,'w') as f :
            json.dump(properties,f,indent=4)
        logging.info("saving file success to %s" % lightFile)

    #该函数用于获得内部路径
    def getDirectory(self):
        directory = os.path.join(pm.internalVar(userAppDir=True), 'lightManager')
        if not os.path.exists(directory):
            os.mkdir(directory)
        return directory

    #该函数用于导入灯光，使用json中的属性创建灯光
    def importLight(self):
        directory = self.getDirectory()
        fileName = QtWidgets.QFileDialog.getOpenFileName(self,"Light Browser",directory)
        with open(fileName[0], 'r') as r:
            properties = json.load(r)

        for name,pair in properties.items():
            typeValue= pair.get('lightType')
            for typename,hint in lightTypes.items():
                if (typename) == typeValue:
                    break
            else:
                logging.info("error lightType %s  caused:%s" %(typeValue,name))
                continue

            #设置灯光的属性
            light = self.loadLight(lightType=typeValue)
            trans = light.getTransform()
            light.setColor(pair.get('color'))
            light.setIntensity(pair.get('intensity'))
            trans.setTranslation(pair.get("translate"))
            trans.setScale(pair.get("scale"))
            trans.setRotation(pair.get("rotation"))

        #导入后，更新所有灯光
        self.loadOrignLight()

    #该函数用于子控件的仅选中功能
    def onSolo(self,value):
        #寻找所有lightWidget控件
        lightWidgets = self.findChildren(lightWidget)
        for widget in lightWidgets:
            if widget != self.sender():
                widget.disableLight(value)

    #该函数用于加载场景中的灯光
    def loadOrignLight(self):
        while self.scrollLayout.count():
            #takeAT会帮助widget设置parent为None
            widget = self.scrollLayout.takeAt(0).widget()
            if widget:
                widget.setVisible(True)
                widget.deleteLater()

        allLight = pm.ls(type='light')
        for light in allLight:
            self.createLight(light)

    #该函数用于从选项中添加灯光，或导入时添加灯光
    def loadLight(self,lightType = None,add=True):
        if  lightType == None:
            lightType = self.lightTypeCB.currentText()
        func = lightTypes[lightType]
        light = func()
        if add:
            self.createLight(light)
        return light

    #该函数用于添加灯光控件
    def createLight(self,light):

        widget = lightWidget(light)
        self.scrollLayout.addWidget(widget)
        #控件信号，发出信号会触发Manager的函数onSolo
        widget.onSolo.connect(self.onSolo)


#子控件灯光widget
class lightWidget(QtWidgets.QDialog):
    onSolo = QtCore.Signal(bool)
    def __init__(self,light):
        super(lightWidget, self).__init__()

        #得到灯光的shape型节点
        if isinstance(light,str):
            light = pm.PyNode(light)
        if isinstance(light,pm.nodetypes.Transform):
            light = light.getShape()

        self.light = light
        self.buildUI()

    def buildUI(self):
        #scorll部分用网格布局和checkBox
        layout = QtWidgets.QGridLayout(self)
        self.name = QtWidgets.QCheckBox(str(self.light.getTransform()))
        self.name.setChecked(self.light.getTransform().visibility.get())
        #可见性勾选
        self.name.toggled.connect(lambda val:self.light.getTransform().visibility.set(val))
        layout.addWidget(self.name,0,0)

        #删除灯光
        deleteBtn = QtWidgets.QPushButton('X')
        deleteBtn.setMaximumSize(35,35)
        deleteBtn.clicked.connect(self.deleteLight)
        layout.addWidget(deleteBtn,0,2)

        #强度滑动条
        slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        slider.setValue(self.light.getIntensity())
        slider.setMaximum(10)
        slider.setMinimum(1)
        slider.valueChanged.connect(lambda val:self.light.setIntensity(val))
        layout.addWidget(slider)

        #单独选中
        onlyChoseBtn = QtWidgets.QPushButton('仅选中')
        onlyChoseBtn.setMaximumSize(40,25)
        onlyChoseBtn.setCheckable(True)
        onlyChoseBtn.toggled.connect(lambda val:self.onSolo.emit(val))
        layout.addWidget(onlyChoseBtn)

        #查看/设置颜色
        self.colorBtn = QtWidgets.QPushButton()
        self.initColorBtn()
        self.colorBtn.setMaximumSize(40, 25)
        self.colorBtn.clicked.connect(self.createColorUI)
        layout.addWidget(self.colorBtn)

    #该函数用于初始化颜色按钮的background color
    def initColorBtn(self):
        lightcolor = self.light.getColor()
        r, g, b, a = [float(c)  for c in lightcolor]
        str = "background-color: rgba(%f,%f,%f,1)" % (r*255,g*255,b*255)
        self.colorBtn.setStyleSheet(str)

    #该函数用于改变颜色和按钮background color
    def createColorUI(self):
        lightcolor = self.light.getColor()
        color = pm.colorEditor(rgbValue = lightcolor)
        #返回的是str值
        r,g,b,a = [float(c) for c in color.split()]
        color = (r,g,b)
        self.light.color.set(color)
        str = "background-color: rgba(%f,%f,%f,1)"%(r*255,g*255,b*255)
        self.colorBtn.setStyleSheet(str)

    #该函数是辅助单独选中功能的，用于设置可见性
    def disableLight(self,value):
        self.light.getTransform().visibility.set(not value)
        self.name.setChecked(self.light.getTransform().visibility.get())

    #该函数用于删除light控件
    def deleteLight(self):
        self.setParent(None)
        self.setVisible(False)
        self.deleteLater()
        pm.delete(self.light.getTransform())





