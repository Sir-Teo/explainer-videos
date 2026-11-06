from __future__ import annotations

from videos.philosophy.philosophy7.common import *  # noqa: F403


class Minds(VoiceoverScene):
    def construct(self):
        card = chapter_card(16, r"Minds and machines", r"Do the theorems show that we are not machines?",
                            lit=(1961,), part=PART)
        with self.voiceover("Chapter sixteen. Minds and machines."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.argument()
        self.price_list()
        self.godel()
        self.misuses()

    def argument(self):
        hcs = VGroup(history_card(1961, r"J. R. Lucas", r"`Minds, machines and Gödel'", width=5.0, color=HIST),
                     history_card(1989, r"Roger Penrose", r"\textit{The Emperor's New Mind}; \ \textit{Shadows of the "
                                  r"Mind} (1994)", width=6.4, color=HIST)).arrange(RIGHT, buff=0.4).to_edge(UP, buff=0.4)
        rows = VGroup(label(r"suppose my mathematical mind were a formal system $F$", font_size=26),
                      label(r"$F$ cannot prove its Gödel sentence $G_F$", font_size=26),
                      label(r"but I can \textit{see} that $G_F$ is true", font_size=26, color=GOAL),
                      label(r"so I am not $F$, \ nor any machine", font_size=28, color=BAD)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.3).next_to(hcs, DOWN, buff=0.6)
        with self.voiceover(
            "Do Gödel's theorems show that the human mind is not a machine? Two famous arguments say so. "
            "<bookmark mark='a'/>The philosopher J. R. Lucas in 1961, and the physicist Roger Penrose in two books, "
            "in 1989 and 1994. <bookmark mark='b'/>Suppose my mathematical reasoning were captured by some formal "
            "system F. F cannot prove its own Gödel sentence. <bookmark mark='c'/>But I can see that the Gödel "
            "sentence is true. <bookmark mark='d'/>So I can do something F cannot, and I am not F. Since F was "
            "arbitrary, I am no machine at all."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(hcs))
            for mk, r in zip("bcd", (VGroup(rows[0], rows[1]), rows[2], rows[3])):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
        self.clear_scene()

    def price_list(self):
        d = load("minds")
        claims = [(c["key"], c["text"]) for c in d["claims"]]
        pl = PriceList(claims, mus=[tuple(x) for x in d["mus"]], radius=2.4, width=4.4, font_size=22,
                       center=[0, -0.6, 0], title=r"The Price List: \ minds and machines")
        bg = label(r"held fixed, \ a theorem: \ Gödel II, \ a consistent $F$ does not prove $\mathrm{Con}(F)$",
                   font_size=20, color=GREY_B).to_edge(DOWN, buff=0.25)
        positions = [(("M",), r"anti-mechanism", r"Lucas; \ Penrose"),
                     (("K",), r"we cannot know our own consistency", r"Benacerraf (1967); \ Putnam; \ Feferman"),
                     (("C",), r"we are inconsistent", r"Turing (1947): \ `if a machine is expected to be "
                      r"infallible, \ it cannot also be intelligent'")]
        assert sorted(tuple(x) for x in d["mcs"]) == sorted(p_[0] for p_ in positions)
        with self.voiceover(
            "The argument can be laid out as a Price List. <bookmark mark='a'/>Three claims. Mechanism: our "
            "mathematical knowledge is what some formal system F proves. We can know that F is consistent. And F "
            "is in fact consistent. Hold fixed Gödel's second theorem, and the three are inconsistent: if we knew "
            "F's consistency, F would prove it. <bookmark mark='b'/>Lucas and Penrose deny mechanism. "
            "<bookmark mark='c'/>Most logicians, from Paul Benacerraf in 1967 to Hilary Putnam and Solomon "
            "Feferman, deny the second claim: we have no way to know that the system that captures our own "
            "reasoning is consistent. We might be such a machine, and not know which one. "
            "<bookmark mark='d'/>And one can deny the third. Turing said in 1947 that if a machine is expected to "
            "be infallible, it cannot also be intelligent. Human mathematicians are not infallible either."
        ) as vo:
            self.play(FadeIn(pl.title), LaggedStart(*[FadeIn(c) for c in pl.cards], lag_ratio=0.25),
                      Create(pl.conflict))
            vo.wait_until("a")
            self.play(FadeIn(bg))
            for i, (mk, (mcs, name, who)) in enumerate(zip("bcd", positions)):
                vo.wait_until(mk)
                if i:
                    self.play(*pl.reset(), run_time=0.6)
                anims, centre = pl.position(mcs, name, who, width=3.2)
                self.play(*anims)
        self.clear_scene()

    def godel(self):
        hc = history_card(1951, r"Kurt Gödel, \ the Gibbs lecture", r"`Some basic theorems on the foundations of "
                          r"mathematics and their implications'", width=7.2, color=HIST).to_corner(UL, buff=0.35)
        disj = VGroup(label(r"either the human mind infinitely surpasses the powers of any finite machine,",
                            font_size=26, color=GOAL),
                      label(r"or there exist absolutely unsolvable mathematical problems", font_size=26,
                            color=GOAL)).arrange(DOWN, buff=0.25).move_to([0, 0.6, 0])
        br = label(r"Gödel's disjunction: \ the theorems prove this much, \ and no more", font_size=26,
                   color=OK).next_to(disj, DOWN, buff=0.6)
        himself = label(r"Gödel himself leaned to the first, \ but never claimed to have proved it", font_size=24,
                        color=GREY_A).next_to(br, DOWN, buff=0.4)
        with self.voiceover(
            "Gödel's own view was more careful. <bookmark mark='a'/>In his Gibbs lecture of 1951 he argued for a "
            "disjunction: either the human mind infinitely surpasses the powers of any finite machine, or there "
            "are absolutely unsolvable mathematical problems. <bookmark mark='b'/>The theorems prove this much, "
            "and no more. <bookmark mark='c'/>Gödel leaned towards the first, a mind beyond machines, but he never "
            "claimed his theorems proved it."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(disj))
            vo.wait_until("b")
            self.play(FadeIn(br))
            vo.wait_until("c")
            self.play(FadeIn(himself))
        self.clear_scene()

    def misuses(self):
        hc = history_card(2005, r"Torkel Franzén", r"\textit{Gödel's Theorem: \ An Incomplete Guide to Its Use and "
                          r"Abuse}", width=7.0, color=HIST).to_corner(UL, buff=0.35)
        rows = [(r"`Gödel proved that nothing can be known for certain'",
                 r"no: \ PA proves every true $\Sigma_1$ sentence, \ and most of mathematics is untouched"),
                (r"`any system of thought is incomplete'", r"only formal systems that contain arithmetic, \ and are "
                 r"consistent, \ and listable"),
                (r"`there are truths we can never know'", r"each $G_F$ is provable in a stronger system; \ the theorem "
                 r"is about one system at a time"),
                (r"`so mathematics is inconsistent'", r"the theorems \textit{assume} consistency; \ they say we cannot "
                 r"\textit{prove} it from within")]
        tab = VGroup()
        for i, (a, b) in enumerate(rows):
            y = 1.3 - 1.05 * i
            la = label(a, font_size=24, color=BAD).move_to([-6.3, y + 0.2, 0], aligned_edge=LEFT)
            lb = label(b, font_size=22, color=GREY_A).move_to([-5.9, y - 0.25, 0], aligned_edge=LEFT)
            tab.add(VGroup(la, lb))
        with self.voiceover(
            "Few theorems have been quoted as widely, or as wrongly. The logician Torkel Franzén wrote a whole book "
            "on the misuses. <bookmark mark='a'/>Gödel did not prove that nothing can be known for certain: PA "
            "proves every true sigma one sentence, and almost all ordinary mathematics is untouched. "
            "<bookmark mark='b'/>He did not prove that every system of thought is incomplete: only consistent, "
            "listable formal systems that contain enough arithmetic. <bookmark mark='c'/>He did not show that some "
            "truths are unknowable: each Gödel sentence is provable in a stronger system. The theorem concerns one "
            "system at a time. <bookmark mark='d'/>And he did not show that mathematics is inconsistent. The "
            "theorems assume consistency, and say only that a system cannot prove it from within."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcd", tab):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
        self.clear_scene()
