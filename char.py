class Char:
    def __init__(self):
        self.name = "Player01"
        self.inventory = []
        self.coins = 230

    def __iter__(self):
        yield 'coins', self.coins
        yield 'name', self.name
