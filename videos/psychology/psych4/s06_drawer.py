from __future__ import annotations

import numpy as np

from videos.psychology.psych4.common import *  # noqa: F403


class Drawer(VoiceoverScene):
    def construct(self):
        self.card()
        self.funnel()
        self.curse()
        self.pcurves()

    def card(self):
        card = chapter_card(5, r"The file drawer", r"What does a literature look like when only the successes are "
                            r"printed?", lit={1979: r"Rosenthal: the file-drawer problem"}, part=PART,
                            scale=("group", "culture"), marr=("what",))
        with self.voiceover(
            "Chapter five. The file drawer."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def _funnel(self, d, name, cx, title):
        est, se, pub = np.asarray(d[f"{name}_est"]), np.asarray(d[f"{name}_se"]), np.asarray(d[f"{name}_pub"]) > 0.5
        A = axes([-1.0, 1.4], [0, 0.5], x_length=6.1, y_length=4.0, xticks=[-0.8, -0.4, 0, 0.4, 0.8, 1.2],
                 xlabel=r"effect the laboratory found ($d$)", center=[cx, -0.55, 0], font_size=19)
        ax = A.ax
        y = lambda s_: 0.5 - s_  # precise studies at the top  # noqa: E731
        hidden = scatter(ax, est[~pub], y(se[~pub]), DRAWER, radius=0.028, opacity=0.8)
        shown = scatter(ax, est[pub], y(se[pub]), SIG, radius=0.04, opacity=0.95)
        truth = DashedLine(ax.c2p(d[name]["d"], 0), ax.c2p(d[name]["d"], 0.5), color=TRUTH, stroke_width=3)
        tl = label(rf"truth: \ {d[name]['d']:.1f}", font_size=20, color=TRUTH).next_to(truth, UP, buff=0.04)
        mean = DashedLine(ax.c2p(d[name]["mean_published"], 0), ax.c2p(d[name]["mean_published"], 0.42), color=SIG,
                          stroke_width=3)
        ml = label(rf"published: \ {r2(d[name]['mean_published'])}", font_size=20, color=SIG).next_to(mean, UP,
                                                                                                    buff=0.04)
        ttl = label(title, font_size=28, color=WHITE).next_to(A, UP, buff=0.42)
        side = label(r"larger studies $\rightarrow$", font_size=18, color=GREY_B).rotate(PI / 2)
        side.next_to(ax.c2p(-1.0, 0.25), LEFT, buff=0.1)
        count = label(rf"{d[name]['published']} published", font_size=26, color=SIG)
        count.next_to(ax.c2p(-1.0, 0.46), RIGHT, buff=0.15)
        g = VGroup(A, hidden, shown, truth, tl, mean, ml, ttl, side, count)
        g.A, g.hidden, g.shown, g.truth, g.mean, g.ttl = VGroup(A, side), hidden, shown, VGroup(truth, tl), VGroup(mean, ml), ttl
        g.count = count
        return g

    def funnel(self):
        d = load("drawer")
        head = heading(rf"{fmt_int(d['k'])} laboratories study one question")
        left = self._funnel(d, "null", -3.55, r"when there is nothing to find")
        right = self._funnel(d, "small", 3.65, r"when the effect is real, and small")
        counts = VGroup(left.count, right.count)
        # the opening picture: twenty studies, and where nineteen of them go
        studies = VGroup(*[Square(0.5, stroke_width=0, fill_color=(SIG if i == 13 else DRAWER), fill_opacity=1)
                           for i in range(20)]).arrange_in_grid(2, 10, buff=0.16).move_to([0, 1.2, 0])
        s_cap = label(r"twenty studies of one question", font_size=26, color=GREY_A).next_to(studies, UP, buff=0.25)
        box = Rectangle(width=4.6, height=1.3, color=GREY_B, stroke_width=3, fill_color="#111722", fill_opacity=1)
        box.move_to([-2.6, -1.9, 0])
        handle = Line(box.get_center() + LEFT * 0.5 + UP * 0.25, box.get_center() + RIGHT * 0.5 + UP * 0.25,
                      color=GREY_B, stroke_width=6)
        box_l = label(r"the file drawer", font_size=26, color=GREY_A).move_to(box.get_center() + DOWN * 0.25)
        journal = VGroup(RoundedRectangle(width=3.0, height=1.3, corner_radius=0.1, color=SIG, stroke_width=3),
                         label(r"the journal", font_size=26, color=SIG)).move_to([2.9, -1.9, 0])
        journal[1].move_to(journal[0].get_center() + DOWN * 0.3)
        winner = studies[13]
        losers = VGroup(*[s_ for i, s_ in enumerate(studies) if i != 13])
        tag = note(rf"simulated: the false-positive lab; \ {d['n_lo']} to {d['n_hi']} people a group").to_corner(
            DR, buff=0.2)
        with self.voiceover(
            "Now add the journals. For most of the last century a study that found nothing was very hard to "
            "publish. <bookmark mark='x'/> It went into a file drawer, <bookmark mark='y'/> and the literature "
            f"was whatever was left. So let's build a literature. <bookmark mark='a'/> A thousand laboratories each run one study of a treatment that "
            "does nothing at all. Each dot is a laboratory: its estimate across, and larger studies higher up. "
            "They scatter round zero in a funnel, wide at the bottom where the studies are small. "
            f"<bookmark mark='b'/> Now publish only the ones that came out significant, in the hoped-for "
            f"direction. {d['null']['published']} of them make it. <bookmark mark='c'/> And what do those "
            f"papers report? An average effect of {d['null']['mean_published']:.2f}. A medium effect, found "
            f"again and again by {d['null']['published']} independent laboratories, and there is nothing there. "
            "<bookmark mark='d'/> Now a treatment that does work, a little: a true effect of point two. "
            f"<bookmark mark='e'/> This time {d['small']['published']} get published, and they report "
            f"{d['small']['mean_published']:.2f}. More than twice the truth. Look at the shape of what's printed "
            "in both pictures: only the right-hand edge of the funnel. If you ever see a plot of a literature "
            "where the small studies all report big effects, and a corner is missing, you're looking at a file "
            "drawer."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(studies, lag_ratio=0.05), FadeIn(s_cap), run_time=2.0)
            self.play(FadeIn(box), FadeIn(handle), FadeIn(box_l), FadeIn(journal))
            vo.wait_until("x")
            self.play(LaggedStart(*[s_.animate.move_to(box.get_center() + UP * 0.25).set_opacity(0) for s_ in losers],
                                  lag_ratio=0.08), run_time=3.0)
            vo.wait_until("y")
            self.play(winner.animate.move_to(journal[0].get_center() + UP * 0.2), run_time=1.2)
            vo.wait_until("a")
            self.play(FadeOut(VGroup(winner, s_cap, box, handle, box_l, journal)))
            self.play(FadeIn(left.A), FadeIn(left.ttl), FadeIn(left.truth), FadeIn(left.hidden, lag_ratio=0.002),
                      FadeIn(left.shown, lag_ratio=0.01), run_time=3.0)
            vo.wait_until("b")
            self.play(left.hidden.animate.set_opacity(0.18), FadeIn(counts[0]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(left.mean))
            vo.wait_until("d")
            self.play(FadeIn(right.A), FadeIn(right.ttl), FadeIn(right.truth), FadeIn(right.hidden, lag_ratio=0.002),
                      FadeIn(right.shown, lag_ratio=0.01), run_time=3.0)
            vo.wait_until("e")
            self.play(right.hidden.animate.set_opacity(0.18), FadeIn(counts[1]), FadeIn(right.mean), run_time=1.5)
        self.clear_scene()

    def curse(self):
        d = load("drawer")
        head = heading(r"The winner's curse: \ small studies, big published effects")
        ns, ys = np.asarray(d["curse_n"]), np.asarray(d["curse"])
        xs = np.log10(ns)
        A = axes([1.0, 2.7], [0, 1.2], x_length=7.4, y_length=3.9, xticks=list(np.log10([10, 20, 50, 100, 200, 400])),
                 yticks=[0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2], xfmt=lambda v: f"{10 ** v:.0f}",
                 xlabel=r"people in each group", ylabel=r"effect reported in print ($d$)", center=[-2.6, -0.45, 0])
        ax = A.ax
        truth = DashedLine(ax.c2p(1.0, d["curse_d"]), ax.c2p(2.7, d["curse_d"]), color=TRUTH, stroke_width=3)
        tl = label(rf"the truth: \ {d['curse_d']}", font_size=24, color=TRUTH).next_to(ax.c2p(1.0, d["curse_d"]), UR,
                                                                                    buff=0.08)
        line = curve(ax, xs, ys, SIG, stroke_width=4)
        dots = VGroup(*[Dot(ax.c2p(x, y), radius=0.08, color=SIG) for x, y in zip(xs, ys)])
        i20, i200 = list(ns).index(20), list(ns).index(200)
        side = VGroup(
            wrapped_label(r"One true effect. \ Only significant studies are printed.", 4.6, 28, WHITE),
            label(rf"20 a group: \ print says {r2(ys[i20])}", font_size=30, color=SIG),
            label(rf"200 a group: \ print says {r2(ys[i200])}", font_size=30, color=SIG),
            wrapped_label(r"A published effect from a small study is an upper bound on the truth, and often a "
                          r"distant one.", 4.6, 27, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.5, 0.1, 0])
        tag = note(r"simulated: the false-positive lab").to_corner(DR, buff=0.2)
        with self.voiceover(
            "The size of the exaggeration follows a rule, and it's worth carrying around. <bookmark mark='a'/> "
            "Keep the true effect at point two, publish only what's significant, and change nothing but the size "
            f"of the studies. <bookmark mark='b'/> With twenty people a group, the printed effect averages "
            f"{ys[i20]:.2f}, nearly four times the truth. <bookmark mark='c'/> With two hundred a group it's "
            f"{ys[i200]:.2f}, and it settles toward the truth as studies grow. <bookmark mark='d'/> The reason "
            "is the one from chapter three: a small study can only be significant by overshooting. So read a "
            "published effect from a small study as an upper bound, not as an estimate. And notice that this "
            "happens when the effect is real. Bias doesn't only manufacture findings that are false. It "
            "inflates the true ones."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), Create(truth), FadeIn(tl), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(side[0]), Create(line), LaggedStart(*[FadeIn(p_) for p_ in dots], lag_ratio=0.2),
                      run_time=3.0)
            vo.wait_until("b")
            self.play(Flash(dots[i20], color=WHITE), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Flash(dots[i200], color=WHITE), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3], shift=UP * 0.1))
        self.clear_scene()

    def pcurves(self):
        d = load("drawer")["pcurves"]
        head = heading(r"Reading a literature from its p-values alone")
        specs = [("nothing", r"nothing there", NULLC, r"flat: \ every value as likely as the next"),
                 ("real", r"a real effect", TRUTH, r"piled up near zero"),
                 ("pushed", r"nothing there, and results nudged", BAD, r"piled up just under .05")]
        panels = VGroup()
        for i, (key, title, color, cap) in enumerate(specs):
            A = axes([0, 0.05], [0, 1.0], x_length=3.7, y_length=3.0, xticks=[0, 0.01, 0.02, 0.03, 0.04, 0.05],
                     xfmt=lambda v: f"{v:.2f}".replace("0.", ".", 1) if v else "0", xlabel=r"p-value of a published study",
                     center=[-4.6 + 4.6 * i, -0.1, 0], font_size=17)
            bars = hist(A.ax, np.linspace(0, 0.05, 6), np.asarray(d[key]), color, 0.9)
            t = label(title, font_size=27, color=color).next_to(A, UP, buff=0.25)
            c = label(cap, font_size=24, color=GREY_A).next_to(A, DOWN, buff=0.75)
            panels.add(VGroup(A, bars, t, c))
        end = label(r"The shape of the significant p-values tells you whether there was anything to find.",
                    font_size=28, color=P.ACCENT).to_edge(DOWN, buff=0.6)
        tag = note(r"simulated: 60,000 laboratories each; \ shares of the published p-values").to_corner(DR, buff=0.2)
        # the opening picture: of all p-values, only a sliver is printed
        ruler = Line([-5.5, 0.4, 0], [5.5, 0.4, 0], color=GREY_B, stroke_width=4)
        px = lambda p: -5.5 + 11.0 * p  # noqa: E731
        sliver = Line([px(0), 0.4, 0], [px(0.05), 0.4, 0], color=SIG, stroke_width=14)
        ticks = VGroup(*[VGroup(Line([px(p), 0.28, 0], [px(p), 0.52, 0], color=GREY_B, stroke_width=3),
                                label(t, font_size=24, color=GREY_A).move_to([px(p), -0.05, 0]))
                         for p, t in ((0.0, r"0"), (0.05, r".05"), (0.5, r".5"), (1.0, r"1"))])
        r_cap = label(r"every p-value a study could produce", font_size=26, color=GREY_A).next_to(ruler, UP, buff=0.5)
        s_cap = label(r"only these are printed", font_size=26, color=SIG).next_to(sliver, DOWN, buff=0.75)
        s_cap.align_to(sliver, LEFT)
        opening = VGroup(ruler, sliver, ticks, r_cap, s_cap)
        with self.voiceover(
            "There's a way to tell these literatures apart without seeing a single unpublished study. "
            "<bookmark mark='z'/> Look only "
            "at the significant p-values, the ones between zero and point oh five, and ask how they're spread. "
            "<bookmark mark='a'/> If there's nothing to find, every p-value is as likely as any other. So the "
            "published ones are spread evenly: as many between point oh four and point oh five as between zero "
            "and point oh one. <bookmark mark='b'/> If the effect is real, most significant results are very "
            "significant. The values pile up near zero. <bookmark mark='c'/> And if there's nothing there but "
            "results have been nudged across the line, by the kind of choices you made in the last chapter, they "
            "pile up just under point oh five, because people stop nudging as soon as they're across. "
            "<bookmark mark='d'/> This is called a p-curve. It was devised by the same three psychologists, and "
            "it lets an outsider audit a body of research from its printed pages. We use it properly in Part 50."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(ruler), FadeIn(ticks), FadeIn(r_cap))
            vo.wait_until("z")
            self.play(Create(sliver), FadeIn(s_cap))
            for m, pnl in zip("abc", panels):
                vo.wait_until(m)
                if m == "a":
                    self.play(FadeOut(opening), run_time=0.6)
                self.play(FadeIn(pnl[0]), FadeIn(pnl[2]), FadeIn(pnl[1], lag_ratio=0.2), run_time=1.5)
                self.play(FadeIn(pnl[3]))
            vo.wait_until("d")
            self.play(FadeIn(end, shift=UP * 0.15))
        self.clear_scene()
