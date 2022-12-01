from NodeGraphQt import BaseNode
from NodeGraphQt import BackdropNode

class BackdropIn(BackdropNode):
    # unique node identifier.
    __identifier__ = 'nodes.backdrop'

    # initial default node name.
    NODE_NAME = 'Instruction 1'

    def __init__(self):
        super(BackdropIn, self).__init__()

        # # create node inputs.
        self.add_input('in A')
        # # create node outputs.
        self.add_output('out A')

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

class BasicNodeD(BaseNode):

    # unique node identifier.
    __identifier__ = 'nodes.basic'

    # initial default node name.
    NODE_NAME = 'Condition 1'
    
    def __init__(self):
        super(BasicNodeD, self).__init__()

        # create node inputs.
        self.add_input('in')
        # create node outputs.
        self.add_output('out')