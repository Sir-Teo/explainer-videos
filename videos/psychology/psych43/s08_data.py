from __future__ import annotations

from videos.psychology.psych43.common import *  # noqa: F403


def lab_forest(y, v, center, color, x_range, label_text, width=5.4, height=4.6, scale=1.0, xfmt=None):
    """A forest of per-lab estimates with 95% intervals, sorted, in an axes box."""
    order = np.argsort(y)
    y, v = np.asarray(y)[order] * scale, np.asarray(v)[order] * scale ** 2
    k = len(y)
    A = axes(list(x_range), [0, k + 1], x_length=width, y_length=height, xticks=None, yticks=None,
             xlabel=label_text, center=center, font_size=12)
    g = VGroup()
    for i, (a, b) in enumerate(zip(y, v)):
        se = np.sqrt(b)
        lo, hi = max(x_range[0], a - 1.96 * se), min(x_range[1], a + 1.96 * se)
        g.add(Line(A.ax.c2p(lo, i + 1), A.ax.c2p(hi, i + 1), color=GREY_B, stroke_width=1.5),
              Dot(A.ax.c2p(float(np.clip(a, *x_range)), i + 1), radius=0.045, color=color))
    zero = DashedLine(A.ax.c2p(0, 0), A.ax.c2p(0, k + 1), color=GREY_B, stroke_width=1.5)
    return A, g, zero


class Data(VoiceoverScene):
    def construct(self):
        self.card()
        self.labs()
        self.sizes()

    def card(self):
        card = chapter_card(7, r"The data", r"Where do the numbers come from?",
                            lit={2014: r"Alogna et al.", 2016: r"Hagger et al."}, part=PART, scale=("person",),
                            marr=("what",))
        with self.voiceover("Chapter seven. The data."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def labs(self):
        c = load("confirm")
        head = heading(r"Two registered multi-lab replications")
        A1, g1, z1 = lab_forest(c["vo_y"], c["vo_v"], [-3.4, -0.2, 0], GOOD, (-50, 30),
                                r"fewer correct picks per 100 (describe minus control)", scale=100.0)
        A2, g2, z2 = lab_forest(c["ed_y"], c["ed_v"], [3.4, -0.2, 0], AUTH, (-1.0, 1.0),
                                r"Hedges's $g$ (depleted minus control)")
        t1 = label(rf"verbal overshadowing: \ {c['vo_k']} labs, \ {num(c['vo_N'])} people", font_size=17,
                   color=GOOD).next_to(A1, UP, buff=0.15)
        t2 = label(rf"ego depletion: \ {c['ed_k']} labs, \ {num(c['ed_N'])} people", font_size=17,
                   color=AUTH).next_to(A2, UP, buff=0.15)
        foot = wrapped_label(r"each line one laboratory, \ with its 95\% interval; \ the data are open, \ fetched and "
                             r"checked on first use, \ and fixed", 6.4, 17, YOU).to_edge(DOWN, buff=0.2).to_edge(RIGHT, buff=0.4)
        tag = published_tag(r"Alogna et al.\ (2014); \ Hagger et al.\ (2016)")
        with self.voiceover(
            "The film can't collect its own data, so it uses two registered multi-lab replications whose data are "
            "open. <bookmark mark='a'/> Verbal overshadowing: twenty-two laboratories, about two thousand people, each "
            "lab's difference in correct line-up picks between those who described the face and those who didn't. "
            "<bookmark mark='b'/> Ego depletion: twenty-three laboratories, about two thousand one hundred people, "
            "each lab's standardized difference in self-control after the demanding or the easy task. "
            "<bookmark mark='c'/> Each line is one laboratory, with its interval. The data are fetched from the "
            "archive, checked on first use, and fixed. The plan was written before this chapter."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(A1), FadeIn(z1), FadeIn(t1), LaggedStart(*[FadeIn(x) for x in g1], lag_ratio=0.02),
                      run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(A2), FadeIn(z2), FadeIn(t2), LaggedStart(*[FadeIn(x) for x in g2], lag_ratio=0.02),
                      run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

    def sizes(self):
        d = load("labs")
        head = heading(r"Forty-five laboratories, \ lab by lab")
        A = axes([0, 23], [0, 200], x_length=5.6, y_length=2.2, xticks=None, yticks=[0, 100, 200],
                 yfmt=lambda v: f"{v:.0f}", ylabel=r"people", center=[-3.3, 1.2, 0], font_size=13)
        B = axes([0, 24], [0, 200], x_length=5.6, y_length=2.2, xticks=None, yticks=[0, 100, 200],
                 yfmt=lambda v: f"{v:.0f}", ylabel=r"people", center=[-3.3, -1.9, 0], font_size=13)
        b1 = bars(A.ax, np.arange(1, len(d["vo_n"]) + 1), d["vo_n"], [GOOD] * len(d["vo_n"]), width=0.7)
        b2 = bars(B.ax, np.arange(1, len(d["ed_n"]) + 1), d["ed_n"], [AUTH] * len(d["ed_n"]), width=0.7)
        l1 = label(rf"verbal overshadowing: \ {len(d['vo_n'])} labs, \ {num(d['vo_total'])} people", font_size=14,
                   color=GOOD).next_to(A, UP, buff=0.05)
        l2 = label(rf"ego depletion: \ {len(d['ed_n'])} labs, \ {num(d['ed_total'])} people", font_size=14,
                   color=AUTH).next_to(B, UP, buff=0.05)
        rows = rows_of([
            (rf"labs ranged from {int(min(d['vo_n'].min(), d['ed_n'].min()))} to "
             rf"{int(max(d['vo_n'].max(), d['ed_n'].max()))} people: \ every one larger than either original study", WHITE),
            (r"each lab ran the same protocol, \ in its own language and setting, \ with its own experimenters", SYMP),
            (r"pooling weights each lab by its precision; \ no lab's result, \ alone, \ decides", MODEL),
            (r"the variation between labs is itself a finding: \ how much of an effect travels", YOU),
        ], 6.0, 19, 0.38).move_to([3.4, -0.1, 0])
        with self.voiceover(
            "Look at the labs themselves. <bookmark mark='a'/> They ranged from about fifty to about one hundred and "
            "eighty people each. Every one was larger than either original study. <bookmark mark='b'/> Each ran the "
            "same protocol, in its own language and setting, with its own experimenters. <bookmark mark='c'/> Pooling "
            "weights each lab by its precision, so no lab's result alone decides. <bookmark mark='d'/> And the "
            "variation between labs is a finding in itself: how far an effect travels."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(B), FadeIn(l1), FadeIn(l2))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), LaggedStart(*[FadeIn(x) for x in b1], lag_ratio=0.05),
                      LaggedStart(*[FadeIn(x) for x in b2], lag_ratio=0.05), run_time=2.0)
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
