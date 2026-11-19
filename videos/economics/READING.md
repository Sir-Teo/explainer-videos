# Economics, Built: textbooks, papers and models

The series' reading in one place, written by `python -m videos.economics.reading` from
[`reading.py`](reading.py), the syllabus and the parts themselves; `tests/economics/test_reading.py` fails when
it is out of date. Section 1 is the textbook spine, tier by tier: the books an economics degree, a graduate
core and the practice are taught from. Section 2 maps the field's classic papers and models to the parts that
teach them. Section 3 is every built part's reference card, as it appears on screen, and section 4 says what
the series leaves out.

Both *Parts* columns are found, not typed. *Planned* lists the parts whose entry in
[`SYLLABUS.md`](SYLLABUS.md) names the book or paper; *Built* lists the parts whose scenes, compute step or
README cite it (a dot: none yet). Fuller notes (editions, chapters, what each source was used for) are in each
part's README, under *Sources*. Built so far: Parts 1–15.

## 1. The textbook spine

### Principles

| Short name | Book | Planned | Built |
|---|---|---|---|
| Mankiw | N. G. Mankiw, *Principles of Economics* (10th ed., 2024) | 1–2 | 1–3 |
| Krugman–Wells | P. Krugman and R. Wells, *Economics* (6th ed., 2021) | 2 | 2 |
| Acemoglu–Laibson–List | D. Acemoglu, D. Laibson and J. List, *Economics* (3rd ed., 2022) | 4 | 4 |
| CORE | The CORE Team, *The Economy* (2017; 2.0, 2023) | 1 | 1, 9 |
| Heilbroner | R. Heilbroner, *The Worldly Philosophers* (7th ed., 1999) | 1 | 1 |

### The major

| Short name | Book | Planned | Built |
|---|---|---|---|
| Varian | H. Varian, *Intermediate Microeconomics* (9th ed., 2014) | 2, 5–8, 10 | 2, 5–8, 10 |
| Nicholson–Snyder | W. Nicholson and C. Snyder, *Microeconomic Theory* (13th ed., 2021) | 5–6 | 5–6, 8 |
| Jones | C. I. Jones, *Macroeconomics* (6th ed., 2023) | 20 | · |
| Blanchard | O. Blanchard, *Macroeconomics* (8th ed., 2021) | 27, 32 | · |
| Stock–Watson | J. Stock and M. Watson, *Introduction to Econometrics* (4th ed., 2019) | 4 | 4 |
| Angrist–Pischke | J. Angrist and J.-S. Pischke, *Mostly Harmless Econometrics* (2009) | 4, 50, 67 | 4 |
| Osborne | M. Osborne, *An Introduction to Game Theory* (2004) | 11 | 11 |
| Krugman–Obstfeld–Melitz | P. Krugman, M. Obstfeld and M. Melitz, *International Economics* (12th ed., 2022) | 34–35 | · |
| Mishkin | F. Mishkin, *The Economics of Money, Banking, and Financial Markets* (13th ed., 2022) | 26 | · |
| Cabral | L. Cabral, *Introduction to Industrial Organization* (2nd ed., 2017) | 12–13 | 12–13 |
| Borjas | G. Borjas, *Labor Economics* (8th ed., 2020) | 38 | · |
| Gruber | J. Gruber, *Public Finance and Public Policy* (7th ed., 2022) | 15, 41–42, 50 | 7, 15 |
| Ray | D. Ray, *Development Economics* (1998) | 46 | · |
| Weil | D. Weil, *Economic Growth* (3rd ed., 2013) | 7, 19 | 3, 7 |

### Graduate micro

| Short name | Book | Planned | Built |
|---|---|---|---|
| MWG | A. Mas-Colell, M. Whinston and J. Green, *Microeconomic Theory* (1995) | 5–9, 11, 13, 15, 18, 56 | 5–11, 13, 15 |
| Kreps | D. Kreps, *Microeconomic Foundations I* (2013) | 5, 7, 9, 11, 56 | 5, 7, 9, 11–13 |
| Jehle–Reny | G. Jehle and P. Reny, *Advanced Microeconomic Theory* (3rd ed., 2011) | 5, 9 | 5–6, 9 |
| Fudenberg–Tirole | D. Fudenberg and J. Tirole, *Game Theory* (1991) | 11–12, 53 | 11–12 |
| Osborne–Rubinstein | M. Osborne and A. Rubinstein, *A Course in Game Theory* (1994) | 11 | 11 |
| Bolton–Dewatripont | P. Bolton and M. Dewatripont, *Contract Theory* (2005) | 13–14 | 13–14 |
| Krishna | V. Krishna, *Auction Theory* (2nd ed., 2010) | 16 | · |
| Milgrom | P. Milgrom, *Putting Auction Theory to Work* (2004) | 16 | · |
| Roth–Sotomayor | A. Roth and M. Sotomayor, *Two-Sided Matching* (1990) | 17 | · |
| Börgers | T. Börgers, *An Introduction to the Theory of Mechanism Design* (2015) | 17 | · |
| Tirole IO | J. Tirole, *The Theory of Industrial Organization* (1988) | 10–12, 53 | 10, 12 |

