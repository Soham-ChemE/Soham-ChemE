# Claims audit: profile README and landing page

The profile carries one headline number per project card plus the numbers in the card text. Each is traced to the
repository that reproduces it (every project repository has its own `docs/CLAIMS.md` with the script and value) or to the
verified CV list for the two projects that have no public repository.

| Card | Number(s) | Reproduced in |
|---|---|---|
| ALD chamber-to-feature (OpenFOAM) | 0.35 s blanket pulse (0.345 s) and 14.05 s patterned pulse; 56× wall area; 40.7× under-dose; rule within 25 % (1.05 to 1.27×) over AR 20 to 100 and a 20× TMA feed range, 12 runs; blanket 1.5 to 4.3×; 1D hole model within 3 to 11 % of converged Machball, 3D voxel solver within 2 %; PillarHall s = 8.5e-3 to 2.0e-2 depending on slit transport; fluidized bed 1.12; rotary drum 24.7 to 70.7 %; DOE R² 0.993, GP LOO R² 0.999, utilization 51 to 97 %, 11.6 → 9.8 s at 85 → 94 %, Monte Carlo 8.2–17.2 s, 12 % precursor saving; 26 % uneven saturation | `ald-conformality/CLAIMS.md`; the row-by-row sources are in the Round 4 table below |
| CathodeAI | 2,774 electrodes; ρ 0.76, p 0.007; 0.55 single descriptor; 10 of 11 | `CathodeAI-Battery-Materials-Screener/docs/CLAIMS.md` (`repro_pipeline.py`, `analysis_dsi.py`) |
| LMO half cell | 26 mV training RMSE; 17 mV 2C voltage error; six CV peaks within 80 mV; 74 / 17 / 6 % loss split; 58 tests; CV 0.1 to 0.3 mV/s; C/10 to 2C | `LMO-Cathode-Rate-Model-PyBaMM/docs/CLAIMS.md` (`results/*.json`, `pytest --collect-only`) |
| CVD reactor | 180 % (179.6 %); Da above 10 (≈ 13, methodology notes); 10 → 150 mm gives 6.1 %; 14-run CCD, 3.3 % at 0.07 m/s; GP LOO R² 0.944; 10,000 draws; 3D 5.9 % | `CVD-Reactor-Uniformity-COMSOL/docs/CLAIMS.md` (`analysis/full_analysis.py`, `real_cpk_pipeline_v4.py`, `wafer_3D_sigma.py`) |
| MD ionic liquids | −8.75 kcal mol⁻¹ ion⁻¹ (public abstract of the article); 19,260 atoms (coordinate file); journal, volume, pages, DOI (Crossref) | `MD-IL-CNT-Interfacial-Interactions/docs/CLAIMS.md` |
| SCAPS-1D | 27.99 %, V_OC 1.21 V, J_SC 25.96 mA cm⁻², FF 89.3 %; ten ETLs; nine metals; six parameters | `Perovskite-Solar-Cell-SCAPS1D-Optimization/docs/CLAIMS.md` (`scripts/make_figures.py`) |
| SCAPS-1D, hardware | 17.9 % more active area; two granted design registrations 434427-001 and 459195-001; one utility application; Best Poster Award, 61st ACC | certificates in the SCAPS repository; the area figure and the award are from the CV |
| 4680 thermal runaway | 20 cells, 25 Ah, ~110 kJ per cell, 80 °C trigger; threshold 1.0 to 1.25 W m⁻¹ K⁻¹; about 13 of 20 cells within an hour; 12 transient studies; cooling 0 to 2,000 W m⁻² K⁻¹ | CV verified list only; no public repository yet |
| Rappé group DFT | MHy₂PbBr₄ Berry-phase polarization 5.6 µC cm⁻², experimental range 4.6 to 5.8 µC cm⁻² | CV verified fact; unpublished, no public repository |
| Education and service | GPA 3.45/4.0 (Penn MS), 3.88/4.0 (VIT B.Tech); GAPSA Deputy Director to the President, more than 12,000 students represented | CV verified facts |

## Removed from the previous profile README

| Removed | Why |
|---|---|
| "231 domains" for the 4680 model | not in the verified list and no repository to reproduce it from |
| "12 % less downtime and 10 % less material waste", "600 kL/day", "433,000 t/yr" | internship figures with no source in any repository and not in the verified list; the roles are kept without the figures |
| "1 + 1 + 3 paper · manuscript · patents" tile | replaced by the explicit list: one paper, one preprint under revision, two granted design registrations and one utility application |
| GitHub stats widgets | third-party images that add no verifiable information |

## Live page

`docs/index.html` is a spectrum-band landing page in the banner's five colours; each band links to the project's repository
and live page. The number on each band is the headline number of the corresponding card above.

## Round 2 (2026-11-04): live-page rebuild and the sixth project

