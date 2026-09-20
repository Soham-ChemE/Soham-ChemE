<p align="center"><img src="https://raw.githubusercontent.com/Soham-ChemE/Soham-ChemE/main/profile_banner.png" alt="Soham Kavathekar" width="100%"></p>

<p align="center">
<a href="https://www.linkedin.com/in/soham-kavathekar-72a22b246"><img src="https://img.shields.io/badge/LinkedIn-Soham%20Kavathekar-0b1220?style=flat-square&logo=linkedin&logoColor=22D3EE"></a>
<a href="mailto:stg3719@seas.upenn.edu"><img src="https://img.shields.io/badge/Email-stg3719%40seas.upenn.edu-0b1220?style=flat-square&logo=gmail&logoColor=22D3EE"></a>
<img src="https://img.shields.io/badge/Available-full--time%20from%20May%202027-0b1220?style=flat-square&logoColor=f5a524">
<img src="https://img.shields.io/badge/Philadelphia%2C%20PA-0b1220?style=flat-square">
</p>

Chemical engineer (MS, University of Pennsylvania, 2027) working across **batteries, semiconductor processing and materials modelling**. I build physics-based and data-driven models of energy materials and processes, then check them the way a fab or a cell line would: designed experiments, capability statistics, and re-running everything from raw data before believing a number. Hands-on with Li-ion cell electrochemistry, a manufacturing process-improvement project in industry, one peer-reviewed paper, one manuscript under revision and three patent filings.

---

## Featured work

<table>
<tr>
<td width="50%" valign="top">
<a href="https://github.com/Soham-ChemE/CathodeAI-Battery-Materials-Screener"><img src="https://raw.githubusercontent.com/Soham-ChemE/CathodeAI-Battery-Materials-Screener/main/hero.png" width="100%"></a>

