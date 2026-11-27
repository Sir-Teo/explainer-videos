# Industry, Built: Part 20, Pharmaceuticals

Part 20 of a sixty-four-part series on how each industry works (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the sixth of Act III, *Making*. It asks: why does a pill that costs cents to make sell for
dollars, and then one day for cents? It answers with Pfizer's 2012 annual report, the 2025 annual reports of Eli Lilly and
Merck and Lilly's results releases of February 2025, February 2026 and October 2026; the SEC company facts of fifteen drug,
biotech and generics companies; BIO, Informa and QLS's study of clinical development success rates, 2011-2020; the FDA's
study of generic competition and prices, its generic approvals and its lists of novel drugs; the Centers for Medicare &
Medicaid Services' fact sheet on the first negotiated prices; the BLS's drug producer prices, the Federal Reserve's
medicine output and the CPI (via FRED); and the Works' drug company. The answer: most candidate drugs fail, mostly in
Phase II, and the ones that succeed take about ten and a half years from the first human test to approval, so each
approved medicine carries the cost of about a dozen failures and of the years of waiting; while it is protected by patents
and exclusivity its price is set by what it is worth to patients and payers, not by what it costs to make; when
protection ends, copies arrive and the price falls to near the cost of making it; so a drug company is a few protected
products and a calendar, and spends its years before each date building or buying the next ones.

It opens on Lipitor's fall: Pfizer sold $10.7bn of it in 2010, $9.6bn in 2011 and $3.9bn in 2012, the year after its US
exclusivity ended (-59%); on Lilly's tirzepatide (Mounjaro and Zepbound), $36.5bn in 2025 and 56% of Lilly's revenue; and
on Keytruda, 49% of Merck's sales, whose main US patent ends in 2028. From there it covers:

- Run it: pay for Phase III? A drug has passed Phase II, with a 30% chance of a big market ($3bn a year at its peak) and
  70% of a small one ($150m). Phase III costs $250m; going on is worth +$2.63bn if the market is big and -$108m if it is
  small. Committing to Phase III whatever happens is worth $712m; keeping the right to stop, $788m; the option to stop,
  $76m. With BIO's odds, one approval needs about 12.7 candidates entering Phase I, 6.6 entering Phase II, 1.9 entering
  Phase III and 1.1 submissions;
- from molecule to medicine: Phase I (2.3 years), Phase II (3.6), Phase III (3.3) and FDA review (1.3), 10.5 years in all;
  of 100 candidates entering Phase I, 52 reach Phase II, 15 Phase III, 9 are submitted and 8 approved;
- the odds: 52.0%, 28.9%, 57.8% and 90.6% by phase, 7.9% in all; Phase II from 48.1% (hematology) to 15.0% (urology);
  approval from 23.9% (hematology) and 17.0% (rare diseases) to 5.9% (chronic, common diseases) and 5.3% (oncology),
  which had 1,628 of the programmes;
- the cost of one medicine: about $94m spent on the average candidate, $1.20bn per approved drug, and $2.57bn with the
  waiting counted at 10.5% a year (a dollar spent at the start must return $2.85 by approval); research and development
  from Regeneron's 41% and Vertex's 33% of revenue to Teva's 6%; $102.6bn across fourteen companies in 2025, 21% of
  their revenue;
- a drug's life: the Works' drug, a ramp to $2bn a year, twelve years of exclusivity and the cliff, worth $5.8bn at
  launch, 96% of it earned before the cliff; Merck's later Keytruda patents;
- the cliff: the FDA's generic prices, 39% below the brand's with one generic maker, 54% with two, 79% with four and more
  than 95% with six or more, a median of 40% of the brand's price; 633 to 773 generic approvals a year from 2021 to 2024;
  Lipitor, country by country;
- an intermission: drug producer prices up 8.3 times since 1982 against 3.3 for consumer prices (2.5 times relative);
  America's medicine output, 4.4 times its 1972 level at its 2007 peak, down by a quarter to 2019, 3.9 times in 2025;
  novel drugs approved: 50, 37, 55, 50 and 46 from 2021 to 2025;
- companies of a few products: Keytruda's $31.6bn; Pfizer's revenue from about $41bn (2018-2020) to $81.3bn (2021) and
  $101.2bn (2022), and $59.6bn in 2023; Merck's $9.2bn purchase of Cidara in January 2026;
- the price, and Medicare's turn: the maker, the wholesaler, the pharmacy, the insurer and its benefit manager, and
  rebates; the first ten negotiated drugs, used by 8.8 million people in 2023, $6bn (22%) less net spending had the prices
  applied that year; the timeline, from the first offers on 1 February 2024 to agreement on 1 August 2024 and the prices in
  force on 1 January 2026;
- a boom: tirzepatide, $16.5bn in 2024 and $36.5bn in 2025; Mounjaro outside America from $2.6bn to $9.3bn; Zepbound's
  $13.5bn, almost all in America; Lilly's capital expenditure from $3.4bn (2023) to $7.8bn (2025), ten new sites, its
  inventories from $5.8bn to $13.7bn and up to about $10bn of supply commitments; its third quarter of 2026, $24.4bn, up
  39%;
- biotech: Moderna's revenue from $60m (2019) to $18.5bn (2021) and $1.9bn (2025); Vertex and Regeneron, which keep about a
  third of revenue as profit; big companies buying small ones;
- the landscape, November 2026: fifteen companies by revenue and median margin, 2021-2025; the dollar of thirteen
  companies' revenue in 2025 (making 26 cents, research 20, everything else 36, profit 18); and the map of the business;
- *Called it?*: Lilly's guidance (2025: $58.0-61.0bn against $65.2bn; 2026: $80-83bn, raised in October to $91-92bn) and
  this series' call that Lilly's 2026 revenue will reach at least $92.0bn (55%);
- cents and dollars: the answer, and the trade every country argues over.

## Build it

```bash
python -m videos.industry.industry20.compute               # every number, printed
EXPLAINER_TTS=silent python tools/build.py industry20 -q l  # the whole part, silent preview
python tools/build.py industry20                           # 1080p30 with narration
python -m videos.industry.labs 20                          # the lab
python -m pytest tests/industry                            # the Register and the Works (test_pharma.py)
```

Every figure is a row of the Register (`explainer/industry/data/rows_p20.py`) or comes from the Filing Room: the drug
companies' accounts (`sec_pharma.csv`) and FRED's drug producer prices, medicine output and consumer prices
(`fred_pharma.csv`).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | The cliff | Lipitor before and after 2011; tirzepatide and Keytruda; the title |
| 1 | Run it: pay for Phase III? | The decision tree; the option to stop; the pipeline one approval needs |
| 2 | From molecule to medicine | The phases and their years; a hundred candidates through the funnel |
| 3 | The odds | Success by phase; Phase II by disease; approval by disease |
| 4 | The cost of one medicine | The arithmetic; the cost of waiting; research as a share of revenue; the total |
| 5 | A drug's life | The sales curve; the value before and after the cliff; patents |
| 6 | The cliff | Generic prices by number of makers; generic approvals; Lipitor's fall |
| — | Intermission | Drug prices against all prices; medicine output; novel approvals |
| 7 | Companies of a few products | Keytruda's share; Pfizer's revenue; the dates |
| 8 | The price, and Medicare's turn | The channel and rebates; the first ten drugs; the negotiation's timeline |
| 9 | A boom: the weight-loss drugs | Tirzepatide; outside America; Lilly's factories; the third quarter of 2026 |
| 10 | Biotech: the small companies | Moderna's arc; the biotechs that made it; buying the pipeline |
| 11 | The landscape, November 2026 | Revenue against margin; where the dollar goes; the map of the business |
| 12 | Called it? | Lilly's guidance; this series' call |
| — | Cents and dollars | The answer; Part 21, medical technology |

## What is computed, and from what

`compute.py` reads the Filing Room and the Register. The drug company is the Works' (`explainer/industry/works/pharma.py`):
the phase durations and success rates are BIO's (2011-2020, all diseases); the stage costs ($25m, $60m, $250m and $5m),
the cost of capital (10.5% a year), the drug's peak, ramp, exclusivity, margin (60% of sales after making and selling it)
and its erosion after the cliff (40%, 12%, 6%, 4% and then 3% of the last protected year) are illustrations, labelled on
screen. A stage's cost is paid by the candidates that reach it; the capitalized cost compounds each stage's spending from
its start to approval. In Run it, Phase III's cost is paid now, review's at the end of Phase III, and the drug's value at
launch is discounted over Phase III and review (4.6 years). Margins are profit attributable to the parent over revenue
from the companies' filings; the landscape uses the median of 2021-2025. Johnson & Johnson's research line in company
facts is not its total (0.1% of revenue), so it is left out of research measures and of the dollar, which also leaves out
Regeneron and Novartis, whose facts lack a cost or revenue line for 2025. Producer and consumer prices are annual
averages, the CPI of eleven months in 2025 (the BLS published no October 2025 CPI); medicine output is the annual average
of the Federal Reserve's index, set to 1 in 1972. Lipitor's sales are Pfizer's worldwide revenue from it.

## Problems and solutions

**1.** *A candidate entering Phase I passes it with probability 0.520, Phase II with 0.289, Phase III with 0.578 and FDA
review with 0.906. The stages cost $25m, $60m, $250m and $5m, paid only by candidates that reach them. What does the
average candidate cost, what share is approved, and what is the out-of-pocket cost per approved drug?*

*Solution.* The candidate reaches Phase II with probability 0.520, Phase III with 0.520 × 0.289 = 0.150 and review with
0.150 × 0.578 = 0.0869; it is approved with 0.0869 × 0.906 = 0.0787. Expected spending is 25 + 60 × 0.520 + 250 × 0.150 +
5 × 0.0869 = 25 + 31.2 + 37.6 + 0.4 = $94.2m. Each approval carries 1 / 0.0787 = 12.7 candidates, so 94.2 / 0.0787 =
$1.20bn per approved drug, before counting the years of waiting.

**2.** *A drug has passed Phase II. If its market is big (probability 0.3) it is worth $8.70bn at launch; if small,
$0.435bn. Phase III costs $250m now and succeeds with 0.578; review costs $5m 3.3 years from now and succeeds with 0.906;
launch is 4.6 years from now. At 10.5% a year, what is going on worth in each case, and what is the option to stop worth?*

*Solution.* 1.105^3.3 = 1.390 and 1.105^4.6 = 1.583. Big: -250 - 0.578 × 5 / 1.390 + 0.578 × 0.906 × 8,701 / 1.583 =
-250 - 2.1 + 2,878.6 = $2,626m. Small: -250 - 2.1 + 0.5237 × 435.1 / 1.583 = -250 - 2.1 + 143.9 = -$108m. Committing
whatever the market: 0.3 × 2,626 + 0.7 × (-108) = $712m. Stopping when it is small: 0.3 × 2,626 + 0.7 × 0 = $788m. The
right to stop is worth 788 - 712 = $76m: the value of the information Phase II bought.

**3.** *A brand sells for $10 a pill before generic competition. Using the FDA's estimates (prices 39% below the brand's
with one generic maker, 54% with two, 79% with four and more than 95% with six or more), what do generics sell for in each
case? Lipitor's sales were $9,577m in 2011 and $3,948m in 2012; by how much did they fall?*

