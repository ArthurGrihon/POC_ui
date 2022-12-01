#!/usr/bin/python
from Qt import QtGui, QtCore, QtWidgets

from collections import OrderedDict
from NodeGraphQt.qgraphics.node_abstract import AbstractNodeItem
from NodeGraphQt.qgraphics.pipe import PipeItem
from NodeGraphQt.qgraphics.port import PortItem, CustomPortItem
from NodeGraphQt.constants import (
    ITEM_CACHE_MODE,
    ICON_NODE_BASE,
    Z_VAL_PIPE,
    NodeEnum,
    PortEnum,
    PortTypeEnum,
    Z_VAL_NODE
)
class BackdropSizer(QtWidgets.QGraphicsItem):
    """
    Sizer item for resizing a backdrop item.

    Args:
        parent (BackdropNodeItem): the parent node item.
        size (float): sizer size.
    """

    def __init__(self, parent=None, size=6.0):
        super(BackdropSizer, self).__init__(parent)
        self.setFlag(self.ItemIsSelectable, True)
        self.setFlag(self.ItemIsMovable, True)
        self.setFlag(self.ItemSendsScenePositionChanges, True)
        self.setCursor(QtGui.QCursor(QtCore.Qt.SizeFDiagCursor))
        self.setToolTip('double-click auto resize')
        self._size = size

    @property
    def size(self):
        return self._size

    def set_pos(self, x, y):
        x -= self._size
        y -= self._size
        self.setPos(x, y)

    def boundingRect(self):
        return QtCore.QRectF(0.5, 0.5, self._size, self._size)

    def itemChange(self, change, value):
        if change == self.ItemPositionChange:
            item = self.parentItem()
            mx, my = item.minimum_size
            x = mx if value.x() < mx else value.x()
            y = my if value.y() < my else value.y()
            value = QtCore.QPointF(x, y)
            item.on_sizer_pos_changed(value)
            return value
        return super(BackdropSizer, self).itemChange(change, value)

    def mouseDoubleClickEvent(self, event):
        item = self.parentItem()
        item.on_sizer_double_clicked()
        super(BackdropSizer, self).mouseDoubleClickEvent(event)

    def mousePressEvent(self, event):
        self.__prev_xy = (self.pos().x(), self.pos().y())
        super(BackdropSizer, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        current_xy = (self.pos().x(), self.pos().y())
        if current_xy != self.__prev_xy:
            item = self.parentItem()
            item.on_sizer_pos_mouse_release()
        del self.__prev_xy
        super(BackdropSizer, self).mouseReleaseEvent(event)

    def paint(self, painter, option, widget):
        """
        Draws the backdrop sizer on the bottom right corner.

        Args:
            painter (QtGui.QPainter): painter used for drawing the item.
            option (QtGui.QStyleOptionGraphicsItem):
                used to describe the parameters needed to draw.
            widget (QtWidgets.QWidget): not used.
        """
        painter.save()

        margin = 1.0
        rect = self.boundingRect()
        rect = QtCore.QRectF(rect.left() + margin,
                             rect.top() + margin,
                             rect.width() - (margin * 2),
                             rect.height() - (margin * 2))

        item = self.parentItem()
        if item and item.selected:
            color = QtGui.QColor(*NodeEnum.SELECTED_BORDER_COLOR.value)
        else:
            color = QtGui.QColor(*item.color)
            color = color.darker(110)
        path = QtGui.QPainterPath()
        path.moveTo(rect.topRight())
        path.lineTo(rect.bottomRight())
        path.lineTo(rect.bottomLeft())
        painter.setBrush(color)
        painter.setPen(QtCore.Qt.NoPen)
        painter.fillPath(path, painter.brush())

        painter.restore()


class BackdropNodeItem(AbstractNodeItem):
    """
    Base Backdrop item.

    Args:
        name (str): name displayed on the node.
        text (str): backdrop text.
        parent (QtWidgets.QGraphicsItem): parent item.
    """

    def __init__(self, name='backdrop', text='', parent=None):
        super(BackdropNodeItem, self).__init__(name, parent)
        self.setZValue(Z_VAL_PIPE - 1)
        self._properties['backdrop_text'] = text
        self._min_size = 80, 80
        self._sizer = BackdropSizer(self, 26.0)
        self._sizer.set_pos(*self._min_size)
        self._nodes = [self]
        self._input_items = OrderedDict()
        self._output_items = OrderedDict()

    def _combined_rect(self, nodes):
        group = self.scene().createItemGroup(nodes)
        rect = group.boundingRect()
        self.scene().destroyItemGroup(group)
        return rect

    def mouseDoubleClickEvent(self, event):
        viewer = self.viewer()
        if viewer:
            viewer.node_double_clicked.emit(self.id)
        super(BackdropNodeItem, self).mouseDoubleClickEvent(event)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            pos = event.scenePos()
            rect = QtCore.QRectF(pos.x() - 5, pos.y() - 5, 10, 10)
            item = self.scene().items(rect)[0]

            if isinstance(item, (PortItem, PipeItem)):
                self.setFlag(self.ItemIsMovable, False)
                return
            if self.selected:
                return

            viewer = self.viewer()
            [n.setSelected(False) for n in viewer.selected_nodes()]

            self._nodes += self.get_nodes(False)
            [n.setSelected(True) for n in self._nodes]

    def mouseReleaseEvent(self, event):
        super(BackdropNodeItem, self).mouseReleaseEvent(event)
        self.setFlag(self.ItemIsMovable, True)
        [n.setSelected(True) for n in self._nodes]
        self._nodes = [self]

    def on_sizer_pos_changed(self, pos):
        self._width = pos.x() + self._sizer.size
        self._height = pos.y() + self._sizer.size

    def on_sizer_pos_mouse_release(self):
        size = {
            'pos': self.xy_pos,
            'width': self._width,
            'height': self._height}
        self.viewer().node_backdrop_updated.emit(
            self.id, 'sizer_mouse_release', size)

    def on_sizer_double_clicked(self):
        size = self.calc_backdrop_size()
        self.viewer().node_backdrop_updated.emit(
            self.id, 'sizer_double_clicked', size)

    def paint(self, painter, option, widget):
        """
        Draws the backdrop rect.

        Args:
            painter (QtGui.QPainter): painter used for drawing the item.
            option (QtGui.QStyleOptionGraphicsItem):
                used to describe the parameters needed to draw.
            widget (QtWidgets.QWidget): not used.
        """
        painter.save()
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtCore.Qt.NoBrush)

        margin = 1.0
        rect = self.boundingRect()
        rect = QtCore.QRectF(rect.left() + margin,
                             rect.top() + margin,
                             rect.width() - (margin * 2),
                             rect.height() - (margin * 2))

        radius = 2.6
        color = (self.color[0], self.color[1], self.color[2], 50)
        painter.setBrush(QtGui.QColor(*color))
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawRoundedRect(rect, radius, radius)

        top_rect = QtCore.QRectF(rect.x(), rect.y(), rect.width(), 26.0)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(*self.color)))
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawRoundedRect(top_rect, radius, radius)
        for pos in [top_rect.left(), top_rect.right() - 5.0]:
            painter.drawRect(
                QtCore.QRectF(pos, top_rect.bottom() - 5.0, 5.0, 5.0))

        if self.backdrop_text:
            painter.setPen(QtGui.QColor(*self.text_color))
            txt_rect = QtCore.QRectF(
                top_rect.x() + 5.0, top_rect.height() + 3.0,
                rect.width() - 5.0, rect.height())
            painter.setPen(QtGui.QColor(*self.text_color))
            painter.drawText(txt_rect,
                             QtCore.Qt.AlignLeft | QtCore.Qt.TextWordWrap,
                             self.backdrop_text)

        if self.selected:
            sel_color = [x for x in NodeEnum.SELECTED_COLOR.value]
            sel_color[-1] = 15
            painter.setBrush(QtGui.QColor(*sel_color))
            painter.setPen(QtCore.Qt.NoPen)
            painter.drawRoundedRect(rect, radius, radius)

        txt_rect = QtCore.QRectF(top_rect.x(), top_rect.y(),
                                 rect.width(), top_rect.height())
        painter.setPen(QtGui.QColor(*self.text_color))
        painter.drawText(txt_rect, QtCore.Qt.AlignCenter, self.name)

        border = 0.8
        border_color = self.color
        if self.selected and NodeEnum.SELECTED_BORDER_COLOR.value:
            border = 1.0
            border_color = NodeEnum.SELECTED_BORDER_COLOR.value
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.setPen(QtGui.QPen(QtGui.QColor(*border_color), border))
        painter.drawRoundedRect(rect, radius, radius)

        painter.restore()

    def get_nodes(self, inc_intersects=False):
        mode = {True: QtCore.Qt.IntersectsItemShape,
                False: QtCore.Qt.ContainsItemShape}
        nodes = []
        if self.scene():
            polygon = self.mapToScene(self.boundingRect())
            rect = polygon.boundingRect()
            items = self.scene().items(rect, mode=mode[inc_intersects])
            for item in items:
                if item == self or item == self._sizer:
                    continue
                if isinstance(item, AbstractNodeItem):
                    nodes.append(item)
        return nodes

    def calc_backdrop_size(self, nodes=None):
        nodes = nodes or self.get_nodes(True)
        padding = 40
        nodes_rect = self._combined_rect(nodes)
        return {
            'pos': [
                nodes_rect.x() - padding, nodes_rect.y() - padding
            ],
            'width': nodes_rect.width() + (padding * 2),
            'height': nodes_rect.height() + (padding * 2)
        }

    @property
    def minimum_size(self):
        return self._min_size

    @minimum_size.setter
    def minimum_size(self, size=(50, 50)):
        self._min_size = size

    @property
    def backdrop_text(self):
        return self._properties['backdrop_text']

    @backdrop_text.setter
    def backdrop_text(self, text):
        self._properties['backdrop_text'] = text
        self.update(self.boundingRect())

    @AbstractNodeItem.width.setter
    def width(self, width=0.0):
        AbstractNodeItem.width.fset(self, width)
        self._sizer.set_pos(self._width, self._height)

    @AbstractNodeItem.height.setter
    def height(self, height=0.0):
        AbstractNodeItem.height.fset(self, height)
        self._sizer.set_pos(self._width, self._height)

    @property
    def inputs(self):
        """
        Returns:
            list[PortItem]: input port graphic items.
        """
        return list(self._input_items.keys())

    @property
    def outputs(self):
        """
        Returns:
            list[PortItem]: output port graphic items.
        """
        return list(self._output_items.keys())

    def _add_port(self, port):
        """
        Adds a port qgraphics item into the node.

        Args:
            port (PortItem): port item.

        Returns:
            PortItem: port qgraphics item.
        """
        text = QtWidgets.QGraphicsTextItem(port.name, self)
        text.font().setPointSize(8)
        text.setFont(text.font())
        text.setVisible(port.display_name)
        text.setCacheMode(ITEM_CACHE_MODE)
        if port.port_type == PortTypeEnum.IN.value:
            self._input_items[port] = text
        elif port.port_type == PortTypeEnum.OUT.value:
            self._output_items[port] = text
        if self.scene():
            self.post_init()
        return port

    def add_input(self, name='input', multi_port=False, display_name=True,
                  locked=False, painter_func=None):
        """
        Adds a port qgraphics item into the node with the "port_type" set as
        IN_PORT.

        Args:
            name (str): name for the port.
            multi_port (bool): allow multiple connections.
            display_name (bool): display the port name.
            locked (bool): locked state.
            painter_func (function): custom paint function.

        Returns:
            PortItem: input port qgraphics item.
        """
        if painter_func:
            port = CustomPortItem(self, painter_func)
        else:
            port = PortItem(self)
        port.name = name
        port.port_type = PortTypeEnum.IN.value
        port.multi_connection = multi_port
        port.display_name = display_name
        port.locked = locked
        return self._add_port(port)

    def add_output(self, name='output', multi_port=False, display_name=True,
                   locked=False, painter_func=None):
        """
        Adds a port qgraphics item into the node with the "port_type" set as
        OUT_PORT.

        Args:
            name (str): name for the port.
            multi_port (bool): allow multiple connections.
            display_name (bool): display the port name.
            locked (bool): locked state.
            painter_func (function): custom paint function.

        Returns:
            PortItem: output port qgraphics item.
        """
        if painter_func:
            port = CustomPortItem(self, painter_func)
        else:
            port = PortItem(self)
        port.name = name
        port.port_type = PortTypeEnum.OUT.value
        port.multi_connection = multi_port
        port.display_name = display_name
        port.locked = locked
        return self._add_port(port)

    def _delete_port(self, port, text):
        """
        Removes port item and port text from node.

        Args:
            port (PortItem): port object.
            text (QtWidgets.QGraphicsTextItem): port text object.
        """
        port.setParentItem(None)
        text.setParentItem(None)
        self.scene().removeItem(port)
        self.scene().removeItem(text)
        del port
        del text

    def delete_input(self, port):
        """
        Remove input port from node.

        Args:
            port (PortItem): port object.
        """
        self._delete_port(port, self._input_items.pop(port))

    def delete_output(self, port):
        """
        Remove output port from node.

        Args:
            port (PortItem): port object.
        """
        self._delete_port(port, self._output_items.pop(port))

    def get_input_text_item(self, port_item):
        """
        Args:
            port_item (PortItem): port item.

        Returns:
            QGraphicsTextItem: graphic item used for the port text.
        """
        return self._input_items[port_item]

    def get_output_text_item(self, port_item):
        """
        Args:
            port_item (PortItem): port item.

        Returns:
            QGraphicsTextItem: graphic item used for the port text.
        """
        return self._output_items[port_item]