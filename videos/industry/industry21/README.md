# Industry, Built: Part 21, Medical Technology

Part 21 of a sixty-four-part series on how each industry works (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the seventh of Act III, *Making*. It asks: who is the customer when the one who uses it,
the one who chooses it and the one who pays are three different people? It answers with the 2025 annual reports of
Intuitive Surgical, Abbott, Boston Scientific, Stryker, Quest Diagnostics, GE HealthCare and Edwards Lifesciences,
Medtronic's for fiscal 2026 and Abbott's for 2022; Intuitive's report for the third quarter of 2026 and its results
releases of January 2025, January 2026 and October 2026; the SEC company facts of twenty-three device, imaging, tools,
laboratory and contract research companies; openFDA's 510(k), De Novo, premarket approval and recall records; the BLS's
instrument producer prices, the Federal Reserve's output of medical equipment and the CPI (via FRED); and the Works' robot
market. The answer: the surgeon chooses, and skill learned on one system ties the surgeon to it; the hospital buys, out of
a capital budget, and increasingly lets the maker place the machine and pays by use; the payer sets the price, and where
it buys for a nation, as in China, it sets it low; and the maker earns most after the sale, from the instruments, service
and tests that the installed base buys again and again. Most devices reach the market by comparison with the last one,
so they improve by small steps, rivals follow fast, and an advantage lasts until the next procedure rather than until a
patent date.

It opens on Intuitive's da Vinci robots: about 3.15 million operations in 2025 on 11,106 robots, about 300 operations a
robot a year; a robot sells for $0.7m to $3.1m, and each operation brings $900 to $3,700 of instruments; and on the four
people around one purchase. From there it covers:

- Run it: sell the robot, or place it? In the Works' market of 101 hospitals doing 50 to 550 robotic operations a year,
  each worth $4,000 to a hospital and using $1,800 of instruments, selling at $2m with a service contract brings 61
  buyers (those doing 247 or more a year), $258m of value and 24,400 operations a year; placing robots free at $1,000 an
  operation brings all 101, $232m and 30,300 operations, with 11 placements below the break-even of 103 a year; at
  $1,159 an operation placing pays as well as selling. Intuitive had 3,210 robots on operating leases at the end of 2025,
  1,810 paid by use (1,023 in 2023), and $874m of lease revenue ($500m in 2023);
- four businesses: implants and therapies (Medtronic's $36.4bn in fiscal 2026: Cardiovascular $14.0bn, Neuroscience
  $10.3bn, Medical Surgical $8.8bn, Diabetes $3.1bn); equipment and service (GE HealthCare's $13.7bn of products and $7.0bn
  of services); consumables (Dexcom's revenue from $100m in 2012 to $4.7bn in 2025); and diagnostics (Quest's 244 million
  requisitions, $10.8bn, about $44 each);
- two roads to market: about 3,140 510(k) clearances, 35 De Novo grants and 29 original premarket approvals a year
  (2021-2025); 510(k)s of 2025 by panel, led by radiology (478) and orthopedics (404); products in Class I recalls, from 51
  (2017) to 558 (2014) a year, 495 in 2023 from 80 recall events, the largest naming 123;
- the surgeon, the hospital and the payer: Intuitive's clinical sales team on site; Stryker's Mako robot, more than 2
  million operations; robot placements heavier in the fourth quarter as budgets reset; consolidated purchasing and its
  pricing pressure; Quest's payer mix (insurers 43% of tests and 39% of revenue, government 17% and 16%, clients 37% and
  31%, patients 1% and 12%); benign operations that rise when deductibles are met;
- the installed base: Intuitive's revenue by kind, 2023-2025, 84% recurring; GE HealthCare's gross margins, 35% on
  products and 51% on services; a hospital's five years with one robot, about $5.3m (robot $1.9m, service $0.64m,
  instruments $2.7m), about $3,520 an operation; the hospitals' antitrust case over instrument repair and Intuitive's
  $450m settlement charge in the third quarter of 2026;
