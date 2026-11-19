from __future__ import annotations

from explainer.music.monochord.audio import ClipStore
from explainer.music.sound import SoundScene

from videos.economics.econ4.common import *  # noqa: F403

MONTH_COLOR = ["#5DADEC", "#6FB7E8", "#7EC8F5", "#7BD88F", "#A6D96A", "#D9EF8B", "#F7D154", "#F2B84B",
               "#F28C6F", "#F26D6D", "#E9A3C9", "#C9A0FF"]
MONTHS = ["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"]


class Intermission(SoundScene):
    """The draft lottery of 1 December 1969, without narration: 366 capsules, one per birthday, drawn in order, each
    placed by its birthday (across) and the order it was drawn (up), with each month's average order beside them;
    under it, each capsule's birth month as a pitch, so that a fair draw would wander and this one does not; then the
    story so far."""

    def construct(self):
        film, dr = load("film"), load("draft")
        clip = ClipStore("econ4").load("intermission.melody")
        days = np.array(film["order_day"])
        months = np.array(film["order_month"])
        times = np.array(film["times"])
        x0, x1, y0, y1 = -5.5, 1.9, -2.7, 2.3

        def X(day):
            return x0 + (x1 - x0) * (day - 0.5) / 366

        def Y(rank):
            return y1 - (y1 - y0) * (rank - 1) / 365

        frame = VGroup(Line([x0, y0, 0], [x1, y0, 0], color=GREY_C, stroke_width=2),
                       Line([x0, y0, 0], [x0, y1, 0], color=GREY_C, stroke_width=2))
        starts = np.cumsum([0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30])
        for k, st in enumerate(starts):
            frame.add(label(MONTHS[k], font_size=20, color=GREY_B).move_to([X(st + 15), y0 - 0.25, 0]))
        frame.add(label(r"birthday", font_size=20, color=GREY_A).move_to([(x0 + x1) / 2, y0 - 0.65, 0]))
        frame.add(label(r"called first", font_size=18, color=GREY_B).next_to([x0, y1, 0], LEFT, buff=0.1))
        frame.add(label(r"called last", font_size=18, color=GREY_B).next_to([x0, y0, 0], LEFT, buff=0.1))
        dots = VGroup(*[Dot([X(d), Y(k + 1), 0], radius=0.045, color=MONTH_COLOR[m - 1]).set_opacity(0)
                        for k, (d, m) in enumerate(zip(days, months))])
        # each month's average order so far, as bars on the right (higher bar: called earlier on average)
        bx0, bx1, by0, by1 = 2.7, 6.6, -2.7, 2.3
        bw = (bx1 - bx0) / 12
        bars = VGroup()
        for m in range(12):
            r = Rectangle(width=bw * 0.75, height=0.01, stroke_width=0, fill_color=MONTH_COLOR[m], fill_opacity=0.9)
            r.move_to([bx0 + bw * (m + 0.5), by0, 0], aligned_edge=DOWN)
            bars.add(r)
        bframe = VGroup(Line([bx0, by0, 0], [bx1, by0, 0], color=GREY_C, stroke_width=2),
                        DashedLine([bx0, by0 + (by1 - by0) * 0.5, 0], [bx1, by0 + (by1 - by0) * 0.5, 0],
                                   color=GREY_B, stroke_width=1.2))
        for m in range(12):
            bframe.add(label(MONTHS[m], font_size=18, color=GREY_B).move_to([bx0 + bw * (m + 0.5), by0 - 0.25, 0]))
        bframe.add(label(r"how early each month is called, \\ against the draws so far", font_size=18, color=GREY_A).move_to(
            [(bx0 + bx1) / 2, by1 + 0.35, 0]))
        bframe.add(label(r"fair", font_size=16, color=GREY_B).next_to([bx1, by0 + (by1 - by0) * 0.5, 0], RIGHT,
                                                                      buff=0.05))
        cap = label(r"capsules drawn:", font_size=20, color=GREY_B).move_to([x0, y1 + 0.5, 0], aligned_edge=LEFT)
        counter = Integer(0, font_size=36, color=GREY_A).next_to(cap, RIGHT, buff=0.15)
        verdict = label(rf"a fair draw would show no trend; \ this one: \ correlation ${dr['rho']:.2f}$, \ "
                        rf"{round(dr['p_perm'] * 20000)} of 20{{,}}000 fair shuffles came as far", font_size=21, color=E.MISS)
        verdict.to_edge(UP, buff=0.2).set_opacity(0)
        tag = data_tag(r"Selective Service System, the lottery of 1 December 1969 (JSE data archive)", corner=DL,
                       font_size=14)
        stag = note(r"sound: each birthday's month as a pitch, \ in the order drawn (computed)", font_size=14,
                    color=E.ACCENT).to_corner(DR, buff=0.3)
        rank_of = {}

        def k_at(t):
            return int(np.clip(np.searchsorted(times, t, side="right"), 0, 366))

        def draw(m, t):
            k = k_at(t)
            for i, d in enumerate(m):
                d.set_opacity(0.95 if i < k else 0.0)

        def count(m, t):
            m.set_value(k_at(t))
            m.next_to(cap, RIGHT, buff=0.15)

        def grow(m, t):
            k = k_at(t)
            for mo in range(12):
                sel = [j + 1 for j in range(k) if months[j] == mo + 1]
                if not sel:
                    continue
                avg = float(np.mean(sel))
                # the month's average place among the k drawn so far, 1 (first) to k (last), as a height: a fair
                # draw keeps every bar near the middle line at every k, since its expected place is (k + 1) / 2
                frac = 1 - (avg - 1) / (k - 1) if k > 1 else 0.5
                h = max((by1 - by0) * frac, 0.01)
                m[mo].stretch_to_fit_height(h).move_to([bx0 + bw * (mo + 0.5), by0, 0], aligned_edge=DOWN)

        def show_verdict(m, t):
            m.set_opacity(1.0 if t >= times[-1] + 0.3 else 0.0)

        del rank_of
        with self.listen(clip) as snd:
            snd.caption(r"the draft lottery of 1969, \ capsule by capsule, \ under each birthday's month as a pitch")
            snd.show(tag, stag)
            snd.drive(dots, draw)
            snd.drive(counter, count)
            snd.drive(bars, grow)
            snd.drive(verdict, show_verdict)
            snd.show(dots, counter, cap, bars, verdict, frame, bframe)
            self.play(FadeIn(frame), FadeIn(bframe), run_time=1.2)
            snd.wait_until("film_end")
            self.play(*[FadeOut(m) for m in (frame, bframe, dots, bars, tag, stag, verdict, cap)],
                      counter.animate.set_opacity(0.0), run_time=1.0)
            story = point_cards([
                (r"one cloud, two curves", r"prices and quantities trace \\ whichever curve moved less", OLSC),
                (r"the instrument", r"something that moves one curve \\ and not the other", IVC),
                (r"identification", r"what the data could reveal \\ even with infinite data", E.ACCENT),
                (r"omitted variables", r"ability raises school and pay: \\ the line overstates", "#F2B84B"),
                (r"selection", r"trainees differ before \\ the training starts", NONEXP),
                (r"LaLonde's test", r"the methods missed the experiment, \\ and could not tell", EXP),
            ], width=12.6, cols=3, font_size=22).move_to(DOWN * 0.3)
            head = label(r"The story so far", font_size=40).to_edge(UP, buff=0.5)
            nxt = label(r"next: \ the lotteries the world runs anyway, \ experiments, \ and Lucas", font_size=22,
                        color=GREY_B).to_edge(DOWN, buff=0.4)
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in story.cards], lag_ratio=0.6),
                      run_time=max(3.0, snd.remaining() - 1.6))
            self.play(FadeIn(nxt))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
