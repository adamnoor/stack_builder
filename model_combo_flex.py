class FlexCombo:
    def __init__(self, rb1, rb2, wr1, wr2, wr3, te, fx):
        self.rb1 = rb1
        self.rb2 = rb2
        self.wr1 = wr1
        self.wr2 = wr2
        self.wr3 = wr3
        self.te = te
        self.fx = fx
        self.salary = rb1.salary + rb2.salary + wr1.salary + wr2.salary + wr3.salary + te.salary + fx.salary
        self.projection = rb1.projection + rb2.projection + wr1.projection + wr2.projection + wr3.projection + te.projection + fx.projection
        self.ratio = rb1.ratio + rb2.ratio + wr1.ratio + wr2.ratio + wr3.ratio + te.ratio + fx.ratio
