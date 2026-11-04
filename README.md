<p align="center"><a href="https://soham-cheme.github.io/Soham-ChemE/"><img src="docs/assets/hero.svg" alt="Soham Kavathekar: six project marks drawn from each project's own data, lighting up in turn" width="100%"></a></p>

<p align="center"><b><a href="https://soham-cheme.github.io/Soham-ChemE/">Open the live page</a></b> · one scroll-driven 3D scene that flies through all six projects, each drawn from its own data</p>

<p align="center">
<a href="https://www.linkedin.com/in/soham-kavathekar-cheme"><img src="https://img.shields.io/badge/LinkedIn-soham--kavathekar--cheme-0a0a0b?style=for-the-badge&logo=linkedin&logoColor=22d3ee" alt="LinkedIn"></a>
<a href="mailto:stg3719@seas.upenn.edu"><img src="https://img.shields.io/badge/Email-stg3719%40seas.upenn.edu-0a0a0b?style=for-the-badge&logo=gmail&logoColor=ff7a1a" alt="Email"></a>
<a href="https://soham-cheme.github.io/Soham-ChemE/"><img src="https://img.shields.io/badge/Live%20project%20pages-6%20interactive%203D%20sites-0a0a0b?style=for-the-badge&logoColor=a78bfa" alt="Live project pages"></a>
</p>

<h3 align="center">Soham Kavathekar · MS Chemical &amp; Biomolecular Engineering, University of Pennsylvania (May 2027) · process engineering and batteries</h3>

<p align="center">Physics-based and data-driven models of energy materials and processes, checked the way a fab or a cell line would check them:<br>designed experiments, capability statistics, and every number re-run from raw data before it is believed.</p>

---

## Projects

Each card carries one number that is reproduced from the repository's own data (the audit trail is in every repo's `docs/CLAIMS.md`) and links to the code and to a live page with an interactive 3D view of the work.

<table>
<tr>
<td width="50%" valign="top">

