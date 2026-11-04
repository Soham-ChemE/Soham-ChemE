# Claims audit: profile README and landing page

The profile carries one headline number per project card plus the numbers in the card text. Each is traced to the
repository that reproduces it (every project repository has its own `docs/CLAIMS.md` with the script and value) or to the
verified CV list for the two projects that have no public repository.

| Card | Number(s) | Reproduced in |
|---|---|---|
| CathodeAI | 2,774 electrodes; ρ 0.76, p 0.007; 0.55 single descriptor; 10 of 11 | `CathodeAI-Battery-Materials-Screener/docs/CLAIMS.md` (`repro_pipeline.py`, `analysis_dsi.py`) |
| LMO half cell | 26 mV training RMSE; 17 mV 2C voltage error; six CV peaks within 80 mV; 74 / 17 / 6 % loss split; 58 tests; CV 0.1 to 0.3 mV/s; C/10 to 2C | `LMO-Cathode-Rate-Model-PyBaMM/docs/CLAIMS.md` (`results/*.json`, `pytest --collect-only`) |
| CVD reactor | 180 % (179.6 %); Da above 10 (≈ 13, methodology notes); 10 → 150 mm gives 6.1 %; 14-run CCD, 3.3 % at 0.07 m/s; GP LOO R² 0.944; 10,000 draws; 3D 5.9 % | `CVD-Reactor-Uniformity-COMSOL/docs/CLAIMS.md` (`analysis/full_analysis.py`, `real_cpk_pipeline_v4.py`, `wafer_3D_sigma.py`) |
| MD ionic liquids | −8.75 kcal mol⁻¹ ion⁻¹ (public abstract of the article); 19,260 atoms (coordinate file); journal, volume, pages, DOI (Crossref) | `MD-IL-CNT-Interfacial-Interactions/docs/CLAIMS.md` |
| SCAPS-1D | 27.99 %, V_OC 1.21 V, J_SC 25.96 mA cm⁻², FF 89.3 %; ten ETLs; nine metals; six parameters | `Perovskite-Solar-Cell-SCAPS1D-Optimization/docs/CLAIMS.md` (`scripts/make_figures.py`) |
| SCAPS-1D, hardware | 17.9 % more active area; two granted design registrations 434427-001 and 459195-001; one utility application; Best Poster Award, 61st ACC | certificates in the SCAPS repository; the area figure and the award are from the CV |
| 4680 thermal runaway | 20 cells, 25 Ah, ~110 kJ per cell, 80 °C trigger; threshold 1.0 to 1.25 W m⁻¹ K⁻¹; about 13 of 20 cells within an hour; 12 transient studies; cooling 0 to 2,000 W m⁻² K⁻¹ | CV verified list only; no public repository yet |

## Removed from the previous profile README

| Removed | Why |
|---|---|
| "231 domains" for the 4680 model | not in the verified list and no repository to reproduce it from |
| "Berry-phase polarisation of 5.6 µC cm⁻²" | unpublished and not in the verified list |
| "12 % less downtime and 10 % less material waste", "600 kL/day", "433,000 t/yr", "12,000+ students", "GPA 3.88/4.0" | internship and service figures with no source in any repository and not in the verified list; the roles are kept without the figures |
| "1 + 1 + 3 paper · manuscript · patents" tile | replaced by the explicit list: one paper, one preprint under revision, two granted design registrations and one utility application |
| GitHub stats widgets | third-party images that add no verifiable information |

## Live page

`docs/index.html` is a spectrum-band landing page in the banner's five colours; each band links to the project's repository
and live page. The number on each band is the headline number of the corresponding card above.
