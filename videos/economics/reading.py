"""The reading of *Economics, Built*, as data: the textbooks the series follows, the classic papers and models it
teaches, and each built part's reference card.  ``python -m videos.economics.reading`` writes
``videos/economics/READING.md`` from it; ``tests/economics/test_reading.py`` checks that every book and paper listed is
planned by the syllabus for the parts it names, and that the file is up to date.

Two columns are found, never typed.  *Planned* lists the parts whose entry in ``SYLLABUS.md`` (section 4) names the
book or paper; *Built* lists the parts whose scenes, compute step or README cite it.  So the map cannot claim that a
part covers something its plan does not mention, nor that a film teaches something it does not show.
"""

from __future__ import annotations

import ast
import re
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
PARTS = range(1, 69)


def fold(s: str) -> str:
    """ASCII text with TeX and Unicode accents removed and TeX's dashes and ampersands made plain, so that
    G\\"odel, Gödel and Godel all match, and so do "Gode \\& Sunder", "Gode & Sunder" and "Gode and Sunder"."""
    s = re.sub(r"\\[`'\"^~=.]\{?([A-Za-z])\}?", r"\1", s)
    s = re.sub(r"\\[vuc]\{([A-Za-z])\}", r"\1", s)
    s = s.replace("\\&", "&").replace("\\emph{", "").replace("\\ ", " ")
    s = re.sub(r"\s+", " ", s).replace(" and ", " & ")
    s = s.replace("---", "-").replace("--", "-").replace("–", "-").replace("—", "-")
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()


def built_parts() -> list[int]:
    return sorted(int(p.parent.name[4:]) for p in HERE.glob("econ[0-9]*/manifest.py"))


def sources(part: int) -> str:
    d = HERE / f"econ{part}"
    files = sorted(d.glob("s[0-9]*.py")) + [d / "compute.py", d / "README.md"]
    return fold("\n".join(p.read_text() for p in files if p.exists()))


def syllabus_entries() -> dict[int, str]:
    """Each part's entry in SYLLABUS.md section 4, from its ``### Part N · `` heading to the next heading."""
    text = (HERE / "SYLLABUS.md").read_text()
    out = {}
    for m in re.finditer(r"^### Part (\d+) · .*?(?=^##)", text, flags=re.M | re.S):
        out[int(m.group(1))] = fold(m.group(0))
    return out


_BUILT: dict[int, str] = {}
_PLANNED: dict[int, str] = {}


def cited_by(pattern: str) -> list[int]:
    """The built parts whose scenes, compute step or README match ``pattern`` (a regex over accent-folded text)."""
    if not _BUILT:
        _BUILT.update({n: sources(n) for n in built_parts()})
    return [n for n, t in _BUILT.items() if re.search(pattern, t)]


def planned_in(pattern: str) -> list[int]:
    """The parts whose syllabus entry matches ``pattern``."""
    if not _PLANNED:
        _PLANNED.update(syllabus_entries())
    return [n for n, t in sorted(_PLANNED.items()) if re.search(pattern, t)]


