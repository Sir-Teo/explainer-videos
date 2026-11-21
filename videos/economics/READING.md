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
part's README, under *Sources*. Built so far: Parts 1–63.

## 1. The textbook spine

### Principles

| Short name | Book | Planned | Built |
|---|---|---|---|
| Mankiw | N. G. Mankiw, *Principles of Economics* (10th ed., 2024) | 1–2 | 1–3, 20, 22, 28, 30, 32 |
| Krugman–Wells | P. Krugman and R. Wells, *Economics* (6th ed., 2021) | 2 | 2 |
| Acemoglu–Laibson–List | D. Acemoglu, D. Laibson and J. List, *Economics* (3rd ed., 2022) | 4 | 4 |
| CORE | The CORE Team, *The Economy* (2017; 2.0, 2023) | 1 | 1, 9, 30, 46 |
| Heilbroner | R. Heilbroner, *The Worldly Philosophers* (7th ed., 1999) | 1 | 1 |

### The major

| Short name | Book | Planned | Built |
|---|---|---|---|
| Varian | H. Varian, *Intermediate Microeconomics* (9th ed., 2014) | 2, 5–8, 10 | 2, 5–8, 10, 16, 61 |
| Nicholson–Snyder | W. Nicholson and C. Snyder, *Microeconomic Theory* (13th ed., 2021) | 5–6 | 5–6, 8 |
| Jones | C. I. Jones, *Macroeconomics* (6th ed., 2023) | 20 | · |
| Blanchard | O. Blanchard, *Macroeconomics* (8th ed., 2021) | 27, 32 | 20, 24, 27–28, 32, 39 |
| Stock–Watson | J. Stock and M. Watson, *Introduction to Econometrics* (4th ed., 2019) | 4 | 4, 45, 49, 55, 57 |
| Angrist–Pischke | J. Angrist and J.-S. Pischke, *Mostly Harmless Econometrics* (2009) | 4, 50, 67 | 4, 50 |
| Osborne | M. Osborne, *An Introduction to Game Theory* (2004) | 11 | 11 |
| Krugman–Obstfeld–Melitz | P. Krugman, M. Obstfeld and M. Melitz, *International Economics* (12th ed., 2022) | 34–35 | 34–36 |
| Mishkin | F. Mishkin, *The Economics of Money, Banking, and Financial Markets* (13th ed., 2022) | 26 | 31, 57 |
| Cabral | L. Cabral, *Introduction to Industrial Organization* (2nd ed., 2017) | 12–13 | 12–13 |
| Borjas | G. Borjas, *Labor Economics* (8th ed., 2020) | 38 | 38 |
| Gruber | J. Gruber, *Public Finance and Public Policy* (7th ed., 2022) | 15, 41–42, 50 | 7, 15, 41–42, 49–51, 58 |
| Ray | D. Ray, *Development Economics* (1998) | 46 | 46 |
| Weil | D. Weil, *Economic Growth* (3rd ed., 2013) | 7, 19 | 3, 7, 19–21, 23, 57 |

### Graduate micro

| Short name | Book | Planned | Built |
|---|---|---|---|
| MWG | A. Mas-Colell, M. Whinston and J. Green, *Microeconomic Theory* (1995) | 5–9, 11, 13, 15, 18, 56 | 5–11, 13, 15–16, 18, 56 |
| Kreps | D. Kreps, *Microeconomic Foundations I* (2013) | 5, 7, 9, 11, 56 | 5, 7, 9, 11–13, 53, 56 |
| Jehle–Reny | G. Jehle and P. Reny, *Advanced Microeconomic Theory* (3rd ed., 2011) | 5, 9 | 5–6, 9 |
| Fudenberg–Tirole | D. Fudenberg and J. Tirole, *Game Theory* (1991) | 11–12, 53 | 11–12, 53 |
| Osborne–Rubinstein | M. Osborne and A. Rubinstein, *A Course in Game Theory* (1994) | 11 | 11 |
| Bolton–Dewatripont | P. Bolton and M. Dewatripont, *Contract Theory* (2005) | 13–14 | 13–14 |
| Krishna | V. Krishna, *Auction Theory* (2nd ed., 2010) | 16 | 16 |
| Milgrom | P. Milgrom, *Putting Auction Theory to Work* (2004) | 16 | 16 |
| Roth–Sotomayor | A. Roth and M. Sotomayor, *Two-Sided Matching* (1990) | 17 | · |
| Börgers | T. Börgers, *An Introduction to the Theory of Mechanism Design* (2015) | 17 | 17 |
| Tirole IO | J. Tirole, *The Theory of Industrial Organization* (1988) | 10–12, 53 | 10, 12 |

### Graduate macro

| Short name | Book | Planned | Built |
|---|---|---|---|
| Romer | D. Romer, *Advanced Macroeconomics* (5th ed., 2019) | 20, 22–23, 28–29, 56 | · |
| Ljungqvist–Sargent | L. Ljungqvist and T. Sargent, *Recursive Macroeconomic Theory* (4th ed., 2018) | 29, 52, 56 | 22, 24, 29, 52, 56 |
| SLP | N. Stokey, R. Lucas and E. Prescott, *Recursive Methods in Economic Dynamics* (1989) | 29, 51 | 29 |
| Acemoglu | D. Acemoglu, *Introduction to Modern Economic Growth* (2009) | 20–21 | · |
| Galí | J. Galí, *Monetary Policy, Inflation, and the Business Cycle* (2nd ed., 2015) | 30, 56 | 29–30, 56 |
| Woodford | M. Woodford, *Interest and Prices* (2003) | 30 | 30, 32 |
| Walsh | C. Walsh, *Monetary Theory and Policy* (4th ed., 2017) | 25 | 25, 30–31 |
| Obstfeld–Rogoff | M. Obstfeld and K. Rogoff, *Foundations of International Macroeconomics* (1996) | 34 | 34 |
| Pissarides | C. Pissarides, *Equilibrium Unemployment Theory* (2nd ed., 2000) | 24 | 24 |
| Cochrane | J. Cochrane, *Asset Pricing* (rev. ed., 2005) | 23 | · |
| Freixas–Rochet | X. Freixas and J.-C. Rochet, *Microeconomics of Banking* (2nd ed., 2008) | 26 | 26 |

### Econometrics and computation

| Short name | Book | Planned | Built |
|---|---|---|---|
| Hayashi | F. Hayashi, *Econometrics* (2000) | 54, 56 | 23, 54, 56 |
| Wooldridge | J. Wooldridge, *Econometric Analysis of Cross Section and Panel Data* (2nd ed., 2010) | 54 | 38–39 |
| Hansen | B. Hansen, *Econometrics* (2022) | 54 | · |
| Hamilton | J. Hamilton, *Time Series Analysis* (1994) | 55 | 6 |
| Kilian–Lütkepohl | L. Kilian and H. Lütkepohl, *Structural Vector Autoregressive Analysis* (2017) | 55 | 55 |
| Train | K. Train, *Discrete Choice Methods with Simulation* (2nd ed., 2009) | 43, 54 | 43, 54 |
| Judd | K. Judd, *Numerical Methods in Economics* (1998) | 51 | 29, 41, 51 |
| QuantEcon | T. Sargent and J. Stachurski, *Quantitative Economics* (QuantEcon lectures) | 51 | 51 |

### The fields

| Short name | Book | Planned | Built |
|---|---|---|---|
| Feenstra | R. Feenstra, *Advanced International Trade* (2nd ed., 2016) | 6, 35–36 | 6, 8, 20, 35–36 |
| Cahuc–Carcillo–Zylberberg | P. Cahuc, S. Carcillo and A. Zylberberg, *Labor Economics* (2nd ed., 2014) | 24, 38 | 24, 38 |
| Atkinson–Stiglitz | A. Atkinson and J. Stiglitz, *Lectures on Public Economics* (1980; 2015) | 41 | 6, 41 |
| Salanié | B. Salanie, *The Economics of Taxation* (2nd ed., 2011) | 41 | 13–14, 41 |
| Banerjee–Duflo | A. Banerjee and E. Duflo, *Poor Economics* (2011) | 46 | 46 |
| Persson–Tabellini | T. Persson and G. Tabellini, *Political Economics* (2000) | 47 | · |
| Dhami | S. Dhami, *The Foundations of Behavioral Economic Analysis* (2016) | 45 | 45 |
| Fujita–Krugman–Venables | M. Fujita, P. Krugman and A. Venables, *The Spatial Economy* (1999) | 37 | 37 |
| Nordhaus | W. Nordhaus, *A Question of Balance* (2008) | 48 | 48 |
| Jackson | M. Jackson, *Social and Economic Networks* (2008) | 63 | · |

