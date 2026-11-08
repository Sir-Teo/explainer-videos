# Philosophy, Built — Part 20: What There Is

Part 20 of *Philosophy, Built* ([series plan](../README.md), [syllabus](../SYLLABUS.md)) opens Act V, *The World*,
with ontology. How many things are on a table? Quine's "On What There Is": Plato's beard, the criterion of
ontological commitment as quantification (sentences regimented and their commitments read off), the Geach–Kaplan
sentence checked by brute force over all 31 groups of five critics on three admiration graphs (Boolos on plural
innocence), Ockham's razor and "no entity without identity", and gavagai (inscrutability of reference). Meinong's
golden mountain and round square, Russell's theory of descriptions with both scopes of "the present King of France
is not bald" evaluated in a model, Strawson, the neo-Meinongians (Parsons, Zalta, Priest), and Sherlock Holmes
(pretence, encoding, creationism). Universals: realism, tropes and nominalism drawn side by side; Porphyry,
Boethius, Abelard, Ockham; Armstrong's sparse universals; Bradley's regress. Resemblance nominalism tested on property
tables: Goodman's imperfect community (one spurious maximal class, every real property lost) and companionship
(the F's never a maximal class), and Rodriguez-Pereyra's replies. Abstract objects: Lewis's four ways, Frege's
directions (seven lines, three directions), Hume's principle and Basic Law V, Platonism and its rivals, and Lewis's
classes as sums of singletons. Mereology axiom by axiom: every partial order on up to six elements, up to
isomorphism (1, 2, 5, 16, 63, 318), tested for weak and strong supplementation and unrestricted fusion; only sizes 1
and 3 model classical extensional mereology; the Boolean algebras with zero removed (1, 3, 7, 15 elements) checked;
the twin and lonely counterexamples. The special composition question counted on six blocks (nihilism 6, contact 40,
universalism 63), organicism, Merricks's overdetermination argument, and mereotopology's boundary puzzle. The
Lewis–Sider argument from vagueness (with "there are exactly two things" in pure logic) and **the Wall's twentieth
brick**; composition as identity. The problem of the many as a **Price List**, and Tibbles. Metaontology: Carnap's
internal and external questions, Putnam's three individuals (3 objects or 7), quantifier variance, easy ontology and
Sider's structure. Grounding: examples, a grounding graph checked as a strict partial order (five fundamental facts,
three levels, and a cycle), Fine's truth-functional logic of ground unfolded to the literals, and the debate (Fine,
Schaffer, Rosen, Wilson). Fundamentality: gunk by dyadic bisection, four shapes for reality, priority monism.
Description logic: ALC semantics, the family TBox, a tableau reasoner that proves Mother ⊑ Parent in ten rule
applications and returns a counter-model for Parent ⊑ Mother, and an ABox with open-world answers (yes, no,
unknown). Ontologies in practice: the semantic web, the Gene Ontology, SNOMED CT, Basic Formal Ontology, and OntoClean
flagging three errors in a taxonomy. Knowledge graphs: a two-dimensional TransE embedding that infers Tokyo is in
Asia, confidently misplaces Lisbon, and answers nonsense; and what a language model commits to.

The worked model results are computed by the Reasoner's new modules `explainer/philosophy/reasoner/mereo.py` and
`explainer/philosophy/reasoner/dl.py`, tested in `tests/philosophy/test_mereo.py` and `tests/philosophy/test_dl.py`,
and cached by [`compute.py`](compute.py).

## Build it

```bash
python -m videos.philosophy.philosophy20.compute       # every computed item (under a minute; .cache/philosophy20)
python tools/build.py philosophy20 -q l                # 480p preview
python tools/build.py philosophy20                     # 1080p30 -> renders/philosophy20.mp4
python tools/qa_scene.py philosophy20 Mereology        # one chapter, silent, with a contact sheet
```

## Chapters