# (tier, short name, the book, the pattern that finds it in a syllabus entry or a part)
SPINE = [
 ("Principles", "Mankiw", "N. G. Mankiw, *Principles of Economics* (10th ed., 2024)", r"(?<!& )Mankiw(?!( 19| &|, Romer|'s))"),
 ("Principles", "Krugman–Wells", "P. Krugman and R. Wells, *Economics* (6th ed., 2021)", r"Krugman & Wells"),
 ("Principles", "Acemoglu–Laibson–List", "D. Acemoglu, D. Laibson and J. List, *Economics* (3rd ed., 2022)", r"Acemoglu, Laibson & List"),
 ("Principles", "CORE", "The CORE Team, *The Economy* (2017; 2.0, 2023)", r"CORE"),
 ("Principles", "Heilbroner", "R. Heilbroner, *The Worldly Philosophers* (7th ed., 1999)", r"Heilbroner"),
 ("The major", "Varian", "H. Varian, *Intermediate Microeconomics* (9th ed., 2014)", r"Varian(?!( 19| 20|, \"))"),
 ("The major", "Nicholson–Snyder", "W. Nicholson and C. Snyder, *Microeconomic Theory* (13th ed., 2021)", r"Nicholson"),
 ("The major", "Jones", "C. I. Jones, *Macroeconomics* (6th ed., 2023)", r"Jones, \*Macro|Jones chs?"),
 ("The major", "Blanchard", "O. Blanchard, *Macroeconomics* (8th ed., 2021)", r"Blanchard(?!( &| 19| 20|-))"),
 ("The major", "Stock–Watson", "J. Stock and M. Watson, *Introduction to Econometrics* (4th ed., 2019)", r"Stock & Watson(?! (19|20))"),
 ("The major", "Angrist–Pischke", "J. Angrist and J.-S. Pischke, *Mostly Harmless Econometrics* (2009)", r"Angrist & Pischke"),
 ("The major", "Osborne", "M. Osborne, *An Introduction to Game Theory* (2004)", r"(?<!& )Osborne(?!( &|'s))"),
 ("The major", "Krugman–Obstfeld–Melitz", "P. Krugman, M. Obstfeld and M. Melitz, *International Economics* (12th ed., 2022)", r"Krugman, Obstfeld & Melitz"),
 ("The major", "Mishkin", "F. Mishkin, *The Economics of Money, Banking, and Financial Markets* (13th ed., 2022)", r"(?<!& )Mishkin(?! (19|20))"),
 ("The major", "Cabral", "L. Cabral, *Introduction to Industrial Organization* (2nd ed., 2017)", r"Cabral"),
 ("The major", "Borjas", "G. Borjas, *Labor Economics* (8th ed., 2020)", r"Borjas(?! (19|20))"),
 ("The major", "Gruber", "J. Gruber, *Public Finance and Public Policy* (7th ed., 2022)", r"Gruber(?! (19|20))"),
 ("The major", "Ray", "D. Ray, *Development Economics* (1998)", r"\bRay(,|;| chs?|\.)"),
 ("The major", "Weil", "D. Weil, *Economic Growth* (3rd ed., 2013)", r"(?<!& )Weil(?! 1992)"),
 ("Graduate micro", "MWG", "A. Mas-Colell, M. Whinston and J. Green, *Microeconomic Theory* (1995)", r"MWG|Mas-Colell"),
 ("Graduate micro", "Kreps", "D. Kreps, *Microeconomic Foundations I* (2013)", r"Kreps(?! 19| &)"),
 ("Graduate micro", "Jehle–Reny", "G. Jehle and P. Reny, *Advanced Microeconomic Theory* (3rd ed., 2011)", r"Jehle"),
 ("Graduate micro", "Fudenberg–Tirole", "D. Fudenberg and J. Tirole, *Game Theory* (1991)", r"Fudenberg & Tirole"),
 ("Graduate micro", "Osborne–Rubinstein", "M. Osborne and A. Rubinstein, *A Course in Game Theory* (1994)", r"Osborne & Rubinstein"),
 ("Graduate micro", "Bolton–Dewatripont", "P. Bolton and M. Dewatripont, *Contract Theory* (2005)", r"Bolton & Dewatripont"),
 ("Graduate micro", "Krishna", "V. Krishna, *Auction Theory* (2nd ed., 2010)", r"\bKrishna\b"),
 ("Graduate micro", "Milgrom", "P. Milgrom, *Putting Auction Theory to Work* (2004)", r"Putting Auction Theory|Milgrom, \*"),
 ("Graduate micro", "Roth–Sotomayor", "A. Roth and M. Sotomayor, *Two-Sided Matching* (1990)", r"Roth & Sotomayor"),
 ("Graduate micro", "Börgers", "T. Börgers, *An Introduction to the Theory of Mechanism Design* (2015)", r"Borgers"),
 ("Graduate micro", "Tirole IO", "J. Tirole, *The Theory of Industrial Organization* (1988)", r"Tirole, \*(The Theory of )?Industrial|Tirole chs"),
 ("Graduate macro", "Romer", "D. Romer, *Advanced Macroeconomics* (5th ed., 2019)", r"Romer, \*Advanced|Romer chs?|; Romer;"),
 ("Graduate macro", "Ljungqvist–Sargent", "L. Ljungqvist and T. Sargent, *Recursive Macroeconomic Theory* (4th ed., 2018)", r"Ljungqvist"),
 ("Graduate macro", "SLP", "N. Stokey, R. Lucas and E. Prescott, *Recursive Methods in Economic Dynamics* (1989)", r"Stokey, Lucas & Prescott"),
 ("Graduate macro", "Acemoglu", "D. Acemoglu, *Introduction to Modern Economic Growth* (2009)", r"Acemoglu, \*|Acemoglu chs?"),
 ("Graduate macro", "Galí", "J. Galí, *Monetary Policy, Inflation, and the Business Cycle* (2nd ed., 2015)", r"Gali(,| chs?|;|\.)"),
 ("Graduate macro", "Woodford", "M. Woodford, *Interest and Prices* (2003)", r"Woodford(,| chs?|;|\.)"),
 ("Graduate macro", "Walsh", "C. Walsh, *Monetary Theory and Policy* (4th ed., 2017)", r"Walsh(?! (19|20))"),
 ("Graduate macro", "Obstfeld–Rogoff", "M. Obstfeld and K. Rogoff, *Foundations of International Macroeconomics* (1996)", r"Obstfeld & Rogoff"),
 ("Graduate macro", "Pissarides", "C. Pissarides, *Equilibrium Unemployment Theory* (2nd ed., 2000)", r"Equilibrium Unemployment Theory"),
 ("Graduate macro", "Cochrane", "J. Cochrane, *Asset Pricing* (rev. ed., 2005)", r"Cochrane, \*Asset|Cochrane chs?"),
 ("Graduate macro", "Freixas–Rochet", "X. Freixas and J.-C. Rochet, *Microeconomics of Banking* (2nd ed., 2008)", r"Freixas"),
 ("Econometrics and computation", "Hayashi", "F. Hayashi, *Econometrics* (2000)", r"Hayashi(?! 19)"),
 ("Econometrics and computation", "Wooldridge", "J. Wooldridge, *Econometric Analysis of Cross Section and Panel Data* (2nd ed., 2010)", r"Wooldridge"),
 ("Econometrics and computation", "Hansen", "B. Hansen, *Econometrics* (2022)", r"Hansen, \*Econometrics|B\. Hansen"),
 ("Econometrics and computation", "Hamilton", "J. Hamilton, *Time Series Analysis* (1994)", r"Hamilton, \*Time|Hamilton chs?|Hamilton(;|\.)"),
 ("Econometrics and computation", "Kilian–Lütkepohl", "L. Kilian and H. Lütkepohl, *Structural Vector Autoregressive Analysis* (2017)", r"Kilian & Lutkepohl"),
 ("Econometrics and computation", "Train", "K. Train, *Discrete Choice Methods with Simulation* (2nd ed., 2009)", r"Train(,|;|\.| chs?)"),
 ("Econometrics and computation", "Judd", "K. Judd, *Numerical Methods in Economics* (1998)", r"Judd(,|;|\.)"),
 ("Econometrics and computation", "QuantEcon", "T. Sargent and J. Stachurski, *Quantitative Economics* (QuantEcon lectures)", r"Stachurski|QuantEcon"),
 ("The fields", "Feenstra", "R. Feenstra, *Advanced International Trade* (2nd ed., 2016)", r"Feenstra(?! (19|20))"),
 ("The fields", "Cahuc–Carcillo–Zylberberg", "P. Cahuc, S. Carcillo and A. Zylberberg, *Labor Economics* (2nd ed., 2014)", r"Cahuc"),
 ("The fields", "Atkinson–Stiglitz", "A. Atkinson and J. Stiglitz, *Lectures on Public Economics* (1980; 2015)", r"Atkinson & Stiglitz"),
 ("The fields", "Salanié", "B. Salanie, *The Economics of Taxation* (2nd ed., 2011)", r"(?<!& )Salanie(?! (19|20))"),
 ("The fields", "Banerjee–Duflo", "A. Banerjee and E. Duflo, *Poor Economics* (2011)", r"Poor Economics"),
 ("The fields", "Persson–Tabellini", "T. Persson and G. Tabellini, *Political Economics* (2000)", r"Persson & Tabellini"),
 ("The fields", "Dhami", "S. Dhami, *The Foundations of Behavioral Economic Analysis* (2016)", r"Dhami"),
 ("The fields", "Fujita–Krugman–Venables", "M. Fujita, P. Krugman and A. Venables, *The Spatial Economy* (1999)", r"Fujita"),
 ("The fields", "Nordhaus", "W. Nordhaus, *A Question of Balance* (2008)", r"Question of Balance"),
 ("The fields", "Jackson", "M. Jackson, *Social and Economic Networks* (2008)", r"Jackson, \*Social|Social and Economic Networks"),
 ("Practice", "Blinder", "A. Blinder, *Central Banking in Theory and Practice* (1998)", r"Blinder(;|,|\.)"),
 ("Practice", "Boardman", "A. Boardman and others, *Cost-Benefit Analysis* (5th ed., 2018)", r"Boardman"),
 ("Practice", "Davis–Garcés", "P. Davis and E. Garces, *Quantitative Techniques for Competition and Antitrust Analysis* (2010)", r"Davis & Garces"),
 ("Practice", "Talluri–van Ryzin", "K. Talluri and G. van Ryzin, *The Theory and Practice of Revenue Management* (2004)", r"Talluri"),
 ("Practice", "Kohavi–Tang–Xu", "R. Kohavi, D. Tang and Y. Xu, *Trustworthy Online Controlled Experiments* (2020)", r"Kohavi"),
 ("Practice", "Lazear–Gibbs", "E. Lazear and M. Gibbs, *Personnel Economics in Practice* (3rd ed., 2014)", r"Lazear & Gibbs"),
]

