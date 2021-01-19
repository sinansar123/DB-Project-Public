class Instrument():
    def __init__(self, type, model, prod_year, mods, link, added_by, id=None):
        self.id = id
        self.type = type
        self.model = model
        self.prod_year = prod_year
        self.mods = mods
        self.link = link
        self.added_by = added_by

