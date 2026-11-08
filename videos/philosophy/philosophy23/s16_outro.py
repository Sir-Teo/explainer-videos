from __future__ import annotations

from videos.philosophy.philosophy23.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.toolbox()
        self.problems()
        self.payoffs()
        self.references()

    def recap(self):
        items = [
            r"Anselm's reductio, \ valid; \ Gaunilo's island; \ Kant's thalers",
            r"Plantinga's argument: \ valid on every S5 frame, \ and so is its mirror",
            r"Gödel's axioms: \ no model; \ Scott's: \ one God, \ one world \ (the Wall)",
            r"the third way's quantifier shift; \ Leibniz; \ van Inwagen's collapse, \ computed",
            r"al-Ghazālī's planets and Hilbert's hotel; \ fine-tuning with a multiverse",
            r"Pascal's wager and Hájek's mixed strategies; \ James and Clifford",
            r"Mackie, \ the free-will defence modelled; \ Rowe as Bayes \ (a Price List)",
            r"Hume's miracles by the numbers; \ branching time; \ Udayana, \ Dharmakīrti, \ Avicenna",
        ]
        card = objectives_card(items, title=r"What we built", font_size=22)
        with self.voiceover(
            "Let's gather what we built. <bookmark mark='a'/>Anselm's argument, valid as a reductio, with its parody "
            "and Kant's objection. <bookmark mark='b'/>Plantinga's modal argument, valid on every S5 frame, and its "
            "mirror image, equally valid. <bookmark mark='c'/>Gödel's proof in a finite higher-order modal logic: "
            "his own axioms have no model, and Scott's have models only with one world, the modal collapse that is "
            "this part's brick in the Wall. <bookmark mark='d'/>The cosmological arguments, a countermodel to the "
            "third way, and van Inwagen's collapse of the principle of sufficient reason. <bookmark mark='e'/>The "
            "kalām and the infinite; fine-tuning, with and without a multiverse. <bookmark mark='f'/>Pascal's wager "
            "and the trouble with infinity. <bookmark mark='g'/>The problem of evil, logical and evidential. "
            "<bookmark mark='h'/>Hume on miracles, branching time, and arguments from India and the Islamic world."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefgh", range(8)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()

    def toolbox(self):
        head = label(r"The Reasoner, so far", font_size=36, color=CONN).to_edge(UP, buff=0.4)
        mods = [(r"\texttt{theism.plantinga}", r"the modal argument on every frame"),
                (r"\texttt{theism.godel}", r"Gödel and Scott, \ every finite model"),
                (r"\texttt{theism.psr\_collapse, third\_way}", r"van Inwagen; \ Aquinas"),
                (r"\texttt{theism.fine\_tuning, revolutions}", r"design; \ al-Ghazālī"),
                (r"\texttt{theism.pascal, rowe, hume}", r"wager; \ evil; \ miracles"),
                (r"\texttt{theism.sea\_battle}", r"branching time"),
                (r"\texttt{prop.mus\_mcs}", r"Mackie, \ the free-will defence, \ Dharmakīrti"),
                (r"\texttt{worlds.*}, \ \texttt{persist.*}, \ \texttt{mereo.*}, \ \dots", r"Parts 1--22")]
        lefts = [label(a, font_size=20, color=P.WORLD) for a, _ in mods]
        rights = [label(b, font_size=20, color=GREY_A) for _, b in mods]
        x0, y0 = -6.4, head.get_bottom()[1] - 0.5
        rows = VGroup()
        for i, (a, b) in enumerate(zip(lefts, rights)):
            y = y0 - i * 0.52
            if a.width > 7.6:
                a.width = 7.6
            a.move_to([x0 + a.width / 2, y, 0])
            if b.width > 4.2:
                b.width = 4.2
            b.move_to([1.9 + b.width / 2, y, 0])
            rows.add(VGroup(a, b))
        tests = label(r"checked: \ \texttt{tests/philosophy/test\_theism.py}", font_size=22,
                      color=GREY_B).to_edge(DOWN, buff=0.4)
        w = wall(upto=23, current=23).scale(0.36).to_corner(DR, buff=0.3).shift(UP * 0.5)
        with self.voiceover(
            "The Reasoner has a new module, theism. <bookmark mark='a'/>It checks the modal ontological argument on "
            "every small frame, searches every finite model of Gödel's and Scott's axioms, tests the principle of "
            "sufficient reason on spaces of worlds, builds a countermodel to the third way, computes fine-tuning "
            "likelihoods with a multiverse, Pascal's expected utilities, Rowe's and Hume's posteriors, and Prior's "
            "branching time. <bookmark mark='b'/>And the Wall has its twenty-third brick."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.15))
            vo.wait_until("a")
            self.play(FadeIn(tests))
            vo.wait_until("b")
            self.play(FadeIn(w), Indicate(w.brick[23], color=P.CONCL, scale_factor=1.06))
        self.wait(1.5)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Formalize Gaunilo's island in Anselm's form. \ Which premise does Plantinga's reply reject?",
            r"Find a T frame on which $\Diamond\Box g \to \Box g$ fails. \ Which world falsifies it?",
            r"Show that Gödel's definition of essence makes the empty property an essence of everything.",
            r"Pascal: \ give a decision rule under which wagering beats flipping a coin. \ What does it give up?",
            r"Rowe: \ for what value of $P(E \mid G)$ does the posterior stay at one half?",
            r"Hume: \ with correlated witnesses, \ how many does it take? \ Model the correlation.",
        ], font_size=20)
        with self.voiceover(
            "Six problems, with full solutions in this part's notes. <bookmark mark='a'/>Formalize Gaunilo's island; "
            "find the frame that breaks the modal argument; show what goes wrong in Gödel's essence; rescue the wager "
            "from mixed strategies; balance Rowe's likelihoods; and model correlated witnesses for Hume. Pause here, "
            "and try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in ps.rows], lag_ratio=0.25), run_time=3)
            self.wait(3)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"time, \ the arrow and the beginning of the universe", [24, 25]),
            (r"quantum cosmology and the many worlds", [26]),
            (r"consciousness, \ souls and other minds", [30, 31]),
            (r"freedom, \ foreknowledge and fatalism", [32]),
            (r"decisions with infinite stakes", [33]),
            (r"morality without God? \ divine command theory", [35, 37]),
            (r"existential risk, \ value and the very long future", [36, 42]),
        ], font_size=22)
        nxt = label(r"Next: \ Part 24, \textit{Laws, Chance and the Arrow}", font_size=26,
                    color=P.CONCL).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/>Time, its arrow, and the beginning of the universe, in Parts "
            "24 and 25. Quantum cosmology and many worlds, in Part 26. Consciousness, souls and other minds, in Parts "
            "30 and 31. Freedom and fatalism, in Part 32. Decisions with infinite stakes, in Part 33. Whether "
            "morality needs God, in Parts 35 and 37. And value over the very long future, in Parts 36 and 42. "
            "<bookmark mark='b'/>Next, Part 24: laws, chance, and the arrow of time."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows], lag_ratio=0.25))
            vo.wait_until("b")
            self.play(FadeIn(nxt))
        self.clear_scene()

    def references(self):
        ref = reference_card(
            [r"Oppy, \textit{Arguing about Gods} (2006); \ Mackie, \textit{The Miracle of Theism} (1982)",
             r"Swinburne, \textit{The Existence of God} (2nd ed., 2004); \ Plantinga, \textit{God, Freedom, and Evil} "
             r"(1974)",
             r"Craig and Moreland (eds.), \textit{The Blackwell Companion to Natural Theology} (2009); \ Hájek, "
             r"`Pascal's Wager', \textit{Stanford Encyclopedia}",
             r"Earman, \textit{Hume's Abject Failure} (2000); \ Benzmüller and Woltzenlogel Paleo (2016)"],
            [r"Anselm 1078; Aquinas 1270; Molina 1588; Pascal 1670; Leibniz 1714; Hume 1748, 1779; Kant 1781",
             r"Paley 1802; Clifford 1877; James 1896; Mackie 1955; Hick 1966; Prior 1967; Plantinga 1974",
             r"Rowe 1979; Craig 1979; van Inwagen 1983; Wykstra 1984; Gödel 1987; Sobel 1987; Hacking 1987",
             r"Alston 1991; White 2000; Hájek 2003; Borde, Guth and Vilenkin 2003; Pruss 2006; Udayana; Dharmakīrti"])
        with self.voiceover(
            "The books and papers this part follows are on screen, and in the notes. Thanks for watching."
        ):
            self.play(FadeIn(ref))
            self.wait(4)
        self.clear_scene()
