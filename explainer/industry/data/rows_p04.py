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
OWID = "https://ourworldindata.org/grapher/"
DAL = "https://www.sec.gov/Archives/edgar/data/27904/000002790426000013/dal-20251231.htm"
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
    # --- Delta's operating expenses, line by line ---------------------------------------------------------------
    r("dal.opex", 57.542, "USD bn", "Delta Air Lines total operating expense, 2025, in thirteen lines ($bn): salaries "
      "and related costs 17.520; aircraft fuel and related taxes 9.819; ancillary businesses and refinery 5.987; "
      "contracted services 4.617; landing fees and other rents 3.564; regional carrier expense 2.553; passenger "
      "commissions and other selling 2.485; depreciation and amortization 2.443; aircraft maintenance materials and "
      "outside repairs 2.432; passenger service 1.855; profit sharing 1.337; aircraft rent 0.542; other 2.388",
      "Delta Air Lines Form 10-K 2025, results of operations", DAL, "2025", kind="filing"),
    r("dal.horizon", 0, "note", "this film's rough sort of Delta's expense lines by how soon cancelling flying avoids "
      "them: within days (fuel, landing fees and rents, passenger service, commissions and selling), within about a "
      "year (salaries, maintenance, contracted services, regional carriers, the refinery and other businesses, profit "
      "sharing, other), only over the aircraft's lives (depreciation, aircraft rent)", "this film's classification of "
      "Delta's Form 10-K 2025 lines", DAL, "2025", kind="assumption"),
    r("dal.covid", 0, "note", "Delta Air Lines, 2019 against 2020 ($bn): operating revenue 47.007 and 17.095; total "
      "operating expense 40.389 and 29.564; operating income 6.618 and -12.469. 2020's expense is as reported: it "
      "includes restructuring charges (early retirements, aircraft retired early) and is net of government payroll "
      "support recognized against costs", "Delta Air Lines Forms 10-K 2020 and 2021 (SEC XBRL company facts: "
      "RevenueFromContractWithCustomerExcludingAssessedTax, CostsAndExpenses, OperatingIncomeLoss)",
      "https://data.sec.gov/api/xbrl/companyfacts/CIK0000027904.json", "2019-2020", kind="filing"),
    r("dal.rev.2019", 47.007, "USD bn", "Delta Air Lines operating revenue, 2019", "Delta Air Lines Form 10-K 2020 "
      "(SEC company facts)", "https://data.sec.gov/api/xbrl/companyfacts/CIK0000027904.json", "2019", kind="filing"),
    r("dal.rev.2020", 17.095, "USD bn", "Delta Air Lines operating revenue, 2020", "Delta Air Lines Form 10-K 2021 "
      "(SEC company facts)", "https://data.sec.gov/api/xbrl/companyfacts/CIK0000027904.json", "2020", kind="filing"),
    r("dal.cost.2019", 40.389, "USD bn", "Delta Air Lines total operating expense, 2019", "Delta Air Lines Form 10-K "
      "2020 (SEC company facts)", "https://data.sec.gov/api/xbrl/companyfacts/CIK0000027904.json", "2019",
      kind="filing"),
    r("dal.cost.2020", 29.564, "USD bn", "Delta Air Lines total operating expense, 2020, as reported", "Delta Air "
      "Lines Form 10-K 2021 (SEC company facts)", "https://data.sec.gov/api/xbrl/companyfacts/CIK0000027904.json",
      "2020", kind="filing"),
    r("dal.cargo", 0.900, "USD bn", "Delta Air Lines cargo revenue, 2025 (2024: $0.822bn), carried mostly in the "
      "holds of passenger aircraft", "Delta Air Lines Form 10-K 2025, operating revenue", DAL, "2025", kind="filing"),
    r("scale.six_tenths", 0.6, "exponent", "the six-tenths rule of thumb of process engineering: a plant's cost "
      "rises with its capacity to about the power 0.6, so doubling capacity raises cost by about half (2^0.6 = 1.52)",
      "process-engineering estimating practice (a rule of thumb, not a law)",
      "https://en.wikipedia.org/wiki/Six-tenths_rule", "rule of thumb", kind="assumption",
      note="an engineering rule of thumb used for early cost estimates; actual exponents vary by plant"),
    r("concorde.1976", 1976, "year", "Richard Dawkins and Tamsin Carlisle name the 'Concorde fallacy': continuing to "
      "invest because of what has already been invested ('Parental investment, mate desertion and a fallacy', Nature "
      "262:131-133, 8 July 1976)", "Nature 262, 131-133 (1976), DOI 10.1038/262131a0",
      "https://www.nature.com/articles/262131a0", "1976-07", kind="study"),
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
    # --- solar: prices and capacity (Economics, Built's Data Room, solar_pv.csv) ------------------------------------
    r("solar.price.1975", 132.3757, "USD/W", "solar photovoltaic module price, 1975, in constant 2025 dollars per watt",
      "IRENA and other sources (Nemet; Farmer and Lafond), via Our World in Data, solar-pv-prices",
      OWID + "solar-pv-prices", "1975", kind="study"),
    r("solar.price.2025", 0.12, "USD/W", "solar photovoltaic module price, 2025, in constant 2025 dollars per watt "
      "(2000: 6.50; 2010: 2.51; 2020: 0.33)", "IRENA and other sources, via Our World in Data, solar-pv-prices",
      OWID + "solar-pv-prices", "2025", kind="study"),
    r("solar.cap.2000", 1.2, "GW", "world installed solar capacity, 2000", "IRENA (2026), via Our World in Data, "
      "installed-solar-pv-capacity", OWID + "installed-solar-pv-capacity", "2000"),
    r("solar.cap.2020", 721.2, "GW", "world installed solar capacity, 2020", "IRENA (2026), via Our World in Data, "
      "installed-solar-pv-capacity", OWID + "installed-solar-pv-capacity", "2020"),
    r("solar.cap.2025", 2396.7, "GW", "world installed solar capacity, 2025 (2024: 1,883)", "IRENA (2026), via Our "
      "World in Data, installed-solar-pv-capacity", OWID + "installed-solar-pv-capacity", "2025"),
    r("iea.pv_china", 0.8, "share", "China's share of global manufacturing capacity in every main stage of solar panel "
      "making (polysilicon, ingots, wafers, cells, modules): more than 80%", "IEA, Solar PV Global Supply Chains "
      "(July 2022)", "https://www.iea.org/reports/solar-pv-global-supply-chains", "2021", kind="study"),
    # --- memory: the price war and what stops it -------------------------------------------------------------
    r("dram.fines", 0.729, "USD bn", "criminal fines for fixing DRAM prices, US Department of Justice: Infineon $160m "
      "(2004), Hynix $185m (2005), Samsung $300m (2005), Elpida $84m (2006); the sum is this film's",
      "US Department of Justice, Antitrust Division press releases, 2005-2006",
      "https://www.justice.gov/archive/opa/pr/2006/March/06_at_165.html", "2004-2006", kind="official"),
    r("micron.elpida", 2013, "year", "Micron completed its acquisition of Elpida Memory, the Japanese DRAM maker then "
      "in corporate reorganization (bankruptcy), on 31 July 2013", "Micron Technology Form 8-K, 31 July 2013",
      "https://www.sec.gov/Archives/edgar/data/0000723125/000072312513000133/form8k-elpidaclosingpr.htm", "2013-07-31",
      kind="filing"),
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
