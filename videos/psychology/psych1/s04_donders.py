from __future__ import annotations

import numpy as np

from videos.psychology.psych1.common import *  # noqa: F403

SYLLABLES = ("ka", "ke", "ki", "ko", "ku")


def chips(words, lit=("ki",), font_size=28) -> VGroup:
    """Syllables as small chips; those in ``lit`` are bright."""
    g = VGroup()
    for w in words:
        on = w in lit
        t = label(rf"\textit{{{w}}}", font_size=font_size, color=WHITE if on else GREY_B)
        box = RoundedRectangle(width=0.78, height=0.5, corner_radius=0.1, stroke_color=WHITE if on else GREY_D,
                               stroke_width=1.5, fill_color="#1B2230", fill_opacity=1)
        t.move_to(box)
        g.add(VGroup(box, t))
    return g.arrange(RIGHT, buff=0.1)


class Donders(VoiceoverScene):
    def construct(self):
        self.card()
        self.setup_experiment()
        self.subtract()
        self.psyche()

    def card(self):
        card = chapter_card(3, r"Subtracting one task from another", r"How long does it take to make a choice?",
                            lit=(1868,), part=PART, scale=("mind",), marr=("how",))
        with self.voiceover(
            "Chapter three. Subtracting one task from another."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    # ------------------------------------------------------------------
    def drum(self) -> VGroup:
        """The record on Donders' drum: a tuning fork's wave as the clock, and the two voices."""
        w, h = 7.4, 2.9
        box = panel(w, h)
        x = np.linspace(-w / 2 + 0.3, w / 2 - 0.3, 500)
        fork = VMobject(color=P.ACCENT, stroke_width=2.5).set_points_smoothly(
            [[xi, 0.85 + 0.16 * np.sin(13 * xi), 0] for xi in x[::4]])

        def voice(start, y, color, seed):
            rng = np.random.default_rng(seed)
            pts = []
            for xi in x[::2]:
                amp = 0.0 if xi < start else 0.3 * np.exp(-0.9 * (xi - start)) * (0.5 + rng.random())
                pts.append([xi, y + amp * np.sin(40 * xi), 0])
            return VMobject(color=color, stroke_width=2.5).set_points_as_corners(pts)

        x1, x2 = -1.9, 0.9
        said = voice(x1, 0.0, WHITE, 1)
        answer = voice(x2, -0.85, P.RESP, 2)
        marks = VGroup(*[DashedLine([xx, -1.25, 0], [xx, 1.2, 0], color=GREY_B, stroke_width=1.5) for xx in (x1, x2)])
        labs = VGroup(label(r"tuning fork: \ the clock", font_size=22, color=P.ACCENT),
                      label(r"experimenter: \ ``ki''", font_size=22, color=WHITE),
                      label(r"subject: \ ``ki''", font_size=22, color=P.RESP))
        for t, y in zip(labs, (0.85, 0.0, -0.85)):
            t.move_to([-w / 2 - 0.2 - t.width / 2, y, 0])
        span = Line([x1, 1.3, 0], [x2, 1.3, 0])
        br = brace_note(span, r"count the waves: \ the reaction time", UP, P.ACCENT, font_size=24)
        g = VGroup(box, fork, said, answer, marks, labs, br)
        g.fork, g.said, g.answer, g.marks, g.labs, g.brace = fork, said, answer, marks, labs, br
        return g

    def method_row(self, letter, name, hears, rule, lit):
        tag = label(letter, font_size=60, color=METHOD[letter])
        nm = label(name, font_size=36, color=METHOD[letter])
        left = VGroup(tag, nm).arrange(RIGHT, buff=0.3, aligned_edge=DOWN)
        heard = VGroup(label(r"may hear", font_size=28, color=GREY_B), chips(hears, lit=lit, font_size=34).scale(1.15))
        heard.arrange(RIGHT, buff=0.3)
        say = VGroup(label(r"says", font_size=28, color=GREY_B), label(rule, font_size=34, color=P.RESP))
        say.arrange(RIGHT, buff=0.3)
        row = VGroup(left, heard, say)
        row.left, row.heard, row.say = left, heard, say
        return row

    def setup_experiment(self):
        hc = history_card(1868, r"Franciscus Donders, Utrecht", r"physiologist and eye doctor: \ \emph{On the speed "
                          r"of mental processes}", color=P.ARCHIVE, width=7.4, font_size=30)
        idea = label(r"Make the brain do a little more, \ and see how much longer it takes.", font_size=38)
        top = VGroup(hc, idea).arrange(DOWN, buff=0.7).move_to(ORIGIN)
        drum = self.drum().scale(1.15).move_to([0, -1.25, 0])
        sch = schematic_tag(DR)
        rows = VGroup(
            self.method_row("a", r"simple", ("ki",), r"\textit{ki}", ("ki",)),
            self.method_row("b", r"choice", SYLLABLES, r"whichever syllable was said", SYLLABLES),
            self.method_row("c", r"go/no-go", SYLLABLES, r"\textit{ki} only; \ silent for the rest", ("ki",)),
        )
        head = heading(r"Donders' three methods")
        needs = VGroup(*[label(t, font_size=32, color=c) for t, c in (
            (r"react", METHOD["a"]), (r"react + tell apart + choose", METHOD["b"]),
            (r"react + tell apart", METHOD["c"]))])
        for r, n, y in zip(rows, needs, (1.75, -0.35, -2.45)):
            r.left.move_to([-6.6, y, 0], aligned_edge=LEFT)
            r.heard.move_to([-3.9, y + 0.36, 0], aligned_edge=LEFT)
            r.say.move_to([-3.9, y - 0.36, 0], aligned_edge=LEFT)
            r.say[1].align_to(r.heard[1], LEFT)
            n.move_to([6.7, y, 0], aligned_edge=RIGHT)
        src = historical_tag(archive.DONDERS_1868.cite)
        with self.voiceover(
            "The man who took up that tenth of a second was a Dutch physiologist and eye doctor, Franciscus "
            "Donders, in Utrecht. His idea was to make the brain do a little more, and see how much longer it "
            "took. <bookmark mark='a'/> His experiment used speech. The experimenter says a syllable: ki. The "
            "subject repeats it as fast as he can. Both voices scratch their vibrations onto a turning drum, "
            "beside the trace of a tuning fork, and the tuning fork is the clock. Count its waves between one "
            "voice and the other. <bookmark mark='b'/> He ran the experiment three ways. Method a: you know the "
            "syllable in advance. It will be ki, so just repeat it. That's a simple reaction. "
            "<bookmark mark='c'/> Method b: it could be any of five syllables, and you must repeat whichever "
            "one you hear. Now you have to tell which syllable it was, and choose which one to say. "
            "<bookmark mark='d'/> And method c, the clever one. Any of the five may come, but you answer only "
            "to ki, and stay silent for the others. You still have to tell the syllables apart. But you never "
            "have to choose a response, because there's only one."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(src))
            self.play(FadeIn(idea, shift=UP * 0.15))
            vo.wait_until("a")
            self.play(FadeOut(hc), idea.animate.scale(0.8).to_edge(UP, buff=0.45))
            self.play(FadeIn(drum[0]), FadeIn(drum.labs), FadeIn(sch))
            self.play(Create(drum.fork), run_time=1.5)
            self.play(Create(drum.said), run_time=1.5)
            self.play(Create(drum.answer), run_time=1.5)
            self.play(FadeIn(drum.marks), FadeIn(drum.brace))
            vo.wait_until("b")
            self.play(FadeOut(VGroup(idea, drum, sch)), FadeIn(head))
            for mark, r, n in zip("bcd", rows, needs):
                vo.wait_until(mark)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
                self.play(FadeIn(n))
        self.clear_scene()

    def subtract(self):
        d = load("donders")
        unit = 0.03
        a_stage = (r"everything a simple reaction needs", d["a"], METHOD["a"])
        bars = {
            "a": stage_bar([a_stage], unit=unit, height=0.62, font_size=24),
            "c": stage_bar([a_stage, (r"tell apart", d["discriminate"], DISC)], unit=unit, height=0.62, font_size=24),
            "b": stage_bar([a_stage, (r"tell apart", d["discriminate"], DISC), (r"choose", d["choose"], CHOOSE)],
                           unit=unit, height=0.62, font_size=24),
        }
        x_left = -4.3
        for k, y in zip("acb", (1.6, 0.0, -1.6)):
            b = bars[k]
            b.shift([x_left - b.cells[0].get_left()[0], y - b.cells[0].get_y(), 0])
        for k in "cb":
            bars[k].names[0].set_opacity(0)
        bars["b"].names[1].set_opacity(0)
        tags, totals = {}, {}
        names = {"a": r"simple", "c": r"go/no-go", "b": r"choice"}
        for k in "acb":
            t = VGroup(label(k, font_size=44, color=METHOD[k]), label(names[k], font_size=24, color=METHOD[k]))
            t.arrange(DOWN, buff=0.05).next_to(bars[k].cells[0], LEFT, buff=0.35)
            tags[k] = t
            totals[k] = MathTex(rf"{d[k]:.0f}\ \text{{ms}}", font_size=36, color=P.HUMAN)
            totals[k].next_to(bars[k].cells[-1], RIGHT, buff=0.3)
        eq1 = MathTex(r"c - a", r"=", rf"{d['c']:.0f} - {d['a']:.0f}", r"=", rf"{d['discriminate']:.0f}\ \text{{ms}}",
                      font_size=40)
        eq2 = MathTex(r"b - c", r"=", rf"{d['b']:.0f} - {d['c']:.0f}", r"=", rf"{d['choose']:.0f}\ \text{{ms}}",
                      font_size=40)
        eq1[-1].set_color(DISC)
        eq2[-1].set_color(CHOOSE)
        n1 = label(r"to tell five syllables apart", font_size=26, color=DISC)
        n2 = label(r"to choose one of five responses", font_size=26, color=CHOOSE)
        e1 = VGroup(eq1, n1).arrange(RIGHT, buff=0.4)
        e2 = VGroup(eq2, n2).arrange(RIGHT, buff=0.4)
        eqs = VGroup(e1, e2).arrange(DOWN, buff=0.3, aligned_edge=LEFT).to_edge(DOWN, buff=0.75)
        head = heading(r"Donders' own times")
        src = historical_tag(archive.DONDERS_1868.cite)
        with self.voiceover(
            "Here are Donders' own times, in thousandths of a second. <bookmark mark='a'/> The simple reaction: "
            f"{d['a']:.0f}. <bookmark mark='b'/> Go/no-go: {d['c']:.0f}. <bookmark mark='c'/> Choice: "
            f"{d['b']:.0f}. <bookmark mark='d'/> Now subtract. Method c is method a, plus telling the syllables "
            f"apart. So c minus a, {d['discriminate']:.0f} milliseconds, is the time it takes to tell them apart. "
            "<bookmark mark='e'/> And method b is method c, plus choosing a response. So b minus c, "
            f"{d['choose']:.0f} milliseconds, is the time of a choice. <bookmark mark='f'/> Look at what just "
            "happened. A purely mental act, choosing among five things, which nobody can see, has been given a "
            f"duration: {d['choose']:.0f} thousandths of a second. On a drum, with a tuning fork. "
            "<bookmark mark='g'/> Kant said that mathematics can't be applied to the inner sense. This is a "
            "subtraction."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            for mark, k in zip("abc", "acb"):
                vo.wait_until(mark)
                self.play(FadeIn(tags[k]), GrowFromEdge(bars[k].cells[0], LEFT), FadeIn(bars[k].names[0]),
                          FadeIn(bars[k].ms[0]))
                extra = [x for i in range(1, len(bars[k].cells)) for x in
                         (bars[k].cells[i], bars[k].names[i], bars[k].ms[i])]
                self.play(*[FadeIn(x) for x in extra], FadeIn(totals[k]), run_time=0.8)
            vo.wait_until("d")
            self.play(Indicate(bars["c"].cells[1], color=WHITE), FadeIn(e1, shift=UP * 0.15))
            vo.wait_until("e")
            self.play(Indicate(bars["b"].cells[2], color=WHITE), FadeIn(e2, shift=UP * 0.15))
            vo.wait_until("f")
            self.play(Circumscribe(eq2[-1], color=CHOOSE, buff=0.12))
            vo.wait_until("g")
            self.play(Indicate(VGroup(eq1[0], eq2[0]), color=P.ACCENT, scale_factor=1.2))
        self.clear_scene()

    def psyche(self):
        d = load("donders")
        t = np.asarray(d["t"])
        sub = d["sim_subtraction"]
        # the chain of stages, as a program
        chain = VGroup()
        shown = {"discriminate": r"tell apart"}
        for name, _ in d["stages"]["b"]:
            c = STAGE_COLOR[name]
            txt = label(shown.get(name, name), font_size=30, color=c)
            box = RoundedRectangle(width=txt.width + 0.6, height=0.85, corner_radius=0.12, stroke_color=c,
                                   stroke_width=2, fill_color=c, fill_opacity=0.12)
            txt.move_to(box)
            chain.add(VGroup(box, txt))
        chain.arrange(RIGHT, buff=0.7)
        arrows = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.08, color=GREY_B, stroke_width=3,
                                max_tip_length_to_length_ratio=0.3) for a, b in zip(chain, chain[1:])])
        stim = label(r"stimulus", font_size=28, color=P.STIM).next_to(chain, LEFT, buff=0.7)
        resp = label(r"response", font_size=28, color=P.RESP).next_to(chain, RIGHT, buff=0.7)
        ends = VGroup(Arrow(stim.get_right(), chain[0].get_left(), buff=0.08, color=GREY_B, stroke_width=3),
                      Arrow(chain[-1].get_right(), resp.get_left(), buff=0.08, color=GREY_B, stroke_width=3))
        prog = VGroup(chain, arrows, stim, resp, ends).to_edge(UP, buff=0.55)
        rule = MathTex(r"\text{RT}", r"=", r"T_{\text{sense}}", r"+", r"T_{\text{tell apart}}", r"+",
                       r"T_{\text{choose}}", r"+", r"T_{\text{respond}}", font_size=40)
        for i, c in ((2, SENSE), (4, DISC), (6, CHOOSE), (8, RESPOND)):
            rule[i].set_color(c)
        rule.next_to(prog, DOWN, buff=0.35)
        A = rt_axes([120, 480], 0.026, x_length=8.4, y_length=3.3, center=[-2.2, -1.55, 0],
                    xticks=[150, 200, 250, 300, 350, 400, 450])
        ax = A.ax
        curves = {k: curve(ax, t, d[f"pdf_{k}"], P.PSYCHE, 4) for k in "acb"}
        ticks, labs = {}, {}
        for k in "acb":
            peak = float(np.max(d[f"pdf_{k}"]))
            ticks[k] = Line(ax.c2p(d[k], 0), ax.c2p(d[k], peak), color=P.HUMAN, stroke_width=2.5)
            labs[k] = label(k, font_size=34, color=METHOD[k]).next_to(ax.c2p(d[k], peak), UP, buff=0.08)
        out = VGroup(
            MathTex(rf"c - a = {sub['discriminate']:.1f} \pm {sub['discriminate_se']:.1f}", font_size=36, color=DISC),
            MathTex(rf"b - c = {sub['choose']:.1f} \pm {sub['choose_se']:.1f}", font_size=36, color=CHOOSE),
            label(r"20,000 simulated trials each", font_size=24, color=GREY_B),
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT).next_to(A, RIGHT, buff=0.5).shift(UP * 0.5)
        leg = legend([(P.PSYCHE, r"Psyche: \ the model"), (P.HUMAN, r"Donders' means")], font_size=24)
        leg.next_to(out, DOWN, buff=0.45).align_to(out, LEFT)
        pulse = glow_dot(stim.get_right(), color=P.ACCENT, radius=0.09)
        tag = psyche_tag()
        with self.voiceover(
            "This is the first model of the series, so let's build it properly. <bookmark mark='a'/> A response "
            "is produced by a chain of stages. <bookmark mark='b'/> Each stage takes a random time, a little "
            "different on every trial, and the reaction time is their sum. <bookmark mark='c'/> That's a "
            "program, and here it is running: twenty thousand simulated trials of each method. The white lines "
            "are Donders' three averages. <bookmark mark='d'/> Subtract the model's averages, and it gives back "
            "the stage durations we built in. <bookmark mark='e'/> In this series, a model that runs is always "
            "drawn in orange, and it has a name: Psyche. Human data are always white. This is Psyche's first "
            "faculty. It can react."
        ) as vo:
            self.play(FadeIn(stim), FadeIn(resp), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.15) for c in chain], lag_ratio=0.35), FadeIn(arrows),
                      FadeIn(ends), run_time=2.5)
            vo.wait_until("b")
            self.play(Write(rule))
            self.add(pulse)
            for c, rt_ in zip(chain, (0.9, 0.35, 0.5, 0.6)):
                self.play(pulse.animate.move_to(c), run_time=0.3)
                self.play(Indicate(c, color=WHITE, scale_factor=1.06), run_time=rt_)
            self.play(pulse.animate.move_to(resp.get_left()), run_time=0.3)
            self.play(FadeOut(pulse, run_time=0.3))
            vo.wait_until("c")
            self.play(FadeIn(A))
            for k in "acb":
                self.play(Create(curves[k]), FadeIn(labs[k]), run_time=1.1)
            self.play(*[Create(ticks[k]) for k in "acb"], FadeIn(leg))
            vo.wait_until("d")
            self.play(FadeIn(out, shift=LEFT * 0.2))
            vo.wait_until("e")
            self.play(*[Indicate(curves[k], color=P.PSYCHE, scale_factor=1.03) for k in "acb"])
        self.clear_scene()
