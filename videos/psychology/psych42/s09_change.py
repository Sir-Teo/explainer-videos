from __future__ import annotations

from videos.psychology.psych42.common import *  # noqa: F403


class Change(VoiceoverScene):
    def construct(self):
        self.card()
        self.rci()
        self.patients()
        self.categories()

    def card(self):
        card = chapter_card(8, r"Clinical significance", r"Did this person get better?",
                            lit={1991: r"Jacobson \& Truax"}, part=PART, scale=("person",), marr=("what", "how"))
        with self.voiceover("Chapter eight. Clinical significance."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def rci(self):
        d = load("rci")
        head = heading(r"Two questions about one person")
        eqs = VGroup(
            MathTex(r"\mathrm{SE} = s\sqrt{1 - r_{xx}}, \qquad S_{\text{diff}} = \sqrt{2}\,\mathrm{SE}", font_size=32,
                    color=MODEL),
            MathTex(r"\mathrm{RCI} = \frac{x_{\text{after}} - x_{\text{before}}}{S_{\text{diff}}}, \qquad "
                    r"|\mathrm{RCI}| > 1.96", font_size=32, color=MODEL),
            MathTex(r"c = \frac{s_{\text{clin}}\,\bar{x}_{\text{well}} + s_{\text{well}}\,\bar{x}_{\text{clin}}}"
                    r"{s_{\text{clin}} + s_{\text{well}}}", font_size=32, color=GOOD),
        ).arrange(DOWN, buff=0.35).move_to([-3.4, 0.2, 0])
        rows = rows_of([
            (r"Jacobson and Truax, \ 1991: \ a group's average effect says nothing about whether one person changed", WHITE),
            (r"first: \ is the change bigger than measurement error? \ Part 3's standard error of measurement, \ for a "
             r"difference of two scores", MODEL),
            (rf"for a scale with SD 7 and reliability 0.85, \ a change must exceed {d['threshold']:.1f} points", PERSON),
            (rf"second: \ did the person end nearer the well than the ill? \ the cut-off between the distributions, \ "
             rf"here {d['cutoff']:.1f}", GOOD),
        ], 6.0, 19, 0.38).move_to([3.4, -0.2, 0])
        tag = psyche_tag(r"\texttt{clinic.reliable\_change}, \ \texttt{jt\_cutoff}; \ Jacobson \& Truax (1991)")
        with self.voiceover(
            "A group's average says little about one person. <bookmark mark='a'/> In 1991 Neil Jacobson and Paula "
            "Truax proposed two questions for each client. <bookmark mark='b'/> First, is the change bigger than "
            "measurement error? It's Part 3's standard error of measurement, applied to a difference of two scores. "
            "Divide the change by it, and call it reliable if the ratio passes one point nine six. "
            "<bookmark mark='c'/> For a scale with a standard deviation of seven and a reliability of zero point eight "
            "five, a change must exceed about seven and a half points. <bookmark mark='d'/> Second, did the person "
            "end nearer the well than the ill? The cut-off sits between the two distributions, weighted by their "
            "spreads. Here, about sixteen and a half."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(eqs[0]), FadeIn(eqs[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]), FadeIn(eqs[2]))
        self.clear_scene()

    def patients(self):
        d = load("rci")
        head = heading(r"Four clients")
        A = axes([10, 36], [10, 36], x_length=4.4, y_length=4.4, xticks=[10, 20, 30], yticks=[10, 20, 30],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", xlabel=r"before", ylabel=r"after",
                 center=[-3.4, 0.1, 0], font_size=13)
        diag = DashedLine(A.ax.c2p(10, 10), A.ax.c2p(36, 36), color=GREY_B, stroke_width=1.5)
        cut = DashedLine(A.ax.c2p(10, d["cutoff"]), A.ax.c2p(36, d["cutoff"]), color=GOOD, stroke_width=1.5)
        c_l = label(r"cut-off", font_size=12, color=GOOD).next_to(A.ax.c2p(36, d["cutoff"]), UP, buff=0.05)
        names = [r"recovered", r"no reliable change", r"crossed the cut-off, \ but not reliably", r"improved, \ "
                 r"not recovered"]
        cols = [GOOD, GREY_A, SYMP, PERSON]
        dots = VGroup(*[Dot(A.ax.c2p(float(a), float(b)), radius=0.08, color=c)
                        for a, b, c in zip(d["pre"], d["post"], cols)])
        rows = VGroup()
        for i in range(4):
            rows.add(wrapped_label(rf"{d['pre'][i]:.0f} $\to$ {d['post'][i]:.0f}: \ RCI {d['rci'][i]:+.2f}; \ "
                                   rf"{names[i]}", 5.8, 19, cols[i]))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.36).move_to([3.4, 0.4, 0])
        foot = wrapped_label(r"outcome monitoring with these two rules shows clinician and client, \ session by "
                             r"session, \ who is on track", 6.0, 18, YOU).next_to(rows, DOWN, buff=0.45)
        with self.voiceover(
            "Here are four clients. <bookmark mark='a'/> The first went from thirty to fourteen: a reliable change, "
            "and across the cut-off. Recovered. <bookmark mark='b'/> The second, thirty to twenty-five: no reliable "
            "change. <bookmark mark='c'/> The third, twenty-two to fifteen: across the cut-off, but by less than "
            "measurement error. <bookmark mark='d'/> The fourth, thirty-four to twenty: a reliable change, but still "
            "on the ill side. Improved, not recovered. <bookmark mark='e'/> Outcome monitoring with these two rules "
            "shows clinician and client, session by session, who is on track."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(diag), FadeIn(cut), FadeIn(c_l))
            for m, i in zip("abcd", range(4)):
                vo.wait_until(m)
                self.play(FadeIn(dots[i], scale=1.5), FadeIn(rows[i], shift=RIGHT * 0.15))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def categories(self):
        d = load("categories")
        head = heading(r"Recovered, \ by these rules, \ without treatment")
        arms = (("none", r"no treatment"), ("waitlist", r"waiting list"), ("placebo", r"placebo therapy"),
                ("active", r"active therapy"))
        cats = (("recovered", GOOD), ("improved", SYMP), ("unchanged", GREY_B), ("deteriorated", AUTH))
        A = axes([0.3, 4.7], [0, 1], x_length=5.6, y_length=3.2, xticks=None, yticks=[0, 0.5, 1],
                 yfmt=lambda v: f"{100 * v:.0f}\\%", ylabel=r"share of clients", center=[-3.3, 0.5, 0], font_size=13)
        stacks = VGroup()
        for i, (a, _) in enumerate(arms):
            base = 0.0
            for k, c in cats:
                h = d[f"{a}_{k}"]
                lo, hi = A.ax.c2p(i + 1, base), A.ax.c2p(i + 1, base + h)
                w = abs(A.ax.c2p(i + 1.3, 0)[0] - A.ax.c2p(i + 0.7, 0)[0])
                stacks.add(Rectangle(width=w, height=max(1e-3, hi[1] - lo[1]), stroke_width=0, fill_color=c,
                                     fill_opacity=0.85).move_to([lo[0], (lo[1] + hi[1]) / 2, 0]))
                base += h
        names = VGroup(*[wrapped_label(t, 1.3, 12, GREY_A).next_to(A.ax.c2p(i + 1, 0), DOWN, buff=0.15)
                         for i, (_, t) in enumerate(arms)])
        key = VGroup(*[label(k, font_size=12, color=c) for k, c in cats]).arrange(RIGHT, buff=0.3).next_to(
            names, DOWN, buff=0.2)
        rows = rows_of([
            (r"Psyche applies both rules to everyone in chapter two's trial, \ 2{,}000 per arm", WHITE),
            (rf"with no treatment at all, \ {pct(d['none_recovered'])} count as recovered: \ regression to the "
             rf"mean fools individual rules too", AUTH),
            (rf"placebo therapy, \ {pct(d['placebo_recovered'])}; \ active therapy, \ {pct(d['active_recovered'])}",
             GOOD),
            (r"so a clinic's recovery rate means little alone; \ the comparison with a control is still what shows the "
             r"therapy's share", YOU),
        ], 6.0, 19, 0.38).move_to([3.4, -0.2, 0])
        tag = psyche_tag(r"\texttt{clinic.jt\_categories}, \ 2{,}000 per arm")
        with self.voiceover(
            "Now apply both rules to everyone in chapter two's trial. <bookmark mark='a'/> Psyche classifies two "
            "thousand people in each arm as recovered, improved, unchanged or deteriorated. <bookmark mark='b'/> With "
            "no treatment at all, about a third count as recovered. Regression to the mean fools individual rules "
            "too. <bookmark mark='c'/> With placebo therapy, under half; with the active therapy, over half. "
            "<bookmark mark='d'/> So a clinic's recovery rate means little on its own. The comparison with a control "
            "is still what shows the therapy's share."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), LaggedStart(*[FadeIn(x) for x in stacks], lag_ratio=0.05), run_time=2.0)
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
