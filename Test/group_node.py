from NodeGraphQt import GroupNode


class State(GroupNode):
    """
    example test group node with a in port and out port.
    """

    # set a unique node identifier.
    __identifier__ = 'nodes.group'

    # set the initial default node name.
    NODE_NAME = 'Status 1'

    def __init__(self):
        super(State, self).__init__()
        self.set_color(50, 8, 25)

        # create input and output port.
        self.add_input('in')


       