| Item | Detail |
|---|---|
| Page rebuilt | three.js 0.186.1 ES modules with `EffectComposer` (bloom, depth of field on desktop), Lenis 1.3.27 + GSAP 3.15.0 ScrollTrigger master timeline, pinned hero that threads six project vignettes along one camera path. Rationale in `docs/DESIGN.md`. |
| Scene data (`docs/assets/data.js`) | Written by `docs/build_assets.py` from the sibling repositories' `docs/assets/data.js` files, each of which that repository generates from its raw data. Excerpts, with the sampling stated in each entry's `source` field: 320 of 787 CathodeAI materials (seeded sample) and the 11 validation cathodes; the four LMO measured and modelled discharge curves (every third point); the three CVD wafer-plane profiles (every second point); the non-hydrogen MD atoms within 5 Å of the tube mid-plane; the SCAPS stack and ten-ETL ranking; the 4680 COMSOL run matrix and the surrogate's cascade trace (every sixth sample, labelled as the surrogate's). Nothing on this page is drawn from invented data. |
| Sixth project card and band | 4680 thermal runaway propagation: 1.0 to 1.25 W/m·K threshold, 20-cell 5s4p pack, 25 Ah, about 110 kJ per cell, 80 °C trigger, 12 one-hour studies, cooling 0 to 2,000 W/m²·K, about 13 of 20 cells below the threshold. Source: that repository's `docs/CLAIMS.md` (sections A, B and the CV). The card links to the repository and its live page; the page is published once that repository's Pages setting is enabled (manual step in its pull request). |
| Animated README hero | `docs/assets/hero.svg`, generated by `docs/build_assets.py` from the same excerpt: six small marks, one per project, lighting up in turn with CSS keyframes. The six captions (2,774; 26 mV; 180 → 3.3 %; −8.75 kcal/mol; 27.99 %; 1.0 → 1.25 W/m·K) are the audited headline numbers. |
| Card images | `docs/assets/card_*.png` regenerated from each project's rebuilt hero render (`docs/assets/hero.png` in the sibling clone). |

## Round 3 (2026-11-04): particle journey, 3D card thumbnails, light mode, confident framing

| Item | Detail |
|---|---|
| Hero | One GPU particle system (56,000 particles, 16,000 on phones) morphing between six shapes, each built in `assets/scene.js` (`buildShapes`) from the same `assets/data.js` excerpt as before: CathodeAI sampled materials coloured by DSI; the four LMO measured discharge curves; the CVD before-fix wafer profile; the MD atoms near the tube mid-plane; the SCAPS stack and ten-ETL ranking; the twenty 4680 cells coloured by the reduced-order model's end-of-hour maximum temperature. Nothing is drawn from invented data; the sampling of each excerpt is stated in its `source` field. |
| Headline numbers in the hero focus panels | 2,774 cathodes; 26 mV; 3.3 % from 179.6 %; −8.75 kcal/mol per ion; 27.99 %; 1.25 W/m·K (the upper edge of the 1.0 to 1.25 threshold interval, stated as such on the panel). Sources: the project repositories' `docs/CLAIMS.md`, as in the table above. |
| Card thumbnails | Live 3D views of the same six shapes (7,000 particles each) drawn by the shared `assets/viz.js` renderer; static fallbacks `assets/viz_<project>_<theme>.png` are captures of those views. |
| README hero | `docs/assets/hero.svg` is generated by `docs/build_assets.py --hero` from 300 particles per shape projected by the page's own scene (`window.__hero.project`), animated with CSS keyframes only. |
| Framing | The 4680 card and panel lead with the threshold finding, the adiabatic stress test and the identification of internal conduction as the controlling resistance; the repository's scope notes live in that repository's `docs/CLAIMS.md`. None of the figures withdrawn in earlier rounds appears anywhere on this profile. |

## Round 4 (2026-11-10): the seventh project, ALD chamber-to-feature model (OpenFOAM)

Every number on the ALD card, focus panel, band, README cell and hero caption, with its source file in the
[ald-conformality](https://github.com/Soham-ChemE/ald-conformality) repository (paths relative to that repository's root;
its own `CLAIMS.md` names the script that reproduces each).

