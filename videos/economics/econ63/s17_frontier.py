from __future__ import annotations

from videos.economics.econ63.common import *  # noqa: F403

NS = (("n_2", 2, LINK), ("n_3", 3, SEED), ("n_5", 5, GAIN))


class Frontier(VoiceoverScene):
    def construct(self):
        card(self, 15, r"Frontier: \ fragile by design", r"If firms choose their suppliers to insure themselves, \ "
             r"why can the whole network collapse at once?", "Chapter fifteen. Frontier: fragile by design.",
             lit={2022: r"Elliott, Golub and Leduc"}, scale=("firm", "world"), horizon=("a decade",))
        self.cliff()
        self.open_()

    def cliff(self):
        F = load("fragility")
        r = np.array(F["r"])
        ax = plane([0.3, 1.0], [0, 1.0], center=LEFT * 2.4 + DOWN * 0.3, x_length=6.8, y_length=4.6,
                   xticks=[0.4, 0.6, 0.8, 1.0], yticks=[0, 0.25, 0.5, 0.75, 1.0],
                   xlabel=r"strength of each supply relationship \ (chance it works)",
                   ylabel=r"share of firms able to produce", xfmt=lambda v: f"{v:.1f}",
                   yfmt=lambda v: rf"{100 * v:.0f}\%", font_size=14)
        lines = VGroup(*[path(ax, r, F[k]["rho"], c, 3.4, smooth=False) for k, _, c in NS])
        side = VGroup(
            label(rf"each firm needs {F['inputs']} essential inputs", font_size=19, color=WHITE),
            label(r"blue: \ 2 possible suppliers of each", font_size=19, color=LINK),
            label(r"orange: \ 3; \ green: \ 5", font_size=19, color=SEED),
            label(r"weaken every link a little: \\ production falls off a cliff", font_size=19, color=SHOCK),
            label(r"more suppliers move the cliff, \\ they do not remove it", font_size=19, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4)
        c3 = F["n_3"]
        tag = published_tag(r"Elliott, \ Golub and Leduc, \ American Economic Review 112(8) (2022); \ the Island: \ "
                            r"agora.network.fragility", corner=DL, font_size=12)
        with self.voiceover(
            "The frontier is the network that firms build for themselves. Matthew Elliott, Benjamin Golub and "
            "Matthew Leduc model a large economy in which every firm needs several essential inputs, here four, "
            "and keeps relationships with a few possible suppliers of each. Any relationship can fail, and a "
            "supplier delivers only if it can produce itself. <bookmark mark='a'/> With two suppliers of each "
            "input, production is high while relationships are very reliable. <bookmark mark='b'/> With three, "
            "or five, the economy tolerates weaker relationships. <bookmark mark='c'/> But look at the shape. As "
            f"relationships weaken, production holds up, and then, at about {c3['cliff']:.2f} with three "
            f"suppliers, it falls from {100 * c3['at_cliff']:.0f} percent of firms to none. A small aggregate "
            "shock, a slight weakening of every link, can cause a collapse. <bookmark mark='d'/> Their result is "
            "that firms, insuring themselves just enough, tend to settle near the cliff's edge: fragile in "
            "equilibrium, though never efficiently so. <bookmark mark='e'/> More suppliers move the cliff; they do "
            "not remove it."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(lines[0]), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(lines[1]), Create(lines[2]), FadeIn(side[2]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(side[3]), Indicate(lines[1], color=WHITE, scale_factor=1.0))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def open_(self):
        head = label(r"what remains open", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.4)
        cards = point_cards([
            (r"networks that rewire", r"firms change suppliers after a shock: \ models where the network itself is "
             r"chosen (Oberfield, \ 2018; \ Acemoglu and Azar, \ 2020)", LINK),
            (r"resilience against efficiency", r"a second source costs money every year; \ who pays for the "
             r"insurance everyone shares? \ Part 66", SEED),
            (r"measuring the network", r"tax invoices and payment records now show who supplies whom, \ firm by "
             r"firm, \ in a growing number of countries", GDP),
            (r"what remains hard", r"telling contagion from common shocks and sorting, \ in data that were not "
             r"built for it", SHOCK),
        ], cols=2, width=12.8, font_size=20).next_to(head, DOWN, buff=0.45)
        tag = published_tag(r"Oberfield, \ Econometrica 86(2) (2018); \ Acemoglu and Azar, \ Econometrica 88(1) "
                            r"(2020)", corner=DL, font_size=12)
        with self.voiceover(
            "What remains open? <bookmark mark='a'/> Networks rewire: after a shock, firms change suppliers, so "
            "the network is an outcome, not a given. Ezra Oberfield, and Daron Acemoglu and Pablo Azar, have "
            "built models in which it is chosen. <bookmark mark='b'/> Resilience costs money: a second source, or "
            "a stock of parts, is paid for every year and used rarely, and its benefit is shared by everyone "
            "downstream. Part sixty-six takes that up for whole countries. <bookmark mark='c'/> Measurement is "
            "improving fast: tax invoices and payment records now show who supplies whom, firm by firm, in a "
            "growing number of countries. <bookmark mark='d'/> And the old difficulty remains: telling what "
            "travels along the links from what the linked simply share."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(cards.cards[k], shift=UP * 0.1))
        self.clear_scene()
