from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai19.common import (BYTEC, COSTC, DECODEC, F, PART, PREFILLC, hbars, load, x_)


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.thinking()
        self.prices()
        self.devices()

    def card(self):
        card = chapter_card(17, r"The frontier, \ late 2026", r"What does thinking longer cost, \ and who can run these "
                            r"models?", lit=(2024, 2025), part=PART)
        with self.voiceover("Chapter seventeen. The frontier, late 2026."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def thinking(self):
        fr = load("frontier")
        th = fr["thinking"]
        R = F.R1_0528
        keys = ["1000", str(R["tokens_old"]), str(R["tokens_new"]), str(R["max_len"])]
        names = [rf"${int(k) // 1000}$k tokens" for k in keys]
        usd = [th[k]["usd"] * 1e3 for k in keys]
        b = hbars(usd, names, [GREY_B, DECODEC, COSTC, C.SURPRISE], width=4.2, row_h=0.55, font_size=21, lo=0,
                  hi=max(usd) * 1.1, fmt_v=lambda v: rf"\${v:.2f}" if v >= 0.1 else rf"\${v:.3f}")
        b.move_to([-2.2, -0.4, 0])
        bt = label(r"cost per thousand answers, \ by answer length", font_size=22, color=COSTC).next_to(b, UP, buff=0.3)
        per = VGroup(*[label(rf"{nm}: \ batch ${th[k]['bmax']}$, \ \${th[k]['per_mtok']:.2f} per million",
                             font_size=19, color=GREY_A) for k, nm in zip(keys, names)])
        per.arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([4.2, -0.6, 0])
        tag = note(r"Llama 3.1 8B on one H100, \ the roofline model of chapter three, \ \$2 per GPU-hour",
                   font_size=17).to_corner(DR, buff=0.2)
        hc = history_card(2025, r"DeepSeek-R1-0528", rf"AIME: \ ${R['tokens_old'] // 1000}$k $\to$ "
                          rf"${R['tokens_new'] // 1000}$k tokens a question, \ ${R['acc_old']:.0f}\% \to "
                          rf"{R['acc_new']}\%$", width=4.4, font_size=17, color=COSTC).to_corner(UR, buff=0.25)
        k1, k2 = str(R["tokens_old"]), str(R["tokens_new"])
        r1 = VGroup(
            label(r"DeepSeek-R1 on AIME 2025", font_size=22, color=COSTC),
            hbars([R["tokens_old"] / 1e3, R["tokens_new"] / 1e3], [r"January 2025", r"May 2025 (0528)"],
                  [DECODEC, COSTC], width=4.0, row_h=0.55, font_size=21, lo=0, hi=R["tokens_new"] / 1e3 * 1.1,
                  fmt_v=lambda v: rf"{v:.0f}\text{{k tokens a question}}"),
            label(rf"accuracy: \ ${R['acc_old']:.0f}\%$ $\to$ ${R['acc_new']}\%$", font_size=22, color=COSTC),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([-1.6, 0.0, 0])
        ratio = th[k2]["usd"] / th[k1]["usd"]
        tok = R["tokens_new"] / R["tokens_old"]
        with self.voiceover(
            "Reasoning models, Part 28's subject, think in tokens, and every token is a decode step. "
            "<bookmark mark='a'/> In May 2025 DeepSeek's update to R1 lifted its score on a hard maths competition "
            f"from {R['acc_old']:.0f} to {R['acc_new']} percent, and it did so partly by thinking longer: "
            f"{R['tokens_new'] // 1000} thousand tokens a question instead of {R['tokens_old'] // 1000}. "
            "<bookmark mark='b'/> What does length cost? Take chapter three's model of a GPU serving a model, "
            "and write answers of each length, with as many conversations as the memory holds. "
            f"<bookmark mark='c'/> {tok:.1f} times the tokens cost {x_(ratio)} times as much, because the caches grow, "
            "the batch shrinks, and every token gets dearer: from "
            f"{th[k1]['per_mtok']:.2f} to {th[k2]['per_mtok']:.2f} dollars per million. Thinking longer is a "
            "decoding problem, and everything in this part is how it is made affordable."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(hc), FadeIn(r1[0]), LaggedStart(*[AnimationGroup(FadeIn(r_.name), GrowFromEdge(r_.bar, LEFT),
                                                                            FadeIn(r_.val)) for r_ in r1[1]],
                                                          lag_ratio=0.4), FadeIn(r1[2]))
            vo.wait_until("b")
            self.play(FadeOut(r1))
            self.play(FadeIn(bt), LaggedStart(*[AnimationGroup(FadeIn(r_.name), GrowFromEdge(r_.bar, LEFT),
                                                               FadeIn(r_.val)) for r_ in b], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(FadeIn(per))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def prices(self):
        fr = load("frontier")
        yrs, usd, names = np.asarray(fr["price_years"]), np.asarray(fr["price_usd"]), list(fr["price_names"])
        g = axes([2020.5, 2025], [-1.2, 2.0], x_length=7.0, y_length=4.0, xlabel=r"year",
                 ylabel=r"USD per million input tokens \ (log)", xticks=[2021, 2022, 2023, 2024, 2025],
                 yticks=[-1, 0, 1, 2], yfmt=lambda v: {-1: "0.1", 0: "1", 1: "10", 2: "100"}[int(v)],
                 center=[-2.0, -0.3, 0])
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(y, math.log10(u)), radius=0.08, color=COSTC) for y, u in zip(yrs, usd)])
        labs = VGroup(*[label(rf"{n}: \ \${u:g}", font_size=17, color=COSTC).next_to(d_, UR, buff=0.06)
                        for n, u, d_ in zip(names, usd, dots)])
        fit = np.polyfit(yrs, np.log10(usd), 1)
        line = DashedLine(ax.c2p(2020.7, np.polyval(fit, 2020.7)), ax.c2p(2024.9, np.polyval(fit, 2024.9)),
                          color=COSTC, dash_length=0.08).set_stroke(opacity=0.6)
        fl = label(rf"$\approx {fr['price_fall']:.1f}\times$ cheaper a year", font_size=20, color=COSTC)
        fl.next_to(ax.c2p(2023.5, np.polyval(fit, 2023.5)), DL, buff=0.2)
        ep = F.EPOCH_PRICES
        hc = history_card(2025, r"Ben Cottier et al., \ Epoch AI", rf"the price of a fixed level of ability fell "
                          rf"${ep['lo']}$ to ${ep['hi']}\times$ a year, \ by task; \ GPT-4's level on PhD science: "
                          rf"${ep['gpqa']}\times$", width=4.4, font_size=16, color=COSTC).to_corner(UR, buff=0.2)
        hc.shift(DOWN * 1.0)
        src = cite(r"OpenAI list prices: \ the cheapest model at least as good as GPT-3", corner=DL)
        with self.voiceover(
            "Meanwhile the price of a token has collapsed. <bookmark mark='a'/> Take the cheapest OpenAI model at "
            "least as good as the original GPT-3: sixty dollars per million tokens in 2021, twenty after a cut in "
            f"2022, two for the ChatGPT model in 2023, fifteen cents for GPT-4o mini in 2024. "
            f"<bookmark mark='b'/> That's {fr['price_total']:.0f} times in about three and a half years, "
            f"{fr['price_fall']:.1f} times a year. <bookmark mark='c'/> Epoch AI, tracking many benchmarks, found "
            "the price of a fixed level of ability falling between nine and nine hundred times a year, depending "
            "on the task. Some of that is this part's methods, some is Part 17's hardware, and some is smaller "
            "models trained on more data, as Part 12 described."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(d_, scale=0.5), FadeIn(l_)) for d_, l_ in zip(dots, labs)],
                                  lag_ratio=0.5), run_time=3.0)
            vo.wait_until("b")
            self.play(Create(line), FadeIn(fl))
            vo.wait_until("c")
            self.play(FadeIn(hc))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def devices(self):
        fr = load("frontier")
        devs, models = list(fr["devices"]), list(fr["models"])
        bound = np.asarray(fr["bound"])
        bw = np.asarray(fr["bw"])
        head = label(r"the speed limit of chapter one, \ device by device: \ tokens a second $\le$ bandwidth $\div$ "
                     r"bytes read per token", font_size=20, color=GREY_A).to_edge(UP, buff=0.35)
        # a table: rows devices, columns models
        cw, rh = 2.2, 0.62
        x0, y0 = -3.2, 1.6
        hdr = VGroup(*[label(m.replace(", ", r", \\ "), font_size=17, color=C.NEURAL).move_to([x0 + cw * (j + 0.5), y0, 0])
                       for j, m in enumerate(models)])
        rows = VGroup()
        for i, (d, b_) in enumerate(zip(devs, bw)):
            y = y0 - 0.75 - i * rh
            nm = label(rf"{d} \ (${b_ / 1e9:,.0f}$ GB/s)".replace(",", "{,}"), font_size=18, color=BYTEC)
            nm.move_to([x0 - 0.2, y, 0], aligned_edge=RIGHT)
            cells = VGroup()
            for j in range(len(models)):
                v = bound[i, j]
                t = MathTex(f"{v:,.0f}".replace(",", "{,}") if v >= 1 else (f"{v:.1f}" if v > 0 else r"\text{--}"),
                            font_size=24, color=DECODEC if v >= 20 else (GREY_B if v > 0 else GREY_D))
                cells.add(t.move_to([x0 + cw * (j + 0.5), y, 0]))
            rows.add(VGroup(nm, cells))
        note_ = note(r"--: \ the model doesn't fit in the device's memory; \ bytes per token: \ active weights, \ "
                     r"scales included", font_size=16).to_edge(DOWN, buff=0.75)
        ours = label(rf"our novels model on this computer: \ bound ${fr['ours_bound']:.0f}$, \ measured "
                     rf"${fr['ours_meas']:.0f}$ tokens a second", font_size=20, color=DECODEC).to_edge(DOWN, buff=0.35)
        ap = F.APPLE_ON_DEVICE
        hc = history_card(2025, r"Apple Intelligence, \ on device", rf"about ${ap['params'] / 1e9:.0f}$B parameters in "
                          rf"${ap['bits']}$ bits, \ an ${ap['kv_bits']}$-bit cache shared between layers "
                          rf"(${ap['kv_share']}\%$ smaller)", width=4.4, font_size=15, color=C.NEURAL)
        hc.move_to([-4.3, -1.95, 0])
        cpx = F.RUBIN_CPX
        hc2 = history_card(2025, r"NVIDIA, \ Rubin CPX", rf"a GPU for the long-context work of reading prompts: \ "
                           rf"${cpx['mem'] / 1e9:.0f}$ GB of GDDR7, \ ${cpx['nvfp4'] / 1e15:.0f}$ PFLOP/s in NVFP4",
                           width=4.4, font_size=15, color=PREFILLC).move_to([4.3, -1.95, 0])
        i_m5, i_h = devs.index("Apple M5"), devs.index("NVIDIA H100")
        j_oss = models.index("gpt-oss-20b, MXFP4")
        eff = fr["ours_meas"] / fr["ours_bound"]
        if eff <= 1.0:
            eff_say = f"Our own model on this computer reaches {100 * eff:.0f} percent of its bound."
        else:
            eff_say = (f"Our own model on this computer beats its bound, at {100 * eff:.0f} percent: its weights fit "
                       "in the processor's cache, which is faster than memory.")
        with self.voiceover(
            "Chapter one's speed limit also says who can run these models. <bookmark mark='a'/> Divide a device's "
            "memory bandwidth by the bytes a token reads. <bookmark mark='b'/> A laptop with Apple's M5, at 153 "
            f"gigabytes a second, can write at most {bound[i_m5, j_oss]:.0f} tokens a second with gpt-oss-20b, "
            f"whose experts in MXFP4 make each token read under two gigabytes; an H100, {bound[i_h, j_oss]:,.0f}. "
            "<bookmark mark='c'/> That is why four-bit formats and experts matter for running models at home, "
            "where llama.cpp started in 2023, and why Apple's on-device model, in 2025, was trained for two-bit "
            "weights. " + eff_say + " <bookmark mark='d'/> And the split between prefill and decode is reaching the hardware: in September "
            "2025 NVIDIA announced Rubin CPX, a GPU with cheaper memory and plenty of arithmetic, for the "
            "long-context work of reading prompts, which it said would ship by the end of 2026."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hdr), FadeIn(note_))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in rows], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("b")
            self.play(Indicate(rows[i_m5][1][j_oss], color=DECODEC, scale_factor=1.4))
            vo.wait_until("c")
            self.play(FadeIn(hc), FadeIn(ours))
            vo.wait_until("d")
            self.play(FadeIn(hc2))
        self.wait(0.3)
        self.clear_scene()
