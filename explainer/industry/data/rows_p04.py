"""Register rows for Part 4, *The Cost Curve*.  Checked 2026-11-23.

The power plants' costs are EIA's assumptions for the Annual Energy Outlook 2026 (built on Sargent & Lundy's January
2024 estimates); the fleet, its fuel costs and heat rates are the Filing Room's ``eia_power.csv`` (Electric Power
Annual 2025); solar module prices and installed capacity are *Economics, Built*'s Data Room (``solar_pv``). Part 4
also reads Part 1's Micron rows and Part 3's Delta and Microsoft rows.
"""

from explainer.industry.register import Row, add

C = "2026-11-23"
P = (4,)
EMM = "https://www.eia.gov/outlooks/aeo/assumptions/pdf/EMM_Assumptions.pdf"
STEO = "https://www.eia.gov/outlooks/steo/archives/nov26.pdf"
IEA = ("https://iea.blob.core.windows.net/assets/fdd86c6e-e172-4053-86da-cc68236f2125/TechnologyRoadmap-"
       "SolarPhotovoltaicEnergy2010Foldout.pdf")


def r(key, value, unit, definition, source, url, fact, kind="official", note="", **kw):
    return Row(key, value, unit, definition, source, url, fact, C, kind, note=note, parts=P, **kw)


def plant(key, name, size, lead, overnight, vom, fom, heat):
    """One technology's row set from EIA's Table 3 (2025 dollars)."""
    src = "EIA, Assumptions to the Annual Energy Outlook 2026, Electricity Market Module, Table 3 (April 2026)"
    return [r(f"plant.{key}.size", size, "MW", f"{name}: typical size", src, EMM, "2026-04"),
            r(f"plant.{key}.lead", lead, "years", f"{name}: lead time to build", src, EMM, "2026-04"),
            r(f"plant.{key}.overnight", overnight, "USD/kW", f"{name}: total overnight capital cost, 2025 dollars", src,
              EMM, "2026-04"),
            r(f"plant.{key}.vom", vom, "USD/MWh", f"{name}: variable operating and maintenance cost", src, EMM,
              "2026-04"),
            r(f"plant.{key}.fom", fom, "USD/kW-yr", f"{name}: fixed operating and maintenance cost", src, EMM,
              "2026-04"),
            r(f"plant.{key}.heat", heat, "Btu/kWh", f"{name}: heat rate (3,412 for plants that burn no fuel)", src,
              EMM, "2026-04")]


add(
    # --- Wright, 1936 --------------------------------------------------------------------------------------------
    r("wright.1936", 1936, "year", "T. P. Wright, of the Curtiss-Wright Corporation in Buffalo, published 'Factors "
      "Affecting the Cost of Airplanes', Journal of the Aeronautical Sciences 3(4), February 1936: the labour in an "
      "airframe fell by a constant share each time the number built doubled, about 20% across US aircraft makers "
      "(an 80% curve)", "CIA reading room, Theory and Applications of the Learning Curve; Journal of the Aeronautical "
      "Sciences 3(4):122-128, DOI 10.2514/8.155", "https://www.cia.gov/readingroom/node/384237", "1936-02", "study"),
    r("wright.rate", 0.20, "share", "Wright's average fall in labour per airframe with each doubling of cumulative "
      "output", "CIA reading room, Theory and Applications of the Learning Curve", "https://www.cia.gov/readingroom/"
      "node/384237", "1936", "study"),
    # --- new plants: EIA's cost and performance assumptions ------------------------------------------------------
    *plant("cc1", "Combined-cycle gas, single-shaft", 627, 3, 1086, 3.49, 16.23, 6226),
    *plant("cc2", "Combined-cycle gas, multi-shaft", 1227, 3, 1032, 3.57, 12.69, 6226),
    *plant("ct_aero", "Combustion turbine, aeroderivative", 211, 2, 2275, 5.97, 9.99, 9447),
    *plant("ct_frame", "Combustion turbine, industrial frame", 419, 2, 1158, 4.17, 7.18, 9142),
    *plant("nuclear", "Nuclear, light water reactor", 2156, 6, 8255, 2.62, 163.40, 10445),
    *plant("smr", "Nuclear, small modular reactor", 480, 6, 9831, 3.32, 127.62, 10445),
    *plant("wind", "Onshore wind", 200, 3, 1712, 0.0, 34.57, 3412),
    *plant("solar", "Solar photovoltaic with tracking", 150, 2, 1484, 0.0, 23.60, 3412),
    *plant("battery", "Battery storage", 150, 1, 1521, 0.0, 41.84, 0),
    r("plant.optimism", 0, "note", "EIA applies a 'technological optimism factor' to the first four units of a new "
      "design, reflecting 'the demonstrated tendency to underestimate actual costs for a first-of-a-kind unit' "
      "(1.05 for large reactors, 1.10 for small modular ones)", "EIA, Assumptions to the AEO2026, EMM, Table 3, note c",
      EMM, "2026-04"),
    # --- the 2027 outlook ----------------------------------------------------------------------------------------
    r("steo.solar.2025", 298.3, "TWh", "US utility-scale solar generation, electric power sector, 2025", "EIA, "
      "Short-Term Energy Outlook, November 2026, Table 7d", STEO, "2025"),
    r("steo.solar.2027", 425.7, "TWh", "EIA's forecast of US utility-scale solar generation, 2027 (2026: 356.9)",
      "EIA, Short-Term Energy Outlook, November 2026, Table 7d", STEO, "2027", kind="official", note="a forecast, not an outcome"),
    r("steo.coal.2025", 730.5, "TWh", "US coal generation, electric power sector, 2025", "EIA, Short-Term Energy "
      "Outlook, November 2026, Table 7d", STEO, "2025"),
    r("steo.coal.2027", 645.2, "TWh", "EIA's forecast of US coal generation, 2027 (2026: 679.1)", "EIA, Short-Term "
      "Energy Outlook, November 2026, Table 7d", STEO, "2027", kind="official", note="a forecast, not an outcome"),
    r("steo.q2_2027", 126.0, "TWh", "EIA's forecast of utility-scale solar generation in April-June 2027, against "
      "135.0 TWh from coal", "EIA, Short-Term Energy Outlook, November 2026, Table 7d", STEO, "2027-Q2",
      kind="official", note="a forecast, not an outcome"),
    r("steo.new_capacity", 72, "GW", "new solar capacity EIA expects in 2026 and 2027 together (wind: 20 GW); 13 GW of "
      "coal capacity scheduled to retire by the end of 2027", "EIA, Short-Term Energy Outlook, November 2026", STEO,
      "2026-11", kind="official", note="a forecast, not an outcome"),
    # --- the IEA's 2010 solar roadmap ------------------------------------------------------------------------------
    r("iea.pv2010.2020", 200, "GW", "the IEA's 2010 solar PV roadmap: global installed capacity 'could reach' 200 GW in "
      "2020 (900 GW in 2030, 2,000 GW in 2040, 3,000 GW in 2050; a market of 34 GW a year in 2020)", "IEA, Technology "
      "Roadmap: Solar Photovoltaic Energy (11 May 2010), foldout", IEA, "2010-05", kind="study"),
    r("iea.pv2010.2040", 2000, "GW", "the IEA's 2010 roadmap: global solar PV capacity in 2040", "IEA, Technology "
      "Roadmap: Solar Photovoltaic Energy (2010), foldout", IEA, "2010-05", kind="study"),
)
