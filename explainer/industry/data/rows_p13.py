"""Register rows for Part 13, *Electricity*.  Checked 2026-11-27.

Samuel Insull's address of 25 February 1910 (in *Central-Station Electric Service*, 1915); the FERC-NERC-Regional
Entity staff report on the February 2021 cold weather outages (November 2021); the Independent Market Monitor for ERCOT's
State of the Market reports for 2021 and 2024; Vistra's and Duke Energy's Forms 10-K; the National Audit Office on
Britain's energy supplier market (2022); the EIA's Annual Energy Outlooks of 2005 and 2021 and its Today in Energy of 16
June 2026; the Department of Energy on Lawrence Berkeley National Laboratory's data center report (2024).  Series are
the Filing Room's EIA-930, Monthly Energy Review, FRED, Our World in Data and SEC extracts.
"""

from explainer.industry.register import Row, add

C = "2026-11-27"
P = (13,)
INSULL = "https://archive.org/details/centralstationel00insuiala"
NERC = "https://www.nerc.com/pa/rrm/ea/Documents/February_2021_Cold_Weather_Report.pdf"
IMM21 = "https://www.potomaceconomics.com/wp-content/uploads/2022/05/2021-State-of-the-Market-Report.pdf"
IMM24 = "https://www.potomaceconomics.com/wp-content/uploads/2025/06/2024-State-of-the-Market-Report.pdf"
VST = "https://www.sec.gov/Archives/edgar/data/1692819/000169281922000005/vistra-20211231.htm"
DUK = "https://www.sec.gov/Archives/edgar/data/1326160/000132616026000014/duk-20251231.htm"
NAO = "https://www.nao.org.uk/wp-content/uploads/2022/03/The-energy-supplier-market-Summary.pdf"
AEO05 = "https://www.eia.gov/outlooks/archive/aeo05/pdf/0383(2005).pdf"
AEO21 = "https://www.eia.gov/outlooks/aeo/excel/aeotab_8.xlsx"
TIE_CAISO = "https://www.eia.gov/todayinenergy/detail.php?id=67784"
DOE_DC = ("https://www.energy.gov/articles/doe-releases-new-report-evaluating-increase-electricity-demand-data-"
          "centers")


def r(key, value, unit, definition, source, url, fact, kind="official", note="", **kw):
    return Row(key, value, unit, definition, source, url, fact, C, kind, note=note, parts=P, **kw)


def insull(key, value, unit, definition):
    return r(key, value, unit, definition, "Samuel Insull, address at the General Electric Company's dinner for New "
             "England central-station men, Boston, 25 February 1910; in Central-Station Electric Service (1915), "
             "pp. 127-130", INSULL, "1910-02-25", "study")


def nerc(key, value, unit, definition, **kw):
    return r(key, value, unit, definition, "FERC, NERC and Regional Entity staff, 'The February 2021 Cold Weather "
             "Outages in Texas and the South Central United States' (November 2021)", NERC, "2021-02", **kw)


def imm(key, value, unit, definition, year=2021, **kw):
    return r(key, value, unit, definition, f"Potomac Economics, Independent Market Monitor for ERCOT, {year} State of "
             "the Market Report for the ERCOT Electricity Markets", IMM21 if year == 2021 else IMM24, str(year), **kw)


def duke(key, value, unit, definition, fact, **kw):
    return r(key, value, unit, definition, "Duke Energy Corporation, Form 10-K 2025, electric rate cases", DUK, fact,
             "filing", **kw)


def nao(key, value, unit, definition, fact="2021-2022", **kw):
    return r(key, value, unit, definition, "National Audit Office, The energy supplier market (HC 1065, June 2022), "
             "summary", NAO, fact, **kw)


