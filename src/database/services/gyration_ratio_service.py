from database.repositories.gyration_ratio_repository import GyrationRatioRepository
from database.models.gyration_ratio import GyrationRatio
from layout.layout import Layout

class GyrationRatioService():
    """
    Business logic layer for gyration ratio operations.
    """
    def __init__(self, gyration_ratio_repository: GyrationRatioRepository) -> None:
        """Initialize service with repository.
        
        Args:
            gyration_ratio_repository (GyrationRatioRepository): Data access layer.
        """
        self._gyration_ratio_repo = gyration_ratio_repository

    def add_or_update_gyration_ratio(self, atoms: int, cube_gr: float | None, sphere_gr: float | None, random_gr: float | None) -> GyrationRatio:
        """Add or update a gyration ratio record.
        
        Args:
            atoms (int): Number of atoms.
            cube_gr (float | None): Radius of gyration for cube layout.
            sphere_gr (float | None): Radius of gyration for sphere layout.
            random_gr (float | None): Radius of gyration for random layout.
        
        Returns:
            GyrationRatio: Added or updated record.
        """
        gyration_ratio = GyrationRatio(
            atoms = atoms,
            cube_gr = cube_gr,
            sphere_gr = sphere_gr,
            random_gr = random_gr,
        )
        gyration_record = self._gyration_ratio_repo.get_by_atoms(atoms)
        if gyration_record is None:
            return self._gyration_ratio_repo.add(gyration_ratio)
        gyration_ratio.cube_gr = cube_gr if cube_gr is not None else gyration_record.cube_gr
        gyration_ratio.sphere_gr = sphere_gr if sphere_gr is not None else gyration_record.sphere_gr
        gyration_ratio.random_gr = random_gr if random_gr is not None else gyration_record.random_gr
        return self._gyration_ratio_repo.update_gyration_ratios_by_id(gyration_record.id, gyration_ratio)

    def get_all_gyration_ratios_with_layout(self, layout: Layout) -> list[GyrationRatio]:
        """Retrieve all gyration ratios for a specific layout.
        
        Args:
            layout (Layout): Type of layout to filter by.
        
        Returns:
            list[GyrationRatio]: Records with non-null gyration radius for the layout.
        """
        all_gyration_ratios = self._gyration_ratio_repo.get_all()
        if layout == Layout.CUBE:
            return [gr for gr in all_gyration_ratios if gr.cube_gr is not None]
        if layout == Layout.SPHERE:
            return [gr for gr in all_gyration_ratios if gr.sphere_gr is not None]
        if layout == Layout.RANDOM:
            return [gr for gr in all_gyration_ratios if gr.random_gr is not None]
        return []

    def delete_all_data(self) -> None:
        """Delete all entries from the gyration ratio table."""
        self._gyration_ratio_repo.delete_all()