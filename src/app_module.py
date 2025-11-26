from injector import Module, singleton, provider
from sqlalchemy.orm import Session
from sqlalchemy.engine import Engine

from database.db_connect import get_engine, get_session
from database.repositories.gyration_ratio_repository import GyrationRatioRepository
from database.services.gyration_ratio_service import GyrationRatioService

class AppModule(Module):

    @singleton
    @provider
    def provide_engine(self) -> Engine:
        return get_engine()

    @provider
    def provide_session(self) -> Session:
        return next(get_session())

    @provider
    def provide_gyration_ratio_repository(self, session : Session) -> GyrationRatioRepository:
        return GyrationRatioRepository(session)

    @provider
    def provide_gyration_ratio_service(self, repo : GyrationRatioRepository) -> GyrationRatioService:
        return GyrationRatioService(repo)