### Practice

| Short name | Book | Planned | Built |
|---|---|---|---|
| Blinder | A. Blinder, *Central Banking in Theory and Practice* (1998) | 31 | 30–31, 39, 60 |
| Boardman | A. Boardman and others, *Cost-Benefit Analysis* (5th ed., 2018) | 50, 58 | 50, 58 |
| Davis–Garcés | P. Davis and E. Garces, *Quantitative Techniques for Competition and Antitrust Analysis* (2010) | 59 | 59 |
| Talluri–van Ryzin | K. Talluri and G. van Ryzin, *The Theory and Practice of Revenue Management* (2004) | 10, 60 | 10, 60 |
| Kohavi–Tang–Xu | R. Kohavi, D. Tang and Y. Xu, *Trustworthy Online Controlled Experiments* (2020) | 61 | 61 |
| Lazear–Gibbs | E. Lazear and M. Gibbs, *Personnel Economics in Practice* (3rd ed., 2014) | 62 | 62 |

## 2. Papers and models, and where they are taught

### Markets and prices

| Model or result | Paper | Planned | Built |
|---|---|---|---|
| the division of labour | Smith (1776), *The Wealth of Nations* | 1 | 1–2, 19, 21, 39 |
| comparative advantage | Ricardo (1817), *Principles*, ch. 7 | 2, 8, 35–36 | 1–2, 8, 19, 22, 25, 33–36, 52 |
| supply and demand, the scissors | Marshall (1890), *Principles of Economics* | 2, 37 | 2, 14, 37 |
| the price system as information | Hayek (1945), "The Use of Knowledge in Society" | 1, 9 | 1, 9 |
| the double auction in the classroom | Chamberlin (1948); Smith (1962) | 1–2 | 1 |
| zero-intelligence traders | Gode and Sunder (1993) | 2 | 1–2 |
| general equilibrium and its welfare theorems | Arrow and Debreu (1954); Debreu (1959) | 9 | 8–9 |
| consumer surplus | Dupuit (1844) | 2, 10 | 2, 9–10, 18, 41, 58 |

### Choice

| Model or result | Paper | Planned | Built |
|---|---|---|---|
| revealed preference | Samuelson (1938); Afriat (1967); Varian (1982) | 5 | 5–6 |
| expected utility | von Neumann and Morgenstern (1944) | 7 | 7, 11 |
| prospect theory | Kahneman and Tversky (1979) | 7, 45 | 7, 45 |
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
| equilibrium in games | Nash (1950, 1951) | 11 | 11, 53 |
| oligopoly in quantities and prices | Cournot (1838); Bertrand (1883) | 12 | 6, 12, 43, 53 |
| demand estimation with differentiated products | Berry, Levinsohn and Pakes (1995) | 43 | 35, 42–43 |

### Information and design

| Model or result | Paper | Planned | Built |
|---|---|---|---|
| lemons | Akerlof (1970) | 13 | 13 |
| signalling | Spence (1973) | 13 | · |
| screening in insurance | Rothschild and Stiglitz (1976) | 7, 13 | 7, 13, 42 |
| second-price auctions | Vickrey (1961) | 16 | 16–17, 56 |
| optimal auctions | Myerson (1981) | 16 | 16, 56 |
| stable matching | Gale and Shapley (1962) | 17 | 17 |
| Bayesian persuasion | Kamenica and Gentzkow (2011) | 53 | 52–53 |
| incentives that crowd out | Gneezy and Rustichini (2000), "A Fine Is a Price" | 1, 14 | 1, 14, 45, 49 |

### Welfare and the state

| Model or result | Paper | Planned | Built |
|---|---|---|---|
| externalities and their tax | Pigou (1920) | 10, 15, 56 | 10, 15, 41, 56 |
| bargaining over externalities | Coase (1960) | 15 | 15, 56 |
| public goods | Samuelson (1954) | 15 | · |
| governing the commons | Ostrom (1990) | 15 | 15 |
| the impossibility of social choice | Arrow (1951) | 18 | · |
| optimal income taxation | Mirrlees (1971); Saez (2001) | 14, 41 | 6, 14, 16, 41 |
| optimal commodity taxation | Ramsey (1927); Diamond and Mirrlees (1971) | 6, 10, 41 | · |

### Growth

| Model or result | Paper | Planned | Built |
|---|---|---|---|
| the Malthusian economy | Malthus (1798) | 19 | 18–19 |
| the long run in numbers | the Maddison Project (Bolt and van Zanden 2024) | 1 | 1, 3, 14, 19–20 |
| the neoclassical growth model | Solow (1956); Ramsey (1928); Cass (1965) | 20 | 20 |
| endogenous growth | Romer (1990); Aghion and Howitt (1992) | 21 | · |
| misallocation | Hsieh and Klenow (2009) | 9, 21 | 9, 21 |

### Macroeconomics

| Model or result | Paper | Planned | Built |
|---|---|---|---|
| national accounts | Kuznets (1934) | 3 | 2 |
| the General Theory and IS-LM | Keynes (1936); Hicks (1937) | 27 | · |
| the permanent income hypothesis | Friedman (1957); Hall (1978) | 22 | 22 |
| the Phillips curve and the natural rate | Phillips (1958); Friedman (1968); Phelps (1967) | 28 | · |
| the Lucas critique | Lucas (1976) | 4, 28, 54 | 4, 28, 54, 57 |
| time inconsistency and rules | Kydland and Prescott (1977) | 28 | 28, 56 |
| real business cycles | Kydland and Prescott (1982) | 29 | 54 |
| staggered prices | Calvo (1983) | 30 | 30 |
| the Taylor rule | Taylor (1993) | 30 | · |
| search and unemployment | Diamond (1982); Mortensen and Pissarides (1994) | 24 | 24 |
| heterogeneous agents | Bewley (1977); Huggett (1993); Aiyagari (1994) | 52, 56 | 52, 56 |
| the equity premium puzzle | Mehra and Prescott (1985) | 7, 23 | 7, 22–23 |

### Money and finance

| Model or result | Paper | Planned | Built |
|---|---|---|---|
| money as a medium of exchange | Kiyotaki and Wright (1989) | 25 | 25 |
| bank runs | Diamond and Dybvig (1983) | 26 | 26 |
| debt deflation and financial instability | Fisher (1933); Minsky (1986) | 33 | 33 |
| the financial accelerator | Bernanke, Gertler and Gilchrist (1999) | 33 | 33 |
| forecasting by professionals | the Survey of Professional Forecasters (Philadelphia Fed) | 1, 57 | 1, 31, 55, 57 |

### The world economy

| Model or result | Paper | Planned | Built |
|---|---|---|---|
| optimum currency areas and the trilemma | Mundell (1961, 1963) | 34 | 34 |
| exchange-rate overshooting | Dornbusch (1976) | 34 | · |
| factor prices and trade | Stolper and Samuelson (1941) | 35 | 35 |
| trade with increasing returns | Krugman (1979, 1980) | 36 | · |
| heterogeneous firms in trade | Melitz (2003) | 36 | · |
| gravity | Anderson and van Wincoop (2003) | 36 | 36 |
| economic geography | Krugman (1991) | 37 | · |

### People

| Model or result | Paper | Planned | Built |
|---|---|---|---|
| human capital | Becker (1964); Mincer (1974) | 38 | 13, 38 |
| the minimum wage | Card and Krueger (1994) | 4, 38 | 4, 38 |
| skills, tasks and technology | Autor, Levy and Murnane (2003); Acemoglu and Autor (2011) | 39 | 39 |
| mobility and place | Chetty and others (2014) | 40, 42 | · |
| top incomes | Piketty and Saez (2003) | 40 | 40–41 |
| the economics of crime | Becker (1968) | 49 | 49 |

### Method

| Model or result | Paper | Planned | Built |
|---|---|---|---|
| positive economics | Friedman (1953) | 8 | 1, 8 |
| models as maps | Rodrik (2015), *Economics Rules* | 1, 67 | 1 |
| identification by instruments | Wright (1928); Haavelmo (1944) | 4 | 4 |
| the credibility of econometrics | Leamer (1983); LaLonde (1986) | 4 | 4 |
| vector autoregressions | Sims (1980) | 55 | 55 |
| dynamic discrete choice | Rust (1987) | 44, 54 | 54 |
| generalized method of moments | Hansen (1982) | 54 | 54, 56 |
| machine learning for causal questions | Chernozhukov and others (2018); Athey and Imbens (2019) | 64 | 21 |
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