### Graduate macro

| Short name | Book | Planned | Built |
|---|---|---|---|
| Romer | D. Romer, *Advanced Macroeconomics* (5th ed., 2019) | 20, 22–23, 28–29, 56 | · |
| Ljungqvist–Sargent | L. Ljungqvist and T. Sargent, *Recursive Macroeconomic Theory* (4th ed., 2018) | 29, 52, 56 | · |
| SLP | N. Stokey, R. Lucas and E. Prescott, *Recursive Methods in Economic Dynamics* (1989) | 29, 51 | · |
| Acemoglu | D. Acemoglu, *Introduction to Modern Economic Growth* (2009) | 20–21 | · |
| Galí | J. Galí, *Monetary Policy, Inflation, and the Business Cycle* (2nd ed., 2015) | 30, 56 | · |
| Woodford | M. Woodford, *Interest and Prices* (2003) | 30 | · |
| Walsh | C. Walsh, *Monetary Theory and Policy* (4th ed., 2017) | 25 | · |
| Obstfeld–Rogoff | M. Obstfeld and K. Rogoff, *Foundations of International Macroeconomics* (1996) | 34 | · |
| Pissarides | C. Pissarides, *Equilibrium Unemployment Theory* (2nd ed., 2000) | 24 | · |
| Cochrane | J. Cochrane, *Asset Pricing* (rev. ed., 2005) | 23 | · |
| Freixas–Rochet | X. Freixas and J.-C. Rochet, *Microeconomics of Banking* (2nd ed., 2008) | 26 | · |

### Econometrics and computation

| Short name | Book | Planned | Built |
|---|---|---|---|
| Hayashi | F. Hayashi, *Econometrics* (2000) | 54, 56 | · |
| Wooldridge | J. Wooldridge, *Econometric Analysis of Cross Section and Panel Data* (2nd ed., 2010) | 54 | · |
| Hansen | B. Hansen, *Econometrics* (2022) | 54 | · |
| Hamilton | J. Hamilton, *Time Series Analysis* (1994) | 55 | 6 |
| Kilian–Lütkepohl | L. Kilian and H. Lütkepohl, *Structural Vector Autoregressive Analysis* (2017) | 55 | · |
| Train | K. Train, *Discrete Choice Methods with Simulation* (2nd ed., 2009) | 43, 54 | · |
| Judd | K. Judd, *Numerical Methods in Economics* (1998) | 51 | · |
| QuantEcon | T. Sargent and J. Stachurski, *Quantitative Economics* (QuantEcon lectures) | 51 | · |

### The fields

| Short name | Book | Planned | Built |
|---|---|---|---|
| Feenstra | R. Feenstra, *Advanced International Trade* (2nd ed., 2016) | 6, 35–36 | 6, 8 |
| Cahuc–Carcillo–Zylberberg | P. Cahuc, S. Carcillo and A. Zylberberg, *Labor Economics* (2nd ed., 2014) | 24, 38 | · |
| Atkinson–Stiglitz | A. Atkinson and J. Stiglitz, *Lectures on Public Economics* (1980; 2015) | 41 | 6 |
| Salanié | B. Salanie, *The Economics of Taxation* (2nd ed., 2011) | 41 | 13–14 |
| Banerjee–Duflo | A. Banerjee and E. Duflo, *Poor Economics* (2011) | 46 | · |
| Persson–Tabellini | T. Persson and G. Tabellini, *Political Economics* (2000) | 47 | · |
| Dhami | S. Dhami, *The Foundations of Behavioral Economic Analysis* (2016) | 45 | · |
| Fujita–Krugman–Venables | M. Fujita, P. Krugman and A. Venables, *The Spatial Economy* (1999) | 37 | · |
| Nordhaus | W. Nordhaus, *A Question of Balance* (2008) | 48 | · |
| Jackson | M. Jackson, *Social and Economic Networks* (2008) | 63 | · |

### Practice

