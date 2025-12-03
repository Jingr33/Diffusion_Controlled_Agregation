from DI_container import injector
from database.services.gyration_ratio_service import GyrationRatioService

class DbCleaner():
    """
    Manages database cleaning operations.
    """
    def __init__(self, enable_clean: bool) -> None:
        """Initialize cleaner and optionally clean database.
        
        Args:
            enable_clean (bool): If True, removes all entries from gyration ratio table.
        """
        self._gyratio_ratio_service = injector.get(GyrationRatioService)
        if enable_clean:
            self._clean_db()

    def _clean_db(self) -> None:
        """
        Clean the database by removing all entries from the gyration ratio table.
        """
        self._gyratio_ratio_service.delete_all_data()