**Part 16, *Auctions*.** Books: Vijay Krishna, *Auction Theory* (2nd ed., 2010); Paul Klemperer, *Auctions: Theory and Practice* (2004); Paul Milgrom, *Putting Auction Theory to Work* (2004); John Kagel and Dan Levin, *Common Value Auctions and the Winner's Curse* (2002). Papers: Vickrey (1961); Myerson (1981); Riley and Samuelson (1981); Milgrom and Weber (1982); Capen, Clapp and Campbell (1971); Bazerman and Samuelson (1983); Kagel, Harstad and Levin (1987); Cox, Smith and Walker (1988); Bulow and Klemperer (1996); Maskin and Riley (2000); Guerre, Perrigne and Vuong (2000); Cramton and Schwartz (2000); Binmore and Klemperer (2002); Klemperer (2002a, 2002b); Edelman, Ostrovsky and Schwarz (2007); Varian (2007); Ostrovsky and Schwarz (2009); Garbade and Ingber (2005); Akbarpour and Li (2020); Milgrom and Segal (2020).

**Part 17, *Markets by Design*.** Books: Alvin E. Roth, *Who Gets What and Why* (2015); Alvin E. Roth and Marilda Sotomayor, *Two-Sided Matching* (1990); Tilman Börgers, *An Introduction to the Theory of Mechanism Design* (2015); Nisan, Roughgarden, Tardos and Vazirani, *Algorithmic Game Theory* (2007), chs. 9–10. Papers: Gale and Shapley (1962); Shapley and Shubik (1971); Shapley and Scarf (1974); Vickrey (1961); Clarke (1971); Groves (1973); Green and Laffont (1977); Myerson (1979); Myerson and Satterthwaite (1983); Chatterjee and Samuelson (1983); Dubins and Freedman (1981); Roth (1982, 1984, 1991, 2002, 2007, 2008); Roth and Peranson (1999); Kagel and Roth (2000); Abdulkadiroğlu and Sönmez (2003); Abdulkadiroğlu, Pathak and Roth (2005); Chen and Kesten (2017); Roth, Sönmez and Ünver (2004); Rees et al. (2009); Kojima and Pathak (2009); Azevedo and Leshno (2016); Abdulkadiroğlu, Angrist and Pathak (2014); Abdulkadiroğlu, Angrist, Narita and Pathak (2017); Bansak et al. (2018).

**Part 18, *Social Choice and Welfare*.** Books: Kenneth J. Arrow, *Social Choice and Individual Values* (1951; 3rd ed. 2012); Amartya Sen, *Collective Choice and Social Welfare* (1970; expanded ed. 2017); Mas-Colell, Whinston and Green, *Microeconomic Theory* (1995), chs. 21–22; Matthew Adler, *Measuring Social Welfare* (2019). Papers: Condorcet (1785); Black (1948); May (1952); Downs (1957); McKelvey (1976); Gibbard (1973); Satterthwaite (1975); Duverger (1951); Riker (1982); Robbins (1932); Hammond (1976); d'Aspremont and Gevers (1977); Geanakoplos (2005); Harsanyi (1953, 1955, 1975); Rawls (1971); Atkinson (1970); Okun (1975); Kaldor (1939); Hicks (1939); Scitovsky (1941); Sen (1970); Kaplow and Shavell (1994); Schelling (1968); Thaler and Rosen (1976); Ashenfelter and Greenstone (2004); Ravallion (2012); Bernheim and Rangel (2009); Lalley and Weyl (2018); Conitzer et al. (2024).

**Part 19, *The Great Escape*.** Books: Gregory Clark, *A Farewell to Alms* (2007); Robert C. Allen, *The British Industrial Revolution in Global Perspective* (2009); Joel Mokyr, *A Culture of Growth* (2016); Oded Galor, *Unified Growth Theory* (2011); Kenneth Pomeranz, *The Great Divergence* (2000). Papers: Malthus (1798); Ricardo (1817); Ashraf and Galor (2011, 2013); Broadberry, Campbell, Klein, Overton and van Leeuwen (2015); Humphries and Weisdorf (2019); Voigtländer and Voth (2013); North and Weingast (1989); Clark (1996); Humphries (2013); Kelly, Mokyr and Ó Gráda (2014); Broadberry, Guan and Li (2018); Crafts and Harley (1992); Crafts (2004); Allen (2009); Voth (2000); de Vries (1994); Becker and Lewis (1973); Kremer (1993); Galor and Weil (2000); Comin, Easterly and Gong (2010); Spolaore and Wacziarg (2009); Kelly (2019); Ehrlich (1968).

**Part 20, *Growth I: Capital*.** Books: Charles I. Jones and Dietrich Vollrath, *Introduction to Economic Growth* (3rd ed., 2013); Daron Acemoglu, *Introduction to Modern Economic Growth* (2009), chs. 2–3 and 8; David Romer, *Advanced Macroeconomics* (5th ed., 2019), chs. 1–2; William Easterly, *The Elusive Quest for Growth* (2001). Papers: Harrod (1939); Domar (1946); Solow (1956, 1957); Swan (1956); Kaldor (1961); Phelps (1961); Ramsey (1928); Cass (1965); Koopmans (1965); Abel, Mankiw, Summers and Zeckhauser (1989); Barro (1991); Mankiw, Romer and Weil (1992); Islam (1995); Quah (1996); Pritchett (1997); Krugman (1994); Young (1995); Hsieh (2002); Hall and Jones (1999); Caselli (2005); Lucas (1990); Song, Storesletten and Zilibotti (2011); Easterly (1999); Blanchard (2019); Fernald (2015); Syverson (2017); Kremer, Willis and You (2022); Acemoglu and Molina (2022); Feenstra, Inklaar and Timmer, the Penn World Table (2015; version 11.0, 2025).

**Part 21, *Growth II: Ideas and Institutions*.** Books: Charles I. Jones and Dietrich Vollrath, *Introduction to Economic Growth* (3rd ed., 2013), chs. 4–6; Daron Acemoglu, *Introduction to Modern Economic Growth* (2009), chs. 13–15; Philippe Aghion and Peter Howitt, *The Economics of Growth* (2009); David Warsh, *Knowledge and the Wealth of Nations* (2006); Acemoglu and Robinson, *Why Nations Fail* (2012). Papers: Nordhaus (1996); Arrow (1962); Romer (1986, 1990); Lucas (1988); Aghion and Howitt (1992); Jones (1995, 2022); Bloom, Jones, Van Reenen and Webb (2020); Comin and Hobijn (2010); Basu and Weil (1998); Hsieh and Klenow (2009); Bils, Klenow and Ruane (2021); Acemoglu, Johnson and Robinson (2001, 2002); Albouy (2012); Dell (2010); Rodrik et al. (2004); Alsan (2015); Nunn and Wantchekon (2011); Acemoglu (2002); Katz and Murphy (1992); Moser (2005); Williams (2013); Jones and Williams (1998); Bloom, Schankerman and Van Reenen (2013); Dechezleprêtre et al. (2023); Bloom, Van Reenen and Williams (2019); Aghion, Jones and Jones (2019).

**Part 22, *Consumption and Saving*.** Books: Angus Deaton, *Understanding Consumption* (1992); David Romer, *Advanced Macroeconomics* (5th ed., 2019), chs. 2 and 8; Lars Ljungqvist and Thomas Sargent, *Recursive Macroeconomic Theory* (4th ed., 2018), chs. 17–18; Milton Friedman, *A Theory of the Consumption Function* (1957). Papers: Modigliani and Brumberg (1954); Hall (1978); Flavin (1981); Campbell and Mankiw (1989); Working (1960); Zeldes (1989); Kimball (1990); Deaton (1991); Carroll (1997, 2006); Johnson, Parker and Souleles (2006); Parker et al. (2013, 2022); Hsieh (2003); Kueng (2018); Kaplan, Violante and Weidner (2014); Kaplan and Violante (2014); Fagereng, Holm and Natvik (2021); Jappelli and Pistaferri (2014); Fuster, Kaplan and Zafar (2021); Sahm, Shapiro and Slemrod (2012); Barro (1974); Samuelson (1958); Diamond (1965); Abel, Mankiw, Summers and Zeckhauser (1989); Dynan, Skinner and Zeldes (2004); Modigliani and Cao (2004); Chamon and Prasad (2010); Wei and Zhang (2011); Ganong and Noel (2019).

