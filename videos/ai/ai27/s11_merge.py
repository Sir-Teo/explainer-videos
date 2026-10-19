from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai27.common import ADAPT, ASSIST, BASE, GOLD, PART, PENALTY, POLICY, REF, REWARD, load


class Merge(VoiceoverScene):
    def construct(self):
        self.card()
        self.basins()
        self.arithmetic()
        self.ours()
        self.family()

    def card(self):
        card = chapter_card(10, r"Adding models together", r"What happens if you average two networks' weights?",
                            lit=(2022, 2023), part=PART)
        with self.voiceover("Chapter ten. Adding models together."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def basins(self):
        # a schematic loss landscape: fine-tunes of one model stay in one valley
        g = axes([-3, 3], [0, 3], x_length=6.0, y_length=3.0, xticks=[], yticks=[], xlabel=r"weights",
                 ylabel=r"loss", center=[-3.2, -0.4, 0])
        xs = np.linspace(-3, 3, 200)
        L = 0.25 * xs ** 2 + 0.6 * np.exp(-((xs - 2.4) ** 2) * 3) + 0.25
        land = VMobject().set_points_smoothly([g.ax.c2p(a, b) for a, b in zip(xs, L)]).set_stroke(GREY_B, 3)
        pre = Dot(g.ax.c2p(0.0, 0.25 + 1.2), radius=0.08, color=BASE)
        f1 = Dot(g.ax.c2p(-0.8, 0.25 * 0.64 + 0.25), radius=0.08, color=ASSIST)
        f2 = Dot(g.ax.c2p(0.9, 0.25 * 0.81 + 0.25), radius=0.08, color=POLICY)
        mid = Dot(g.ax.c2p(0.05, 0.25 + 0.01), radius=0.09, color=GOLD)
        seg = DashedLine(f1.get_center(), f2.get_center(), color=GOLD, dash_length=0.06)
        tag = note(r"schematic").to_corner(DL, buff=0.3)
        cards = VGroup(
            history_card(2020, r"linear mode connectivity \ (Frankle et al.)", r"two networks trained from the same "
                         r"start can often be joined by a straight line along which the loss stays low", width=5.8,
                         color=GOLD),
            history_card(2022, r"model soups \ (Wortsman et al.)", r"average the weights of fine-tunes with "
                         r"different settings: \ better than the best single one, \ at no cost at inference",
                         width=5.8, color=ASSIST),
        ).arrange(DOWN, buff=0.35).move_to([3.4, 0.0, 0])
        with self.voiceover(
            "Averaging the weights of two different networks usually produces garbage: their units are arranged "
            "differently, and the average lands on a ridge between two valleys. <bookmark mark='a'/> But fine-tunes "
            "of one pretrained model are different. They start from the same point and move only a little, so they "
            "tend to stay in the same valley, and the straight line between them stays low: linear mode "
            "connectivity. <bookmark mark='b'/> In 2022 Mitchell Wortsman and colleagues averaged the weights of "
            "many fine-tunes run with different settings, a model soup, and got a better model than any one of them, "
            "with no extra cost at inference."
        ) as vo:
            self.play(FadeIn(g), Create(land), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(pre))
            self.play(TransformFromCopy(pre, f1), TransformFromCopy(pre, f2))
            self.play(Create(seg), FadeIn(mid, scale=1.5), FadeIn(cards[0], shift=UP * 0.15))
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=UP * 0.15))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def arithmetic(self):
        rows = [
            cmath(r"\tau_{\text{task}}", r"=", r"\theta_{\text{fine-tuned}} - \theta_{\text{pretrained}}", font_size=36),
            cmath(r"\theta", r"=", r"\theta_{\text{pretrained}} + \lambda\, (\tau_A + \tau_B)", font_size=36),
            cmath(r"\theta", r"=", r"\theta_{\text{pretrained}} - \lambda\, \tau_{\text{toxic}}", font_size=36),
        ]
        for r_ in rows:
            r_[0].set_color(ADAPT)
        whys = [why(r"a task vector: \ what fine-tuning changed"), why(r"add two: \ a model that does both"),
                why(r"subtract one: \ forget a behaviour")]
        step = ladder(self, rows, whys, keep=3, top=2.4, x=-1.8, buff=0.65, edge=6.9)
        hc = note(r"Ilharco et al., \textit{Editing models with task arithmetic} (2023)").to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "In 2023 Gabriel Ilharco and colleagues turned this into arithmetic. Subtract the pretrained weights "
            "from a fine-tuned model's weights, and call the difference a task vector: everything fine-tuning "
            "changed. <bookmark mark='a'/> Add two task vectors to the pretrained model, and you often get a model "
            "that can do both tasks, without training on both. <bookmark mark='b'/> Subtract one, and the model "
            "unlearns it: subtracting the vector of a model fine-tuned on toxic text made the original less toxic."
        ) as vo:
            step(0)
            self.play(FadeIn(hc))
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ours(self):
        d = load("merge")
        rows = d["rows"]
        names = {"which only": r"which-book \\ fine-tune", "line only": r"line \\ fine-tune"}

        def nm(name):
            if name in names:
                return names[name]
            lam = name.split()[-1]
            return r"the base" if float(lam) == 0 else rf"base $+$ \\ $\lambda = {lam}$"

        g = axes([0, len(rows)], [0, 1], x_length=10.5, y_length=3.6, yticks=[0, 0.5, 1],
                 yfmt=lambda v: rf"{100 * v:.0f}\%", center=[0.3, -0.1, 0])
        groups = VGroup()
        for k, (name, acc, gold_, ended) in enumerate(rows):
            col = ADAPT if name.startswith("sum") else ASSIST
            bars = VGroup()
            for j, (v, c) in enumerate(((acc, ASSIST), (ended, ADAPT))):
                h = max(g.ax.c2p(0, v)[1] - g.ax.c2p(0, 0)[1], 0.02)
                bars.add(Rectangle(width=0.55, height=h, stroke_width=0, fill_color=c, fill_opacity=0.9)
                         .move_to(g.ax.c2p(k + 0.5 + (j - 0.5) * 0.62, 0), aligned_edge=DOWN))
                bars.add(label(rf"${100 * v:.0f}\%$", font_size=18, color=c).next_to(bars[-1], UP, buff=0.06))
            tag_ = label(nm(name), font_size=19, color=col).next_to(g.ax.c2p(k + 0.5, 0), DOWN, buff=0.2)
            groups.add(VGroup(bars, tag_))
        lg = legend([(ASSIST, r"which book? \ placed right"), (ADAPT, r"a line about\dots: \ ended cleanly")],
                    font_size=20).to_corner(UR, buff=0.4)
        multi = label(rf"one model trained on both at once: \ ${100 * d['multitask_which']:.0f}\%$ placed right",
                      font_size=22, color=GREY_A).to_edge(DOWN, buff=0.55)
        tag = note(r"computed: \ each task fine-tuned alone from the novels model; \ $\tau$ = the change in "
                   r"every weight").to_corner(DL, buff=0.2)
        merged = [r for r in rows if r[0].startswith("sum") and float(r[0].split()[-1]) > 0]
        best = max(merged, key=lambda r: r[1] + r[3])
        w_only = rows[0]
        said_ = (f"Adding the two task vectors, at lambda {best[0].split()[-1]}, the merged model places "
                 f"{100 * best[1]:.0f} percent of sentences, against {100 * w_only[1]:.0f} for the which-book model "
                 f"alone, and ends {100 * best[3]:.0f} percent of its lines cleanly.")
        with self.voiceover(
            "We tried it on the novels model. Fine-tune one copy only on which-book questions, another only on lines "
            "about things, and take their task vectors. <bookmark mark='a'/> Each fine-tune is good at its own "
            "task. <bookmark mark='b'/> " + said_ + " <bookmark mark='c'/> Merging is not free, but it is "
            "remarkably cheap: no training at all, just addition."
        ) as vo:
            self.play(FadeIn(g), FadeIn(lg), FadeIn(tag))
            vo.wait_until("a")
            self.play(*[FadeIn(gr_) for gr_ in groups[:2]])
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(gr_) for gr_ in groups[2:]], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(FadeIn(multi))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def family(self):
        cards = VGroup(
            history_card(2023, r"TIES-merging \ (Yadav et al.)", r"keep each task vector's largest changes, \ settle "
                         r"sign conflicts by vote, \ then add", width=6.2, color=ADAPT),
            history_card(2024, r"DARE \ (Yu et al.)", r"drop most of a task vector's entries at random and rescale the "
                         r"rest: \ the vectors barely interfere", width=6.2, color=ADAPT),
            history_card(2024, r"Llama 3", r"averaged models trained on different data and settings at each "
                         r"post-training stage", width=6.2, color=ASSIST),
            history_card(2024, r"open leaderboards", r"merges of fine-tunes of the same base model often led them", width=6.2,
                         color=GOLD),
        ).arrange_in_grid(rows=2, cols=2, buff=0.35).move_to(UP * 0.1)
        cite_ = cite(r"Yadav et al.\ (2023); \ Yu et al.\ (2024); \ Llama Team (2024)")
        with self.voiceover(
            "Merging became a craft. <bookmark mark='a'/> TIES keeps only each task vector's largest changes and "
            "resolves disagreements in sign by a vote before adding. <bookmark mark='b'/> DARE drops most of a task "
            "vector's entries at random and rescales the rest, and the vectors interfere much less. "
            "<bookmark mark='c'/> Meta's Llama 3 averaged models trained with different data and settings at each "
            "stage of post-training. <bookmark mark='d'/> And for a while, merged models topped the open "
            "leaderboards."
        ) as vo:
            self.play(FadeIn(cite_))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.15))
        self.wait(0.3)
        self.clear_scene()