# (area, model or result, the paper, the pattern)
PAPERS = [
 ("Markets and prices", "the division of labour", "Smith (1776), *The Wealth of Nations*", r"Smith 1776|Wealth of Nations"),
 ("Markets and prices", "comparative advantage", "Ricardo (1817), *Principles*, ch. 7", r"Ricardo"),
 ("Markets and prices", "supply and demand, the scissors", "Marshall (1890), *Principles of Economics*", r"Marshall('s)? \(?1890|Marshall's scissors"),
 ("Markets and prices", "the price system as information", "Hayek (1945), \"The Use of Knowledge in Society\"", r"Hayek \(?1945|Use of Knowledge in Society"),
 ("Markets and prices", "the double auction in the classroom", "Chamberlin (1948); Smith (1962)", r"Chamberlin('s market| \(?1948)"),
 ("Markets and prices", "zero-intelligence traders", "Gode and Sunder (1993)", r"Gode"),
 ("Markets and prices", "general equilibrium and its welfare theorems", "Arrow and Debreu (1954); Debreu (1959)", r"Arrow & Debreu"),
 ("Markets and prices", "consumer surplus", "Dupuit (1844)", r"Dupuit"),
 ("Choice", "revealed preference", "Samuelson (1938); Afriat (1967); Varian (1982)", r"Afriat"),
 ("Choice", "expected utility", "von Neumann and Morgenstern (1944)", r"von Neumann & Morgenstern"),
 ("Choice", "prospect theory", "Kahneman and Tversky (1979)", r"Kahneman & Tversky"),
 ("Choice", "present bias", "Laibson (1997)", r"Laibson 1997"),
 ("Firms", "why firms exist", "Coase (1937), \"The Nature of the Firm\"", r"Coase 1937|Nature of the Firm"),
 ("Firms", "organizations and markets", "Simon (1991)", r"Simon 1991|Simon \(1991\)|Organizations & Markets"),
 ("Firms", "incomplete contracts and ownership", "Grossman and Hart (1986)", r"Grossman & Hart"),
 ("Firms", "moral hazard and the principal", "Holmström (1979)", r"Holmstrom"),
 ("Strategy", "equilibrium in games", "Nash (1950, 1951)", r"Nash 1950"),
 ("Strategy", "oligopoly in quantities and prices", "Cournot (1838); Bertrand (1883)", r"Cournot"),
 ("Strategy", "demand estimation with differentiated products", "Berry, Levinsohn and Pakes (1995)", r"Berry, Levinsohn & Pakes"),
 ("Information and design", "lemons", "Akerlof (1970)", r"Akerlof 1970"),
 ("Information and design", "signalling", "Spence (1973)", r"Spence 1973"),
 ("Information and design", "screening in insurance", "Rothschild and Stiglitz (1976)", r"Rothschild & Stiglitz"),
 ("Information and design", "second-price auctions", "Vickrey (1961)", r"Vickrey \(?1961"),
 ("Information and design", "optimal auctions", "Myerson (1981)", r"Myerson 1981"),
 ("Information and design", "stable matching", "Gale and Shapley (1962)", r"Gale & Shapley"),
 ("Information and design", "Bayesian persuasion", "Kamenica and Gentzkow (2011)", r"Kamenica"),
 ("Information and design", "incentives that crowd out", "Gneezy and Rustichini (2000), \"A Fine Is a Price\"", r"Gneezy"),
 ("Welfare and the state", "externalities and their tax", "Pigou (1920)", r"Pigou"),
 ("Welfare and the state", "bargaining over externalities", "Coase (1960)", r"Coase 1960"),
 ("Welfare and the state", "public goods", "Samuelson (1954)", r"Samuelson 1954"),
 ("Welfare and the state", "governing the commons", "Ostrom (1990)", r"Ostrom"),
 ("Welfare and the state", "the impossibility of social choice", "Arrow (1951)", r"Arrow 1951"),
 ("Welfare and the state", "optimal income taxation", "Mirrlees (1971); Saez (2001)", r"Mirrlees"),
 ("Welfare and the state", "optimal commodity taxation", "Ramsey (1927); Diamond and Mirrlees (1971)", r"Ramsey 1927"),
 ("Growth", "the Malthusian economy", "Malthus (1798)", r"Malthus 1798|Malthusian|Thomas Malthus"),
 ("Growth", "the long run in numbers", "the Maddison Project (Bolt and van Zanden 2024)", r"Maddison"),
 ("Growth", "the neoclassical growth model", "Solow (1956); Ramsey (1928); Cass (1965)", r"Solow 1956"),
 ("Growth", "endogenous growth", "Romer (1990); Aghion and Howitt (1992)", r"Romer 1990"),
 ("Growth", "misallocation", "Hsieh and Klenow (2009)", r"Hsieh & Klenow"),
 ("Macroeconomics", "national accounts", "Kuznets (1934)", r"Kuznets \(?1934|1934 Simon Kuznets"),
 ("Macroeconomics", "the General Theory and IS-LM", "Keynes (1936); Hicks (1937)", r"Keynes 1936"),
 ("Macroeconomics", "the permanent income hypothesis", "Friedman (1957); Hall (1978)", r"Friedman 1957"),
 ("Macroeconomics", "the Phillips curve and the natural rate", "Phillips (1958); Friedman (1968); Phelps (1967)", r"Phillips 1958"),
 ("Macroeconomics", "the Lucas critique", "Lucas (1976)", r"Lucas 1976|Lucas critique"),
 ("Macroeconomics", "time inconsistency and rules", "Kydland and Prescott (1977)", r"Kydland & Prescott 1977"),
 ("Macroeconomics", "real business cycles", "Kydland and Prescott (1982)", r"Kydland & Prescott 1982"),
 ("Macroeconomics", "staggered prices", "Calvo (1983)", r"Calvo('s fairy| \(?1983)"),
 ("Macroeconomics", "the Taylor rule", "Taylor (1993)", r"Taylor 1993"),
 ("Macroeconomics", "search and unemployment", "Diamond (1982); Mortensen and Pissarides (1994)", r"Mortensen & Pissarides"),
 ("Macroeconomics", "heterogeneous agents", "Bewley (1977); Huggett (1993); Aiyagari (1994)", r"Aiyagari"),
 ("Macroeconomics", "the equity premium puzzle", "Mehra and Prescott (1985)", r"Mehra & Prescott"),
 ("Money and finance", "money as a medium of exchange", "Kiyotaki and Wright (1989)", r"Kiyotaki & Wright"),
 ("Money and finance", "bank runs", "Diamond and Dybvig (1983)", r"Diamond & Dybvig"),
 ("Money and finance", "debt deflation and financial instability", "Fisher (1933); Minsky (1986)", r"Minsky"),
 ("Money and finance", "the financial accelerator", "Bernanke, Gertler and Gilchrist (1999)", r"Bernanke, Gertler"),
 ("Money and finance", "forecasting by professionals", "the Survey of Professional Forecasters (Philadelphia Fed)", r"Professional Forecasters|SPF"),
 ("The world economy", "optimum currency areas and the trilemma", "Mundell (1961, 1963)", r"Mundell"),
 ("The world economy", "exchange-rate overshooting", "Dornbusch (1976)", r"Dornbusch 1976"),
 ("The world economy", "factor prices and trade", "Stolper and Samuelson (1941)", r"Stolper"),
 ("The world economy", "trade with increasing returns", "Krugman (1979, 1980)", r"Krugman 1979, 1980"),
 ("The world economy", "heterogeneous firms in trade", "Melitz (2003)", r"Melitz 2003"),
 ("The world economy", "gravity", "Anderson and van Wincoop (2003)", r"van Wincoop"),
 ("The world economy", "economic geography", "Krugman (1991)", r"Krugman 1991"),
 ("People", "human capital", "Becker (1964); Mincer (1974)", r"Becker \(?1964|Mincer"),
 ("People", "the minimum wage", "Card and Krueger (1994)", r"Card & Krueger"),
 ("People", "skills, tasks and technology", "Autor, Levy and Murnane (2003); Acemoglu and Autor (2011)", r"Autor, Levy & Murnane"),
 ("People", "mobility and place", "Chetty and others (2014)", r"Chetty et al\. 2014"),
 ("People", "top incomes", "Piketty and Saez (2003)", r"Piketty & Saez"),
 ("People", "the economics of crime", "Becker (1968)", r"Becker[^;]{0,12}1968"),
 ("Method", "positive economics", "Friedman (1953)", r"Friedman 1953|Methodology of Positive"),
 ("Method", "models as maps", "Rodrik (2015), *Economics Rules*", r"Rodrik[^;]{0,3}(2015|\*Economics Rules)|Economics Rules"),
 ("Method", "identification by instruments", "Wright (1928); Haavelmo (1944)", r"Haavelmo"),
 ("Method", "the credibility of econometrics", "Leamer (1983); LaLonde (1986)", r"LaLonde"),
 ("Method", "vector autoregressions", "Sims (1980)", r"Sims 1980"),
 ("Method", "dynamic discrete choice", "Rust (1987)", r"Rust 1987"),
 ("Method", "generalized method of moments", "Hansen (1982)", r"Hansen 1982"),
 ("Method", "machine learning for causal questions", "Chernozhukov and others (2018); Athey and Imbens (2019)", r"Chernozhukov"),
 ("Method", "publication bias in economics", "Brodeur and others (2016)", r"Brodeur"),
]

