
#from PySide2.QtGui import *
#from PySide2.QtCore import *
import hou
import toolutils

from hutil.Qt.QtCore import *
from hutil.Qt.QtWidgets import *

sv=toolutils.sceneViewer()

class VEX_Occur(QFrame):
    def __init__(self, parent=None):
        super( VEX_Occur , self).__init__(parent)
        title = QLabel("Symbol occurs")
        self.typeCombo=QComboBox()
        for i in "all types,point,primitive,vertex,detail".split(","):
            self.typeCombo.addItem(i)
        self.inSelected=QCheckBox("Look in selected only")
        self.lockedAsset=QCheckBox("Look in locked HDA's")
        self.bypassedNode=QCheckBox("Look in bypassed")
        self.inSelected.setChecked(False)
        self.lockedAsset.setChecked(False)
        self.bypassedNode.setChecked(False)
        layout = QVBoxLayout(self)
        layout.addWidget(title)
        self.textEdit = QLineEdit()
        layout.addWidget(self.textEdit)
        layout.addWidget(self.typeCombo)
        layout.addWidget(self.inSelected)
        layout.addWidget(self.lockedAsset)
        layout.addWidget(self.bypassedNode)

        self.found={}
        self.widget = QWidget()
        self.glayout = QGridLayout(self)
        self.widget.setLayout( self.glayout)
        #Scroll Area Properties
        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        #Scroll Area Layer add
        layout.addWidget(self.scroll)
        self.setLayout(layout)

        self.textEdit.textEdited.connect(self.populate)
        self.lockedAsset.stateChanged.connect(self.populate)
        self.bypassedNode.stateChanged.connect(self.populate)
        self.typeCombo.currentIndexChanged.connect(self.populate)
    def buttonClick(self):
        s = self.sender().text()
        node=hou.node(s)
        ppath=hou.node(s).parent().path()
        sv.cd(ppath)
        node.setSelected(1,1)

    def populate(self):
        self.clear_results()
        self.found.clear()
        text = self.textEdit.text()
        self.find_word(text)
        a=0
        if len( text)>=1:
            print ("Searching for " + text)
            self.widget = QFrame()
            self.glayout = QGridLayout(self)
            self.widget.setLayout( self.glayout)
            self.scroll.setWidget(self.widget)

            for i,k in self.found.items():
                node = hou.node(i)
                print (node)
                if node.type().name()=="attribwrangle":
                    awClass = node.parm("class").evalAsString()
                    currentClass = str(self.typeCombo.currentText())
                    asset = node.isInsideLockedHDA()
                    bypass = node.isBypassed()
                    if currentClass=="all types" or awClass==currentClass:
                        if asset and not self.lockedAsset.isChecked():
                            print ("an asset")
                        elif bypass  and not self.bypassedNode.isChecked():
                            print ("bypass")
                        else:
                            self.create_row(a,i,k,asset,bypass,awClass)
                            a+=1


    def create_row(self, a, but, txt, asset, bypass, awclass ):
        text = self.textEdit.text()
        b = QPushButton(but)
        t =  QTextBrowser()
        if asset:          # locked in asset
            t.setStyleSheet("background-color: teal;")
        if bypass:          # node is bypassed
            t.setStyleSheet("background-color: olive;")
        format_text = "<br>".join(txt).replace( text,"<html><b><font color=red>%s</b</font></html>"%text )
        t.setText(format_text)
        self.glayout.addWidget(b,a,0)
        self.glayout.addWidget(t,a,1)
        b.clicked.connect(self.buttonClick)

    def clear_results(self):
        try:
            self.widget.hide()
            self.widget.deleteLater()
        except:
            pass

    def print_tree_with_word(self,path, word):
        node = hou.node(path)
        for child in node.children():
            if child.type().name()=="attribwrangle" or child.type().name()=="pointwrangle":
                text=child.parm("snippet").evalAsString()
                a=0
                lines = text.split('\n')
                if word in text:
                    print (child.path())
                    message=[]
                    for line in lines:
                        a+=1
                        try:
                            if word in line:
                                g="line %d:<br> %s"%(a,line)
                                message.append(g)
                        except:pass
                    self.found[child.path()]=message
            child0 = path+"/"+child.name()
            self.print_tree_with_word(child0,word)

    def find_word(self,word):
        selNodes=hou.selectedNodes()
        # search everywhere if nothing is selected or "inSelected is checked"
        if not self.inSelected.isChecked() or len(selNodes) < 1:
            path="/"
            self.print_tree_with_word (path, word)
        else:
            for n in selNodes:
                path = n.path()
                self.print_tree_with_word (path, word)