- diagnostics: Quest's revenue per requisition (-5.9%, +1.3%, +0.1% in 2023-2025) against its volume (+12.3% in 2025,
  3.4% organic); Abbott's COVID-19 tests, $3.9bn (2020), $7.7bn, $8.4bn (2022), then $1.6bn, $0.75bn and $0.30bn (2025);
  laboratories' median margins (Quest 9%, Labcorp 6%) against the makers of instruments and tests (15% to 20%);
- an intermission: instrument producer prices up 1.47 times since 1986 against 2.94 for consumer prices (half, relative);
  output of medical equipment 5.2 times its 1972 level, down 1% in 2009; 510(k) clearances since 1977, a peak of 5,644 in
  1994 and about 3,000 a year since;
- a new procedure: pulsed field ablation; Boston Scientific's electrophysiology sales, $0.8bn (2023), $1.9bn, $3.3bn
  (2025), and its total revenue from $14.2bn to $20.1bn; $386m of write-downs, mostly of cryoablation; Medtronic's
  heart-rhythm sales up 17%; Watchman from $1.27bn to $1.96bn;
- picks and shovels: Thermo Fisher ($44.6bn), Danaher ($24.6bn), IQVIA ($16.3bn), Agilent ($6.9bn), Illumina ($4.3bn);
  Thermo Fisher's pandemic years; IQVIA from $4.3bn (2011) to $16.3bn; Illumina's stall and losses in 2022-2024;
- China's procurement: where the robots are (6,364 in the US, 2,168 in Europe, 1,993 in Asia, 581 elsewhere);
  volume-based procurement in Stryker's, Abbott's and GE HealthCare's words; China's quota of 559 surgical robots (2023)
  and its provinces' caps on charges for robotic surgery;
- the landscape, November 2026: twenty-one companies by revenue and median margin; a dollar of thirteen device makers'
  revenue (making 39 cents, research 8, everything else 40, profit 12) beside Part 20's drug makers (26, 20, 36, 18); and
  the map of the business;
- *Called it?*: Intuitive's procedure guidance (2025: 13-16% against 18%; 2026: 13-15%, narrowed to 14-15%), why it
  forecasts operations, and this series' call that it will report 2026 growth of 15% or more (45%);
- the three customers: the five answers.

## Build it

```bash
python -m videos.industry.industry21.compute               # every number, printed
EXPLAINER_TTS=silent python tools/build.py industry21 -q l  # the whole part, silent preview
python tools/build.py industry21                           # 1080p30 with narration
python -m videos.industry.labs 21                          # the lab
python -m pytest tests/industry                            # the Register and the Works (test_medtech.py)
```

Every figure is a row of the Register (`explainer/industry/data/rows_p21.py`) or comes from the Filing Room: the companies'
accounts (`sec_medtech.csv`), FRED's prices, output and jobs (`fred_medtech.csv`) and openFDA's counts
(`fda_devices.csv`, `fda_510k_panels.csv`).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Three customers | Intuitive's robots and instruments; the surgeon, the hospital, the payer and the patient; the title |
| 1 | Run it: sell the robot, or place it? | The market; selling; placing; the fee that pays as well; Intuitive's leases |
| 2 | Four businesses | Medtronic's segments; GE HealthCare's products and services; Dexcom; Quest |
| 3 | Two roads to market | 510(k), PMA and De Novo; the counts; the panels; Class I recalls |
| 4 | The surgeon, the hospital and the payer | The sales team and the Mako robot; budgets and purchasing; who pays a laboratory; deductibles |
| 5 | The installed base | Intuitive's revenue by kind; GE HealthCare's margins; a hospital's five years; the repair case |
| 6 | Diagnostics: the laboratory | Requisitions; price against volume; Abbott's tests; laboratories against makers |
| — | Intermission | Instrument prices against all prices; output; 510(k)s since 1977 |
| 7 | A new procedure: pulsed field ablation | The procedure; Boston Scientific's sales; write-downs and rivals; Watchman |
| 8 | Picks and shovels | The suppliers; Thermo Fisher; IQVIA; Illumina |
| 9 | China's procurement | Where the robots are; volume-based procurement; its effects; the robot quota |
| 10 | The landscape, November 2026 | Revenue against margin; the device dollar beside the drug dollar; the map |
| 11 | Called it? | Intuitive's guidance; why operations; this series' call |
| — | The three customers | The five answers; Part 22, consumer goods |

