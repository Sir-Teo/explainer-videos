from __future__ import annotations

from videos.philosophy.philosophy24.common import *  # noqa: F403


class Past(VoiceoverScene):
    def construct(self):
        card = chapter_card(11, r"A special beginning", r"Why was the past lower in entropy?", lit=(1895, 2000),
                            part=PART)
        with self.voiceover("Chapter eleven. A special beginning."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.hypothesis()
        self.special()
        self.fluctuation()
        self.price()

    def hypothesis(self):
        both, slow = load("both"), load("slowring")
        t_now = next(t for t, x in enumerate(slow["delta"]) if x <= 0.6)
        hc = history_card(2000, r"David Albert", r"\textit{Time and Chance}", width=5.0,
                          color=HIST).to_corner(UL, buff=0.3)
        f = MathTex(r"\text{PH: the universe began in a macrostate } M_0 \text{ of very low entropy}", font_size=30,
                    color=TIME).next_to(hc, DOWN, buff=0.35).set_x(0)
        axl = Axes(x_range=[-30, 30, 10], y_range=[0.6, 1.02, 0.2], x_length=5.4, y_length=2.8,
                   axis_config={"color": GREY_B, "font_size": 14, "include_numbers": True}).move_to([-3.4, -1.2, 0])
        axr = Axes(x_range=[0, 80, 20], y_range=[0, 1.02, 0.5], x_length=5.4, y_length=2.8,
                   axis_config={"color": GREY_B, "font_size": 14, "include_numbers": True}).move_to([3.4, -1.2, 0])
        vcurve = series_plot(axl, both["entropy"], BAD, xs=both["t"], width=3)
        mono = series_plot(axr, slow["entropy"][:81], OK, width=3)
        now_r = DashedLine(axr.c2p(t_now, 0), axr.c2p(t_now, 1.02), color=GOAL)
        cl = label(r"no special beginning: \ a dip at now", font_size=19, color=BAD).next_to(axl, UP, buff=0.2)
        cr = label(r"a special beginning at $t = 0$: \ entropy rises all the way", font_size=19,
                   color=OK).next_to(axr, UP, buff=0.2)
        nl = label(r"now: \ 80\% white", font_size=17, color=GOAL).next_to(axr.c2p(t_now, 1.02), UP, buff=0.05)
        foot = label(r"add PH to the Mentaculus: \ conditional on it, \ the past was lower in entropy, \ and records "
                     r"are reliable", font_size=20, color=GOAL).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "David Albert's name for the special beginning is the Past Hypothesis. <bookmark mark='a'/>The "
            "universe began in a macrostate of very low entropy. <bookmark mark='b'/>Without it, a typical present "
            "is a dip, with entropy rising in both directions: the last chapter's picture. "
            "<bookmark mark='c'/>With it, the history starts at a low point, and entropy rises all the way from the "
            "beginning to now and beyond. <bookmark mark='d'/>Add the Past Hypothesis to the dynamics and the "
            "uniform probability, and the Mentaculus is complete. Conditional on the special beginning and on what "
            "we see now, the past was lower in entropy than the present, the half-melted ice cube was recently less "
            "melted, and our records and memories are reliable."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(Write(f))
            vo.wait_until("b")
            self.play(Create(axl), FadeIn(cl), Create(vcurve))
            vo.wait_until("c")
            self.play(Create(axr), FadeIn(cr), Create(mono), Create(now_r), FadeIn(nl))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def special(self):
        head = label(r"How special?", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        big = MathTex(r"1 \;\text{ in }\; 10^{10^{123}}", font_size=72, color=TIME).move_to([0, 1.3, 0])
        who = label(r"Penrose's estimate of the precision of the Big Bang \ (\textit{The Emperor's New Mind}, \ "
                    r"1989)", font_size=21, color=GREY_A).next_to(big, DOWN, buff=0.3)
        rows = [
            (r"the twist", r"the early universe was hot and nearly uniform: \ high entropy for a gas, \ but for "
                           r"gravity, \ smoothness is the rare state", ENT),
            (r"Penrose \ (1979)", r"the Weyl curvature hypothesis: \ the initial singularity had no tidal curvature", ABS),
            (r"a law?", r"Albert and Loewer: \ yes, \ an axiom of the best system; \ Callender: \ a brute fact needing "
                        r"no explanation", LAW),
            (r"or explained?", r"Price: \ this, \ not the rise, \ is the real puzzle; \ Carroll and Chen: \ "
                               r"perhaps baby universes", CHANCE),
        ]
        g = rows_table(rows, top=-0.1, gap=0.38, width=8.6, x_text=-2.6, label_size=21, text_size=20)
        with self.voiceover(
            "How special was the beginning? <bookmark mark='a'/>Roger Penrose estimated it: of all the ways the "
            "matter of the universe could have been arranged, a fraction of about one in ten to the ten to the one "
            "hundred and twenty-three would have the low entropy ours had. <bookmark mark='b'/>There is a twist. "
            "The early universe was hot and nearly uniform, which for a gas in a box is maximum entropy. But "
            "gravity reverses the rule: gravitating matter gains entropy by clumping, so a smooth universe is the "
            "rare, low-entropy state. <bookmark mark='c'/>Penrose's Weyl curvature hypothesis of 1979 says the "
            "initial singularity was smooth in just this sense. <bookmark mark='d'/>Is the Past Hypothesis a law? "
            "Albert and Loewer say yes, an axiom of the best system, as simple and as strong as any. Craig "
            "Callender says it is a brute fact that needs no explanation. <bookmark mark='e'/>Huw Price argues that "
            "the special beginning, not the rise of entropy since, is the real puzzle of time's arrow; and Sean "
            "Carroll and Jennifer Chen have proposed that universes like ours are born as baby universes from a "
            "high-entropy parent."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(big), FadeIn(who))
            for mk, r in zip("bcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def fluctuation(self):
        d = load("boltzmann")
        hc = history_card(1895, r"Ludwig Boltzmann", r"`On Certain Questions of the Theory of Gases', \ "
                          r"\textit{Nature}", width=6.4, color=HIST).to_corner(UL, buff=0.3)
        hd = [r"\text{fluctuation: left side holds}", r"\text{entropy drop}", r"\log_{10} P"]
        rows = [[MathTex(f"{f['left']}" + r"\text{ of } 100", font_size=22),
                 MathTex(f"{f['entropy_drop']:.1f}", font_size=22, color=ENT),
                 MathTex(f"{f['log10_p']:.1f}", font_size=22, color=BAD)] for f in d["fluctuations"]]
        grid = ValueGrid(hd, rows, col_w=[4.4, 2.2, 1.8], cell_h=0.44, font_size=19).move_to([-2.4, -0.9, 0])
        side = stack([(r"Boltzmann: \ the universe is in equilibrium, \ and we live in a rare fluctuation", WHITE),
                      (r"but small fluctuations are vastly more probable than large ones", BAD),
                      (r"a lone brain, \ with false memories of a past, \ beats a whole low-entropy universe", ENT),
                      (r"Eddington \ (1931); \ Feynman; \ `Boltzmann brains': \ Albrecht and Sorbo \ (2004)", HIST)],
                     font_size=20, aligned_edge=LEFT, width=4.6).move_to([4.6, -0.6, 0])
        assert all(a["log10_p"] > b["log10_p"] for a, b in zip(d["fluctuations"], d["fluctuations"][1:]))
        with self.voiceover(
            "Boltzmann had another idea. <bookmark mark='a'/>In 1895, crediting his assistant Dr Schuetz, he "
            "suggested that the universe as a whole is in equilibrium, and that our region is a rare fluctuation, "
            "the only kind of place where observers could exist. No special beginning is needed: wait long enough "
            "and every fluctuation happens. <bookmark mark='b'/>But fluctuations are exponentially rarer the "
            "larger they are. The Reasoner counts them in the box of a hundred molecules: a drop of two units of "
            "entropy has a chance of one in a hundred; a drop to perfect order, one in ten to the thirty. "
            "<bookmark mark='c'/>So if we are a fluctuation, we are almost certainly the smallest fluctuation that "
            "could contain us: a single brain, assembled for a moment with false memories of a past that never was, "
            "is vastly more probable than a whole low-entropy universe. <bookmark mark='d'/>Eddington made the point "
            "in 1931 and Feynman in his lectures; Andreas Albrecht and Lorenzo Sorbo named the result Boltzmann "
            "brains in 2004. A theory on which you are probably a Boltzmann brain undermines its own evidence."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(grid.head), Create(grid.rule))
            for r in range(len(rows)):
                self.play(*[FadeIn(c) for c in grid.cell[r]], run_time=0.4)
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def price(self):
        d = load("arrow")
        claims = [(c["key"], c["text"]) for c in d["claims"]]
        assert d["mcs"] == [["D"], ["R"], ["T"], ["I"]]
        pl = PriceList(claims, mus=[tuple(m) for m in d["mus"]], radius=2.9, width=3.7, font_size=19,
                       center=[0, -0.5, 0], title=r"The Price List: \ the arrow of time")
        positions = [(("I",), r"the Past Hypothesis", r"Albert, \ Loewer: \ a special beginning, \ as a law"),
                     (("D",), r"asymmetric laws", r"Penrose; \ Prigogine; \ Albert on GRW collapse"),
                     (("T",), r"Boltzmann's fluctuation", r"the arrow is a local fluke: \ and Boltzmann brains"),
                     (("R",), r"the skeptic", r"our records are illusions: \ a skeptical catastrophe")]
        with self.voiceover(
            "Put the arrow on a Price List. <bookmark mark='a'/>The fundamental dynamics is time-symmetric. Entropy "
            "was lower in the past, so our records and memories are reliable. The rise of entropy is lawlike, not a "
            "fluke. And nothing about the beginning is special. <bookmark mark='b'/>The Kac ring showed why the "
            "four cannot all hold: symmetric laws and a typical state give entropy rising toward the past. "
            "<bookmark mark='c'/>Albert and Loewer give up the fourth: the beginning was special, and that is a law. "
            "<bookmark mark='d'/>Others give up the first, and look for time-asymmetric fundamental laws: Penrose, "
            "Ilya Prigogine, or Albert's suggestion that the collapse of the wave function in the theory of "
            "Ghirardi, Rimini and Weber does the work. <bookmark mark='e'/>Boltzmann's fluctuation gives up the "
            "third, and pays with Boltzmann brains. <bookmark mark='f'/>And giving up the second is the skeptic's "
            "price: our records and memories are illusions, a skeptical catastrophe that nobody accepts."
        ) as vo:
            self.play(FadeIn(pl.title))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in pl.cards], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(Create(pl.conflict))
            first = True
            for mk, (mcs, name, who) in zip("cdef", positions):
                vo.wait_until(mk)
                if not first:
                    self.play(*pl.reset())
                first = False
                anims, centre = pl.position(mcs, name, who, width=3.0)
                self.play(*anims)
        self.clear_scene()
