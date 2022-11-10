import signal

from Qt import QtCore, QtWidgets

from NodeGraphQt import NodeGraph


signal.signal(signal.SIGINT, signal.SIG_DFL)

QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

app = QtWidgets.QApplication([])

# create graph controller.

node_graph = NodeGraph()
context_menu = node_graph.get_context_menu('graph')
graph_widget = node_graph.widget
graph_widget.resize(1100, 800)
graph_widget.show()

app.exec_()



