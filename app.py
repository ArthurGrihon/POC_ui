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
class Window(QMainWindow, Ui_MainWindow):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        #Calling methods
        self.setWindowIcon(QtGui.QIcon('icone.png'))
        # self.UiComponents()
        self.connectSignalsSlots()
        self.graph = NodeGraph()
        self.graph.register_nodes([
            basic_nodes.BasicNodeA,
            basic_nodes.BasicNodeB,
            basic_nodes.BasicNodeC,
            group_node.MyGroupNodeA,
            group_node.MyGroupNodeB,
            group_node.MyGroupNodeC,
            widget_nodes.DropdownMenuNodeA,
            widget_nodes.DropdownMenuNodeB,
            widget_nodes.CheckboxNode
        ])

        self.graph_widget = self.graph.widget
    
        #Setting widget to MainWindow
        self.setCentralWidget(self.graph_widget)
            # create a node properties bin widget.
        properties_bin = PropertiesBinWidget(node_graph=self.graph)
        properties_bin.setWindowFlags(QtCore.Qt.Tool)

        # example show the node properties bin widget when a node is double clicked.
        def display_properties_bin(node):
            if not properties_bin.isVisible():
                properties_bin.show()

        # wire function to "node_double_clicked" signal.
        self.graph.node_double_clicked.connect(display_properties_bin)

    # def UiComponents(self):

    #     #Creating a NodeGraph canvas
    #     graph = NodeGraph()

    #     # registered example nodes.
    #     graph.register_nodes([
    #         basic_nodes.BasicNodeA,
    #         basic_nodes.BasicNodeB,
    #         basic_nodes.BasicNodeC,
    #         group_node.MyGroupNodeA,
    #         group_node.MyGroupNodeB,
    #         group_node.MyGroupNodeC,
    #         widget_nodes.DropdownMenuNodeA,
    #         widget_nodes.DropdownMenuNodeB,
    #         widget_nodes.CheckboxNode
    #     ])

    #     self.graph_widget = graph.widget
    
    #     #Setting widget to MainWindow
    #     self.setCentralWidget(self.graph_widget)
    #     return graph

    def connectSignalsSlots(self):
        self.action_Exit.triggered.connect(self.close)
        self.action_Find_Replace.triggered.connect(self.findAndReplace)
        self.action_About.triggered.connect(self.about)
        self.actionentity.triggered.connect(self.Entity)
        self.actionAction.triggered.connect(self.Action)
        self.actionStatus.triggered.connect(self.Status)

    def findAndReplace(self):
        dialog = FindReplaceDialog(self)
        dialog.exec()

    def Entity(self):
        self.graph.create_node(
        'nodes.basic.BasicNodeA', text_color='#feab20')
    
    def Action(self):
        self.graph.create_node(
        'nodes.widget.DropdownMenuNodeA', text_color='#feab20')
    
    def Status(self):
        self.graph.create_node(
        'nodes.group.MyGroupNodeA', text_color='#feab20')

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

class FindReplaceDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi("ui/find_replace.ui", self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.showMaximized()
    sys.exit(app.exec())
