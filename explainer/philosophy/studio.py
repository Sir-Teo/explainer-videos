"""The scene toolkit of *Philosophy, Built*: ``from explainer.philosophy.studio import *`` in every scene.

It brings in manim, the AI series' visual instruments and lecture cards (``explainer.ai``: ``cmath``, ``morph``,
``axes``, ``definition_card``, ``theorem_card``, ``history_card``, ``pause_card``, ``objectives_card``,
``problem_set``, ``SearchTree``, ...) and the analysis series' text helpers (``label``, ``note``, ``ladder``, ``why``),
and adds what holds this series together:

* :data:`PARTS`, :data:`ACTS` and :func:`series_map`: forty-two parts in a prologue, seven acts and a finale;
* :func:`timeline` and :func:`chapter_card`: the strip from 600 BCE to 2030 (compressed before 1500), lit as the
  series reaches each idea;
* **the Wall** (:data:`WALL`, :func:`wall`, :func:`wall_card`): philosophy's impossibility theorems as bricks, one per
  part, laid as the parts are built;
* **the Price List** (:class:`PriceList`): an inconsistent set of plausible claims as a ring, and each minimal way
  out (computed by the Reasoner) as a position with its philosophers;
* :func:`payoff_card`: "where this comes back", by part number and name.

The logic instruments (truth tables, Fitch proofs, formula trees, argument maps) are in
:mod:`explainer.philosophy.logicviz`, exported here.
"""

from __future__ import annotations

import os
from types import SimpleNamespace

import numpy as np

from explainer.ai import *  # noqa: F401,F403
from explainer.ai import zh, data_text  # noqa: F401
from explainer.analysis import label, note, wrapped_label  # noqa: F401
from explainer.analysis import WIDE_TEX

# Transliterated Arabic, Sanskrit and Pali names (Ḥunayn, Ṛg Veda, ʿAlī) need letters pdflatex's T1 encoding lacks;
# xelatex (the Chinese renders, whose template was copied before this) sets them from the font directly.
_DOT_BELOW = {"1E24": "H", "1E62": "S", "1E6C": "T", "1E0C": "D", "1E92": "Z", "1E93": "z", "1E46": "N", "1E42": "M",
              "1E5A": "R", "1E36": "L", "1E5C": r"\=R", "1E5D": r"\=r", "1E38": r"\=L", "1E39": r"\=l"}
WIDE_TEX.add_to_preamble(
    r"\ifdefined\XeTeXrevision\else"
    + "".join(rf"\DeclareUnicodeCharacter{{{k}}}{{\d{{{v}}}}}" for k, v in _DOT_BELOW.items())
    + r"\DeclareUnicodeCharacter{02BF}{\textquoteleft}\DeclareUnicodeCharacter{02BE}{\textquoteright}"
    r"\DeclareUnicodeCharacter{1E2B}{\b{h}}\DeclareUnicodeCharacter{1E35}{\b{k}}\fi")

SERIES_EN = "Philosophy, Built"
SERIES_ZH = "哲学，从零搭建"

# ---------------------------------------------------------------------------
# Colour is meaning, for the whole series
# ---------------------------------------------------------------------------
P = SimpleNamespace(
    TRUE="#7BD389",       # true, satisfied, valid, kept
    FALSE="#FF6B6B",      # false, conflict, invalid, rejected
    CLAIM="#6FB7FF",      # a claim, a premise, an atom
    CONCL="#FFD166",      # a conclusion, a goal, the thing at stake
    RULE="#C3A6FF",       # rules of inference, operators, the machine's moves
    WORLD="#5EE6D0",      # worlds, models, valuations
    AGENT="#FF9F68",      # agents, people, voters
    HIST="#E8C07D",       # history: people and years
    WALL="#B5654A",       # the Wall: impossibility theorems
    PRICE="#F28EC2",      # the Price List: positions and what they give up
    DIM=GREY_D,
)
TRUE_C, FALSE_C = P.TRUE, P.FALSE
MONO = "DejaVu Sans Mono"

# ---------------------------------------------------------------------------
# The forty-two parts
# ---------------------------------------------------------------------------
ACTS = [
    (r"Prologue", (1, 1)),
    (r"I.\ The Machinery of Reason", (2, 5)),
    (r"II.\ The Limits of Reason", (6, 9)),
    (r"III.\ Knowledge", (10, 14)),
    (r"IV.\ Science", (15, 19)),
    (r"V.\ The World", (20, 26)),
    (r"VI.\ Mind and Meaning", (27, 32)),
    (r"VII.\ Value", (33, 40)),
    (r"Finale", (41, 42)),
]
PARTS = {
    1: r"Calculemus",
    2: r"The Laws of Thought", 3: r"All and Some", 4: r"Necessity and Possibility", 5: r"Beyond True and False",
    6: r"Paradise and Paradox", 7: r"The Limits of Proof", 8: r"The Liar", 9: r"What Is Mathematics About?",
    10: r"The Mind's Own Laws", 11: r"What Is Knowledge?", 12: r"Knowledge Among Many", 13: r"Degrees of Belief",
    14: r"Changing Your Mind",
    15: r"The Problem of Induction", 16: r"Evidence by Numbers", 17: r"Cause", 18: r"Theories and Reality",
    19: r"Life",
    20: r"What There Is", 21: r"Identity and Persistence", 22: r"Possible Worlds", 23: r"God and the Philosophers",
    24: r"Laws, Chance and the Arrow", 25: r"Space and Time", 26: r"The Quantum Puzzle",
    27: r"Sense and Reference", 28: r"Meaning in Use", 29: r"Being and Time-Consciousness", 30: r"Mind and Machine",
    31: r"Consciousness", 32: r"Free Will",
    33: r"Rational Choice", 34: r"Games and the Social Contract", 35: r"The Right and the Good",
    36: r"Weighing Lives", 37: r"Is and Ought", 38: r"Justice", 39: r"The Arithmetic of Democracy", 40: r"Beauty",
    41: r"Fair Machines", 42: r"Aligning Reasoners",
}


def act_of(part: int) -> int:
    for k, (_, (a, b)) in enumerate(ACTS):
        if a <= part <= b:
            return k
    raise KeyError(part)