| Short name | Book | Planned | Built |
|---|---|---|---|
| Blinder | A. Blinder, *Central Banking in Theory and Practice* (1998) | 31 | · |
| Boardman | A. Boardman and others, *Cost-Benefit Analysis* (5th ed., 2018) | 50, 58 | · |
| Davis–Garcés | P. Davis and E. Garces, *Quantitative Techniques for Competition and Antitrust Analysis* (2010) | 59 | · |
| Talluri–van Ryzin | K. Talluri and G. van Ryzin, *The Theory and Practice of Revenue Management* (2004) | 10, 60 | 10 |
| Kohavi–Tang–Xu | R. Kohavi, D. Tang and Y. Xu, *Trustworthy Online Controlled Experiments* (2020) | 61 | · |
| Lazear–Gibbs | E. Lazear and M. Gibbs, *Personnel Economics in Practice* (3rd ed., 2014) | 62 | · |

## 2. Papers and models, and where they are taught

### Markets and prices

| Model or result | Paper | Planned | Built |
|---|---|---|---|
| the division of labour | Smith (1776), *The Wealth of Nations* | 1 | 1–2 |
| comparative advantage | Ricardo (1817), *Principles*, ch. 7 | 2, 8, 35–36 | 1–2, 8 |
| supply and demand, the scissors | Marshall (1890), *Principles of Economics* | 2, 37 | 2, 14 |
| the price system as information | Hayek (1945), "The Use of Knowledge in Society" | 1, 9 | 1, 9 |
| the double auction in the classroom | Chamberlin (1948); Smith (1962) | 1–2 | 1 |
| zero-intelligence traders | Gode and Sunder (1993) | 2 | 1–2 |
| general equilibrium and its welfare theorems | Arrow and Debreu (1954); Debreu (1959) | 9 | 8–9 |
| consumer surplus | Dupuit (1844) | 2, 10 | 2, 9–10 |

### Choice

| Model or result | Paper | Planned | Built |
|---|---|---|---|
| revealed preference | Samuelson (1938); Afriat (1967); Varian (1982) | 5 | 5–6 |
| expected utility | von Neumann and Morgenstern (1944) | 7 | 7, 11 |
| prospect theory | Kahneman and Tversky (1979) | 7, 45 | 7 |
| present bias | Laibson (1997) | 7, 45 | 7 |

### Firms

| Model or result | Paper | Planned | Built |
|---|---|---|---|
| why firms exist | Coase (1937), "The Nature of the Firm" | 1, 8 | 1, 8 |
| organizations and markets | Simon (1991) | 1 | 1 |
| incomplete contracts and ownership | Grossman and Hart (1986) | 8, 14 | 8, 14 |
| moral hazard and the principal | Holmström (1979) | 14 | 14 |

### Strategy

| Model or result | Paper | Planned | Built |
|---|---|---|---|
| equilibrium in games | Nash (1950, 1951) | 11 | 11 |
| oligopoly in quantities and prices | Cournot (1838); Bertrand (1883) | 12 | 6, 12 |
| demand estimation with differentiated products | Berry, Levinsohn and Pakes (1995) | 43 | · |

### Information and design

| Model or result | Paper | Planned | Built |
|---|---|---|---|
| lemons | Akerlof (1970) | 13 | 13 |
| signalling | Spence (1973) | 13 | · |
| screening in insurance | Rothschild and Stiglitz (1976) | 7, 13 | 7, 13 |
| second-price auctions | Vickrey (1961) | 16 | · |
| optimal auctions | Myerson (1981) | 16 | · |
| stable matching | Gale and Shapley (1962) | 17 | · |
| Bayesian persuasion | Kamenica and Gentzkow (2011) | 53 | · |
| incentives that crowd out | Gneezy and Rustichini (2000), "A Fine Is a Price" | 1, 14 | 1, 14 |

### Welfare and the state

| Model or result | Paper | Planned | Built |
|---|---|---|---|
| externalities and their tax | Pigou (1920) | 10, 15, 56 | 10, 15 |
| bargaining over externalities | Coase (1960) | 15 | 15 |
| public goods | Samuelson (1954) | 15 | · |
| governing the commons | Ostrom (1990) | 15 | 15 |
| the impossibility of social choice | Arrow (1951) | 18 | · |
| optimal income taxation | Mirrlees (1971); Saez (2001) | 14, 41 | 6, 14 |
| optimal commodity taxation | Ramsey (1927); Diamond and Mirrlees (1971) | 6, 10, 41 | · |

### Growth

| Model or result | Paper | Planned | Built |
|---|---|---|---|
| the Malthusian economy | Malthus (1798) | 19 | · |
| the long run in numbers | the Maddison Project (Bolt and van Zanden 2024) | 1 | 1, 3, 14 |
| the neoclassical growth model | Solow (1956); Ramsey (1928); Cass (1965) | 20 | · |
| endogenous growth | Romer (1990); Aghion and Howitt (1992) | 21 | · |
| misallocation | Hsieh and Klenow (2009) | 9, 21 | 9 |