## What is computed, and from what

`compute.py` reads the Filing Room and the Register. The robot market is the Works' (`explainer/industry/works/medtech.py`):
101 hospitals evenly spaced from 50 to 550 robotic operations a year; a hospital gains $4,000 an operation and pays $1,800
of instruments (Intuitive: $900 to $3,700, about $1,830 on average); a sold robot costs $2.0m with service at $160,000 a
year (Intuitive: $0.7m to $3.1m and $95,000 to $225,000); the maker builds a robot for $0.9m, instruments for $550 an
operation and services one for $60,000 a year; seven years at 8%. A hospital buys if the discounted gain less service covers
the price; a placed robot (service included) is taken whenever the fee leaves the hospital a gain. A hospital's five years
use the middle of Intuitive's ranges ($1.9m and $160,000) and its instruments revenue per operation in 2025 ($6,019m over
3.15 million da Vinci and 144,100 Ion operations, rounded to $1,830). Operations per robot divide 2025's operations by the
average of the installed bases at the ends of 2024 and 2025. openFDA's counts are summed by calendar year of the decision or
report: 510(k)s found substantially equivalent; De Novo decisions (numbers beginning DEN); original PMAs approved
(supplement number empty); Class I recall products (each product in an enforcement report). Margins are profit
attributable to the parent over revenue, by fiscal year (Medtronic's ends in April, BD's in September, ResMed's in June,
Steris's in March; a year ending in the first week of January counts as the one before); the landscape uses the median of
2021-2025. The device dollar sums thirteen device makers' latest fiscal years (Abbott, with its nutrition and medicines, is
left out). Producer and consumer prices are annual averages (eleven months of CPI in 2025: the BLS published no October 2025
CPI); output is the Federal Reserve's annual average, 1972 = 1.

## Problems and solutions

**1.** *A hospital would do N robotic operations a year. Each gains it $4,000 and uses $1,800 of instruments. A robot costs
$2.0m with a service contract of $160,000 a year, and lasts seven years; money costs 8% a year (a seven-year annuity factor
of 5.206). Above what N does the hospital buy?*

*Solution.* It buys if 5.206 × (2,200 N - 160,000) ≥ 2,000,000, that is 2,200 N ≥ 2,000,000 / 5.206 + 160,000 = 384,150 +
160,000 = 544,150, so N ≥ 247 operations a year. In the Works' market of 101 hospitals spread evenly from 50 to 550, 61 do
that many.

**2.** *The maker instead places robots free, service included, and charges $1,000 an operation on top of the instruments.
A robot costs it $0.9m to build, instruments $550 an operation and service $60,000 a year. Below what volume does a placed
robot lose money?*

*Solution.* A placed robot is worth -900,000 + 5.206 × (N × (1,800 + 1,000 - 550) - 60,000). It breaks even when 2,250 N =
900,000 / 5.206 + 60,000 = 172,880 + 60,000 = 232,880, so N = 103.5. The eleven hospitals doing fewer than about 104
operations a year cost the maker money; the fee charges the big users more and carries the small ones.

**3.** *Intuitive's 2025 revenue was $6,018.9m from instruments and accessories, $2,473.7m from systems (of which $874.3m
from operating leases) and $1,572.1m from service. Its recurring revenue counts instruments, service and leases. What share
of revenue recurred, and how much did instruments bring per operation, given 3,153,000 da Vinci and 144,100 Ion
operations?*

*Solution.* Recurring: 6,018.9 + 1,572.1 + 874.3 = $8,465.3m of $10,064.7m, 84%. Instruments per operation: 6,018.9m /
3,297,100 = about $1,825, inside the $900 to $3,700 range the company gives.

**4.** *In 2025 GE HealthCare sold $13,661m of products at a cost of $8,942m and $6,964m of services at a cost of $3,436m.
Find each gross margin and services' share of revenue and of gross profit.*

