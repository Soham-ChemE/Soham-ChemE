<p align="center"><img src="https://raw.githubusercontent.com/Soham-ChemE/Soham-ChemE/main/profile_banner.png" alt="Soham Kavathekar" width="100%"></p>

<p align="center">
<a href="https://www.linkedin.com/in/soham-kavathekar-cheme"><img src="https://img.shields.io/badge/LinkedIn-Soham%20Kavathekar-0a0a0b?style=for-the-badge&logo=linkedin&logoColor=22d3ee"></a>
<a href="mailto:stg3719@seas.upenn.edu"><img src="https://img.shields.io/badge/Email-stg3719%40seas.upenn.edu-0a0a0b?style=for-the-badge&logo=gmail&logoColor=ff7a1a"></a>
<img src="https://img.shields.io/badge/UPenn%20MS%20ChemE-class%20of%202027-0a0a0b?style=for-the-badge&logoColor=a78bfa">
<img src="https://img.shields.io/badge/open%20to-internships%20%C2%B7%20full--time%20from%20May%202027-0a0a0b?style=for-the-badge&logoColor=f59e0b">
</p>

<h3 align="center">I build physics-based and data-driven models of energy materials and processes, then check them the way a fab or a cell line would.</h3>

<p align="center">Designed experiments · capability statistics · every number re-run from raw data before it is believed.<br>
Batteries, semiconductor processing, thin-film photovoltaics, first-principles materials.</p>

<table align="center">
<tr>
<td align="center"><b>2,774</b><br><sub>Li-ion electrodes screened,<br>structure-resolved</sub></td>
<td align="center"><b>180 % → 3.3 %</b><br><sub>CVD within-wafer<br>non-uniformity</sub></td>
<td align="center"><b>ρ = 0.76</b><br><sub>durability index vs 11<br>experimental cathodes</sub></td>
<td align="center"><b>27.99 %</b><br><sub>simulated PCE, lead-free<br>ETL on ZnSe/CdTe</sub></td>
<td align="center"><b>1 + 1 + 3</b><br><sub>paper · manuscript under<br>revision · patents</sub></td>
</tr>
</table>

---

## Featured

<table>
<tr>
<td width="50%" valign="top">
<a href="https://github.com/Soham-ChemE/CathodeAI-Battery-Materials-Screener"><img src="https://raw.githubusercontent.com/Soham-ChemE/CathodeAI-Battery-Materials-Screener/main/hero.png" width="100%"></a>

