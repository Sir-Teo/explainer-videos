from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai25.common import (AUG, GNN_C, HIST, MESH_C, PAIR_C, PART, PLAIN, PRED_C, STRUCT, SYM, TRUE_C,
                                   field_image, framed, load, node_box, take_away)


class Weather(VoiceoverScene):
    def construct(self):
        self.card()
        self.history()
        self.graphcast()
        self.toy()
        self.skill()
        self.ensembles()

    def card(self):
        card = chapter_card(13, r"Weather on a mesh", r"Can a network learn the atmosphere?", lit=(1950,), part=PART)
        with self.voiceover("Chapter thirteen. Weather on a mesh."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def history(self):
        cards = VGroup(
            history_card(1904, r"Vilhelm Bjerknes", r"forecasting as physics: \ the state now, \ the equations, \ "
                         r"the state later", width=4.2, color=HIST),
            history_card(1922, r"Lewis Fry Richardson", r"a six-hour forecast by hand, \ for two points, \ over "
                         r"about six weeks: \ off by $145$\,hPa; \ he imagined $64{,}000$ people computing it in step",
                         width=4.2, color=HIST),
            history_card(1950, r"Charney, Fj\o rtoft \& von Neumann", r"forecasts on ENIAC: \ $24$ hours of "
                         r"weather in about $24$ hours of computing", width=4.2, color=HIST),
            history_card(1979, r"ECMWF", r"the first medium-range forecasts; \ since then skill has grown by about "
                         r"a day per decade", width=4.2, color=HIST),
        ).arrange_in_grid(rows=2, cols=2, buff=(0.35, 0.3)).move_to(DOWN * 0.2)
        head = label(r"Numerical weather prediction", font_size=34).to_edge(UP, buff=0.35)
        cite_ = cite(r"Lynch (2006); \ Bauer, Thorpe \& Brunet, \textit{Nature} (2015)", corner=DR)
        with self.voiceover(
            "Weather forecasting became physics in 1904, when Vilhelm Bjerknes described it as a problem of "
            "initial values: measure the atmosphere now, and step the equations of fluid flow forward. <bookmark "
            "mark='a'/> Lewis Fry Richardson tried it by hand during the First World War: a six-hour forecast for "
            "two points in Europe, worked out over some six weeks, and wrong by a hundred and forty-five "
            "hectopascals. He dreamed of a hall of sixty-four thousand people computing the weather in step. "
            "<bookmark mark='b'/> In 1950 Jule Charney, Ragnar Fjørtoft and John von Neumann ran the first forecasts "
            "on ENIAC: twenty-four hours of weather took about twenty-four hours to compute. <bookmark mark='c'/> "
            "The European Centre for Medium-Range Weather Forecasts issued its first forecasts in 1979, and in the "
            "decades since, better physics, better data and bigger computers have added about a day of useful "
            "forecast every ten years."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cards[0], shift=UP * 0.1), FadeIn(cite_))
            for k, mk in enumerate("abc", 1):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def graphcast(self):
        w = load("weather")
        pos = np.asarray(w["mesh_pos"])
        edges = np.asarray(w["mesh_edges"])
        S = 3.8 / (2 * np.pi)
        c = np.array([-3.6, -0.1, 0])
        to = lambda p: c + np.array([S * p[0] - 1.9, S * p[1] - 1.9, 0])  # noqa: E731
        grid = VGroup(*[Dot(to(np.array([i, j]) * 2 * np.pi / 32), radius=0.012, color=GREY_C)
                        for i in range(32) for j in range(32)])
        nodes = VGroup(*[Dot(to(p), radius=0.035, color=MESH_C) for p in pos])
        lev = {}
        for a, b in edges:
            pa, pb = pos[a], pos[b]
            d = np.abs((pb - pa + np.pi) % (2 * np.pi) - np.pi).max()
            if np.abs(pb - pa).max() > np.pi:  # wraps around: skip in the drawing
                continue
            L = 0 if d < 0.5 else (1 if d < 1.0 else 2)
            lev.setdefault(L, VGroup()).add(Line(to(pa), to(pb), stroke_width=[0.8, 1.4, 2.0][L],
                                                 color=[MESH_C, SYM, PAIR_C][L], stroke_opacity=[0.6, 0.7, 0.8][L]))
        ml = label(r"our mesh: \ $16 \times 16$ nodes, \ edges of three lengths", font_size=20, color=MESH_C)
        ml.next_to(grid, DOWN, buff=0.2)
        facts = VGroup(
            label(r"GraphCast \ (Lam et al., \textit{Science} 2023)", font_size=26, color=STRUCT),
            label(r"grid: \ $0.25^\circ$, \ $1{,}038{,}240$ points, \ $227$ numbers each", font_size=21),
            label(r"multimesh: \ an icosahedron refined six times, \ $40{,}962$ nodes, \ $327{,}660$ edges", font_size=21),
            label(r"encode to the mesh, \ $16$ rounds of message passing, \ decode", font_size=21),
            label(r"in: \ the last two states, \ $6$ hours apart; \ out: \ the next", font_size=21),
            label(r"$39$ years of ERA5 \ (1979--2017); \ four weeks on $32$ TPUs", font_size=21),
            label(r"a 10-day forecast in under a minute; \ better than ECMWF's HRES \ on $90\%$ of $1{,}380$ targets",
                  font_size=21, color=PAIR_C),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.1, 0.0, 0])
        if facts.width > 6.6:
            facts.width = 6.6
        facts.set_x(3.3)
        with self.voiceover(
            "Machine learning came to this in the 2020s, trained on ERA5, ECMWF's reconstruction of the global "
            "weather since 1940. In 2023 Remi Lam and colleagues at Google DeepMind published GraphCast. <bookmark "
            "mark='a'/> The atmosphere is stored on a latitude–longitude grid, a million points with two hundred "
            "and twenty-seven numbers each: wind, temperature, humidity and more, at thirty-seven heights. But such "
            "a grid crowds its points near the poles, so GraphCast works on a mesh instead: <bookmark mark='b'/> an "
            "icosahedron, refined six times, keeping the edges of every level, so that some edges are short and "
            "some span continents, and a message can cross the planet in a few steps. Here is our own small "
            "version, on a square. <bookmark mark='c'/> Encode the grid onto the mesh, pass messages sixteen times, "
            "decode back to the grid: the next state, six hours on, from the last two. <bookmark mark='d'/> Trained "
            "on thirty-nine years of ERA5 for four weeks on thirty-two TPUs, it makes a ten-day forecast in under a "
            "minute, and beat ECMWF's flagship deterministic forecast on ninety percent of 1,380 verification "
            "targets."
        ) as vo:
            self.play(FadeIn(facts[0]))
            vo.wait_until("a")
            self.play(FadeIn(grid), FadeIn(facts[1]))
            vo.wait_until("b")
            self.play(FadeIn(nodes), FadeIn(facts[2]))
            for L in sorted(lev):
                self.play(Create(lev[L], lag_ratio=0.002), run_time=1.0)
            self.play(FadeIn(ml))
            vo.wait_until("c")
            self.play(FadeIn(facts[3]), FadeIn(facts[4]))
            vo.wait_until("d")
            self.play(FadeIn(facts[5]), FadeIn(facts[6]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def toy(self):
        w = load("weather")
        truth = np.asarray(w["show_truth"])  # the truth at the predicted steps: 1, 5, 9, ... steps ahead
        mm = w["multimesh"]
        pred = np.asarray(mm["show"])  # every 4th predicted step from step 2
        vmax = float(np.abs(truth).max())
        leads = [1, 3, 5, 9]  # in units of 4 steps
        S = 2.0
        cols = Group()
        for j, L in enumerate(leads):
            t_img = framed(field_image(truth[L], S, vmax))
            p_img = framed(field_image(pred[L], S, vmax), color=STRUCT)
            ttl = label(rf"$+{4 * L + 1}$ steps", font_size=20, color=GREY_A)
            cols.add(Group(ttl, t_img, p_img).arrange(DOWN, buff=0.15))
        cols.arrange(RIGHT, buff=0.3).move_to([1.4, -0.2, 0])
        rl = VGroup(label(r"truth", font_size=22, color=TRUE_C), label(r"our mesh network", font_size=22,
                                                                         color=STRUCT))
        rl[0].next_to(cols[0][1], LEFT, buff=0.3)
        rl[1].next_to(cols[0][2], LEFT, buff=0.3)
        world = label(r"a toy atmosphere: \ swirling vorticity, \ stirred by a fixed pattern and damped",
                      font_size=22, color=GREY_A).to_edge(UP, buff=0.35)
        tag = note(rf"computed: \ $32 \times 32$ periodic grid, \ one step $= {w['dt']:.1f}$ time units; \ "
                   rf"${mm['params']:,}$ weights, \ trained on $32$ runs".replace(",", "{,}"), font_size=18)
        tag.to_corner(DR, buff=0.15)
        with self.voiceover(
            "Ours is a toy atmosphere: a two-dimensional fluid on a square that wraps around, stirred by a fixed "
            "pattern and damped by friction, so that eddies form, drift, merge and die. It is chaotic, like the "
            "weather. <bookmark mark='a'/> A small encode–process–decode network on the mesh we just saw learns "
            "one step at a time from thirty-two simulated runs, then rolls forward on its own, feeding each "
            "prediction back in. <bookmark mark='b'/> Top row, the truth; bottom row, our network, from the same "
            "start. For a while the two agree; then they drift apart."
        ) as vo:
            self.play(FadeIn(world), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rl), FadeIn(cols[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c_) for c_ in cols[1:]], lag_ratio=0.4), run_time=2.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def skill(self):
        w = load("weather")
        lead = int(w["lead"])
        t = np.arange(1, lead + 1)
        mm, fi = w["multimesh"], w["finest"]
        pers, clim = np.asarray(w["persistence"]), np.asarray(w["climatology"])
        rm, rf_ = np.asarray(mm["rmse"]), np.asarray(fi["rmse"])
        top = float(np.ceil(max(pers.max(), clim.max(), min(rm.max(), 2 * clim.max()), min(rf_.max(),
                                                                                         2 * clim.max())) + 0.5))
        g = axes([1, lead], [0, top], x_length=6.2, y_length=3.8, xlabel=r"steps ahead",
                 ylabel=r"error \ (root mean square)", xticks=[1, 10, 20, 30, 40], yticks=[0, top],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", center=[-2.3, -0.2, 0])
        clip = lambda y: np.minimum(y, top)  # noqa: E731
        cp = curve(g.ax, t, clip(pers), GREY_B, 3)
        cc = DashedLine(g.ax.c2p(1, clim.mean()), g.ax.c2p(lead, clim.mean()), color=GREY_C)
        cm = curve(g.ax, t, clip(rm), STRUCT, 3.5)
        cf = curve(g.ax, t, clip(rf_), PLAIN, 3)
        lg = legend([(STRUCT, r"mesh network, \ multimesh"), (PLAIN, r"the same, \ finest edges only"),
                     (GREY_B, r"persistence: \ nothing changes"), (GREY_C, r"climatology: \ the average state")],
                    font_size=20).move_to([4.4, 1.2, 0])
        beat_p = [k for k in range(lead) if rm[k] < pers[k]]
        hor = beat_p[-1] + 1 if beat_p and beat_p[0] == 0 else 0
        cross_c = next((k + 1 for k in range(lead) if rm[k] > clim.mean()), None)
        s1 = (f"One step ahead its error is {rm[0]:.2f}, against {pers[0]:.2f} for assuming nothing changes"
              if rm[0] < pers[0] else f"Even one step ahead it is no better than assuming nothing changes")
        s2 = (f"It stays ahead of persistence for {hor} steps" if hor >= 2 else "Its lead over persistence is short-lived")
        s3 = (f"and after {cross_c} steps it is worse than simply forecasting the average state, as every forecast of "
              "a chaotic system eventually is" if cross_c else "and it stays better than the average state throughout")
        mm_better = np.mean(rm[:10]) < np.mean(rf_[:10])
        s4 = ("The long edges matter: the same network with only the shortest edges does worse over the first ten "
              "steps" if mm_better else "In our toy the long edges don't help over the first ten steps")
        tag = note(r"computed: \ $8$ test runs, \ $40$ steps each", font_size=20).to_corner(DR, buff=0.2)
        with self.voiceover(
            "Scored over eight new runs: the error, step by step. <bookmark mark='a'/> " + s1 + ". <bookmark "
            "mark='b'/> " + s2 + ", " + s3 + ". <bookmark mark='c'/> " + s4 + ". GraphCast was trained on rollouts "
            "of up to twelve steps for exactly this reason: to learn from its own drifting predictions."
        ) as vo:
            self.play(FadeIn(g), FadeIn(tag), Create(cp), Create(cc), FadeIn(lg[2]), FadeIn(lg[3]))
            vo.wait_until("a")
            self.play(Create(cm), FadeIn(lg[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Indicate(lg[0]))
            vo.wait_until("c")
            self.play(Create(cf), FadeIn(lg[1]), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ensembles(self):
        blur = VGroup(
            label(r"trained on squared error, \ a forecast drifts toward the average of what might happen: \ blur",
                  font_size=22, color=GREY_A),
        ).to_edge(UP, buff=0.4)
        cards = VGroup(
            history_card(2024, r"GenCast \ (Price et al., \textit{Nature})", r"a diffusion model of the next state: \ "
                         r"$50$ or more samples, \ an ensemble; \ $0.25^\circ$, \ $15$ days; \ better than ECMWF's "
                         r"ensemble on $97.2\%$ of $1{,}320$ targets \ ($99.8\%$ beyond $36$ hours)", width=6.4,
                         color=HIST),
            history_card(2025, r"ECMWF's AIFS goes operational", r"AIFS Single on 25 February, \ AIFS ENS on 1 July: "
                         r"\ graph encoder and decoder, \ transformer processor; \ version 2 on 12 May 2026",
                         width=6.4, color=HIST),
            history_card(2025, r"and elsewhere", r"Google's WeatherNext 2 \ (November); \ NOAA's first AI global "
                         r"models \ (17 December)", width=6.4, color=HIST),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(blur, DOWN, buff=0.35)
        if cards.height > 5.4:
            cards.height = 5.4
        cards.set_x(0)
        cite_ = cite(r"Price et al.\ (2024); \ ECMWF (2025, 2026); \ NOAA (2025)", corner=DR)
        with self.voiceover(
            "There is a deeper problem. A network trained on squared error learns to predict the average of what "
            "might happen, and far ahead, the average of many possible weathers is a blur. <bookmark mark='a'/> "
            "Forecasters answer uncertainty with ensembles, many runs from slightly different starts. In 2024 "
            "Google DeepMind's GenCast learned to sample the next state with diffusion: fifty and more samples make "
            "an ensemble, and it beat ECMWF's own ensemble on 97.2 percent of 1,320 targets, 99.8 percent beyond a "
            "day and a half. <bookmark mark='b'/> Then the learned models went into daily service. On 25 February "
            "2025 ECMWF made its own Artificial Intelligence Forecasting System operational, a graph network "
            "encoder and decoder around a transformer, and its ensemble version that July; <bookmark mark='c'/> "
            "Google released WeatherNext 2 in November, and in December America's NOAA put its first AI global "
            "models into operation."
        ) as vo:
            self.play(FadeIn(blur), FadeIn(cite_))
            vo.wait_until("a")
            self.play(FadeIn(cards[0], shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(cards[2], shift=UP * 0.1))
        self.wait(0.6)
        tk = take_away(r"weather: \ a mesh, \ messages that cross the planet, \ and ensembles for what can't be "
                       r"known")
        with self.voiceover(
            "So the weather became a graph problem: a mesh that wraps the planet, messages that cross it in a few "
            "steps, and diffusion for the part of the future that can't be known. Next: networks that learn whole "
            "equations."
        ):
            self.play(FadeOut(cards), FadeIn(tk, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
