from __future__ import annotations

from videos.psychology.psych26.common import *  # noqa: F403


class Sampling(VoiceoverScene):
    def construct(self):
        self.card()
        self.dbs()
        self.ranges()

    def card(self):
        card = chapter_card(12, r"Where values come from", r"Why is the value curve that shape?",
                            lit={1965: r"Parducci", 2006: r"Stewart, \ Chater \& Brown", 2015: r"Walasek \& Stewart"},
                            part=PART, scale=("mind",), marr=("why",))
        with self.voiceover("Chapter twelve. Where values come from."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def dbs(self):
        d = load("sampling")
        head = heading(r"Decision by sampling")
        A = axes([0, 4], [0, 1], x_length=5.0, y_length=2.0, xticks=[0, 1, 2, 3, 4], yticks=None,
                 xfmt=lambda v: f"10^{{{v:.0f}}}", xlabel=r"amount, \ dollars", center=[-3.5, 1.55, 0],
                 font_size=16)
        hb = d["hist_bins"]
        mids = (hb[:-1] + hb[1:]) / 2
        hc = d["hist_c"] / d["hist_c"].max()
        hd = d["hist_d"] / d["hist_d"].max()
        bc = bars(A.ax, mids - 0.03, hc, GAIN, width=0.06, opacity=0.8)
        bd = bars(A.ax, mids + 0.03, hd, LOSS, width=0.06, opacity=0.6)
        key = legend([(GAIN, rf"credits: \ {num(d['n_credits'])}, \ larger"),
                      (LOSS, rf"debits: \ {num(d['n_debits'])}, \ smaller")], font_size=17).move_to(
            A.ax.c2p(3.2, 0.8))
        B = axes([0, 1000], [-1, 1], x_length=5.0, y_length=2.0, xticks=[0, 500, 1000], yticks=[-1, 0, 1],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", xlabel=r"amount, \ dollars",
                 ylabel=r"value: \ rank among remembered amounts", center=[-3.5, -2.0, 0], font_size=16)
        vg = curve(B.ax, d["x"], d["v_gain"], GAIN, 4)
        vl = curve(B.ax, d["x"], d["v_loss"], LOSS, 4)
        rows = rows_of([
            (r"Stewart, \ Chater and Brown, \ 2006: \ the mind has no scale for money, \ only comparisons with "
             r"amounts it remembers", WHITE),
            (r"an amount's value is its rank in that sample; \ right-skewed amounts make the curve concave", MODEL),
            (r"debits are many and small, \ credits few and large: \ so a loss outranks the same gain", LOSS),
            (rf"in Psyche's illustrative bank account, \ losing \$100 ranks {d['loss_at']:.2f}, \ gaining it "
             rf"{d['gain_at']:.2f}: \ {d['ratio_at']:.1f} times as large", RISKY),
        ], 5.6, 22, 0.3).move_to([3.5, -0.1, 0])
        tag = psyche_tag(r"\texttt{choice.dbs\_value}: \ illustrative, \ lognormal amounts")
        with self.voiceover(
            "Prospect theory describes the value curve; it doesn't say where its shape comes from. "
            "<bookmark mark='a'/> In 2006 Neil Stewart, Nick Chater and Gordon Brown proposed an answer called "
            "decision by sampling. The mind has no internal scale for money, only comparisons. The value of an "
            "amount is its rank among amounts you've met and remember. <bookmark mark='b'/> Amounts in life are "
            "right-skewed: many small ones, few large. Rank among a right-skewed sample, and each extra dollar "
            "moves you up less and less. A concave curve, with no utility function assumed. "
            "<bookmark mark='c'/> They looked at bank accounts, and found debits much more frequent, and typically "
            "smaller, than credits. So a given loss outranks the same gain among the amounts you'd compare it to. "
            "<bookmark mark='d'/> In this illustrative account, losing a hundred dollars ranks at "
            f"{d['loss_at']:.2f} among debits, and gaining it at {d['gain_at']:.2f} among credits: a loss looms "
            f"about {d['ratio_at']:.1f} times as large. Loss aversion, from the statistics of the world."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(A), FadeIn(bc), FadeIn(bd), FadeIn(key))
            self.play(FadeIn(B), Create(vg), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(vl), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def ranges(self):
        head = heading(r"Values move with the range")
        rows = rows_of([
            (r"Parducci, \ 1965: \ range--frequency theory; \ a judgement depends on where a value sits in the range "
             r"and in the ranks of what was seen with it", WHITE),
            (r"Walasek and Stewart, \ 2015: \ let gains range twice as widely as losses, \ and loss aversion "
             r"appears; \ reverse the ranges, \ and it disappears, \ or reverses", LOSS),
            (r"the value curve is partly a summary of the context, \ not a fixed property of the person", MODEL),
            (r"efficient coding: \ a system with limited precision should spend it where values are common; \ the "
             r"same logic as Part 13's eye \ (and Part 58)", NORM),
        ], 12.2, 25, 0.42).move_to([0, -0.1, 0])
        tag = published_tag(r"Parducci (1965); \ Walasek \& Stewart (2015)")
        with self.voiceover(
            "If values are ranks, they should move when the context does. <bookmark mark='a'/> Allen Parducci's "
            "range-frequency theory, from 1965, says just that about judgements in general: a value is judged by "
            "where it sits in the range of what's been seen, and in its rank among them. <bookmark mark='b'/> In "
            "2015 Lukasz Walasek and Stewart offered people fifty-fifty gambles. When the possible gains ranged twice "
            "as widely as the losses, the usual loss aversion appeared. When the ranges were "
            "reversed, it disappeared, and on some measures reversed. <bookmark mark='c'/> So the curve that "
            "prospect theory draws is partly a summary of the context, not a fixed property of the person. "
            "<bookmark mark='d'/> There's a deeper version of this idea: a system with limited precision should "
            "spend it where values are common. It's the same logic as the efficient coding in the eye, in Part 13, "
            "and it returns in Part 58."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
