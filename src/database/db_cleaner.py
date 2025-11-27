from DI_container import injector
from database.services.gyration_ratio_service import GyrationRatioService

class DbCleaner():
    def __init__(self, enable_clean : bool) -> None:
        self._gyratio_ratio_service = injector.get(GyrationRatioService)
        if enable_clean:
            self._clean_db()

    def _clean_db(self) -> None:
        """
        Clean the database by removing all entries from the gyration ratio table.
        """
        self._gyratio_ratio_service.delete_all_data()