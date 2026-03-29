from abc import ABC, abstractmethod


class BaseRepository[T](ABC):
    """
    Generic abstract repository interface.

    Subclasses should implement methods to perform basic CRUD operations
    for entities of type `T`. Methods are intentionally abstract so that
    different storage backends (in-memory, file, database) can provide
    concrete implementations.
    """
    @abstractmethod
    def get_all(self) -> list[T]|iter[T]:
        """
        Retrieves all records of the entity from the database.
        
        :param self: The repository instance (the current object on which the method is called).
        :return: (List|Iterator) of objects of type T.
        :rtype: list[T]|iter[T]
        """
        ...

    @abstractmethod
    def get(self, id: int) -> T:
        """
        Retrieve a record of the entity from the database.
        
        :param self: The repository instance (the current object on which the method is called).
        :param id: The ID of the entity to retrieve.
        :type id: int
        :return: The entity with the given ID, or None if not found.
        :rtype: T
        """
        ...

    @abstractmethod
    def delete(self, id: int) -> None:
        """
        Remove a record of the entity from the database.
        
        :param self: The repository instance (the current object on which the method is called).
        :param id: The ID of the entity to delete.
        :type id: int
        """
        ...

    @abstractmethod
    def update(self, entity: T) -> None:
        """
        Docstring for update
        
        :param self: The repository instance (the current object on which the method is called).
        :param entity: The entity to update
        :type entity: T
        """
        ...

    @abstractmethod
    def insert(self, entity: T) -> None:
        """
        Docstring for insert
        
        :param self: The repository instance (the current object on which the method is called).
        :param entity: The new entity to insert
        :type entity: T
        """
        ...
