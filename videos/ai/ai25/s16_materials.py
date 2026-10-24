from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai25.common import (HIST, MSA_C, PAIR_C, PART, PLAIN, PRED_C, SEARCH_C, STRUCT, SYM, TRUE_C, load,
                                   node_box, take_away, takeaway_anims, words_num)

STABLE = MSA_C


class Materials(VoiceoverScene):
    def construct(self):
        self.card()
        self.hull()
        self.gnome()
        self.flywheel()
        self.debate()

    def card(self):
        card = chapter_card(15, r"Materials by the million", r"Can a network find crystals no one has made?", lit=(),
                            part=PART)
        with self.voiceover("Chapter fifteen. Materials by the million."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def hull(self):
        m = load("materials")
        x = np.asarray(m["sys_x"])
        E = np.asarray(m["sys_E"])
        st = np.asarray(m["sys_stable"]).astype(bool)
        H = np.asarray(m["sys_hull"])
        lo = float(np.floor(min(E.min(), H[:, 1].min()) * 4) / 4 - 0.1)
        hi = float(np.ceil(max(E.max(), 0.1) * 4) / 4)
        g = axes([0, 1], [lo, hi], x_length=6.0, y_length=4.0, xlabel=r"composition: \ share of element B",
                 ylabel=r"formation energy per atom", xticks=[0, 0.5, 1], yticks=[lo, 0, hi],
                 xfmt=lambda v: {0: r"\text{A}", 0.5: r"\text{AB}", 1: r"\text{B}"}[v], yfmt=lambda v: f"{v:.2f}",
                 center=[-2.6, -0.2, 0])
        zero = DashedLine(g.ax.c2p(0, 0), g.ax.c2p(1, 0), color=GREY_D)
        pts = VGroup(*[Dot(g.ax.c2p(a, b), radius=0.06, color=STABLE if s else GREY_B) for a, b, s in zip(x, E, st)])
        hull = VMobject(stroke_color=PAIR_C, stroke_width=3.5).set_points_as_corners([g.ax.c2p(a, b) for a, b in H])
        # one unstable compound and its distance above the hull
        k = int(np.argmax(np.where(~st, -np.abs(E - np.interp(x, H[:, 0], H[:, 1]) - 0.15), -9)))
        hx, hy = x[k], float(np.interp(x[k], H[:, 0], H[:, 1]))
        br = Line(g.ax.c2p(hx, hy), g.ax.c2p(hx, E[k]), color=PLAIN, stroke_width=3)
        brl = label(r"energy above the hull", font_size=18, color=PLAIN).next_to(br, RIGHT, buff=0.1)
        d = definition_card(r"stable", r"on the lower convex hull of all compounds of the same elements: \ no mix of "
                            r"other compounds has lower energy, \ so it won't decompose", width=5.6, font_size=21)
        d.move_to([3.9, 1.5, 0])
        facts = VGroup(
            label(r"$230$ space groups: \ the symmetries a crystal can have \ (Fedorov, Schoenflies, 1891)",
                  font_size=20, color=SYM),
            label(r"energies from density functional theory \ (Kohn \& Sham, 1965): \ hours of computing each",
                  font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.9, -1.3, 0])
        for f_ in facts:
            if f_.width > 5.8:
                f_.width = 5.8
        tag = note(r"illustrative: \ one binary system of this chapter's made-up chemistry", font_size=18)
        tag.to_corner(DR, buff=0.2)
        n_st = int(st.sum())
        with self.voiceover(
            "A crystal is a pattern of atoms repeated in space, and its symmetries are one of 230 space groups, "
            "classified in 1891. Which crystals exist? <bookmark mark='a'/> Take two elements, A and B, and all "
            "their possible compounds, each with an energy of formation, computed by density functional theory "
            "at hours of computer time apiece. <bookmark mark='b'/> A compound is stable if no mixture of the "
            "others has lower energy: if it lies on the lower convex hull of the points. <bookmark mark='c'/> One "
            "above the hull would rather decompose into its neighbours, and how far above it lies says how "
            f"unstable it is. In this system, {words_num(n_st)} compounds are on the hull."
        ) as vo:
            self.play(FadeIn(g), Create(zero), FadeIn(facts[0]), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p_, scale=1.5) for p_ in pts], lag_ratio=0.02), FadeIn(facts[1]),
                      run_time=1.5)
            vo.wait_until("b")
            self.play(Create(hull), FadeIn(d))
            vo.wait_until("c")
            self.play(Create(br), FadeIn(brl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def gnome(self):
        steps = [(r"candidates: \\ substitutions, \\ random structures", GREY_A),
                 (r"graph networks \\ predict the energy", STRUCT), (r"DFT checks \\ the most promising", PAIR_C),
                 (r"the results \\ train the networks", SEARCH_C)]
        boxes = VGroup(*[node_box(t, c, font_size=22, height=1.2) for t, c in steps])
        pos = [[-4.6, 1.6, 0], [-0.8, 1.6, 0], [-0.8, -0.6, 0], [-4.6, -0.6, 0]]
        for b_, p_ in zip(boxes, pos):
            b_.move_to(p_)
        arr = VGroup(Arrow(boxes[0].get_right(), boxes[1].get_left(), buff=0.08, color=GREY_B, stroke_width=2.5),
                     Arrow(boxes[1].get_bottom(), boxes[2].get_top(), buff=0.08, color=GREY_B, stroke_width=2.5),
                     Arrow(boxes[2].get_left(), boxes[3].get_right(), buff=0.08, color=GREY_B, stroke_width=2.5),
                     Arrow(boxes[3].get_top(), boxes[0].get_bottom(), buff=0.08, color=GREY_B, stroke_width=2.5))
        nums = VGroup(
            label(r"GNoME \ (Merchant et al., \textit{Nature} 2023)", font_size=24, color=STRUCT),
            label(r"before: \ about $48{,}000$ stable crystals known from computation", font_size=21, color=GREY_A),
            label(r"found: \ $2.2$ million stable against what was known; \ $381{,}000$ on the new hull", font_size=21,
                  color=STABLE),
            label(r"hit rate: \ above $80\%$ with structures, \ $33\%$ from compositions alone, \ against about "
                  r"$1\%$ before", font_size=21, color=PAIR_C),
            label(r"$736$ already made, \ independently, \ by other labs", font_size=21, color=HIST),
            label(r"the networks' error falls as a power law in the data", font_size=21, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.6, 0.2, 0])
        if nums.width > 6.4:
            nums.width = 6.4
        nums.set_x(3.75)
        cite_ = cite(r"Merchant et al.\ (2023); \ Google DeepMind (29 November 2023)", corner=DR)
        with self.voiceover(
            "In 2023 Amil Merchant, Ekin Dogus Cubuk and colleagues at Google DeepMind published GNoME, graph "
            "networks for materials exploration. <bookmark mark='a'/> It generates candidate crystals by swapping "
            "elements in known ones and by random search; <bookmark mark='b'/> graph networks, built on distances "
            "between atoms and so invariant to how the crystal is turned, predict each candidate's energy; "
            "<bookmark mark='c'/> density functional theory checks the most promising; <bookmark mark='d'/> and "
            "every check becomes training data for the next round. <bookmark mark='e'/> Before, computation had "
            "found about forty-eight thousand stable crystals. GNoME reported 2.2 million stable against everything "
            "known, 381,000 of them on the new convex hull. The fraction of its picks that DFT confirmed rose above "
            "eighty percent, from around one percent in earlier work, and 736 of its predictions had already been "
            "made independently by other laboratories."
        ) as vo:
            self.play(FadeIn(boxes[0]), FadeIn(nums[0]), FadeIn(cite_))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                if k < 3:
                    self.play(GrowArrow(arr[k]), FadeIn(boxes[k + 1]))
                else:
                    self.play(GrowArrow(arr[3]))
            vo.wait_until("e")
            self.play(LaggedStart(*[FadeIn(n_) for n_ in nums[1:]], lag_ratio=0.6), run_time=6.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def flywheel(self):
        m = load("materials")
        rounds = len(m["model_s0"])
        r_ = np.arange(1, rounds + 1)
        H = {p: np.array([[h["hit_rate"] for h in m[f"{p}_s{s}"]] for s in (0, 1, 2)]) for p in ("model", "random")}
        MAE = np.array([[h["mae"] for h in m[f"model_s{s}"]] for s in (0, 1, 2)])
        F = {p: np.array([[h["found"] for h in m[f"{p}_s{s}"]] for s in (0, 1, 2)]) for p in ("model", "random")}
        g = axes([1, rounds], [0, 1], x_length=5.2, y_length=3.4, xlabel=r"round", ylabel=r"hit rate: \ picks truly "
                 r"stable", xticks=list(r_), yticks=[0, 0.5, 1.0], xfmt=lambda v: f"{v:.0f}", center=[-3.2, 0.2, 0])
        objs = {}
        for p, col in (("model", STRUCT), ("random", GREY_B)):
            A = H[p]
            objs[p] = VGroup(band(g.ax, r_, A.min(0), A.max(0), col, 0.22), curve(g.ax, r_, A.mean(0), col, 3.5),
                             VGroup(*[Dot(g.ax.c2p(a, b), radius=0.05, color=col) for a, b in zip(r_, A.mean(0))]))
        lg = legend([(STRUCT, r"the surrogate's picks"), (GREY_B, r"random picks")], font_size=20)
        lg.next_to(g, DOWN, buff=0.25).align_to(g.ax, LEFT)
        mae = MAE.mean(0)
        stats = VGroup(
            label(rf"$6{{,}}840$ candidates, \ ${m['n_stable']}$ truly stable", font_size=22, color=GREY_A),
            label(rf"each round: \ $60$ `DFT' checks", font_size=22, color=GREY_A),
            label(rf"surrogate error: \ ${mae[0]:.3f}$ \ $\to$ \ ${mae[-1]:.3f}$", font_size=22, color=STRUCT),
            label(rf"stable found after {rounds} rounds: \ ${F['model'][:, -1].mean():.0f}$ \ vs \ "
                  rf"${F['random'][:, -1].mean():.0f}$ at random", font_size=22, color=STABLE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([3.5, 0.6, 0])
        h_m, h_r = H["model"].mean(0), H["random"].mean(0)
        share = m["n_stable"] / m["n_candidates"]
        hm0, hm1, hmax = 100 * h_m[0], 100 * h_m[-1], 100 * h_m.max()
        if h_m[-1] > h_m[0] + 0.05:
            trend = (f"and it climbs as the surrogate learns, from {hm0:.0f} percent in the first round to {hm1:.0f} in "
                     "the last")
        elif h_m[-1] < h_m.max() - 0.05 and int(np.argmax(h_m)) > 0:
            trend = (f"rise to {hmax:.0f}, and then fall, to {hm1:.0f} in the last round, as the easiest stable "
                     "compounds are used up; still several times the random rate")
        elif h_m[-1] < h_m.max() - 0.05:
            trend = (f"and then fall, to {hm1:.0f} in the last round, as the easiest stable compounds are used up; "
                     "still several times the random rate")
        else:
            trend = f"and it stays around {100 * h_m.mean():.0f} percent: in our toy the surrogate is good from the start"
        tag = note(r"computed: \ a made-up chemistry, \ three seeds \ (band: \ min--max)", font_size=20)
        tag.to_corner(DR, buff=0.2)
        with self.voiceover(
            "We can run the flywheel on a made-up chemistry: twenty invented elements, every pair of them, nine "
            f"compositions and four crystal types, {m['n_candidates']:,} candidates, whose 'DFT' energy is a hidden "
            "formula we only reveal sixty at a time. <bookmark mark='a'/> Start knowing three percent of them. Each "
            "round, train a small ensemble on everything known, predict the rest, and check the sixty that look most "
            "stable: those predicted to fall furthest below the hull of everything else, known or predicted. A hit "
            "is a pick that is truly stable, on the hull of the full chemistry. <bookmark mark='b'/> Random picks "
            f"hit {100 * h_r.mean():.0f} percent of the time, about the share of stable compounds among the "
            f"candidates, {100 * share:.0f} percent. <bookmark "
            f"mark='c'/> The surrogate's picks hit {100 * h_m[0]:.0f} percent in the first round, {trend}. "
            f"<bookmark mark='d'/> Its error falls from {mae[0]:.3f} to {mae[-1]:.3f}, and after {rounds} rounds it "
            f"has found {F['model'][:, -1].mean():.0f} of the {m['n_stable']} truly stable compounds, against "
            f"{F['random'][:, -1].mean():.0f} for random picks."
        ) as vo:
            self.play(FadeIn(g), FadeIn(stats[0]), FadeIn(stats[1]), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(lg))
            vo.wait_until("b")
            self.play(FadeIn(objs["random"]))
            vo.wait_until("c")
            self.play(FadeIn(objs["model"]))
            vo.wait_until("d")
            self.play(FadeIn(stats[2]), FadeIn(stats[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def debate(self):
        cards = VGroup(
            history_card(2024, r"Cheetham \& Seshadri", r"a random sample of GNoME's list: \ scant evidence of "
                         r"compounds that are at once new, credible and useful; \ many order atoms that real crystals "
                         r"mix", width=6.2, color=PLAIN),
            history_card(2023, r"the A-Lab \ (Szymanski et al.)", r"a robot lab reported $41$ new compounds from $58$ "
                         r"targets in $17$ days; \ critics (Leeman et al.\ 2024) disputed the X-ray analysis; \ a 2026 "
                         r"correction: \ $36$ compounds of $57$", width=6.2, color=PLAIN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([-3.4, 0.0, 0])
        if cards.height > 6.4:
            cards.height = 6.4
        cards.set_x(-3.2)
        after = VGroup(
            label(r"since: \ universal learned potentials \ (MACE-MP-0, \ 2023)", font_size=22, color=STRUCT),
            label(r"generative design: \ MatterGen \ (\textit{Nature} 2025)", font_size=22, color=STRUCT),
            label(r"the lesson: \ a prediction is a hypothesis; \ the synthesis is the test", font_size=24,
                  color=PAIR_C),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.6, 0.0, 0])
        for a_ in after:
            if a_.width > 5.8:
                a_.width = 5.8
        head = label(r"the pushback", font_size=34, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The claims drew pushback from chemists. <bookmark mark='a'/> In 2024 Anthony Cheetham and Ram Seshadri "
            "examined a random sample of GNoME's predictions and found scant evidence of compounds that were at "
            "once new, credible and useful; many placed atoms in neat orders that real crystals mix at random, and "
            "they argued these were crystalline compounds, not yet materials. <bookmark mark='b'/> The same year, "
            "critics disputed the X-ray analysis behind a robot laboratory's report of forty-one new compounds; in "
            "January 2026 the paper was corrected to thirty-six compounds from fifty-seven targets. <bookmark "
            "mark='c'/> The tools kept improving, universal learned potentials for any element, generative models "
            "that propose crystals with chosen properties, <bookmark mark='d'/> but the lesson stuck: a predicted "
            "crystal is a hypothesis, and making it is the test."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(cards[0], shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(after[0]), FadeIn(after[1]))
            vo.wait_until("d")
            self.play(FadeIn(after[2]))
        self.wait(0.6)
        tk = take_away(r"materials: \ an invariant network as a cheap first opinion, \ DFT and the lab as the judge")
        with self.voiceover(
            "In materials, then, the network is a cheap first opinion that makes expensive checks count. In "
            "mathematics, the check can be perfect."
        ):
            self.play(FadeIn(tk, shift=UP * 0.1), *takeaway_anims(self, tk))
        self.wait(0.3)
        self.clear_scene()
