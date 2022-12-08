# To translate .ui file 
##python -m PyQt5.uic.pyuic -o main_window_ui.py ui\main_window.ui  ##
import sys

from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QMessageBox
from PyQt5.uic import loadUi
from PyQt5 import QtCore, QtWidgets, QtGui

from main_window_ui import Ui_MainWindow

from NodeGraphQt import (
    NodeGraph,
    PropertiesBinWidget,
    NodesTreeWidget,
    NodesPaletteWidget
)

# import example nodes from the "Test" package
from Test import group_node
from Test.custom_nodes import (
    basic_nodes,
    custom_ports_node,
    widget_nodes,
)
class Window(QMainWindow, Ui_MainWindow,NodeGraph):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('ui\\resources\icone.png'))
        self.connectSignalsSlots()
        self.graph = NodeGraph()
        self.graph.register_nodes([
            basic_nodes.Entity,
            widget_nodes.Action,
            basic_nodes.State,
            basic_nodes.Tool,
            basic_nodes.Condition,            
            basic_nodes.BackdropIn,            
            widget_nodes.ApplyTo
        ])

        self.graph_widget = self.graph.widget
    
        # Setting widget to MainWindow
        self.setCentralWidget(self.graph_widget)

        # create a node properties bin widget.
        self.properties_bin = PropertiesBinWidget(node_graph=self.graph)
        self.properties_bin.setWindowFlags(QtCore.Qt.Tool)

        # Show the node properties bin widget when a node is double clicked.
        def display_properties_bin():
            if not self.properties_bin.isVisible():
                self.properties_bin.show()

        # wire function to "node_double_clicked" signal.
        self.graph.node_double_clicked.connect(display_properties_bin)

        #create a node tree widget
        self.nodes_tree = NodesTreeWidget(node_graph=self.graph)
        self.nodes_tree.show()

    # connect functions to buttons
    def connectSignalsSlots(self):
        self.action_Exit.triggered.connect(self.close)
        self.action_Find_Replace.triggered.connect(self.findAndReplace)
        self.action_About.triggered.connect(self.about)
        self.actionentity.triggered.connect(self.Entity)
        self.actionAction.triggered.connect(self.Action)
        self.actionStatus.triggered.connect(self.State)
        self.actionTool.triggered.connect(self.Tool)
        self.actionBackDrop.triggered.connect(self.BackdropIn)
        self.actionApply.triggered.connect(self.ApplyTo)
        self.actioncondition.triggered.connect(self.Condition)

    # create find and replace function
    def findAndReplace(self):
        dialog = FindReplaceDialog(self)
        dialog.exec()

    # create Entity node function
    def Entity(self):
        self.graph.create_node(
        'nodes.basic.Entity', text_color='#feab20')
    
    # create Action node function
    def Action(self):
        self.graph.create_node(
        'nodes.widget.Action', text_color='#feab20')
    
    # create State node function
    def State(self):
        self.graph.create_node(
        'nodes.basic.State', text_color='#feab20')

    # create Tool node function
    def Tool(self):
        self.graph.create_node(
        'nodes.basic.Tool', text_color='#feab20')

    # create BacdropIn wrapper node function
    def BackdropIn(self):
        self.graph.create_node(
        'nodes.backdrop.BackdropIn')

    # create ApplyTo node function
    def ApplyTo(self):
         self.graph.create_node(
        'nodes.widget.ApplyTo', name='checkbox node')
    
    # create Condition node function
    def Condition(self):
        self.graph.create_node(
        'nodes.basic.Condition', text_color='#feab20')

    # create About function
    def about(self):
        QMessageBox.about(
            self,
            "About POC",
            "<p>A POC for aero maintenance instruction builder, built with :</p>"
            "<p>- PyQt</p>"
            "<p>- Qt Designer</p>"
            "<p>- Python</p>"
            "<p>- FreeCad</p>",
        )
# FinReplace =  New window in UI => New Class
class FindReplaceDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi("ui/find_replace.ui", self)


if __name__ == "__main__":

    app = QApplication(sys.argv)
    win = Window()
    win.showMaximized()
    sys.exit(app.exec())
    

    