# What the series does not teach, said once so that nobody looks for it (README, "What it follows").
LEAVES_OUT = [
    ("Accounting and corporate finance", "The firm's books and its capital structure appear only where an economic "
     "argument needs them (the T-accounts of money and banks in Parts 25 and 26); there is no course in valuation or "
     "financial reporting."),
    ("Derivatives and financial engineering", "Asset pricing is taught as economics (Part 23: the stochastic discount "
     "factor and its puzzles); option pricing and the mathematics of hedging belong to *Quant, Built*."),
    ("The history of economic thought as a field", "Each idea arrives with its people, its year and its dead ends, "
     "but the series does not survey schools for their own sake. Marxian, Austrian, post-Keynesian, institutionalist "
     "and complexity arguments appear where they bear on a part's question, with their best case (SYLLABUS, section 1)."),
    ("Sector fields", "Agricultural, health, transport and energy economics are drawn on for examples (health "
     "insurance in Part 42, carbon in Part 48) but have no parts of their own."),
    ("Country studies", "The Data Room's countries are evidence, not subjects: no part is a course on one economy."),
]


def reference_cards() -> dict[int, tuple[list[str], list[str]]]:
    """Each built part's on-screen reference card: (books, papers), as TeX strings."""
    out = {}
    for n in built_parts():
        for f in sorted((HERE / f"econ{n}").glob("s*.py")):
            for node in ast.walk(ast.parse(f.read_text())):
                if isinstance(node, ast.Call) and getattr(node.func, "id", None) == "reference_card":
                    out[n] = (ast.literal_eval(node.args[0]), ast.literal_eval(node.args[1]))
    return out


