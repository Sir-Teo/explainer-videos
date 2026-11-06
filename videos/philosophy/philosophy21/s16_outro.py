from __future__ import annotations

from videos.philosophy.philosophy21.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.toolbox()
        self.problems()
        self.payoffs()
        self.references()

    def recap(self):
        items = [
            r"identity: \ two axioms, \ transitivity and necessity derived; \ \texttt{is} and \texttt{==}",
            r"the identity of indiscernibles; \ Black's spheres and the singlet: \ weakly discernible, \ computed",
            r"the statue and the lump, \ modal profiles; \ Theseus plank by plank; \ sortals; \ opacity",
            r"Evans's proof, \ and models where it needs rigid names",
            r"endurance, \ perdurance, \ stages; \ the spinning disc; \ temporary intrinsics \ (a Price List)",
            r"Locke, \ Reid's officer and the ancestral; \ quasi-memory; \ Williams's two tellings",
            r"connectedness and continuity simulated; \ the teleporter; \ the spectrum; \ fission \ (the Wall)",
            r"animalism and Brownson; \ the chariot, \ the bundle, \ the self-model; \ copies and forks",
        ]
        card = objectives_card(items, title=r"What we built", font_size=23)
        with self.voiceover(
            "Let's gather what we built. <bookmark mark='a'/>Identity in the numerical sense, with two axioms from "
            "which its other properties follow. <bookmark mark='b'/>The identity of indiscernibles, and Black's "
            "spheres and entangled electrons, weakly discernible, as the Reasoner computed. <bookmark mark='c'/>The "
            "statue and the lump, the ship of Theseus plank by plank, and sortal concepts. <bookmark mark='d'/>Evans's "
            "argument against vague identity, and models showing where it needs rigid names. <bookmark mark='e'/>Three "
            "pictures of persistence, and temporary intrinsics. <bookmark mark='f'/>Locke's memory criterion, Reid's "
            "officer, and quasi-memory. <bookmark mark='g'/>Parfit's two relations simulated, his teletransporter and "
            "spectrum, and fission: this part's brick in the Wall. <bookmark mark='h'/>And animalism, the Buddhist "
            "chariot, and minds that can be copied."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefgh", range(8)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()

    def toolbox(self):
        head = label(r"The Reasoner, so far", font_size=36, color=CONN).to_edge(UP, buff=0.4)
        mods = [(r"\texttt{persist.automorphisms, discernibility}", r"indiscernibility"),
                (r"\texttt{persist.black\_spheres}", r"Black; \ the singlet"),
                (r"\texttt{persist.theseus}", r"the ship"),
                (r"\texttt{persist.evans}", r"vague identity"),
                (r"\texttt{persist.reid, memory\_chain}", r"memory; \ connectedness"),
                (r"\texttt{persist.fission}", r"branching"),
                (r"\texttt{mereo.*}, \ \texttt{dl.*}, \ \texttt{evo.*}, \ \dots", r"Parts 1--20")]
        lefts = [label(a, font_size=20, color=P.WORLD) for a, _ in mods]
        rights = [label(b, font_size=20, color=GREY_A) for _, b in mods]
        x0, y0 = -6.4, head.get_bottom()[1] - 0.55
        rows = VGroup()
        for i, (a, b) in enumerate(zip(lefts, rights)):
            y = y0 - i * 0.55
            if a.width > 7.6:
                a.width = 7.6
            a.move_to([x0 + a.width / 2, y, 0])
            if b.width > 4.2:
                b.width = 4.2
            b.move_to([1.9 + b.width / 2, y, 0])
            rows.add(VGroup(a, b))
        tests = label(r"checked: \ \texttt{tests/philosophy/test\_persist.py}", font_size=22,
                      color=GREY_B).to_edge(DOWN, buff=0.4)
        w = wall(upto=21, current=21).scale(0.36).to_corner(DR, buff=0.3).shift(UP * 0.5)
        with self.voiceover(
            "The Reasoner has a new module, persist. <bookmark mark='a'/>It finds the symmetries of small "
            "structures and grades discernibility, replaces and rebuilds a ship, checks Evans's argument across "
            "precisifications, computes memory chains and their ancestral, simulates connectedness fading over a "
            "life, and draws the branching graph of fission. <bookmark mark='b'/>And the Wall has its twenty-first "
            "brick."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.15))
            vo.wait_until("a")
            self.play(FadeIn(tests))
            vo.wait_until("b")
            self.play(FadeIn(w), Indicate(w.brick[21], color=P.CONCL, scale_factor=1.06))
        self.wait(1.5)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Derive symmetry and transitivity of identity from reflexivity and Leibniz's law.",
            r"Find a structure on three objects where two are relatively but not absolutely discernible.",
            r"Run Nozick's closest continuer on Theseus: \ what if ship B is assembled only after ship A sinks?",
            r"Give a model with non-rigid names where $\nabla(a = b)$ holds. \ Which step of Evans's proof fails?",
            r"Reid's officer: \ add a memory link from the general to the boy. \ Is Locke's view now consistent?",
            r"Parfit: \ in the fission case, \ is double survival better, \ worse, \ or as good as ordinary "
            r"survival?",
        ], font_size=20)
        with self.voiceover(
            "Six problems, with full solutions in this part's notes. <bookmark mark='a'/>Derive the logic of "
            "identity; build a relatively discernible structure; run the closest continuer theory on a sinking ship; "
            "find a model of vague reference; repair Reid's officer; and weigh double survival. Pause here, and try "
            "them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in ps.rows], lag_ratio=0.25), run_time=3)
            self.wait(3)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"counterparts, \ essences and modal properties", [22]),
            (r"survival after death \ (resurrection, \ reincarnation)", [23]),
            (r"the open future, \ presentism and the B-theory", [24, 25]),
            (r"identical particles and entanglement", [26]),
            (r"names, \ rigid designation and Frege's puzzle", [27]),
            (r"minds, \ machines and copies", [30, 31]),
            (r"future people, \ prudence and the self", [36]),
        ], font_size=22)
        nxt = label(r"Next: \ Part 22, \textit{Possible Worlds}", font_size=26, color=P.CONCL).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/>Counterparts and essences, in Part 22. Survival after death, "
            "in Part 23. The open future and the nature of time, in Parts 24 and 25. Identical particles, in Part 26. "
            "Names and rigid designation, in Part 27. Minds and copies, in Parts 30 and 31. And future people and "
            "the self, in Part 36. <bookmark mark='b'/>Next, Part 22: possible worlds."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows], lag_ratio=0.25))
            vo.wait_until("b")
            self.play(FadeIn(nxt))
        self.clear_scene()

    def references(self):
        ref = reference_card(
            [r"Noonan and Curtis, `Identity', \textit{Stanford Encyclopedia} (2022); \ Wiggins, \textit{Sameness and "
             r"Substance Renewed} (2001)",
             r"Sider, \textit{Four-Dimensionalism} (2001); \ Hawley, \textit{How Things Persist} (2001)",
             r"Parfit, \textit{Reasons and Persons}, Part III (1984); \ Olson, \textit{The Human Animal} (1997)",
             r"Siderits, \textit{Buddhism as Philosophy} (2007); \ Perry (ed.), \textit{Personal Identity} (1975, "
             r"2008)"],
            [r"Leibniz 1686; Locke 1694; Butler 1736; Hume 1739; Reid 1785; Black 1952; Geach 1967; Perry 1970",
             r"Shoemaker 1970; Lewis 1971, 1976, 1986, 1988; Parfit 1971; Gibbard 1975; Quine 1976; Evans 1978",
             r"Nozick 1981; Johnston 1987; French and Redhead 1988; Baker 2000; Bennett 2004; Saunders 2006",
             r"Muller and Saunders 2008; Muller and Seevinck 2009; Sandberg and Bostrom 2008"])
        with self.voiceover(
            "The books and papers this part follows are on screen, and in the notes. Thanks for watching."
        ):
            self.play(FadeIn(ref))
            self.wait(4)
        self.clear_scene()
