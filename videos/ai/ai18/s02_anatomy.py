from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai18.common import (C_COL, D_COL, EDU, F, GPU, LR_COL, N_COL, PAGE, PART, REMOVED, load, stage_row,
                                   take_away)


class Anatomy(VoiceoverScene):
    def construct(self):
        self.card()
        self.stages()
        self.runs()
        self.cost()

    def card(self):
        card = chapter_card(1, r"Anatomy of a frontier run", r"What happens between raw text and a base model?",
                            lit=(2020, 2024), part=PART)
        with self.voiceover("Chapter one. Anatomy of a frontier run."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def stages(self):
        top = stage_row([(r"crawl", PAGE), (r"filter", REMOVED), (r"deduplicate", C.DUP), (r"mix", EDU),
                         (r"tokenize", GREY_A)], font_size=22).move_to(UP * 2.6)
        bot = stage_row([(r"pretrain", N_COL), (r"anneal, \ mid-train", LR_COL), (r"long context", C.POSITION),
                         (r"post-train", C.REWARD)], font_size=22).move_to(UP * 1.25)
        # an elbow from the last data stage down to the first training stage, between the two rows
        y_mid = (top.boxes[-1].get_bottom()[1] + bot.boxes[0].get_top()[1]) / 2
        p0, p3 = top.boxes[-1].get_bottom() + DOWN * 0.06, bot.boxes[0].get_top() + UP * 0.04
        p1, p2 = np.array([p0[0], y_mid, 0]), np.array([p3[0], y_mid, 0])
        link = VGroup(VMobject(stroke_color=GREY_B, stroke_width=2.5).set_points_as_corners([p0, p1, p2]),
                      Arrow(p2, p3, buff=0, color=GREY_B, stroke_width=2.5, tip_length=0.14,
                            max_tip_length_to_length_ratio=0.7))
        O, S = F.OLMO3, F.SMOLLM3
        # two published runs, stage by stage, as bars proportional to tokens
        W = 11.0
        tot_o = O["pre"] + O["mid"] + O["long"][0]
        tot_s = S["stages"][-1][1] + sum(t[1] - t[0] for t in S["long"]) * 0 + 0.1e12
        rows = VGroup()
        specs = [(r"Olmo 3, 7B", [(O["pre"], N_COL, r"pretraining $5.9$T"), (O["mid"], LR_COL, r"mid $0.1$T"),
                                  (O["long"][0], C.POSITION, r"long $0.05$T")], tot_o),
                 (r"SmolLM3, 3B", [(S["stages"][0][1], N_COL, r"stage 1: \ $8$T"),
                                   (S["stages"][1][1] - S["stages"][1][0], LR_COL, r"stage 2: \ $2$T"),
                                   (S["stages"][2][1] - S["stages"][2][0], EDU, r"3: \ $1.1$T"),
                                   (0.1e12, C.POSITION, r"")], tot_s)]
        for k, (name, segs, tot) in enumerate(specs):
            x = -W / 2 + 1.2
            row = VGroup()
            nm = label(name, font_size=22, color=GREY_A)
            for n, col, txt in segs:
                w = max(W * 0.86 * n / tot, 0.04)
                r = Rectangle(width=w, height=0.5, stroke_width=1, stroke_color=BLACK, fill_color=col, fill_opacity=0.85)
                r.move_to([x + w / 2, -0.6 - 1.15 * k, 0])
                row.add(r)
                if txt and w > 1.4:
                    row.add(label(txt, font_size=18, color=BLACK).move_to(r))
                x += w
            nm.next_to(row[0], LEFT, buff=0.2)
            rows.add(VGroup(nm, row))
        thin = label(r"mid-training and long context: \ thin slivers of the tokens, \ chosen with great care",
                     font_size=22, color=LR_COL).move_to(DOWN * 3.05)
        src = cite(r"Team OLMo, Olmo 3 (2025); \ Hugging Face, SmolLM3 (2025)", corner=DR, font_size=17)
        with self.voiceover(
            "A frontier pretraining run is a pipeline. It starts with a crawl of billions of web pages, "
            "<bookmark mark='a'/> filtered for language and quality, deduplicated, mixed with books, code, maths and "
            "synthetic text, and cut into tokens. <bookmark mark='b'/> Then the model trains: a long pretraining "
            "phase, a short "
            "annealing on the best data, often called mid-training, a stage for long context, and the post-training "
            "of Part "
            "27. <bookmark mark='c'/> Here are two published runs to scale. Ai2's Olmo 3, seven billion parameters: "
            "5.9 "
            "trillion tokens of pretraining, then 100 billion of mid-training and 50 billion for long context. "
            "Hugging Face's "
            "SmolLM3: three pretraining stages, then long context. <bookmark mark='d'/> The last stages are a few "
            "percent of "
            "the tokens, chosen with the most care."
        ) as vo:
            pipe = VGroup(top, bot, link)  # in the middle, larger, until the runs need the space below it
            pipe.save_state()
            pipe.scale(1.15).shift(DOWN * 1.9)
            ghost = bot.boxes.copy().set_opacity(0.15)
            self.play(FadeIn(top.boxes[0]), FadeIn(ghost))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(GrowArrow(a), FadeIn(b)) for a, b in zip(top.arrows, top.boxes[1:])],
                                  lag_ratio=0.5), run_time=3.0)
            vo.wait_until("b")
            self.play(Create(link), LaggedStart(*[FadeIn(b) for b in bot.boxes], lag_ratio=0.4),
                      LaggedStart(*[GrowArrow(a) for a in bot.arrows], lag_ratio=0.4), run_time=3.0)
            self.remove(ghost)
            vo.wait_until("c")
            self.play(Restore(pipe), run_time=1.0)
            self.play(FadeIn(src), FadeIn(rows[0][0]), LaggedStart(*[FadeIn(m) for m in rows[0][1]], lag_ratio=0.3))
            self.play(FadeIn(rows[1][0]), LaggedStart(*[FadeIn(m) for m in rows[1][1]], lag_ratio=0.3))
            vo.wait_until("d")
            self.play(FadeIn(thin, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def runs(self):
        cols = [r"model", r"released", r"tokens", r"chips", r"number format", r"optimizer"]
        L, D, K, O, N4, V4 = F.LLAMA3, F.DSV3, F.KIMIK2, F.OLMO3, F.NEMOTRON3, F.DSV4
        data = [
            (r"Llama 3.1 405B", r"Jul 2024", r"$15.6$T", r"$16{,}384$ H100", r"BF16", r"AdamW"),
            (r"DeepSeek-V3", r"Dec 2024", r"$14.8$T", r"$2{,}048$ H800", r"FP8", r"AdamW"),
            (r"Kimi K2", r"Jul 2025", r"$15.5$T", r"H800", r"--", r"MuonClip"),
            (r"Olmo 3 32B", r"Nov 2025", r"$5.9$T", r"$1{,}024$ H100", r"BF16", r"--"),
            (r"Nemotron 3 Super", r"Mar 2026", r"$25$T", r"--", r"NVFP4", r"--"),
            (r"DeepSeek-V4-Pro", r"Apr 2026", r"$33$T", r"--", r"FP8 mixed", r"Muon"),
        ]
        xs = [-5.1, -2.3, -0.55, 1.4, 3.55, 5.55]
        head = VGroup(*[label(c, font_size=25, color=GREY_B).move_to([x, 2.75, 0]) for c, x in zip(cols, xs)])
        rule = Line([-6.6, 2.42, 0], [6.6, 2.42, 0], color=GREY_D, stroke_width=1.5)
        body = VGroup()
        colors = [C.TOKEN, GREY_A, D_COL, GPU, C.QUANT, C.MUON]
        for i, row in enumerate(data):
            y = 1.95 - 0.7 * i
            body.add(VGroup(*[label(t, font_size=25, color=WHITE if j == 0 else colors[j]).move_to([x, y, 0])
                              for j, (t, x) in enumerate(zip(row, xs))]))
        src = cite(r"Llama Team (2024); \ DeepSeek-AI (2024, 2026); \ Kimi Team (2025); \ Team OLMo (2025); \ "
                   r"NVIDIA (2026). \ --: \ not stated", font_size=17)
        tw = take_away(r"tokens up $2\times$ in two years; \ fewer bits; \ a new optimizer", color=C.BITS,
                       font_size=26).shift(UP * 0.2)
        with self.voiceover(
            "Here are six open runs of the last two years, as their reports state them. <bookmark mark='a'/> Llama "
            "3.1 405B: "
            "15.6 trillion tokens on 16,384 H100 GPUs, in sixteen-bit bfloat numbers, with AdamW. DeepSeek-V3: 14.8 "
            "trillion "
            "tokens on 2,048 H800s, in eight-bit floating point. <bookmark mark='b'/> Kimi K2: 15.5 trillion tokens "
            "with "
            "MuonClip, a version of the Muon optimizer. Olmo 3, the most open, data included. <bookmark mark='c'/> "
            "And in "
            "2026, NVIDIA's Nemotron 3 Super, pretrained in four-bit numbers on 25 trillion tokens, and "
            "DeepSeek-V4-Pro, on 33 "
            "trillion with Muon. <bookmark mark='d'/> In two years the token counts doubled, the numbers shrank from "
            "sixteen "
            "bits to eight and four, and the optimizer began to change."
        ) as vo:
            self.play(FadeIn(head), Create(rule), FadeIn(src), FadeIn(body[0]), FadeIn(body[1]))
            vo.wait_until("a")
            self.play(Indicate(body[0], scale_factor=1.03), Indicate(body[1], scale_factor=1.03))
            vo.wait_until("b")
            self.play(FadeIn(body[2]), FadeIn(body[3]))
            vo.wait_until("c")
            self.play(FadeIn(body[4]), FadeIn(body[5]))
            vo.wait_until("d")
            self.play(FadeIn(tw, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cost(self):
        P, D, L = load("published"), F.DSV3, F.LLAMA3
        colors = {r"C": C_COL, r"N": N_COL, r"D": D_COL}
        rows = [
            cmath(r"C", r"\approx", r"6\,N\,D", colors=colors, font_size=40),
            cmath(r"C_{\text{Llama 3.1}}", r"\approx", r"6 \times 405\text{B} \times 15.6\text{T}", r"=",
                  sci(P["llama_6nd"], 2), colors=colors, font_size=34),
            cmath(r"C_{\text{DeepSeek-V3}}", r"\approx", r"6 \times 37\text{B} \times 14.8\text{T}", r"=",
                  sci(P["dsv3_6nd"], 2), colors=colors, font_size=34),
        ]
        whys = [why(r"Part 14: \ two operations per parameter forward, four back", font_size=20),
                why(rf"reported: \ ${sci(L['flops'], 1)}$", font_size=20),
                why(r"$37$B of its $671$B parameters are active per token", font_size=20)]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-1.0, buff=0.5, edge=6.8)
        hours = VGroup(
            label(rf"pretraining: \ ${D['hours_pre'] / 1e6:.3f}$M H800 GPU-hours", font_size=24, color=GPU),
            label(rf"longer context: \ ${D['hours_ctx'] / 1e3:.0f}$k; \ post-training: \ ${D['hours_post'] / 1e3:.0f}$k",
                  font_size=24, color=GPU),
            label(rf"at \$${D['rate']:.0f}$ an hour: \ \$${P['dsv3_usd'] / 1e6:.3f}$ million", font_size=28, color=C_COL),
            label(rf"each trillion tokens: \ ${D['hours_per_T'] / 1e3:.0f}$k GPU-hours $=$ ${P['dsv3_days_per_T']:.1f}$ "
                  rf"days on ${D['gpus']:,}$ GPUs".replace(",", "{,}"), font_size=24, color=D_COL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([0, -1.9, 0])
        caveat = note(r"the final run only: \ not the experiments, the data, the people, or the cluster itself",
                      font_size=20).next_to(hours, DOWN, buff=0.25)
        src = cite(r"DeepSeek-AI (2024), \ Table 1; \ Llama Team (2024)", corner=DR, font_size=17)
        # the two compute totals to scale
        cbars = VGroup()
        for k, (nm, v) in enumerate(((r"Llama 3.1", P["llama_6nd"]), (r"DeepSeek-V3", P["dsv3_6nd"]))):
            y_ = 0.4 - 0.6 * k
            r_ = Rectangle(width=7.4 * v / P["llama_6nd"], height=0.36, stroke_width=0, fill_color=C_COL,
                           fill_opacity=0.8)
            r_.move_to([-3.4 + r_.width / 2, y_, 0])
            t_ = label(nm, font_size=21, color=GREY_A).next_to([-3.4, y_, 0], LEFT, buff=0.2)
            v_ = label(rf"${sci(v, 2)}$ FLOP", font_size=20, color=C_COL).next_to(r_, RIGHT, buff=0.15)
            cbars.add(VGroup(t_, r_, v_))
        with self.voiceover(
            "How big is such a run? Part 14 gave the rule: about six operations per parameter per token. "
            "<bookmark mark='a'/> For Llama 3.1, six times 405 billion times 15.6 trillion is "
            f"{P['llama_6nd'] / 1e25:.2f} times ten to the twenty-five, just what Meta reports. <bookmark mark='b'/> "
            "DeepSeek-V3 is a mixture of experts: only 37 billion of its parameters work on each token, so it needs "
            f"{P['dsv3_6nd'] / 1e24:.1f} times ten to the twenty-four, about a tenth. <bookmark mark='c'/> Its report "
            "also "
            "gives the bill: 2.664 million H800 GPU-hours for pretraining; at two dollars an hour, "
            f"{P['dsv3_usd'] / 1e6:.3f} million dollars for the whole run. <bookmark mark='d'/> That prices the final "
            "run only: "
            "not the experiments before it, the data, or the cluster."
        ) as vo:
            step(0)
            self.play(FadeIn(src))
            vo.wait_until("a")
            step(1)
            self.play(FadeIn(cbars[0][0]), GrowFromEdge(cbars[0][1], LEFT), FadeIn(cbars[0][2]))
            vo.wait_until("b")
            step(2)
            self.play(FadeIn(cbars[1][0]), GrowFromEdge(cbars[1][1], LEFT), FadeIn(cbars[1][2]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(h, shift=UP * 0.1) for h in hours[:3]], lag_ratio=0.5), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(hours[3]), FadeIn(caveat))
        self.wait(0.3)
        self.clear_scene()