def series_map(current: int | None = None, done: int = 0, font_size=17, width=13.4, height=7.4) -> VGroup:
    """The nine acts in a grid of three columns; each part a row. Parts up to ``done`` white, ``current`` lit and
    boxed, the rest dim."""
    cols = VGroup()
    for act, (a, b) in ACTS:
        head = label(act, font_size=font_size + 3, color=GREY_A)
        rows = VGroup()
        for p in range(a, b + 1):
            color = P.CONCL if p == current else (WHITE if p <= done else GREY_C)
            rows.add(label(rf"{p}.\ {PARTS[p]}", font_size=font_size, color=color))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.11)
        col = VGroup(head, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        col.head, col.rows = head, rows
        cols.add(col)
    # three columns: (Prologue, I, II), (III, IV, V), (VI, VII, Finale)
    columns = VGroup(VGroup(*cols[0:3]), VGroup(*cols[3:6]), VGroup(*cols[6:9]))
    for c in columns:
        c.arrange(DOWN, aligned_edge=LEFT, buff=0.32)
    columns.arrange(RIGHT, aligned_edge=UP, buff=0.55)
    if columns.width > width:
        columns.width = width
    if columns.height > height:
        columns.height = height
    g = VGroup(columns)
    g.cols = cols
    g.part = {}
    for col, (_, (a, b)) in zip(cols, ACTS):
        for p, row in zip(range(a, b + 1), col.rows):
            g.part[p] = row
    if current is not None:
        box = SurroundingRectangle(g.part[current], color=P.CONCL, buff=0.08, corner_radius=0.06, stroke_width=2)
        g.add(box)
        g.box = box
    return g.move_to(ORIGIN)


# ---------------------------------------------------------------------------
# The timeline strip: 600 BCE to 2030, compressed before 1500
# ---------------------------------------------------------------------------
# (year, what) for the whole series; a part lights the years its chapters reach.  Negative years are BCE.
TIMELINE = [
    (-585, r"Thales"), (-500, r"Heraclitus; Confucius"), (-480, r"the Buddha"), (-475, r"Parmenides"), (-450, r"Zeno's paradoxes"),
    (-400, r"Socrates; Mozi"), (-380, r"Plato: \textit{Meno}, \textit{Republic}"), (-369, r"Plato's \textit{Theaetetus}"), (-350, r"Aristotle's logic"), (-340, r"Eubulides: the heap; the liar"),
    (-300, r"Stoic logic; Zhuangzi"), (-280, r"the School of Names"), (-150, r"the \textit{Milindapañha}"), (150, r"Nāgārjuna; the \textit{Nyāya Sūtra}"), (263, r"Liu Hui on the \textit{Nine Chapters}"),
    (480, r"Dignāga"), (524, r"Boethius: \textit{The Consolation of Philosophy}"), (640, r"Dharmakīrti against a creator"), (770, r"Dharmottara's mirage"), (830, r"the House of Wisdom, Baghdad"), (950, r"al-Fārābī"), (1020, r"Avicenna: the floating man"), (1037, r"Avicenna; the Necessary Existent"), (984, r"Udayana: proofs of God"), (1180, r"Averroes"), (1078, r"Anselm"), (1095, r"al-Ghazālī"), (1240, r"D\={o}gen: `Being-Time' (\textit{Uji})"), (1270, r"Aquinas"),
    (1247, r"Qin Jiushao: remainders"), (1292, r"Mallisena: the seven predications"), (1305, r"Llull's \textit{Ars Magna}"), (1320, r"Ockham"), (1324, r"Bradwardine: \textit{insolubilia}"), (1572, r"Bombelli's \textit{Algebra}"), (1637, r"Descartes: \textit{La Géométrie}"), (1638, r"Galileo's paradox"), (1641, r"Descartes; \textit{Meditations}"), (1643, r"Elisabeth of Bohemia to Descartes"), (1651, r"Hobbes"), (1655, r"Hobbes: the ship of Theseus"), (1666, r"Leibniz: the art of combinations"),
    (1670, r"Pascal's \textit{Pensées}"), (1677, r"Spinoza's \textit{Ethics}"), (1679, r"Leibniz's characteristic"), (1685, r"\textit{Calculemus}"),
    (1686, r"Leibniz: \textit{Discourse on Metaphysics}"), (1687, r"Newton's \textit{Principia}: the bucket"), (1688, r"Molyneux's question"), (1689, r"Locke"), (1694, r"Locke on personal identity"), (1703, r"Leibniz on binary"), (1710, r"Berkeley's \textit{Principles}"), (1714, r"Leibniz's \textit{Monadology}"), (1715, r"the Leibniz--Clarke correspondence"), (1739, r"Hume's \textit{Treatise}"), (1748, r"Hume's \textit{Enquiry}"), (1763, r"Bayes"),
    (1768, r"Kant: incongruent counterparts"), (1779, r"Hume's \textit{Dialogues}"), (1781, r"Kant's \textit{Critique}"), (1783, r"Kant's \textit{Prolegomena}"), (1785, r"Condorcet; Reid's brave officer"), (1791, r"Bentham: the Panopticon"), (1802, r"Paley's \textit{Natural Theology}"), (1807, r"Hegel's \textit{Phenomenology}"), (1814, r"Laplace's demon"), (1823, r"Fresnel's reflection equations"), (1829, r"Lobachevsky: non-Euclidean geometry"), (1832, r"Bolyai: absolute geometry"), (1843, r"Mill's \textit{System of Logic}; Kierkegaard: \textit{Either/Or}"), (1847, r"De Morgan"), (1859, r"Darwin: \textit{On the Origin of Species}"), (1866, r"Venn: \textit{The Logic of Chance}"), (1851, r"Bolzano: paradoxes of the infinite"),
    (1854, r"Boole's \textit{Laws of Thought}; Riemann: the hypotheses of geometry"), (1867, r"Maxwell's demon"), (1872, r"Boltzmann: the $H$-theorem"), (1876, r"Loschmidt: reversibility"), (1877, r"Boltzmann: $S = k \log W$"), (1880, r"Peirce: nand"), (1882, r"Nietzsche: \textit{The Gay Science}"), (1883, r"Cantor's transfinite numbers"), (1874, r"Cantor; Brentano: intentionality"), (1879, r"Frege's \textit{Begriffsschrift}"),
    (1884, r"Frege's \textit{Grundlagen}"), (1889, r"Peano's axioms; Bertrand's chords"), (1888, r"Dedekind's axioms"), (1890, r"Poincaré: recurrence; James: the specious present"), (1891, r"Cantor's diagonal"), (1892, r"Frege: sense and reference"), (1895, r"Boltzmann: the fluctuation hypothesis"), (1896, r"James: `The Will to Believe'; Zermelo: recurrence"), (1899, r"Hilbert's \textit{Grundlagen der Geometrie}"), (1900, r"Husserl: \textit{Logical Investigations}"), (1902, r"Russell's paradox; Poincaré: \textit{Science and Hypothesis}"), (1903, r"Peirce: abduction"), (1904, r"Zermelo: well-ordering; Meinong"), (1905, r"Russell: descriptions; Einstein: special relativity; Husserl: lectures on time-consciousness"), (1906, r"Poincaré: the vicious circle; Duhem's holism"), (1907, r"Brouwer's thesis; Galton's ox"), (1909, r"Ritz and Einstein on radiation"), (1911, r"Nishida: \textit{An Inquiry into the Good}"), (1912, r"Lewis: strict implication"),
    (1908, r"Zermelo; Grelling--Nelson; Minkowski: spacetime; McTaggart: the unreality of time"), (1913, r"\textit{Principia}; Sheffer's stroke; Russell on cause; Einstein's hole argument; Husserl: \textit{Ideas I}"), (1920, r"Łukasiewicz: three values"), (1921, r"Post; the \textit{Tractatus}; Keynes on probability"),
    (1915, r"Löwenheim's theorem; Einstein: general relativity"), (1916, r"Leśniewski: mereology; Saussure: \textit{Course in General Linguistics}"), (1918, r"Weyl: \textit{Das Kontinuum}"), (1919, r"Eddington's eclipse"), (1925, r"Hilbert: `On the infinite'; Fisher's \textit{Statistical Methods}; Broad: emergence"), (1923, r"von Neumann's ordinals; Neyman's potential outcomes"), (1924, r"Banach--Tarski"), (1926, r"Ramsey on credence; Born: the probability rule"), (1927, r"Heidegger: \textit{Being and Time}; Russell: \textit{The Analysis of Matter}"), (1928, r"the \textit{Entscheidungsproblem}; Ramsey on laws; Reichenbach: \textit{The Philosophy of Space and Time}"), (1929, r"Gödel: completeness; Ramsey's test; the Vienna Circle; Szilard's engine; the Davos debate"), (1930, r"Heyting's logic; Zermelo's hierarchy"), (1931, r"Gödel: incompleteness"),
    (1932, r"von Neumann: \textit{Mathematical Foundations of Quantum Mechanics}"), (1933, r"Tarski on truth; Kolmogorov's axioms; Neyman--Pearson"), (1934, r"Skolem: nonstandard numbers; Popper's \textit{Logik}"), (1935, r"Gentzen; EPR; Schrödinger's cat"), (1936, r"Turing; Church; Tarski; quantum logic"), (1937, r"de Finetti: coherence"), (1938, r"Kleene; Bochvar; Gödel's $L$; Reichenbach's vindication"), (1939, r"Moore: `here is one hand'; Jeffreys; Ville's martingales"), (1941, r"Post's lattice"), (1942, r"Curry's paradox; Mayr: species"),
    (1943, r"Sartre: \textit{Being and Nothingness}"), (1944, r"von Neumann--Morgenstern; Onsager's Ising solution; Schrödinger: \textit{What Is Life?}"), (1945, r"Hempel's ravens; Wald's sequential test; Merleau-Ponty: \textit{Phenomenology of Perception}"), (1946, r"Barcan: quantified modal logic"), (1947, r"Gödel on the continuum; Horkheimer--Adorno: \textit{Dialectic of Enlightenment}"), (1948, r"Quine: `On What There Is'; Hempel--Oppenheim"), (1949, r"Jaspers: the Axial Age; Church on Ayer; Gödel's rotating universe; Beauvoir: \textit{The Second Sex}; Ryle: \textit{The Concept of Mind}"), (1950, r"Turing's test; Brier's score; Carnap's \textit{Foundations}; Strawson: `On Referring'"), (1952, r"Black's spheres; Bohm: hidden variables"), (1951, r"Arrow; Quine's dogmas; von Wright; Simpson's paradox; Goodman"),
    (1953, r"the \textit{Investigations}; Rudner on values; the double helix; Williams: tropes; Quine: three grades"), (1954, r"Thomson's lamp; Harris: distributional structure"), (1955, r"Goodman's grue; Beth's tableaux; Löb; Mackie: evil and omnipotence"), (1956, r"Reichenbach: the common cause; Popper: the arrow of radiation; Place: the identity theory"), (1957, r"Prior: tense logic; Jaynes: maximum entropy; Lindley's paradox; Everett: relative states; Firth: `the company it keeps'; Grice: `Meaning'"), (1958, r"Curry--Feys: propositions as types"), (1959, r"Kripke semantics; Kac's ring; Smart: sensations and brain processes"), (1960, r"Davis--Putnam; Quine: \textit{Word and Object}; Gadamer: \textit{Truth and Method}; MacKay: self-prediction"), (1961, r"Lucas: minds and machines; Kyburg's lottery; Nagel: reduction; Landauer: erasure costs heat; Wigner's friend"),
    (1962, r"Kuhn; Radó: busy beavers; Hintikka; Blackwell--Dubins; Birnbaum; Wynne-Edwards; Geach: donkey sentences; Austin: \textit{How to Do Things with Words}; P. F. Strawson: `Freedom and Resentment'"), (1963, r"Gettier; Cohen's forcing; Fitch; Putnam's diagonal; Lorenz: deterministic chaos"), (1964, r"Bell's theorem; Lawvere's ETCS; Solomonoff; Hamilton's rule"), (1965, r"Robinson: resolution; Zadeh: fuzzy sets; Jeffrey's \textit{Logic of Decision}; Dreyfus: `Alchemy and AI'"), (1966, r"von Neumann: self-reproducing automata; Hick: soul-making; Rietdijk: relativity against the open future; Donnellan: referential and attributive"), (1967, r"Gold: learning in the limit; Putnam: multiple realizability; Geach: relative identity; Prior: branching time; Putnam: time and physical geometry; Kochen--Specker; Davidson: `Truth and Meaning'; Derrida: \textit{Of Grammatology}"), (1968, r"Tseitin's encoding; Stalnaker's conditionals; Lewis: counterparts"),
    (1969, r"Lewis: \textit{Convention}; Lindström; Hoare; Armitage on repeated tests; CHSH; Searle: \textit{Speech Acts}; McCarthy--Hayes: the frame problem; Frankfurt: alternate possibilities; Nozick: Newcomb's problem"), (1970, r"Kripke: naming; Suppes on causality; Lakatos; Lewontin; Price; Conway's Life; Montague: `English as a Formal Language'"), (1971, r"Rawls; Cook; Salmon: relevance; Parfit: personal identity; Kripke; Frankfurt: freedom of the will"), (1972, r"Routley--Meyer semantics; Horn: scales; Dreyfus: \textit{What Computers Can't Do}"),
    (1973, r"Lewis: counterfactuals; Benacerraf; Akaike; Maynard Smith--Price; Wright: functions; Bennett: reversible computation; Evans: Madagascar; Davidson: radical interpretation"), (1974, r"Nagel's bat; Chaitin; Miller and Tichý; Rubin; Ghiselin: species as individuals; Plantinga: \textit{The Nature of Necessity}; Kirk: zombies"), (1975, r"Kripke on truth; Goldblatt--Thomason; Fine; Putnam: no miracles; Cummins: functions; Gibbard: Lumpl; Putnam: Twin Earth; Grice: `Logic and Conversation'; Foucault: \textit{Discipline and Punish}; Fodor: \textit{The Language of Thought}"), (1976, r"Lewis's triviality; Aumann; van Benthem; Lakatos; Dawkins; Lewis: survival; Lewis: the paradoxes of time travel; Foster's problem; Williams--Nagel: moral luck"),
    (1977, r"Pnueli; Belnap; Paris--Harrington; Laudan; Dretske and Tooley: laws as relations; Malament: simultaneity from causality; Kaplan: `Demonstratives'"), (1978, r"Rissanen: MDL; BACON; Taylor--Jonker: replicator dynamics; Armstrong: universals; Evans: vague identity; Stalnaker: assertion; Block: the China brain"), (1979, r"Priest: the logic of paradox; Goldman: reliabilism; Doyle: truth maintenance; the spandrels; Kripke: a puzzle about belief; Rowe: evil and atheism; Craig: the kalām; Penrose: the Weyl curvature hypothesis; Burge: arthritis"),
    (1980, r"the Chinese room; Putnam on models; Field; Lewis: the Principal Principle; Reiter: defaults; Axelrod's tournament; Unger and Geach: the many"), (1981, r"model checking; Nozick: tracking; Laudan; Kitcher; Barwise--Cooper: generalized quantifiers; Kamp: discourse representation; Habermas: \textit{The Theory of Communicative Action}; Block: Blockhead; Churchland: eliminativism; Dretske: information"), (1982, r"Kirby--Paris: Goodstein; Byzantine generals; Bennett: the demon exorcised; Fredkin--Toffoli: conservative logic; Aspect's Bell tests; Kripke: \textit{Wittgenstein on Rules and Private Language}; Jackson: Mary's room"), (1983, r"Wright: Frege's theorem; Carter: Doomsday; Hacking; Cartwright; van Inwagen: the PSR collapses; Armstrong: \textit{What Is a Law of Nature?}; Levine: the explanatory gap; van Inwagen: the consequence argument; Libet: the readiness potential"), (1984, r"Parfit; Salmon: causal processes; Sober; Millikan; Boolos: plurals; Wykstra: CORNEA; Kim: supervenience"), (1985, r"AGM; Haken; FLP; McGee"), (1986, r"Lewis: worlds; Gärdenfors's impossibility; Salmon: \textit{Frege's Puzzle}; Earman: \textit{A Primer on Determinism}; GRW: spontaneous collapse; Keenan--Stavi: conservativity; Rosenthal: higher-order thought"), (1987, r"Girard: linear logic; the Sendai subway; Simons: \textit{Parts}; Johnston: adverbialism; Gödel's proof published; Hacking: the inverse gambler; Earman and Norton: the hole argument"), (1988, r"Pearl: Bayesian networks; Grove; Spohn; Lewis on Evans; Fodor--Pylyshyn: systematicity; Baars: the global workspace"), (1989, r"Martin--Steel: determinacy; the email game; Worrall; Armstrong: combinatorialism; van Fraassen: \textit{Laws and Symmetry}; GHZ; Crimmins--Perry: hidden indexicals"), (1990, r"Etchemendy on consequence; Halpern--Moses; KLM; van Inwagen: \textit{Material Beings}; Peres--Mermin: the magic square; Harnad: the symbol grounding problem"), (1991, r"Lewis: \textit{Parts of Classes}; Schmidt-Schauß--Smolka; Alston: \textit{Perceiving God}; Deutsch: closed timelike curves; Groenendijk--Stokhof: dynamic predicate logic; Reiter: successor-state axioms; Varela--Thompson--Rosch: \textit{The Embodied Mind}"), (1992, r"Yablo: mental causation"), (1993, r"Yablo; Gupta--Belnap; Spirtes--Glymour--Scheines; Lewis: many, but almost one; Yablo on conceivability"), (1994, r"the Pentium bug; Williamson: \textit{Vagueness}; twin networks; Joyce: NASA's definition of life; Fine: essence and modality; Martin: dispositions and conditionals; Lewis: Humean supervenience debugged; Hall: the New Principle; Brandom: \textit{Making It Explicit}; G. Strawson: the basic argument"),
    (1995, r"the hard problem; Dung's argumentation; the do-calculus; Sato: distribution semantics; Maudlin: three measurement problems"), (1996, r"CDCL solvers; Lewis: `Elusive Knowledge'; Wolpert: no free lunch; Rovelli: relational quantum mechanics; FraCaS; Varela: neurophenomenology; Chalmers: \textit{The Conscious Mind}; Kane: \textit{The Significance of Free Will}; McKay--Johnson: rule beta"), (1997, r"Shapiro; Resnik: structuralism; Olson: animalism; Nolan: impossible worlds; Lewis: finkish dispositions; Maldacena: holography"), (1998, r"Joyce: accuracy; Kim: exclusion; Heim--Kratzer: \textit{Semantics in Generative Grammar}; Clark--Chalmers: the extended mind; Fischer--Ravizza: reasons-responsiveness"), (1999, r"Barbour: \textit{The End of Time}"), (2000, r"Pearl's \textit{Causality}; Williamson: knowledge first; Sleeping Beauty; Maynard Smith: information; White: fine-tuning; Earman: Hume's abject failure; Albert: \textit{Time and Chance}"), (2001, r"experimental philosophy; Sider; Fine; the semantic web; Noveck: children and `some'"), (2002, r"Batterman: \textit{The Devil in the Details}; OntoClean; Gendler--Hawthorne: conceivability; QBism"), (2003, r"Woodward: \textit{Making Things Happen}; Schaffer: a fundamental level?; Hájek: Pascal's wager; Norton's dome; Schlenker: a plea for monsters"), (2004, r"Magnus--Callender: the base rate; Tononi: integrated information; Matthias: the responsibility gap"), (2005, r"Baker: the cicadas; Ioannidis; Halpern--Pearl"), (2006, r"Beall--Restall: pluralism; Shpitser--Pearl; Nowak: five rules; Saunders: weak discernibility; Chalmers: two dimensions; Conway and Kochen: the free will theorem"), (2007, r"Zollman's networks; Kelly's razor; Hájek: reference classes; Bird: \textit{Nature's Metaphysics}; Maudlin: \textit{The Metaphysics Within Physics}"), (2008, r"Schurz: meta-induction; Sandberg--Bostrom: emulation"), (2009, r"Douglas: values in science; OWL 2"), (2010, r"Nowak--Tarnita--Wilson; Schaffer: monism; Rosen; Skyrms: \textit{Signals}; Friston: free energy"), (2011, r"`False-Positive Psychology'; Bem; Sider: structure"), (2012, r"Hamkins: the multiverse; the Knowledge Graph; Bérut et al.: Landauer's bound measured; PBR; Wallace: \textit{The Emergent Multiverse}; Frank--Goodman: rational speech acts; the Cambridge Declaration on Consciousness; Schurger--Sitt--Dehaene: the stochastic accumulator"), (2013, r"the HoTT book; CUPED; Weisberg; Dawid; TransE; Williamson: necessitism; Maldacena and Susskind: ER = EPR; word2vec"), (2014, r"Aaronson: an objection to IIT"), (2015, r"the Reproducibility Project; Halpern: actual causation; loophole-free Bell tests"),
    (2017, r"Leitgeb: stable belief; Wachter et al.: counterfactual explanations"), (2016, r"Pythagorean triples; fairness theorems; the ASA on $p$-values; Gödel's proof machine-checked"), (2018, r"Mayo: severe testing; \textit{The Book of Why}; Frauchiger--Renner; SCAN; Spider: text to SQL; Shea: \textit{Representation in Cognitive Science}; Chalmers: the meta-problem"), (2019, r"Shafer--Vovk: testing by betting; Chan: Lenia; Berto--Jago: impossible worlds; MED: monotonicity"), (2020, r"PhilPapers survey; Bender--Koller: the octopus"), (2021, r"AlphaFold 2"), (2022, r"the Liquid Tensor Experiment; Nobel prize for Bell tests; Piantadosi--Hill: meaning without reference"), (2023, r"Othello-GPT; the reversal curse; Mollo--Millière: vector grounding; Butlin, Long et al.: indicators of consciousness in AI"), (2024, r"machine-checked BB(5); the New York Declaration on Animal Consciousness"),
    (2025, r"Cogitate: IIT and the global workspace tested"), (2026, r"this series"),
]
_BREAKS = [(-600, 0.0), (0, 0.17), (1500, 0.30), (1900, 0.58), (2030, 1.0)]


def _tx(year: float, width: float) -> float:
    for (y0, f0), (y1, f1) in zip(_BREAKS, _BREAKS[1:]):
        if year <= y1:
            return -width / 2 + width * (f0 + (f1 - f0) * (year - y0) / (y1 - y0))
    return width / 2


def year_tex(y: int) -> str:
    """A year as text: 380 BCE for -380 (translated in the Chinese build by the table's patterns)."""
    return rf"{-y}\ BCE" if y < 0 else str(y)


def timeline(lit=(), width=12.6, show_labels=True, font_size=17) -> VGroup:
    """The strip from 600 BCE to 2030 (the axis is compressed before 1500, marked by breaks); years in ``lit`` glow
    and get their names."""
    g = VGroup()
    segs = [(-600, 1500), (1500, 2030)]
    for a, b in segs:
        g.add(Line([_tx(a, width), 0, 0], [_tx(b, width), 0, 0], color=GREY_D, stroke_width=2))
    for yr in (1500,):  # the scale changes: two little slashes
        x = _tx(yr, width)
        for dx in (-0.05, 0.05):
            g.add(Line([x + dx - 0.04, -0.09, 0], [x + dx + 0.04, 0.09, 0], color=GREY_C, stroke_width=1.5))
    for yr in (-500, 0, 1000, 1700, 1800, 1900, 1950, 2000):
        x = _tx(yr, width)
        g.add(Line([x, -0.06, 0], [x, 0.06, 0], color=GREY_D, stroke_width=1.5))
        g.add(label(year_tex(yr) if yr else r"0", font_size=13, color=GREY_D).next_to([x, 0, 0], DOWN, buff=0.12))
    labels, anchors = VGroup(), []
    side = 1
    for yr, name in TIMELINE:
        on = yr in lit
        d = Dot([_tx(yr, width), 0, 0], radius=0.06 if on else 0.032, color=P.HIST if on else GREY_C)
        g.add(d)
        if on and show_labels:
            t = label(rf"{year_tex(yr)}\; {name}", font_size=font_size, color=P.HIST)
            t.next_to(d, UP if side > 0 else DOWN, buff=0.14 if side > 0 else 0.4)
            side = -side
            labels.add(t)
            anchors.append(d)
    for row in (1, -1):
        same = sorted([t for t in labels if np.sign(t.get_y()) == row], key=lambda t: t.get_x())
        for a, b in zip(same, same[1:]):
            gap = b.get_left()[0] - a.get_right()[0]
            if gap < 0.2:
                b.shift(RIGHT * (0.2 - gap))
        if same and same[-1].get_right()[0] > 6.9:
            same[-1].shift(LEFT * (same[-1].get_right()[0] - 6.9))
            for i in range(len(same) - 2, -1, -1):
                gap = same[i + 1].get_left()[0] - same[i].get_right()[0]
                if gap < 0.2:
                    same[i].shift(LEFT * (0.2 - gap))
        if same and same[0].get_left()[0] < -6.9:
            same[0].shift(RIGHT * (-6.9 - same[0].get_left()[0]))
    leaders = VGroup()
    for t, d in zip(labels, anchors):
        if abs(t.get_x() - d.get_x()) > 0.1:
            above = t.get_y() > 0
            leaders.add(Line(d.get_top() if above else d.get_bottom(), t.get_bottom() if above else t.get_top(),
                             color=P.HIST, stroke_width=1, stroke_opacity=0.4))
    g.add(leaders, labels)
    g.labels, g.leaders = labels, leaders
    return g


def chapter_card(number, title: str, question: str = "", lit=(), part: int | None = None) -> VGroup:
    """Chapter title, the question it answers, and the timeline strip with this chapter's years lit."""
    if zh():
        head_text = (rf"第{part}部分 \textperiodcentered\ " if part else "") + f"第{number}章"
    else:
        head_text = (rf"Part {part} \textperiodcentered\ " if part else "") + f"Chapter {number}"
    head = label(head_text, font_size=28, color=GREY_B)
    t = label(title, font_size=52)
    g = VGroup(head, t)
    if question:
        g.add(wrapped_label(question, 12.0, 30, GREY_A))
    g.arrange(DOWN, buff=0.3).shift(UP * 0.6)
    strip = timeline(lit=lit).to_edge(DOWN, buff=0.9)
    return VGroup(g, strip)


def part_title(part: int) -> VGroup:
    """The opening title of a part: series name, part number, part name, act."""
    act = ACTS[act_of(part)][0]
    s = label(SERIES_ZH if zh() else SERIES_EN, font_size=30, color=GREY_B)
    n = label((rf"第{part}部分" if zh() else rf"Part {part}"), font_size=34, color=P.CONCL)
    t = label(PARTS[part], font_size=64)
    a = label(act, font_size=26, color=GREY_A)
    return VGroup(s, n, t, a).arrange(DOWN, buff=0.3)


# ---------------------------------------------------------------------------
# The Wall: one impossibility theorem per part
# ---------------------------------------------------------------------------
# part: (brick label, the dream, the wall, year, what it forces)
WALL = {
    1: (r"Zeno", r"motion and change described by reason alone",
        r"Zeno's paradoxes; Meno's paradox of inquiry", -450,
        r"an account of the infinite, and an account of inquiry"),
    2: (r"Cook--Levin", r"decide any argument by calculation",
        r"SAT is NP-complete; resolution needs exponential proofs (Haken)", 1971,
        r"calculation is possible, but it can cost more than the universe can pay"),
    3: (r"Church--Turing", r"decide validity in full logic", r"first-order validity is undecidable", 1936,
        r"proof search that may never end"),
    4: (r"Goldblatt--Thomason", r"one logic of necessity read off the frames",
        r"some modal axioms have no first-order frame condition", 1975, r"modal logic is not just first-order logic"),
    5: (r"Sorites", r"sharp concepts for a vague world", r"the sorites: tolerance + bivalence + classical logic",
        -350, r"a sharp cutoff, a gap, or a new logic"),
    6: (r"Russell; Cohen", r"every collection is a set; every question about sets has an answer",
        r"Russell's paradox; the independence of CH", 1963, r"axioms chosen, not read off"),
    7: (r"Gödel", r"a complete, consistent theory of arithmetic that proves its own consistency",
        r"the incompleteness theorems; the halting problem; Tarski; Löb", 1931,
        r"truth outruns proof"),
    8: (r"The liar", r"a language that contains its own truth predicate",
        r"the liar and its revenge", 1975, r"a gap, a glut, or a hierarchy"),
    9: (r"Benacerraf", r"know mathematical objects as we know tables",
        r"Benacerraf's dilemmas: access and identification", 1973, r"structure, fiction, or a special faculty"),
    10: (r"Hume; Kant", r"necessary knowledge from experience", r"Hume's problem; Kant's antinomies", 1739,
         r"the mind's own contribution, or skepticism"),
    11: (r"Gettier", r"knowledge = justified true belief + X",
         r"Gettier cases; anti-luminosity (Williamson)", 1963, r"knowledge may be unanalyzable"),
    12: (r"Coordinated attack", r"common knowledge by messages",
         r"no common knowledge over unreliable channels (Halpern--Moses)", 1990, r"act without certainty"),
    13: (r"Bertrand", r"one rational prior from ignorance", r"Bertrand's paradox", 1889,
         r"priors are choices"),
    14: (r"Lewis triviality", r"conditionals as propositions with probability $P(C \mid A)$",
         r"Lewis's triviality; Gärdenfors's impossibility", 1976, r"conditionals may not state facts"),
    15: (r"No free lunch", r"induction justified without assumptions",
         r"Hume; grue; no free lunch (Wolpert); Gold's theorem", 1996, r"every learner bets on a world"),
    16: (r"Birnbaum", r"error control and evidential meaning together",
         r"Birnbaum: sufficiency + conditionality give the likelihood principle", 1962, r"choose your principle"),
    17: (r"Markov equivalence", r"causes read off correlations",
         r"Verma and Pearl: \ observationally equivalent causal graphs", 1990, r"intervene, or assume"),
    18: (r"Underdetermination", r"evidence fixes theory", r"underdetermination; the pessimistic meta-induction",
         1981, r"realism has a price"),
    19: (r"Levels of selection", r"one level at which selection acts", r"the Price equation splits any level",
         1970, r"pluralism about units"),
    20: (r"Composition", r"a principled answer to when parts make a whole",
         r"the special composition question", 1990, r"nihilism, universalism, or vagueness"),
    21: (r"Fission", r"identity is what matters in survival", r"fission and the transitivity of identity",
         1971, r"identity is not what matters"),
    22: (r"Necessary a posteriori", r"conceivability as a guide to possibility",
         r"Kripke's necessary a posteriori", 1970, r"two dimensions of meaning, or none"),
    23: (r"Modal collapse", r"a proof of God from possibility", r"modal collapse in Gödel's proof",
         1987, r"everything true is necessary"),
    24: (r"Loschmidt", r"the arrow of time from the laws", r"reversibility and recurrence objections",
         1876, r"a special beginning"),
    25: (r"Hole argument", r"spacetime points as real things in a deterministic theory",
         r"the hole argument (Einstein; Earman--Norton)", 1987, r"sophisticated substantivalism or relationalism"),
    26: (r"Bell; Kochen--Specker", r"local, non-contextual hidden values",
         r"Bell's theorem; Kochen--Specker", 1964, r"non-locality, many worlds, or no values"),
    27: (r"Frege's puzzle", r"meaning is reference", r"Frege's puzzle; Kripke's modal argument", 1892,
         r"senses, or Russellian meanings with a price"),
    28: (r"Kripkenstein", r"a fact that fixes what a rule means", r"the rule-following paradox", 1982,
         r"meaning in community and use"),
    29: (r"Frame problem", r"relevance by rule", r"the frame problem", 1969, r"background know-how"),
    30: (r"Causal exclusion", r"a mind that is both physical and causally its own",
         r"Kim's exclusion argument", 1998, r"reduce, overdetermine, or epiphenomenalize"),
    31: (r"Hard problem", r"consciousness entailed by physical truths", r"the hard problem; the explanatory gap",
         1995, r"new properties, new concepts, or illusion"),
    32: (r"Consequence argument", r"freedom and determinism together",
         r"the consequence argument; Frankfurt cases", 1983, r"redefine freedom, or deny determinism"),
    33: (r"Allais; Newcomb", r"one theory of rational choice", r"Allais, Ellsberg and Newcomb", 1953,
         r"EU, its rivals, or two theories"),
    34: (r"Prisoner's dilemma", r"individual rationality is collectively rational",
         r"the prisoner's dilemma; backward induction", 1950, r"institutions and repeated games"),
    35: (r"Paradox of deontology", r"a theory that matches every moral intuition",
         r"Harsanyi's theorem; the paradox of deontology", 1955, r"some intuition must go"),
    36: (r"Arrhenius", r"an axiology for populations that meets every adequacy condition",
         r"Arrhenius's impossibility theorems", 2000, r"accept a repugnant-seeming conclusion"),
    37: (r"Hume's law", r"ought from is", r"Schurz's is--ought theorem; Frege--Geach", 1997,
         r"bridge principles, or a non-factual ought"),
    38: (r"Sen", r"liberty and Pareto together", r"the impossibility of a Paretian liberal", 1970,
         r"rights constrain welfare"),
    39: (r"Arrow", r"a fair way to add up preferences", r"Arrow; Gibbard--Satterthwaite; List--Pettit", 1951,
         r"restrict the domain, use intensities, or accept manipulation"),
    40: (r"Taste", r"a rule for beauty", r"Hume's paradox of taste", 1757, r"trained judges, not rules"),
    41: (r"Kleinberg--Chouldechova", r"a classifier fair by every measure",
         r"calibration and balance are incompatible with unequal base rates", 2016, r"choose which fairness"),
    42: (r"Löb; no free lunch for values", r"specify what we want, then optimize",
         r"Goodhart; no free lunch for preferences; the Löbian obstacle", 2018, r"judgment that stays in the loop"),
}


def wall(upto: int, current: int | None = None, cols: int = 7, brick_w: float = 1.8, brick_h: float = 0.7,
         font_size=17) -> VGroup:
    """The Wall as bricks laid in running bond, six courses of seven, one brick per part: laid (with its theorem's
    name) for parts up to ``upto``, a faint outline for the rest, and ``current`` glowing. Course 0 is at the
    bottom, so the wall rises as the series goes on. Returns a VGroup with ``.brick[part]``."""
    g = VGroup()
    g.brick = {}
    for p in range(1, 43):
        row, col = divmod(p - 1, cols)
        x = (col - (cols - 1) / 2) * (brick_w + 0.06) + (0.5 * (brick_w + 0.06) if row % 2 else 0.0)
        y = row * (brick_h + 0.06)
        laid = p <= upto
        r = Rectangle(width=brick_w, height=brick_h, stroke_color=P.WALL if laid else GREY_D,
                      stroke_width=1.5, fill_color=P.WALL, fill_opacity=(0.85 if p == current else 0.45) if laid else 0)
        r.move_to([x, y, 0])
        b = VGroup(r)
        if laid:
            t = label(WALL[p][0], font_size=font_size, color=WHITE)
            if t.width > brick_w - 0.14:
                t.width = brick_w - 0.14
            b.add(t.move_to(r))
        else:
            b.add(label(str(p), font_size=font_size - 2, color=GREY_D).move_to(r))
        if p == current:
            b.add(SurroundingRectangle(r, buff=0.04, color=P.CONCL, stroke_width=3))
        g.brick[p] = b
        g.add(b)
    return g.move_to(ORIGIN)


def wall_card(part: int, width=9.6, font_size=24) -> VGroup:
    """This part's brick, close up: the dream, the theorem that stops it, the year, and what it forces."""
    name, dream, thm, year, price = WALL[part]
    head = VGroup(label(r"The Wall", font_size=font_size - 2, color=P.WALL),
                  label(name, font_size=font_size + 10, color=WHITE)).arrange(RIGHT, buff=0.35, aligned_edge=DOWN)
    rows = VGroup()
    for k, v, c in ((r"the dream", dream, P.CLAIM), (r"the wall", rf"{thm} ({year_tex(year)})", P.WALL),
                    (r"what it forces", price, P.PRICE)):
        rows.add(VGroup(label(k, font_size=font_size - 4, color=c), wrapped_label(v, width - 3.4, font_size, WHITE)))
    for r in rows:
        r[0].align_to(ORIGIN, LEFT)
        r[1].next_to(ORIGIN, RIGHT, buff=2.6)
        r[1].align_to(r[0], UP)
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
    inner = VGroup(head, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
    box = RoundedRectangle(width=max(width, inner.width + 0.6), height=inner.height + 0.6, corner_radius=0.14,
                           stroke_color=P.WALL, stroke_width=2, fill_color="#0B0F17", fill_opacity=0.95)
    inner.move_to(box)
    return VGroup(box, inner)


# ---------------------------------------------------------------------------
# The Price List
# ---------------------------------------------------------------------------
class PriceList(VGroup):
    """An inconsistent set of plausible claims as a ring of cards, and the positions that escape it.

    ``claims``: [(key, text)], in ring order. Build with the Reasoner's ``mus_mcs`` result: ``self.mus`` is drawn as
    red chords between the claims of each minimal inconsistent set (``self.conflict``); :meth:`position` returns the
    animations that light one minimal correction set: its claims are struck through and dimmed, the rest glow, and a
    centre card names the position, its holders, and (optionally) a survey share as a bar.

        pl = PriceList(claims, radius=2.6)
        self.play(FadeIn(pl.cards))
        self.play(Create(pl.conflict))
        anims, centre = pl.position(("good",), r"Free-will theodicy", r"Plantinga 1974", share=None)
    """

    def __init__(self, claims, mus=(), radius=2.9, width=3.9, font_size=25, center=ORIGIN, title: str | None = None,
                 squash=0.8):
        super().__init__()
        self.keys = [k for k, _ in claims]
        n = len(claims)
        self.center_pt = np.asarray(center, float)
        self.cards = VGroup()
        self.card = {}
        for i, (k, text) in enumerate(claims):
            ang = PI / 2 - TAU * i / n
            pos = self.center_pt + np.array([radius * 1.45 * np.cos(ang), radius * squash * np.sin(ang), 0])
            t = wrapped_label(text, width - 0.35, font_size, WHITE)
            box = RoundedRectangle(width=max(t.width + 0.35, 1.6), height=t.height + 0.3, corner_radius=0.12,
                                   stroke_color=P.CLAIM, stroke_width=2, fill_color="#0B0F17", fill_opacity=0.95)
            c = VGroup(box, t.move_to(box)).move_to(pos)
            c.box, c.text = box, t
            self.card[k] = c
            self.cards.add(c)
        self.conflict = VGroup()
        for S in mus:
            idx = sorted(self.keys.index(k) for k in S)   # ring order: a convex polygon, not a bow tie
            pts = [self.card[self.keys[i]].get_center() for i in idx]
            if len(pts) >= 2:
                poly = Polygon(*pts, stroke_color=P.FALSE, stroke_width=3, fill_opacity=0) if len(pts) > 2 else \
                    Line(*pts, color=P.FALSE, stroke_width=3)
                self.conflict.add(poly)
        self.add(self.conflict, self.cards)
        self.conflict.set_z_index(-1)
        self.title = None
        if title:
            self.title = label(title, font_size=34, color=P.PRICE).to_edge(UP, buff=0.3)
            self.add(self.title)
        self._marks = VGroup()

    def position(self, mcs, name: str, holders: str = "", share: float | None = None, share_note: str = "",
                 width=4.6):
        """Animations that show one position (the claims in ``mcs`` given up), and the centre card (already
        placed). Undo with :meth:`reset`."""
        anims = []
        marks = VGroup()
        for k in self.keys:
            c = self.card[k]
            if k in mcs:
                x = VGroup(Line(c.box.get_corner(UL), c.box.get_corner(DR), color=P.FALSE, stroke_width=4),
                           Line(c.box.get_corner(DL), c.box.get_corner(UR), color=P.FALSE, stroke_width=4))
                marks.add(x)
                anims += [c.animate.set_opacity(0.35), Create(x)]
            else:
                anims += [c.box.animate.set_stroke(P.TRUE, width=3)]
        body = VGroup(label(name, font_size=28, color=P.PRICE))
        if holders:
            body.add(wrapped_label(holders, width, 20, GREY_A))
        if share is not None:
            bar_bg = Rectangle(width=width * 0.8, height=0.18, stroke_width=1, stroke_color=GREY_C, fill_opacity=0)
            bar = Rectangle(width=max(width * 0.8 * share, 0.02), height=0.18, stroke_width=0, fill_color=P.PRICE,
                            fill_opacity=0.9)
            bar.align_to(bar_bg, LEFT)
            pct = label(rf"{round(100 * share)}\%", font_size=20, color=P.PRICE)
            sb = VGroup(VGroup(bar_bg, bar), pct).arrange(RIGHT, buff=0.15)
            body.add(sb)
            if share_note:
                body.add(note(share_note, font_size=16))
        body.arrange(DOWN, buff=0.14).move_to(self.center_pt)
        self._marks = marks
        self._centre = body
        anims.append(FadeIn(body, scale=0.9))
        return anims, body

    def reset(self):
        anims = [FadeOut(self._marks), FadeOut(self._centre)]
        for k in self.keys:
            c = self.card[k]
            anims += [c.animate.set_opacity(1.0), c.box.animate.set_stroke(P.CLAIM, width=2)]
        return anims


# ---------------------------------------------------------------------------
# Payoffs
# ---------------------------------------------------------------------------
def payoff_card(items, font_size=24, title=r"Where this comes back") -> VGroup:
    """``items``: (idea, [part numbers]). Each row: the idea, an arrow, the parts that use it (number and name)."""
    head = label(title, font_size=font_size + 12)
    rows = VGroup()
    for idea, parts in items:
        left = label(idea, font_size=font_size, color=P.CONCL)
        right = label(r",\ ".join(rf"{p}\ \textit{{{PARTS[p]}}}" for p in parts), font_size=font_size - 2,
                      color=GREY_A)
        rows.add(VGroup(left, right))
    lw = max(r[0].width for r in rows)
    for r in rows:
        r[0].align_to(ORIGIN, LEFT)
        arrow = MathTex(r"\longrightarrow", font_size=font_size + 4, color=GREY_C)
        r.insert(1, arrow)
        arrow.next_to(ORIGIN, RIGHT, buff=0).shift(RIGHT * (lw + 0.3))
        r[2].next_to(arrow, RIGHT, buff=0.3)
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
    for r in rows:
        r[1].set_y(r[0].get_y())
        r[2].set_y(r[0].get_y())
    g = VGroup(head, rows).arrange(DOWN, buff=0.5)
    if g.width > 13.4:
        g.width = 13.4
    g.head, g.rows = head, rows
    return g.move_to(ORIGIN)


def quote_card(text: str, who: str, source: str = "", width=10.0, font_size=30, color=None) -> VGroup:
    """A quotation, large, with its author and source (the translation named in ``source``)."""
    color = color or P.HIST
    q = wrapped_label(rf"``{text}''", width - 0.8, font_size, WHITE)
    w = label(rf"--- {who}", font_size=font_size - 6, color=color)
    parts = [q, w]
    if source:
        parts.append(note(source, font_size=18))
    inner = VGroup(*parts).arrange(DOWN, aligned_edge=RIGHT, buff=0.22)
    q.align_to(inner, LEFT)
    bar = Rectangle(width=0.07, height=inner.height, stroke_width=0, fill_color=color, fill_opacity=1)
    return VGroup(bar, inner).arrange(RIGHT, buff=0.3, aligned_edge=UP)


def bar_row(values, labels, colors, width=6.0, height=0.36, font_size=22, vmax=None, fmt=lambda v: f"{v:,.0f}",
            log=False, gap=0.22) -> VGroup:
    """Horizontal bars: a label on the left, the bar, the value on the right (log scale if asked)."""
    vals = np.asarray(values, float)
    if log:
        vals = np.log10(np.maximum(vals, 1)) + 0.15
    vmax = vmax or vals.max()
    names = [label(t, font_size=font_size, color=c) for t, c in zip(labels, colors)]
    lw = max(n.width for n in names)
    rows = VGroup()
    for v, raw, nm, col in zip(vals, values, names, colors):
        bar = Rectangle(width=max(width * v / vmax, 0.02), height=height, stroke_width=0, fill_color=col,
                        fill_opacity=0.85)
        val = MathTex(fmt(raw).replace(",", "{,}"), font_size=font_size + 2, color=col)
        row = VGroup(nm, bar, val)
        row.name, row.bar, row.value = nm, bar, val
        rows.add(row)
    for i, r in enumerate(rows):
        y = -i * (height + gap)
        r.name.move_to([-lw / 2 - 0.1 + (lw - r.name.width) / 2, y, 0])
        r.bar.move_to([0.15 + r.bar.width / 2, y, 0])
        r.value.next_to(r.bar, RIGHT, buff=0.15)
    return rows.move_to(ORIGIN)


from explainer.philosophy.logicviz import *  # noqa: F401,F403,E402