| # | Scene | What it establishes | Computed on screen |
|---|---|---|---|
| 0 | `Hook` | Quine (1948); the table; the plan. | — |
| 1 | `Quine` | Plato's beard; the criterion; Geach and Kaplan; Boolos (1984); Ockham; Quine (1968). | the Geach–Kaplan sentence on three graphs |
| 2 | `Meinong` | Meinong (1904); Russell (1905); Strawson (1950); Parsons (1980); Zalta (1983); Priest (2005); Walton (1990); Thomasson (1999). | both scopes in a kingless model |
| 3 | `Universals` | Plato; Aristotle; Williams (1953); Porphyry; Boethius; Abelard; Ockham; Armstrong (1978, 1997); Lewis (1983); Bradley (1893). | — |
| 4 | `Resemblance` | Russell (1912); Goodman (1951); Rodriguez-Pereyra (2002). | maximal resemblance classes against extensions |
| 5 | `Abstract` | Lewis (1986); Frege (1884); Hume's principle; Benacerraf (1973); Hale and Wright; Linnebo (2018); Field (1980); Thomasson (2015); Lewis (1991). | directions as parallelism classes |
| 6 | `Mereology` | Leśniewski (1916); CEM; Tarski (1935); constitution. | every poset on ≤ 6 elements; Boolean algebras minus zero |
| 7 | `Composition` | van Inwagen (1987, 1990); Merricks (2001); Whitehead; Clarke (1981); Bolzano; Brentano; Casati and Varzi (1999). | objects among six blocks on three answers |
| 8 | `Vagueness` | Lewis (1986); Sider (2001); **the Wall's twentieth brick**; Baxter (1988); Lewis (1991); Sider (2007); Cotnoir (2013). | — |
| 9 | `Many` | Unger (1980); Geach (1980); the problem of the many as a **Price List**; Lewis (1993); Williamson; supervaluation. | the conflict and its exits |
| 10 | `Meta` | Carnap (1950); Quine (1951); Putnam (1987); Hirsch (2002, 2011); Thomasson (2015); Sider (2011). | 3 objects or 7 |
| 11 | `Grounding` | Fine (2001, 2012); Schaffer (2009); Rosen (2010); Wilson (2014). | a grounding graph and a cycle; Fine's rules unfolded |
| 12 | `Fundamental` | Whitehead; Sider (1993); Schaffer (2003, 2010); Bohn; Horgan and Potrč. | dyadic bisection |
| 13 | `Logic` | ALC; Schmidt-Schauß and Smolka (1991); Baader et al. (2003). | the family tableau; a counter-model; ABox answers |
| 14 | `Industry` | Berners-Lee, Hendler and Lassila (2001); OWL; Gene Ontology; SNOMED CT; BFO (ISO 2021); Guarino and Welty (2002). | OntoClean on a taxonomy |
| 15 | `Graphs` | Wikidata; the Knowledge Graph (2012); Bordes et al. (2013); Li et al. (2023). | a TransE embedding and its answers |
| 16 | `Outro` | recap; the Reasoner's modules; the Wall; problems; payoffs; references. | — |

## Sources

Texts: Loux and Crisp, *Metaphysics: A Contemporary Introduction* (4th ed. 2017); van Inwagen, *Material Beings*
(1990); Simons, *Parts: A Study in Ontology* (1987); Casati and Varzi, *Parts and Places* (1999); Armstrong,
*Universals and Scientific Realism* (1978) and *Universals: An Opinionated Introduction* (1989); Lewis, *On the
Plurality of Worlds* (1986) and *Parts of Classes* (1991); Rodriguez-Pereyra, *Resemblance Nominalism* (2002);
Chalmers, Manley and Wasserman (eds.), *Metametaphysics* (2009); Sider, *Writing the Book of the World* (2011);
Baader et al., *The Description Logic Handbook* (2003); Arp, Smith and Spear, *Building Ontologies with Basic Formal
Ontology* (2015).

Papers: Meinong (1904); Russell (1905); Leśniewski (1916); Quine (1948, 1951, 1968); Carnap (1950); Strawson (1950);
Goodman (1951); Williams (1953); van Inwagen (1977, 1987); Unger (1980); Geach (1980); Parsons (1980); Clarke (1981);
Lewis (1983, 1993); Boolos (1984); Putnam (1987); Baxter (1988); Schmidt-Schauß and Smolka (1991); Sider (1993, 2001,
2007); Thomasson (1999); Fine (2001, 2012); Merricks (2001); Hirsch (2002); Guarino and Welty (2002); Schaffer (2003,
2009, 2010); Rosen (2010); Cotnoir (2013); Bordes et al. (2013); Wilson (2014); Li et al. (2023).