**[CathodeAI](https://github.com/Soham-ChemE/CathodeAI-Battery-Materials-Screener)** · *manuscript under revision, Phys. Chem. Chem. Phys.*
Structure-aware screening of 2,774 Materials Project Li insertion electrodes. A transparent Degradation Screening Index ranks the durability of 11 experimental cathodes better than the metal-identity heuristic it replaces (Spearman 0.76 vs 0.55), and polymorph-resolved data show one composition spanning three durability classes. Includes an honest negative result on ML for energy density. Every figure regenerates from cached data.
<br>`Python` `pymatgen` `scikit-learn` `SHAP` `Materials Project API`
</td>
<td width="50%" valign="top">
<a href="https://github.com/Soham-ChemE/CVD-Reactor-Uniformity-COMSOL"><img src="https://raw.githubusercontent.com/Soham-ChemE/CVD-Reactor-Uniformity-COMSOL/main/hero_cvd.png" width="100%"></a>

**[CVD Reactor Uniformity](https://github.com/Soham-ChemE/CVD-Reactor-Uniformity-COMSOL)** · *COMSOL Multiphysics 6.4*
Diagnosed a mass-transfer-limited APCVD reactor and redesigned the inlet for a 300 mm wafer: non-uniformity 180 % → 3.3 %, coverage 17 % → 92 %. A 14-run central composite design shows inlet velocity and wafer temperature are decoupled; a Gaussian-process surrogate (LOO R² 0.94) propagates sourced MFC and thermocouple tolerances into a process-capability estimate. 3D model with asymmetric exhaust included.
<br>`COMSOL` `DOE` `Gaussian process` `Monte Carlo Cpk`
</td>
</tr>
<tr>
<td width="50%" valign="top">
<a href="https://github.com/Soham-ChemE/Perovskite-Solar-Cell-SCAPS1D-Optimization"><img src="https://raw.githubusercontent.com/Soham-ChemE/Perovskite-Solar-Cell-SCAPS1D-Optimization/main/hero_scaps.png" width="100%"></a>

**[ZnSe/CdTe Solar Cell Optimisation](https://github.com/Soham-ChemE/Perovskite-Solar-Cell-SCAPS1D-Optimization)** · *SCAPS-1D · Best Poster, ACC 2024*
Ten electron-transport layers and nine back-contact metals screened in a lead-free FTO/ZnSe/CdTe/ETL/Ni stack; Cs₂BiAgI₆ with Ni reaches a simulated 27.99 %. Layer-thickness and temperature sweeps, Schottky-barrier explanation of the contact series, and every figure regenerated from the raw SCAPS exports. Two granted design patents on the panel geometry.
<br>`SCAPS-1D` `drift-diffusion` `device physics`
</td>
<td width="50%" valign="top">
<a href="https://github.com/Soham-ChemE/MD-IL-CNT-Interfacial-Interactions"><img src="https://raw.githubusercontent.com/Soham-ChemE/MD-IL-CNT-Interfacial-Interactions/main/hero_md.png" width="100%"></a>

**[Ionic Liquids at Carbon Nanotube Interfaces](https://github.com/Soham-ChemE/MD-IL-CNT-Interfacial-Interactions)** · *Structural Chemistry, 2024*
All-atom MD of four imidazolium ionic liquids in a (15,15) nanotube. Cation chain length controls orientation, binding (to −8.75 kcal mol⁻¹ per ion) and ion mobility; [EMIM][BF₄] is the best conductor at 0.005 S m⁻¹. Peer-reviewed and published with Springer Nature.
<br>`NAMD` `OPLS-AA` `VMD`
</td>
</tr>
</table>

## Also in progress

| | Project | Status | What it shows |
|---|---|---|---|
| 🔥 | **Thermal-runaway propagation in a tabless 4680 pack** | being written up | Coupled electrochemical-thermal FEM of a 20-cell pack (231 domains) with event-triggered failure; a propagation threshold in axial conductivity near 1 to 1.25 W m⁻¹ K⁻¹ separates tabbed from tabless behaviour, and the envelope over cooling coefficient 0 to 2000 W m⁻² K⁻¹ is mapped. COMSOL Battery Design Module. |
| ⚛️ | **Hybrid perovskite ferroelectrics** (Rappé Lab, with Oak Ridge National Laboratory) | ongoing, unpublished | First-principles DFT (Quantum ESPRESSO, NERSC) on methylhydrazinium lead halides; Berry-phase polarisation of 5.6 µC cm⁻² within the experimental range; halide defect formation and migration. |

## How I work

- **Re-run before believing.** When two referees questioned CathodeAI, I re-ran the whole pipeline from cached data, found the original submission's errors myself, disclosed them and rebuilt the paper around what survived.
- **Treat a model like a process.** The CVD project is not a pretty flow field: it is a designed experiment, a surrogate, a tolerance stack-up and a capability number, with every one of the 13 modelling choices sourced or declared.
- **Report negatives.** The ML model that adds nothing beyond V × C × ρ is in the paper. The efficiency that is a ceiling, not a forecast, is labelled as one.

## Hands-on and industry

- **Li-ion cell electrochemistry** (UPenn MSE 5550): cyclic voltammetry and galvanostatic cycling of commercial LiMn₂O₄ coin cells on a Bio-Logic VMP-300, C/10 to 2C, rate capability and capacity retention.
- **Chemical process intern, Lubrikote Specialities** (2025): DOE and SPC on a die-casting release-agent line, 12 % less downtime and 10 % less material waste; high-temperature formulation, SOPs, KPI dashboards.
- **Process engineering intern, Lupin** (GMP API plant, 2023): 600 kL/day zero-liquid-discharge water reclamation, solvent-recovery distillation, HAZOP and permit-to-work audits.
- **Quality assurance intern, Britannia Industries** (2023): raw-material and in-process analytics on a 433,000 t/yr line; ISO 22000, ISO 9000, HACCP.

## Skills

| | |
|---|---|
| **Process and yield** | DOE (CCD, factorial), SPC, Cpk, Monte Carlo tolerance analysis, FMEA, root-cause and failure analysis, SOP authoring |
| **Battery** | cell testing, CV, GCD, rate capability, degradation and cycle-life analysis, cathode screening, thermal-runaway and pack-safety modelling |
| **Semiconductor and devices** | device physics, CMOS and MOSFET operation, CVD transport and kinetics, thin-film device simulation, cleanroom and nanofabrication coursework |
| **Modelling** | COMSOL Multiphysics (Battery Design Module), SCAPS-1D, Quantum ESPRESSO, VESTA, NAMD, Aspen HYSYS, DFT, MD, FEM, Gaussian-process surrogates |
| **Software** | Python (NumPy, pandas, scikit-learn, SHAP, matplotlib, SciPy), MATLAB, LaTeX, Linux, NERSC HPC job scheduling, Fusion 360, AutoCAD |
| **Standards** | GMP, HAZOP, ISO 22000, ISO 9000, HACCP |

## Publications, patents, awards

- Biswas R., Banerjee P., **Kavathekar S. S.**, "Molecular dynamics studies on interfacial interactions between imidazolium-based ionic liquids and carbon nanotubes", *Structural Chemistry* **35**, 1743–1753 (2024). [10.1007/s11224-024-02323-3](https://doi.org/10.1007/s11224-024-02323-3)
- **Kavathekar S.**, "Beyond heuristics: structure-aware screening reveals the limits of composition-based cathode design", under revision at *Phys. Chem. Chem. Phys.* (2026).
- Design patents (Government of India, co-inventor): Detachable Spiral Solar Panel, 434427-001 (granted Oct 2024); Dual-Layer Detachable Spiral Solar Panel, 459195-001 (granted May 2025); utility patent on the fabrication method under review.
- Best Poster Presentation Award, 61st Annual Convention of Chemists (ACC 2024), Indian Chemical Society.

## Education and service

**University of Pennsylvania**, MS Chemical and Biomolecular Engineering, 2025 to 2027 · Deputy Director to the President, Graduate and Professional Student Assembly (12,000+ students) · TA for Wharton MGMT 4020 and SEAS MEAM 2030
**Vellore Institute of Technology**, B.Tech Chemical Engineering, 2021 to 2025, GPA 3.88/4.0

<p align="center">
<img src="https://github-readme-stats.vercel.app/api?username=Soham-ChemE&show_icons=true&hide_border=true&bg_color=0a0a0b&title_color=22d3ee&icon_color=ff7a1a&text_color=e5e7eb" height="160">
<img src="https://github-readme-stats.vercel.app/api/top-langs/?username=Soham-ChemE&layout=compact&hide_border=true&bg_color=0a0a0b&title_color=22d3ee&text_color=e5e7eb" height="160">
</p>
