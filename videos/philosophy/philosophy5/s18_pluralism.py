from __future__ import annotations

from videos.philosophy.philosophy5.common import *  # noqa: F403


class Pluralism(VoiceoverScene):
    def construct(self):
        card = chapter_card(17, r"One logic or many?", r"Is there a single correct logic?", lit=(2006,),
                            part=PART)
        with self.voiceover("Chapter seventeen. One logic or many?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.carnap()
        self.gtt()
        self.monism()
        self.abduction()

    def carnap(self):
        q = quote_card(r"In logic, there are no morals. \ Everyone is at liberty to build up his own logic, \ i.e.\ his "
                       r"own form of language, as he wishes.", r"Rudolf Carnap, \textit{The Logical Syntax of Language} "
                       r"(1934)", r"the principle of tolerance", width=10.4, font_size=28).move_to([0, 1.2, 0])
        quine = quote_card(r"Change of logic, change of subject.", r"W.\ V.\ Quine, \textit{Philosophy of Logic} "
                           r"(1970)", width=8.0, font_size=28, color=BAD).next_to(q, DOWN, buff=0.7)
        with self.voiceover(
            "This part has built a dozen logics. Is one of them right? <bookmark mark='a'/>Rudolf Carnap's answer, "
            "in 1934, was his principle of tolerance: in logic there are no morals; everyone may build the logic, "
            "the form of language, that suits his purpose. <bookmark mark='b'/>Quine's reply, in 1970, was that "
            "there is no real disagreement to have: a deviant logician who rejects excluded middle has simply "
            "changed the meaning of 'not'. Change of logic, change of subject."
        ) as vo:
            self.play(FadeIn(q))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(quine))
        self.clear_scene()

    def gtt(self):
        hc = history_card(2006, r"JC Beall \& Greg Restall", r"\textit{Logical Pluralism}", width=5.4,
                          color=HIST).to_corner(UL, buff=0.35)
        gt = VGroup(label(r"the Generalized Tarski Thesis:", font_size=26, color=GOAL),
                    MathTex(r"\text{valid}_x \iff \text{in every case}_x \text{ where the premises are true, so is the "
                            r"conclusion}", font_size=30)).arrange(DOWN, buff=0.25).next_to(hc, DOWN, buff=0.5)
        gt.set_x(0)
        cases = VGroup()
        for c, lg, col in ((r"cases = complete, consistent worlds", r"classical logic", OK),
                           (r"cases = stages of construction", r"intuitionistic logic", P.CLAIM),
                           (r"cases = situations, possibly incomplete or inconsistent", r"relevant logic", BOTH)):
            cases.add(VGroup(label(c, font_size=24), MathTex(r"\Rightarrow", font_size=30, color=GREY_B),
                             label(lg, font_size=26, color=col)).arrange(RIGHT, buff=0.3))
        cases.arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(gt, DOWN, buff=0.55)
        cases.set_x(0)
        moral = label(r"all three are correct, \ each for its own cases", font_size=26, color=GOAL).to_edge(DOWN,
                                                                                                     buff=0.45)
        with self.voiceover(
            "In 2006 JC Beall and Greg Restall defended a precise pluralism. <bookmark mark='a'/>Start from Tarski's "
            "definition, and generalize it: an argument is valid relative to a kind of case if in every such case "
            "where the premises are true, the conclusion is true. <bookmark mark='b'/>If the cases are complete, "
            "consistent worlds, you get classical logic. If they are stages of construction, like Kripke's stages "
            "in Chapter 8, intuitionistic logic. If they are situations that may be incomplete or inconsistent, "
            "a relevant logic. <bookmark mark='c'/>All three, they argue, are correct, each capturing a genuine "
            "sense of 'follows'."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(gt))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.15) for c in cases], lag_ratio=0.5), run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(moral))
        self.clear_scene()

    def monism(self):
        head = label(r"The monist's reply: \ the collapse argument", font_size=32, color=CONN).to_edge(UP, buff=0.5)
        steps = VGroup(label(r"suppose both classical and relevant logic are correct", font_size=26),
                       label(r"I know $p \lor q$ and $\lnot p$, \ about the actual world", font_size=26),
                       label(r"the actual world is a case of every kind", font_size=26),
                       label(r"so may I conclude $q$? \ If yes, the strongest logic wins; \ if no, the weakest",
                             font_size=26, color=BAD),
                       label(r"either way, \ one logic does the work: \ Priest (2006), \ Read (2006), \ Williamson",
                             font_size=24, color=GOAL)).arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(head, DOWN,
                                                                                                     buff=0.6)
        with self.voiceover(
            "The monists answer with what is called the collapse argument. <bookmark mark='a'/>Suppose classical "
            "and relevant logic are both correct. <bookmark mark='b'/>I know, about the real world, that p or q, "
            "and that not p. <bookmark mark='c'/>The real world is a case of every kind. "
            "<bookmark mark='d'/>So may I conclude q? Classical logic says yes; relevant logic says the argument is "
            "invalid. If I may, the stronger logic is the one I reason with; if not, the weaker one is. "
            "<bookmark mark='e'/>Either way, when it comes to drawing conclusions, one logic does the work. Graham "
            "Priest and Stephen Read made versions of this argument; Timothy Williamson defends classical logic as "
            "the one."
        ) as vo:
            self.play(FadeIn(head))
            for mk, s_ in zip("abcde", steps):
                vo.wait_until(mk)
                self.play(FadeIn(s_, shift=RIGHT * 0.15))
        self.clear_scene()

    def abduction(self):
        d = load("compare")
        head = label(r"Anti-exceptionalism: \ choose a logic as you choose a theory", font_size=30,
                     color=CONN).to_edge(UP, buff=0.45)
        who = label(r"Williamson (2017); \ Hjortland (2017); \ Priest (2016)", font_size=22, color=GREY_B).next_to(
            head, DOWN, buff=0.2)
        counts = [sum(r["cells"][j]["valid"] for r in d["rows"]) for j in range(len(d["logics"]))]
        assert dict(zip(d["logics"], counts)) == {"CL": 6, "K3": 3, "LP": 3, "Ł3": 4, "FDE": 0}
        bars = bar_row(counts, d["logics"], [OK, P.CLAIM, BOTH, HALF, NEITHER], width=3.8, height=0.4,
                       font_size=24, vmax=len(d["rows"])).move_to([-3.6, -0.6, 0])
        bl = label(rf"strength: \ how many of the {len(d['rows'])} inferences of Chapter 2 each keeps", font_size=22,
                   color=GREY_A).next_to(bars, UP, buff=0.35)
        crit = VGroup(label(r"strength: \ more valid inferences", font_size=24),
                      label(r"simplicity: \ fewer special cases", font_size=24),
                      label(r"fit with the data: \ mathematics, \ paradoxes, \ judgments", font_size=24),
                      label(r"classical logic is strongest; \ the paradoxes", font_size=24, color=GOAL),
                      label(r"are its data problem", font_size=24, color=GOAL)).arrange(DOWN, aligned_edge=LEFT,
                                                                                      buff=0.28).move_to([3.1, -0.6, 0])
        with self.voiceover(
            "The newest view treats logic as continuous with science. <bookmark mark='a'/>Timothy Williamson and "
            "Ole Thomas Hjortland, among others, argue that we choose a logic as we choose any theory, by "
            "abduction: comparing theories for strength, simplicity and fit with the data. "
            "<bookmark mark='b'/>Strength is measurable. Of the six inferences of Chapter 2, classical logic keeps "
            "all six, Łukasiewicz four, K3 and LP three each, and FDE none. <bookmark mark='c'/>The data are "
            "mathematics, which classical logic serves superbly, our judgments about arguments, and the paradoxes, "
            "which it serves badly. <bookmark mark='d'/>On this view, the choice among the logics of this part is "
            "a live scientific question, and the next three parts collect the hardest data: sets, proof, and the "
            "liar."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(who), LaggedStart(*[FadeIn(c) for c in crit[:3]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(bl), FadeIn(bars))
            vo.wait_until("c")
            self.play(Indicate(crit[2], color=GOAL))
            vo.wait_until("d")
            self.play(FadeIn(crit[3:]))
        self.clear_scene()