# Duke Energy's electric rate cases (10-K 2025): (key, name, regulator, $m increase, ROE %, equity %, effective)
DUKE_CASES = [
    ("dec_sc_2025", "Duke Energy Carolinas, South Carolina 2025", "PSCSC", 19, 9.99, 53, "2026-03"),
    ("dep_sc_2025", "Duke Energy Progress, South Carolina 2025", "PSCSC", 40, 9.99, 53, "2026-02"),
    ("dek_2024", "Duke Energy Kentucky 2024", "KPSC", 44, 9.8, 52.73, "2025-07"),
    ("dei_2024", "Duke Energy Indiana 2024", "IURC", 385, 9.75, 53, "2025-03"),
    ("def_2024", "Duke Energy Florida 2024", "FPSC", 262, 10.3, 53, "2025-01"),
    ("dec_sc_2024", "Duke Energy Carolinas, South Carolina 2024", "PSCSC", 150, 9.94, 51.21, "2024-08"),
    ("dec_nc_2023", "Duke Energy Carolinas, North Carolina 2023", "NCUC", 768, 10.1, 53, "2024-01"),
    ("dek_2022", "Duke Energy Kentucky 2022", "KPSC", 48, 9.75, 52.145, "2023-10"),
    ("dep_nc_2022", "Duke Energy Progress, North Carolina 2022", "NCUC", 494, 9.8, 53, "2023-10"),
    ("dep_sc_2022", "Duke Energy Progress, South Carolina 2022", "PSCSC", 36, 9.6, 52.43, "2023-04"),
    ("deo_2021", "Duke Energy Ohio 2021", "PUCO", 23, 9.5, 50.5, "2023-01"),
]
DUKE_PENDING = [("dec_nc_2025", "Duke Energy Carolinas, North Carolina 2025 (requested)", "NCUC", 1002, 10.95, 53, "2027-01"),
                ("dep_nc_2025", "Duke Energy Progress, North Carolina 2025 (requested)", "NCUC", 729, 10.95, 53, "2027-01")]

# ERCOT's average real-time energy price ($/MWh) and natural gas price ($/MMBtu), from the IMM's tables
ERCOT_PRICE = {2014: 40.64, 2015: 26.77, 2016: 24.62, 2017: 28.25, 2018: 35.63, 2019: 47.06, 2020: 25.73, 2021: 167.88,
               2022: 74.92, 2023: 65.13, 2024: 31.91}
ERCOT_GAS = {2014: 4.32, 2015: 2.57, 2016: 2.45, 2017: 2.98, 2018: 3.22, 2019: 2.47, 2020: 1.99, 2021: 7.30}

