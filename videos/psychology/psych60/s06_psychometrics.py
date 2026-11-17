from __future__ import annotations

from videos.psychology.psych60.common import *  # noqa: F403


class Psychometrics(VoiceoverScene):
    def construct(self):
        card_section(self, 5, r"Psychometrics for machines", r"Is a benchmark a good test?", marr=("what",))
        self.validity()
        self.items()
        self.size()

    def validity(self):
        chips_section(self, r"A benchmark is a test", [
            (r"construct", r"what does the score stand for: \ ``reasoning'', \ ``knowledge'', \ ``safety''? \ "
                           r"Part 3's construct validity", MODEL),
            (r"reliability", r"would the ranking survive another sample of items?", PERSON),
            (r"saturation", r"once every model scores near the top, \ the test no longer separates them", AUTH),
            (r"Goodhart", r"a score that becomes a target stops measuring what it did", SYMP),
        ], "Is a benchmark a good test? It is a test, so ask Part 3's questions. <bookmark mark='a'/> The construct: "
           "what does the score stand for? Reasoning, knowledge, safety? <bookmark mark='b'/> Reliability: would the "
           "ranking survive another sample of items? <bookmark mark='c'/> Saturation: once every model scores near "
           "the top, the test no longer separates them. <bookmark mark='d'/> And Goodhart's law: a score that becomes "
           "a target stops measuring what it did.")

    def items(self):
        d = load("irt")
        head = heading(r"Which items do the work")
        A = axes([-4.5, 4.5], [0, 0.6], x_length=5.6, y_length=3.0, xticks=[-4, -2, 0, 2, 4], yticks=[0, 0.2, 0.4],
                 xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", xlabel=r"item difficulty",
                 ylabel=r"information about these models", center=[-3.3, 0.2, 0], font_size=12)
        b, info, a = np.asarray(d["b"]), np.asarray(d["info"]), np.asarray(d["a"])
        cols = [GOOD if x > np.quantile(info, 0.8) else GREY_B for x in info]
        dots = VGroup(*[Dot(A.ax.c2p(float(np.clip(bb, -4.4, 4.4)), float(min(ii, 0.59))), radius=0.035, color=c)
                        for bb, ii, c in zip(b, info, cols)])
        band = Rectangle(width=A.ax.c2p(1.5, 0)[0] - A.ax.c2p(-1.5, 0)[0], height=3.0, stroke_width=0,
                         fill_color=MODEL, fill_opacity=0.12).move_to(A.ax.c2p(0, 0.3))
        rows = rows_of([
            (r"Psyche's benchmark: \ 300 items fitted by Part 45's two-parameter model; \ twelve models with "
             r"abilities from -1.5 to 1.5 (shaded)", WHITE),
            (rf"the best fifth of the items carry {100 * d['useful_share_info']:.0f}\% of the information: \ "
             rf"discriminating, \ and pitched where the models are", GOOD),
            (r"items far too easy or too hard tell nothing about these models", AUTH),
            (r"a shorter, \ adaptive benchmark could rank them as well (Part 45's computerized adaptive testing)", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{machines.benchmark\_irt}")
        with self.voiceover(
            "Which items do the work? <bookmark mark='a'/> Psyche's benchmark has three hundred items, fitted by "
            "Part 45's two-parameter model, and twelve models with abilities in the shaded band. "
            "<bookmark mark='b'/> The best fifth of the items carry nearly half of the information. They "
            "discriminate, and they're pitched where the models are. <bookmark mark='c'/> Items far too easy or too "
            "hard tell us nothing about these models. <bookmark mark='d'/> A shorter, adaptive benchmark could rank "
            "them as well. That's Part 45's computerized adaptive testing."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(band))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(dots))
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def size(self):
        d = load("separate")
        rows_section(self, r"How many items to tell two models apart?", [
            (r"two models near 70\% accuracy, \ 3 points apart; \ 5\% significance, \ 80\% power", WHITE),
            (rf"scored on separate items: \ about {num(round(d['independent'], -2))} items", AUTH),
            (rf"paired on the same items, \ with correlated item scores: \ about {num(round(d['paired'], -2))}", GOOD),
            (r"many leaderboards separate models by less than their items can resolve; \ report intervals, \ and "
             r"pair the comparison (Part 4)", YOU),
        ], "How many items does it take to tell two models apart? <bookmark mark='a'/> Take two models near seventy "
           "percent accuracy, three points apart, with five percent significance and eighty percent power. "
           "<bookmark mark='b'/> Scored on separate items, it takes about thirty-seven hundred items. "
           "<bookmark mark='c'/> Paired on the same items, with correlated item scores, about eighteen hundred. "
           "<bookmark mark='d'/> Many leaderboards separate models by less than their items can resolve. Report "
           "intervals, and pair the comparison, as Part 4 taught.", tag=psyche_tag(r"\texttt{machines.items\_to\_separate}"))