**[CathodeAI](https://github.com/Soham-ChemE/CathodeAI-Battery-Materials-Screener)** · *manuscript under revision, Phys. Chem. Chem. Phys.*
Screens 2,774 Li-ion insertion electrodes from the Materials Project with a structure-resolved Degradation Screening Index. Ranks the durability of 11 experimental cathodes better than the metal-identity heuristic it replaces (Spearman 0.76 vs 0.55) and resolves three durability classes inside one composition. Every figure regenerates from cached data.
`Python` `pymatgen` `scikit-learn` `SHAP` `Materials Project API`
</td>
<td width="50%" valign="top">
<a href="https://github.com/Soham-ChemE/CVD-Reactor-Uniformity-COMSOL"><img src="https://raw.githubusercontent.com/Soham-ChemE/CVD-Reactor-Uniformity-COMSOL/main/hero_cvd.png" width="100%"></a>

**[CVD Reactor Uniformity](https://github.com/Soham-ChemE/CVD-Reactor-Uniformity-COMSOL)** · *COMSOL Multiphysics 6.4*
Diagnosed a mass-transfer-limited APCVD reactor and redesigned the inlet for a 300 mm wafer: within-wafer non-uniformity from 180 % to 3.3 %, coverage from 17 % to 92 %. A 14-run central composite design shows inlet velocity and wafer temperature are decoupled; a Gaussian-process surrogate (leave-one-out R² 0.94) propagates real MFC and thermocouple tolerances into a process-capability estimate.
`COMSOL` `DOE (pyDOE3)` `Gaussian process` `Monte Carlo Cpk`
</td>
</tr>
</table>

---

## Projects

| | Project | What it shows | Tools |
|---|---|---|---|
| 🔋 | [**CathodeAI**](https://github.com/Soham-ChemE/CathodeAI-Battery-Materials-Screener) | Structure-aware cathode screening; DSI durability index; Pareto and supply-chain analysis; honest negative result on ML for energy density; full reproducibility package | Python, pymatgen, scikit-learn, XGBoost, SHAP |
| 🏭 | [**CVD reactor uniformity**](https://github.com/Soham-ChemE/CVD-Reactor-Uniformity-COMSOL) | Laminar flow + heat transfer + species transport FEM of a poly-Si APCVD reactor; inlet redesign; CCD; GP surrogate; Cpk with sourced tolerances; 3D asymmetric-exhaust model | COMSOL 6.4, NumPy, scikit-learn |
| 🔥 | **Thermal-runaway propagation, tabless 4680 pack** | Coupled electrochemical-thermal FEM of a 20-cell pack (231 domains) with event-triggered cell failure; identifies an axial-conductivity propagation threshold near 1 to 1.25 W m⁻¹ K⁻¹ that separates tabbed from tabless behaviour | COMSOL Battery Design Module |
| ☀️ | [**ZnSe/CdTe thin-film solar cell**](https://github.com/Soham-ChemE/Perovskite-Solar-Cell-SCAPS1D-Optimization) | SCAPS-1D screening of ten electron-transport layers; Cs₂BiAgI₆ + Ni reaches a simulated 27.99 % PCE; Best Poster Award, ACC 2024; two granted design patents | SCAPS-1D |
| 🧪 | [**Ionic liquids at CNT interfaces**](https://github.com/Soham-ChemE/MD-IL-CNT-Interfacial-Interactions) | All-atom MD of four imidazolium ionic liquids in a (15,15) nanotube; chain length controls binding (to −8.75 kcal mol⁻¹ ion⁻¹) and conductivity (0.005 S m⁻¹ for [EMIM][BF₄]); *Structural Chemistry* 2024 | NAMD, OPLS-AA, VMD |
| ⚛️ | **Hybrid perovskite ferroelectrics** (Rappé Lab, with ORNL) | First-principles DFT on methylhydrazinium lead halides; Berry-phase polarisation of 5.6 µC cm⁻² within the experimental range; ongoing, unpublished | Quantum ESPRESSO, NERSC |

The thermal-runaway and DFT projects are not yet public repositories: the first is being written up and the second is collaborative work in progress.

---

## Hands-on and industry

- **Li-ion cell electrochemistry** (UPenn MSE 5550): cyclic voltammetry and galvanostatic cycling of commercial LiMn₂O₄ coin cells on a Bio-Logic VMP-300, C/10 to 2C, rate capability and capacity retention.
- **Chemical process intern, Lubrikote Specialities** (2025): DOE and SPC on a die-casting release-agent line, 12 % less downtime and 10 % less material waste; formulation, SOPs, KPI dashboards.
- **Process engineering intern, Lupin** (GMP API plant, 2023): 600 kL/day zero-liquid-discharge water reclamation, solvent-recovery distillation, HAZOP and permit-to-work audits.
- **Quality assurance intern, Britannia Industries** (2023): raw-material and in-process analytics on a 433,000 t/yr line; ISO 22000, ISO 9000, HACCP.

## Skills

**Process and yield**: DOE, SPC, Cpk, FMEA, root-cause analysis, SOP authoring · **Battery**: cell testing, CV, GCD, degradation and cycle-life analysis, thermal-runaway modelling · **Semiconductor**: device physics, CMOS operation, CVD process modelling, thin-film device simulation, cleanroom processing coursework · **Modelling**: COMSOL, SCAPS-1D, Quantum ESPRESSO, NAMD, Aspen HYSYS, DFT, MD, FEM, Gaussian-process surrogates · **Software**: Python (NumPy, pandas, scikit-learn, SHAP, matplotlib), MATLAB, LaTeX, Linux, HPC job scheduling · **Standards**: GMP, HAZOP, ISO 22000, ISO 9000, HACCP

## Publications, patents, awards

- Biswas R., Banerjee P., **Kavathekar S. S.**, "Molecular dynamics studies on interfacial interactions between imidazolium-based ionic liquids and carbon nanotubes", *Structural Chemistry* **35**, 1743–1753 (2024). [10.1007/s11224-024-02323-3](https://doi.org/10.1007/s11224-024-02323-3)
- **Kavathekar S.**, "Beyond heuristics: structure-aware screening reveals the limits of composition-based cathode design", under revision at *Phys. Chem. Chem. Phys.* (2026).
- Design patents (Government of India, co-inventor): Detachable Spiral Solar Panel, 434427-001 (granted Oct 2024); Dual-Layer Detachable Spiral Solar Panel, 459195-001 (granted May 2025); utility patent on the fabrication method under review.
- Best Poster Presentation Award, 61st Annual Convention of Chemists (ACC 2024), Indian Chemical Society.

## Education

**University of Pennsylvania**, MS Chemical and Biomolecular Engineering, 2025 to 2027 · Deputy Director to the President, Graduate and Professional Student Assembly · TA for Wharton MGMT 4020 and SEAS MEAM 2030
**Vellore Institute of Technology**, B.Tech Chemical Engineering, 2021 to 2025, GPA 3.88/4.0

<p align="center">
<img src="https://github-readme-stats.vercel.app/api?username=Soham-ChemE&show_icons=true&theme=tokyonight&hide_border=true&bg_color=0b1220&title_color=22d3ee&icon_color=22d3ee&text_color=c9d4e2" height="160">
<img src="https://github-readme-stats.vercel.app/api/top-langs/?username=Soham-ChemE&layout=compact&theme=tokyonight&hide_border=true&bg_color=0b1220&title_color=22d3ee&text_color=c9d4e2" height="160">
</p>
