from __future__ import annotations

from explainer.music.monochord.audio import ClipStore
from explainer.music.sound import SoundScene

from videos.economics.econ1.common import *  # noqa: F403

LO, HI = np.log10(300), np.log10(150000)


class Intermission(SoundScene):
    """Two hundred years in thirty-three seconds, without narration: every country's income per head, year by year,
    under the world's income per head played as a tune (the series' data melody); then the story so far."""

    def construct(self):
        film = load("film")
        mel = load("melody")
        clip = ClipStore("econ1").load("intermission.melody")
        years = np.array(film["years"])
        G, P = np.array(film["log_gdppc"]), np.array(film["log_pop"])
        regions = film["regions"]
        lanes = [r for r in ("Western Offshoots", "Western Europe", "Eastern Europe", "Latin America",
                             "Middle East and North Africa", "East Asia", "South and South East Asia",
                             "Sub Saharan Africa")]
        x0, x1 = -4.2, 6.6
        y_top, dy = 2.35, 0.62

        def X(lg10):
            return x0 + (x1 - x0) * (lg10 - LO) / (HI - LO)

        lane_y = {r: y_top - k * dy for k, r in enumerate(lanes)}
        frame = VGroup()
        for r in lanes:
            y = lane_y[r]
            frame.add(Line([x0, y, 0], [x1, y, 0], color=GREY_D, stroke_width=1))
            frame.add(label(REGION_SHORT[r], font_size=18, color=REGION_COLOR[r]).next_to([x0, y, 0], LEFT, buff=0.2))
        for v in (500, 1000, 2000, 5000, 10000, 20000, 50000, 100000):
            x = X(np.log10(v))
            frame.add(Line([x, y_top + 0.35, 0], [x, lane_y[lanes[-1]] - 0.35, 0], color=GREY_D, stroke_width=0.6,
                           stroke_opacity=0.5))
            frame.add(MathTex(f"{v:,}".replace(",", "{,}"), font_size=18, color=GREY_B).move_to(
                [x, lane_y[lanes[-1]] - 0.62, 0]))
        axis_name = label(r"GDP per head, \ 2011 dollars, \ log scale", font_size=20, color=GREY_A).move_to(
            [(x0 + x1) / 2, lane_y[lanes[-1]] - 1.0, 0])
        rng = np.random.default_rng(1820)
        jitter = rng.uniform(-0.2, 0.2, len(regions))
        dots = VGroup(*[Circle(radius=0.05, stroke_width=0.6, stroke_color=BACKGROUND,
                               fill_color=REGION_COLOR.get(r, GREY_B), fill_opacity=0.85) for r in regions])
        year_t = Integer(1820, font_size=96, color=GREY_C, group_with_commas=False).move_to([4.6, 3.25, 0]).set_z_index(-2)
        world_line = Line([0, y_top + 0.4, 0], [0, lane_y[lanes[-1]] - 0.4, 0], color=WHITE, stroke_width=2.5)
        world_lab = label(r"the world", font_size=18, color=WHITE)
        tag = data_tag(r"Maddison Project Database 2023 (Bolt and van Zanden 2024); log-linear between benchmark "
                       r"years; dot size: population", font_size=15)
        stag = note(r"sound: the world's GDP per head, as a tune (computed)", font_size=15, color=E.ACCENT)
        stag.to_corner(DR, buff=0.3)
        t_end = film_time(2022)

        def year_of(t):
            return float(np.clip(1820 + (t - film_time(1820)) * (2022 - 1820) / (t_end - film_time(1820)), 1820,
                                 2022))

        def place(m, t):
            yr = year_of(t)
            i = int(np.clip(np.floor(yr - 1820), 0, len(years) - 2))
            w = yr - years[i]
            for k, dot in enumerate(m):
                g0, g1 = G[k, i], G[k, i + 1]
                if not np.isfinite(g0):
                    dot.set_opacity(0)
                    continue
                g = g0 if not np.isfinite(g1) else (1 - w) * g0 + w * g1
                lp = P[k, i] if np.isfinite(P[k, i]) else np.log(1000.0)
                r = 0.038 + 0.0062 * np.sqrt(np.exp(lp) / 1000.0)
                dot.set_width(2 * min(r, 0.42))
                dot.move_to([X(g / np.log(10)), lane_y[regions[k]] + jitter[k], 0])
                dot.set_fill(opacity=0.85)
                dot.set_stroke(opacity=1)

        def counter(m, t):
            m.set_value(int(year_of(t)))

        def world(m, t):
            yr = year_of(t)
            v = np.interp(yr, years, film["world"])
            m.set_x(X(np.log10(v)))

        def world_label(m, t):
            m.next_to(world_line, UP, buff=0.08)

        with self.listen(clip) as snd:
            snd.caption(r"the world's GDP per head, 1820 to 2022, as a tune")
            snd.show(tag, stag)
            snd.drive(dots, place)
            snd.drive(year_t, counter)
            snd.drive(world_line, world)
            snd.drive(world_lab, world_label)
            snd.show(dots, year_t, world_line, world_lab, frame, axis_name)
            # the lanes draw in while the film holds on 1820 (film_time(1820) = 1.5 s), so the picture moves from
            # the first note
            self.play(LaggedStart(*[Create(m) if isinstance(m, Line) else FadeIn(m) for m in frame], lag_ratio=0.02),
                      FadeIn(axis_name), run_time=1.4)
            snd.wait_until("film_end")
            self.play(*[FadeOut(m) for m in (frame, axis_name, tag, dots, world_line, world_lab, stag)],
                      year_t.animate.set_opacity(0.0), run_time=1.0)
            story = point_cards([
                (r"prices", r"found by people who see only their own card", E.DEMAND),
                (r"cost", r"what you give up; \ trade gains from comparative advantage", CRUSOE),
                (r"specialization", r"multiplies output, \ if there is a market to sell to", E.FIRMS),
                (r"messages", r"a price carries what nobody knows in full", TIN),
                (r"incentives", r"they work through what people take them to mean", FINE),
                (r"the escape", r"flat for millennia; \ about fifteen times richer since 1820", WHITE),
            ], width=12.6, cols=3, font_size=22).move_to(DOWN * 0.3)
            head = label(r"The story so far", font_size=40).to_edge(UP, buff=0.5)
            nxt = label(r"next: \ what a model is, \ when the order fails, \ and the economy as plumbing",
                        font_size=22, color=GREY_B).to_edge(DOWN, buff=0.4)
            # the cards arrive one by one over what is left of the tune, so the picture moves until the last note
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in story.cards], lag_ratio=0.6),
                      run_time=max(3.0, snd.remaining() - 1.6))
            self.play(FadeIn(nxt))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
