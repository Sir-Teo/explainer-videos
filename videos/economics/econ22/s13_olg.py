from __future__ import annotations

from videos.economics.econ22.common import *  # noqa: F403


def ce(e):
    """Consumption-equivalent welfare change (percent) of each pension against none: with log utility, scaling both
    periods' consumption by 1 + x changes lifetime utility by (1 + beta) ln(1 + x)."""
    u = np.array(e["welfare"]["utility"])
    return 100 * (np.exp((u - u[0]) / (1 + e["beta"])) - 1)


class OLG(VoiceoverScene):
    def construct(self):
        card(self, 11, r"Overlapping generations", r"How do generations trade with each other, \ and when is a "
             r"pension a free lunch?", "Chapter eleven. Overlapping generations.",
             lit={1958: r"Samuelson", 1965: r"Diamond", 1989: r"Abel, Mankiw, Summers, Zeckhauser"},
             scale=("nation",), horizon=("generations",))
        self.samuelson()
        self.diamond()
        self.inefficient()
        self.evidence()

    def samuelson(self):
        s = load("samuelson")
        o = load("olg")
        gens = VGroup()
        for k in range(4):
            y = 2.7 - 0.72 * k
            young = RoundedRectangle(width=2.2, height=0.48, corner_radius=0.1, stroke_color=YOUNG, fill_color=YOUNG,
                                     fill_opacity=0.25).move_to([-4.6 + 2.4 * k, y, 0])
            old = RoundedRectangle(width=2.2, height=0.48, corner_radius=0.1, stroke_color=OLD, fill_color=OLD,
                                   fill_opacity=0.25).next_to(young, RIGHT, buff=0.2)
            gens.add(VGroup(young, label(r"young: \ works", font_size=15, color=YOUNG).move_to(young), old,
                            label(r"old: \ retired", font_size=15, color=OLD).move_to(old)))
        arrows = VGroup(*[Arrow(gens[k + 1][0].get_top(), gens[k][2].get_bottom(), buff=0.03, color=SAVE,
                                stroke_width=4, max_tip_length_to_length_ratio=0.5) for k in range(3)])
        side = VGroup(
            label(r"goods cannot be stored; \ the old have nothing", font_size=21, color=GREY_A),
            label(r"the young cannot lend to the old: \ they will be gone before repayment", font_size=21,
                  color=GREY_A),
            label(r"money: \ each old generation sells paper to the young for goods", font_size=21, color=SAVE),
            label(rf"its return is the growth of the population: \ $1 + n = {s['return']:.1f}$ a generation \ "
                  rf"(about {100 * o['annual_n']:.1f}\% a year)", font_size=21, color=SAVE),
            label(r"a pay-as-you-go pension is the same contract, \ written by the state", font_size=21,
                  color=PENSION),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.35)
        tag = published_tag(r"Samuelson, JPE 66(6) (1958): \ 467--482", corner=DR, font_size=12)
        with self.voiceover(
            "Everything so far has been one household and its own life. But lives overlap. In 1958 Paul Samuelson "
            "imagined the simplest economy with that feature. <bookmark mark='a'/> Each generation lives two "
            "periods: young and working, then old and retired. Goods cannot be stored, so the old have nothing. "
            "<bookmark mark='b'/> The young cannot lend to the old, because the old will be gone before they could "
            "repay. Without some arrangement, the old starve. <bookmark mark='c'/> The arrangement is money. Each "
            "old generation holds pieces of paper, and sells them to the young for goods. The young accept the "
            "paper because the next young generation will accept it from them. <bookmark mark='d'/> If each "
            "generation is larger than the last, the paper buys more when they are old: its return is the growth of "
            f"the population, {s['return']:.1f} a generation here, about {100 * o['annual_n']:.1f} percent a year. "
            "<bookmark mark='e'/> A pay-as-you-go pension, in which today's workers pay today's retirees, is the "
            "same contract, written by the state. Samuelson called it a social contrivance."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(g) for g in gens], lag_ratio=0.2), FadeIn(tag), FadeIn(side[0]),
                      run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.3), FadeIn(side[2]), run_time=2)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def diamond(self):
        o = load("olg")
        e = o["economies"][1]
        st = e["steady"]
        top = 2.5
        ax = plane([0, top], [0, top], center=LEFT * 2.6 + DOWN * 0.4, x_length=5.4, y_length=5.0,
                   xticks=[0, 1, 2], yticks=[0, 1, 2], xlabel=r"capital per worker today, \ $k_t$",
                   ylabel=r"$k_{t+1}$", xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", font_size=16)
        diag = seg(ax, 0, 0, top, top, color=GREY_B, width=2, dashed=True)
        mp = path(ax, e["map_k"], e["map_next"], color=SAVE, width=4, xr=(0, top), yr=(0, top))
        pts = e["path"]
        web = VGroup()
        for a, b in zip(pts[:-1], pts[1:]):
            web.add(Line(ax.ax.c2p(a, a), ax.ax.c2p(a, b), color=YOUNG, stroke_width=2))
            web.add(Line(ax.ax.c2p(a, b), ax.ax.c2p(b, b), color=YOUNG, stroke_width=2))
        star = dot(ax, st["k"], st["k"], color=WHITE, r=0.08)
        rows = VGroup(
            label(r"Peter Diamond, \ 1965: \ add capital", font_size=23, color=E.ACCENT),
            label(r"the young earn a wage, \ consume, \ and save", font_size=20, color=YOUNG),
            label(r"their savings are next period's capital", font_size=20, color=SAVE),
            MathTex(r"k_{t+1} = \frac{s\big(w(k_t), R_{t+1}\big)}{1+n}", font_size=34, color=SAVE),
            label(r"the old live on their capital's return", font_size=20, color=OLD),
            label(rf"a steady state: \ $k^* = {st['k']:.2f}$ \ ($\beta = {e['beta']}$ a generation)", font_size=20,
                  color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.45)
        tag = agora_tag(corner=DR, font_size=14)
        with self.voiceover(
            "In 1965 Peter Diamond put capital into Samuelson's economy. <bookmark mark='a'/> Now the young earn a "
            "wage, consume part of it, and save the rest. <bookmark mark='b'/> Their savings become next period's "
            "capital, spread over the next, larger, generation of workers. <bookmark mark='c'/> So capital per "
            "worker tomorrow is a function of capital per worker today, through the wage it pays the young. "
            "<bookmark mark='d'/> The old live on the return to their capital. <bookmark mark='e'/> Follow the map "
            "from a low start and it climbs to a steady state where the curve crosses the diagonal, here at "
            f"{st['k']:.2f}."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(diag), FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcd", rows[1:5]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
                if mk == "c":
                    self.play(Create(mp), run_time=1.5)
            vo.wait_until("e")
            self.play(Create(web), run_time=3)
            self.play(FadeIn(star), FadeIn(rows[5]))
        self.clear_scene()

    def inefficient(self):
        o = load("olg")
        pat, imp = o["economies"]
        rows = VGroup(
            label(r"the golden rule: \ the return on capital equals the growth rate, \ $R = 1 + n$", font_size=24,
                  color=E.ACCENT),
            VGroup(
                VGroup(label(rf"patient \ ($\beta = {pat['beta']}$)", font_size=22, color=YOUNG),
                       label(rf"$R = {pat['steady']['R']:.2f} < 1 + n = {1 + o['n']:.1f}$", font_size=22, color=WHITE),
                       label(rf"$k^* = {pat['steady']['k']:.2f}$, \ golden $= {pat['steady']['k_gold']:.2f}$",
                             font_size=20, color=GREY_A),
                       label(r"too much capital: \ dynamically inefficient", font_size=20, color=HOLD)).arrange(
                    DOWN, aligned_edge=LEFT, buff=0.15),
                VGroup(label(rf"impatient \ ($\beta = {imp['beta']}$)", font_size=22, color=OLD),
                       label(rf"$R = {imp['steady']['R']:.2f} > 1 + n = {1 + o['n']:.1f}$", font_size=22, color=WHITE),
                       label(rf"$k^* = {imp['steady']['k']:.2f}$, \ golden $= {imp['steady']['k_gold']:.2f}$",
                             font_size=20, color=GREY_A),
                       label(r"efficient", font_size=20, color=SPEND)).arrange(DOWN, aligned_edge=LEFT, buff=0.15),
            ).arrange(RIGHT, buff=1.2),
        ).arrange(DOWN, buff=0.45).to_edge(UP, buff=0.45)
        ce_p, ce_i = ce(pat), ce(imp)
        ds = pat["welfare"]["d"]
        a1 = plane([0, 0.8], [-0.2, 0.6], center=LEFT * 3.3 + DOWN * 2.0, x_length=5.0, y_length=2.6,
                   xticks=[0, 0.4, 0.8], yticks=[0, 0.5], xlabel=r"pension per worker, \ $d$",
                   ylabel=r"welfare change, \ \% of consumption", xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}",
                   font_size=14)
        a2 = plane([0, 0.8], [-15, 1], center=RIGHT * 3.3 + DOWN * 2.0, x_length=5.0, y_length=2.6,
                   xticks=[0, 0.4, 0.8], yticks=[-15, -10, -5, 0], xlabel=r"pension per worker, \ $d$",
                   ylabel=r"welfare change, \ \% of consumption", xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}",
                   font_size=14)
        c1 = path(a1, ds, ce_p, color=YOUNG, width=4)
        c2 = path(a2, ds, ce_i, color=OLD, width=4)
        best = int(np.argmax(ce_p))
        l1 = label(rf"best at $d = {ds[best]:g}$: \ $+{ce_p[best]:.2f}\%$", font_size=16, color=YOUNG).next_to(
            a1.ax.c2p(ds[best], ce_p[best]), UP, buff=0.12)
        l2 = label(rf"$d = {ds[-1]:g}$: \ ${ce_i[-1]:.1f}\%$", font_size=16, color=OLD).next_to(
            a2.ax.c2p(ds[-1], ce_i[-1]), UP + LEFT, buff=0.12)
        tag = agora_tag(corner=DR, font_size=13)
        with self.voiceover(
            "Now the question that made Diamond's model famous. <bookmark mark='a'/> In Part twenty, Phelps's "
            "golden rule chose the capital stock that maximizes consumption in the steady state. Here it is where "
            "the return on capital equals the growth factor, one plus n. <bookmark mark='b'/> Take a patient "
            f"economy, with beta {pat['beta']} a generation. It saves so much that the return on capital, "
            f"{pat['steady']['R']:.2f} a generation, is below the growth factor of {1 + o['n']:.1f}. It has more "
            "capital than the golden rule. Every generation could consume more, now and for ever, if it had less. "
            "That is dynamic inefficiency, and it is a failure of competitive markets with no externality in sight. "
            "<bookmark mark='c'/> Introduce a pay-as-you-go pension. Each young worker pays d, each retiree "
            "receives the larger young generation's payments. It returns one plus n, more than capital, so the young "
            "save less, capital falls toward the golden rule, and every generation gains, up to a pension of "
            f"{ds[best]:g}. A free lunch, though a small one. <bookmark mark='d'/> In an impatient economy, beta "
            f"{imp['beta']}, the return on capital is {imp['steady']['R']:.2f}, above the growth factor. Now the "
            "pension pays less than the capital it displaces, and every size of pension lowers welfare: by "
            f"{-ce_i[-1]:.0f} percent of consumption at the largest."
        ) as vo:
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1][0]))
            vo.wait_until("c")
            self.play(FadeIn(a1), FadeIn(tag), Create(c1), FadeIn(l1), run_time=2)
            vo.wait_until("d")
            self.play(FadeIn(rows[1][1]), FadeIn(a2), Create(c2), FadeIn(l2), run_time=2)
        self.clear_scene()

    def evidence(self):
        rows = VGroup(
            label(r"which economy do we live in?", font_size=28, color=E.ACCENT),
            label(r"comparing the safe interest rate with growth is misleading when returns are risky", font_size=22,
                  color=GREY_A),
            label(r"Abel, \ Mankiw, \ Summers and Zeckhauser, \ 1989: \ compare capital's cash flows with "
                  r"investment", font_size=22, color=WHITE),
            label(r"if capital pays out more than it takes in, \ year after year, \ the economy is efficient",
                  font_size=22, color=GREY_A),
            label(r"the United States and the other large OECD economies: \ efficient", font_size=23, color=SPEND),
            label(r"so a pay-as-you-go pension is a transfer between generations, \ not a free lunch; \ moving to a "
                  r"funded one leaves a generation paying twice \ (Part 42)", font_size=21, color=PENSION),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Abel, Mankiw, Summers and Zeckhauser, REStud 56(1) (1989): \ 1--19", corner=DR,
                            font_size=12)
        with self.voiceover(
            "Which economy do we live in? <bookmark mark='a'/> The safe interest rate has often been below the "
            "growth rate, which looks like inefficiency. But with risk, comparing the safe rate with growth is "
            "misleading. <bookmark mark='b'/> In 1989 Andrew Abel, Gregory Mankiw, Lawrence Summers and Richard "
            "Zeckhauser gave a test that works with risk. Compare the cash that capital pays out, profits and rents, "
            "with the investment it absorbs. <bookmark mark='c'/> If capital pays out more than it takes in, year "
            "after year, the economy is efficient. <bookmark mark='d'/> In the United States and the other large "
            "OECD economies, it did. <bookmark mark='e'/> So a pay-as-you-go pension is a transfer between "
            "generations, not a free lunch. And switching to a funded system has a catch: the generation in "
            "between must pay for its parents' pensions and save for its own. Part forty-two takes that up."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
