# Theme F (F5): shift current sigma_zzz for 9 cubic CsBX3 under [001] polar displacement

sigma_zzz(omega) for B=Ge/Sn/Pb x X=Cl/Br/I (Kashikar-13 TB, P4mm, delta in {0.10,0.15,0.20} A).
Method: Fregoso 2017 Eq.(C2) TB generalized derivative (w-term); sign anchored on Rice-Mele
Eq.(D15)/(D16) (F4-3) and Tan&Rappe 2016 Eq.14 symmetry laws (F4-2). Relative units.

Reproduce:
    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONPATH=src python scripts/scan_shift_current_9materials.py production

Outputs: outputs/raw/sigma_zzz_9materials.csv, outputs/figures/sigma_zzz_9materials.png,
convergence/ (k/eta/omega studies). See MANIFEST.json key_numbers.


