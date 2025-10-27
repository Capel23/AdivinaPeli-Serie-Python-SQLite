import random

START_POINTS = 30

class GameSession:
    def __init__(self, item):
        self.item = item
        self.points = START_POINTS
        self.revealed = set(i for i, ch in enumerate(self.item['title']) if not ch.isalpha())
        self.used_hints = []

    def mask_title(self):
        out = []
        for i, ch in enumerate(self.item['title']):
            if ch.isalpha():
                out.append(ch if i in self.revealed else "_")
            else:
                out.append(ch)
        return "".join(out)

    def reveal_letter(self):
        alpha_indices = [i for i, ch in enumerate(self.item['title']) if ch.isalpha()]
        hidden = [i for i in alpha_indices if i not in self.revealed]
        if not hidden:
            return
        i = random.choice(hidden)
        self.revealed.add(i)
        self.points -= 1

    def use_hint(self, hint_cost):
        self.points -= hint_cost

    def guess(self, guess_text):
        return guess_text.strip().lower() == self.item['title'].strip().lower()