*Solution.* Products: 1 - 8,942 / 13,661 = 34.5%; services: 1 - 3,436 / 6,964 = 50.7%. Services are 6,964 / 20,625 = 34%
of revenue but (6,964 - 3,436) / (20,625 - 12,378) = 3,528 / 8,247 = 43% of gross profit.

**5.** *Quest's revenue per requisition rose 0.1% in 2025 while its requisitions rose 12.3%, of which 3.4% organically.
Roughly how much did its laboratory revenue grow, and how much of that came from acquisitions? Its laboratory revenue was
$9,614m in 2024 and $10,785m in 2025.*

*Solution.* Revenue ≈ volume × price, so growth ≈ 1.123 × 1.001 - 1 = 12.4%; the reported figure is 10,785 / 9,614 - 1 =
12.2%. Organic volume was 3.4 points, so about 12.3 - 3.4 = 8.9 points of volume came from laboratories it bought (Quest
puts acquisitions' contribution to revenue at about 6.7%, since the laboratories it bought earn less per requisition).

## Glossary

- **510(k):** a premarket notification showing the FDA that a device is substantially equivalent to one already legally
  sold; the device is then cleared.
- **Premarket approval (PMA):** the FDA's review of a high-risk device, usually with clinical studies, before it may be
  sold.
- **De Novo:** the route for a new kind of low- or moderate-risk device with nothing to compare it to.
- **Recall, Class I:** a recall where there is a reasonable probability that the product will cause serious harm or death.
- **Installed base:** the machines a maker has placed that are still in use.
- **Placement, usage-based lease:** a machine put in a hospital and paid for by use rather than bought.
- **Consumables:** products used up and bought again, such as instruments, catheters, sensors and reagents.
- **Requisition:** an order for one or more laboratory tests on a patient's sample, with whom to bill.
- **Payer:** whoever pays for care: an insurer, a government programme or the patient.
- **Deductible:** the amount a patient pays each year before insurance starts to pay.
- **Pulsed field ablation:** destroying heart tissue that sets off an irregular rhythm with short pulses of electric field.
- **Volume-based procurement:** buying devices or medicines for many hospitals at once, in volume, for a lower price.
- **Contract research organization:** a company that runs clinical trials for drug and device makers.

## Lab and interactive

- `python -m videos.industry.labs 21`: Intuitive's robots and instruments; the Run it market, selling against placing and
  the fee that pays as well; Medtronic's segments, GE HealthCare's products and services, Dexcom and Quest; the FDA's
  roads and recalls; Quest's payers, price and volume; the installed base and a hospital's five years; Abbott's tests;
  prices and output; pulsed field ablation; the tools companies; the robots by region; the landscape and the device
  dollar; and Intuitive's forecasts, with this series' call.
- The interactive (course site): sell or place. Set the robot's price, the fee an operation, the hospitals' gain an
  operation and the instrument price, and see which hospitals buy or take one, the maker's value both ways, the
  operations done and the placements that lose money.

## Sources

Every figure is in the Register (`explainer/industry/data/rows_p21.py`) or the Filing Room
(`explainer/industry/data/SOURCES.md`). The main ones:

- SEC EDGAR: Forms 10-K 2025 of Intuitive Surgical, Abbott, Boston Scientific, Stryker, Quest Diagnostics, GE HealthCare
  and Edwards Lifesciences; Medtronic's Form 10-K for fiscal 2026; Abbott's Form 10-K 2022; Intuitive's Form 10-Q for the
  third quarter of 2026 and Forms 8-K of 23 January 2025, 22 January 2026 and 20 October 2026; the company facts of
  Medtronic, Abbott, Boston Scientific, Stryker, Intuitive, Edwards, BD, Zimmer Biomet, Baxter, Dexcom, Insulet, ResMed,
  Danaher, Thermo Fisher, Illumina, Labcorp, Quest, IQVIA, Agilent, Philips, Align, Steris and GE HealthCare.
- US Food and Drug Administration via openFDA: 510(k) and PMA decisions and device recall enforcement reports.
- FRED: the BLS's producer price indexes for surgical and medical instruments and for surgical appliances, its employment
  in miscellaneous durable goods manufacturing and the CPI-U; the Federal Reserve's industrial production of medical
  equipment and supplies.
