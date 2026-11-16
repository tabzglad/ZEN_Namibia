## Update to latest Zen creator version
- Update your environment to the newest Zen creator version (2.1.0 or newer):
  ```
  pip install --upgrade zen-creator
  pip show zen-creator
  ```
  
## General comments
- I removed import/export constraints for now (dont use historical data, but rather physical transmission limits to neighboring countries)
- For coal and diesel, I changed the assumption that infinite imports are available. But they do need an import price.
- Check if Namibia really has no hydro potential. Currently hydro turbines cannot be expanded
- At the moment, capacity of wind and PV cannot be expanded (capacity_limit=0 -> get an estimate for PV/wind potential in Namibia)
- The manual dispatch assumptions can be removed. The dispatch is optimized, when prices for import and opex for technologies are set.


## Next steps
1) Add import prices for coal and diesel
2) Add opex for coal, diesel, hydro, PV and wind (if applicable, use e.g. dea data or pypsa data (see e.g. zen europe))
3) Add import limit and import price in GW (not GWh/h) for neighboring countries equal to the line capacities of those countries. Check e.g. pypsa world or estimate from highest value in NAM data (if possible)
4) Rerun the model and check the results.   