**Part 23, *Capital and Asset Prices*.** Books: John Cochrane, *Asset Pricing* (revised ed., 2005), chs. 1–2 and 21; David Romer, *Advanced Macroeconomics* (5th ed., 2019), ch. 9; Avinash Dixit and Robert Pindyck, *Investment under Uncertainty* (1994); Robert Shiller, *Irrational Exuberance* (3rd ed., 2015). Papers: Williams (1938); Gordon and Shapiro (1956); Jorgenson (1963); Tobin (1969); Hayashi (1982); McDonald and Siegel (1986); Bloom (2009); Modigliani and Miller (1958); Myers and Majluf (1984); Lucas (1978); Breeden (1979); Mehra and Prescott (1985); Hansen and Jagannathan (1991); Weil (1989); Campbell and Cochrane (1999); Bansal and Yaron (2004); Rietz (1988); Barro (2006); Shiller (1981); Campbell and Shiller (1988); Tirole (1985); Smith, Suchanek and Williams (1988); Poterba (1984); Chirinko, Fazzari and Meyer (1999); Zwick and Mahon (2017); Novy-Marx and Rauh (2011); Jordà et al. (2019); He and Krishnamurthy (2013); Adrian, Etula and Muir (2014).

**Part 24, *Looking for Work*.** Books: Christopher Pissarides, *Equilibrium Unemployment Theory* (2nd ed., 2000), ch. 1 on; Pierre Cahuc, Stéphane Carcillo and André Zylberberg, *Labor Economics* (2nd ed., 2014), chs. 5, 9; Lars Ljungqvist and Thomas Sargent, *Recursive Macroeconomic Theory* (4th ed., 2018), search and matching; Richard Rogerson, Robert Shimer and Randall Wright, JEL 43(4) (2005): the survey. Papers: Stigler (1961); McCall (1970); Diamond (1982); Mortensen and Pissarides (1994); Hosios (1990); Butters (1977); Petrongolo and Pissarides (2001); Davis and Haltiwanger (1992); Katz and Meyer (1990); Shimer (2005, 2012); Hall (2005); Hagedorn and Manovskii (2008); Pissarides (2009); Ljungqvist and Sargent (2017); Elsby, Michaels and Solon (2009); Burdett and Mortensen (1998); Topel and Ward (1992); Manning (2003); Kroft, Lange and Notowidigdo (2013); Davis and von Wachter (2011); Card, Chetty and Weber (2007); Horton (2017); Belot, Kircher and Muller (2019); Hershbein and Kahn (2018); Marinescu and Rathelot (2018); Hansen et al. (2023).

**Part 25, *Money*.** Books: Carl Walsh, *Monetary Theory and Policy* (4th ed., 2017), chs. 1–4; Milton Friedman and Anna Schwartz, *A Monetary History of the United States, 1867–1960* (1963); Thomas Sargent, *Rational Expectations and Inflation* (3rd ed., 2013); Ricardo Lagos, Guillaume Rocheteau and Randall Wright, JEL 55(2) (2017): liquidity, a survey. Papers: Jevons (1875); Furness (1910); Friedman (1991); Kocherlakota (1998); Kiyotaki and Wright (1989); Duffy and Ochs (1999); Fisher (1896, 1911); McCandless and Weber (1995); Cagan (1956); Sargent (1982); Hanke and Krus (2012); Baumol (1952); Tobin (1956); Lucas and Nicolini (2015); McLeay, Radia and Thomas (2014); Sidrauski (1967); Friedman (1969); Lucas (2000); Ball (2001); Ireland (2009); Gorton and Zhang (2023).

**Part 26, *Banks and Runs*.** Books: Xavier Freixas and Jean-Charles Rochet, *Microeconomics of Banking* (2nd ed., 2008), chs. 2, 7, 9; Gary Gorton, *Misunderstanding Financial Crises* (2012); Walter Bagehot, *Lombard Street* (1873); Anat Admati and Martin Hellwig, *The Bankers' New Clothes* (2013). Papers: Diamond and Dybvig (1983); Diamond (1984); Bernanke (1983); Merton (1977); Gorton and Metrick (2012); Morris and Shin (1998); Goldstein and Pauzner (2005); Friedman and Schwartz (1963); Calomiris and Mason (2003); Curry and Shibut (2000); Jiang, Matvos, Piskorski and Seru (2024); Drechsler, Savov and Schnabl (2017, 2021); Reinhart and Rogoff (2009); Cerra and Saxena (2008); Romer and Romer (2017); Cookson et al. (2023).

**Part 27, *The Keynesian Revolution*.** Books: John Maynard Keynes, *The General Theory of Employment, Interest and Money* (1936); Olivier Blanchard, *Macroeconomics* (8th ed., 2021), chs. 3–9; Barry Eichengreen, *Golden Fetters* (1992); Robert Skidelsky, *John Maynard Keynes* (three volumes, 1983–2000). Papers: Say (1803); Keynes (1919, 1923, 1936); Kahn (1931); Hicks (1937); Fisher (1933); Hayek (1931); Sweeney and Sweeney (1977); Krugman (1998); Okun (1962); Samuelson (1955); Bewley (1999); Card and Hyslop (1997); Dickens et al. (2007); Friedman and Schwartz (1963); Eichengreen and Sachs (1985); Romer (1992); Lucas and Sargent (1979); Mantoux (1946); Ball, Leigh and Loungani (2017); Guerrieri, Lorenzoni, Straub and Werning (2022).

**Part 28, *Inflation and Expectations*.** Books: David Romer, *Advanced Macroeconomics* (5th ed., 2019), chs. 6 and 12; Thomas Sargent, *The Conquest of American Inflation* (1999); Olivier Blanchard, *Macroeconomics* (8th ed., 2021), chs. 8–9; Robert Lucas, *Studies in Business-Cycle Theory* (1981). Papers: Phillips (1958); Samuelson and Solow (1960); Phelps (1967); Friedman (1968); Muth (1961); Lucas (1972, 1973, 1976); Sargent and Wallace (1975); Kydland and Prescott (1977); Barro and Gordon (1983); Rogoff (1985); Alesina and Summers (1993); Ball (1994); Hazell, Herre\ no, Nakamura and Steinsson (2022); Bernanke and Blanchard (2023); Benigno and Eggertsson (2023); Coibion, Gorodnichenko and Kumar (2018); Weber et al. (2022).

**Part 29, *The Cycle as Equilibrium*.** Books: Nancy Stokey, Robert Lucas and Edward Prescott, *Recursive Methods in Economic Dynamics* (1989), chs. 1–4; Lars Ljungqvist and Thomas Sargent, *Recursive Macroeconomic Theory* (4th ed., 2018), chs. 3–4; David Romer, *Advanced Macroeconomics* (5th ed., 2019), ch. 5; Robert King and Sergio Rebelo, "Resuscitating Real Business Cycles", *Handbook of Macroeconomics* (1999). Papers: Kydland and Prescott (1982); Long and Plosser (1983); Hansen (1985); Rogerson (1988); Prescott (1986); Summers (1986); Brock and Mirman (1972); Blanchard and Kahn (1980); Hodrick and Prescott (1997); Hamilton (2018); Tauchen (1986); Kopecky and Suen (2010); Galí (1999); Christiano, Eichenbaum and Vigfusson (2003); Basu, Fernald and Kimball (2006); Chari, Kehoe and McGrattan (2007); Chetty, Guren, Manoli and Weber (2011).

**Part 30, *Sticky Prices*.** Books: Jordi Galí, *Monetary Policy, Inflation, and the Business Cycle* (2nd ed., 2015), chs. 3–5; Michael Woodford, *Interest and Prices* (2003); David Romer, *Advanced Macroeconomics* (5th ed., 2019), chs. 7 and 12; Carl Walsh, *Monetary Theory and Policy* (4th ed., 2017). Papers: Calvo (1983); Mankiw (1985); Akerlof and Yellen (1985); Taylor (1993); Bils and Klenow (2004); Nakamura and Steinsson (2008); Golosov and Lucas (2007); Clarida, Galí and Gertler (1999, 2000); Blanchard and Galí (2007); Christiano, Eichenbaum and Evans (2005); Smets and Wouters (2007); Eggertsson and Woodford (2003); Del Negro, Giannoni and Patterson (2012); McKay, Nakamura and Steinsson (2016).

