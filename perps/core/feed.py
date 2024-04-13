from abc import abstractmethod


class Feed:
    """Abstract feed base class"""

    @abstractmethod
    def run_ticks(self):
        """Run feed ticks for a bit then release control"""
