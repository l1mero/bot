from motor.motor_asyncio import AsyncIOMotorClient
from typing import Any, Dict


class MongoDB:
    def __init__(self, uri: str, db_name: str):
        """
        Инициализация подключения к базе данных MongoDB.

        :param uri: URI для подключения к MongoDB.
        :param db_name: Имя базы данных, с которой будем работать.
        """
        self.client = AsyncIOMotorClient(uri)
        self.db = self.client[db_name]

    async def insert_one(self, collection_name: str, document: Dict[str, Any]) -> str:
        """
        Вставка одного документа в коллекцию.

        :param collection_name: Название коллекции.
        :param document: Документ для вставки.
        :return: ID вставленного документа.
        """
        collection = self.db[collection_name]
        result = await collection.insert_one(document)
        return str(result.inserted_id)

    async def find_one(self, collection_name: str, query: Dict[str, Any]) -> Dict[str, Any]:
        """
        Поиск одного документа по запросу.

        :param collection_name: Название коллекции.
        :param query: Запрос для поиска.
        :return: Найденный документ.
        """
        collection = self.db[collection_name]
        document = await collection.find_one(query)
        return document

    async def update_one(self, collection_name: str, query: Dict[str, Any], update: Dict[str, Any]) -> bool:
        """
        Обновление одного документа по запросу.

        :param collection_name: Название коллекции.
        :param query: Запрос для поиска документа.
        :param update: Обновления для документа.
        :return: True если обновление прошло успешно, иначе False.
        """
        collection = self.db[collection_name]
        result = await collection.update_one(query, update)
        return result.modified_count > 0

    async def delete_one(self, collection_name: str, query: Dict[str, Any]) -> bool:
        """
        Удаление одного документа по запросу.

        :param collection_name: Название коллекции.
        :param query: Запрос для поиска документа.
        :return: True если удаление прошло успешно, иначе False.
        """
        collection = self.db[collection_name]
        result = await collection.delete_one(query)
        return result.deleted_count > 0

    async def find_all(self, collection_name: str, query: Dict[str, Any] = {}) -> list:
        """
        Поиск всех документов по запросу.

        :param collection_name: Название коллекции.
        :param query: Запрос для поиска (по умолчанию пустой).
        :return: Список найденных документов.
        """
        collection = self.db[collection_name]
        documents = []
        async for document in collection.find(query):
            documents.append(document)
        return documents