**Part 31, *The Central Bank*.** Books: Frederic Mishkin, *The Economics of Money, Banking and Financial Markets*, chs. 14–16 and 23–25; Carl Walsh, *Monetary Theory and Policy* (4th ed., 2017), chs. 1, 11 and 12; Alan Blinder, *Central Banking in Theory and Practice* (1998); Valerie Ramey, "Macroeconomic Shocks and Their Propagation", *Handbook of Macroeconomics* 2A (2016). Papers: Sims (1992); Christiano, Eichenbaum and Evans (1999); Romer and Romer (1989, 2000, 2004); Kuttner (2001); Gertler and Karadi (2015); Nakamura and Steinsson (2018); Coibion (2012); Orphanides (2001, 2004); Laubach and Williams (2003); Holston, Laubach and Williams (2023); Wallace (1981); Gagnon, Raskin, Remache and Sack (2011); Swanson (2021); Bernanke (2020); Calvo (1988); De Grauwe (2011).

**Part 32, *The Treasury*.** Books: Olivier Blanchard, *Fiscal Policy under Low Interest Rates* (2023); David Romer, *Advanced Macroeconomics* (5th ed., 2019), ch. 13; Valerie Ramey, "Ten Years After the Financial Crisis: What Have We Learned from the Renaissance in Fiscal Research?", *JEP* 33(2) (2019); John Cochrane, *The Fiscal Theory of the Price Level* (2023). Papers: Domar (1944); Barro (1974, 1979); Diamond (1965); Sargent and Wallace (1981); Sims (1994); Blanchard and Perotti (2002); Ramey (2011); Nakamura and Steinsson (2014); Ramey and Zubairy (2018); Romer and Romer (2010); Alesina and Ardagna (2010); Guajardo, Leigh and Pescatori (2014); Reinhart and Rogoff (2010); Herndon, Ash and Pollin (2014); Blanchard and Leigh (2013); Eaton and Gersovitz (1981); Arellano (2008); Blanchard (2019).

**Part 33, *Crises*.** Books: Charles Kindleberger and Robert Aliber, *Manias, Panics, and Crashes* (7th ed., 2015); Atif Mian and Amir Sufi, *House of Debt* (2014); Carmen Reinhart and Kenneth Rogoff, *This Time Is Different* (2009); Adam Tooze, *Crashed* (2018); Ben Bernanke, Timothy Geithner and Henry Paulson, *Firefighting* (2019). Papers: Fisher (1933); Minsky (1986); Bernanke (1983); Townsend (1979); Kiyotaki and Moore (1997); Bernanke, Gertler and Gilchrist (1999); Geanakoplos (2010); Schularick and Taylor (2012); Jordá, Schularick and Taylor (2013, 2017); Greenwood et al. (2022); Gorton and Metrick (2012); Brunnermeier and Pedersen (2009); Brunnermeier and Sannikov (2014); Mian, Rao and Sufi (2013); Calvo (1998); Rajan (2005).

**Part 34, *The Open Economy*.** Books: Paul Krugman, Maurice Obstfeld and Marc Melitz, *International Economics* (12th ed., 2022), Part 3; Maurice Obstfeld and Kenneth Rogoff, *Foundations of International Macroeconomics* (1996); Barry Eichengreen, *Globalizing Capital* (3rd ed., 2019); Martin Uribe and Stephanie Schmitt-Grohé, *Open Economy Macroeconomics* (2017). Papers: Mundell (1961, 1963); Fleming (1962); Dornbusch (1976); Balassa (1964); Samuelson (1964); Krugman (1979); Obstfeld (1996); Calvo (1998); Meese and Rogoff (1983); Fama (1984); Rogoff (1996); Lustig and Verdelhan (2007); Gourinchas and Rey (2007); Rey (2013); Gopinath, Itskhoki and Rigobon (2010); Gopinath et al. (2020); Gabaix and Maggiori (2015); Itskhoki and Mukhin (2021); Caballero, Farhi and Gourinchas (2017); Rossi (2013).

**Part 35, *Trade I: Comparative Advantage*.** Books: Paul Krugman, Maurice Obstfeld and Marc Melitz, *International Economics* (12th ed., 2022), chs 3–6, 9–10; Robert Feenstra, *Advanced International Trade* (2nd ed., 2015), chs 1–3; Douglas Irwin, *Clashing over Commerce: A History of US Trade Policy* (2017); Arnaud Costinot and Andrés Rodríguez-Clare, "Trade Theory with Numbers", *Handbook of International Economics* vol. 4 (2014). Papers: Ricardo (1817); Heckscher (1919); Ohlin (1933); Stolper and Samuelson (1941); Lerner (1952); Leontief (1953); Jones (1971); Dornbusch, Fischer and Samuelson (1977); Leamer (1980); Grossman and Helpman (1994); Trefler (1995); Bagwell and Staiger (1999); Goldberg and Maggi (1999); Eaton and Kortum (2002); Bernhofen and Brown (2004, 2005); Irwin (2005); Arkolakis, Costinot and Rodríguez-Clare (2012); Costinot and Donaldson (2012).

**Part 36, *Trade II: Scale, Firms and Gravity*.** Books: Paul Krugman, Maurice Obstfeld and Marc Melitz, *International Economics* (12th ed., 2022), chs 7–8; Robert Feenstra, *Advanced International Trade* (2nd ed., 2015), chs 5–6; Keith Head and Thierry Mayer, "Gravity Equations", *Handbook of International Economics* vol. 4 (2014); Marc Levinson, *The Box* (2006). Papers: Tinbergen (1962); Grubel and Lloyd (1975); Krugman (1979, 1980); McCallum (1995); Bernard and Jensen (1995); Eaton and Kortum (2002); Melitz (2003); Anderson and van Wincoop (2003); Santos Silva and Tenreyro (2006); Dekle, Eaton and Kortum (2008); Xing and Detert (2010); Arkolakis, Costinot and Rodríguez-Clare (2012); Autor, Dorn and Hanson (2013); Amiti, Redding and Weinstein (2019); Fajgelbaum et al. (2020); Boehm et al. (2023).

**Part 37, *Cities and Regions*.** Books: Jan Brueckner, *Lectures on Urban Economics* (2011); Edward Glaeser, *Triumph of the City* (2011); Masahisa Fujita, Paul Krugman and Anthony Venables, *The Spatial Economy* (1999); Stephen Redding and Esteban Rossi-Hansberg, "Quantitative Spatial Economics", *Annual Review of Economics* 9 (2017). Papers: von Thünen (1826); Alonso (1964); Schelling (1971); Rosen (1979); Roback (1982); Krugman (1991); Ciccone and Hall (1996); Gabaix (1999); Duranton and Puga (2004); Baum-Snow (2007); Saiz (2010); Combes et al. (2010); Kline and Moretti (2014); Ahlfeldt et al. (2015); Chetty, Hendren and Katz (2016); Donaldson (2018); Diamond, McQuade and Qian (2019); Hsieh and Moretti (2019); Greaney (2026).

**Part 38, *Work and Wages*.** Books: David Card and Alan Krueger, *Myth and Measurement* (1995); Alan Manning, *Monopsony in Motion* (2003); George Borjas, *Labor Economics*; Pierre Cahuc, Stéphane Carcillo and André Zylberberg, *Labor Economics*; Jacob Mincer, *Schooling, Experience, and Earnings* (1974). Papers: Robinson (1933); Stigler (1946); Roy (1951); Becker (1964); Heckman (1979); Card (1990); Angrist and Krueger (1991); Card and Krueger (1994); Card (1995); Camerer et al. (1997); Neumark and Wascher (2000); Oreopoulos (2006); Chetty et al. (2011); Farber (2015); Borjas (2017); Cengiz et al. (2019); Peri and Yasenov (2019); Angrist, Caldwell and Hall (2021); Sokolova and Sorensen (2021); Jardim et al. (2022).

