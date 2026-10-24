from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai19.common import (F, KVC, PART, ROTC, RTNC, hbars, heat, load, bnum, bunit)

KIVIC, FP8C = C.HOT, C.TRUE_P


class KVQuant(VoiceoverScene):
    def construct(self):
        self.card()
        self.channels()
        self.results()

    def card(self):
        card = chapter_card(13, r"The cache in fewer bits", r"How small can the keys and values be?", part=PART)
        with self.voiceover("Chapter thirteen. The cache in fewer bits."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def channels(self):
        k = load("kvquant")
        kv = load("kv")
        km, vm = np.asarray(k["k_map"]), np.asarray(k["v_map"])
        ik = heat(km.T, width=5.0, height=2.6, color=KVC)
        iv = heat(vm.T, width=5.0, height=2.6, color=C.VALUE)
        ik.move_to([-3.4, 0.2, 0])
        iv.move_to([3.4, 0.2, 0])
        bk, bv = SurroundingRectangle(ik, buff=0, color=GREY_C, stroke_width=1), SurroundingRectangle(iv, buff=0,
                                                                                                    color=GREY_C,
                                                                                                    stroke_width=1)
        lk = label(r"keys: \ $|k|$, \ channels down, \ tokens across", font_size=20, color=KVC).next_to(ik, UP, buff=0.15)
        lv = label(r"values: \ $|v|$", font_size=20, color=C.VALUE).next_to(iv, UP, buff=0.15)
        layer, head = int(k["layer"]), int(k["head"])
        tag = note(rf"computed: \ our novels model, \ layer ${layer + 1}$, \ head ${head + 1}$, \ $96$ tokens of a "
                   r"held-out novel").next_to(VGroup(ik, iv), DOWN, buff=0.2).set_x(0)
        # the shown head: each channel's average size over the tokens, largest against median
        ck, cv = km.mean(0), vm.mean(0)
        ratio, vratio = float(ck.max() / np.median(ck)), float(cv.max() / np.median(cv))
        if vratio < 0.6 * ratio:
            chan_say = (f"The keys have outlier channels, whole rows that are large for every token, the largest "
                        f"{ratio:.1f} times the median; the values' largest is only {vratio:.1f} times theirs.")
        else:
            chan_say = (f"Both have channels larger than the rest: the keys' largest is {ratio:.1f} times their median, "
                        f"the values' {vratio:.1f}.")
        cc = kv["curve_llama70"]
        i128 = int(np.argmin(np.abs(np.asarray(kv["ctxs"]) - 131072)))
        big = float(np.asarray(cc)[i128])
        why_ = label(rf"Llama 3.1 70B, \ $128$k tokens: \ ${big / 1e9:.0f}$ GB of cache per conversation, \ "
                     r"in $16$ bits", font_size=22, color=KVC).to_edge(UP, buff=0.35)
        W70 = 2 * F.LLAMA31_70B["params"]
        sizes = hbars([W70 / 1e9, big / 1e9, big / 4e9, big / 8e9],
                      [r"Llama 3.1 70B's weights", r"one conversation's cache, \ $16$ bits", r"the cache in $4$ bits",
                       r"the cache in $2$ bits"], [C.WEIGHTS, KVC, KVC, KIVIC], width=5.0, row_h=0.62, font_size=22,
                      lo=0, hi=W70 / 1e9 * 1.05, fmt_v=lambda v: rf"{v:.0f}\,\text{{GB}}" if v >= 10 else
                      rf"{v:.1f}\,\text{{GB}}")
        sizes.move_to([0.4, 0.3, 0])
        rule = VGroup(label(r"keys: \ a scale per channel", font_size=22, color=KIVIC),
                      label(r"values: \ a scale per token", font_size=22, color=KIVIC)).arrange(DOWN, aligned_edge=LEFT,
                                                                                                buff=0.12)
        rule.to_edge(DOWN, buff=0.45).shift(LEFT * 2.5)
        hc = history_card(2024, r"Zirui Liu et al., \ KIVI", rf"$2$-bit caches: \ ${F.KIVI['batch']}\times$ the batch, "
                          rf"\ ${F.KIVI['tput'][0]}$--${F.KIVI['tput'][1]}\times$ the throughput", width=4.6,
                          font_size=16, color=KIVIC).to_edge(DOWN, buff=0.25).shift(RIGHT * 3.4)
        with self.voiceover(
            "Chapters two and three showed that long conversations are dominated by the cache: one 128-thousand "
            f"token conversation with Llama 3.1 70B keeps {bnum(big):g} {bunit(big)} of keys and values. So round the cache "
            "too. <bookmark mark='a'/> But keys and values are different animals. Here is one head of our model "
            "over a stretch of text: the size of each key and value entry, channel by channel, token by token. "
            "<bookmark mark='b'/> " + chan_say + " <bookmark mark='c'/> So in 2024 Zirui Liu and "
            "colleagues, in KIVI, gave keys a scale per channel and values a scale per token, and stored both in "
            "two bits."
        ) as vo:
            self.play(FadeIn(why_))
            self.play(LaggedStart(*[AnimationGroup(FadeIn(r_.name), GrowFromEdge(r_.bar, LEFT), FadeIn(r_.val))
                                    for r_ in sizes], lag_ratio=0.4), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeOut(sizes))
            self.play(FadeIn(ik), Create(bk), FadeIn(lk), FadeIn(iv), Create(bv), FadeIn(lv), FadeIn(tag))
            vo.wait_until("b")
            self.play(Indicate(ik, color=KVC, scale_factor=1.03))
            vo.wait_until("c")
            self.play(FadeIn(rule), FadeIn(hc))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def results(self):
        k = load("kvquant")
        base = float(k["fp32"])
        L = k["loss"]
        bits = [4, 3, 2]
        series = [("token", r"a scale per token", RTNC), ("kivi", r"KIVI: \ keys per channel", KIVIC),
                  ("rot", r"rotated first \ (Hadamard)", ROTC)]
        hi = max(L[f"{m}_{b}"] - base for m, _, _ in series for b in bits)
        g = VGroup()
        for b in bits:
            vals = [L[f"{m}_{b}"] - base for m, _, _ in series]
            g.add(VGroup(label(rf"${b}$-bit keys and values", font_size=20, color=GREY_A),
                         hbars(vals, [nm for _, nm, _ in series], [c_ for _, _, c_ in series], width=3.6, row_h=0.38,
                               font_size=18, lo=0, hi=hi * 1.1, fmt_v=lambda v: rf"{v:+.3f}"))
                  .arrange(DOWN, aligned_edge=LEFT, buff=0.1))
        g.arrange(DOWN, aligned_edge=LEFT, buff=0.3).scale(1.2).move_to([-1.6, -0.4, 0])
        head = label(r"extra loss on held-out novels \ (nats per token), \ the cache rounded as it is written",
                     font_size=22, color=GREY_A).to_edge(UP, buff=0.35)
        e8, f8 = L["token_8"] - base, L["fp8_8"] - base
        side = VGroup(label(rf"$8$ bits, \ integers: \ ${e8:+.4f}$", font_size=20, color=RTNC),
                      label(rf"$8$ bits, \ FP8 (E4M3): \ ${f8:+.4f}$", font_size=20, color=FP8C),
                      label(rf"Apple's on-device model: \ an ${F.APPLE_ON_DEVICE['kv_bits']}$-bit cache", font_size=20,
                            color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([4.6, 1.2, 0])
        t2, k2, r2 = (L[f"{m}_2"] - base for m in ("token", "kivi", "rot"))
        t3, k3 = L["token_3"] - base, L["kivi_3"] - base
        best2 = min((("kivi", k2), ("rot", r2), ("token", t2)), key=lambda x: x[1])[0]
        if max(abs(e8), abs(f8)) < 0.001:
            say8 = "At eight bits, integer or FP8, nothing measurable is lost."
        else:
            say8 = f"At eight bits, integer or FP8, the loss grows by at most {max(e8, f8):.4f} nats."
        if best2 == "kivi":
            best_say = ("The best here is KIVI's split. Keys need their outlier channels respected, by a scale of "
                        "their own or by a rotation that spreads them.")
        elif best2 == "rot":
            best_say = ("The best here is the rotation. Keys need their outlier channels respected, by a scale of "
                        "their own or by a rotation that spreads them.")
        else:
            best_say = ("Here one scale per token does best: our keys' outlier channels are too mild to need "
                        "anything more.")
        with self.voiceover(
            "On our model, the cache rounded as it is written, and the loss measured on held-out novels. "
            "<bookmark mark='a'/> " + say8 + " " +
            f"At four bits, one scale per token costs {L['token_4'] - base:.3f}. "
            f"<bookmark mark='b'/> At three bits, one scale per token costs {t3:.3f} nats a token; KIVI's split "
            f"{k3:.3f}. <bookmark mark='c'/> At two bits the differences grow: per token {t2:.2f}, rotated "
            f"{r2:.2f}, KIVI {k2:.2f}. " + best_say
        ) as vo:
            self.play(FadeIn(head), FadeIn(side[:2]), FadeIn(side[2]))
            vo.wait_until("a")
            self.play(FadeIn(g[0]))
            vo.wait_until("b")
            self.play(FadeIn(g[1]))
            vo.wait_until("c")
            self.play(FadeIn(g[2]))
        self.wait(0.3)
        self.clear_scene()
