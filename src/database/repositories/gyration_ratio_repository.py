from sqlalchemy.orm import Session

from database.models.gyration_ratio import GyrationRatio

class GyrationRatioRepository():
    def __init__(self, session : Session) -> None:
        self._session = session

    def get_all(self) -> list[GyrationRatio]:
        return self._session.query(GyrationRatio).all()

    def get_by_atoms(self, atoms : int) -> GyrationRatio | None:
        return (
            self._session.query(GyrationRatio)
            .filter(GyrationRatio.atoms == atoms)
            .first()
        )
    
    def add(self, gyration_ratio : GyrationRatio) -> GyrationRatio:
        self._session.add(gyration_ratio)
        self._session.commit()
        self._session.refresh(gyration_ratio)
        return gyration_ratio

    def update_gyration_ratios_by_id(self, id: int, gyration_ratio : GyrationRatio) -> int:
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
        self._session.query(GyrationRatio).delete()
        self._session.commit()