**Part 39, *The Wage Structure*.** Books: Claudia Goldin and Lawrence Katz, *The Race between Education and Technology* (2008); Gary Becker, *The Economics of Discrimination* (1957); Claudia Goldin, *Career and Family* (2021); David Card, 'Who Set Your Wage?', *AER* (2022). Papers: Rosen (1974, 1981); Phelps (1972); Arrow (1973); Oaxaca (1973); Blinder (1973); Katz and Murphy (1992); Abowd, Kramarz and Margolis (1999); Goldin and Rouse (2000); Autor, Levy and Murnane (2003); Bertrand and Mullainathan (2004); Acemoglu and Autor (2011); Autor and Dorn (2013); Card, Heining and Kline (2013); Goldin (2014); Mas and Pallais (2017); Quillian et al. (2017); Kleven, Landais and S\ogaard (2019); Acemoglu and Restrepo (2020); Autor et al. (2020); Cullen and Pakzad-Hurson (2023).

**Part 40, *Inequality and Mobility*.** Books: Anthony Atkinson, *Inequality: What Can Be Done?* (2015); Thomas Piketty, *Capital in the Twenty-First Century* (2014); Branko Milanovic, *Global Inequality* (2016); Frank Cowell, *Measuring Inequality* (3rd edition, 2011). Papers: Pareto (1896); Champernowne (1953); Kuznets (1955); Atkinson (1970); Pen (1971); Solon (1992); Piketty and Saez (2003); Mazumder (2005); Gabaix (2009); Corak (2013); Chetty, Hendren, Kline and Saez (2014); Rognlie (2015); Krusell and Smith (2015); Gabaix, Lasry, Lions and Moll (2016); Lakner and Milanovic (2016); Chetty et al. (2016, 2017); Chetty and Hendren (2018); Piketty, Saez and Zucman (2018); Jakobsen et al. (2020); Black et al. (2020); Auten and Splinter (2024).

**Part 41, *Taxes*.** Books: Bernard Salanié, *The Economics of Taxation* (2nd edition, 2011); Joel Slemrod and Jon Bakija, *Taxing Ourselves* (5th edition, 2017); Peter Diamond and Emmanuel Saez, 'The Case for a Progressive Tax', *JEP* (2011); Jonathan Gruber, *Public Finance and Public Policy*, chapters 18–25. Papers: Ramsey (1927); Harberger (1962); Mirrlees (1971); Diamond and Mirrlees (1971); Allingham and Sandmo (1972); Atkinson and Stiglitz (1976); Judd (1985); Chamley (1986); Feldstein (1995); Diamond (1998); Saez (2001, 2002, 2010); Gruber and Saez (2002); Chetty, Looney and Kroft (2009); Kleven et al. (2011); Saez, Slemrod and Giertz (2012); Kleven and Waseem (2013); Kleven, Landais and Saez (2013); Zucman (2013); Piketty, Saez and Stantcheva (2014); Fuest, Peichl and Siegloch (2018); Straub and Werning (2020).

**Part 42, *Social Insurance*.** Books: Jonathan Gruber, *Public Finance and Public Policy*, chapters 12–17; Nicholas Barr, *The Economics of the Welfare State* (6th edition, 2020); Liran Einav and Amy Finkelstein, *Risky Business* (2023); Raj Chetty and Amy Finkelstein, 'Social Insurance: Connecting Theory to Data', *Handbook of Public Economics* 5 (2013). Papers: Arrow (1963); Pauly (1968); Zeckhauser (1970); Akerlof (1978); Baily (1978); Robins (1985); Manning et al. (1987); Meyer (1990); Eissa and Liebman (1996); Gruber (1997); Madrian and Shea (2001); Chetty (2006, 2008); Card, Chetty and Weber (2007); Finkelstein et al. (2012); Schmieder, von Wachter and Bender (2012); Baicker et al. (2013); Maestas, Mullen and Strand (2013); Chetty et al. (2014); Taubman et al. (2014); Ganong and Noel (2019); Finkelstein, Hendren and Luttmer (2019); Hendren and Sprung-Keyser (2020).

**Part 43, *Measuring Market Power*.** Books: Jean Tirole, *The Theory of Industrial Organization* (1988); Kenneth Train, *Discrete Choice Methods with Simulation* (2nd edition, 2009); Aviv Nevo, 'A Practitioner's Guide to Estimation of Random-Coefficients Logit Models of Demand', *JEMS* (2000); Steven Berry and Philip Haile, 'Foundations of Demand Estimation', *Handbook of Industrial Organization* 4 (2021). Papers: Bain (1951); Lancaster (1966); Demsetz (1973); McFadden (1974); Bresnahan (1982); Lau (1982); Bresnahan and Reiss (1991); Berry (1994); Berry, Levinsohn and Pakes (1995, 2004); Olley and Pakes (1996); Werden (1996); Nevo (2001); Axtell (2001); Petrin (2002); Levinsohn and Petrin (2003); Farrell and Shapiro (2010); Syverson (2011); De Loecker and Warzynski (2012); Ackerberg, Caves and Frazer (2015); Ashenfelter, Hosken and Weinberg (2015); Miller and Weinberg (2017); Traina (2018); Basu (2019); De Loecker, Eeckhout and Unger (2020); Bond et al. (2021).

**Part 44, *Dynamics, Platforms and Antitrust*.** Books: Jean Tirole, *The Theory of Industrial Organization* (1988); Aguirregabiria, *Empirical Industrial Organization: Models, Methods, and Applications* (2021); Michael Whinston, *Lectures on Antitrust Economics* (2006); Jean Tirole, *Economics for the Common Good* (2017). Papers: Spengler (1950); Arrow (1962); Baron and Myerson (1982); David (1985); Rust (1987); Arthur (1989); Liebowitz and Margolis (1990); Hotz and Miller (1993); Pakes and McGuire (1994); Ericson and Pakes (1995); Rochet and Tirole (2003); Rysman (2004); Aghion et al. (2005); Armstrong (2006); Bajari, Benkard and Levin (2007); Ryan (2012); Kwoka (2013, 2015); Khan (2017); Calvano et al. (2020); Cunningham, Ederer and Ma (2021); Assad et al. (2024).

**Part 45, *Behavioural Economics*.** Books: Richard Thaler, *Misbehaving: The Making of Behavioral Economics* (2015); Daniel Kahneman, *Thinking, Fast and Slow* (2011); Sanjit Dhami, *The Foundations of Behavioral Economic Analysis* (2016); Bernheim, DellaVigna and Laibson (eds.), *Handbook of Behavioral Economics* (2018–19). Papers: Kahneman and Tversky (1979); Thaler (1980); Kahneman, Knetsch and Thaler (1990); Laibson (1997); O'Donoghue and Rabin (1999); Fehr and Schmidt (1999); Madrian and Shea (2001); Genesove and Mayer (2001); List (2003); Thaler and Benartzi (2004); Sims (2003); DellaVigna and Malmendier (2004, 2006); Ashraf, Karlan and Yin (2006); Gabaix and Laibson (2006); DellaVigna (2009); Bernheim and Rangel (2009); Pope and Schweitzer (2011); DellaVigna and Linos (2022).

**Part 46, *Development*.** Books: Abhijit Banerjee and Esther Duflo, *Poor Economics* (2011); Debraj Ray, *Development Economics* (1998); Amartya Sen, *Development as Freedom* (1999); Angus Deaton, *The Great Escape* (2013). Papers: Lewis (1954); Townsend (1994); Duflo (2001); Miguel and Kremer (2004); Schultz (2004); Thornton (2008); Nunn (2008); Cohen and Dupas (2010); Dell (2010); Deaton (2010); Duflo, Kremer and Robinson (2011); Banerjee et al. (2015); Banerjee, Karlan and Zinman (2015); Haushofer and Shapiro (2016); Suri and Jack (2016); Muralidharan and Niehaus (2017); Balboni et al. (2022); Egger et al. (2022); Aiken et al. (2022).

**Part 47, *Political Economy*.** Books: Mancur Olson, *The Logic of Collective Action* (1965); Torsten Persson and Guido Tabellini, *Political Economics* (2000); Daron Acemoglu and James Robinson, *Economic Origins of Dictatorship and Democracy* (2006); Timothy Besley and Torsten Persson, *Pillars of Prosperity* (2011). Papers: Tullock (1967); Stigler (1971); Barro (1973); Krueger (1974); Nordhaus (1975); Ferejohn (1986); Grossman and Helpman (1994); Goldberg and Maggi (1999); Fisman (2001); Lee, Moretti and Butler (2004); Reinikka and Svensson (2004); Miguel et al. (2004); Olken (2007); Fisman and Miguel (2007); DellaVigna and Kaplan (2007); Lee (2008); Ferraz and Finan (2011); Cattaneo et al. (2015); Acemoglu et al. (2019); Funke et al. (2023).

