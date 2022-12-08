from NodeGraphQt import BaseNode


class Action(BaseNode):
    """
    An example node with a embedded added QCombobox menu.
    """

    # unique node identifier.
    __identifier__ = 'nodes.widget'

    # initial default node name.
    NODE_NAME = 'Action 1'

    def __init__(self):
        super(Action, self).__init__()

        # create input & output ports
        # self.add_input('in 1')
        # self.add_output('out 1')
        # self.add_output('out 2')
        

        # create the QComboBox menu.
        items = ['Sand Down', 'Replace', 'Remove']
        self.add_combo_menu('my_menu', 'Menu Test', items=items)

class ApplyTo(BaseNode):
    """
    An example of a node with 2 embedded QCheckBox widgets.
    """

    # set a unique node identifier.
    __identifier__ = 'nodes.widget'

    # set the initial default node name.
    NODE_NAME = 'Apply to'

    def __init__(self):
        super(ApplyTo, self).__init__()

        # create the checkboxes.
        self.add_checkbox('cb_1', '', 'Right Flap 1', True)
        self.add_checkbox('cb_2', '', 'Right Flap 2', False)
        self.add_checkbox('cb_3', '', 'Right Flap 3', True)

        # create input and output port.
        self.add_input('in', color=(200, 100, 0))
        self.add_output('out', color=(0, 100, 200))