def tex_to_md(s: str) -> str:
    s = re.sub(r"\\(emph|textit)\{([^}]*)\}", r"*\2*", s)
    for a, b in (("\\ ", " "), ("``", "\""), ("''", "\""), ("`", "'"), ("--", "–"), ("\\&", "&"), ("~", " ")):
        s = s.replace(a, b)
    accents = {"\"": "\u0308", "'": "\u0301", "`": "\u0300", "^": "\u0302", "~": "\u0303", "=": "\u0304", ".": "\u0307"}
    s = re.sub(r"\\([\"'`^~=.])\{?([A-Za-z])\}?", lambda m: unicodedata.normalize("NFC", m.group(2) + accents[m.group(1)]), s)
    s = re.sub(r"\\([cvu])\{([A-Za-z])\}",
               lambda m: unicodedata.normalize("NFC", m.group(2) + {"c": "\u0327", "v": "\u030c", "u": "\u0306"}[m.group(1)]), s)
    s = s.replace("{", "").replace("}", "").replace("$", "")
    return re.sub(r"\s+", " ", s).strip()


def short_parts(ps: list[int]) -> str:
    """[3, 4, 5, 7] -> '3–5, 7'; [] -> '·'."""
    if not ps:
        return "·"
    out, i = [], 0
    while i < len(ps):
        j = i
        while j + 1 < len(ps) and ps[j + 1] == ps[j] + 1:
            j += 1
        out.append(str(ps[i]) if j == i else f"{ps[i]}–{ps[j]}")
        i = j + 1
    return ", ".join(out)