*Solution.* $6.10 with one maker, $4.60 with two, $2.10 with four and less than $0.50 with six or more. Lipitor fell by
1 - 3,948 / 9,577 = 58.8%, in the first full year after its US exclusivity ended in November 2011; the generic makers' price
was never Pfizer's, and Pfizer's own sales of the brand fell as patients and insurers moved to the copies.

**4.** *With the success rates of Problem 1, how many candidates must enter each stage, on average, for one approval? A
company wants two new drugs a year. How many candidates must it start each year?*

*Solution.* Entering review: 1 / 0.906 = 1.10; Phase III: 1.10 / 0.578 = 1.91; Phase II: 1.91 / 0.289 = 6.61; Phase I:
6.61 / 0.520 = 12.7. Two approvals a year need about 2 × 12.7 = 25 candidates entering Phase I every year, about 13 entering
Phase II and 4 entering Phase III; most of the company's decisions are which ones to stop.

**5.** *In 2025 thirteen drug companies had $482bn of revenue, $127bn of cost of sales, $96.7bn of research and
development and $84.7bn of net income. Split a dollar of their revenue. Medicare says its first ten negotiated prices would
have saved $6bn, 22% of its net spending on those drugs, had they applied in 2023. What was that net spending?*

*Solution.* Making: 127 / 482 = 26 cents; research: 96.7 / 482 = 20 cents; profit: 84.7 / 482 = 18 cents; everything else
(selling, running the company, write-offs of bought research, interest and taxes): 100 - 26 - 20 - 18 = 36 cents. Net
spending was about 6 / 0.22 = $27bn, so the negotiated prices would have cost Medicare about $21bn.

