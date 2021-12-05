from PySide2 import QtWidgets
from PySide2 import QtCore
from maya import cmds
import os
import pprint
import json

USERAPPDATA = cmds.internalVar(userAppDir = True)
DIRECTORY = os.path.join(USERAPPDATA,"Jpath")
print(DIRECTORY)
def creteDirectory(directory = DIRECTORY):
    """
        :param directory(str):
        :return:
    """
    if not os.path.exists(DIRECTORY):
        os.mkdir(DIRECTORY)

class ControllerLibrary(dict):
    #screenshot屏幕截图
    def save(self,*name,directory = DIRECTORY,screenshot = True,**info):
        creteDirectory(directory)
        if not name :
            if len(cmds.ls(selection=True)) == 1:
                name = cmds.ls(selection = True)[0]
                path = os.path.join(directory,"%s"%name)

                cmds.file(rename = path)
                cmds.file(force=True,type = 'mayaAscii',exportSelected = True) #导出

                self[name] = path
            else:
                path = os.path.join(directory, "default save scene")

                cmds.file(rename=path)
                cmds.file(save=True,type = 'mayaAscii',force = True)#直接保存

                self[name] = path

        else:
            #输入名字保存才有json

            path = os.path.join(directory, "%s" % name)
            info['name'] = name
            info['path'] = path

            # 用于创建json的路径名
            infoFile = os.path.join(directory, 'wtf.json' )

            #用于屏幕快照标志，并同时保存在info
            if screenshot:
                info['screenshot'] = self.saveScreenshot(name,directory = directory)
            cmds.file(rename=path)
            if cmds.ls(selection=True):
                cmds.file(force=True, type='mayaAscii', exportSelected=True)
            else:
                cmds.file(save=True, type='mayaAscii', force=True)

            # 用于写json文件，打开该文件存储到名为temp_file的变量
            with open(infoFile, 'w') as temp_file:
                # 使用json转储得到的字典，设置缩进为4
                json.dump(info, temp_file, indent=4)
            self[name] = info

    def find(self,directory = DIRECTORY):
        self.clear()
        if not os.path.exists(directory):
            return
        #os.listdir用于找到目录下的所有文件名
        listdir = os.listdir(directory)
        #找到后缀为ma的文件名
        mayaFiles = [f for f in listdir if f.endswith('.ma')]

        for fn in mayaFiles:
            name,ext = os.path.splitext(fn) #分割前缀和后缀
            path = os.path.join(directory,fn)

            #该项用于查看每个ma文件是否有对应的json文件
            infoFile ='%s.json'%name
            if infoFile in listdir:
                infoFile = os.path.join(directory,infoFile)
                # 用于读json文件，打开该文件存储到名为temp_file的变量
                with open(infoFile, 'w') as temp_file:
                    # 读取json文件
                    info = json.load(temp_file)

            else:
                #如果没有json文件，那么为它创建一个
                info = {}

            # 该项用于查看每个ma文件是否有对应的快照
            screenshot = '%s.jpg' % name
            if screenshot in listdir:
                info['screenshot'] = os.path.join(directory, screenshot)
            else:
                pass
            #如果没有json文件，那么为它创建一个


            info['name'] = name
            info['path'] = path
            self[name] = info #为每个name赋予一个字典
        pprint.pprint(self)
    def load(self,name):
        path = self[name]['path']
        cmds.file(path,i=True,usingNamespaces = False) #不允许将控制器导入到第二个命名空间中

    def saveScreenshot(self, name, directory):
        path = os.path.join(directory,'%s.jpg'%name)
        cmds.viewFit()
        cmds.setAttr('defaultRenderGlobals.imageFormat',8)
        cmds.playblast(completeFilename = path, forceOverwrite = True,
                       format = 'image',width = 200,height = 200,showOrnaments = False,
                       startTime = 1,endTime = 1,viewer = False)
        return path