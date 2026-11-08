from __future__ import annotations

from videos.philosophy.philosophy30.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.toolbox()
        self.problems()
        self.payoffs()
        self.references()

    def recap(self):
        items = [
            r"Avicenna's floating man; \ Descartes's two substances; \ Elisabeth's question",
            r"Ryle's category mistake; \ behaviourism; \ the identity theory; \ Kripke and Putnam",
            r"functionalism: \ one table, \ two substrates, \ in lockstep; \ a role's occupants counted",
            r"Turing's game and nine objections; \ the Chinese room, \ with a rulebook built",
            r"Blockhead's table: \ $10^{25\,764}$ entries for an hour; \ Leibniz's mill; \ the China brain",
            r"supervenience on worlds; \ Kim's exclusion \ (the Wall; \ a Price List); \ Yablo's pigeon",
            r"emergence and Life's glider gun; \ eliminativism; \ real patterns, \ measured",
            r"Dretske's gauge; \ Millikan; \ Fodor; \ systematicity, \ built; \ a probe that reads what is not used",
        ]
        card = objectives_card(items, title=r"What we built", font_size=22)
        with self.voiceover(
            "Let's gather what we built. <bookmark mark='a'/>The floating man, Descartes's dualism and Elisabeth's "
            "question. <bookmark mark='b'/>Behaviourism, the identity theory, and the objections that ended it. "
            "<bookmark mark='c'/>Functionalism, with one machine table run in two substrates in lockstep, and the "
            "occupants of its role counted. "
            "<bookmark mark='d'/>Turing's imitation game, and the Chinese room with a rulebook built. "
            "<bookmark mark='e'/>Blockhead's table, measured against the universe, Leibniz's mill and the China brain. "
            "<bookmark mark='f'/>Supervenience, checked on small sets of worlds, and Kim's exclusion argument, this "
            "part's brick in the Wall and its Price List, with Yablo's pigeon and proportional causes. "
            "<bookmark mark='g'/>Emergence, Life's glider gun, eliminativism and Dennett's real patterns, measured. <bookmark mark='h'/>And content: Dretske's gauge, Millikan, "
            "Fodor, systematicity built, and a probe that reads what a network does not use."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefgh", range(8)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()

    def toolbox(self):
        head = label(r"The Reasoner, so far", font_size=36, color=CONN).to_edge(UP, buff=0.4)
        mods = [(r"\texttt{mind.realizers, ramsey}", r"one role, \ two substrates; \ its occupants"),
                (r"\texttt{mind.rulebook}", r"the Chinese room"),
                (r"\texttt{mind.blockhead}", r"a table's size"),
                (r"\texttt{mind.supervenience}", r"weak, \ strong, \ global"),
                (r"\texttt{mind.proportional}", r"a proportional cause"),
                (r"\texttt{mind.life, real\_patterns}", r"emergence; \ a pattern's worth"),
                (r"\texttt{mind.gauge, systematicity}", r"information; \ composition"),
                (r"\texttt{mind.probe\_vs\_use}", r"decodable is not used"),
                (r"\texttt{phenomenology.*}, \ \texttt{pragmatics.*}, \ \dots", r"Parts 1--29")]
        lefts = [label(a, font_size=20, color=P.WORLD) for a, _ in mods]
        rights = [label(b, font_size=20, color=GREY_A) for _, b in mods]
        x0, y0 = -6.4, head.get_bottom()[1] - 0.5
        rows = VGroup()
        for i, (a, b) in enumerate(zip(lefts, rights)):
            y = y0 - i * 0.48
            if a.width > 7.6:
                a.width = 7.6
            a.move_to([x0 + a.width / 2, y, 0])
            if b.width > 4.2:
                b.width = 4.2
            b.move_to([1.9 + b.width / 2, y, 0])
            rows.add(VGroup(a, b))
        tests = label(r"checked: \ \texttt{tests/philosophy/test\_mind.py}", font_size=22,
                      color=GREY_B).to_corner(DL, buff=0.4)
        w = wall(upto=30, current=30).scale(0.36).to_corner(DR, buff=0.3)
        with self.voiceover(
            "The Reasoner has a new module, mind. <bookmark mark='a'/>It runs one functional role in two substrates and "
            "counts the occupants of a role, writes a Chinese rulebook, sizes Blockhead's table, checks three kinds of "
            "supervenience, finds a proportional cause, runs the Game of Life, prices a real pattern, measures the information in a gauge, tests systematicity, and probes a network for information it "
            "does not use. <bookmark mark='b'/>And the Wall has its thirtieth brick."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.15))
            vo.wait_until("a")
            self.play(FadeIn(tests))
            vo.wait_until("b")
            self.play(FadeIn(w), Indicate(w.brick[30], color=P.CONCL, scale_factor=1.06))
        self.wait(1.5)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Realize the pain table of chapter 3 in a third substrate; \ prove the outputs agree step by step.",
            r"Show that strong supervenience implies weak and global supervenience.",
            r"Find two sets of worlds: \ weak but not global, \ and global but not weak.",
            r"State Kim's argument as five propositions and find every minimal inconsistent subset.",
            r"Estimate Blockhead's table for a 5-minute test with a 10\,000-word vocabulary.",
            r"Build a network that uses $x$, \ and show that removing the probe's direction now hurts the output.",
        ], font_size=20)
        with self.voiceover(
            "Six problems, with full solutions in this part's notes. <bookmark mark='a'/>A third realizer for the pain "
            "table; strong supervenience implies the other two; independence of weak and global; Kim's argument "
            "formalized; Blockhead with a vocabulary of words; and a network whose probe direction matters. Pause "
            "here, and try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in ps.rows], lag_ratio=0.25), run_time=3)
            self.wait(3)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"qualia, \ zombies and the hard problem", [31]),
            (r"agents, \ causes and free will", [32]),
            (r"decision-making minds", [33]),
            (r"machines that decide about people", [41]),
            (r"aligned reasoners", [42]),
        ], font_size=22)
        nxt = label(r"Next: \ Part 31, \textit{Consciousness}", font_size=26, color=P.CONCL).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/>Qualia, zombies and the hard problem, in Part 31. Agents, "
            "causes and free will, in Part 32. Minds that decide, in Part 33. Machines that decide about people, in "
            "Part 41. And aligned reasoners, in Part 42. <bookmark mark='b'/>Next, Part 31: consciousness."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows], lag_ratio=0.25))
            vo.wait_until("b")
            self.play(FadeIn(nxt))
        self.clear_scene()

    def references(self):
        ref = reference_card(
            [r"Kim, \textit{Philosophy of Mind} (3rd ed., 2011); \ Kim, \textit{Mind in a Physical World} (1998)",
             r"Turing, `Computing Machinery and Intelligence' (1950); \ Searle, `Minds, Brains, and Programs' (1980)",
             r"Block, `Psychologism and Behaviorism' (1981); \ Bedau, `Weak Emergence' (1997)",
             r"Shea, \textit{Representation in Cognitive Science} (2018); \ Ravenscroft, \textit{Philosophy of Mind}"],
            [r"Avicenna c.\ 1020; Descartes 1641; Elisabeth 1643; Leibniz 1714; Mill 1843; Broad 1925; Ryle 1949",
             r"Turing 1950; Place 1956; Smart 1959; Putnam 1963, 1967; Armstrong 1968; Davidson 1970; Kripke 1970",
             r"Lewis 1970, 1972; Fodor 1975, 1987, 1990; Block 1978, 1981; Searle 1980; Churchland 1981; Dretske 1981",
             r"Jackson 1982; Kim 1984, 1998; Millikan 1984; Dennett 1987, 1991; Fodor and Pylyshyn 1988; Yablo 1992",
             r"Bedau 1997; Clark and Chalmers 1998; Bennett 2003; Woodward 2003; List and Menzies 2009",
             r"Lake and Baroni 2018, 2023; Elazar et al. 2021; Jones and Bergen 2025"])
        with self.voiceover(
            "The books and papers this part follows are on screen, and in the notes. Thanks for watching."
        ):
            self.play(FadeIn(ref))
            self.wait(4)
        self.clear_scene()
