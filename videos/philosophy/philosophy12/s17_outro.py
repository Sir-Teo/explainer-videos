from __future__ import annotations

from videos.philosophy.philosophy12.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.toolbox()
        self.problems()
        self.payoffs()
        self.references()

    def recap(self):
        items = [
            r"knowledge as a box: \ S5, \ partitions, \ and its critics",
            r"three cards; \ public announcements; \ the muddy children to $n = 8$",
            r"common knowledge, \ the tower of $E$'s, \ reachability; \ Lewis's conventions",
            r"the coordinated attack \ (the Wall); \ Byzantine generals, \ FLP, \ Paxos; \ the email game",
            r"Aumann's agreement theorem, \ talked out; \ no trade",
            r"private updates and lies; \ Moore sentences; \ Fitch's paradox",
            r"testimony and miracles; \ peer disagreement; \ crowds; \ networks of inquiry",
        ]
        card = objectives_card(items, title=r"What we built", font_size=24)
        with self.voiceover(
            "Let's gather what we built. <bookmark mark='a'/>Knowledge as a box, and the logic S5. "
            "<bookmark mark='b'/>Many agents in one model, and the muddy children, solved for eight. "
            "<bookmark mark='c'/>Common knowledge, as a tower and as reachability. <bookmark mark='d'/>The "
            "coordinated attack, this part's brick in the Wall, and the engineering that lives with it. "
            "<bookmark mark='e'/>Aumann's theorem, as a conversation. <bookmark mark='f'/>Private messages, lies, and "
            "the truths that cannot be known. <bookmark mark='g'/>And knowledge from others: testimony, "
            "disagreement, crowds and networks."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefg", range(7)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()

    def toolbox(self):
        head = label(r"The Reasoner, so far", font_size=36, color=CONN).to_edge(UP, buff=0.4)
        mods = [(r"\texttt{epistemic.Model, holds, announce}", r"multi-agent S5; \ $K$, \ $E$, \ $C$; \ public "
                                                                 r"announcements"),
                (r"\texttt{epistemic.muddy\_rounds}", r"the muddy children, \ any $n$"),
                (r"\texttt{epistemic.attack\_depth, email\_game}", r"the generals; \ Rubinstein's unravelling"),
                (r"\texttt{epistemic.agreement\_dialogue}", r"Geanakoplos--Polemarchakis"),
                (r"\texttt{epistemic.private\_update, fitch\_check}", r"product update; \ Fitch by tableau"),
                (r"\texttt{epistemic.diversity, zollman}", r"crowds; \ networks of scientists"),
                (r"\texttt{knowledge.*}, \ \texttt{modern.*}, \ \dots", r"Parts 1--11")]
        lefts = [label(a, font_size=20, color=P.WORLD) for a, _ in mods]
        rights = [label(b, font_size=20, color=GREY_A) for _, b in mods]
        x0, y0 = -6.4, head.get_bottom()[1] - 0.55
        rows = VGroup()
        for i, (a, b) in enumerate(zip(lefts, rights)):
            y = y0 - i * 0.55
            a.move_to([x0 + a.width / 2, y, 0])
            if b.width > 5.6:
                b.width = 5.6
            b.move_to([1.0 + b.width / 2, y, 0])
            rows.add(VGroup(a, b))
        tests = label(r"checked: \ \texttt{tests/philosophy/test\_epistemic.py}", font_size=22,
                      color=GREY_B).to_edge(DOWN, buff=0.4)
        w = wall(upto=12, current=12).scale(0.36).to_corner(DR, buff=0.3).shift(UP * 0.5)
        with self.voiceover(
            "The Reasoner has a module for knowledge among many. <bookmark mark='a'/>Multi-agent models with "
            "knowledge, everyone-knows and common knowledge; public and private updates; the muddy children for any "
            "number of children; the generals and the email game; the agreement dialogue; Fitch's paradox, by "
            "tableau; the diversity theorem; and the Zollman simulator. <bookmark mark='b'/>And the Wall has its "
            "twelfth brick."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.15))
            vo.wait_until("a")
            self.play(FadeIn(tests))
            vo.wait_until("b")
            self.play(FadeIn(w), Indicate(w.brick[12], color=P.CONCL, scale_factor=1.06))
        self.wait(1.5)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Three cards: \ after Ann announces `I hold 0', \ what does Ann know about Bob's card? \ Why?",
            r"Muddy children with $n = 4$ and $k = 2$ muddy: \ list the worlds left after each announcement.",
            r"Show that if E$^2\varphi$ holds at every world, \ so does $C\varphi$, \ in a model with one agent.",
            r"In the agreement dialogue, \ change the event to $\{1, 5\}$ \ and run the conversation.",
            r"A witness is right 999 times in 1000. \ How rare must an event be \ before her report leaves it "
            r"under even odds?",
            r"(Essay) Equal weight or steadfast? \ Take a real disagreement, \ and defend a policy for it.",
        ], font_size=22)
        with self.voiceover(
            "Six problems, with full solutions in this part's notes. <bookmark mark='a'/>The cards; the muddy "
            "children with four; common knowledge for one agent; a new agreement dialogue; Hume's witness; and an "
            "essay on disagreement. Pause here, and try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in ps.rows], lag_ratio=0.25), run_time=3)
            self.wait(3)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"degrees of belief, \ Bayes, \ and the lottery", [13]),
            (r"belief revision, \ and lies believed", [14]),
            (r"evidence from many sources", [16]),
            (r"conventions, \ games and the social contract", [34]),
            (r"democracy, \ juries, \ and Condorcet", [39]),
            (r"agreement among machines that reason", [42]),
        ], font_size=23)
        nxt = label(r"Next: \ Part 13, \textit{Degrees of Belief}", font_size=26, color=P.CONCL).to_edge(DOWN,
                                                                                                    buff=0.4)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/>Degrees of belief and Bayes, in Part 13. Belief revision, in "
            "Part 14. Evidence from many sources, in Part 16. Conventions and the social contract, in Part 34. Juries "
            "and democracy, in Part 39. And agreement among machines that reason, in Part 42. "
            "<bookmark mark='b'/>Next, Part 13: degrees of belief."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows], lag_ratio=0.25))
            vo.wait_until("b")
            self.play(FadeIn(nxt))
        self.clear_scene()

    def references(self):
        ref = reference_card(
            [r"Hintikka, \textit{Knowledge and Belief} (1962); \ Lewis, \textit{Convention} (1969)",
             r"Fagin, Halpern, Moses and Vardi, \textit{Reasoning About Knowledge} (1995)",
             r"van Ditmarsch, van der Hoek and Kooi, \textit{Dynamic Epistemic Logic} (2007)",
             r"Coady, \textit{Testimony} (1992); \ Page, \textit{The Difference} (2007); \ Lackey and Christensen "
             r"(eds.) (2013)"],
            [r"Aumann 1976; Gray 1978; Lamport, Shostak and Pease 1982; Geanakoplos and Polemarchakis 1982",
             r"Milgrom and Stokey 1982; Fischer, Lynch and Paterson 1985; Plaza 1989; Rubinstein 1989",
             r"Halpern and Moses 1990; Baltag, Moss and Solecki 1998; Lamport 1998; Ongaro and Ousterhout 2014",
             r"Fitch 1963; Galton 1907; Christensen 2007; Elga 2007; Kelly 2010; Zollman 2007; Nguyen 2020"])
        with self.voiceover(
            "The books and papers this part follows are on screen, and in the notes. Thanks for watching."
        ):
            self.play(FadeIn(ref))
            self.wait(4)
        self.clear_scene()
