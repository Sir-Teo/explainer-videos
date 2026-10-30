from __future__ import annotations

import math

import numpy as np

from explainer import narration_credit
from explainer.ai import *  # noqa: F403
from videos.ai.ai29.common import AGENT, BELIEF, EXPERT, MODEL, PART, REWARD, WORLD, gray, load, node_box

BC, DAG = C.MODEL_Q, C.INTERVAL


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.payoffs()
        self.problems()
        self.next_time()
        self.references()

    # ------------------------------------------------------------------
    def tiles(self):
        """The part in ten pictures, each drawn from its own computed result."""
        TW, TH = 2.3, 1.55
        mk = lambda xr, yr: Axes(x_range=xr, y_range=yr, x_length=TW * 0.9, y_length=TH * 0.85, tips=False,  # noqa: E731
                                 axis_config={"stroke_color": GREY_D, "include_ticks": False})
        out = []
        b = load("belief")
        B = np.asarray(b["beliefs"])[-1]
        out.append((VGroup(*[Rectangle(width=0.045, height=max(1.4 * v / B.max(), 0.01), stroke_width=0,
                                       fill_color=BELIEF, fill_opacity=0.9) for v in B]).arrange(RIGHT, buff=0.008,
                                                                                               aligned_edge=DOWN),
                    r"a belief", BELIEF))
        a = load("agent")
        ns = np.asarray(a["ns"], float)
        ax = mk([0, 60, 1], [0, 1, 0.5])
        out.append((VGroup(ax, *[curve(ax, ns, np.asarray(a[f"{m}_succ"]), c, 3) for m, c in
                                 (("head", GREY_B), ("react", AGENT), ("check", REWARD))]), r"errors compound", AGENT))
        m = load("metr")
        ax = mk([0, 7.6, 1], [-5, 11, 1])
        out.append((VGroup(ax, *[Dot(ax.c2p(r["t"], math.log2(r["p50"])), radius=0.03, color=C.BITS if r["sota"] else GREY_C)
                                 for r in m["rows"]]), rf"doubling: \ ${float(m['doubling_2023']):.0f}$ days", C.BITS))
        L = load("lane")
        T = int(L["T"])
        ts = np.arange(1, T + 1)
        Jb, Jd = np.asarray(L["bc_J"]).mean(0), np.asarray(L["dagger_J"]).mean(0)
        ax = mk([0, T, 1], [0, float(max(Jb.max(), Jd.max())), 1])
        out.append((VGroup(ax, curve(ax, ts, Jb, BC, 3), curve(ax, ts, Jd, DAG, 3)), r"cloning vs DAgger", DAG))
        w = load("world")
        out.append((Group(*[gray(x, 0.42, MODEL) for x in np.asarray(w["imag"])[:10:2]]).arrange(RIGHT, buff=0.03),
                    r"a dreamed ball", MODEL))
        d = load("dreamer")
        Cd = np.asarray(d["curves"])
        ax = mk([0, float(Cd[0, -1, 1]), 1], [0, 1, 0.5])
        out.append((VGroup(ax, *[curve(ax, Cd[s, :, 1], Cd[s, :, 2], AGENT, 2.5) for s in range(len(Cd))]),
                    r"Dreamer-lite", AGENT))
        snap = d["snaps"][str(max(int(k) for k in d["snaps"]))]
        out.append((Group(*[gray(x, 0.42, MODEL) for x in np.asarray(snap["own"])[:10:2]]).arrange(RIGHT, buff=0.03),
                    r"its own dream", MODEL))
        r = load("randomize")
        mN, mR = np.asarray(r["nominal_map"]).mean(0), np.asarray(r["randomized_map"]).mean(0)

        def hm(M_):
            t = np.clip(M_ / 500, 0, 1)[::-1]
            lo, hi = np.array(ManimColor("#1A2130").to_rgb()), np.array(ManimColor(C.INTERVAL).to_rgb())
            rgb = lo[None, None] * (1 - t[..., None]) + hi[None, None] * t[..., None]
            im = ImageMobject((np.concatenate([rgb, np.ones(t.shape + (1,))], -1) * 255).astype(np.uint8))
            im.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
            return im.stretch_to_fit_width(1.0).stretch_to_fit_height(1.0)

        out.append((Group(hm(mN), hm(mR)).arrange(RIGHT, buff=0.15), r"randomize the sim", C.INTERVAL))
        dt = load("detour")
        last = str(max(int(k) for k in dt["flow_snaps"]))
        paths = VGroup(*[VMobject(stroke_color=DAG, stroke_width=1.5).set_points_as_corners(
            [[0.9 * x, 0.9 * y, 0] for x, y in p_]) for p_ in dt["flow_snaps"][last]["paths"]])
        paths.add(Circle(radius=0.9 * 0.32, stroke_width=0, fill_color=C.PENALTY, fill_opacity=0.5))
        out.append((paths, r"two ways round", DAG))
        f = load("fast")
        rows = f["rows"]
        ax = mk([0.7, 2.7, 1], [-3, -0.7, 1])
        out.append((VGroup(ax, curve(ax, [math.log10(x["tokens"]) for x in rows], [math.log10(x["rmse"]) for x in rows],
                                     C.BITS, 3), Dot(ax.c2p(math.log10(float(f["bin_tokens"])), math.log10(float(f["bin_rmse"]))),
                                                     radius=0.05, color=BC)), r"FAST tokens", C.BITS))
        tiles = Group()
        for pic, cap, col in out:
            box, c_ = tile_frame(cap, col, TW, TH)
            if c_.width > TW + 0.1:
                c_.width = TW + 0.1
            pic.move_to(box.get_center() + UP * 0.22)
            if pic.width > TW:
                pic.width = TW
            if pic.height > TH:
                pic.height = TH
            tiles.add(Group(box, pic, c_))
        tiles.arrange_in_grid(rows=2, cols=5, buff=(0.16, 0.3)).move_to(DOWN * 0.3)
        if tiles.width > 13.7:
            tiles.width = 13.7
        return tiles

    def recap(self):
        tiles = self.tiles()
        head = label(rf"Part {PART}, in ten pictures", font_size=40).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Let's take stock. An agent that cannot see everything acts on a belief, predicted and corrected by "
            "Bayes' rule. A language-model agent runs a loop of thoughts, actions and observations, with tools and "
            "memory around it. Over long tasks small errors compound, so reliability per step sets how far it can "
            "go, and on METR's measurements that reach has been doubling every few months. Copying an expert fails "
            "with the square of the horizon, and DAgger repairs it by learning where the learner actually goes. A "
            "world model lets an agent practise in its imagination, as our Dreamer did. And robots learn in "
            "randomized simulators and from demonstrations, with generative action experts and compressed action "
            "tokens."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t_, shift=UP * 0.15, scale=0.95) for t_ in tiles], lag_ratio=0.85),
                      run_time=max(4.0, vo.duration - 2.0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoffs(self):
        card = payoff_card([
            (r"is the written reasoning the real reasoning?", [30]),
            (r"world models inside networks, \ found by probes", [30]),
            (r"agent evaluations, \ reward hacking, \ control", [31]),
            (r"prompt injection, \ permissions, \ safeguards", [31]),
        ], font_size=26)
        with self.voiceover(
            "All of this comes back. Whether the reasoning an agent writes is really how it decides, and whether "
            "networks carry models of their world inside them, are questions for Part 30. And how to evaluate "
            "agents, keep them from gaming their rewards, and control what they can touch, is the subject of the "
            "last part."
        ) as vo:
            self.play(FadeIn(card.head))
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.1) for r_ in card.rows], lag_ratio=0.4),
                      run_time=max(3.0, vo.duration - 1.5))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def problems(self):
        ps = problem_set([
            r"A robot is at a door with prior probability $q$. \ It senses a door ($P = 0.9$ at one, \ $0.05$ elsewhere). "
            r"\ Find the posterior, \ and how many consistent sightings take $q = 0.1$ above $0.99$.",
            r"Show that $-\ln p \ge 1 - p$, \ so the half-time horizon $n_{1/2} = \ln 2 / (-\ln p)$ is at most "
            r"$0.69/(1-p)$. \ Compute it for $p = 0.98$.",
            r"Prove $J(\hat\pi) \le J(\pi^*) + T^2\varepsilon$ for behaviour cloning, \ and build a task where a single "
            r"mistake costs $1$ at every later step, \ so the bound is nearly reached.",
            r"If success on a task of length $t$ is $e^{-(t/\tau)^k}$, \ show $t_{50}/t_{80} = (\ln 2 / \ln 1.25)^{1/k}$, "
            r"\ and find the $k$ that gives METR's median ratio. \ What does $k < 1$ mean?",
            r"Show that $\operatorname{symlog}$ is odd, \ increasing, \ $\approx x$ near $0$, \ and that "
            r"$\operatorname{symexp}(y) = \operatorname{sign}(y)(e^{|y|} - 1)$ inverts it.",
            r"With $A^\tau = (1-\tau)\varepsilon + \tau A$, \ show $dA^\tau/d\tau = A - \varepsilon$. \ If demonstrations "
            r"are $\pm m$ with probability $\tfrac12$ each, \ show the squared-error-optimal deterministic action is $0$.",
            r"The orthonormal DCT is an orthogonal map. \ Show that rounding its coefficients, \ scaled by $\gamma$, \ "
            r"changes the signal by an RMS error of about $1/(\gamma\sqrt{12})$.",
        ], font_size=21)
        with self.voiceover(
            "Here are seven problems to try, from the belief update to the error of FAST's rounding. Pause here, and "
            "work through them; full solutions are in this part's notes."
        ) as vo:
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows], lag_ratio=0.3),
                      run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_time(self):
        head = label(r"Next: \ Part 30, \ Inside the Model", font_size=40).to_edge(UP, buff=0.5)
        ang = [PI / 2 + 2 * PI * k / 5 for k in range(5)]
        cols = [C.BITS, C.TRUE_P, C.INTERVAL, C.MODEL_Q, C.PENALTY]
        arrows = VGroup(*[Arrow(ORIGIN, 1.8 * np.array([np.cos(a), np.sin(a), 0]), buff=0, color=c, stroke_width=5)
                          for a, c in zip(ang, cols)]).move_to(DOWN * 0.4)
        circle = Circle(radius=1.8, color=GREY_D, stroke_width=1.5).move_to(arrows.get_center())
        l1 = label(r"five ideas \ in two dimensions", font_size=26, color=GREY_A).next_to(circle, RIGHT, buff=0.6)
        l2 = label(r"superposition, \ sparse autoencoders, \ circuits", font_size=26, color=C.BITS).next_to(l1, DOWN, buff=0.3)
        l2.align_to(l1, LEFT)
        tag = note(r"schematic").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Next time: inside the model. How a network stores more ideas than it has dimensions, "
            "<bookmark mark='a'/> how sparse autoencoders pull them apart, and how to trace a thought through its "
            "layers."
        ) as vo:
            self.play(FadeIn(head), Create(circle), LaggedStart(*[GrowArrow(a_) for a_ in arrows], lag_ratio=0.2),
                      FadeIn(tag), FadeIn(l1))
            vo.wait_until("a")
            self.play(FadeIn(l2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def references(self):
        card = reference_card(
            [r"S.~Thrun, W.~Burgard \& D.~Fox, \textit{Probabilistic Robotics} (2005)",
             r"R.~S.~Sutton \& A.~G.~Barto, \textit{Reinforcement Learning: An Introduction}, 2nd ed.\ (2018)"],
            [r"Nilsson (1984), \textit{Shakey the Robot}; \ Thrun et al., \textit{Stanley} (2006); \ Urmson et al., "
             r"\textit{Boss} (2008); \ \AA str\"om (1965); \ Kaelbling, Littman \& Cassandra (1998)",
             r"Yao et al., \textit{ReAct} (2022); \ Schick et al., \textit{Toolformer} (2023); \ Park et al.\ (2023); \ "
             r"Shinn et al., \textit{Reflexion} (2023); \ Wang et al., \textit{Voyager} (2023); \ Packer et al., "
             r"\textit{MemGPT} (2023); \ Anthropic, \textit{MCP} (2024) and multi-agent research (2025)",
             r"Kwa et al.\ (METR, 2025); \ METR, \textit{Time Horizon 1.1} (2026); \ Jimenez et al., \textit{SWE-bench} "
             r"(2024); \ Yang et al., \textit{SWE-agent} (2024); \ Deng et al., \textit{SWE-Bench Pro} (2025); \ Merrill "
             r"et al., \textit{Terminal-Bench} (2026); \ Xie et al., \textit{OSWorld} (2024), \textit{OSWorld 2.0} (2026)",
             r"Pomerleau, \textit{ALVINN} (1989); \ Ross \& Bagnell (2010); \ Ross, Gordon \& Bagnell, \textit{DAgger} "
             r"(2011); \ Kelly et al., \textit{HG-DAgger} (2019)",
             r"Sutton, \textit{Dyna} (1990); \ Ha \& Schmidhuber (2018); \ Hafner et al., \textit{PlaNet} (2019), "
             r"\textit{Dreamer} (2020), \textit{DreamerV2} (2021), \textit{DreamerV3} (2023/2025), \textit{Dreamer 4} "
             r"(2025); \ Bruce et al., \textit{Genie} (2024); \ Google DeepMind, \textit{Genie 2, 3, 4} (2024--26); \ "
             r"Assran et al., \textit{V-JEPA 2} (2025)",
             r"Tobin et al.\ (2017); \ Peng et al.\ (2018); \ OpenAI, \textit{Rubik's Cube} (2019); \ Makoviychuk et "
             r"al., \textit{Isaac Gym} (2021); \ Rudin et al.\ (2022)",
             r"Brohan et al., \textit{RT-1} (2022), \textit{RT-2} (2023); \ Open X-Embodiment (2023); \ Kim et al., "
             r"\textit{OpenVLA} (2024); \ Black et al., \textit{$\pi_0$} (2024); \ Pertsch et al., \textit{FAST} (2025); "
             r"\ Physical Intelligence, \textit{$\pi_{0.5}$} (2025), \textit{$\pi^*_{0.6}$} (2025), \textit{$\pi_{0.7}$} "
             r"(2026); \ Gemini Robotics Team (2025); \ NVIDIA, \textit{GR00T N1} (2025)"])
        credit = note(narration_credit(), font_size=18).to_edge(DOWN, buff=0.15)
        if card.get_bottom()[1] < credit.get_top()[1] + 0.1:
            card.shift(UP * (credit.get_top()[1] + 0.1 - card.get_bottom()[1]))
        with self.voiceover(
            "The best place to go deeper on the first half of this part is Thrun, Burgard and Fox's Probabilistic "
            "Robotics, and on learning to act, Sutton and Barto. Thanks for watching, and see you in Part 30."
        ):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(1.5)
        self.clear_scene()
