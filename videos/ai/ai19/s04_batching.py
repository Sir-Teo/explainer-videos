from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai17.specs import GPUS
from videos.ai.ai19.common import (BYTEC, COSTC, DECODEC, F, FLOPC, KVC, PART, WEIGHTC, load, loglog, take_away, x_)


class Batching(VoiceoverScene):
    def construct(self):
        self.card()
        self.tradeoff()
        self.model()
        self.cost()

    def card(self):
        card = chapter_card(3, r"Batching: \ speed against cost", r"How fast for one person, \ how cheap for everyone?",
                            part=PART)
        with self.voiceover("Chapter three. Batching: speed against cost."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def tradeoff(self):
        e = load("economics")
        B = np.asarray(e["meas_B"])
        user, tot = np.asarray(e["meas_user"]), np.asarray(e["meas_total"])
        g = loglog((math.log10(user.min() * 0.6), math.log10(user.max() * 1.6)),
                   (math.log10(tot.min() * 0.6), math.log10(tot.max() * 1.8)), x_length=6.4, y_length=4.2,
                   xlabel=r"tokens a second, \ for each conversation", ylabel=r"tokens a second, \ all together",
                   center=[-2.5, -0.3, 0])
        ax = g.ax
        pts = [ax.c2p(math.log10(u), math.log10(t)) for u, t in zip(user, tot)]
        dots = VGroup(*[Dot(p_, radius=0.07, color=DECODEC) for p_ in pts])
        line = VMobject(color=DECODEC, stroke_width=2.5).set_points_as_corners(pts)
        labs = VGroup(*[MathTex(rf"B={int(b)}", font_size=18, color=GREY_B).next_to(d_, UR, buff=0.04)
                        for b, d_ in zip(B, dots) if int(b) in (1, 4, 16, 64, 256)])
        head = label(r"our novels model, \ this computer: \ one decode step, \ batch $B$", font_size=24,
                     color=GREY_A).to_edge(UP, buff=0.35)
        k = list(B).index(256)
        fair = VGroup(label(rf"$B = 1$: \ ${user[0]:.0f}$ tokens/s for one person", font_size=22, color=DECODEC),
                      label(rf"$B = 256$: \ ${tot[k]:,.0f}$ in all, \ ${user[k]:.0f}$ each".replace(",", "{,}"),
                            font_size=22, color=DECODEC)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.2, 1.2, 0])
        with self.voiceover(
            "Every server faces the trade from chapter one. <bookmark mark='a'/> Here it is for our model on this "
            "computer: each dot a batch size, its speed for one conversation across, its total work up. "
            f"<bookmark mark='b'/> Alone, a conversation gets {user[0]:.0f} tokens a second. Batched with 255 "
            f"others, the computer writes {tot[k]:,.0f} tokens a second in all, {x_(tot[k] / tot[0])} times as many, "
            f"but each conversation gets {user[k]:.0f}. <bookmark mark='c'/> Up and to the left is cheap; down and "
            "to the right is fast. A provider picks a point on this curve, and the price follows."
        ) as vo:
            self.play(FadeIn(g), FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_, scale=0.5) for d_ in dots], lag_ratio=0.12), Create(line), FadeIn(labs),
                      run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(fair[0]), Indicate(dots[0], color=DECODEC, scale_factor=1.8))
            self.play(FadeIn(fair[1]), Indicate(dots[k], color=DECODEC, scale_factor=1.8))
            vo.wait_until("c")
            self.play(Indicate(line, color=WHITE))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def model(self):
        e = load("economics")
        H = GPUS["H100"]
        m = F.LLAMA31_8B
        colors = {r"W": WEIGHTC, r"B": DECODEC, r"c": KVC, r"\kappa": KVC, r"\beta": BYTEC, r"P": FLOPC, r"N": WEIGHTC}
        rows = [
            cmath(r"t(B)", r"\ge", r"\frac{W + B\,c\,\kappa}{\beta}", colors=colors, font_size=38),
            cmath(r"t(B)", r"\ge", r"\frac{2N B}{P}", colors=colors, font_size=38),
            cmath(r"W + B\,c\,\kappa", r"\le", r"\text{memory}", colors=colors, font_size=38),
            cmath(r"\text{cost per token}", r"=", r"\frac{\text{price per second}}{B / t(B)}", colors=colors,
                  font_size=38),
        ]
        whys = [why(r"read the weights $W$ and $B$ caches of $c$ tokens"), why(r"do the arithmetic"),
                why(r"everything has to fit"), why(r"the machine's time, shared by $B$")]
        step = ladder(self, rows, whys, keep=4, top=2.6, x=-2.6, buff=0.42, edge=6.8)
        spec = VGroup(
            label(rf"Llama 3.1 8B: \ $W = {2 * m['params'] / 1e9:.0f}$ GB, \ "
                  rf"$\kappa = {e['kv_tok'] / 1024:.0f}$ KiB per token", font_size=22, color=WEIGHTC),
            label(rf"one H100: \ $\beta = {H['bw'] / 1e12:.2f}$ TB/s, \ $P = {H['tensor'] / 1e12:.0f}$ TFLOP/s, \ "
                  rf"${H['mem'] / 1e9:.0f}$ GB", font_size=22, color=GREY_A),
            label(rf"price: \ \${e['price']:.0f} per GPU-hour, \ the rate DeepSeek costed its service at",
                  font_size=22, color=COSTC),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.45)
        hc = history_card(2022, r"Reiner Pope et al., \ Google", rf"{F.POPE['model']}: \ "
                          rf"${F.POPE['latency_ms']}$ ms a token at small batches, \ ${F.POPE['mfu']}\%$ of peak "
                          r"reading prompts", width=4.6, font_size=18, color=COSTC).to_corner(UR, buff=0.3)
        tag = note(r"a roofline model, \ not a measurement: \ real servers reach a fraction of it").to_corner(UL, buff=0.2)
        with self.voiceover(
            "To see what this means for a real model on a real chip, model it with the roofline. "
            "<bookmark mark='a'/> A decode step reads the weights, W bytes, and every conversation's cache: c "
            "tokens at kappa bytes each. It can't go faster than the memory, beta. <bookmark mark='b'/> Nor faster "
            "than the arithmetic: two N B operations at P a second. <bookmark mark='c'/> And it all has to fit in "
            "memory, which caps the batch. <bookmark mark='d'/> The machine's time is shared, so the cost of a "
            "token is the price of a second divided by the tokens written per second. <bookmark mark='e'/> We use "
            "Llama 3.1 8B on one H100, at two dollars an hour: the rental price DeepSeek used to cost its own "
            "service. In 2022 Reiner Pope and colleagues at Google worked through this accounting for PaLM: the "
            "same weights, read faster or shared wider."
        ) as vo:
            self.play(FadeIn(tag))
            step(0)
            vo.wait_until("a")
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
            vo.wait_until("e")
            self.play(LaggedStart(*[FadeIn(s_, shift=UP * 0.1) for s_ in spec], lag_ratio=0.3), FadeIn(hc))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cost(self):
        e = load("economics")
        ctxs = (1024, 8192, 32768, 131072)
        cols = [DECODEC, KVC, C.BITS, C.SURPRISE]
        allu = np.concatenate([np.asarray(e[f"c{c}"]["user"]) for c in ctxs])
        allc = np.concatenate([np.asarray(e[f"c{c}"]["cost"]) for c in ctxs])
        g = loglog((math.log10(allu.min() * 0.7), math.log10(allu.max() * 1.4)),
                   (math.floor(math.log10(allc.min() * 0.8)), math.log10(allc.max() * 2)), x_length=6.6,
                   y_length=4.3, xlabel=r"tokens a second, \ for each conversation",
                   ylabel=r"USD per million tokens written", center=[-2.5, -0.35, 0])
        ax = g.ax
        lines, ends = VGroup(), VGroup()
        for c, col in zip(ctxs, cols):
            d = e[f"c{c}"]
            pts = [ax.c2p(math.log10(u), math.log10(v)) for u, v in zip(d["user"], d["cost"])]
            lines.add(VMobject(color=col, stroke_width=3).set_points_as_corners(pts))
            ends.add(VGroup(Dot(pts[0], radius=0.06, color=col), Dot(pts[-1], radius=0.07, color=col)))
        leg = legend([(col, rf"context ${c // 1024}$k tokens") for c, col in zip(ctxs, cols)], font_size=20)
        leg.move_to([4.6, 1.6, 0])
        d1, d128 = e["c1024"], e["c131072"]
        notes = VGroup(
            label(rf"$1$k context: \ $B$ up to ${d1['bmax']}$", font_size=21, color=DECODEC),
            label(rf"\${d1['cost'][0]:.2f} $\to$ \${d1['cost'][-1]:.3f} per million", font_size=21, color=DECODEC),
            label(rf"$128$k context: \ $B$ up to ${d128['bmax']}$", font_size=21, color=C.SURPRISE),
            label(rf"at best \${d128['cost'][-1]:.2f} per million", font_size=21, color=C.SURPRISE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([4.6, -1.1, 0])
        tw = take_away(r"big batches make tokens cheap; \ long contexts keep batches small", font_size=26)
        fall = d1["cost"][0] / d1["cost"][-1]
        slow = d1["user"][0] / d1["user"][-1]
        mfu = d1["mfu"][-1]
        with self.voiceover(
            "Here is what the model gives. <bookmark mark='a'/> Each line is a context length; along it, the batch "
            "grows from one, up and to the left, until memory runs out. <bookmark mark='b'/> With a thousand tokens "
            f"of context, one conversation alone costs {d1['cost'][0]:.2f} dollars per million tokens. A batch of "
            f"{d1['bmax']} brings that to {d1['cost'][-1]:.3f}: {fall:.0f} times cheaper, while each conversation "
            f"gets {x_(slow)} times slower. Even then the chip does only {100 * mfu:.0f} percent of the arithmetic it "
            f"could. <bookmark mark='c'/> At 128 thousand tokens, {d128['bmax']} conversations fill the memory, and a "
            "token "
            f"costs at least {d128['cost'][-1]:.2f} dollars per million. That's why long contexts cost more, and "
            "why so much of this part is about shrinking the cache."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.25), FadeIn(leg), FadeIn(ends), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(notes[:2]), Indicate(ends[0], color=DECODEC, scale_factor=1.6))
            vo.wait_until("c")
            self.play(FadeIn(notes[2:]), Indicate(ends[3], color=C.SURPRISE, scale_factor=1.6))
            self.play(FadeIn(tw))
        self.wait(0.3)
        self.clear_scene()
