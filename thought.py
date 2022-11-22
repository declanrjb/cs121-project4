from item import Item

class Thought(Item):
    def __init__(self, name, desc, order, blurb):
        Item.__init__(self, name, desc)
        self.order = order
        self.blurb = blurb
