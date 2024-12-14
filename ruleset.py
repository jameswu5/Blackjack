class Ruleset():
    def __init__(self, threshold, stand_soft, das, surrender):
        self.threshold = threshold
        self.stand_soft = stand_soft  # Stand on soft threshold or not
        self.das = das  # Double after split
        self.surrender = surrender


class StandardRuleset(Ruleset):
    def __init__(self):
        super().__init__(17, True, True, True)


sr = StandardRuleset()
