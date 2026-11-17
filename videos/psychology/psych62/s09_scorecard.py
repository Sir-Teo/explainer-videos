from __future__ import annotations

from videos.psychology.psych62.common import *  # noqa: F403


class Scorecard(VoiceoverScene):
    def construct(self):
        card_section(self, 8, r"Psyche's scorecard", r"Can one model with one set of parameters do it all?",
                     scale=("person",), marr=("how",))
        self.table()
        self.failures()

    def table(self):
        d = load("scorecard")
        head = heading(r"The Battery, \ task by task")
        cols = {"yes": GOOD, "no": AUTH, "n/a": GREY_B}
        rows = VGroup()
        xs = [0.0, 0.55, 3.45, 7.95, 12.6]  # left edges of the five columns
        for num, name, sig, psy, ok in zip(d["num"], d["name"], d["signature"], d["psyche"], d["pass"]):
            if ok == "n/a":
                continue
            sig, psy = sig.replace("%", r"\%"), psy.replace("%", r"\%")
            cells = [label(num, font_size=20, color=cols[ok]), wrapped_label(name, 2.6, 18, WHITE),
                     wrapped_label(sig, 4.2, 16, GREY_A), wrapped_label(psy, 4.4, 16, cols[ok]),
                     label(ok, font_size=20, color=cols[ok])]
            for x, c in zip(xs, cells):
                c.move_to([x, 0, 0], aligned_edge=UL)
            rows.add(VGroup(*cells))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([0, 0.35, 0])
        if rows.height > 5.0:
            rows.scale_to_fit_height(5.0)
        rest = [n for n, ok in zip(d["name"], d["pass"]) if ok == "n/a"]
        foot = wrapped_label(r"modelled only inside their own parts: \ " + r", \ ".join(rest), 12.4, 18, GREY_B)
        foot.to_edge(DOWN, buff=0.35)
        npass = sum(1 for ok in d["pass"] if ok == "yes")
        nrun = sum(1 for ok in d["pass"] if ok != "n/a")
        with self.voiceover(
            f"Now Psyche sits the Battery, the twelve tasks and one questionnaire fixed in Part 1, through one shared "
            f"interface, with one set of default parameters. <bookmark mark='a'/> Reaction time, the threshold, "
            f"Stroop, change detection and risky choice match their published signatures. <bookmark mark='b'/> Two "
            f"don't. Visual search's target-absent slope is three and a half times the present slope, not about "
            f"twice; and in free recall with default parameters, recency runs back over most of the list, so the "
            f"first item is recalled no better than the middle. Part 20's fitted parameters fix recall, but then it's "
            f"a different Psyche. <bookmark mark='c'/> Six more tasks were only "
            f"ever modelled inside their own parts. So: {npass} of {nrun} with one set of parameters, and a unified "
            f"Psyche is still the open problem Part 58 named."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in rows], lag_ratio=0.4), run_time=5.0)
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.wait(1.0)
        self.clear_scene()

    def failures(self):
        d = load("failures")
        head = heading(r"The two failures, \ drawn")
        sizes = np.asarray(d["sizes"], dtype=float)
        A1 = axes([0, 34], [400, 1800], x_length=4.4, y_length=2.2, xticks=[4, 8, 16, 32], yticks=[500, 1000, 1500],
                  xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", xlabel=r"items in the display",
                  ylabel=r"ms", center=[-4.0, 1.45, 0], font_size=11)
        lines = VGroup()
        tags = VGroup()
        for key, col, name, ty in (("feature", GOOD, r"feature", 1400),
                                   ("present", MODEL, r"conjunction, present", 1550),
                                   ("absent", AUTH, r"conjunction, absent", 1700)):
            ys = np.asarray(d[key])
            lines.add(VGroup(curve(A1.ax, sizes, ys, col, stroke_width=3), scatter(A1.ax, sizes, ys, col, radius=0.05)))
            tags.add(label(name, font_size=13, color=col).move_to(A1.ax.c2p(2, ty), aligned_edge=LEFT))
        spc = np.asarray(d["spc"])
        pos = np.arange(1, len(spc) + 1)
        A2 = axes([0, 17], [0, 1.0], x_length=4.4, y_length=2.2, xticks=[1, 4, 8, 12, 16], yticks=[0, 0.5, 1.0],
                  xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}", xlabel=r"position in the list",
                  ylabel=r"recalled", center=[-4.0, -1.65, 0], font_size=11)
        sp = VGroup(curve(A2.ax, pos, spc, PERSON, stroke_width=3), scatter(A2.ax, pos, spc, PERSON, radius=0.05))
        ratio = (d["absent"][-1] - d["absent"][0]) / (d["present"][-1] - d["present"][0])
        rows = rows_of([
            (rf"feature search is flat, \ about {np.mean(d['feature']):.0f} ms at every set size, \ as it should "
             rf"be", GOOD),
            (rf"conjunction search: \ the absent slope is {ratio:.1f} times the present one; \ people's are about "
             rf"twice", AUTH),
            (rf"free recall: \ recency runs back over most of the list; \ the first item ({spc[0]:.2f}) is recalled "
             rf"no better than the eighth ({spc[7]:.2f}); \ people's curves have a short recency, \ a flat middle "
             rf"and a clear primacy", PERSON),
            (r"each failure names a fix, \ a quitting rule for search and rehearsal for the first items, \ and each "
             r"fix must then be tested on every other task: \ the price of one model", YOU),
        ], 6.2, 18, 0.34).move_to([3.0, -0.1, 0])
        tag = psyche_tag(r"\texttt{battery.run}, \ default parameters")
        with self.voiceover(
            "Here are the two failures, drawn. <bookmark mark='a'/> Visual search first. Feature search is flat, "
            "about half a second at every set size, as it should be. <bookmark mark='b'/> Conjunction search rises "
            "by about ten milliseconds an item when the target is there, and by about thirty-five when it's absent. "
            "People's absent slopes are about twice their present ones, and Psyche's are three and a half times as "
            "steep. <bookmark mark='c'/> Free recall. The last items are recalled best, but the advantage runs back "
            "over most of the list, and the first item is recalled no better than the eighth. People's curves have a "
            "short recency, a flat middle and a clear primacy. <bookmark mark='d'/> Each failure names a fix: a "
            "different quitting rule for search, and rehearsal for the first items. And each fix then has to be "
            "tested on every other task, because a change made for one task can break another. That's the price of "
            "one model."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A1), FadeIn(A2))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(lines[0]), FadeIn(tags[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(lines[1]), FadeIn(lines[2]), FadeIn(tags[1]), FadeIn(tags[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(sp))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