### Macroeconomics

| Model or result | Paper | Planned | Built |
|---|---|---|---|
| national accounts | Kuznets (1934) | 3 | 2 |
| the General Theory and IS-LM | Keynes (1936); Hicks (1937) | 27 | · |
| the permanent income hypothesis | Friedman (1957); Hall (1978) | 22 | · |
| the Phillips curve and the natural rate | Phillips (1958); Friedman (1968); Phelps (1967) | 28 | · |
| the Lucas critique | Lucas (1976) | 4, 28, 54 | 4 |
| time inconsistency and rules | Kydland and Prescott (1977) | 28 | · |
| real business cycles | Kydland and Prescott (1982) | 29 | · |
| staggered prices | Calvo (1983) | 30 | · |
| the Taylor rule | Taylor (1993) | 30 | · |
| search and unemployment | Diamond (1982); Mortensen and Pissarides (1994) | 24 | · |
| heterogeneous agents | Bewley (1977); Huggett (1993); Aiyagari (1994) | 52, 56 | · |
| the equity premium puzzle | Mehra and Prescott (1985) | 7, 23 | 7 |

### Money and finance

| Model or result | Paper | Planned | Built |
|---|---|---|---|
| money as a medium of exchange | Kiyotaki and Wright (1989) | 25 | · |
| bank runs | Diamond and Dybvig (1983) | 26 | · |
| debt deflation and financial instability | Fisher (1933); Minsky (1986) | 33 | · |
| the financial accelerator | Bernanke, Gertler and Gilchrist (1999) | 33 | · |
| forecasting by professionals | the Survey of Professional Forecasters (Philadelphia Fed) | 1, 57 | 1 |

### The world economy

| Model or result | Paper | Planned | Built |
|---|---|---|---|
| optimum currency areas and the trilemma | Mundell (1961, 1963) | 34 | · |
| exchange-rate overshooting | Dornbusch (1976) | 34 | · |
| factor prices and trade | Stolper and Samuelson (1941) | 35 | · |
| trade with increasing returns | Krugman (1979, 1980) | 36 | · |
| heterogeneous firms in trade | Melitz (2003) | 36 | · |
| gravity | Anderson and van Wincoop (2003) | 36 | · |
| economic geography | Krugman (1991) | 37 | · |

### People

| Model or result | Paper | Planned | Built |
|---|---|---|---|
| human capital | Becker (1964); Mincer (1974) | 38 | 13 |
| the minimum wage | Card and Krueger (1994) | 4, 38 | 4 |
| skills, tasks and technology | Autor, Levy and Murnane (2003); Acemoglu and Autor (2011) | 39 | · |
| mobility and place | Chetty and others (2014) | 40, 42 | · |
| top incomes | Piketty and Saez (2003) | 40 | · |
| the economics of crime | Becker (1968) | 49 | · |

### Method

| Model or result | Paper | Planned | Built |
|---|---|---|---|
| positive economics | Friedman (1953) | 8 | 1, 8 |
| models as maps | Rodrik (2015), *Economics Rules* | 1, 67 | 1 |
| identification by instruments | Wright (1928); Haavelmo (1944) | 4 | 4 |
| the credibility of econometrics | Leamer (1983); LaLonde (1986) | 4 | 4 |
| vector autoregressions | Sims (1980) | 55 | · |
| dynamic discrete choice | Rust (1987) | 44, 54 | · |
| generalized method of moments | Hansen (1982) | 54 | · |
| machine learning for causal questions | Chernozhukov and others (2018); Athey and Imbens (2019) | 64 | · |
| publication bias in economics | Brodeur and others (2016) | 67 | · |

## 3. Every built part's reference card

**Part 1, *Who Feeds Paris?*.** Books: Adam Smith, *The Wealth of Nations* (1776), Book I, chs 1–3; David Ricardo, *Principles of Political Economy and Taxation* (1817), ch. 7; Frédéric Bastiat, *Economic Sophisms* (1845); The CORE Team, *The Economy*, units 1–2; N. Gregory Mankiw, *Principles of Economics*, chs 1–3; Robert Heilbroner, *The Worldly Philosophers*; Dani Rodrik, *Economics Rules* (2015). Papers: Hayek (1945), "The Use of Knowledge in Society", *AER* 35; Coase (1937), "The Nature of the Firm", *Economica* 4; Simon (1991), *JEP* 5(2); Chamberlin (1948), *JPE* 56; Smith (1962), *JPE* 70; Gode and Sunder (1993), *JPE* 101; Cliff (1997); Gneezy and Rustichini (2000), "A Fine Is a Price", *Journal of Legal Studies* 29; Friedman (1953), "The Methodology of Positive Economics"; Read (1958), "I, Pencil"; Bolt and van Zanden (2024), the Maddison Project Database 2023; Besley and Hennessy (2009).

