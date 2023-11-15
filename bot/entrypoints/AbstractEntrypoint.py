from abc import ABC, abstractmethod


class AbstractEntrypoint(ABC):
    @staticmethod
    @abstractmethod
    def launch() -> None:
        """
        Launch the entrypoint and listen to responses
        """
        raise NotImplementedError