add(
    # --- Insull, 1910 ----------------------------------------------------------------------------------------------
    insull("insull.apartments", 193, "apartments", "A block in a residence district of Chicago with 193 apartments"),
    insull("insull.customers", 189, "customers", "Commonwealth Edison's customers in that block (10-11 lamps each)"),
    insull("insull.kwh", 33000, "kWh a year", "Electricity the block used in a year"),
    insull("insull.peaks", 68.5, "kW", "The sum of the customers' separate maxima"),
    insull("insull.lf_alone", 5.5, "%", "Load factor on the customers' separate maxima"),
    insull("insull.peak", 20, "kW", "The maximum at the transformers, the customers' combined peak"),
    insull("insull.lf_together", 19, "%", "Load factor on the combined peak"),
    insull("insull.turn", 5, "years", "'The very best result that can be obtained from capital invested in central-station "
           "business is to turn that capital about once in five years; ... the average ... once in seven years'"),
    # --- February 2021 ---------------------------------------------------------------------------------------------
    nerc("nerc.units", 1045, "generating units", "Generating units in Texas and the South Central US with outages, derates "
         "or failures to start, 8-20 February 2021 (192,818 MW of nameplate capacity; 4,124 events)"),
    nerc("nerc.ercot_unavail", 34000, "MW", "ERCOT's average unavailable generation, 7 a.m. 15 February to 1 p.m. 17 "
         "February 2021, nearly half its all-time winter peak of 69,871 MW"),
    nerc("nerc.winter_peak", 69871, "MW", "ERCOT's all-time winter peak load before the event"),
    nerc("nerc.people", 4.5, "million people", "People in Texas who lost power during the event, some for as long as "
         "four days"),
    nerc("nerc.deaths", 210, "people", "People who died during the event, at least, with most of the deaths connected "
         "to the power outages (the report cites Houston Public Media's count)"),
    nerc("nerc.shed", 20000, "MW", "ERCOT's firm load shed at the worst point, 7:15 p.m. 15 February 2021: the largest "
         "controlled firm load shed in US history"),
    nerc("nerc.minutes", 9, "minutes", "How long ERCOT's operators had to prevent about 17,000 MW of generating units "
         "tripping on underfrequency, early on 15 February 2021"),
    nerc("nerc.not_adopted", 40, "%", "Share of generator owners and operators in ERCOT and MISO South, where freezing was "
         "the main cause of outages, who said they had not incorporated specific generator recommendations of the 2011 "
         "report ('over 40 percent'); those recommendations were voluntary"),
    nerc("nerc.freezing", 44.2, "%", "Share of outages, derates and failures to start caused by freezing issues"),
    nerc("nerc.fuel", 31.4, "%", "Share caused by fuel issues (natural gas supply 87% of these)"),
    nerc("nerc.gas_share", 58, "%", "Natural gas-fired units' share of the 1,045 units affected (wind 27%, coal 6%, "
         "solar 2%)"),
    nerc("nerc.fleet_gas", 52, "%", "Natural gas in ERCOT's generation fleet (wind 25%, coal 12%, solar 5%, nuclear "
         "4%)"),
    imm("imm.voll", 9000, "$ per MWh", "ERCOT's value of lost load and system-wide offer cap, February 2021; prices held "
        "there until mid-morning on 19 February though the last firm load shed was recalled just before midnight on "
        "17 February"),
    imm("imm.value", 59, "$ billion", "The total value of electricity in ERCOT, 13-19 February 2021"),
    imm("imm.price.2021", 167.88, "$ per MWh", "ERCOT's average real-time energy price, 2021 ($40.73 without Winter "
        "Storm Uri)"),
    imm("imm.price.2021x", 40.73, "$ per MWh", "ERCOT's average real-time energy price, 2021, without Winter Storm Uri"),
    imm("imm.marginal", 1, "note", "'natural gas units are generally on the margin in ERCOT'"),
    *[imm(f"imm.price.{y}", v, "$ per MWh", f"ERCOT's average real-time energy price, {y}", 2024 if y >= 2022 else 2021)
      for y, v in ERCOT_PRICE.items() if y != 2021],
    *[imm(f"imm.gas.{y}", v, "$ per MMBtu", f"Natural gas price used by the IMM, {y}") for y, v in ERCOT_GAS.items()],
    imm("imm.solar.2024", 7.5, "GW", "New solar capacity in ERCOT, 2024", 2024),
    imm("imm.storage.2024", 5.0, "GW", "New energy storage capacity in ERCOT, 2024", 2024),
    r("vst.uri", 2.2, "$ billion", "Winter Storm Uri's negative impact on Vistra's pre-tax earnings, 2021, after about "
      "$544 million of securitization proceeds; driven by 'the need to procure power in ERCOT at market prices at or near "
      "the price cap due to lower output from our natural gas-fueled power plants'", "Vistra Corp., Form 10-K 2021",
      VST, "2021", "filing"),
    # --- Duke's rate cases -----------------------------------------------------------------------------------------
    *[duke(f"duke.{k}.rev", v, "$ million", f"{n} ({reg}): approved revenue increase", f) for k, n, reg, v, _, _, f in DUKE_CASES],
    *[duke(f"duke.{k}.roe", roe, "%", f"{n} ({reg}): approved return on equity", f) for k, n, reg, _, roe, _, f in DUKE_CASES],
    *[duke(f"duke.{k}.eq", eq, "%", f"{n} ({reg}): equity share of the capital structure", f) for k, n, reg, _, _, eq, f in DUKE_CASES],
    *[duke(f"duke.{k}.rev", v, "$ million", f"{n} ({reg}): revenue increase requested", f) for k, n, reg, v, _, _, f in DUKE_PENDING],
    *[duke(f"duke.{k}.roe", roe, "%", f"{n} ({reg}): return on equity requested", f) for k, n, reg, _, roe, _, f in DUKE_PENDING],
    # --- Britain's suppliers ---------------------------------------------------------------------------------------
    nao("nao.failed", 29, "suppliers", "Energy suppliers that failed, July 2021 to May 2022, affecting nearly four million "
        "households"),
    nao("nao.suppliers.2010", 12, "suppliers", "Domestic energy suppliers in Britain, December 2010", "2010-12"),
    nao("nao.suppliers.peak", 70, "suppliers", "Domestic energy suppliers at the peak, mid-2018", "2018"),
    nao("nao.suppliers.2022", 23, "suppliers", "Domestic energy suppliers, May 2022", "2022-05"),
    nao("nao.cap.2018", 1105, "£ a year", "Typical bill at the price cap, winter 2018-19", "2018-19"),
    nao("nao.cap.2022", 1971, "£ a year", "Typical bill at the price cap, summer 2022", "2022"),
    nao("nao.gas_x", 6, "times", "Rise in the weekly average wholesale gas price, February to December 2021 ('nearly "
        "six-fold')", "2021"),
    nao("nao.cost", 2.7, "£ billion", "Ofgem's best estimate of the cost of failed suppliers' exits (about £94 per "
        "customer)"),
    nao("nao.per_customer", 94, "£", "That cost per customer"),
    nao("nao.bulb", 1.6, "million customers", "Bulb Energy's customers when it was placed in special administration, "
        "November 2021", "2021-11"),
    nao("nao.new_share", 40, "%", "New entrants' share of the market by September 2021", "2021-09"),
    # --- the outlooks and the bill -------------------------------------------------------------------------------
    r("aeo05.elec.2003", 3657, "billion kWh", "Total US electricity consumption, purchases and on-site generation, 2003",
      "EIA, Annual Energy Outlook 2005", AEO05, "2003"),
    r("aeo05.elec.2025", 5467, "billion kWh", "AEO2005's projection of that consumption in 2025 (1.8% a year), led by "
      "'rapid growth in electricity use for computers, office equipment, and a variety of electrical appliances'",
      "EIA, Annual Energy Outlook 2005", AEO05, "2005 projection for 2025", "tracker"),
    r("aeo21.gen", 5.83, "cents per kWh", "Generation's part of the average US retail price, 2020 (10.42 cents in all)",
      "EIA, Annual Energy Outlook 2021, Table 8", AEO21, "2020"),
    r("aeo21.trans", 1.35, "cents per kWh", "Transmission's part of the average US retail price, 2020",
      "EIA, Annual Energy Outlook 2021, Table 8", AEO21, "2020"),
    r("aeo21.dist", 3.25, "cents per kWh", "Distribution's part of the average US retail price, 2020",
      "EIA, Annual Energy Outlook 2021, Table 8", AEO21, "2020"),
    r("caiso.solar.cap", 25, "GW", "Utility-scale solar capacity in the California ISO, April 2026 (+19% since April "
      "2024)", "EIA, Today in Energy, 16 June 2026", TIE_CAISO, "2026-04"),
    r("caiso.battery.cap", 16, "GW", "Net battery storage capacity in the California ISO, April 2026 (+79% since April "
      "2024)", "EIA, Today in Energy, 16 June 2026", TIE_CAISO, "2026-04"),
    r("caiso.gas.cap", 29, "GW", "Natural gas capacity in the California ISO, April 2026, nearly unchanged",
      "EIA, Today in Energy, 16 June 2026", TIE_CAISO, "2026-04"),
    r("caiso.solar_days", 82, "%", "Days in January-May 2026 on which CAISO's utility-scale solar out-generated natural "
      "gas (21% in 2024 and 2025)", "EIA, Today in Energy, 16 June 2026", TIE_CAISO, "2026-01 to 2026-05"),
    r("caiso.battery_x", 3, "times", "Battery discharge in CAISO, January-May 2026 against the same months of 2024",
      "EIA, Today in Energy, 16 June 2026", TIE_CAISO, "2026-01 to 2026-05"),
    r("dc.share.2023", 4.4, "%", "Data centers' share of US electricity, 2023 (176 TWh; 58 TWh in 2014)", "US Department "
      "of Energy, on Lawrence Berkeley National Laboratory's 2024 United States Data Center Energy Usage Report", DOE_DC,
      "2023", "study"),
    r("dc.twh.2014", 58, "TWh", "US data centers' electricity use, 2014", "US Department of Energy (LBNL report)", DOE_DC,
      "2014", "study"),
    r("dc.twh.2023", 176, "TWh", "US data centers' electricity use, 2023", "US Department of Energy (LBNL report)", DOE_DC,
      "2023", "study"),
    r("dc.twh.2028", 452.5, "TWh", "US data centers' electricity use projected for 2028: 325-580 TWh (6.7-12% of US "
      "electricity)", "US Department of Energy (LBNL report)", DOE_DC, "2028 projection", "study", lo=325, hi=580),
)
