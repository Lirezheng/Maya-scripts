from PySide2 import QtCore,QtWidgets,QtGui

class GUI(QtWidgets.QDialog):



    def __init__(self):
        super(GUI, self).__init__()

        self.setWindowTitle("Auto Rigging")
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
        for item in oriItem:
            self.oriOptionsBtn.addItem(item)
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
        self.btnGroup.addButton(self.radioBtnIK)
        self.btnGroup.addButton(self.radioBtnFK)
        self.btnGroup.addButton(self.radioBtnIKFK)


        self.BtnLayout.addWidget(self.radioBtnIK)
        self.BtnLayout.addWidget(self.radioBtnFK)
        self.BtnLayout.addWidget(self.radioBtnIKFK)

        #step3
        line2 = QtWidgets.QFrame()
        line2.setFrameShape(QtWidgets.QFrame.HLine)
        self.layout.addWidget(line2)

        thirdLabel = QtWidgets.QLabel('STEP3')
        self.layout.addWidget(thirdLabel)


        self.IKIconStyleCombo = QtWidgets.QComboBox()
        self.FKIconStyleCombo = QtWidgets.QComboBox()
        self.HandIconCombo = QtWidgets.QComboBox()
        self.PVIconCombo = QtWidgets.QComboBox()

        self.BtnWidget1 = QtWidgets.QWidget()
        self.BtnLayout1 = QtWidgets.QHBoxLayout(self.BtnWidget1)
        self.layout.addWidget(self.BtnWidget1)
        self.BtnWidget2 = QtWidgets.QWidget()
        self.BtnLayout2 = QtWidgets.QHBoxLayout(self.BtnWidget2)
        self.layout.addWidget(self.BtnWidget2)
        self.BtnWidget3 = QtWidgets.QWidget()
        self.BtnLayout3 = QtWidgets.QHBoxLayout(self.BtnWidget3)
        self.layout.addWidget(self.BtnWidget3)
        self.BtnWidget4 = QtWidgets.QWidget()
        self.BtnLayout4 = QtWidgets.QHBoxLayout(self.BtnWidget4)
        self.layout.addWidget(self.BtnWidget4)

        self.IKStyleLabel = QtWidgets.QLabel('IK Icon Style')
        self.FKIconStyleLabel = QtWidgets.QLabel('FK Icon Style')
        self.HandIconStyleLabel = QtWidgets.QLabel('Hand Icon Style')
        self.PVIconStyleLabel = QtWidgets.QLabel('PV Icon Style')

        self.BtnLayout1.addWidget(self.IKStyleLabel)
        self.BtnLayout1.addWidget(self.IKIconStyleCombo)
        self.BtnLayout2.addWidget(self.FKIconStyleLabel)
        self.BtnLayout2.addWidget(self.FKIconStyleCombo)
        self.BtnLayout3.addWidget(self.HandIconStyleLabel)
        self.BtnLayout3.addWidget(self.HandIconCombo)
        self.BtnLayout4.addWidget(self.PVIconStyleLabel)
        self.BtnLayout4.addWidget(self.PVIconCombo)

        #STEP4
        line3 = QtWidgets.QFrame()
        line3.setFrameShape(QtWidgets.QFrame.HLine)
        self.layout.addWidget(line3)

        fourthLabel = QtWidgets.QLabel('STEP4')
        self.layout.addWidget(fourthLabel)

        self.ColorWidget = QtWidgets.QWidget()
        self.ColorLayout = QtWidgets.QGridLayout(self.ColorWidget)
        self.layout.addWidget(self.ColorWidget)

        self.ColorTextBtn1 = QtWidgets.QPushButton()
        self.ColorTextBtn2 = QtWidgets.QPushButton()
        self.ColorTextBtn3 = QtWidgets.QPushButton()
        self.ColorTextBtn4 = QtWidgets.QPushButton()

        self.ColorTextBtn1.setStyleSheet("Background-color:red")
        self.ColorTextBtn2.setStyleSheet("Background-color:blue")
        self.ColorTextBtn3.setStyleSheet("Background-color:yellow")
        self.ColorTextBtn4.setStyleSheet("Background-color:brown")

        self.ColorTextBtn1.clicked.connect(self.getColor1)
        self.ColorTextBtn2.clicked.connect(self.getColor2)
        self.ColorTextBtn3.clicked.connect(self.getColor3)
        self.ColorTextBtn4.clicked.connect(self.getColor4)

        self.ColorLayout.addWidget(self.ColorTextBtn1,5,0)
        self.ColorLayout.addWidget(self.ColorTextBtn2,5,1)
        self.ColorLayout.addWidget(self.ColorTextBtn3,5,2)
        self.ColorLayout.addWidget(self.ColorTextBtn4,5,3)

        self.IconText = QtWidgets.QLabel("Picked Color")
        self.IconText.setStyleSheet("Background-color:red")
        self.ColorLayout.addWidget(self.IconText,6,0,1,4)

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

    def getColor1(self):
        self.IconText.setStyleSheet("Background-color:red")
    def getColor2(self):
        self.IconText.setStyleSheet("Background-color:blue")
    def getColor3(self):
        self.IconText.setStyleSheet("Background-color:yellow")
    def getColor4(self):
        self.IconText.setStyleSheet("Background-color:brown")
    def finalize(self):
        pass

ui = GUI()
ui.show()