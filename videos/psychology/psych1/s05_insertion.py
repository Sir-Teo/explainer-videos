from __future__ import annotations

import numpy as np

from videos.psychology.psych1.common import *  # noqa: F403

SHORT = {"discriminate": r"tell apart", "go or no-go": r"go or no-go", "choose": r"choose", "program": r"program",
         "sense": r"sense", "respond": r"respond"}


class Insertion(VoiceoverScene):
    def construct(self):
        self.card()
        self.assumption()
        self.distribution()
        self.variance_test()
        self.additive()

    def card(self):
        card = chapter_card(4, r"What subtraction assumes", r"When a task gets harder, is a stage added, or does "
                            r"everything change?", lit={1880: r"Wundt's objection", 1969: r"Sternberg's additive "
                                                        r"factors"},
                            part=PART, scale=("mind",), marr=("how",))
        with self.voiceover(
            "Chapter four. What subtraction assumes."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    # ------------------------------------------------------------------
    def reading(self, rows, unit, y, font_size=22):
        """One task under one model: the simple reaction as a single block, then the model's inserted stages."""
        base = sum(ms for name, ms in rows if name in ("sense", "respond"))
        stages = [(r"simple reaction", base, METHOD["a"])]
        stages += [(SHORT[name], ms, STAGE_COLOR[name]) for name, ms in rows if name not in ("sense", "respond")]
        bar = stage_bar(stages, unit=unit, height=0.62, font_size=font_size)
        bar.remove(bar.names)  # the stages are named by the colour key above the bars
        bar.shift([-4.4 - bar.cells[0].get_left()[0], y - bar.cells[0].get_y(), 0])
        return bar

    def assumption(self):
        d = load("donders")
        unit = 0.031
        defn = definition_card(r"Pure insertion", r"Going from the easier task to the harder one adds a stage, "
                               r"and leaves every other stage exactly as it was.", color=P.ACCENT, width=10.4,
                               font_size=34).move_to([0, 0.75, 0])
        wundt = quote_card(r"In method c you still decide something: whether to speak or to keep silent. That is a "
                           r"choice.", r"Wilhelm Wundt's objection, 1880 (paraphrase)", width=10.4, font_size=32,
                           color=GONOGO).move_to([0, -2.0, 0])
        recap = VGroup(
            MathTex(rf"c - a = {d['discriminate']:.0f}\ \text{{ms}}", r"\quad\text{to tell apart}", font_size=44),
            MathTex(rf"b - c = {d['choose']:.0f}\ \text{{ms}}", r"\quad\text{to choose}", font_size=44),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        recap[0].set_color(DISC)
        recap[1].set_color(CHOOSE)
        ys = {("c", 0): 1.55, ("c", 1): 0.45, ("b", 0): -1.05, ("b", 1): -2.15}
        key = VGroup()
        for name in ("discriminate", "go or no-go", "choose", "program"):
            sw = Square(side_length=0.26, stroke_width=0, fill_color=STAGE_COLOR[name], fill_opacity=0.9)
            key.add(VGroup(sw, label(SHORT[name], font_size=26, color=STAGE_COLOR[name])).arrange(RIGHT, buff=0.14))
        base_key = VGroup(Square(side_length=0.26, stroke_width=0, fill_color=METHOD["a"], fill_opacity=0.9),
                          label(r"the simple reaction", font_size=26, color=METHOD["a"])).arrange(RIGHT, buff=0.14)
        key = VGroup(base_key, *key).arrange(RIGHT, buff=0.55).to_edge(UP, buff=0.5)
        bars = {(k, i): self.reading(d["stages" if i == 0 else "rival_stages"][k], unit, y)
                for (k, i), y in ys.items()}
        tags = {}
        for (k, i), b in bars.items():
            who = r"Donders" if i == 0 else r"a rival"
            t = VGroup(label(k, font_size=40, color=METHOD[k]), label(who, font_size=22, color=GREY_A))
            t.arrange(RIGHT, buff=0.2, aligned_edge=DOWN).next_to(b.cells[0], LEFT, buff=0.3)
            tot = MathTex(rf"{d[k]:.0f}", font_size=34, color=P.HUMAN).next_to(b.cells[-1], RIGHT, buff=0.25)
            tags[(k, i)] = VGroup(t, tot)
        same = label(r"the same three averages", font_size=30, color=P.HUMAN)
        same.next_to(VGroup(*[tags[k][1] for k in tags]), RIGHT, buff=0.35)
        arrows = VGroup(*[Line(same.get_left() + LEFT * 0.05, tags[k][1].get_right() + RIGHT * 0.05, color=GREY_C,
                               stroke_width=1.5) for k in tags])
        note_ = quote_card(r"In Donders' own laboratory notebook, never published, his students show no difference "
                           r"between b and c.", r"Roelofs (2018), \emph{Acta Psychologica} 191", width=10.4,
                           font_size=34, color=STATUS_COLOR["contested"]).move_to([0, 0.9, 0])
        gap = VGroup(
            VGroup(label(r"Donders himself", font_size=30, color=P.HUMAN),
                   MathTex(rf"b - c = {d['choose']:.0f}\ \text{{ms}}", font_size=40, color=CHOOSE)).arrange(DOWN, buff=0.15),
            VGroup(label(r"his students", font_size=30, color=P.HUMAN),
                   MathTex(r"b - c \approx 0", font_size=40, color=STATUS_COLOR["contested"])).arrange(DOWN, buff=0.15),
        ).arrange(RIGHT, buff=1.6).move_to([0, -1.9, 0])
        tag = psyche_tag(r"models: \ the rival's split is one of many that fit")
        with self.voiceover(
            "Donders' subtraction rests on one assumption, and it has a name: pure insertion. "
            "<bookmark mark='a'/> Going from the easier task to the harder one slips a stage into the chain, and "
            "everything else stays exactly as it was. Is that true? <bookmark mark='b'/> Wilhelm Wundt didn't "
            "think so. In method c, he pointed out, you still have to decide something: whether to speak, or keep "
            "silent. That is a choice. So c minus a is not pure discrimination, and b minus c is not the whole of "
            "choosing. <bookmark mark='c'/> Here are Donders' two harder tasks, read his way. "
            "<bookmark mark='d'/> And here is a rival reading, built on Wundt's objection. Go/no-go contains a "
            "small decision of its own. And in the choice task the response can't be prepared in advance, so it "
            "has to be programmed. Different stages, with different durations. <bookmark mark='e'/> And exactly "
            "the same three averages. Three numbers cannot tell these two stories apart. "
            "<bookmark mark='f'/> There's a postscript. In 2018 Ardi Roelofs went back to Donders' handwritten "
            "laboratory notebook, and found the data of Donders' students, which Donders never published. For the "
            "students, methods b and c took the same time."
        ) as vo:
            self.play(FadeIn(recap, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(recap.animate.scale(0.62).to_edge(UP, buff=0.35), FadeIn(defn, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(wundt, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeOut(defn), FadeOut(wundt), FadeOut(recap))
            self.play(*[FadeIn(VGroup(bars[k], tags[k])) for k in (("c", 0), ("b", 0))], FadeIn(tag), FadeIn(key))
            vo.wait_until("d")
            self.play(*[FadeIn(VGroup(bars[k], tags[k]), shift=UP * 0.15) for k in (("c", 1), ("b", 1))])
            vo.wait_until("e")
            self.play(FadeIn(same), Create(arrows))
            vo.wait_until("f")
            self.play(FadeOut(VGroup(same, arrows, key, tag, *bars.values(), *tags.values())))
            self.play(FadeIn(note_, shift=UP * 0.2))
            self.play(FadeIn(gap[0]), FadeIn(gap[1]))
        self.clear_scene()

    def distribution(self):
        d = load("insertion")
        t, ts = np.asarray(d["t"]), np.asarray(d["stage_t"])
        head = heading(r"What pure insertion says about the whole distribution")

        def small(x_range, y_max, xlabel, xticks):
            return axes(list(x_range), [0, y_max], x_length=3.3, y_length=1.9, xlabel=xlabel, xticks=xticks,
                        font_size=18)

        A1 = small([100, 420], 0.026, r"simple (ms)", [100, 200, 300, 400])
        A2 = small([0, 160], 0.026, r"inserted stage (ms)", [0, 50, 100, 150])
        A3 = small([100, 420], 0.026, r"go/no-go (ms)", [100, 200, 300, 400])
        star = MathTex(r"\ast", font_size=60)
        eq = MathTex(r"=", font_size=60)
        row = VGroup(A1, star, A2, eq, A3).arrange(RIGHT, buff=0.35).move_to([0, 1.1, 0])
        c1 = curve(A1.ax, t, d["pdf_short_inserted"], METHOD["a"], 4)
        c2 = curve(A2.ax, ts[1:], np.asarray(d["stage_pdf"])[1:], DISC, 4)
        c3 = curve(A3.ax, t, d["pdf_long_inserted"], METHOD["c"], 4)
        ghost = curve(A3.ax, t, d["pdf_short_inserted"], METHOD["a"], 2).set_stroke(opacity=0.45)
        eqs = VGroup(
            MathTex(r"\text{RT}_c", r"=", r"\text{RT}_a", r"+", r"D", font_size=40),
            MathTex(r"\mathbb{E}[\text{RT}_c]", r"=", r"\mathbb{E}[\text{RT}_a]", r"+", r"\mathbb{E}[D]", font_size=40),
            MathTex(r"\operatorname{Var}[\text{RT}_c]", r"=", r"\operatorname{Var}[\text{RT}_a]", r"+",
                    r"\operatorname{Var}[D]", font_size=40),
        )
        for e in eqs:
            e[0].set_color(METHOD["c"])
            e[2].set_color(METHOD["a"])
            e[4].set_color(DISC)
        whys = VGroup(why(r"a stage $D$ is inserted; \ nothing else changes", 26), why(r"averages always add", 26),
                      why(r"variances add when $D$ is independent of the rest", 26))
        eqs.arrange(DOWN, buff=0.32)
        for e in eqs:  # line the three up on their equals signs
            e.shift(RIGHT * (-3.4 - e[1].get_x()))
        eqs.shift(UP * (-2.1 - eqs.get_y()))
        for e, w_ in zip(eqs, whys):
            w_.move_to([0.9, e.get_y(), 0], aligned_edge=LEFT)
        tag = psyche_tag()
        with self.voiceover(
            "Can the assumption be tested? Not with three averages. But a reaction time isn't one number. It's a "
            "whole distribution, and pure insertion says something strong about distributions. "
            "<bookmark mark='a'/> Suppose the harder task really is the easier one plus an extra stage, "
            "independent of the rest. <bookmark mark='b'/> Then the harder task's distribution is the easier "
            "one's, smeared out by the extra stage. Mathematicians call that a convolution: slide one curve "
            "along the other, and add. <bookmark mark='c'/> And when independent durations are added, two "
            "things follow. Their averages add: that's Donders' subtraction. <bookmark mark='d'/> And their "
            "variances add too. The spread of the harder task must be the spread of the easier one, plus the "
            "spread of whatever was inserted."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A1))
            self.play(Create(c1), run_time=2.0)
            vo.wait_until("a")
            self.play(Write(eqs[0]), FadeIn(whys[0]))
            self.play(FadeIn(star), FadeIn(A2), Create(c2))
            vo.wait_until("b")
            self.play(FadeIn(eq), FadeIn(A3), FadeIn(ghost))
            self.play(ReplacementTransform(c1.copy(), c3), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(eqs[1], shift=UP * 0.1), FadeIn(whys[1]))
            vo.wait_until("d")
            self.play(FadeIn(eqs[2], shift=UP * 0.1), FadeIn(whys[2]))
            self.play(Circumscribe(eqs[2], color=P.ACCENT, buff=0.12))
        self.clear_scene()

    def variance_test(self):
        d = load("insertion")
        head = heading(r"A check that could fail")
        unit = 5.2 / 1400.0

        def world(key, title, x0, verdict, vcolor):
            w = d[key]
            t = label(title, font_size=30, color=WHITE)
            a = Rectangle(width=w["var_short"] * unit, height=0.7, stroke_width=0, fill_color=METHOD["a"],
                          fill_opacity=0.85)
            c = Rectangle(width=w["var_long"] * unit, height=0.7, stroke_width=0, fill_color=METHOD["c"],
                          fill_opacity=0.85)
            a.move_to([x0 + a.width / 2, 0.75, 0])
            c.move_to([x0 + c.width / 2, -0.45, 0])
            la = label(rf"simple: \ ${w['var_short']:.0f}$", font_size=28, color=METHOD["a"])
            lc = label(rf"go/no-go: \ ${w['var_long']:.0f}$", font_size=28, color=METHOD["c"])
            la.next_to(a, UP, buff=0.08).align_to(a, LEFT)
            lc.next_to(c, DOWN, buff=0.08).align_to(c, LEFT)
            t.move_to([x0, 2.1, 0], aligned_edge=LEFT)
            need = MathTex(rf"\operatorname{{Var}}[D] = {w['d_var']:+.0f}", font_size=44, color=vcolor)
            need.move_to([x0, -1.85, 0], aligned_edge=LEFT)
            v = wrapped_label(verdict, 6.0, 28, vcolor).next_to(need, DOWN, buff=0.2).align_to(need, LEFT)
            g = VGroup(t, a, c, la, lc, need, v)
            g.title, g.bars, g.need, g.verdict = t, VGroup(a, c, la, lc), need, v
            return g

        ok = world("inserted", r"A world where a stage is inserted", -6.5,
                   rf"a real stage: \ the one we built in has variance {d['stage_var']:.0f}", STATUS_COLOR["replicated"])
        bad = world("changed", r"A world where the other stages change", 0.5,
                    r"no stage has a negative variance: \ insertion refuted", STATUS_COLOR["failed"])
        rule = MathTex(r"\operatorname{Var}[\text{RT}_c]", r"=", r"\operatorname{Var}[\text{RT}_a]", r"+",
                       r"\operatorname{Var}[D]", font_size=60)
        rule[0].set_color(METHOD["c"])
        rule[2].set_color(METHOD["a"])
        rule[4].set_color(DISC)
        units = label(r"variance of the reaction time, in ms$^2$; \ 4,000 trials of each task", font_size=22,
                      color=GREY_B).to_corner(DL, buff=0.3)
        tag = psyche_tag()
        with self.voiceover(
            "So here is a check that could fail. The harder task must be more variable than the easier one, by "
            "the variance of the stage that was inserted. <bookmark mark='a'/> In a model world where a stage is "
            "purely inserted, Psyche passes. The variance goes up, by the variance of the stage we built in. "
            "<bookmark mark='b'/> Now a second world. Here, knowing the response in advance changes how the "
            "response is made: it can be prepared, and sometimes it jumps the gun. The average difference between "
            "the two tasks is exactly what it was. <bookmark mark='c'/> But the simple task comes out more "
            "variable than the harder one. An inserted stage would need a negative variance, and no stage has "
            "that. <bookmark mark='d'/> Pure insertion is refuted, and from the shape of the data alone. That is "
            "the method of this whole series in miniature. A verbal idea, a stage is inserted, becomes a model. "
            "The model makes a prediction that could fail. And then you look."
        ) as vo:
            self.play(FadeIn(head), FadeIn(units), FadeIn(tag), FadeIn(rule, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(rule))
            self.play(FadeIn(ok.title), FadeIn(ok.bars, lag_ratio=0.2))
            self.play(FadeIn(ok.need), FadeIn(ok.verdict))
            vo.wait_until("b")
            self.play(FadeIn(bad.title), FadeIn(bad.bars, lag_ratio=0.2))
            vo.wait_until("c")
            self.play(FadeIn(bad.need), FadeIn(bad.verdict))
            vo.wait_until("d")
            self.play(Indicate(bad.need, color=STATUS_COLOR["failed"], scale_factor=1.12))
        self.clear_scene()

    def additive(self):
        d = load("additive")
        head = heading(r"Additive factors: \ Sternberg, 1969")

        def plot(key, title, cx, verdict, vcolor):
            w = d[key]
            exact, sim, se = (np.asarray(w[k]) for k in ("exact", "sim", "sim_se"))
            A = axes([-0.4, 1.4], [270, 385], x_length=4.6, y_length=3.3, xticks=None, yticks=[280, 320, 360],
                     ylabel=r"mean RT (ms)", center=[cx, 0.05, 0])
            ax = A.ax
            xl = VGroup(label(r"few", font_size=22, color=GREY_A).next_to(ax.c2p(0, 270), DOWN, buff=0.15),
                        label(r"many", font_size=22, color=GREY_A).next_to(ax.c2p(1, 270), DOWN, buff=0.15),
                        label(r"alternatives", font_size=22, color=GREY_A).next_to(ax.c2p(0.5, 270), DOWN, buff=0.5))
            lines, pts = VGroup(), VGroup()
            for i, color in enumerate((WHITE, P.ACCENT)):
                lines.add(Line(ax.c2p(0, exact[i, 0]), ax.c2p(1, exact[i, 1]), color=color, stroke_width=4))
                for j in range(2):
                    p = ax.c2p(j, sim[i, j])
                    bar = Line(ax.c2p(j, sim[i, j] - 2 * se[i, j]), ax.c2p(j, sim[i, j] + 2 * se[i, j]), color=color,
                               stroke_width=2)
                    pts.add(VGroup(bar, Dot(p, radius=0.07, color=color)))
            t = label(title, font_size=30, color=WHITE).next_to(A, UP, buff=0.25)
            names = w["factors"]
            leg = legend([(WHITE, rf"{'clear stimulus' if key == 'different' else 'natural mapping'}"),
                          (P.ACCENT, rf"{'degraded stimulus' if key == 'different' else 'awkward mapping'}")],
                         font_size=20).next_to(ax.c2p(-0.35, 383), DR, buff=0.05)
            v = label(verdict, font_size=30, color=vcolor).next_to(xl, DOWN, buff=0.25)
            g = VGroup(A, xl, lines, pts, t, leg, v)
            g.ax, g.lines, g.pts, g.title, g.leg, g.verdict, g.names = A, lines, pts, t, leg, v, names
            g.frame = VGroup(A, xl, t, leg)
            return g

        left = plot("different", r"two factors, \ two different stages", -3.6,
                    rf"parallel: \ interaction ${d['different']['interaction']:.0f}$ ms", STATUS_COLOR["replicated"])
        right = plot("same", r"two factors, \ the same stage", 3.6,
                     rf"fanning out: \ interaction ${d['same']['interaction']:.0f}$ ms", P.ACCENT)
        tag = psyche_tag(r"lines: Psyche's exact means; \ dots: a simulated experiment, $\pm 2$ SE")
        with self.voiceover(
            "A hundred years after Donders, Saul Sternberg found a way to study stages without inserting "
            "anything. Keep the task the same, and change two things about it. <bookmark mark='a'/> Say, make the "
            "stimulus harder to see, and increase the number of alternatives. If those two changes slow down "
            "different stages, their effects on the reaction time simply add. On a plot like this, that means "
            "parallel lines. <bookmark mark='b'/> Now change two things that both act on the same stage: more "
            "alternatives, and an awkward mapping from stimulus to response. Both make choosing harder, the "
            "effects compound, and the lines fan out. <bookmark mark='c'/> So a pattern in average reaction "
            "times, parallel or not, tells you something about the architecture inside. That's the additive "
            "factor method. It needs no subtraction of one task from another, and we'll use it ourselves in "
            "Part 19."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(left.frame))
            self.play(Create(left.lines), FadeIn(left.pts, lag_ratio=0.1))
            self.play(FadeIn(left.verdict))
            vo.wait_until("b")
            self.play(FadeIn(right.frame))
            self.play(Create(right.lines), FadeIn(right.pts, lag_ratio=0.1))
            self.play(FadeIn(right.verdict))
            vo.wait_until("c")
            self.play(Indicate(left.lines, color=WHITE, scale_factor=1.04), Indicate(right.lines, color=P.ACCENT,
                                                                                       scale_factor=1.04))
        self.clear_scene()