**Part 2, *The Scissors*.** Books: Alfred Marshall, *Principles of Economics* (1890), Book V; Adam Smith, *The Wealth of Nations* (1776), Book I, ch. 4; Hal Varian, *Intermediate Microeconomics*, chs 1, 15–16; N. Gregory Mankiw, *Principles of Economics*, chs 4–8; Krugman and Wells, chs 3–5. Papers: Smith (1962), *JPE* 70; Gode and Sunder (1993), *JPE* 101; Cliff and Bruten (1997); Dupuit (1844); Whately (1832), Lecture IX; Havranek, Irsova and Janda (2012); Chetty, Looney and Kroft (2009), *AER* 99; Kopczuk, Marion, Muehlegger and Slemrod (2016); Diamond, McQuade and Qian (2019), *AER* 109; Calvano, Calzolari, Denicoló and Pastorello (2020), *AER* 110; Assad, Clark, Ershov and Xu (2024), *JPE* 132.

**Part 3, *The Measure*.** Books: Diane Coyle, *GDP: A Brief but Affectionate History* (2014); François Lequiller and Derek Blades, *Understanding National Accounts* (OECD, 2nd ed., 2014); N. Gregory Mankiw, *Macroeconomics*, ch. 2, "The Data of Macroeconomics"; Wassily Leontief, *Input-Output Economics* (2nd ed., 1986). Papers: Kuznets et al., *National Income, 1929–32* (1934); Petty, *Verbum Sapienti* (1665); Boskin et al. (1996); Lebow and Rudd (2003), *JEL* 41; Moulton (2018), Brookings; Deaton and Heston (2010), *AEJ: Macro* 2; Jones and Klenow (2016), *AER* 106; Nordhaus and Tobin (1972); Piketty, Saez and Zucman (2018), *QJE* 133; Corrado, Hulten and Sichel (2009); Henderson, Storeygard and Weil (2012), *AER* 102; Martinez (2022), *JPE* 130.

**Part 4, *The Evidence*.** Books: Joshua Angrist and Jörn-Steffen Pischke, *Mostly Harmless Econometrics* (2009) and *Mastering 'Metrics* (2014); James Stock and Mark Watson, *Introduction to Econometrics*, chs. 1–3, 12–13; Scott Cunningham, *Causal Inference: The Mixtape* (2021); Daron Acemoglu, David Laibson and John List, *Economics*, ch. 2. Papers: Working (1927), *QJE* 41; Wright (1928), Appendix B; Stock and Trebbi (2003), *JEP* 17; Haavelmo (1944); Leamer (1983), *AER* 73; LaLonde (1986), *AER* 76; Lucas (1976); Angrist (1990); Angrist and Krueger (1991); Card and Krueger (1994); Imbens and Angrist (1994); Bound, Jaeger and Baker (1995); Staiger and Stock (1997); Card (2001), *Econometrica* 69; Deaton, Imbens and Heckman (2010), *JEL* 48; Angrist and Pischke (2010), *JEP* 24; Crépon et al. (2013), *QJE* 128; Egger et al. (2022) and Muralidharan et al. (2023), *Econometrica*.

**Part 5, *What People Want*.** Books: Hal Varian, *Intermediate Microeconomics*, chs. 2–7; Andreu Mas-Colell, Michael Whinston and Jerry Green, *Microeconomic Theory*, chs. 1–3; David Kreps, *Microeconomic Foundations I*, chs. 1–4; Jehle and Reny, *Advanced Microeconomic Theory*, ch. 1; Christopher Chambers and Federico Echenique, *Revealed Preference Theory* (2016). Papers: Samuelson (1938), *Economica* 5; Houthakker (1950), *Economica* 17; Debreu (1954); Afriat (1967), *IER* 8; Varian (1982), *Econometrica* 50; Bronars (1987); Becker (1962), *JPE* 70; Harbaugh, Krause and Berry (2001); Andreoni and Miller (2002); Choi et al. (2007, 2014), *AER*; Saez (2010); Blundell, Browning and Crawford (2008); McFadden (1974); Kitamura and Stoye (2018); Chen, Liu, Shan and Zhong (2023), *PNAS*.

