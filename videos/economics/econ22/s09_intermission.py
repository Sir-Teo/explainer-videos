from __future__ import annotations

from explainer.music.monochord.audio import ClipStore
from explainer.music.sound import SoundScene

from videos.economics.econ22.common import *  # noqa: F403


class Intermission(SoundScene):
    """Thirty-six years of income and spending, month by month: real disposable income and real spending on
    nondurables and services (January 1990 = 1), with the saving rate below, drawn as a date counter runs; the rebate
    spikes of 2001, 2008 and 2020-21 marked as they pass; under it, the saving rate as a tune; then the story so far."""

    def construct(self):
        film = load("film")
        clip = ClipStore("econ22").load("intermission.melody")
        t = np.array(film["t"])
        top = plane([1990, 2027], [0.9, 3.5], center=UP * 1.15 + LEFT * 0.3, x_length=11.6, y_length=3.0,
                    xticks=[1990, 2000, 2010, 2020], yticks=[1, 2, 3], ylabel=r"January 1990 $= 1$",
                    xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}", font_size=14)
        bot = plane([1990, 2027], [0, 35], center=DOWN * 2.2 + LEFT * 0.3, x_length=11.6, y_length=1.9,
                    xticks=[], yticks=[0, 10, 20, 30], ylabel=r"saving rate, \ \%",
                    yfmt=lambda v: f"{v:g}", font_size=14)
        full_y = path(top, t, film["Y"], color=INCOME, width=2.5, smooth=False)
        full_c = path(top, t, film["C"], color=SPEND, width=3, smooth=False)
        full_s = path(bot, t, film["saving"], color=SAVE, width=2.5, smooth=False)
        gy, gc, gs = full_y.copy(), full_c.copy(), full_s.copy()
        t0, t1 = film_time(t[0]), film_time(t[-1])

        def grower(full):
            def f(m, tt):
                frac = float(np.clip((tt - t0) / (t1 - t0), 1e-3, 1))
                m.pointwise_become_partial(full, 0, frac)
            return f

        year = Integer(1990, font_size=48, color=E.ACCENT, group_with_commas=False).move_to(
            top.ax.c2p(1995, 3.1))

        def set_year(m, tt):
            y = t[0] + (tt - t0) / (t1 - t0) * (t[-1] - t[0])
            m.set_value(int(np.clip(y, t[0], t[-1])))

        marks = VGroup()
        for ev in film["events"]:
            x = top.ax.c2p(ev["t"], 0.9)[0]
            ln = DashedLine([x, top.ax.c2p(0, 0.95)[1], 0], [x, bot.ax.c2p(0, 0)[1], 0], color=GREY_B,
                            stroke_width=1.2, dash_length=0.06)
            tx = label(ev["say"], font_size=13, color=GREY_A).next_to([x, top.ax.c2p(0, 3.4)[1], 0],
                                                                      RIGHT if ev["t"] < 2015 else LEFT, buff=0.05)
            marks.add(VGroup(ln, tx))
        # keep the event labels apart vertically
        for k, mk in enumerate(marks):
            mk[1].shift(DOWN * 0.25 * k)

        def appear(ev, ttl=7.0):
            def f(m, tt):
                a = float(np.clip((tt - ev["time"]) / 0.6, 0, 1))
                m[0].set_opacity(a * 0.8)
                m[1].set_opacity(a * float(np.clip((ev["time"] + ttl - tt) / 1.0, 0, 1)))
            return f

        for mk in marks:
            mk.set_opacity(0)
        leg = VGroup(label(r"real disposable income", font_size=15, color=INCOME),
                     label(r"real spending on nondurables and services", font_size=15, color=SPEND)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.06).move_to(top.ax.c2p(2003, 2.5))
        src = data_tag(r"BEA via FRED: \ DSPIC96, \ PCEND, \ PCES, \ PSAVERT", corner=DL, font_size=13).to_edge(
            UP, buff=0.12).to_edge(LEFT, buff=0.3)
        stag = note(r"sound: \ the saving rate, \ quarter by quarter \ (computed)", font_size=13,
                    color=E.ACCENT).to_corner(UR, buff=0.15)
        with self.listen(clip) as snd:
            snd.caption(r"income and spending, \ month by month, \ 1990--2026; \ the saving rate as a tune")
            snd.show(src, stag)
            for g, full in ((gy, full_y), (gc, full_c), (gs, full_s)):
                snd.drive(g, grower(full))
            for mk, ev in zip(marks, film["events"]):
                snd.drive(mk, appear(ev))
            snd.drive(year, set_year)
            snd.show(top, bot, gy, gc, gs, year, leg, *marks)
            self.play(FadeIn(top), FadeIn(bot), FadeIn(leg), run_time=1.2)
            snd.wait_until("film_end")
            self.play(*[FadeOut(m) for m in (top, bot, gy, gc, gs, year, leg, marks, src, stag)], run_time=1.0)
            story = point_cards([
                (r"Keynes and Kuznets", r"the rich save more; \\ nations do not", SPEND),
                (r"permanent income", r"spend the annuity \\ of a windfall", INCOME),
                (r"Hall's random walk", r"rejected: \ past income \\ predicts spending", HOLD),
                (r"too sensitive, \ too smooth", r"rule-of-thumb \\ households", SAVE),
                (r"the buffer stock", r"prudence bends \\ the consumption function", CASH),
                (r"the rebates", r"20--40\% in a quarter, \\ most for the cash-poor", HOUSE),
            ], width=12.6, cols=3, font_size=22).move_to(DOWN * 0.3)
            head = label(r"The story so far", font_size=40).to_edge(UP, buff=0.5)
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in story.cards], lag_ratio=0.6),
                      run_time=max(3.0, snd.remaining() - 0.6))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