## Glossary

- **Candidate (drug candidate):** a molecule a company is testing as a possible medicine.
- **Phase I, II, III:** the three stages of human trials: safety in a small group; whether it works at all, in patients;
  and large trials against a placebo or the best existing treatment.
- **Likelihood of approval:** the probability that a candidate entering Phase I is eventually approved.
- **Cost of capital:** the return investors could have had elsewhere, which money tied up for years must also earn.
- **Patent:** a legal right to stop others making a new invention for a period, usually twenty years from filing.
- **Exclusivity:** the time in which no copy of a drug may be sold, from its patents and from the regulator's own rules.
- **Loss of exclusivity (the patent cliff):** the date copies may be sold, and the fall in sales that follows.
- **Generic:** a copy of a small-molecule drug, shown to the regulator to work the same way.
- **Biologic and biosimilar:** a medicine made in living cells, and a near copy of one.
- **Blockbuster:** a drug with sales of a billion dollars or more a year.
- **Rebate:** a payment from a drug maker back to an insurer or benefit manager, often for a good place on its list.
- **Pharmacy benefit manager:** a company that runs an insurer's drug benefit and negotiates with makers.
- **Biotech company:** a company built on a new science of medicine, often with one or a few drugs.
- **Guidance:** a company's own published forecast of its year.

