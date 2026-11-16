from __future__ import annotations

import numpy as np

from videos.music.music65.common import *  # noqa: F403


class Judging(SoundScene):
    def construct(self):
        chapter(self, 10, r"Judging machines", r"How do you tell whether a composing machine is any good?")
        self.quiz()
        self.table()
        self.pitfalls()
        self.listening()

    # ------------------------------------------------------------------
    def table(self):
        d = load("judge")
        cols = {"order 1": GREY_B, "order 2": WHITE, "order 8": EAR, "recombined": BLUE, "transformer": TUNE, "Bach (held out)": GOLD}
        names = {"order 1": r"Markov, \ order 1", "order 2": r"Markov, \ order 2", "order 8": r"Markov, \ order 8", "recombined": r"recombined", "transformer": r"transformer", "Bach (held out)": r"Bach \ (kept back)"}
        g = VGroup()
        for k in d["order"]:
            r = d["rows"][k]
            g.add(VGroup(label(names[k], font_size=18, color=cols[k]), label(f"{r['kl']:.2f}", font_size=18, color=cols[k]), label(f"{100 * r['cadence']:.0f}\\%", font_size=18, color=cols[k]),
                         label(f"{100 * r['share8']:.0f}\\%", font_size=18, color=cols[k]), label(f"{r['longest']:.1f}", font_size=18, color=cols[k])))
        g.arrange(DOWN, buff=0.28)
        for r in g:
            for i, x in enumerate((-4.6, -1.9, 0.4, 2.6, 4.8)):
                r[i].set_x(x)
        g.move_to(DOWN * 0.5)
        top = VGroup(*[label(t, font_size=14, color=GREY_A).move_to([x, g.get_top()[1] + 0.55, 0]) for t, x in
                       ((r"interval divergence \ (bits)", -1.9), (r"phrases ending \ on the tonic chord", 0.4), (r"inside a copied \ run of 8", 2.6), (r"longest copied \ run", 4.8))])
        head = label(r"every machine, \ the same judges", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        rw = d["rows"]
        with self.voiceover(
            "Put every machine before the same judges, twenty tunes each, beside Bach's own tunes kept back. "
            "<bookmark mark='a'/> How far its melodic intervals are from Bach's; how often its phrases end on the tonic "
            "chord; how much of it is copied. <bookmark mark='b'/> On intervals and cadences every machine is close to Bach, "
            "even order one, and the recombiner closest of all. Only the copying column tells them apart: "
            f"{say(round(100 * rw['order 8']['share8']))} per cent copied for order eight, "
            f"{say(round(100 * rw['recombined']['share8']))} for the recombiner, {say(round(100 * rw['transformer']['share8']))} "
            f"for the transformer, whose intervals are the furthest from Bach's, {say(rw['transformer']['kl'], 2)} bits. "
            "No single number ranks them; a table like this one, with the copying column always in it, is the least "
            "an honest report needs."
        ) as vo:
            self.play(FadeIn(head), FadeIn(top))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in g], lag_ratio=0.2), run_time=2.0)
            vo.wait_until("b")
            self.play(*[Indicate(r[3], color=EAR) for r in g])
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def pitfalls(self):
        items = [
            (r"statistics can be matched by copying: \ every judge here rewards a perfect copy, \ except the copying column", WHITE),
            (r"likelihood rewards prediction, \ not quality: \ a model can predict well and compose dully", WHITE),
            (r"cherry-picking: \ the best of a hundred samples says little about the hundredth", WHITE),
            (r"`could listeners tell?' \ tests depend on the listeners, \ the excerpt length and the alternatives", WHITE),
            (r"report: \ uncurated samples, \ likelihood on unseen music, \ copying, \ and a listening test with its design", TUNE),
        ]
        rows_scene(self, r"pitfalls", items,
                   "Each judge has its traps. <bookmark mark='b'/> Statistics can be matched by copying: every judge here rewards a "
                   "perfect copy of Bach, except the copying column. <bookmark mark='c'/> Likelihood on unseen music rewards "
                   "prediction, not quality: a model can predict well and compose dully. <bookmark mark='d'/> Cherry-picking: the "
                   "best of a hundred samples says little about the hundredth, and demonstrations are usually the best. "
                   "<bookmark mark='e'/> Could-listeners-tell tests depend on who listens, how long the excerpt is, and what it is "
                   "set beside. <bookmark mark='f'/> So report uncurated samples, likelihood on music the model never saw, how much "
                   "is copied, and a listening test with its design.", marks="bcdef")

    # ------------------------------------------------------------------
    def listening(self):
        items = [
            (r"a Turing-style test asks only whether a machine passes for a person: \ the hook's question", WHITE),
            (r"better: \ rate qualities \ (coherence, \ interest, \ style) \ blind, \ against real music of the same kind", WHITE),
            (r"experts and novices hear differently: \ say who listened \ (Part 58's listening tests)", WHITE),
            (r"and long-range form is another important property to evaluate: \ judge whole pieces, \ not eight bars", TUNE),
        ]
        rows_scene(self, r"listening tests", items,
                   "And listening tests. <bookmark mark='b'/> A Turing-style test asks only whether the machine passes for a person, as the hook of this part did. <bookmark mark='c'/> Better to rate qualities, coherence, interest and style, blind, against real music of the same kind. <bookmark mark='d'/> Experts and novices hear differently, so say who listened, as Part 58's listening tests did. <bookmark mark='e'/> And long-range form is another important property to evaluate, so judge whole pieces, not eight bars.", marks="bcde")

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("copyquiz")
        c = clip("copyquiz.two")
        card = listen_card(r"Two machine tunes, \ harmonized. \ One is mostly copied from Bach, \ note for note; \ one is not. \ Which is copied?", width=9.6)
        with self.voiceover("Your turn. Two machine tunes, harmonized the same way. One is mostly copied from Bach, note for note; the other is not. Which is the copy?"):
            self.play(FadeIn(card))
        self.wait(0.8)
        boxes = choice_boxes([r"first", r"second"]).move_to(UP * 0.6)
        self.play(FadeOut(card), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"new, \ or copied?", kind="synthesized", detail=r"two machines; \ Part 17's harmony", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["first"], st["second"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["second"], c.duration, buff=0.08)
        res = label(rf"the second: \ an order-8 chain, \ {100 * d['copied']:.0f}\% inside copied runs \ (longest {d['longest']['length']} notes); \ the first, \ the transformer, \ {100 * d['copied_new']:.0f}\%",
                    font_size=17, color=TUNE).move_to(DOWN * 1.4)
        with self.voiceover(
            f"The second was the copy: an order-eight chain, {say(round(100 * d['copied']))} per cent of it inside runs copied "
            f"from Bach. The first, from the transformer, {say(round(100 * d['copied_new']))} per cent. If you could not tell, "
            "that is the point: copying can be hard to identify by ear without knowing the source, so it has to be measured."
        ):
            self.play(boxes[1][0].animate.set_stroke(TUNE, width=4), FadeIn(res))
        self.wait(0.4)
        self.clear_scene()
