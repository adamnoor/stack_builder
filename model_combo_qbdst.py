class QbDstCombo:
    def __init__(self, qb, dst):
        self.qb = qb
        self.dst = dst
        self.salary = qb.salary + dst.salary
        self.projection = qb.projection + dst.projection
        self.ratio = qb.ratio + dst.ratio
