class HerbChecker():
    def __init__(self, f):
        common_herbs = [e.strip() for e in open(f).readlines()]
        self.common_herbs_set = set(common_herbs)

        # create reverse index
        self.reverse_index = {}
        for herb in common_herbs:
            ch = herb[0]
            if ch in self.reverse_index:
                self.reverse_index[ch].append(herb)
            else:
                self.reverse_index[ch] = [herb]

    def check(self, token):
        """check if token is a name of a herb"""
        if len(token) > 8:
            return False
        if token in self.common_herbs_set:
            return True
        if len(token) < 2:
            return False

        # contains a valid herb name
        for ch in token:
            if ch in self.reverse_index:
                if any([token.find(_) != -1 for _ in self.reverse_index[ch]]):
                       return True

        return False