**Part 6, *Demand*.** Books: Hal Varian, *Intermediate Microeconomics*, chs. 6–10, 14; Andreu Mas-Colell, Michael Whinston and Jerry Green, *Microeconomic Theory*, chs. 2–3; Angus Deaton and John Muellbauer, *Economics and Consumer Behavior* (1980); Walter Nicholson and Christopher Snyder, *Microeconomic Theory*, chs. 5–6. Papers: Slutsky (1915); Hicks and Allen (1934), *Economica*; Hicks, *Value and Capital* (1939); Jensen and Miller (2008), *AER* 98(4); Stigler (1947); Rosen (1999), *JPE*; Roy (1947); Shephard (1953); Hurwicz and Uzawa (1971); Konüs (1924); Hicks (1940); Willig (1976), *AER*; Hausman (1981), *AER*; Hausman (1997), new goods; Stone (1954); Deaton and Muellbauer (1980), *AER*; Gorman (1953); Houthakker (1957); Hamilton (2001), *AER*; Costa (2001), *JPE*; Almås (2012), *AER*; Deaton (1989); Feenstra (1994); Jaravel (2019), *QJE*; Redding and Weinstein (2020); Jaravel and Lashkari (2024); Atkin et al. (2024).

**Part 7, *Time and Risk*.** Books: Hal Varian, *Intermediate Microeconomics*, chs. 10–13; Andreu Mas-Colell, Michael Whinston and Jerry Green, *Microeconomic Theory*, ch. 6; David Kreps, *Microeconomic Foundations I*, chs. 5–6; Christian Gollier, *The Economics of Risk and Time* (2001). Papers: Bernoulli (1738); Fisher, *The Theory of Interest* (1930); Samuelson (1937); Koopmans (1960); von Neumann and Morgenstern (1944); Savage (1954); Allais (1953); Ellsberg (1961); Pratt (1964); Arrow (1965); Mossin (1968); Merton (1969); Rothschild and Stiglitz (1970); Kahneman and Tversky (1979); Machina (1982); Gilboa and Schmeidler (1989); Rabin (2000); Kreps and Porteus (1978); Epstein and Zin (1989); Mehra and Prescott (1985); Weil (1989); Hall (1988); Strotz (1955–56); Laibson (1997); Holt and Laury (2002); Barsky et al. (1997); Hayden and Platt (2009); Hansen and Sargent, *Robustness* (2008); Manski (2004); Madrian and Shea (2001); Thaler and Benartzi (2004).

**Part 8, *The Firm*.** Books: Hal Varian, *Intermediate Microeconomics*, chs. 19–24; Andreu Mas-Colell, Michael Whinston and Jerry Green, *Microeconomic Theory*, ch. 5; Oliver Williamson, *The Economic Institutions of Capitalism* (1985); Oliver Hart, *Firms, Contracts, and Financial Structure* (1995). Papers: Cobb and Douglas (1928), *AER*; Douglas (1976), *JPE*; Felipe and Adams (2005); Arrow, Chenery, Minhas and Solow (1961); Chenery (1949); Samuelson's Le Chatelier principle; Hall and Hitch (1939); Alchian (1950); Friedman (1953); Coase (1937), *Economica*; Williamson (1975, 1985); Klein, Crawford and Alchian (1978); Coase (2000), Klein (2000), Freeland (2000), Casadesus-Masanell and Spulber (2000), *JLE*; Grossman and Hart (1986); Hart and Moore (1990), *JPE*; Gollin (2002); Karabarbounis and Neiman (2014); Haskel and Westlake (2018); Brynjolfsson, Li and Raymond (2025); Shahidi et al. (2025).

**Part 9, *The Invisible Hand, Proved*.** Books: Andreu Mas-Colell, Michael Whinston and Jerry Green, *Microeconomic Theory*, chs. 15–19; Gerard Debreu, *Theory of Value* (1959); David Kreps, *Microeconomic Foundations I* (2013); Jehle and Reny, *Advanced Microeconomic Theory*, ch. 5; Herbert Scarf, *The Computation of Economic Equilibria* (1973). Papers: Radford (1945), *Economica*; Edgeworth, *Mathematical Psychics* (1881); Walras (1874); Arrow and Debreu (1954); McKenzie (1954); Debreu and Scarf (1963); Aumann (1964); Arrow, Block and Hurwicz (1959); Scarf (1960, 1967); Anderson, Plott, Shimomura and Granat (2004); Sonnenschein (1973); Mantel (1974); Debreu (1974); Kirman (1992); Brown and Matzkin (1996); Arrow (1953); Mises (1920); Lange (1936–37); Hayek (1945); Kantorovich (1939); Hsieh and Klenow (2009); Bils, Klenow and Ruane (2021); Kehoe (2005, 2014); Papadimitriou (1994); Daskalakis, Goldberg and Papadimitriou (2009); Shapley and Scarf (1974); Budish (2011).

