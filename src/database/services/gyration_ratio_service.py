from database.repositories.gyration_ratio_repository import GyrationRatioRepository
from database.models.gyration_ratio import GyrationRatio
from layout.layout import Layout

class GyrationRatioService():
    def __init__(self, gyration_ratio_repository : GyrationRatioRepository) -> None:
        self._gyration_ratio_repo = gyration_ratio_repository

    def add_or_update_gyration_ratio(self, atoms : int, cube_gr : int | None, sphere_gr : int | None, random_gr : int | None) -> GyrationRatio:
        gyration_ratio = GyrationRatio(
            atoms = atoms,
            cube_gr = cube_gr,
            sphere_gr = sphere_gr,
            random_gr = random_gr,
        )
        gyraton_record = self._gyration_ratio_repo.get_by_atoms(atoms)
        if gyraton_record is None:
            return self._gyration_ratio_repo.add(gyration_ratio)
        gyration_ratio.cube_gr = cube_gr if cube_gr is not None else gyraton_record.cube_gr
        gyration_ratio.sphere_gr = sphere_gr if sphere_gr is not None else gyraton_record.sphere_gr
        gyration_ratio.random_gr = random_gr if random_gr is not None else gyraton_record.random_gr
        return self._gyration_ratio_repo.update_gyration_ratios_by_id(gyraton_record.id, gyration_ratio)

    def get_all_gyration_ratios_with_layout(self, layout : Layout) -> list[GyrationRatio]:
        all_gyration_ratios = self._gyration_ratio_repo.get_all()
        if layout == Layout.CUBE:
            return [gr for gr in all_gyration_ratios if gr.cube_gr is not None]
        if layout == Layout.SPHERE:
            return [gr for gr in all_gyration_ratios if gr.sphere_gr is not None]
        if layout == Layout.RANDOM:
            return [gr for gr in all_gyration_ratios if gr.random_gr is not None]
        return []
