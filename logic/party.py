MAX_PARTY = 6

class Party:
    def __init__(self, members=None):
        self.members = list(members or [])[:MAX_PARTY]

    def add(self, mon):
        if len(self.members) >= MAX_PARTY:
            return False
        self.members.append(mon)
        return True

    def lead(self):
        """First mon that can still fight (None if the party is wiped)."""
        for mon in self.members:
            if mon.hp > 0:
                return mon
        return None

    def swap(self, i, j):
        self.members[i], self.members[j] = self.members[j], self.members[i]

    def is_wiped(self):
        return self.lead() is None

    def heal_all(self):
        for mon in self.members:
            mon.hp = mon.max_hp