### <img src="https://img.shields.io/badge/-%20-22d3ee?style=flat-square" alt=""> CathodeAI: structure-aware cathode screening
**2,774** Li-ion insertion electrodes from the Materials Project screened through an eight-layer funnel. A three-descriptor Degradation Screening Index ranks 11 experimentally characterised cathodes at Spearman ρ = 0.76 (p = 0.007), against 0.55 for volume strain alone, and puts 10 of 11 on the right side of the durable split. Sole author; preprint on ChemRxiv, manuscript under revision at *Phys. Chem. Chem. Phys.*
`Python` `pymatgen` `scikit-learn` `SHAP`
[Repository](https://github.com/Soham-ChemE/CathodeAI-Battery-Materials-Screener) · [Live page](https://soham-cheme.github.io/CathodeAI-Battery-Materials-Screener/)

</td>
<td width="50%" valign="top">

### <img src="https://img.shields.io/badge/-%20-ff7a1a?style=flat-square" alt=""> LiMn₂O₄ half cell: PyBaMM rate model on my own data
Commercial LMO half cells cycled on a Bio-Logic VMP-300 (CV at 0.1 to 0.3 mV/s; C/10 to 2C). A Doyle-Fuller-Newman model with three fitted parameters (**26 mV** training RMSE on C/5 and C/2 only) predicts the unseen 2C average voltage within 17 mV and all six CV peaks within 80 mV, then names the 2C loss: 74 % ohmic, 17 % charge transfer, 6 % diffusion. 58 automated tests.
`PyBaMM` `SciPy` `pytest`
[Repository](https://github.com/Soham-ChemE/LMO-Cathode-Rate-Model-PyBaMM) · [Live page](https://soham-cheme.github.io/LMO-Cathode-Rate-Model-PyBaMM/)

</td>
</tr>
<tr>
<td width="50%" valign="top">

### <img src="https://img.shields.io/badge/-%20-f43f5e?style=flat-square" alt=""> CVD reactor uniformity in COMSOL
A 300 mm single-wafer showerhead reactor, 2D axisymmetric, flow + heat + species + surface kinetics. The 180 % non-uniformity was root-caused as mass-transfer limited (Da above 10) and fixed at the inlet: widening it from 10 to 150 mm gives 6.1 %, and a 14-run central composite design reaches **3.3 %** at 0.07 m/s. Gaussian-process surrogate (leave-one-out R² 0.944), 10,000-draw Monte Carlo on MFC and thermocouple tolerances, 3D model with asymmetric exhaust (5.9 %).
`COMSOL` `DOE` `Gaussian process` `Monte Carlo`
[Repository](https://github.com/Soham-ChemE/CVD-Reactor-Uniformity-COMSOL) · [Live page](https://soham-cheme.github.io/CVD-Reactor-Uniformity-COMSOL/)

</td>
<td width="50%" valign="top">

### <img src="https://img.shields.io/badge/-%20-a78bfa?style=flat-square" alt=""> Ionic liquids at carbon nanotube walls (MD)
All-atom NAMD simulations of four imidazolium [BF₄] ionic liquids confined in a (15,15) nanotube: chain length sets orientation, binding and mobility, with [OMIM]⁺ binding at **−8.75 kcal mol⁻¹ per ion**. Co-author, *Structural Chemistry* (Springer Nature, 2024), doi 10.1007/s11224-024-02323-3. The repository ships the 19,260-atom minimised structure, which the live page renders.
`NAMD` `OPLS-AA` `VMD`
[Repository](https://github.com/Soham-ChemE/MD-IL-CNT-Interfacial-Interactions) · [Live page](https://soham-cheme.github.io/MD-IL-CNT-Interfacial-Interactions/)

</td>
</tr>
<tr>
<td width="50%" valign="top">

### <img src="https://img.shields.io/badge/-%20-f59e0b?style=flat-square" alt=""> ZnSe/CdTe thin-film cell in SCAPS-1D
FTO/ZnSe/CdTe heterojunction with ten electron-transport layers and nine back-contact metals screened in a six-parameter design of experiments. Best simulated efficiency **27.99 %** with a Cs₂BiAgI₆ ETL and nickel contact (V<sub>OC</sub> 1.21 V, J<sub>SC</sub> 25.96 mA cm⁻², FF 89.3 %), labelled as a simulation ceiling. Spiral panel architecture with 17.9 % more active area: two granted Indian design registrations, one utility application under review. Best Poster Award, 61st Annual Convention of Chemists.
`SCAPS-1D` `drift-diffusion` `device physics`
[Repository](https://github.com/Soham-ChemE/Perovskite-Solar-Cell-SCAPS1D-Optimization) · [Live page](https://soham-cheme.github.io/Perovskite-Solar-Cell-SCAPS1D-Optimization/)

</td>
<td width="50%" valign="top">

### <img src="https://img.shields.io/badge/-%20-f97316?style=flat-square" alt=""> 4680 thermal-runaway propagation in COMSOL
A 20-cell 5s4p pack of 4680 cells adapted from COMSOL's validated propagation model: 25 Ah and about 110 kJ per cell, 80 °C trigger. Twelve transient one-hour studies over base cooling from 0 to 2,000 W m⁻² K⁻¹ locate a sharp threshold in through-layer (radial) conductivity between **1.0 and 1.25 W m⁻¹ K⁻¹**: below it about 13 of 20 cells cascade within the hour, above it propagation stops at the initiating cell. The model file no longer exists, so the repository is the written record, a claims audit, the scaling arguments as tested code and a reduced-order surrogate labelled as such.
`COMSOL Battery Design Module` `reduced-order model` `pytest`
[Repository](https://github.com/Soham-ChemE/4680-Thermal-Runaway-Propagation-COMSOL) · [Live page](https://soham-cheme.github.io/4680-Thermal-Runaway-Propagation-COMSOL/)

</td>
</tr>
</table>

Also ongoing, in the Rappé group at Penn: Berry-phase spontaneous polarization of MHy₂PbBr₄ computed at 5.6 µC cm⁻², within the 4.6 to 5.8 µC cm⁻² experimental range (DFT, Quantum ESPRESSO, collaboration with Oak Ridge CNMS).

## Toolkit

COMSOL Multiphysics (Battery Design Module) · PyBaMM · Python (NumPy, pandas, scikit-learn, SciPy, SHAP, matplotlib) · DFT with Quantum ESPRESSO · SCAPS-1D · NAMD and VMD · DOE (central composite, factorial), SPC, Cpk and Monte Carlo tolerance analysis · Aspen HYSYS · MATLAB · LaTeX · Linux and HPC job scheduling

## Experience

Chemical process intern, Lubrikote Specialities (2025): DOE and SPC on a die-casting release-agent line, formulation, SOPs and KPI dashboards · Process engineering intern, Lupin (GMP API plant, 2023): zero-liquid-discharge water reclamation, solvent-recovery distillation, HAZOP and permit-to-work audits · Quality assurance intern, Britannia Industries (2023): raw-material and in-process analytics under ISO 22000, ISO 9000 and HACCP.

## Publications, patents, awards

- Biswas R., Banerjee P., **Kavathekar S. S.**, "Molecular dynamics studies on interfacial interactions between imidazolium-based ionic liquids and carbon nanotubes", *Structural Chemistry* **35**, 1743–1753 (2024). [10.1007/s11224-024-02323-3](https://doi.org/10.1007/s11224-024-02323-3)
- **Kavathekar S.**, CathodeAI: structure-aware degradation screening of lithium-ion cathodes. Preprint, ChemRxiv, [10.26434/chemrxiv.15010709/v1](https://doi.org/10.26434/chemrxiv.15010709/v1); manuscript under revision at *Phys. Chem. Chem. Phys.* (2026).
- Design registrations (Government of India, co-inventor): Detachable Spiral Solar Panel, 434427-001 (granted Oct 2024); Dual-Layer Detachable Spiral Solar Panel, 459195-001 (granted May 2025); utility application on the fabrication method under review.
- Best Poster Award, 61st Annual Convention of Chemists (ACC 2024), Indian Chemical Society.

## Education

**University of Pennsylvania**, MS Chemical and Biomolecular Engineering, 2025 to 2027, GPA 3.45/4.0 · Deputy Director to the President of GAPSA, Penn's graduate student government, which represents more than 12,000 students
**Vellore Institute of Technology**, B.Tech Chemical Engineering, 2021 to 2025, GPA 3.88/4.0

## Contact

[stg3719@seas.upenn.edu](mailto:stg3719@seas.upenn.edu) · [linkedin.com/in/soham-kavathekar-cheme](https://www.linkedin.com/in/soham-kavathekar-cheme) · [github.com/Soham-ChemE](https://github.com/Soham-ChemE) · [live project pages](https://soham-cheme.github.io/Soham-ChemE/)
