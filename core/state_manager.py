"""
Core game state machine.

Each game "mode" (overworld, battle, menu, dialogue) is a State subclass.
StateManager owns the active state (or stack of states) and handles
transitions between them.
"""


class State:
    """Base class every game state inherits from."""

    def __init__(self, manager):
        self.manager = manager  # backref, so a state can push/pop/switch states

    def enter(self, **kwargs):
        """Called every time this state becomes active. kwargs let you pass
        data in on transition, e.g. entering BattleState with which
        Pokemon/trainer triggered it."""
        pass

    def exit(self):
        """Called when leaving this state, before the next one enters."""
        pass

    def handle_event(self, event):
        """Raw pygame events (KEYDOWN, etc). One event per call."""
        pass

    def update(self, dt):
        """dt = seconds since last frame. Game logic goes here."""
        pass

    def draw(self, surface):
        """Draw this state's frame onto the given surface."""
        pass


class StateManager:
    """
    Holds a stack of states. A stack (not just a single "current state")
    means you can push MenuState on top of OverworldState and pop back to
    exactly where you were, instead of having to save/restore overworld
    state manually every time a menu opens.
    """

    def __init__(self):
        self._stack = []

    @property
    def current(self):
        return self._stack[-1] if self._stack else None

    def push(self, state, **kwargs):
        if self.current:
            self.current.exit()
        self._stack.append(state)
        state.enter(**kwargs)

    def pop(self, **kwargs):
        if self._stack:
            self._stack.pop().exit()
        if self.current:
            self.current.enter(**kwargs)

    def switch(self, state, **kwargs):
        """Replace the entire stack with a single new state.
        Use this for hard transitions (e.g. overworld -> battle) where you
        don't want to return to what was underneath."""
        while self._stack:
            self._stack.pop().exit()
        self._stack.append(state)
        state.enter(**kwargs)

    def handle_event(self, event):
        if self.current:
            self.current.handle_event(event)

    def update(self, dt):
        if self.current:
            self.current.update(dt)

    def draw(self, surface):
        if self.current:
            self.current.draw(surface)