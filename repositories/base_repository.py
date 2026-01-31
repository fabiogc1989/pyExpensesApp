from abc import ABC, abstractmethod


class BaseRepository[T](ABC):
    """Generic abstract repository interface.

    Subclasses should implement methods to perform basic CRUD operations
    for entities of type `T`. Methods are intentionally abstract so that
    different storage backends (in-memory, file, database) can provide
    concrete implementations.
    """
    @abstractmethod
    def get_all(self) -> list[T]:
        """
        Retrieves all records of the entity from the database.
        
        :param self: The repository instance (the current object on which the method is called).
        :return: List of objects of type T.
        :rtype: list[T]
        """
        ...

    @abstractmethod
    def get(self, id: int) -> T:
        """
        Docstring for get
        
        :param self: The repository instance (the current object on which the method is called).
        :param id: The ID of the entity to retrieve.
        :type id: int
        :return: The entity with the given ID, or None if not found.
        :rtype: T
        """
        ...

    @abstractmethod
    def delete(self, entity: T) -> bool:
        """
        Docstring for delete
        
        :param self: The repository instance (the current object on which the method is called).
        :param entity: The entity to delete.
        :type entity: T
        :return: True if the entity was deleted, False otherwise.
        :rtype: bool
        """
        ...

    @abstractmethod
    def update(self, entity: T) -> bool:
        ...

    @abstractmethod
    def insert(self, entity: T) -> bool:
        ...
