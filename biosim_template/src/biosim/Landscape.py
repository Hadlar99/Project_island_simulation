class lowland:

    def __init__(self, herbivores=None, carnivores= None):
        self.fodder = 800
        self.herbivores = herbivores if herbivores is not None else []
        self.carnivores = carnivores if carnivores is not None else []

    def feasting (self, N):

