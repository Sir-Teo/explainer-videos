from __future__ import annotations

from videos.economics.econ4.common import *  # noqa: F403

CAND_COLOR = {"A": OLSC, "B": "#F2B84B", "C": "#5DADEC", "D": "#F28C6F"}


def countdown(radius: float = 0.42) -> VGroup:
    t = ValueTracker(1.0)
    back = Circle(radius=radius, stroke_color=GREY_D, stroke_width=5)
    arc = always_redraw(lambda: Arc(radius=radius, start_angle=PI / 2, angle=-TAU * max(t.get_value(), 1e-3),
                                    stroke_color=E.ACCENT, stroke_width=5).move_arc_center_to(back.get_center()))
    g = VGroup(back, arc)
    g.t = t
    return g


class PlayIt(VoiceoverScene):
    def construct(self):
        card(self, 1, r"Play it: \ find the demand curve", r"Which line through the cloud is the islanders' demand?",
             "Chapter one. Play it: find the demand curve.", scale=("market",), horizon=("a season",))
        self.choose()
        self.reveal()

    def choose(self):
        s, pl = load("season"), load("playit")
        stage = game_stage(13.0, 6.8, center=DOWN * 0.1)
        ax = fish_axes(center=stage.box.get_center() + LEFT * 2.6 + DOWN * 0.2, x_length=6.0, y_length=4.6)
        dots = day_dots(ax, s, radius=0.04)
        lines = VGroup()
        labels = VGroup()
        for k, slope in pl["candidates"].items():
            ln = line_qp(ax, slope, pl["q_mean"], pl["p_mean"], CAND_COLOR[k], width=3.5)
            lines.add(ln)
            # a flat line leaves the frame at the price axis: label it at its right-hand end instead
            lab = label(k, font_size=26, color=CAND_COLOR[k]).next_to(ln.ends[0] if abs(slope) > 100 else ln.ends[1],
                                                                      UP, buff=0.08)
            labels.add(lab)
        desc = VGroup(*[label(t, font_size=23, color=CAND_COLOR[k]) for k, t in (
            ("A", r"A \ \ the best fit through the dots"),
            ("B", r"B \ \ steep: \ buyers barely respond"),
            ("C", r"C \ \ in between"),
            ("D", r"D \ \ flat: \ buyers respond a great deal"))]).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        desc.move_to(stage.box.get_center() + RIGHT * 3.6 + UP * 0.7)
        q = label(r"Which is the demand curve?", font_size=30, color=E.ACCENT).next_to(desc, DOWN, buff=0.6)
        q.align_to(desc, LEFT)
        ring = countdown().next_to(q, DOWN, buff=0.4)
        tag = island_tag(r"simulated: the Island's fish market; the true curves are planted", corner=UR, font_size=15)
        with self.voiceover(
            "Your turn. Here is the season again: every dot a day. <bookmark mark='a'/> Four lines go through the "
            "middle of the cloud. <bookmark mark='b'/> A is the line that fits the dots best. B is steep: buyers who "
            "hardly respond to the price. C is in between. D is flat: buyers who respond a great deal. "
            "<bookmark mark='c'/> One of them is the islanders' true demand for fish: we planted it, so there is a "
            "right answer. Which one? And before you answer, ask yourself: what in the picture could tell you? "
            "Pause, and pick."
        ) as vo:
            self.play(FadeIn(stage), FadeIn(ax), FadeIn(tag), LaggedStart(*[FadeIn(d, scale=0.5) for d in dots],
                                                                         lag_ratio=0.004), run_time=2.0)
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(l) for l in lines], lag_ratio=0.25), FadeIn(labels), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d, shift=LEFT * 0.1) for d in desc], lag_ratio=0.4), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(q), FadeIn(ring))
        self.add(ring[1])
        self.play(ring.t.animate.set_value(0.0), run_time=4.0, rate_func=linear)
        self.clear_scene()

    def reveal(self):
        s, pl = load("season"), load("playit")
        ax = fish_axes(center=LEFT * 2.4 + DOWN * 0.2)
        a = ax.ax
        dots = day_dots(ax, s, radius=0.04)
        ols = line_qp(ax, s["ols_slope"], pl["q_mean"], pl["p_mean"], OLSC, width=3)
        q_ord = s["groups"]["ordinary"]["q"]
        p_ord = s["groups"]["ordinary"]["p"]
        dem = line_qp(ax, -s["b"], q_ord, p_ord, E.TRUTH, dashed=True)
        sup = line_qp(ax, s["d"], q_ord, p_ord, E.TRUTH, dashed=True)
        dl = label(r"planted demand", font_size=21, color=E.TRUTH).next_to(dem.ends[0], UP, buff=0.1)
        sl = label(r"planted supply", font_size=21, color=E.TRUTH).next_to(sup.ends[1], UP, buff=0.1)
        rows = VGroup(
            label(r"the answer: \ C", font_size=34, color=E.TRUTH),
            label(rf"demand: \ ${-s['b']:.1f}$ fish per dollar", font_size=24, color=E.TRUTH),
            label(rf"supply: \ $+{s['d']:.1f}$ fish per dollar", font_size=24, color=E.TRUTH),
            label(rf"the best fit A: \ $+{s['ols_slope']:.1f}$: \ neither", font_size=24, color=OLSC),
            label(r"nothing in the cloud alone \\ could have told you", font_size=26, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.5).shift(UP * 0.3)
        tag = island_tag(r"simulated: the Island; truth planted in explainer.economics.island", corner=DR, font_size=15)
        with self.voiceover(
            "Here is the truth. <bookmark mark='a'/> The islanders' demand is line C: every dollar on the price "
            f"costs about {s['b']:.0f} fish a day. <bookmark mark='b'/> And here is the supply curve we planted, "
            "sloping up. <bookmark mark='c'/> The line that fits the dots best, A, is neither. "
            "<bookmark mark='d'/> If you chose C, you were lucky, or you guessed what a demand curve usually looks "
            "like. Nothing in the cloud could have told you. The same dots could have come from a steep demand "
            "curve, or a flat one, if the curves had moved differently. To find out which, you need to know why "
            "the dots are where they are."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(dots), Create(ols))
            vo.wait_until("a")
            self.play(Create(dem), FadeIn(dl), FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(Create(sup), FadeIn(sl), FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(Indicate(ols, color=OLSC), FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(FadeIn(rows[4]))
        self.clear_scene()
