from src.infrastructure.contracts.repositories.category import CategoryRepository
from src.infrastructure.controllers.category import CategoryController
from src.infrastructure.orm.db.category.repositories import CategoryDatabaseRepository
from src.infrastructure.usecases.category import CategoryUsecase


class CategoryDatabaseRepositoryFactory:

    @staticmethod
    def get():
        return CategoryDatabaseRepository()

class CategoryRepositoryFactory:

    @staticmethod
    def get():
        db_repo = CategoryDatabaseRepository.get()
        return CategoryRepository(db_repo)

class CategoryUseCaseFactory:

    @staticmethod
    def get():
        db_repo = CategoryRepositoryFactory.get()
        return CategoryUsecase(db_repo)


class CategoryControllerFactory():

    @staticmethod
    def get():
        usecase = CategoryUseCaseFactory.get()
        return CategoryController(usecase)