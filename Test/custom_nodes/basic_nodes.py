from NodeGraphQt import BaseNode


class BasicNodeA(BaseNode):

    # unique node identifier.
    __identifier__ = 'nodes.basic'

    # initial default node name.
    NODE_NAME = 'Right Flap 1'

    def __init__(self):
        super(BasicNodeA, self).__init__()

        # create node inputs.
        # create node outputs.
        self.add_output('out A')


class BasicNodeB(BaseNode):

    # unique node identifier.
    __identifier__ = 'nodes.basic'

    # initial default node name.
    NODE_NAME = 'Right Flap 2'

    def __init__(self):
        super(BasicNodeB, self).__init__()

        # create node inputs.
        # create node outputs.
        self.add_output('out A')

class BasicNodeC(BaseNode):

    # unique node identifier.
    __identifier__ = 'nodes.basic'

    # initial default node name.
    NODE_NAME = 'Right Flap 3'
    
    def __init__(self):
        super(BasicNodeC, self).__init__()

        # create node inputs.
        # create node outputs.
        self.add_output('out A')
