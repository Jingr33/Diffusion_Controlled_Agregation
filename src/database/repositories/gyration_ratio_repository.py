from sqlalchemy.orm import Session

from database.models.gyration_ratio import GyrationRatio

class GyrationRatioRepository():
    """
    Data access layer for gyration ratio records.
    """
    def __init__(self, session: Session) -> None:
        """Initialize repository with database session.
        
        Args:
            session (Session): SQLAlchemy session for database operations.
        """
        self._session = session

    def get_all(self) -> list[GyrationRatio]:
        """Retrieve all gyration ratio records.
        
        Returns:
            list[GyrationRatio]: All records from the database.
        """
        return self._session.query(GyrationRatio).all()

    def get_by_atoms(self, atoms: int) -> GyrationRatio | None:
        """Retrieve gyration ratio record by atom count.
        
        Args:
            atoms (int): Number of atoms to search for.
        
        Returns:
            GyrationRatio | None: Record if found, None otherwise.
        """
        return (
            self._session.query(GyrationRatio)
            .filter(GyrationRatio.atoms == atoms)
            .first()
        )
    
    def add(self, gyration_ratio: GyrationRatio) -> GyrationRatio:
        """Add a new gyration ratio record to the database.
        
        Args:
            gyration_ratio (GyrationRatio): Record to add.
        
        Returns:
            GyrationRatio: Added record with ID assigned.
        """
        self._session.add(gyration_ratio)
        self._session.commit()
        self._session.refresh(gyration_ratio)
        return gyration_ratio

    def update_gyration_ratios_by_id(self, id: int, gyration_ratio: GyrationRatio) -> int:
        """Update gyration ratio values for a specific record.
        
        Args:
            id (int): ID of the record to update.
            gyration_ratio (GyrationRatio): Object containing new values.
        
        Returns:
            int: Number of rows updated.
        """
        rows = (
            self._session.query(GyrationRatio)
            .filter(GyrationRatio.id == id)
            .update({"cube_gr": gyration_ratio.cube_gr,
                     "sphere_gr": gyration_ratio.sphere_gr,
                     "random_gr": gyration_ratio.random_gr}, 
                     synchronize_session="fetch")
        )
        self._session.commit()
        return rows

    def delete_all(self) -> None:
        """Delete all gyration ratio records from the database."""
        self._session.query(GyrationRatio).delete()
        self._session.commit()