## Lab and interactive

- `python -m videos.industry.labs 20`: Lipitor's fall; the Phase III decision and the option to stop; the phases and the
  funnel; success by phase and by disease; the cost per approval, out of pocket and capitalized; research shares; the
  Works' drug and its cliff; the FDA's generic prices; approvals; producer prices and output; Keytruda and Pfizer; the
  Medicare negotiation; tirzepatide and Lilly's factories; the biotech companies; the landscape and the dollar; and the
  forecasts, with this series' call.
- The interactive (course site): the pipeline. Set the phase odds, the stage costs, the cost of capital and the drug's peak
  and exclusivity, and see the cost per approved drug, the drug's value and whether the pipeline pays.

## Sources

Every figure is in the Register (`explainer/industry/data/rows_p20.py`) or the Filing Room
(`explainer/industry/data/SOURCES.md`). The main ones:

- SEC EDGAR: Pfizer's Form 10-K 2012 (Exhibit 13); the Forms 10-K 2025 of Eli Lilly and Merck; Lilly's Forms 8-K of
  6 February 2025, 4 February 2026 and 29 October 2026; the company facts of Pfizer, Merck, Johnson & Johnson, Eli Lilly,
  AbbVie, Bristol Myers Squibb, Amgen, Gilead, Vertex, Regeneron, Biogen, Moderna, Teva, Viatris, AstraZeneca and Novartis.
- BIO, Informa Pharma Intelligence and QLS Advisors, *Clinical Development Success Rates 2011-2020* (2021).
- US Food and Drug Administration: *Generic Competition and Drug Prices: New Evidence Linking Greater Generic Competition
  and Lower Generic Drug Prices* (2019); generic approvals by year; novel drug approvals, 2021-2025.
- Centers for Medicare & Medicaid Services: fact sheet on the negotiated prices for initial price applicability year 2026.
- FRED: the BLS's producer price index for pharmaceutical preparations and the CPI-U; the Federal Reserve's industrial
  production of pharmaceuticals and medicines.
