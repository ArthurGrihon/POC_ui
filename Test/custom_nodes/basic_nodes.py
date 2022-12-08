from NodeGraphQt import BaseNode
from NodeGraphQt import BackdropNode

class BackdropIn(BackdropNode):
    # unique node identifier.
    __identifier__ = 'nodes.backdrop'

    # initial default node name.
    NODE_NAME = 'Instruction 1'

    def __init__(self):
        super(BackdropIn, self).__init__()

        # create node inputs.
        self.add_input('in')
        # create node outputs.
        # self.add_output('out')

class Entity(BaseNode):

    # unique node identifier.
    __identifier__ = 'nodes.basic'

    # initial default node name.
    NODE_NAME = 'Entity 1'

    def __init__(self):
        super(Entity, self).__init__()

        # create node inputs.
        # create node outputs.
        # self.add_output('out')

class State(BaseNode):

    # unique node identifier.
    __identifier__ = 'nodes.basic'

    # initial default node name.
    NODE_NAME = 'State 1'

    def __init__(self):
        super(State, self).__init__()

        # create node inputs.
        # create node outputs.
        # self.add_input('in')

class Tool(BaseNode):
    # unique node identifier.
    __identifier__ = 'nodes.basic'

    # initial default node name.
    NODE_NAME = 'Tool 1'

    def __init__(self):
        super(Tool, self).__init__()

        # create node inputs
        # create node outputs

class Condition(BaseNode):

    # unique node identifier.
    __identifier__ = 'nodes.basic'

    # initial default node name.
    NODE_NAME = 'Condition 1'
    
    def __init__(self):
        super(Condition, self).__init__()

        # create node inputs.
        self.add_input('in')
        # create node outputs.
        self.add_output('out')