def render() -> str:
    from explainer.economics import PARTS as TITLES

    built = built_parts()
    lines = [
        "# Economics, Built: textbooks, papers and models",
        "",
        "The series' reading in one place, written by `python -m videos.economics.reading` from",
        "[`reading.py`](reading.py), the syllabus and the parts themselves; `tests/economics/test_reading.py` fails when",
        "it is out of date. Section 1 is the textbook spine, tier by tier: the books an economics degree, a graduate",
        "core and the practice are taught from. Section 2 maps the field's classic papers and models to the parts that",
        "teach them. Section 3 is every built part's reference card, as it appears on screen, and section 4 says what",
        "the series leaves out.",
        "",
        "Both *Parts* columns are found, not typed. *Planned* lists the parts whose entry in",
        "[`SYLLABUS.md`](SYLLABUS.md) names the book or paper; *Built* lists the parts whose scenes, compute step or",
        "README cite it (a dot: none yet). Fuller notes (editions, chapters, what each source was used for) are in each",
        f"part's README, under *Sources*. Built so far: {'Part' if len(built) == 1 else 'Parts'} {short_parts(built)}.",
        "",
        "## 1. The textbook spine",
        "",
    ]
    tier = None
    for t, short, book, rx in SPINE:
        if t != tier:
            if tier is not None:
                lines.append("")
            lines += [f"### {t}", "", "| Short name | Book | Planned | Built |", "|---|---|---|---|"]
            tier = t
        lines.append(f"| {short} | {book} | {short_parts(planned_in(rx))} | {short_parts(cited_by(rx))} |")
    lines += ["", "## 2. Papers and models, and where they are taught", ""]
    area = None
    for a, model, paper, rx in PAPERS:
        if a != area:
            if area is not None:
                lines.append("")
            lines += [f"### {a}", "", "| Model or result | Paper | Planned | Built |", "|---|---|---|---|"]
            area = a
        lines.append(f"| {model} | {paper} | {short_parts(planned_in(rx))} | {short_parts(cited_by(rx))} |")
    lines += ["", "## 3. Every built part's reference card", ""]
    cards = reference_cards()
    for n in built:
        books, papers = cards[n]
        lines.append(f"**Part {n}, *{tex_to_md(TITLES[n])}*.** Books: " + "; ".join(tex_to_md(b) for b in books)
                     + ". Papers: " + "; ".join(tex_to_md(p) for p in papers) + ".")
        lines.append("")
    lines += ["## 4. What the series leaves out", ""]
    for what, why in LEAVES_OUT:
        lines.append(f"- **{what}.** {why}")
    return "\n".join(lines).rstrip() + "\n"


if __name__ == "__main__":
    (HERE / "READING.md").write_text(render())
    print("wrote", HERE / "READING.md")
