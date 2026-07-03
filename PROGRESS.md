# Progress

## Done
- Meteogram notebook + `meteogram_plot.py` demo, CI nightly run, metadata monitor workflow.
- Solar Production notebook (`notebooks/SolarProduction.ipynb`, `notebooks/solar_plot.py`) — illustrative PV output model built on `gre000h0` radiation forecast, reusing the Meteogram fetch/parse pipeline.
- README updated with a section describing the Solar Production notebook.
- `publish` skill hardened: cherry-picks to the public repo now explicitly check for stray `.claude/` files even without a merge conflict, and document how to strip + amend.

## In progress / not yet committed
- `README.md` and `.claude/skills/publish/SKILL.md` changes are staged in the working tree but not committed.
- `notebooks/SolarProduction.ipynb`, `notebooks/solar_plot.py`, `notebooks/solar_production.png` are untracked.

## Next steps
- Review/run the Solar Production notebook end-to-end to confirm output.
- Commit pending changes and run `/publish` to push to both the private fork and public MeteoSwiss repo.
