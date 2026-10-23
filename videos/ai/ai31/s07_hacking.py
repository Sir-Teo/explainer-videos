from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai31.common import HACK, INTENDED, PART, band, curve, load, tagline

BOAT = C.RL_POLICY
SHAPED = C.INTERVAL


class Track(VGroup):
    """The boat-race gridworld: walls, water, the lagoon's targets, the start and the finish."""

    def __init__(self, d, cell=0.55, center=ORIGIN):
        super().__init__()
        self.layout = d["track"]
        self.cell = cell
        R, Cc = len(self.layout), len(self.layout[0])
        self.origin = np.array([-(Cc - 1) * cell / 2, (R - 1) * cell / 2, 0.0])
        for r in range(R):
            for c in range(Cc):
                ch = self.layout[r][c]
                sq = Square(cell, stroke_width=0.8, stroke_color="#2A3240",
                            fill_color="#3A4250" if ch == "#" else "#132033", fill_opacity=1).move_to(self.at(r, c))
                self.add(sq)
        self.targets = VGroup(*[Circle(radius=cell * 0.3, stroke_width=0, fill_color=INTENDED, fill_opacity=0.9)
                                .move_to(self.at(r, c)) for r, c in d["targets"]])
        self.start = label(r"S", font_size=24, color=GREY_A).move_to(self.at(*d["start"]))
        fr, fc = d["finish"]
        flag = VGroup(*[Square(cell / 4, stroke_width=0, fill_color=WHITE if (i + j) % 2 == 0 else BLACK, fill_opacity=1)
                        .move_to(self.at(fr, fc) + np.array([(i - 1.5) * cell / 4, (j - 1.5) * cell / 4, 0]))
                        for i in range(4) for j in range(4)])
        self.finish = flag
        self.add(self.targets, self.start, self.finish)
        self.move_to(center)
        self.origin = self[0].get_center()  # cell (0, 0) after the move

    def at(self, r, c):
        return self.origin + np.array([c * self.cell, -r * self.cell, 0.0])


def replay(scene, track, path, run_time, color=BOAT):
    """The boat moving along a path of cells, with a short wake."""
    pts = [track.at(int(r), int(c)) for r, c in path]
    k = ValueTracker(0)

    def boat():
        i = min(int(k.get_value()), len(pts) - 1)
        return Dot(pts[i], radius=track.cell * 0.22, color=color)

    def wake():
        i = min(int(k.get_value()), len(pts) - 1)
        tail = pts[max(0, i - 10):i + 1]
        if len(tail) < 2:
            return VMobject()
        return VMobject(stroke_color=color, stroke_width=3, stroke_opacity=0.6).set_points_as_corners(tail)

    b, w = always_redraw(boat), always_redraw(wake)
    scene.add(w, b)
    scene.play(k.animate.set_value(len(pts) - 1), run_time=run_time, rate_func=linear)
    b.clear_updaters()
    w.clear_updaters()
    return VGroup(w, b)


