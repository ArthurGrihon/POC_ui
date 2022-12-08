#!/usr/bin/python
from NodeGraphQt.base.node import NodeObject
from collections import OrderedDict
from NodeGraphQt.constants import (NODE_PROP_QTEXTEDIT,
                                   NODE_LAYOUT_HORIZONTAL,
                                   NODE_LAYOUT_VERTICAL,
                                   PortTypeEnum)
from NodeGraphQt.base.port import Port
from NodeGraphQt.errors import (PortError,
                                PortRegistrationError,
                                NodeWidgetError)                                   
from NodeGraphQt.qgraphics.node_backdrop import BackdropNodeItem


class BackdropNode(NodeObject):
    """
    The ``NodeGraphQt.BackdropNode`` class allows other node object to be
    nested inside, it's mainly good for grouping nodes together.

    **Inherited from:** :class:`NodeGraphQt.NodeObject`

    .. image:: ../_images/backdrop.png
        :width: 250px

    -
    """

    NODE_NAME = 'Backdrop'

    def __init__(self, qgraphics_views=None):
        qgraphics_views = qgraphics_views or {
            NODE_LAYOUT_HORIZONTAL: BackdropNodeItem,
            NODE_LAYOUT_VERTICAL: BackdropNodeItem
        }
        super(BackdropNode, self).__init__(qgraphics_views)
        # override base default color.
        self.model.color = (5, 129, 138, 255)
        self.create_property('backdrop_text', '',
                             widget_type=NODE_PROP_QTEXTEDIT,
                             tab='Backdrop')
        self._inputs = []
        self._outputs = []

    def on_backdrop_updated(self, update_prop, value=None):
        """
        Slot triggered by the "on_backdrop_updated" signal from
        the node graph.

        Args:
            update_prop (str): update property type.
            value (object): update value (optional)
        """
        if update_prop == 'sizer_mouse_release':
            self.graph.begin_undo('resized "{}"'.format(self.name()))
            self.set_property('width', value['width'])
            self.set_property('height', value['height'])
            self.set_pos(*value['pos'])
            self.graph.end_undo()
        elif update_prop == 'sizer_double_clicked':
            self.graph.begin_undo('"{}" auto resize'.format(self.name()))
            self.set_property('width', value['width'])
            self.set_property('height', value['height'])
            self.set_pos(*value['pos'])
            self.graph.end_undo()

    def auto_size(self):
        """
        Auto resize the backdrop node to fit around the intersecting nodes.
        """
        self.graph.begin_undo('"{}" auto resize'.format(self.name()))
        size = self.view.calc_backdrop_size()
        self.set_property('width', size['width'])
        self.set_property('height', size['height'])
        self.set_pos(*size['pos'])
        self.graph.end_undo()

    def wrap_nodes(self, nodes):
        """
        Set the backdrop size to fit around specified nodes.

        Args:
            nodes (list[NodeGraphQt.NodeObject]): list of nodes.
        """
        if not nodes:
            return
        self.graph.begin_undo('"{}" wrap nodes'.format(self.name()))
        size = self.view.calc_backdrop_size([n.view for n in nodes])
        self.set_property('width', size['width'])
        self.set_property('height', size['height'])
        self.set_pos(*size['pos'])
        self.graph.end_undo()

    def nodes(self):
        """
        Returns nodes wrapped within the backdrop node.

        Returns:
            list[NodeGraphQt.BaseNode]: list of node under the backdrop.
        """
        node_ids = [n.id for n in self.view.get_nodes()]
        return [self.graph.get_node_by_id(nid) for nid in node_ids]

    def set_text(self, text=''):
        """
        Sets the text to be displayed in the backdrop node.

        Args:
            text (str): text string.
        """
        self.set_property('backdrop_text', text)

    def text(self):
        """
        Returns the text on the backdrop node.

        Returns:
            str: text string.
        """
        return self.get_property('backdrop_text')

    def set_size(self, width, height):
        """
        Sets the backdrop size.

        Args:
            width (float): backdrop width size.
            height (float): backdrop height size.
        """
        if self.graph:
            self.graph.begin_undo('backdrop size')
            self.set_property('width', width)
            self.set_property('height', height)
            self.graph.end_undo()
            return
        self.view.width, self.view.height = width, height
        self.model.width, self.model.height = width, height

    def size(self):
        """
        Returns the current size of the node.

        Returns:
            tuple: node width, height
        """
        self.model.width = self.view.width
        self.model.height = self.view.height
        return self.model.width, self.model.height
    
    def add_input(self, name='input', multi_input=False, display_name=True,
                    color=None, locked=False, painter_func=None):
            """
            Add input :class:`Port` to node.

            Warnings:
                Undo is NOT supported for this function.

            Args:
                name (str): name for the input port.
                multi_input (bool): allow port to have more than one connection.
                display_name (bool): display the port name on the node.
                color (tuple): initial port color (r, g, b) ``0-255``.
                locked (bool): locked state see :meth:`Port.set_locked`
                painter_func (function or None): custom function to override the drawing
                    of the port shape see example: :ref:`Creating Custom Shapes`

            Returns:
                NodeGraphQt.Port: the created port object.
            """
            if name in self.inputs().keys():
                raise PortRegistrationError(
                    'port name "{}" already registered.'.format(name))

            port_args = [name, multi_input, display_name, locked]
            if painter_func and callable(painter_func):
                port_args.append(painter_func)
            view = self.view.add_input(*port_args)

            if color:
                view.color = color
                view.border_color = [min([255, max([0, i + 80])]) for i in color]

            port = Port(self, view)
            port.model.type_ = PortTypeEnum.IN.value
            port.model.name = name
            port.model.display_name = display_name
            port.model.multi_connection = multi_input
            port.model.locked = locked
            self._inputs.append(port)
            self.model.inputs[port.name()] = port.model
            return port

    def add_output(self, name='output', multi_output=True, display_name=True,
                color=None, locked=False, painter_func=None):
        """
        Add output :class:`Port` to node.

        Warnings:
            Undo is NOT supported for this function.

        Args:
            name (str): name for the output port.
            multi_output (bool): allow port to have more than one connection.
            display_name (bool): display the port name on the node.
            color (tuple): initial port color (r, g, b) ``0-255``.
            locked (bool): locked state see :meth:`Port.set_locked`
            painter_func (function or None): custom function to override the drawing
                of the port shape see example: :ref:`Creating Custom Shapes`

        Returns:
            NodeGraphQt.Port: the created port object.
        """
        if name in self.outputs().keys():
            raise PortRegistrationError(
                'port name "{}" already registered.'.format(name))

        port_args = [name, multi_output, display_name, locked]
        if painter_func and callable(painter_func):
            port_args.append(painter_func)
        view = self.view.add_output(*port_args)

        if color:
            view.color = color
            view.border_color = [min([255, max([0, i + 80])]) for i in color]
        port = Port(self, view)
        port.model.type_ = PortTypeEnum.OUT.value
        port.model.name = name
        port.model.display_name = display_name
        port.model.multi_connection = multi_output
        port.model.locked = locked
        self._outputs.append(port)
        self.model.outputs[port.name()] = port.model
        return port

    def get_input(self, port):
        """
        Get input port by the name or index.

        Args:
            port (str or int): port name or index.

        Returns:
            NodeGraphQt.Port: node port.
        """
        if type(port) is int:
            if port < len(self._inputs):
                return self._inputs[port]
        elif type(port) is str:
            return self.inputs().get(port, None)

    def get_output(self, port):
        """
        Get output port by the name or index.

        Args:
            port (str or int): port name or index.

        Returns:
            NodeGraphQt.Port: node port.
        """
        if type(port) is int:
            if port < len(self._outputs):
                return self._outputs[port]
        elif type(port) is str:
            return self.outputs().get(port, None)

    def delete_input(self, port):
        """
        Delete input port.

        Warnings:
            Undo is NOT supported for this function.

            You can only delete ports if :meth:`BaseNode.port_deletion_allowed`
            returns ``True`` otherwise a port error is raised see also
            :meth:`BaseNode.set_port_deletion_allowed`.

        Args:
            port (str or int): port name or index.
        """
        if type(port) in [int, str]:
            port = self.get_input(port)
            if port is None:
                return
        if not self.port_deletion_allowed():
            raise PortError(
                'Port "{}" can\'t be deleted on this node because '
                '"ports_removable" is not enabled.'.format(port.name()))
        if port.locked():
            raise PortError('Error: Can\'t delete a port that is locked!')
        self._inputs.remove(port)
        self._model.inputs.pop(port.name())
        self._view.delete_input(port.view)
        port.model.node = None
        self.draw()

    def delete_output(self, port):
        """
        Delete output port.

        Warnings:
            Undo is NOT supported for this function.

            You can only delete ports if :meth:`BaseNode.port_deletion_allowed`
            returns ``True`` otherwise a port error is raised see also
            :meth:`BaseNode.set_port_deletion_allowed`.

        Args:
            port (str or int): port name or index.
        """
        if type(port) in [int, str]:
            port = self.get_output(port)
            if port is None:
                return
        if not self.port_deletion_allowed():
            raise PortError(
                'Port "{}" can\'t be deleted on this node because '
                '"ports_removable" is not enabled.'.format(port.name()))
        if port.locked():
            raise PortError('Error: Can\'t delete a port that is locked!')
        self._outputs.remove(port)
        self._model.outputs.pop(port.name())
        self._view.delete_output(port.view)
        port.model.node = None
        self.draw()

    def set_port_deletion_allowed(self, mode=True):
        """
        Allow ports to be removable on this node.

        See Also:
            :meth:`BaseNode.port_deletion_allowed` and
            :meth:`BaseNode.set_ports`

        Args:
            mode (bool): true to allow.
        """
        self.model.port_deletion_allowed = mode

    def port_deletion_allowed(self):
        """
        Return true if ports can be deleted on this node.

        See Also:
            :meth:`BaseNode.set_port_deletion_allowed`

        Returns:
            bool: true if ports can be deleted.
        """
        return self.model.port_deletion_allowed

    def set_ports(self, port_data):
        """
        Create node input and output ports from serialized port data.

        Warnings:
            You can only use this function if the node has
            :meth:`BaseNode.port_deletion_allowed` is `True`
            see :meth:`BaseNode.set_port_deletion_allowed`

        Hint:
            example snippet of port data.

            .. highlight:: python
            .. code-block:: python

                {
                    'input_ports':
                        [{
                            'name': 'input',
                            'multi_connection': True,
                            'display_name': 'Input',
                            'locked': False
                        }],
                    'output_ports':
                        [{
                            'name': 'output',
                            'multi_connection': True,
                            'display_name': 'Output',
                            'locked': False
                        }]
                }

        Args:
            port_data(dict): port data.
        """
        if not self.port_deletion_allowed():
            raise PortError(
                'Ports cannot be set on this node because '
                '"set_port_deletion_allowed" is not enabled on this node.')

        for port in self._inputs:
            self._view.delete_input(port.view)
            port.model.node = None
        for port in self._outputs:
            self._view.delete_output(port.view)
            port.model.node = None
        self._inputs = []
        self._outputs = []
        self._model.outputs = {}
        self._model.inputs = {}

        [self.add_input(name=port['name'],
                        multi_input=port['multi_connection'],
                        display_name=port['display_name'],
                        locked=port.get('locked') or False)
         for port in port_data['input_ports']]
        [self.add_output(name=port['name'],
                         multi_output=port['multi_connection'],
                         display_name=port['display_name'],
                         locked=port.get('locked') or False)
         for port in port_data['output_ports']]
        self.draw()

    def inputs(self):
        """
        Returns all the input ports from the node.

        Returns:
            dict: {<port_name>: <port_object>}
        """
        return {p.name(): p for p in self._inputs}

    def input_ports(self):
        """
        Return all input ports.

        Returns:
            list[NodeGraphQt.Port]: node input ports.
        """
        return self._inputs

    def outputs(self):
        """
        Returns all the output ports from the node.

        Returns:
            dict: {<port_name>: <port_object>}
        """
        return {p.name(): p for p in self._outputs}

    def output_ports(self):
        """
        Return all output ports.

        Returns:
            list[NodeGraphQt.Port]: node output ports.
        """
        return self._outputs

    def input(self, index):
        """
        Return the input port with the matching index.

        Args:
            index (int): index of the input port.

        Returns:
            NodeGraphQt.Port: port object.
        """
        return self._inputs[index]

    def set_input(self, index, port):
        """
        Creates a connection pipe to the targeted output :class:`Port`.

        Args:
            index (int): index of the port.
            port (NodeGraphQt.Port): port object.
        """
        src_port = self.input(index)
        src_port.connect_to(port)

    def output(self, index):
        """
        Return the output port with the matching index.

        Args:
            index (int): index of the output port.

        Returns:
            NodeGraphQt.Port: port object.
        """
        return self._outputs[index]

    def set_output(self, index, port):
        """
        Creates a connection pipe to the targeted input :class:`Port`.

        Args:
            index (int): index of the port.
            port (NodeGraphQt.Port): port object.
        """
        src_port = self.output(index)
        src_port.connect_to(port)

    def connected_input_nodes(self):
        """
        Returns all nodes connected from the input ports.

        Returns:
            dict: {<input_port>: <node_list>}
        """
        nodes = OrderedDict()
        for p in self.input_ports():
            nodes[p] = [cp.node() for cp in p.connected_ports()]
        return nodes

    def connected_output_nodes(self):
        """
        Returns all nodes connected from the output ports.

        Returns:
            dict: {<output_port>: <node_list>}
        """
        nodes = OrderedDict()
        for p in self.output_ports():
            nodes[p] = [cp.node() for cp in p.connected_ports()]
        return nodes

    def on_input_connected(self, in_port, out_port):
        """
        Callback triggered when a new pipe connection is made.

        *The default of this function does nothing re-implement if you require
        logic to run for this event.*

        Note:
            to work with undo & redo for this method re-implement
            :meth:`BaseNode.on_input_disconnected` with the reverse logic.

        Args:
            in_port (NodeGraphQt.Port): source input port from this node.
            out_port (NodeGraphQt.Port): output port that connected to this node.
        """
        return

    def on_input_disconnected(self, in_port, out_port):
        """
        Callback triggered when a pipe connection has been disconnected
        from a INPUT port.

        *The default of this function does nothing re-implement if you require
        logic to run for this event.*

        Note:
            to work with undo & redo for this method re-implement
            :meth:`BaseNode.on_input_connected` with the reverse logic.

        Args:
            in_port (NodeGraphQt.Port): source input port from this node.
            out_port (NodeGraphQt.Port): output port that was disconnected.
        """
        return