**Part 10, *The Price Maker*.** Books: Jean Tirole, *The Theory of Industrial Organization* (1988), chs. 1–4; Paul Belleflamme and Martin Peitz, *Industrial Organization: Markets and Strategies* (2015); Hal Varian, *Intermediate Microeconomics*: monopoly, monopoly behaviour, factor markets; Kalyan Talluri and Garrett van Ryzin, *The Theory and Practice of Revenue Management* (2004). Papers: Dupuit (1844, 1849); Pigou (1920); Robinson (1933); Lerner (1934); Harberger (1954); Posner (1975); Schmalensee (1981); Varian (1985); Mussa and Rosen (1978); Maskin and Riley (1984); Deneckere and McAfee (1996); Oi (1971); Stigler (1963); Adams and Yellen (1976); McAfee, McMillan and Whinston (1989); Coase (1972); Stokey (1981); Bulow (1982, 1986); Gul, Sonnenschein and Wilson (1986); Ramsey (1927); Boiteux (1956); Averch and Johnson (1962); Littlechild (1983); Littlewood (1972); Nakamura and Zerom (2010); Weyl and Fabinger (2013); Hall (1988); De Loecker and Warzynski (2012); De Loecker, Eeckhout and Unger (2020); Traina (2018); Dubé and Misra (2023); Calvano et al. (2020); Assad et al. (2024).

**Part 11, *Games*.** Books: Martin Osborne, *An Introduction to Game Theory* (2004); Osborne and Rubinstein, *A Course in Game Theory* (1994); Drew Fudenberg and Jean Tirole, *Game Theory* (1991), chs. 1–5; Robert Gibbons, *A Primer in Game Theory* (1992); Thomas Schelling, *The Strategy of Conflict* (1960); Robert Axelrod, *The Evolution of Cooperation* (1984); Colin Camerer, *Behavioral Game Theory* (2003); Martin Nowak, *Evolutionary Dynamics* (2006). Papers: von Neumann (1928); Nash (1950, 1951); Flood (1952); Selten (1965, 1978); Harsanyi (1967–68); Aumann (1974); Maynard Smith and Price (1973); Brown (1951); Robinson (1951); Shapley (1964); Friedman (1971); Rubinstein (1982); Kreps, Milgrom, Roberts and Wilson (1982); Fudenberg and Maskin (1986); Axelrod (1980); Nowak and Sigmund (1993); Rosenthal (1981); McKelvey and Palfrey (1992); Güth, Schmittberger and Schwarze (1982); Henrich et al. (2001); Nagel (1995); Stahl and Wilson (1994); Camerer, Ho and Chong (2004); Chiappori, Levitt and Groseclose (2002); Palacios-Huerta (2003); Walker and Wooders (2001); Hart and Mas-Colell (2000); Erev and Roth (1998); Bowling et al. (2015); Brown and Sandholm (2018, 2019).

**Part 12, *Competition among the Few*.** Books: Jean Tirole, *The Theory of Industrial Organization* (1988), chs. 5–9; Luís Cabral, *Introduction to Industrial Organization* (2nd ed., 2017); Dennis Carlton and Jeffrey Perloff, *Modern Industrial Organization*; Belleflamme and Peitz, *Industrial Organization: Markets and Strategies*; Massimo Motta, *Competition Policy: Theory and Practice* (2004); Whinston, *Lectures on Antitrust Economics* (2006); John Connor, *Global Price Fixing* (2nd ed., 2008); Kurt Eichenwald, *The Informant* (2000). Papers: Cournot (1838); Bertrand (1883); Edgeworth (1897); Hotelling (1929); Chamberlin (1933); Robinson (1933); von Stackelberg (1934); Stigler (1964); Williamson (1968); Friedman (1971); Dixit and Stiglitz (1977); Salop (1979); d'Aspremont, Gabszewicz and Thisse (1979); Dixit (1980); Kreps and Scheinkman (1983); Porter (1983); Salant, Switzer and Reynolds (1983); Green and Porter (1984); Fudenberg and Tirole (1984); Farrell and Shapiro (1990); Cowling and Waterson (1976); McGee (1958); Baumol, Panzar and Willig (1982); Milgrom and Roberts (1982); Kreps and Wilson (1982); Borenstein, Cameron and Gilbert (1997); Connor (1998, 2014); Levenstein and Suslow (2006); Boyer and Kotchoni (2015); O'Brien and Salop (2000); Azar, Schmalz and Tecu (2018); Dennis, Gerardi and Schenone (2022); Calvano et al. (2020); Assad et al. (2024).