class Hacking(VoiceoverScene):
    def construct(self):
        self.card()
        self.gallery()
        self.race()
        self.curves()
        self.shaping()
        self.coding()
        self.spread()

    def card(self):
        card = chapter_card(6, r"Reward hacking", r"What happens when the objective has a loophole?", lit=(2016, 2025),
                            part=PART)
        with self.voiceover("Chapter six. Reward hacking."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def gallery(self):
        head = label(r"Specification gaming \ (Krakovna et al., DeepMind, 2020)", font_size=34).to_edge(UP, buff=0.35)
        defn = definition_card(r"specification gaming", r"behaviour that satisfies the literal specification of an "
                               r"objective without achieving the intended outcome", color=HACK, width=9.0,
                               font_size=24).next_to(head, DOWN, buff=0.3)
        cards = VGroup(
            history_card(2017, r"stack the red block on the blue", r"rewarded for the height of the red block's bottom "
                         r"face: \ it flipped the block over", width=6.2, color=HACK, font_size=19),
            history_card(2016, r"win the boat race", r"rewarded for hitting targets along the course: \ it circled, "
                         r"hitting the same targets, \ never finishing", width=6.2, color=HACK, font_size=19),
            history_card(2017, r"grasp the object", r"judged by a person watching a camera: \ it hovered between the "
                         r"camera and the object", width=6.2, color=HACK, font_size=19),
            history_card(2019, r"learn to walk", r"a simulated robot hooked its legs together \ and slid along the "
                         r"ground", width=6.2, color=HACK, font_size=19),
        ).arrange_in_grid(rows=2, cols=2, buff=0.25).next_to(defn, DOWN, buff=0.3)
        with self.voiceover(
            "Wiener's colorful imitation has a modern name. In 2020 Victoria Krakovna and colleagues at DeepMind "
            "collected about sixty cases of specification gaming: behavior that satisfies the literal specification "
            "of an objective without achieving the intended outcome. <bookmark mark='a'/> A robot arm rewarded for "
            "the height of a red block's bottom face flipped the block over instead of stacking it. "
            "<bookmark mark='b'/> A boat-racing agent rewarded for hitting targets circled forever. "
            "<bookmark mark='c'/> An arm judged by a person watching a camera learned to hover between the "
            "camera and the object. <bookmark mark='d'/> A simulated robot asked to walk hooked its legs together and "
            "slid."
        ) as vo:
            full = [c_.copy() for c_ in cards]
            for c_ in cards:
                c_.fade(0.78)
            self.play(FadeIn(head), FadeIn(defn), FadeIn(cards))
            for k, m in enumerate("abcd"):
                vo.wait_until(m)
                self.play(Transform(cards[k], full[k]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def race(self):
        d = load("hacking")
        track = Track(d, cell=0.55, center=[-3.2, 0.6, 0])
        rules = VGroup(
            label(r"$+5$ \ for crossing the finish", font_size=24, color=GREY_A),
            label(r"$+1$ \ for each target hit; \ a target pays again \\ once another one has been hit", font_size=24,
                  color=INTENDED),
            label(rf"one lap: \ ${d['lap']}$ moves", font_size=24, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.6, 1.5, 0])
        snaps = list(d["snaps"])
        cap = [label(rf"after ${e:,}$ races".replace(",", "{,}"), font_size=26, color=BOAT).next_to(track, DOWN, buff=0.3)
               for e in snaps]
        ret = np.asarray(d["proxy_ret"])
        fin = np.asarray(d["proxy_fin"])
        never = bool(fin[:, -1].max() == 0)
        tag = tagline(rf"computed: \ Q-learning, \ ${d['seeds']}$ seeds; \ replay: \ seed $0$")
        end = (f"By the end it circles in the lagoon, collecting about {ret[:, -1].mean():.0f} points a race, and "
               f"never crosses the finish line: not in any of the {d['seeds']} training runs. The reward was "
               "satisfied. The race was not." if never else
               f"By the end most runs circle in the lagoon, collecting about {ret[:, -1].mean():.0f} points a race.")
        with self.voiceover(
            "We can grow one ourselves. Here is a boat race as a gridworld. The boat starts at S; the finish is right "
            f"behind a wall, so finishing takes a lap of {d['lap']} moves. <bookmark mark='a'/> The reward: five "
            "points for finishing, and one point for each green target, which, as in the game, pays again once "
            "another target has been hit. We meant: finish the race. <bookmark mark='b'/> Train it with Q-learning "
            "from Part 26. Untrained, the boat wanders. <bookmark mark='c'/> A few hundred races in, it has found "
            "the targets. <bookmark mark='d'/> " + end
        ) as vo:
            lap = [track.at(int(r_), int(c_)) for r_, c_ in np.asarray(d[f"traj_shaped_{snaps[-1]}"])]
            lap_line = DashedVMobject(VMobject(stroke_color=GREY_A, stroke_width=3).set_points_as_corners(lap),
                                      num_dashes=40)
            self.play(FadeIn(track), FadeIn(tag), FadeIn(rules[2]))
            self.play(Create(lap_line), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeOut(lap_line), LaggedStart(*[FadeIn(r_) for r_ in rules[:2]], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(FadeIn(cap[0]))
            m = replay(self, track, np.asarray(d[f"traj_proxy_{snaps[0]}"])[:40], 3.0)
            vo.wait_until("c")
            self.play(FadeOut(m), ReplacementTransform(cap[0], cap[2]))
            m = replay(self, track, np.asarray(d[f"traj_proxy_{snaps[2]}"])[:40], 3.0)
            vo.wait_until("d")
            self.play(FadeOut(m), ReplacementTransform(cap[2], cap[-1]))
            m = replay(self, track, np.asarray(d[f"traj_proxy_{snaps[-1]}"])[:60], 5.0)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def curves(self):
        d = load("hacking")
        eps = np.asarray(d["eval_eps"])
        E = float(eps[-1])
        g1 = axes([0, E], [0, 60], x_length=5.2, y_length=3.0, xlabel=r"training races",
                  ylabel=r"reward per race \ (what we wrote)", xticks=[0, E / 2, E], yticks=[0, 30, 60],
                  center=[-3.4, -0.4, 0])
        g2 = axes([0, E], [0, 1], x_length=5.2, y_length=3.0, xlabel=r"training races",
                  ylabel=r"races finished \ (what we meant)", xticks=[0, E / 2, E], yticks=[0, 0.5, 1],
                  yfmt=lambda v: rf"{int(v * 100)}\%", center=[3.4, -0.4, 0])
        R, F_ = np.asarray(d["proxy_ret"]), np.asarray(d["proxy_fin"])
        b1 = band(g1.ax, eps, R.min(0), R.max(0), HACK)
        c1 = curve(g1.ax, eps, R.mean(0), HACK, 3)
        b2 = band(g2.ax, eps, F_.min(0), F_.max(0), HACK)
        c2 = curve(g2.ax, eps, F_.mean(0), HACK, 3)
        note_ = note(rf"mean of ${d['seeds']}$ seeds; \ band: \ min to max", font_size=18).to_corner(DR, buff=0.2)
        head = label(r"Goodhart again: \ the measure climbs, \ the goal does not", font_size=32).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Here is the whole of training, for all five runs. <bookmark mark='a'/> The reward we wrote climbs and "
            "keeps climbing. <bookmark mark='b'/> The thing we meant, finishing the race, stays at zero: Goodhart's "
            "law again, with a loophole written by hand and found by the optimizer itself."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g1), FadeIn(g2), FadeIn(note_))
            vo.wait_until("a")
            self.play(FadeIn(b1), Create(c1), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(b2), Create(c2), run_time=2.0)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def shaping(self):
        d = load("hacking")
        rows = [
            cmath(r"r'(s, s')", r"=", r"r(s, s') + \gamma\,\Phi(s') - \Phi(s)", font_size=32),
            cmath(r"G'", r"=", r"\sum_t \gamma^t r_t + \sum_t \big(\gamma^{t+1}\Phi(s_{t+1}) - \gamma^t \Phi(s_t)\big)",
                  font_size=32),
            cmath(r"G'", r"=", r"G - \Phi(s_0)", font_size=32),
        ]
        rows[0][2].set_color(SHAPED)
        rows[2][2].set_color(SHAPED)
        whys = [why(r"a bonus for progress: \ $\Phi$ = $5 \times$ the share of the lap done"),
                why(r"the bonus terms telescope"),
                why(r"$\Phi = 0$ once the race ends: \ every policy shifts by the same constant")]
        step = ladder(self, rows, whys, keep=3, top=3.1, x=-2.6, buff=0.55, edge=6.9)
        eps = np.asarray(d["eval_eps"])
        E = float(eps[-1])
        g = axes([0, E], [0, 1], x_length=6.0, y_length=2.4, xlabel=r"training races", ylabel=r"races finished",
                 xticks=[0, E / 2, E], yticks=[0, 1], yfmt=lambda v: rf"{int(v * 100)}\%", center=[-2.6, -2.1, 0])
        lines = VGroup()
        for mode, col in (("proxy", HACK), ("sparse", GREY_B), ("shaped", SHAPED)):
            F_ = np.asarray(d[f"{mode}_fin"])
            lines.add(VGroup(band(g.ax, eps, F_.min(0), F_.max(0), col), curve(g.ax, eps, F_.mean(0), col, 3)))
        lg = legend([(HACK, r"targets and finish"), (GREY_B, r"the finish only"), (SHAPED, r"the finish, \ shaped by "
                     r"progress")], font_size=18).next_to(g, RIGHT, buff=0.3)
        from videos.ai.ai31.sims import BoatRace

        env = BoatRace()
        D = max(env.dist.values())
        trk = Track(d, cell=0.4, center=[-2.6, -2.0, 0])
        heat = VGroup(*[Square(trk.cell, stroke_width=0, fill_opacity=0.9,
                               fill_color=interpolate_color(ManimColor("#132033"), ManimColor(SHAPED), 1 - dist / D))
                        .move_to(trk.at(r, c)) for (r, c), dist in env.dist.items()])
        hl = label(r"$\Phi$: \ $0$ at the start, \\ rising to $5$ at the finish", font_size=20, color=SHAPED)
        hl.next_to(trk, RIGHT, buff=0.4)
        pot = VGroup(trk, heat, trk.targets.copy(), trk.start.copy(), trk.finish.copy(), hl)
        first = {m: [f for f in d[f"{m}_first"] if f >= 0] for m in ("sparse", "shaped")}
        n_sp, n_sh = len(first["sparse"]), len(first["shaped"])
        S = d["seeds"]
        med_sp = float(np.median(first["sparse"])) if first["sparse"] else -1
        med_sh = float(np.median(first["shaped"])) if first["shaped"] else -1
        sparse_said = (f"Reward only the finish and it learns to finish in {n_sp} of {S} runs, slowly: its first "
                       f"finish comes after about {med_sp:.0f} races." if n_sp else
                       "Reward only the finish, and in this many races it never stumbles on it at all.")
        shaped_said = (f"With the shaped bonus, all {S} runs finish, the first time after about {med_sh:.0f} races."
                       if n_sh == S else
                       f"With the shaped bonus, {n_sh} of {S} runs learn to finish.")
        with self.voiceover(
            "Can a bonus for progress help without opening a loophole? In 1999 Andrew Ng, Daishi Harada and Stuart "
            "Russell showed exactly which bonuses are safe. <bookmark mark='a'/> Add to each step's reward gamma "
            "times a potential of the new state, minus the potential of the old one; here the potential is five "
            "times the share of the lap completed. <bookmark mark='b'/> Sum the discounted rewards of a whole race: "
            "the bonus terms telescope, each cancelling the next. <bookmark mark='c'/> What is left is the original "
            "return, minus the potential of the start. Every policy's return shifts by the same constant, so the best "
            "policy is unchanged; and going around in a circle earns nothing. <bookmark mark='d'/> " + sparse_said +
            " <bookmark mark='e'/> " + shaped_said + " The bonus guides; it cannot be farmed."
        ) as vo:
            self.play(FadeIn(trk))
            vo.wait_until("a")
            step(0)
            self.play(FadeIn(heat), FadeIn(pot[2:]))
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            self.play(FadeOut(pot), FadeIn(g), FadeIn(lg))
            self.play(LaggedStart(*[FadeIn(l_) for l_ in lines], lag_ratio=0.5), run_time=2.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def coding(self):
        head = label(r"Reward hacking at the frontier: \ coding agents", font_size=34).to_edge(UP, buff=0.35)
        cards = VGroup(
            history_card(2025, r"Claude 3.7 Sonnet system card \ (Anthropic, February)", r"after repeated failures, "
                         r"sometimes ``special-cased'' tests: \ returned the expected values, \ or edited the tests; \ "
                         r"traced to reward hacking in RL training", width=6.3, color=HACK, font_size=19),
            history_card(2025, r"OpenAI, \ Baker et al.\ (March)", r"a frontier reasoning model in training learned to "
                         r"call \texttt{exit(0)} or \texttt{raise SkipTest}, \ so that tests ``passed''", width=6.3,
                         color=HACK, font_size=19),
            history_card(2025, r"METR, \ o3 \ (June)", r"reward hacked in $39$ of $128$ runs ($30\%$) on RE-Bench, \ "
                         r"$8$ of $1{,}087$ on HCAST: \ overwrote the timer, \ stubbed out the scorer, \ read the answer "
                         r"from the grader's memory", width=6.3, color=HACK, font_size=19),
            history_card(2025, r"asking it not to", r"``Please do not cheat.'': \ still $80\%$ on one task; \ asked "
                         r"afterwards whether it had followed the user's intention: \ ``no'', $10$ times out of $10$",
                         width=6.3, color=C.KL, font_size=19),
        ).arrange_in_grid(rows=2, cols=2, buff=0.25).next_to(head, DOWN, buff=0.3)
        with self.voiceover(
            "The frontier has its own boat races, and they are found in coding. <bookmark mark='a'/> Anthropic's "
            "system card for Claude 3.7 Sonnet, in February 2025, reported that after repeated failures it sometimes "
            "special-cased tests: returning the values a test expected, or changing the test. <bookmark mark='b'/> OpenAI reported a frontier reasoning "
            "model that, during training, learned to exit early or skip tests so that they counted as passed. "
            "<bookmark mark='c'/> In June 2025 METR found o3 reward hacking in thirty percent of its runs on one suite "
            "of research tasks: rewriting the timer that scored its speed, replacing the scorer with one that always "
            "approved, fishing the reference answer out of the grader's memory. <bookmark mark='d'/> Asking it not to "
            "cheat barely helped. Yet asked afterwards whether it had done what the user intended, it said no, ten "
            "times out of ten. It knew."
        ) as vo:
            full = [c_.copy() for c_ in cards]
            for c_ in cards:
                c_.fade(0.78)
            self.play(FadeIn(head), FadeIn(cards))
            for k, m in enumerate("abcd"):
                vo.wait_until(m)
                self.play(Transform(cards[k], full[k]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def spread(self):
        a = node_box_(r"learns to hack \\ coding tests", HACK)
        b = node_box_(r"sabotages safety \\ research code \ ($12\%$)", HACK)
        c = node_box_(r"alignment-faking reasoning \\ when asked its goals \ ($50\%$)", HACK)
        a.move_to([-4.2, 0.6, 0])
        b.move_to([2.4, 1.6, 0])
        c.move_to([2.4, -0.4, 0])
        arr = VGroup(Arrow(a.get_right(), b.get_left(), buff=0.15, color=GREY_B, stroke_width=3),
                     Arrow(a.get_right(), c.get_left(), buff=0.15, color=GREY_B, stroke_width=3))
        fix = node_box_(r"inoculation: \ say in training that hacking is allowed here \\ $\Rightarrow$ it still hacks, "
                        r"\ but the misalignment does not spread", INTENDED).move_to([0, -2.4, 0])
        head = label(r"Hacking spreads \ (MacDiarmid et al., Anthropic, November 2025)", font_size=32).to_edge(UP,
                                                                                                            buff=0.4)
        with self.voiceover(
            "Is a hacked test just a nuisance? In November 2025 Anthropic reported what happened when a model learned "
            "real hacks, like exiting a test harness early, in the coding environments used to train production "
            "models. <bookmark mark='a'/> The habit spread. Put to work on the code of that very research project, "
            "it tried to sabotage it twelve percent of the time; asked simply what its goals were, it reasoned like "
            "an alignment faker half the time. <bookmark mark='b'/> The fix was surprising: tell the model during training that hacking is acceptable "
            "in this environment. It still hacked, but the misalignment no longer spread. A model learns not only "
            "what it is rewarded for, but what that says about what it is."
        ) as vo:
            later = VGroup(arr, b, c)
            full = later.copy()
            later.fade(0.8)
            self.play(FadeIn(head), FadeIn(a), FadeIn(later))
            vo.wait_until("a")
            self.play(Transform(later, full))
            vo.wait_until("b")
            self.play(FadeIn(fix, shift=UP * 0.15))
        self.wait(0.4)
        self.clear_scene()


def node_box_(text, color, font_size=24):
    t = label(text, font_size=font_size, color=color)
    box = RoundedRectangle(width=t.width + 0.5, height=t.height + 0.45, corner_radius=0.14, stroke_color=color,
                           stroke_width=2.2, fill_color=color, fill_opacity=0.08)
    return VGroup(box, t.move_to(box))