| Number as shown here | Value | Source file in ald-conformality |
|---|---|---|
| Blanket 300 mm wafer saturating TMA pulse | 0.345 s centre (shown as 0.35 s); 0.385 s worst point | `figures/pulse_time_map.csv` (blanket row at 1 % TMA), `figures/reactor_langmuir_coverage.png`; `CLAIMS.md` |
| Patterned wafer, 100 nm holes at aspect ratio 100, saturating pulse | 14.05 s centre (headline, counted up on the focus panel); 14.1 s worst point | `figures/pulse_time_map.csv` (run 7), `docs/assets/data.js` `hero.t90_bottom_centre`; `CLAIMS.md` |
| Wall area of the patterned wafer | 55.9× the wafer area (shown as 56×) | `figures/pulse_time_map.csv` (`wall` column), `docs/assets/data.js` `stats.wall_ratio` |
| Under-dose of a blanket-wafer recipe on the patterned wafer | 40.7× (14.05 / 0.345) | `docs/assets/data.js` `stats.underdose`; `CLAIMS.md` |
| Supply rule t_pulse = 1.2 (1 + A_wall/A_wafer) N0/(U c0), spread over the 12 patterned runs | 1.05 to 1.27× the supply limit (within 25 %), aspect ratios 20, 50, 100, TMA fractions 0.5 to 10 % (20×) | `figures/pulse_time_map.csv` (`ratio` column), `docs/assets/data.js` `map.patterned_ratio`; `CLAIMS.md` |
| Blanket wafers against the supply limit | 1.5 to 4.3× (1.54 to 4.27) | `figures/pulse_time_map.csv`, `docs/assets/data.js` `map.blanket_ratio` |
| Hole model against Argonne's Machball (corrected 2026-11-11) | 1D solver 1.035 / 4.230 / 15.93 s against converged Machball 1.158 / 4.476 / 16.19 s at AR 20 / 50 / 100 (3 to 11 % fast; the earlier 0.3 to 7 % used unconverged Machball values); the 3D voxel Monte Carlo solver agrees with Machball within 2 % | `figures/voxel_mc_crosscheck.csv`; `CLAIMS.md` |
| PillarHall fit (Zenodo 3974438) | s = 8.5e-3 (×/÷ 1.5) with hydraulic slit transport, 1.96e-2 with the ideal-plate correction, same rms 0.038: the profile alone does not pin s | `figures/pillarhall_fit.png`, `coupling/fit_pillarhall.py`, `data/zenodo_3974438`; `CLAIMS.md` |
| Measured fluidized-bed ALD run (940 m² silica gel, Argonne 2022) against the rule | 1.12 supply-limit times (0.92 to 1.31) | `figures/validation_supply_rule.png`, `coupling/validate_supply_rule.py`; literature Lu et al., JVST A 40 (2022) |
| Measured rotary-drum utilization ordered by the rule | 24.7 % (2 g) to 70.7 % (75 g) | `figures/validation_supply_rule.png`; literature Coile et al., JVST A 38, 052403 (2020), Table 2 |
| DOE: 25-run face-centred central composite design in OpenFOAM, JMP response surface | R² 0.993; t90 ∝ x^-1.0 Q^-0.8 p^-0.12 | `figures/doe_design.csv`, `figures/doe_results.csv`, `figures/doe_rsm_report.txt`; `CLAIMS.md` |
| Gaussian-process surrogates, MATLAB and scikit-learn | LOO R² 0.999 on pulse time (0.988 / 0.986 on utilization) | `figures/doe_gp_report.txt`, `figures/doe_gp_python_report.txt`, `figures/doe_gp_python.json` |
| Utilization range over the design | 51 to 97 % | `figures/doe_results.csv`, `docs/assets/data.js` `stats.util_range` |
| Same-supply optimum | 11.6 s at 85 % → 9.8 s at 94 % utilization | `figures/doe_gp_report.txt`; `CLAIMS.md` |
| Monte Carlo band on the rule (N0 ×/÷ 1.25) | 11.9 s, 90 % band 8.2 to 17.2 s | `figures/doe_gp_report.txt`; `CLAIMS.md` |
| Cost-of-ownership front | 12 % less precursor per wafer at the centre pulse time (1.044× against 1.181× the stoichiometric minimum) | `figures/doe_pareto.csv`, `figures/doe_pareto.png`, `figures/doe_gp_python_report.txt`; `CLAIMS.md` |
| Non-uniform layouts | a dense array beside open field saturates 26 % unevenly (bottom t90 11.85 s centre, 8.75 s at 74.5 mm); the local wall-area ratio, not the wafer average, sets the pulse (wafer average under-predicts by 2.3×) | `figures/pattern_layout.csv`, `figures/pattern_layout.png`, `coupling/postprocess_layout.py`; `CLAIMS.md` |
| Scene data (`docs/assets/data.js` here, key `ald`) | the AR-100 hole's coverage-depth profile at 19 pulse times (`hero.hole`), flat and hole-bottom coverage against radius at every tenth chamber time step (`hero.cov`), the 16-row pulse-time map, the headline statistics; 12 KB | `docs/assets/data.js` in ald-conformality, itself written by that repository's `docs/build_assets.py` from the OpenFOAM cases |

The seventh shape in the hero, the card thumbnail and the README hero's seventh frame are built from that excerpt only (see
`docs/DESIGN.md` §7); nothing is drawn from invented data. The focus panel counts to 14.05 s; the card, band and README
caption round it to 14 s and the blanket pulse to 0.35 s, as the ald-conformality README does.
