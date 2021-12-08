from PySide2 import QtCore,QtWidgets,QtGui
from AutoRiggingScripts.AutoRigging import autoRigging
class GUI(QtWidgets.QDialog):



    def __init__(self):
        super(GUI, self).__init__()

        self.setWindowTitle("Auto Rigging")
        self.autoRigging = autoRigging()
        self.buildGui()

    def buildGui(self):
        self.layout = QtWidgets.QVBoxLayout(self)

        #Label
        firstLabel = QtWidgets.QLabel('STEP1')
        self.layout.addWidget(firstLabel)

        #naming options




        self.optionalWidget = QtWidgets.QWidget()
        self.optionalLayout = QtWidgets.QHBoxLayout(self.optionalWidget)
        self.layout.addWidget(self.optionalWidget)

        ori = QtWidgets.QLabel('Ori')
        label = QtWidgets.QLabel('Label')
        self.oriOptionsBtn = QtWidgets.QComboBox()
        self.labelOptionsBtn = QtWidgets.QComboBox()

        oriItem = ["lf_","rt_","ct"]
        lableItem = ['arm','leg']
        self.oriOptionsBtn.addItems(oriItem)
        self.labelOptionsBtn.addItems(lableItem)

        self.optionalLayout.addWidget(ori)
        self.optionalLayout.addWidget(self.oriOptionsBtn)
        self.optionalLayout.addWidget(label)
        self.optionalLayout.addWidget(self.labelOptionsBtn)

        line1 = QtWidgets.QFrame()
        line1.setFrameShape(QtWidgets.QFrame.HLine)
        self.layout.addWidget(line1)

        #step2
        secondLabel = QtWidgets.QLabel('STEP2')
        self.layout.addWidget(secondLabel)
        self.BtnWidget = QtWidgets.QWidget()
        self.BtnLayout = QtWidgets.QHBoxLayout(self.BtnWidget)
        self.layout.addWidget(self.BtnWidget)



        self.radioBtnIK = QtWidgets.QRadioButton('IK')
        self.radioBtnIK.setMinimumSize(50,50)
        self.radioBtnFK = QtWidgets.QRadioButton('FK')
        self.radioBtnFK.setMinimumSize(50, 50)
        self.radioBtnIKFK = QtWidgets.QRadioButton('IKFK')
        self.radioBtnIKFK.setMinimumSize(50, 50)


        self.btnGroup = QtWidgets.QButtonGroup()
        self.btnGroup.addButton(self.radioBtnIK,1)
        self.btnGroup.addButton(self.radioBtnFK,2)
        self.btnGroup.addButton(self.radioBtnIKFK,3)
        self.btnGroup.buttonClicked.connect(self.rigTypeOption)


        self.BtnLayout.addWidget(self.radioBtnIK)
        self.BtnLayout.addWidget(self.radioBtnFK)
        self.BtnLayout.addWidget(self.radioBtnIKFK)
        self.BtnLayout.setSpacing(0.1)

        #step3
        line2 = QtWidgets.QFrame()
        line2.setFrameShape(QtWidgets.QFrame.HLine)


        # STEP3网格布局
        self.comboWidget = QtWidgets.QWidget()
        self.iconComboLayout = QtWidgets.QGridLayout(self.comboWidget)
        self.layout.addWidget(self.comboWidget)

        #step3说明
        self.iconComboLayout.addWidget(line2,0,0,1,2)

        thirdLabel = QtWidgets.QLabel('STEP3')
        self.iconComboLayout.addWidget(thirdLabel)

        #标志
        self.IKStyleLabel = QtWidgets.QLabel('IK Icon Style')
        self.FKIconStyleLabel = QtWidgets.QLabel('FK Icon Style')
        self.HandIconStyleLabel = QtWidgets.QLabel('Hand Icon Style')
        self.PVIconStyleLabel = QtWidgets.QLabel('PV Icon Style')

        #combox
        self.IKIconStyleCombo = QtWidgets.QComboBox()
        self.FKIconStyleCombo = QtWidgets.QComboBox()
        self.HandIconCombo = QtWidgets.QComboBox()
        self.PVIconCombo = QtWidgets.QComboBox()

        #combox选项
        self.IKStyleList = ['BOX','4 Arrows','4 Pin']
        self.FKIconStyleList = ['Circle','Turn Arrows']
        self.HandIconStyleList = ['Circle','COG']
        self.PVIconStyleList = ['Dnmd','Arrow']

        #选项增加
        self.IKIconStyleCombo.addItems(self.IKStyleList)
        self.FKIconStyleCombo.addItems(self.FKIconStyleList)
        self.HandIconCombo.addItems(self.HandIconStyleList)
        self.PVIconCombo.addItems(self.PVIconStyleList)

        #设置按钮
        self.setScaleBtn = QtWidgets.QPushButton()
        self.setScaleBtn.setText('Make test icons to set scale')
        self.setScaleBtn.clicked.connect(self.setScale)

        #添加所有STEP3
        self.iconComboLayout.addWidget(self.IKStyleLabel,2,0)
        self.iconComboLayout.addWidget(self.IKIconStyleCombo,2,1)
        self.iconComboLayout.addWidget(self.FKIconStyleLabel, 3, 0)
        self.iconComboLayout.addWidget(self.FKIconStyleCombo,3,1)
        self.iconComboLayout.addWidget(self.HandIconStyleLabel, 4, 0)
        self.iconComboLayout.addWidget(self.HandIconCombo,4,1)
        self.iconComboLayout.addWidget(self.PVIconStyleLabel, 5, 0)
        self.iconComboLayout.addWidget(self.PVIconCombo,5,1)

        self.iconComboLayout.addWidget(self.setScaleBtn,6,0,1,2)

        #分割线
        line3 = QtWidgets.QFrame()
        line3.setFrameShape(QtWidgets.QFrame.HLine)
        self.iconComboLayout.addWidget(line3,7,0,1,2)


        #STEP4
        fourthLabel = QtWidgets.QLabel('STEP4')


        # STEP4网格布局
        self.colorWidget = QtWidgets.QWidget()
        self.colorLayout = QtWidgets.QGridLayout(self.colorWidget)
        self.layout.addWidget(self.colorWidget)

        #颜色按键
        self.ColorTextBtn1 = QtWidgets.QPushButton()
        self.ColorTextBtn2 = QtWidgets.QPushButton()
        self.ColorTextBtn3 = QtWidgets.QPushButton()
        self.ColorTextBtn4 = QtWidgets.QPushButton()

        #设置按键背景色
        self.ColorTextBtn1.setStyleSheet("Background-color:red")
        self.ColorTextBtn2.setStyleSheet("Background-color:blue")
        self.ColorTextBtn3.setStyleSheet("Background-color:yellow")
        self.ColorTextBtn4.setStyleSheet("Background-color:brown")

        #颜色按键通信
        self.ColorTextBtn1.clicked.connect(self.getColor1)
        self.ColorTextBtn2.clicked.connect(self.getColor2)
        self.ColorTextBtn3.clicked.connect(self.getColor3)
        self.ColorTextBtn4.clicked.connect(self.getColor4)

        #颜色滑动条
        self.colorSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)


        #增加控件
        self.colorLayout.addWidget(fourthLabel,0,0)
        self.colorLayout.addWidget(self.ColorTextBtn1,1,0)
        self.colorLayout.addWidget(self.ColorTextBtn2,1,1)
        self.colorLayout.addWidget(self.ColorTextBtn3,1,2)
        self.colorLayout.addWidget(self.ColorTextBtn4,1,3)
        self.colorLayout.addWidget(self.colorSlider,2,0,1,4)




        line4 = QtWidgets.QFrame()
        line4.setFrameShape(QtWidgets.QFrame.HLine)
        self.layout.addWidget(line4)

        #STEP5
        setIK_Label =  QtWidgets.QLabel("STEP5")
        self.layout.addWidget(setIK_Label)

        self.setIK_Widget = QtWidgets.QWidget()
        self.setIK_Layout = QtWidgets.QHBoxLayout(self.setIK_Widget)
        self.layout.addWidget(self.setIK_Widget)

        self.TwistBtn = QtWidgets.QRadioButton("Twist")
        self.PoleVectorBtn = QtWidgets.QRadioButton("Pole Vector")
        self.setIK_Group = QtWidgets.QButtonGroup()
        self.setIK_Group.addButton(self.TwistBtn)
        self.setIK_Group.addButton(self.PoleVectorBtn)

        self.setIK_Layout.addWidget(self.TwistBtn)
        self.setIK_Layout.addWidget(self.PoleVectorBtn)

        #Finalize the arm
        line5 = QtWidgets.QFrame()
        line5.setFrameShape(QtWidgets.QFrame.HLine)
        line5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.layout.addWidget(line5)

        self.FinalizeBtn = QtWidgets.QPushButton()
        self.FinalizeBtn.clicked.connect(self.finalize)
        self.layout.addWidget(self.FinalizeBtn)

        self.layout.setMargin(0.1)
        self.layout.setSpacing(0.1)

    #当选择rig type时，Icon选项会有所不同
    def rigTypeOption(self,value):
        self.undoIconOptions()
        #获得选中按钮的id
        btnId = self.btnGroup.checkedId()
        self.excOptions(btnId)
    def excOptions(self,btnId):
        if btnId == 1:
            self.FKIconStyleLabel.setVisible(False)
            self.FKIconStyleCombo.setVisible(False)
            self.HandIconStyleLabel.setVisible(False)
            self.HandIconCombo.setVisible(False)
        elif btnId == 2:
            self.IKStyleLabel.setVisible(False)
            self.IKIconStyleCombo.setVisible(False)
            self.HandIconStyleLabel.setVisible(False)
            self.HandIconCombo.setVisible(False)
            self.PVIconStyleLabel.setVisible(False)
            self.PVIconCombo.setVisible(False)
            self.TwistBtn.setVisible(False)
            self.PoleVectorBtn.setVisible(False)
        elif btnId == 3:
            self.undoIconOptions()
    def undoIconOptions(self):
        self.IKStyleLabel.setVisible(True)
        self.FKIconStyleLabel.setVisible(True)
        self.HandIconStyleLabel.setVisible(True)
        self.PVIconStyleLabel.setVisible(True)

        self.IKIconStyleCombo.setVisible(True)
        self.FKIconStyleCombo.setVisible(True)
        self.HandIconCombo.setVisible(True)
        self.PVIconCombo.setVisible(True)

        self.TwistBtn.setVisible(True)
        self.PoleVectorBtn.setVisible(True)


    def getColor1(self):
        self.IconText.setStyleSheet("Background-color:red")
    def getColor2(self):
        self.IconText.setStyleSheet("Background-color:blue")
    def getColor3(self):
        self.IconText.setStyleSheet("Background-color:yellow")
    def getColor4(self):
        self.IconText.setStyleSheet("Background-color:brown")
    def setScale(self):
        pass
    def finalize(self):
        pass

ui = GUI()
ui.show()