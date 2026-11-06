from __future__ import annotations

from videos.philosophy.philosophy12.common import *  # noqa: F403


class Fitch(VoiceoverScene):
    def construct(self):
        card = chapter_card(11, r"Unknowable truths", r"Can every truth be known?", lit=(1963,), part=PART)
        with self.voiceover("Chapter eleven. Unknowable truths."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.moore()
        self.derivation()
        self.price()

    def moore(self):
        d = load("moore")
        head = label(r"A sentence that cannot survive being said", font_size=32, color=CONN).to_edge(UP, buff=0.4)
        s = MathTex(r"p \land \lnot K_b\, p", font_size=46, color=GOAL).next_to(head, DOWN, buff=0.4)
        gl = label(r"`it's raining, \ and you don't know it'", font_size=24, color=GREY_A).next_to(s, DOWN, buff=0.2)
        pos = {"w1": [-1.0, 0, 0], "w0": [1.0, 0, 0]}
        before = AgentGraph(["w1", "w0"], {"b": [("w1", "w0")]}, pos, {"w1": r"p", "w0": r"\lnot p"}, radius=0.4,
                            font_size=26, center=[-3.4, -0.8, 0])
        after = AgentGraph(["w1"], {}, {"w1": [0, 0, 0]}, {"w1": r"p"}, radius=0.4, font_size=26,
                           center=[3.4, -0.8, 0])
        bl = VGroup(label(r"before: \ true at the $p$ world", font_size=21, color=OK), mark(d["before"], 26)).arrange(
            RIGHT, buff=0.2).next_to(before, DOWN, buff=0.35)
        al = VGroup(label(r"after it is announced: \ Bob knows $p$, \ so it is false", font_size=21, color=BAD),
                    mark(not d["after"], 26)).arrange(RIGHT, buff=0.2).next_to(after, DOWN, buff=0.35)
        arr = Arrow([-1.4, -0.8, 0], [2.4, -0.8, 0], buff=0.1, color=GREY_B)
        arl = label(r"announce it", font_size=20, color=GREY_B).next_to(arr, UP, buff=0.1)
        foot = label(r"a Moore sentence: \ true, \ but impossible to know, \ or to learn by being told",
                     font_size=24, color=GOAL).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Some truths destroy themselves when spoken. <bookmark mark='a'/>Take the sentence: p, and you don't "
            "know p. It's raining, and you don't know it. G. E. Moore noticed that one cannot sensibly assert such a "
            "thing about oneself. <bookmark mark='b'/>Here it is in a model. Bob cannot tell whether p. At the world "
            "where p holds, the sentence is true. <bookmark mark='c'/>Now announce it to Bob. The not-p world is "
            "deleted, Bob knows p, and the sentence, which was true, has become false. The Reasoner confirms both "
            "values. <bookmark mark='d'/>A Moore sentence can be true, but it can never be known by the person it is "
            "about, nor learned by being told. That small fact has a large consequence."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(s), FadeIn(gl))
            vo.wait_until("b")
            self.play(FadeIn(before), FadeIn(bl))
            vo.wait_until("c")
            self.play(GrowArrow(arr), FadeIn(arl))
            self.play(FadeIn(after), FadeIn(al))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def derivation(self):
        d = load("fitch")
        head = label(r"Fitch's paradox \ (1963; \ Church's referee report, \ 1945)", font_size=30,
                     color=CONN).to_edge(UP, buff=0.35)
        steps = VGroup(
            MathTex(r"1.\ \ \forall p\,(p \rightarrow \Diamond K p)", r"\quad\text{every truth is knowable}",
                    font_size=30),
            MathTex(r"2.\ \ q \land \lnot K q", r"\quad\text{some truth is unknown}", font_size=30),
            MathTex(r"3.\ \ \Diamond K(q \land \lnot K q)", r"\quad\text{from 1 and 2}", font_size=30),
            MathTex(r"4.\ \ K(q \land \lnot Kq) \rightarrow Kq \land K\lnot Kq", r"\quad\text{$K$ distributes}",
                    font_size=30),
            MathTex(r"5.\ \ K\lnot K q \rightarrow \lnot K q", r"\quad\text{$K$ is factive}", font_size=30),
            MathTex(r"6.\ \ \text{so } K(q \land \lnot K q) \text{ is impossible: contradicts 3}", font_size=30,
                    color=BAD),
            MathTex(r"\therefore\ \ \forall p\,(p \rightarrow K p)", r"\quad\text{all truths are known}",
                    font_size=32, color=GOAL)).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([-1.2, -0.4, 0])
        for st in steps:
            if len(st) > 1:
                st[1].set_color(GREY_A)
        chk = VGroup(label(r"the Reasoner's tableau:", font_size=20, color=KNOW),
                     VGroup(MathTex(r"\lnot K(q \land \lnot Kq)", font_size=26), label(r"valid with T", font_size=19),
                            mark(d["valid_in_T"], 24)).arrange(RIGHT, buff=0.2),
                     VGroup(MathTex(r"\lnot K(q \land \lnot Kq)", font_size=26), label(r"in K alone", font_size=19),
                            mark(d["valid_in_K"], 24)).arrange(RIGHT, buff=0.2)).arrange(DOWN, aligned_edge=LEFT,
                                                                                           buff=0.15)
        chk.to_corner(DR, buff=0.4)
        with self.voiceover(
            "Frederic Fitch published it in 1963; the idea came from an anonymous referee report written by Alonzo "
            "Church in 1945. <bookmark mark='a'/>Suppose every truth is knowable: if p is true, it is possible to know "
            "p. <bookmark mark='b'/>Suppose too that we are not omniscient: some truth q is not known by anyone. "
            "<bookmark mark='c'/>Then the conjunction, q and nobody knows q, is itself true, so by the first "
            "assumption it is knowable. <bookmark mark='d'/>But to know a conjunction is to know both parts: to know "
            "q, and to know that q is not known. <bookmark mark='e'/>And since knowledge is factive, knowing that q "
            "is not known means q is not known, contradicting the knowing of q. <bookmark mark='f'/>So that "
            "conjunction can never be known: the Moore sentence again. The Reasoner's tableau confirms that "
            "knowing it is impossible on every reflexive frame, though not without reflexivity: factivity is doing "
            "the work. <bookmark mark='g'/>So, if every truth is knowable, every truth is already known. The paradox "
            "of knowability."
        ) as vo:
            self.play(FadeIn(head))
            for mk, st in zip("abcdefg", steps):
                vo.wait_until(mk)
                self.play(FadeIn(st, shift=RIGHT * 0.1))
                if mk == "f":
                    self.play(FadeIn(chk))
        self.clear_scene()

    def price(self):
        d = load("fitchprice")
        claims = [(c["key"], c["text"]) for c in d["claims"]]
        pl = PriceList(claims, mus=[tuple(m) for m in d["mus"]], radius=2.5, width=4.0, font_size=22,
                       center=[0, -0.4, 0], title=r"The Price List: \ Fitch's triad")
        assert d["mcs"] == [["F1"], ["F2"], ["F3"]]
        positions = [(("F1",), r"realism", r"some truths are unknowable: \ the price of a mind-independent world"),
                     (("F2",), r"omniscience", r"everything true is known, \ by someone (or by God)"),
                     (("F3",), r"intuitionism", r"the argument then shows only $p \rightarrow \lnot\lnot Kp$: \ no "
                                                r"truth is definitely unknown")]
        foot = label(r"and the restrictions: \ knowability only for `Cartesian' truths (Tennant 1997), \ basic "
                     r"ones (Dummett 2001)", font_size=20, color=GREY_A).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "As a Price List: <bookmark mark='a'/>every truth can be known; some truth is not known by anyone; "
            "knowledge is factive and distributes over conjunction, in classical logic. The Reasoner confirms that "
            "the three are inconsistent, and that dropping any one restores consistency. <bookmark mark='b'/>The "
            "realist gives up the first: there are truths no one could know, which is just what it is for the "
            "world to outrun our minds. This is the usual verdict, and why the paradox is aimed at anti-realists, "
            "who define truth in terms of what can be known. <bookmark mark='c'/>Giving up the second means that "
            "every truth is known by someone, which few accept unless that someone is God. <bookmark mark='d'/>The "
            "intuitionist rejects the classical logic of the last step: the argument then shows only that every truth "
            "is not unknown, which, without double negation elimination, is weaker than saying that it is known. <bookmark mark='e'/>And anti-realists such as Neil Tennant and "
            "Michael Dummett restrict knowability to certain kinds of truth, to avoid the Moore-type conjunctions."
        ) as vo:
            self.play(FadeIn(pl.title))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in pl.cards], lag_ratio=0.4), Create(pl.conflict))
            first = True
            for mk, (mcs, name, who) in zip("bcd", positions):
                vo.wait_until(mk)
                if not first:
                    self.play(*pl.reset())
                first = False
                anims, centre = pl.position(mcs, name, who, width=2.6)
                self.play(*anims)
            vo.wait_until("e")
            self.play(*pl.reset())
            self.play(FadeIn(foot))
        self.clear_scene()
