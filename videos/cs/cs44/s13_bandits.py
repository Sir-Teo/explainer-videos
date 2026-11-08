from __future__ import annotations

from scipy.stats import beta as beta_dist

from explainer.cs import *  # noqa: F403
from videos.cs.cs44.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, axes, load, tag_box, trace


class Bandits(VoiceoverScene):
    def construct(self):
        self.card()
        self.thompson()
        self.regret()
        self.metrics()
        self.goodhart()
        self.dark()
        self.consent()

    def card(self):
        card = chapter_card(12, r"Bandits and metrics", r"Should an experiment earn while it learns, \ and what "
                            r"should it count?", lit=(1933, 2010),
                            extra=((1933, r"Thompson: \ sampling"), (1975, r"Goodhart"),
                                   (2010, r"Brignull: \ dark patterns")), part=PART)
        with self.voiceover("Chapter twelve. Bandits and metrics."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def thompson(self):
        head = label(r"Earning while learning", font_size=36).to_edge(UP, buff=0.3)
        g = axes([0, 0.12, 0.02], [0, 100, 20], x_length=7.2, y_length=3.8, x_label=r"conversion rate",
                 y_label=r"belief", xticks=(0.02, 0.04, 0.06, 0.08, 0.1), fx=lambda v: f"{100 * v:.0f}\\%").move_to(
            [-2.8, -0.2, 0])
        ax = g.ax
        xs = np.linspace(0.001, 0.119, 240)

        def dens(a, b, col):
            return trace(ax, [(x, min(99.0, beta_dist.pdf(x, a, b))) for x in xs], col, width=3)
        early = {"A": (20, 380), "B": (26, 374)}
        late = {"A": (52, 948), "B": (168, 2832)}
        cols = {"A": GREY_B, "B": HEAD}
        curves = VGroup(*[dens(*early[k], cols[k]) for k in "AB"])
        curves2 = VGroup(*[dens(*late[k], cols[k]) for k in "AB"])
        names = VGroup(label(r"A", font_size=22, color=GREY_B).next_to(ax.c2p(0.045, 38), LEFT, buff=0.1),
                       label(r"B", font_size=22, color=HEAD).next_to(ax.c2p(0.072, 33), RIGHT, buff=0.1))
        rng = np.random.default_rng(26)
        rounds = []
        for _ in range(3):
            d = {k: float(rng.beta(*early[k])) for k in "AB"}
            w = max(d, key=d.get)
            dots = VGroup(*[Dot(ax.c2p(d[k], 0), radius=0.08, color=cols[k]) for k in "AB"])
            res = label(rf"draws: \ A {100 * d['A']:.1f}\%, \ B {100 * d['B']:.1f}\% \ $\to$ \ show {w}",
                        font_size=19, color=cols[w]).next_to(g, DOWN, buff=0.15)
            rounds.append((dots, res))
        ill = note(r"illustrative beliefs", font_size=17).next_to(g, UP, buff=0.1).align_to(g, RIGHT)
        notes = VGroup(
            wrapped_label(r"an A/B test gives the worse version half the traffic until the end, \ on purpose", 4.3,
                          font_size=20, color=GREY_A),
            wrapped_label(r"\textbf{Thompson sampling} \ (1933; \ \textit{AI, Built} Part 26): \ a beta "
                          r"distribution of belief for each version", 4.3, font_size=20, color=WHITE),
            wrapped_label(r"for each visitor, \ draw one plausible rate from each belief; \ show the version whose "
                          r"draw is higher", 4.3, font_size=20, color=HEAD),
            wrapped_label(r"a version is tried exactly as often as it might be the best", 4.3, font_size=20,
                          color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.5, -0.2, 0])
        with self.voiceover(
            "An A/B test gives the worse version half its traffic until the end, on purpose. A bandit, named after "
            "the casino's one-armed bandits, shifts traffic while it learns. <bookmark mark='a'/> Part 26 of AI, "
            "Built met the oldest good rule, Thompson sampling, from William Thompson in 1933. Keep a belief about "
            "each version's conversion rate. <bookmark mark='b'/> For each visitor, draw one plausible rate from "
            "each belief, and show the version whose draw is higher. <bookmark mark='c'/> As evidence arrives the "
            "beliefs narrow, and a version is tried exactly as often as it might still be the best."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(notes[0]), FadeIn(ill))
            vo.wait_until("a")
            self.play(Create(curves), FadeIn(names), FadeIn(notes[1]))
            vo.wait_until("b")
            self.play(FadeIn(notes[2]))
            prev = None
            for dots, res in rounds:
                self.play(*([FadeOut(prev)] if prev else []), FadeIn(dots, scale=1.5), FadeIn(res), run_time=0.7)
                self.wait(0.4)
                prev = VGroup(dots, res)
            vo.wait_until("c")
            self.play(FadeOut(prev), Transform(curves, curves2), names[1].animate.next_to(ax.c2p(0.062, 92), RIGHT,
                                                                                          buff=0.1),
                      names[0].animate.next_to(ax.c2p(0.046, 56), LEFT, buff=0.1), FadeIn(notes[3]), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def regret(self):
        b = load("bandit")
        pa, pb = b["p"]
        head = label(r"Regret against precision", font_size=36).to_edge(UP, buff=0.3)
        H = 3.0
        vmax = max(b["regret_ab"], b["regret_ts"])
        y0 = -1.9
        bars = VGroup()
        for i, (v, col, nm) in enumerate(((b["regret_ab"], GREY_B, r"50/50 split"),
                                          (b["regret_ts"], HEAD, r"Thompson"))):
            r = Rectangle(width=1.0, height=v / vmax * H, stroke_width=0, fill_color=col, fill_opacity=0.85)
            r.move_to([-5.6 + i * 1.6, y0, 0], aligned_edge=DOWN)
            bars.add(VGroup(r, label(f"{v:.0f}", font_size=20, color=col).next_to(r, UP, buff=0.08),
                            label(nm, font_size=18, color=col).next_to(r, DOWN, buff=0.12)))
        bt = label(r"conversions lost \ (regret)", font_size=19, color=GREY_A).move_to([-4.8, 2.1, 0])
        # the estimated difference with 95% error bars, against zero
        line = NumberLine(x_range=[-0.015, 0.025, 0.005], length=5.6, color=GREY_C).move_to([2.2, -2.0, 0])
        tl = VGroup(*[label(rf"{100 * v:+.1f}" if v else "0", font_size=16, color=GREY_B).next_to(line.n2p(v), DOWN,
                                                                                                 buff=0.12)
                      for v in (-0.01, 0.0, 0.01, 0.02)])
        unit = label(r"estimated B $-$ A, \ points", font_size=17, color=GREY_A).next_to(line, DOWN, buff=0.45)
        zero = DashedLine(line.n2p(0) + DOWN * 0.1, line.n2p(0) + UP * 2.9, color=NO)
        truth = DashedLine(line.n2p(b["true_diff"]) + DOWN * 0.1, line.n2p(b["true_diff"]) + UP * 2.9, color=YES)
        tlab = label(rf"true {100 * b['true_diff']:+.1f}", font_size=16, color=YES).next_to(truth, UP, buff=0.05)

        def ebar(sd, y, col):
            a, c = line.n2p(b["true_diff"] - 1.96 * sd) + UP * y, line.n2p(b["true_diff"] + 1.96 * sd) + UP * y
            return VGroup(Line(a, c, color=col, stroke_width=6), Line(a + UP * 0.12, a + DOWN * 0.12, color=col),
                          Line(c + UP * 0.12, c + DOWN * 0.12, color=col))
        e1, e2 = ebar(b["sd_ab"], 1.9, GREY_B), ebar(b["sd_ts"], 0.9, HEAD)
        el = VGroup(label(rf"split: \ sd {b['sd_ab']:.4f}", font_size=17, color=GREY_B).next_to(e1, RIGHT,
                                                                                               buff=0.15),
                    label(rf"Thompson: \ sd {b['sd_ts']:.4f}", font_size=17, color=HEAD).next_to(e2, RIGHT,
                                                                                                 buff=0.15))
        top = wrapped_label(rf"{b['n']:,} visitors; \ versions converting {100 * pa:.1f}\% and {100 * pb:.1f}\%; \ "
                            r"200 repetitions; \ the bandit updates every 500 visitors", 7.0, font_size=19,
                            color=GREY_A).move_to([2.4, 2.25, 0])
        moral = wrapped_label(r"bandits for optimizing, \ A/B tests for learning", 6.0, font_size=24,
                              color=WHITE).to_edge(DOWN, buff=0.3).shift(LEFT * 2.6)
        ratio = b["sd_ts"] / b["sd_ab"]
        with self.voiceover(
            f"We raced the two on {b['n']:,} visitors, with versions converting {100 * pa:.0f} and "
            f"{100 * pb:.1f} percent. <bookmark mark='a'/> The fifty-fifty split loses about {b['regret_ab']:.0f} "
            "conversions against always showing the better one: its regret. Thompson sampling loses about "
            f"{b['regret_ts']:.0f}. <bookmark mark='b'/> But look at what each "
            f"learns. The split measures the difference with a standard deviation of {100 * b['sd_ab']:.2f} points. "
            f"The bandit, having starved the worse version, is about {ratio:.0f} times less precise, and its "
            "interval easily includes zero. <bookmark mark='c'/> So: bandits for optimizing, when only the reward "
            "matters, like a headline that lives a day; A/B tests for learning how big an effect is."
        ) as vo:
            self.play(FadeIn(head), FadeIn(top), FadeIn(bt))
            vo.wait_until("a")
            self.play(*[GrowFromEdge(x[0], DOWN) for x in bars], *[FadeIn(x[1:]) for x in bars])
            vo.wait_until("b")
            self.play(Create(line), FadeIn(tl), FadeIn(unit), Create(zero), Create(truth), FadeIn(tlab))
            self.play(Create(e1), FadeIn(el[0]))
            self.play(Create(e2), FadeIn(el[1]))
            vo.wait_until("c")
            self.play(FadeIn(moral))
        self.wait(0.4)
        self.clear_scene()

    def metrics(self):
        head = label(r"What to count", font_size=36).to_edge(UP, buff=0.3)

        def box(t, col, w=3.0):
            r = RoundedRectangle(width=w, height=0.62, corner_radius=0.1, stroke_color=col, fill_color=col,
                                 fill_opacity=0.12)
            return VGroup(r, label(t, font_size=19, color=WHITE).move_to(r))
        star = box(r"north star: \ weekly active buyers", YES, w=4.6).move_to([0, 1.9, 0])
        drivers = VGroup(*[box(t, DATA) for t in (r"searches that end in a purchase", r"repeat buyers",
                                                  r"items per basket")]).arrange(RIGHT, buff=0.35).move_to(
            [0, 0.5, 0])
        arrows = VGroup(*[Arrow(d.get_top(), star.get_bottom() + RIGHT * 0.35 * d.get_x(), buff=0.08,
                                stroke_width=2, color=GREY_B, max_tip_length_to_length_ratio=0.12) for d in drivers])
        guards = VGroup(*[box(t, NO, w=2.7) for t in (r"page load time", r"crash rate", r"unsubscribes",
                                                      r"support tickets")]).arrange(RIGHT, buff=0.25).move_to(
            [0, -1.1, 0])
        band = SurroundingRectangle(guards, color=NO, buff=0.18, corner_radius=0.1, stroke_width=1.5)
        gl = label(r"guardrails: \ must not get worse", font_size=18, color=NO).next_to(band, DOWN, buff=0.1)
        ill = note(r"illustrative metrics", font_size=17).to_corner(UR, buff=0.3).shift(DOWN * 0.5)
        foot = wrapped_label(r"ship when the overall evaluation criterion improves \ (Kohavi) \ and no guardrail "
                             r"regresses; \ latency is a guardrail because Part 42 showed what it costs", 12.4,
                             font_size=20, color=WHITE).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "An experiment must know what better means. <bookmark mark='a'/> Companies choose a north-star "
            "metric, the one number that stands for value delivered to users, here weekly active buyers. "
            "<bookmark mark='b'/> Under it sit driver metrics that move faster and that a team can actually "
            "change. <bookmark mark='c'/> Beside them are guardrails: load time, crashes, unsubscribes, support "
            "tickets, which must not get worse whatever else improves. <bookmark mark='d'/> A change ships when "
            "the overall evaluation criterion, as Ron Kohavi calls it, improves and no guardrail regresses."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ill))
            vo.wait_until("a")
            self.play(FadeIn(star, shift=DOWN * 0.2))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d) for d in drivers], lag_ratio=0.2), *[GrowArrow(a) for a in arrows])
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(x) for x in guards], lag_ratio=0.2), Create(band), FadeIn(gl))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def goodhart(self):
        head = label(r"Goodhart's law", font_size=36).to_edge(UP, buff=0.3)
        quote = label(r"\textit{``When a measure becomes a target, \ it ceases to be a good measure.''}",
                      font_size=26, color=HEAD).next_to(head, DOWN, buff=0.4)
        src = note(r"Marilyn Strathern's \ (1997) \ wording of Charles Goodhart's \ (1975) \ observation",
                   font_size=18).next_to(quote, DOWN, buff=0.12)
        g = axes([0, 10, 2], [0, 10, 2], x_length=6.0, y_length=3.4, x_label=r"optimization pressure on the metric",
                 y_label=r"value").move_to([-3.2, -1.5, 0])
        ax = g.ax
        ts = np.linspace(0, 10, 60)
        proxy = trace(ax, [(t, 0.5 + 0.9 * t) for t in ts], DATA, width=3.5)
        true = trace(ax, [(t, 0.5 + 2.2 * t - 0.22 * t * t) for t in ts], YES, width=3.5)
        pl = label(r"the metric: \ clicks", font_size=18, color=DATA).next_to(ax.c2p(10, 9.5), LEFT, buff=0.1)
        tl = label(r"what it stood for: \ satisfied users", font_size=18, color=YES).move_to(ax.c2p(6.2, 1.4))
        ill = note(r"illustrative", font_size=17).next_to(g, RIGHT, buff=0.1).align_to(g, DOWN)
        notes = VGroup(
            wrapped_label(r"clickbait raises clicks; \ notifications raise sessions; \ an endless feed raises time "
                          r"spent", 5.3, font_size=20, color=WHITE),
            wrapped_label(r"a learning system finds the gap faster than any person: \ reward hacking \ "
                          r"(\textit{AI, Built} Part 31)", 5.3, font_size=20, color=LAM),
            wrapped_label(r"defences: \ several metrics, \ guardrails, \ long-term holdouts, \ and asking users", 5.3,
                          font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.7, -1.4, 0])
        with self.voiceover(
            "Any metric can be gamed by the experiments meant to improve it. <bookmark mark='a'/> The economist "
            "Charles Goodhart observed it of monetary targets in 1975; the anthropologist Marilyn Strathern gave it "
            "the famous wording: when a measure becomes a target, it ceases to be a good measure. "
            "<bookmark mark='b'/> Push hard on clicks and clickbait wins; the metric keeps rising after what it "
            "stood for starts to fall. <bookmark mark='c'/> A learning system finds that gap faster than any "
            "person: reward hacking, from Part 31 of AI, Built. <bookmark mark='d'/> The defences: several "
            "metrics, guardrails, long holdouts, and asking users."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(quote), FadeIn(src))
            vo.wait_until("b")
            self.play(FadeIn(g), FadeIn(ill), FadeIn(notes[0]))
            self.play(Create(proxy), Create(true), FadeIn(pl), FadeIn(tl), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(notes[1]))
            vo.wait_until("d")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def dark(self):
        head = label(r"Dark patterns", font_size=36).to_edge(UP, buff=0.3)
        # a subscription that is one click to join and a maze to leave
        join = VGroup(RoundedRectangle(width=2.6, height=0.7, corner_radius=0.12, stroke_color=YES, fill_color=YES,
                                       fill_opacity=0.3),
                      label(r"Join now", font_size=22, color=WHITE))
        join[1].move_to(join[0])
        join.move_to([-4.3, 1.7, 0])
        steps = VGroup(*[tag_box(t, color=GREY_B, size=16) for t in (
            "Settings", "Account", "Membership", "Are you sure?", "Special offer!", "Call to cancel")])
        for i, st in enumerate(steps):  # a snake: left to right, then down, then right to left
            st.move_to([(-5.5, -3.1, -0.7)[i if i < 3 else 5 - i], -0.6 if i < 3 else -1.7, 0])
        ends = [(steps[i].get_right(), steps[i + 1].get_left()) if i < 2 else
                (steps[i].get_bottom(), steps[i + 1].get_top()) if i == 2 else
                (steps[i].get_left(), steps[i + 1].get_right()) for i in range(len(steps) - 1)]
        chain = VGroup(*[Arrow(a, c, buff=0.06, stroke_width=2, color=NO, max_tip_length_to_length_ratio=0.2)
                         for a, c in ends])
        one = Arrow(join.get_bottom() + DOWN * 0.05, join.get_bottom() + DOWN * 0.9, buff=0, color=YES,
                    stroke_width=3)
        ol = label(r"one click in", font_size=17, color=YES).next_to(one, RIGHT, buff=0.1)
        sub = label(r"subscribed", font_size=18, color=YES).next_to(one, DOWN, buff=0.08)
        ml = label(r"six steps out \ (illustrative)", font_size=17, color=NO).next_to(steps, DOWN, buff=0.2)
        shame = VGroup(RoundedRectangle(width=4.6, height=0.6, corner_radius=0.1, stroke_color=GREY_C),
                       label(r"No thanks, \ I don't like saving money", font_size=18, color=GREY_B))
        shame[1].move_to(shame[0])
        notes = VGroup(
            wrapped_label(r"Harry Brignull \ (2010): \ designs that trick people into doing what they did not "
                          r"mean to", 5.0, font_size=20, color=WHITE),
            wrapped_label(r"easy in, \ hard out; \ a pre-ticked box; \ a cost revealed at the last step; \ "
                          r"guilt on the button that says no:", 5.0, font_size=20, color=NO),
            shame,
            wrapped_label(r"an A/B test that counts only today's sign-ups will find these by itself, \ and "
                          r"report them as wins", 5.0, font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.7, -0.2, 0])
        with self.voiceover(
            "A short-term number can also turn a product against its users. <bookmark mark='a'/> In 2010 the "
            "designer Harry Brignull named dark patterns: designs that trick people into doing what they did not "
            "mean to. <bookmark mark='b'/> One click to subscribe, six steps to leave. A box ticked in advance. A "
            "cost that appears at the last step. A refusal button that mocks you. <bookmark mark='c'/> And an "
            "experiment that counts only today's sign-ups will discover these by itself, and call each a win."
        ) as vo:
            self.play(FadeIn(head), FadeIn(notes[0]))
            vo.wait_until("a")
            self.play(FadeIn(join), GrowArrow(one), FadeIn(ol), FadeIn(sub))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s) for s in steps], lag_ratio=0.25), Create(chain), FadeIn(ml),
                      FadeIn(notes[1]), run_time=2.5)
            self.play(FadeIn(notes[2]))
            vo.wait_until("c")
            self.play(FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()

    def consent(self):
        head = label(r"Experimenting on people", font_size=36).to_edge(UP, buff=0.3)
        feed = VGroup(*[RoundedRectangle(width=2.6, height=0.5, corner_radius=0.08, stroke_color=c, fill_color=c,
                                         fill_opacity=0.2) for c in (YES, GREY_B, NO, YES, GREY_B, NO)])
        feed.arrange(DOWN, buff=0.12).move_to([-4.6, -0.3, 0])
        frame = SurroundingRectangle(feed, color=GREY_B, buff=0.2, corner_radius=0.12)
        fl = label(r"a news feed", font_size=18, color=GREY_A).next_to(frame, UP, buff=0.1)
        hide = [feed[0], feed[3]]
        notes = VGroup(
            wrapped_label(r"Kramer, \ Guillory and Hancock \ (\textit{PNAS}, \ 2014): \ for one week in January 2012, "
                          r"\ about 689,000 Facebook users were shown fewer positive, \ or fewer negative, \ posts",
                          7.4, font_size=20, color=WHITE),
            wrapped_label(r"their own posts shifted slightly the same way: \ a small measured effect", 7.4,
                          font_size=20, color=GREY_A),
            wrapped_label(r"the reaction: \ nobody had been asked; \ the journal published an editorial expression "
                          r"of concern; \ the paper had treated Facebook's data use policy as consent", 7.4,
                          font_size=20, color=NO),
            wrapped_label(r"the Belmont Report \ (1979): \ respect for persons, \ beneficence, \ justice; \ product "
                          r"tests rarely pass an ethics board, \ but the principles still apply", 7.4, font_size=20,
                          color=YES),
            wrapped_label(r"measuring without watching anyone: \ privacy-preserving analytics, \ Chapter 13", 7.4,
                          font_size=20, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).move_to([2.4, -0.3, 0])
        with self.voiceover(
            "Every A/B test is an experiment on people, usually a harmless one. <bookmark mark='a'/> In 2014 Adam "
            "Kramer, Jamie Guillory and Jeffrey Hancock reported that for one week in January 2012, about six "
            "hundred and eighty-nine thousand Facebook users had been shown fewer positive posts, or fewer negative "
            "ones. <bookmark mark='b'/> Their own posts shifted slightly the same way. <bookmark mark='c'/> The "
            "reaction was strong: no one had been asked, and the journal published an editorial expression of "
            "concern. <bookmark mark='d'/> The Belmont Report of 1979 asks research on people for respect for "
            "persons, beneficence and justice; few product tests meet an ethics board, but the principles apply. "
            "<bookmark mark='e'/> Measuring without watching anyone is for the frontier."
        ) as vo:
            self.play(FadeIn(head), FadeIn(feed), Create(frame), FadeIn(fl))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]), *[h.animate.set_opacity(0.15) for h in hide])
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
            vo.wait_until("e")
            self.play(FadeIn(notes[4]))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, KERN, LAM, DATA)
