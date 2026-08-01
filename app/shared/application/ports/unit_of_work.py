from __future__ import annotations

from abc import ABC, abstractmethod


class UnitOfWork(ABC):
    """
    Coordinates a database transaction.
    """

    @abstractmethod
    async def commit(self) -> None:
        """
        Commit the current transaction.
        """
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        """
        Roll back the current transaction.
        """
        raise NotImplementedError