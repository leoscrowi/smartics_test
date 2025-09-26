from src.infrastructure.contracts.repositories.expense import ExpenseRepository
from src.infrastructure.orm.db.expense.repositories import ExpenseDatabaseRepository
from src.infrastructure.usecases.expense import ExpenseUsecase


class ExpenseDatabaseRepositoryFactory:

    @staticmethod
    def get():
        return ExpenseDatabaseRepository()

class ExpenseRepositoryFactory:

    @staticmethod
    def get():
        db_repo = ExpenseDatabaseRepository.get()
        return ExpenseRepository(db_repo)

class ExpenseUseCaseFactory:

    @staticmethod
    def get():
        db_repo = ExpenseRepositoryFactory.get()
        return ExpenseUsecase(db_repo)


class ExpenseControllerFactory:

    @staticmethod
    def get():
        usecase = ExpenseUseCaseFactory.get()
        return