**Part 13, *Lemons and Signals*.** Books: Patrick Bolton and Mathias Dewatripont, *Contract Theory* (2005), chs. 2–3; Mas-Colell, Whinston and Green, ch. 13; Jean-Jacques Laffont and David Martimort, *The Theory of Incentives* (2002); Salanié, *The Economics of Contracts*; Liran Einav, Amy Finkelstein and Ray Fisman, *Risky Business* (2023); Einav and Finkelstein, JEP 25(1) (2011); Bryan Caplan, *The Case against Education* (2018). Papers: Akerlof (1970); Spence (1973); Rothschild and Stiglitz (1976); Riley (1979); Stiglitz and Weiss (1981); Cho and Kreps (1987); Hungerford and Solon (1987); Tyler, Murnane and Willett (2000); Cutler and Reber (1998); Cutler and Zeckhauser (1998); Chiappori and Salanié (2000); Finkelstein and Poterba (2004); Finkelstein and McGarry (2006); Cabral and Hortaçsu (2010); Einav, Finkelstein and Cullen (2010); Handel (2013); Einav, Finkelstein, Ryan, Schrimpf and Cullen (2013); Hackmann, Kolstad and Kowalski (2015); Angrist and Krueger (1991).

**Part 14, *Incentives*.** Books: Patrick Bolton and Mathias Dewatripont, *Contract Theory* (2005), chs. 4, 6, 8, 11; Jean-Jacques Laffont and David Martimort, *The Theory of Incentives* (2002); Salanié, *The Economics of Contracts*; Paul Milgrom and John Roberts, *Economics, Organization and Management* (1992); Robert Gibbons and John Roberts, eds., *The Handbook of Organizational Economics* (2013). Papers: Ross (1973); Holmström (1979, 1982); Mirrlees (1975); Grossman and Hart (1983); Holmström and Milgrom (1987, 1991); Lazear and Rosen (1981); Rosen (1986); Weitzman (1980); Shapiro and Stiglitz (1984); Akerlof (1982); Raff and Summers (1987); Stiglitz (1974); Lazear (2000); Shearer (2004); Bandiera, Barankay and Rasul (2005); Jacob and Levitt (2003); Lin (1992); Banerjee, Gertler and Ghatak (2002); Gneezy and Rustichini (2000); Frey and Oberholzer-Gee (1997); Baker, Gibbons and Murphy (2002); Levin (2003); Hadfield-Menell and Hadfield (2019); Gao, Schulman and Hilton (2023).

**Part 15, *Spillovers*.** Books: Jonathan Gruber, *Public Finance and Public Policy*, chs. 5–9; Mas-Colell, Whinston and Green, *Microeconomic Theory* (1995), ch. 11; Elinor Ostrom, *Governing the Commons* (1990); Tom Tietenberg and Lynne Lewis, *Environmental and Natural Resource Economics*. Papers: Pigou (1920); Meade (1952); Coase (1959, 1960, 1974); Samuelson (1954); Gordon (1954); Hardin (1968); Dales (1968); Montgomery (1972); Cheung (1973); Weitzman (1974); Vickrey (1969); Arnott, de Palma and Lindsey (1990); Duranton and Turner (2011); Fehr and Gächter (2000); Fischbacher, Gächter and Fehr (2001); Herrmann, Thöni and Gächter (2008); Rohlfs (1974); Katz and Shapiro (1985); David (1985); Arthur (1989); Jaffe, Trajtenberg and Henderson (1993); Schmalensee and Stavins (2013); Chay and Greenstone (2003); Currie and Walker (2011); Deryugina et al. (2019).

## 4. What the series leaves out

- **Accounting and corporate finance.** The firm's books and its capital structure appear only where an economic argument needs them (the T-accounts of money and banks in Parts 25 and 26); there is no course in valuation or financial reporting.
- **Derivatives and financial engineering.** Asset pricing is taught as economics (Part 23: the stochastic discount factor and its puzzles); option pricing and the mathematics of hedging belong to *Quant, Built*.
- **The history of economic thought as a field.** Each idea arrives with its people, its year and its dead ends, but the series does not survey schools for their own sake. Marxian, Austrian, post-Keynesian, institutionalist and complexity arguments appear where they bear on a part's question, with their best case (SYLLABUS, section 1).
- **Sector fields.** Agricultural, health, transport and energy economics are drawn on for examples (health insurance in Part 42, carbon in Part 48) but have no parts of their own.
- **Country studies.** The Data Room's countries are evidence, not subjects: no part is a course on one economy.