**Part 48, *Environment and Climate*.** Books: William Nordhaus, *A Question of Balance* (2008) and *The Climate Casino* (2013); Nicholas Stern, *The Economics of Climate Change: The Stern Review* (2007); Paul Sabin, *The Bet* (2013); Tom Tietenberg and Lynne Lewis, *Environmental and Natural Resource Economics*. Papers: Hotelling (1931); Gordon (1954); Smith (1969); Weitzman (1974); Slade (1982); Nordhaus (1992); Borenstein et al. (2002); Hughes et al. (2008); Costello et al. (2008); Weitzman (2009); Kiel et al. (2010); Acemoglu et al. (2012); Dell et al. (2012); Chen et al. (2013); Burke et al. (2015); McGlade and Ekins (2015); Nordhaus (2015, 2017); Barreca et al. (2016); Ebenstein et al. (2017); Deryugina et al. (2020); Dietz et al. (2021); Rennert et al. (2022); Barrage and Nordhaus (2024); Bilal and Känzig (2024).

**Part 49, *The Economic Approach*.** Books: Gary Becker, *The Economic Approach to Human Behavior* (1976) and *A Treatise on the Family* (1981); Steven Levitt and Stephen Dubner, *Freakonomics* (2005), for the stories, read critically; Claudia Goldin, *Career and Family* (2021); Anne Case and Angus Deaton, *Deaths of Despair and the Future of Capitalism* (2020). Papers: Becker (1965, 1968, 1973); Becker and Lewis (1973); Grossman (1972); Becker and Murphy (1988); Levitt (1997); Angrist and Evans (1998); Krueger (1999); Angrist and Lavy (1999, 2019); Lazear (2000); Gneezy and Rustichini (2000); Goldin and Katz (2002); Di Tella and Schargrodsky (2004); Choo and Siow (2006); Heckman et al. (2010); Draca et al. (2011); Wei and Zhang (2011); Nagin (2013); Chetty et al. (2014); Case and Deaton (2015); Lee and McCrary (2017); Chalfin and McCrary (2018); Cooper et al. (2019); Alpert et al. (2022); Durkin et al. (2022).

**Part 50, *The Policy Memo*.** Books: Jonathan Gruber, *Public Finance and Public Policy*, the chapters on cost-benefit analysis and on welfare programmes; Anthony Boardman, David Greenberg, Aidan Vining and David Weimer, *Cost-Benefit Analysis: Concepts and Practice*; Joshua Angrist and Jörn-Steffen Pischke, *Mastering 'Metrics* (2015); Eugene Bardach and Eric Patashnik, *A Practical Guide for Policy Analysis*. Papers: Orcutt (1957); Saez (2001); Chetty, Guren, Manoli and Weber (2011); Milligan (2005); Milligan and Stabile (2011); Aizer, Eli, Ferrie and Lleras-Muney (2016); Hendren and Sprung-Keyser (2020); Corinth, Meyer, Stadnicki and Wu (2021); Ananat, Glasner, Hamilton and Parolin (2022); Baker, Messacar and Stabile (2023); Noble, Magnuson, Duncan, Gennetian et al. (2025); Egger et al. (2022).

**Part 51, *Computing Economies*.** Books: Kenneth Judd, *Numerical Methods in Economics* (1998); Nancy Stokey and Robert Lucas, with Edward Prescott, *Recursive Methods in Economic Dynamics* (1989), chapters 3, 4 and 9; Thomas Sargent and John Stachurski, *Dynamic Programming* and the QuantEcon lectures; Jesús Fernández-Villaverde, Juan Rubio-Ramírez and Frank Schorfheide, 'Solution and estimation methods for DSGE models', *Handbook of Macroeconomics* (2016). Papers: Bellman (1957); Howard (1960); Blackwell (1965); Smolyak (1963); Tauchen (1986); Judd (1992); Den Haan and Marcet (1994); Rouwenhorst (1995); Krueger and Kubler (2004); Schmitt-Grohé and Uribe (2004); Carroll (2006); Aruoba, Fernández-Villaverde and Rubio-Ramírez (2006); Kopecky and Suen (2010); Guerrieri and Iacoviello (2015); Maliar, Maliar and Winant (2021); Achdou, Han, Lasry, Lions and Moll (2022); Azinovic, Gaegauf and Scheidegger (2022).

**Part 52, *Many Agents*.** Books: Lars Ljungqvist and Thomas Sargent, *Recursive Macroeconomic Theory*, chapters 17 and 18; Greg Kaplan, 'Heterogeneous agent macroeconomics', lecture notes, and Benjamin Moll's notes on continuous time; Per Krusell and Anthony Smith, 'Quantitative macroeconomic models with heterogeneous agents' (2006); Adrien Auclert and coauthors, the sequence-space Jacobian toolkit and its documentation. Papers: Gorman (1953); Bewley (1977); Kirman (1992); Hopenhayn (1992); Huggett (1993); Aiyagari (1994); Krusell and Smith (1998); Doepke and Schneider (2006); Khan and Thomas (2008); Den Haan (2010); Young (2010); Benhabib, Bisin and Zhu (2011, 2015); Kaplan and Violante (2014); Werning (2015); McKay, Nakamura and Steinsson (2016); Kaplan, Moll and Violante (2018); Auclert, Bardóczy, Rognlie and Straub (2021); Fagereng, Holm and Natvik (2021); Achdou et al. (2022).

**Part 53, *Information and Persuasion*.** Books: Drew Fudenberg and Jean Tirole, *Game Theory* (1991), chapters 6 to 10; Emir Kamenica, 'Bayesian persuasion and information design', *Annual Review of Economics* (2019); Dirk Bergemann and Stephen Morris, 'Information design: a unified perspective', *JEL* (2019); Stephen Morris and Hyun Song Shin, 'Global games: theory and applications' (2003). Papers: Harsanyi (1967–68); Nash (1950); Blackwell (1953); Coase (1972); Aumann (1976); Selten (1978); Crawford and Sobel (1982); Geanakoplos and Polemarchakis (1982); Rubinstein (1982); Kreps and Wilson (1982); Milgrom and Roberts (1982); Cho and Kreps (1987); Bull (1987); Rubinstein (1989); Banerjee (1992); Bikhchandani, Hirshleifer and Welch (1992); Carlsson and van Damme (1993); Morris and Shin (1998); Levin (2003); DellaVigna and Kaplan (2007); Kamenica and Gentzkow (2011).

**Part 54, *Estimating Models*.** Books: Kenneth Train, *Discrete Choice Methods with Simulation* (2nd ed., 2009); Fumio Hayashi, *Econometrics* (2000), chapters 3, 4 and 7; Hamish Low and Costas Meghir, 'The use of structural models in econometrics', *JEP* (2017); Charles Manski, *Partial Identification of Probability Distributions* (2003). Papers: Marschak (1953); McFadden (1974, 1989); Hansen (1982); Hansen and Singleton (1982); Kydland and Prescott (1982); Rust (1987); Pakes and Pollard (1989); Manski (1990); Gouriéroux, Monfort and Renault (1993); Hotz and Miller (1993); Keane and Wolpin (1997); Gourinchas and Parker (2002); Todd and Wolpin (2006); Chetty (2009); Andrews, Gentzkow and Shapiro (2017); Cranmer, Brehmer and Louppe (2020).

**Part 55, *Identifying Macro*.** Books: Lutz Kilian and Helmut Lütkepohl, *Structural Vector Autoregressive Analysis* (2017); James Hamilton, *Time Series Analysis* (1994), chapters 11 to 13; Valerie Ramey, 'Macroeconomic shocks and their propagation', *Handbook of Macroeconomics* (2016); Emi Nakamura and Jón Steinsson, 'Identification in macroeconomics', *JEP* (2018). Papers: Sims (1980, 1992); Blanchard and Quah (1989); Kuttner (2001); Rigobon (2003); Romer and Romer (2004); Jordá (2005); Uhlig (2005); Christiano, Eichenbaum and Evans (2005); An and Schorfheide (2007); Smets and Wouters (2007); Canova and Sala (2009); Stock and Watson (2012, 2018); Mertens and Ravn (2013); Nakamura and Steinsson (2014, 2018); Gertler and Karadi (2015); Goldsmith-Pinkham, Sorkin and Swift (2020); Plagborg-M\oller and Wolf (2021).

