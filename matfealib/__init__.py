"""MatFeaLib - Materials Feature Library."""

from matfealib.atomicfeatures.features import mendeleev
from matfealib.atomicfeatures.features import pymatgen
from matfealib.atomicfeatures.features import matminer
from matfealib.atomicfeatures.features import lda2015
from matfealib.atomicfeatures.features import (
        dft_pwlda,
        dft_pwlda_spins,
        dft_pbe,
        dft_pbe_spins,
        dft_pbesol,
        dft_pbesol_spins,
        dft_revpbe,
        dft_revpbe_spins,
        dft_pbe0,
        dft_pbe0_spins,
        dft_hse06,
        dft_hse06_spins,
        )

from matfealib.atomicfeatures.features import available_collection 
from matfealib.atomicfeatures.features import available_features

from matfealib.atomicfeatures.features import fetch_elemental_features
from matfealib.atomicfeatures.features import fetch_statistical_features

from matfealib.compositional.element_fraction import fetch_element_fraction
from matfealib.compositional.wstatistical import fetch_wstatistical_features

from matfealib.bulk.bulk import fetch_bulk_features

from matfealib.plot.periodic_table import periodic_table

__all__ = [
    "available_collection",
    "available_features",
    "fetch_elemental_features",
    "fetch_statistical_features",
    "mendeleev",
    "matminer",
    "pymatgen",
    "dft_pwlda",
    "dft_pwlda_spins",
    "dft_pbe",
    "dft_pbe_spins",
    "dft_pbesol",
    "dft_pbesol_spins",
    "dft_revpbe",
    "dft_revpbe_spins",
    "dft_pbe0",
    "dft_pbe0_spins",
    "dft_hse06",
    "dft_hse06_spins",
    "lda2015",
    "periodic_table",
    "fetch_element_fraction",
    "fetch_wstatistical_features",
    "fetch_bulk_features",
    ]
