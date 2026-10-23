from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai31.common import CLEAN, MONO, PART, PRIVATE, SECRET, band, curve, load, tagline, wrap_data

TRAIN, HELD = SECRET, CLEAN  # text the model trained on, text it never saw


class Privacy(VoiceoverScene):
    def construct(self):
        self.card()
        self.history()
        self.definition()
        self.rates()
        self.duplicates()
        self.dp()
        self.canary()

    def card(self):
        card = chapter_card(12, r"What a model remembers", r"Can a model give away its training data?",
                            lit=(2016, 2023), part=PART)
        with self.voiceover("Chapter twelve. What a model remembers."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def history(self):
        cards = VGroup(
            history_card(2021, r"Carlini et al., \ \textit{Extracting Training Data from Large Language Models}",
                         r"from GPT-2's own samples: \ $604$ memorized training examples among $1{,}800$ candidates, \ "
                         r"names, phone numbers and e-mail addresses among them", width=6.3, color=SECRET, font_size=19),
            history_card(2023, r"Carlini et al., \ \textit{Quantifying Memorization}", r"memorization grows log-linearly "
                         r"with model size, \ with how often a text is repeated, \ and with the length of the prompt; \ "
                         r"GPT-J memorized at least $1\%$ of its training set", width=6.3, color=SECRET, font_size=19),
            history_card(2023, r"Nasr et al., \ ChatGPT", r"asked to repeat one word forever, \ it eventually "
                         r"diverged into memorized training text: \ over $10{,}000$ examples for $\$200$ of queries",
                         width=6.3, color=SECRET, font_size=19),
            history_card(2017, r"Shokri et al., \ membership inference", r"no copy needed: \ from a model's outputs "
                         r"alone, \ guess whether a given record was in its training set", width=6.3, color=PRIVATE,
                         font_size=19),
        ).arrange_in_grid(rows=2, cols=2, buff=0.3).move_to(DOWN * 0.3)
        head = label(r"Models remember", font_size=36).to_edge(UP, buff=0.35)
        with self.voiceover(
            "A model trained on text keeps some of that text. In 2021 Nicholas Carlini and colleagues sampled from "
            "GPT-2 and searched the samples for memorized training data. <bookmark mark='a'/> Of eighteen hundred "
            "candidates, six hundred and four were verbatim training text, some with real names, phone numbers and "
            "e-mail addresses. <bookmark mark='b'/> Two years later they showed memorization growing with the size of "
            "the model, with repetition, and with the length of the prompt. <bookmark mark='c'/> And in 2023, asked to repeat a single word forever, ChatGPT eventually "
            "drifted into memorized training text: over ten thousand examples, for two hundred dollars of queries. "
            "<bookmark mark='d'/> And a model can betray its training data without quoting it: in 2017 Reza Shokri "
            "and colleagues showed how to tell, from a model's outputs alone, whether a given record was in its "
            "training set."
        ) as vo:
            full = [c_.copy() for c_ in cards]
            for c_ in cards[1:]:
                c_.fade(0.78)
            self.play(FadeIn(head), FadeIn(cards))
            vo.wait_until("a")
            self.play(Indicate(cards[0], color=SECRET, scale_factor=1.03))
            for k, m in enumerate("bcd", start=1):
                vo.wait_until(m)
                self.play(Transform(cards[k], full[k]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def definition(self):
        d = load("extraction")
        defn = definition_card(r"extractable \ (Carlini et al., 2023)", r"a training text $s$ is extractable with $k$ "
                               r"tokens of context if, \ prompted with the $k$ tokens before it, \ greedy decoding "
                               r"writes exactly $s$", color=SECRET, width=10.4, font_size=24).to_edge(UP, buff=0.35)
        rows = [
            cmath(r"\hat s_j", r"=", r"\arg\max_x\, p(x \mid \text{prefix}, \hat s_{<j})", font_size=34),
            cmath(r"\hat s_{<j} = s_{<j}", r"\Rightarrow", r"\hat s_j = \arg\max_x\, p(x \mid \text{prefix}, s_{<j})",
                  font_size=34),
            cmath(r"\hat s = s", r"\iff", r"\arg\max_x\, p(x \mid \text{prefix}, s_{<j}) = s_j \ \ \text{for every } j",
                  font_size=34),
        ]
        rows[2][2].set_color(SECRET)
        whys = [why(r"greedy decoding: \ always the top token"), why(r"while it matches, \ it reads the true text"),
                why(r"by induction on $j$: \ one forward pass over the true text decides it")]
        step = ladder(self, rows, whys, keep=3, top=1.2, x=-1.6, buff=0.55, edge=6.9)
        toks = VGroup(*[Square(0.34, stroke_width=1.2, stroke_color=GREY_C if k < 10 else TRAIN,
                               fill_color=GREY_D if k < 10 else TRAIN, fill_opacity=0.5 if k < 10 else 0.35)
                        for k in range(18)]).arrange(RIGHT, buff=0.06).move_to([0, -3.0, 0])
        tl1 = label(r"$k$ tokens of prompt", font_size=20, color=GREY_A).next_to(toks[:10], UP, buff=0.12)
        tl2 = label(r"$s$: \ the text that followed", font_size=20, color=TRAIN).next_to(toks[10:], UP, buff=0.12)
        strip = VGroup(toks, tl1, tl2)
        with self.voiceover(
            "We can test our own model. First, a precise definition. <bookmark mark='a'/> A training text is "
            "extractable with k tokens of context if, prompted with the k tokens that came before it, the model's "
            "greedy decoding writes it out exactly. <bookmark mark='b'/> Checking that seems to need generation, "
            "token by token. It doesn't. Greedy decoding always takes the top token. <bookmark mark='c'/> As long "
            "as what it has written matches the text, the model is reading the true text, so its next choice is the "
            "top token given the true prefix. <bookmark mark='d'/> By induction, it reproduces the whole text exactly "
            "when the top token is right at every position: a single forward pass over the true text decides it, "
            f"for every prefix length at once. That made it cheap to test {d['n_win']:,} passages of each kind."
        ) as vo:
            self.play(FadeIn(defn, shift=DOWN * 0.15), FadeIn(strip))
            vo.wait_until("b")
            step(0)
            vo.wait_until("c")
            step(1)
            vo.wait_until("d")
            step(2)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rates(self):
        d = load("extraction")
        ks = np.asarray(d["prefixes"], float)
        tr, va = d["train"], d["valid"]
        top = max(max(tr["hi"]), max(va["hi"]), 0.01)
        ytop = float(np.ceil(top * 100 / 5) * 5) / 100 if top > 0.05 else float(np.ceil(top * 100)) / 100
        g = axes([np.log2(ks[0]), np.log2(ks[-1])], [0, ytop], x_length=6.2, y_length=3.6,
                 xlabel=r"tokens of prompt \ (log scale)",
                 ylabel=rf"next ${d['cont']}$ tokens reproduced exactly",
                 xticks=[v for v in np.log2(ks) if abs(v - np.log2(ks[-1])) < 1e-9 or v < np.log2(ks[-1]) - 0.5],
                 yticks=[0, ytop / 2, ytop], xfmt=lambda v: f"{int(round(2 ** v))}",
                 yfmt=lambda v: rf"{v * 100:.1f}\%" if ytop < 0.1 else rf"{v * 100:.0f}\%", center=[-3.2, -0.3, 0])
        x = np.log2(ks)
        bt = band(g.ax, x, tr["lo"], tr["hi"], TRAIN)
        ct = curve(g.ax, x, tr["rate"], TRAIN, 4)
        bv = band(g.ax, x, va["lo"], va["hi"], HELD)
        cv = curve(g.ax, x, va["rate"], HELD, 4)
        lg = legend([(TRAIN, r"text it trained on"), (HELD, r"held-out text, \ same books")], font_size=20)
        lg.move_to(g.ax.c2p(np.log2(ks[-1]), ytop), aligned_edge=UR)
        ex = d["examples"]["train"]
        k64 = list(d["prefixes"]).index(64)
        pre = wrap_data("..." + ex["prefix"], chars=34, font_size=18, color=GREY_B, max_lines=3)
        if ex["extracted"]:
            lab = label(r"a training passage, \ prompt in grey; \ the model's greedy continuation:", font_size=18,
                        color=GREY_A)
            body = VGroup(wrap_data(ex["truth"], chars=34, font_size=18, color=TRAIN, max_lines=4))
        else:
            lab = label(rf"the training passage greedy decoding followed longest: \ ${ex['lead']}$ tokens",
                        font_size=18, color=GREY_A)
            body = VGroup(label(r"the text:", font_size=17, color=GREY_A),
                          wrap_data(ex["truth"], chars=34, font_size=18, color=WHITE, max_lines=3),
                          label(r"the model wrote:", font_size=17, color=GREY_A),
                          wrap_data(ex["greedy"], chars=34, font_size=18, color=TRAIN, max_lines=3))
            body.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        exg = VGroup(lab, pre, body).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.6, 0.3, 0])
        if exg.width > 6.4:
            exg.width = 6.4
        tag = tagline(rf"computed: \ our model, \ ${d['n_win']}$ passages of each; \ band: $95\%$ interval")
        rt, rv = tr["rate"][k64], va["rate"][k64]
        lt_, lv_ = tr["lead"][k64], va["lead"][k64]
        if max(tr["rate"]) == 0 and max(va["rate"]) == 0:
            said = (f"With 64 tokens of prompt, or any other length we tried, it reproduces the next {d['cont']} "
                    f"tokens exactly for none of the {d['n_win']} training passages, and none of the held-out ones. "
                    f"Its greedy continuation follows the true text for {lt_:.1f} tokens on average before it goes "
                    f"its own way, and for {lv_:.1f} on held-out text. At this size, our model memorizes nothing we "
                    "can extract this way.")
        elif rt > 2 * max(rv, 0.001):
            said = (f"With 64 tokens of prompt, our model reproduces the next {d['cont']} tokens exactly for "
                    f"{rt * 100:.1f} percent of passages it trained on, and {rv * 100:.1f} percent of held-out ones. "
                    "Held-out passages it can only reproduce when the text is predictable from the prompt; the "
                    "difference is memory.")
        else:
            said = (f"With 64 tokens of prompt, it reproduces the next {d['cont']} tokens exactly for "
                    f"{rt * 100:.1f} percent of training passages and {rv * 100:.1f} percent of held-out ones: at this "
                    "size, our model memorizes very little verbatim.")
        if tr["rate"][-1] > tr["rate"][0] + 0.005:
            longer = "Longer prompts help it remember."
        else:
            longer = "Larger models, trained on their text more often, are another matter."
        with self.voiceover(
            f"Our model saw its training text about {d['epochs']:.1f} times. Prompt it with the start of a passage, "
            f"and ask whether it writes the next {d['cont']} tokens exactly. <bookmark mark='a'/> For passages it "
            "trained on, <bookmark mark='b'/> and for held-out passages from the same books. <bookmark mark='c'/> "
            + said + " <bookmark mark='d'/> " + longer
        ) as vo:
            self.play(FadeIn(g), FadeIn(tag), FadeIn(exg))
            vo.wait_until("a")
            self.play(FadeIn(bt), Create(ct), FadeIn(lg[0]))
            vo.wait_until("b")
            self.play(FadeIn(bv), Create(cv), FadeIn(lg[1]))
            vo.wait_until("c")
            self.play(Indicate(exg[-1], color=TRAIN, scale_factor=1.02))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def duplicates(self):
        d = load("extraction")
        rates, ns, cis = d["dup_rate"], d["dup_n"], d["dup_ci"]
        keep = [k for k, n in enumerate(ns) if n >= 20]
        names = [r"once", r"$2$--$4$ times", r"$5$ or more"]
        top = max(0.02, max(cis[k][1] for k in keep) if keep else 0.02)
        g = axes([0, 3], [0, top * 1.1], x_length=5.2, y_length=3.4, ylabel=r"reproduced exactly \ ($64$-token prompt)",
                 yticks=[0, round(top / 2, 2), round(top, 2)], yfmt=lambda v: rf"{v * 100:.0f}\%", center=[-3.4, -0.4, 0])
        bars = VGroup()
        for k in keep:
            p0, p1 = g.ax.c2p(k + 0.2, 0), g.ax.c2p(k + 0.8, max(rates[k], 0.0005))
            bars.add(VGroup(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=TRAIN,
                                      fill_opacity=0.85).move_to((p0 + p1) / 2),
                            Line(g.ax.c2p(k + 0.5, cis[k][0]), g.ax.c2p(k + 0.5, cis[k][1]), color=WHITE, stroke_width=2),
                            label(names[k], font_size=18, color=GREY_A).next_to(g.ax.c2p(k + 0.5, 0), DOWN, buff=0.12)))
        xl = label(r"how often the continuation occurs in the training text", font_size=18, color=GREY_A)
        xl.next_to(g.ax, DOWN, buff=0.55)
        lt, lv = np.asarray(d["train"]["win_loss"]), np.asarray(d["valid"]["win_loss"])
        lo, hi = float(min(lt.min(), lv.min())), float(max(lt.max(), lv.max()))
        h = axes([lo, hi], [0, 1], x_length=5.2, y_length=2.6, xlabel=r"a passage's loss \ (nats per token)",
                 xticks=[round(lo, 1), round(hi, 1)], center=[3.4, 0.2, 0])
        bins = np.linspace(lo, hi, 36)
        m = max(np.histogram(lt, bins, density=True)[0].max(), np.histogram(lv, bins, density=True)[0].max())
        from videos.ai.ai31.common import hist_bars
        ht = hist_bars(h.ax, lt, bins, TRAIN, opacity=0.6, scale=0.95 / m)
        hv = hist_bars(h.ax, lv, bins, HELD, opacity=0.6, scale=0.95 / m)
        auc = d["auc"]
        al = label(rf"telling them apart by loss alone: \ AUC ${auc:.2f}$ \ ($0.5$ = chance)", font_size=20,
                   color=GREY_A).next_to(h, DOWN, buff=0.25)
        hlg = legend([(TRAIN, r"passages it trained on"), (HELD, r"held-out passages")], font_size=18)
        hlg.next_to(h, UP, buff=0.12)
        tag = tagline(r"computed")
        if keep and max(rates[k] for k in keep) == 0:
            dup_said = (f"Even stretches that occur five or more times are reproduced in none of {ns[keep[-1]]} "
                        "tries: for a model this small, repetition is not yet enough.")
        elif len(keep) >= 2 and rates[keep[-1]] > rates[keep[0]] + 0.01:
            dup_said = (f"Text that appears once in the training data is reproduced {rates[keep[0]] * 100:.1f} percent "
                        f"of the time; text repeated five or more times, {rates[keep[-1]] * 100:.0f} percent. "
                        "Repetition is what a model memorizes, which is why training sets are deduplicated.")
        else:
            dup_said = "Here repetition makes little difference."
        with self.voiceover(
            "Two more measurements. <bookmark mark='a'/> Group the training text by how many times each stretch "
            f"occurs in it. {dup_said} <bookmark mark='b'/> And even without exact copies, the model knows its "
            "training text better: passages it trained on have lower loss than held-out ones. An attacker who sees "
            f"only the loss can guess which passages were in the training set with an AUC of {auc:.2f}, where half "
            "is guessing. That is a membership-inference attack, and it works on every model that fits its training "
            "data better than the world."
        ) as vo:
            self.play(FadeIn(g), FadeIn(xl), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(h), FadeIn(hv), FadeIn(ht), FadeIn(al), FadeIn(hlg))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def dp(self):
        defn = definition_card(r"$(\varepsilon, \delta)$-differential privacy \ (Dwork et al., 2006)",
                               r"for any two training sets $D, D'$ that differ in one example, \ and any set of outcomes "
                               r"$S$: \ \ $P[M(D) \in S] \le e^{\varepsilon}\, P[M(D') \in S] + \delta$", color=PRIVATE,
                               width=11.0, font_size=24).to_edge(UP, buff=0.35)
        rows = [
            cmath(r"g_i", r"\leftarrow", r"g_i \cdot \min\!\big(1, C / \|g_i\|\big)", font_size=34),
            cmath(r"\tilde g", r"=", r"\frac1B\Big(\sum_i g_i + \mathcal N(0, \sigma^2 C^2 I)\Big)", font_size=34),
            cmath(r"\varepsilon", r"=", r"\text{accountant}(q, \sigma, T, \delta)", font_size=34),
        ]
        rows[1][2].set_color(PRIVATE)
        whys = [why(r"clip each example's gradient: \ no one example can push hard"),
                why(r"add Gaussian noise scaled to the clip"),
                why(r"$q$: \ batch share, \ $T$: \ steps; \ Abadi et al.\ (2016)")]
        step = ladder(self, rows, whys, keep=3, top=1.0, x=-1.8, buff=0.55, edge=6.9)
        cards = VGroup(
            history_card(2016, r"Abadi et al.", r"MNIST at $97\%$ with $\varepsilon = 8$", width=4.5, color=PRIVATE,
                         font_size=19),
            history_card(2025, r"VaultGemma \ (Google, September)", r"a $1$B model pretrained with DP-SGD, \ "
                         r"$\varepsilon \le 2$ per $1{,}024$-token sequence; \ no detectable memorization", width=6.4,
                         color=PRIVATE, font_size=19),
        ).arrange(RIGHT, buff=0.3).to_edge(DOWN, buff=0.3)
        dset = VGroup(*[Square(0.3, stroke_width=0, fill_color=GREY_B, fill_opacity=0.8) for _ in range(9)])
        dset.arrange(RIGHT, buff=0.06)
        dset[4].set_fill(SECRET, 1.0)
        dset2 = dset.copy()
        dset2[4].set_fill(BACKGROUND, 1.0).set_stroke(GREY_C, 1.0)
        rowsD = VGroup(VGroup(label(r"$D$", font_size=26), dset).arrange(RIGHT, buff=0.25),
                       VGroup(label(r"$D'$", font_size=26), dset2).arrange(RIGHT, buff=0.25)).arrange(DOWN, buff=0.5)
        rowsD.move_to([-3.6, -1.4, 0])
        hx = axes([-3, 3], [0, 1.1], x_length=3.6, y_length=1.8, xlabel=r"what the trained model does",
                  center=[3.2, -1.3, 0])
        xx = np.linspace(-3, 3, 120)
        c1_ = curve(hx.ax, xx, np.exp(-0.5 * xx ** 2), SECRET, 3)
        c2_ = curve(hx.ax, xx, np.exp(-0.5 * (xx - 0.25) ** 2), GREY_B, 3)
        arrD = Arrow(rowsD.get_right(), hx.get_left(), buff=0.3, color=GREY_B, stroke_width=2.5)
        capD = label(r"one example apart \\ $\Rightarrow$ \ nearly the same model", font_size=20, color=PRIVATE)
        capD.next_to(arrD, UP, buff=0.12)
        pic = VGroup(rowsD, hx, c1_, c2_, arrD, capD, note(r"schematic").next_to(hx, DOWN, buff=0.1))
        cards.to_edge(UP, buff=0.35)
        with self.voiceover(
            "There is a defense with a guarantee: differential privacy, defined by Cynthia Dwork and colleagues in "
            "2006. A training algorithm is private if changing any single training example changes the probability "
            "of any outcome by at most a factor of e to the epsilon, plus a small delta. <bookmark mark='a'/> In 2016 Martin Abadi and colleagues made "
            "deep learning private. Clip each example's gradient to a fixed norm, so that no single example can push "
            "the model far; <bookmark mark='b'/> add Gaussian noise scaled to that clip; <bookmark mark='c'/> and keep "
            "an account of how much privacy every step spends. <bookmark mark='d'/> They trained MNIST to ninety-seven "
            "percent at epsilon eight. In 2025 Google trained VaultGemma, a billion-parameter language model, this way "
            "from scratch, at epsilon two per sequence, and found no detectable memorization."
        ) as vo:
            self.play(FadeIn(defn, shift=DOWN * 0.15), FadeIn(pic))
            vo.wait_until("a")
            self.play(FadeOut(pic))
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            self.play(FadeOut(defn), LaggedStart(*[FadeIn(c_, shift=DOWN * 0.15) for c_ in cards], lag_ratio=0.4))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def canary(self):
        d = load("dpsgd")
        plain = {r["reps"]: r for r in d["plain"]}
        dp = d["dp"]
        reps = sorted(plain)
        secret = data_text(d["secret"], font=MONO, font_size=26, color=SECRET)
        sbox = SurroundingRectangle(secret, color=SECRET, buff=0.18, corner_radius=0.1)
        top = VGroup(sbox, secret).to_edge(UP, buff=0.45)
        tl = label(r"planted in a tiny character model's training text \ ($400{,}000$ characters of the novels)",
                   font_size=20, color=GREY_A).next_to(top, DOWN, buff=0.12)
        g = axes([0, len(reps) + 1], [0, 21], x_length=7.4, y_length=3.4, ylabel=r"exposure \ (bits)",
                 yticks=[0, 10, 20], center=[-2.4, -1.2, 0])
        bars, labs, vals = VGroup(), VGroup(), VGroup()
        allr = [(plain[k], rf"SGD, \\ planted ${k}\times$", SECRET) for k in reps] + \
               [(dp, rf"DP-SGD, \\ planted ${dp['reps']}\times$", PRIVATE)]
        for k, (r, t, col) in enumerate(allr):
            p0, p1 = g.ax.c2p(k + 0.2, 0), g.ax.c2p(k + 0.8, max(r["exposure"], 0.05))
            bars.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=col,
                               fill_opacity=0.85).move_to((p0 + p1) / 2))
            labs.add(label(t, font_size=17, color=col).next_to(g.ax.c2p(k + 0.5, 0), DOWN, buff=0.12))
            vals.add(MathTex(rf"\#{r['rank']:,}".replace(",", "{,}"), font_size=18, color=col).next_to(bars[-1], UP,
                                                                                                    buff=0.06))
        cap = MathTex(r"\text{exposure} = \log_2 10^6 - \log_2 \text{rank}", font_size=30).move_to([4.2, -0.2, 0])
        capl = label(r"rank: \ where the true number falls \\ among all $10^6$ six-digit numbers, \\ by the model's "
                     r"probability", font_size=18, color=GREY_A).next_to(cap, DOWN, buff=0.2)
        cost = label(rf"held-out bits per character: \ SGD ${plain[reps[-1]]['held']:.2f}$, \ DP-SGD ${dp['held']:.2f}$",
                     font_size=20, color=GREY_A).next_to(capl, DOWN, buff=0.3)
        epsl = label(rf"DP-SGD: \ $\varepsilon = {dp['eps']:.1f}$, \ $\delta = 10^{{-5}}$", font_size=22,
                     color=PRIVATE).next_to(cost, DOWN, buff=0.2)
        tag = tagline(r"computed: \ a $10$-character context, \ $160$ hidden units")
        from videos.ai.ai31.compute import _dp_text

        text = _dp_text()[0]
        cut = text.find(" ", 5000 + 150)
        snip = VGroup(wrap_data("..." + text[5000:cut], chars=60, font_size=20, color=GREY_B, max_lines=3),
                      wrap_data(d["secret"], chars=60, font_size=20, color=SECRET, max_lines=1),
                      wrap_data(text[cut + 1:cut + 150] + "...", chars=60, font_size=20, color=GREY_B, max_lines=3))
        snip.arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to(DOWN * 0.9)
        k1 = reps[1]
        p1_, pmax = plain[k1], plain[reps[-1]]
        if pmax["exposure"] > 15:
            plain_said = (f"Planted {reps[-1]} times, ordinary training ranks it number {pmax['rank']:,} of a million: "
                          "the model gives the secret away.")
        elif pmax["exposure"] > 5:
            plain_said = (f"Planted {reps[-1]} times, ordinary training ranks it number {pmax['rank']:,} of a million, "
                          f"an exposure of {pmax['exposure']:.0f} bits: far above chance.")
        else:
            plain_said = (f"Planted {reps[-1]} times, ordinary training ranks it {pmax['rank']:,}: this model hardly "
                          "memorizes it.")
        if dp["exposure"] < 4:
            dp_said = f"it ranks {dp['rank']:,}, indistinguishable from a number never seen."
        else:
            dp_said = (f"it ranks {dp['rank']:,}: exposure falls from {pmax['exposure']:.0f} bits to "
                       f"{dp['exposure']:.0f}. Not to nothing: epsilon bounds what one example can do, and "
                       f"{dp['reps']} copies of a secret are {dp['reps']} examples.")
        with self.voiceover(
            "We can watch privacy work on a model small enough to train many times. Plant a secret, the secret number "
            "is two eight one nine seven four, in four hundred thousand characters of the novels, and train a tiny "
            "character model on it. <bookmark mark='a'/> Then ask the trained model how likely each of the million "
            "six-digit numbers is after the words the secret number is. The rank of the true number gives its "
            "exposure: twenty bits means it ranks first; zero means it is lost in the crowd. <bookmark mark='b'/> "
            f"Never planted, it ranks {plain[0]['rank']:,}: nothing. Planted once: {p1_['rank']:,}. " + plain_said +
            f" <bookmark mark='c'/> Train the same model with DP-SGD, at epsilon {dp['eps']:.1f}, the secret planted "
            f"{dp['reps']} times: " + dp_said + f" The price is accuracy: {dp['held']:.2f} bits per character on "
            f"held-out text, against {pmax['held']:.2f}."
        ) as vo:
            self.play(FadeIn(top), FadeIn(tl), FadeIn(tag), FadeIn(snip))
            vo.wait_until("a")
            self.play(FadeOut(snip))
            self.play(FadeIn(g), Write(cap), FadeIn(capl))
            vo.wait_until("b")
            for k in range(len(reps)):
                self.play(GrowFromEdge(bars[k], DOWN), FadeIn(labs[k]), FadeIn(vals[k]), run_time=0.8)
            vo.wait_until("c")
            self.play(GrowFromEdge(bars[-1], DOWN), FadeIn(labs[-1]), FadeIn(vals[-1]), FadeIn(cost), FadeIn(epsl))
        self.wait(0.4)
        self.clear_scene()