**Part 56, *The Core Exam*.** Books: Andreu Mas-Colell, Michael Whinston and Jerry Green, *Microeconomic Theory* (1995); David Kreps, *A Course in Microeconomic Theory* (1990); Lars Ljungqvist and Thomas Sargent, *Recursive Macroeconomic Theory* (2000; 4th ed. 2018); David Romer, *Advanced Macroeconomics* (1996; 5th ed. 2019); Jordi Galí, *Monetary Policy, Inflation, and the Business Cycle* (2008; 2nd ed. 2015); Fumio Hayashi, *Econometrics* (2000). Papers: Mussa and Rosen (1978); Myerson (1981); Riley and Samuelson (1981); Hansen (1982); Burtless and Hausman (1978); Chamley (1986); Blanchard and Quah (1989); Katz and Meyer (1990); Aiyagari (1994); Clarida, Galí and Gertler (1999); Chamberlain and Wilson (2000); Card, Chetty and Weber (2007); Goodman-Bacon (2021); Callaway and Sant'Anna (2021); Borusyak, Jaravel and Spiess (2024).

**Part 57, *Reading the Economy in Real Time*.** Books: Graham Elliott and Allan Timmermann, *Economic Forecasting* (2016); Marta Bańbura, Domenico Giannone, Michele Modugno and Lucrezia Reichlin, 'Now-casting and the real-time data flow', *Handbook of Economic Forecasting* 2A (2013); Dean Croushore, 'Frontiers of real-time data analysis', *JEL* 49(1) (2011). Papers: Bates and Granger (1969); Mankiw and Shapiro (1986); Hamilton (1989); Diebold and Mariano (1995); Estrella and Mishkin (1998); Romer and Romer (2000); Stock and Watson (2002, 2004); Giannone, Reichlin and Small (2008); Henderson, Storeygard and Weil (2012); Baker, Bloom and Davis (2016); Cavallo and Rigobon (2016); An, Jalles and Loungani (2018); Hansen, McMahon and Prat (2018); Sahm (2019); Gentzkow, Kelly and Taddy (2019); Blanchet, Saez and Zucman (2022); Bernanke (2024); Chetty et al. (2024).

**Part 58, *Scoring the Bill*.** Books: Anthony Boardman, David Greenberg, Aidan Vining and David Weimer, *Cost-Benefit Analysis: Concepts and Practice* (5th ed., 2018); HM Treasury, *The Green Book*; Office of Management and Budget, *Circular A-4*; Bent Flyvbjerg, Nils Bruzelius and Werner Rothengatter, *Megaprojects and Risk* (2003). Papers: Dupuit (1844); Hotelling (1947); Schelling (1968); Rosen (1974); Thaler and Rosen (1976); Harberger (1962); Goodhart (1975); Campbell (1979); Kahneman and Lovallo (1993); Diamond and Hausman (1994); Weitzman (1998, 2001); Saez (2001); Flyvbjerg, Holm and Buhl (2002, 2005); Viscusi and Aldy (2003); Auerbach (2005); Kehoe (2005); Bevan and Hood (2006); Drupp et al. (2018); Hendren and Sprung-Keyser (2020).

**Part 59, *The Expert Witness*.** Books: Peter Davis and Eliana Garcés, *Quantitative Techniques for Competition and Antitrust Analysis* (2010); John Kwoka, *Mergers, Merger Control, and Remedies* (2015); The U.S. Merger Guidelines (2010, 2023); the European Commission's horizontal merger guidelines (2004). Papers: Harris and Simons (1989); Werden (1996); Crooke, Froeb, Tschantz and Werden (1999); Katz and Shapiro (2003); Ashenfelter et al. (2006); Abrantes-Metz et al. (2006); Whinston (2007); Farrell and Shapiro (2010); Ashenfelter and Hosken (2010); Cooper et al. (2019); Prager and Schmitt (2021); Shapiro (2021) on AT&T; Krueger and Ashenfelter (2022); Brot-Goldberg et al. (2024).

**Part 60, *The Price*.** Books: Kalyan Talluri and Garrett van Ryzin, *The Theory and Practice of Revenue Management* (2004); Robert Phillips, *Pricing and Revenue Optimization* (2nd ed., 2021); Thomas Nagle and Georg Müller, *The Strategy and Tactics of Pricing*. Papers: Hall and Hitch (1939); Becker, DeGroot and Marschak (1964); Littlewood (1972); Mussa and Rosen (1978); Belobaba (1987); Smith, Leimkuhler and Darrow (1992); Gallego and van Ryzin (1994); Deneckere and McAfee (1996); Blinder et al. (1998); Bakos and Brynjolfsson (1999); Murphy et al. (2005); Blake and Coey (2014); DellaVigna and Gentzkow (2019); Calvano et al. (2020); Blake et al. (2021); Williams (2022).

**Part 61, *Economics at the Platforms*.** Books: Ron Kohavi, Diane Tang and Ya Xu, *Trustworthy Online Controlled Experiments* (2020); David Evans and Richard Schmalensee, *Matchmakers: The New Economics of Multisided Platforms* (2016). Papers: Rochet and Tirole (2003); Edelman, Ostrovsky and Schwarz (2007); Varian (2007); Ostrovsky and Schwarz (2009); Blake, Nosko and Tadelis (2015); Lewis and Rao (2015); Hall, Kendrick and Nosko (2015); Tadelis (2016); Cohen et al. (2016); Einav, Farronato and Levin (2016); Chen et al. (2019); Athey and Luca (2019); Athey, Chetty, Imbens and Kang (2019); Brynjolfsson, Collis and Eggers (2019); Fradkin, Grewal and Holtz (2021); Bajari et al. (2023).

**Part 62, *Inside the Firm*.** Books: Edward Lazear and Michael Gibbs, *Personnel Economics in Practice* (3rd ed., 2014); Robert Gibbons and John Roberts, eds., *The Handbook of Organizational Economics* (2013); Jean Tirole, *The Theory of Corporate Finance* (2006). Papers: Modigliani and Miller (1958); Jensen and Meckling (1976); Myers and Majluf (1984); Jensen and Murphy (1990); Garicano (2000); Lazear (2000); Bertrand and Mullainathan (2001); Graham and Harvey (2001); Syverson (2004, 2011); Bloom and Van Reenen (2007); Bennedsen et al. (2007); Gabaix and Landier (2008); Gibbons and Henderson (2012); Bloom et al. (2013, 2015); Davis et al. (2014); Bruhn, Karlan and Schoar (2018); Benson, Li and Shue (2019).

**Part 63, *The Economy as a Network*.** Books: Matthew O. Jackson, *Social and Economic Networks* (2008); Vasco Carvalho and Alireza Tahbaz-Salehi, "Production Networks: A Primer", *Annual Review of Economics* (2019); Sanjeev Goyal, *Connections: An Introduction to the Economics of Networks* (2007). Papers: Leontief (1936); Domar (1961); Hulten (1978); Lucas (1977); Granovetter (1973); Kremer (1993); Jackson and Wolinsky (1996); Eisenberg and Noe (2001); Ballester, Calvó-Armengol and Zenou (2006); Gabaix (2011); Acemoglu et al. (2012, 2015); Banerjee et al. (2013); Elliott, Golub and Jackson (2014); Barrot and Sauvagnat (2016); Baqaee and Farhi (2019); Boehm et al. (2019); Carvalho et al. (2021); Elliott, Golub and Leduc (2022); Rajkumar et al. (2022).

## 4. What the series leaves out

- **Accounting and corporate finance.** The firm's books and its capital structure appear only where an economic argument needs them (the T-accounts of money and banks in Parts 25 and 26); there is no course in valuation or financial reporting.
- **Derivatives and financial engineering.** Asset pricing is taught as economics (Part 23: the stochastic discount factor and its puzzles); option pricing and the mathematics of hedging belong to *Quant, Built*.
- **The history of economic thought as a field.** Each idea arrives with its people, its year and its dead ends, but the series does not survey schools for their own sake. Marxian, Austrian, post-Keynesian, institutionalist and complexity arguments appear where they bear on a part's question, with their best case (SYLLABUS, section 1).
- **Sector fields.** Agricultural, health, transport and energy economics are drawn on for examples (health insurance in Part 42, carbon in Part 48) but have no parts of their own.
- **Country studies.** The Data Room's countries are evidence, not subjects: no part is a course on one economy.
