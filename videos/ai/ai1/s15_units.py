from __future__ import annotations

import math

from explainer.ai import *  # noqa: F403
from videos.ai.ai1.common import PART, load

TILE_FONT = "DejaVu Sans"


def tiles(tokens, width=12.6, font_size=20, line_gap=0.44, colors=(C.EMBED, C.MLP, C.KEY)) -> VGroup:
    """A paragraph as its tokens, each on a tile; a token's leading space becomes a gap."""
    g, x, y = VGroup(), 0.0, 0.0
    for k, tok in enumerate(tokens):
        space = tok.startswith(" ")
        t = data_text(tok.strip() or "·", font=TILE_FONT, font_size=font_size, color=WHITE)
        w = t.width + 0.1
        if space and x > 0:
            x += 0.1
        if x + w > width:
            x, y = 0.0, y - line_gap
        r = Rectangle(width=w, height=0.36, stroke_width=0, fill_color=colors[k % 3], fill_opacity=0.45)
        r.move_to([x + w / 2, y, 0])
        t.move_to(r)
        g.add(VGroup(r, t))
        x += w
    return g.move_to(ORIGIN)


class Units(VoiceoverScene):
    def construct(self):
        self.card()
        self.tokens()
        self.table()
        self.frontier()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(14, r"Bits per character, bits per token",
                            r"How do you compare models that cut text differently?", lit=(2019,), part=PART)
        with self.voiceover("Chapter fourteen. Before the final scores, a word about units."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def tokens(self):
        u = load("units")
        lms = load("lms")
        sp = lms["surprise"]
        rows = {r["label"]: r for r in u["rows"]}
        g2, q3 = rows["GPT-2 small"], rows["Qwen3-4B"]
        n = int(u["chars"])
        pc = int(u["paragraph_chars"])
        pa = tiles(sp["GPT-2 small"]["tokens"]).move_to(UP * 1.35)
        pb = tiles(sp["Qwen3-4B"]["tokens"]).move_to(DOWN * 1.55)
        la = label(rf"GPT-2's tokens: \ ${len(sp['GPT-2 small']['tokens'])}$ for these ${pc}$ characters", font_size=26,
                   color=C.NEURAL).next_to(pa, UP, buff=0.2)
        lb = label(rf"Qwen3's tokens: \ ${len(sp['Qwen3-4B']['tokens'])}$", font_size=26, color=C.NEURAL).next_to(pb, UP,
                                                                                                         buff=0.2)
        whole = label(rf"the whole passage, ${n:,}$ characters: \ GPT-2 ${g2['tokens']:,}$ tokens "
                      rf"(${g2['chars_per_token']:.2f}$ characters each), \ Qwen3 ${q3['tokens']:,}$ "
                      rf"(${q3['chars_per_token']:.2f}$)".replace(",", "{,}"), font_size=24, color=GREY_A)
        whole.to_edge(DOWN, buff=0.35)
        head = label(r"Two models, two ways of cutting the same text", font_size=32).to_edge(UP, buff=0.25)
        tag = note(r"computed: \ the models' own tokenizers").to_corner(DR, buff=0.25).shift(UP * 0.5)
        with self.voiceover(
            "Language models don't read letters. Each cuts text into tokens with its own vocabulary. "
            "<bookmark mark='a'/> Here is a paragraph of the Falcon passage as GPT-2 cuts it, "
            f"<bookmark mark='b'/> and as Qwen3 does. <bookmark mark='c'/> Over the whole passage, GPT-2 needs "
            f"{g2['tokens']:,} tokens, {g2['chars_per_token']:.2f} characters each on average; Qwen3, with a "
            f"bigger vocabulary, {q3['tokens']:,}."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(la), LaggedStart(*[FadeIn(t) for t in pa], lag_ratio=0.02), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(lb), LaggedStart(*[FadeIn(t) for t in pb], lag_ratio=0.02), FadeIn(tag), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(whole))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def table(self):
        u = load("units")
        cnt = u["counting"]
        rows_d = [cnt] + [r for r in u["rows"] if r["label"] in ("GPT-2 small", "GPT-2 XL", "Qwen3-0.6B", "Qwen3-4B")]
        n, nb = int(u["chars"]), int(u["bytes"])
        eq = cmath(r"\text{total bits}", r"=", r"N_{\text{tokens}} \times \tfrac{\text{bits}}{\text{token}}", r"=",
                   r"N_{\text{characters}} \times \tfrac{\text{bits}}{\text{character}}", font_size=34)
        eq.to_edge(UP, buff=0.35)
        hdr = [r"model", r"characters per token", r"bits per token", r"perplexity", r"bits per character"]
        cols_x = [-6.5, -1.0, 1.4, 3.6, 6.5]
        table = VGroup()
        head_row = VGroup(*[label(h, font_size=22, color=GREY_B) for h in hdr])
        table.add(head_row)
        for r in rows_d:
            name = (r"counting: \ previous " + rf"${r['label'].split()[2]}$ characters" if r is cnt else r["label"])
            table.add(VGroup(label(name, font_size=24, color=C.COUNTING if r is cnt else C.NEURAL),
                             MathTex(f"{r['chars_per_token']:.2f}", font_size=30),
                             MathTex(f"{r['bits_per_token']:.2f}", font_size=30, color=C.SURPRISE),
                             MathTex(f"{r['ppl_token']:.1f}", font_size=30, color=C.SURPRISE),
                             MathTex(f"{r['bpc']:.2f}", font_size=30, color=C.BITS)))
        for i, row in enumerate(table):
            y = 1.5 - 0.62 * i
            for j, m in enumerate(row):
                if j == 0:
                    m.move_to([cols_x[0], y, 0], aligned_edge=LEFT)
                elif j == len(row) - 1:
                    m.move_to([cols_x[-1], y, 0], aligned_edge=RIGHT)
                else:
                    m.move_to([cols_x[j], y, 0])
        hl = SurroundingRectangle(VGroup(table[1][2], table[1][3]), color=C.SURPRISE, buff=0.1, corner_radius=0.08)
        hl2 = SurroundingRectangle(table[1][4], color=C.BITS, buff=0.1, corner_radius=0.08)
        ppl = definition_card(r"perplexity", r"$2^{\text{bits per token}} = e^{\text{nats per token}}$: \ as unsure as "
                              r"a fair choice among that many tokens", width=6.6, color=C.SURPRISE)
        ppl.to_corner(DL, buff=0.3)
        bpb = label(rf"per byte: \ the passage is ${n:,}$ characters, \ ${nb:,}$ bytes".replace(",", "{,}"),
                    font_size=22, color=GREY_A).to_corner(DR, buff=0.4)
        g2 = next(r for r in rows_d if r["label"] == "GPT-2 small")
        wins_token = cnt["bits_per_token"] < g2["bits_per_token"]
        loses_char = cnt["bpc"] > g2["bpc"]
        verdict = (f"Per token, the counting model looks like the winner: {cnt['bits_per_token']:.2f} bits against "
                   f"GPT-2's {g2['bits_per_token']:.2f}, a perplexity of {cnt['ppl_token']:.1f} against "
                   f"{g2['ppl_token']:.1f}. But its tokens are single characters. Per character, it is "
                   f"{cnt['bpc'] / g2['bpc']:.1f} times worse." if wins_token and loses_char else
                   f"Per token, the counting model scores {cnt['bits_per_token']:.2f} bits and GPT-2 "
                   f"{g2['bits_per_token']:.2f}; per character, {cnt['bpc']:.2f} and {g2['bpc']:.2f}.")
        with self.voiceover(
            "A model's loss is reported per token, so its size depends on how much text a token holds. "
            "<bookmark mark='a'/> What matters is the total: tokens times bits per token, which is characters times "
            "bits per character. <bookmark mark='b'/> Here are our models on the passage; for the counting model, "
            f"every token is a character. <bookmark mark='c'/> {verdict} "
            "<bookmark mark='d'/> Perplexity, two to the bits per token, inherits the same problem: it says how many "
            "equally likely tokens a model is choosing among, and tokens differ. <bookmark mark='e'/> So compare "
            "per character, or per byte of the file. That's why the scoreboard counts bits per character."
        ) as vo:
            self.play(FadeIn(eq))
            vo.wait_until("a")
            self.play(Indicate(eq, color=C.BITS, scale_factor=1.03))
            vo.wait_until("b")
            self.play(FadeIn(table[0]), LaggedStart(*[FadeIn(r) for r in table[1:]], lag_ratio=0.25), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(hl))
            self.play(Create(hl2))
            vo.wait_until("d")
            self.play(FadeIn(ppl, shift=UP * 0.2))
            vo.wait_until("e")
            self.play(FadeIn(bpb))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def frontier(self):
        head = label(r"Compression, and what models can do", font_size=34).to_edge(UP, buff=0.4)
        rows = VGroup(
            label(r"$31$ public language models, \ $12$ benchmarks", font_size=28),
            label(r"each model's bits per character on freshly collected text, \ against its average benchmark score",
                  font_size=26,
                  color=GREY_A),
            label(r"almost a straight line: \ Pearson correlation $-0.93$", font_size=30, color=C.BITS),
            label(r"``bits per token are not directly comparable'' \ \ --- so they use bits per character", font_size=24,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.35).move_to(UP * 0.4)
        # the shape of their finding: lower bits, higher scores (schematic)
        ax = Axes(x_range=[0, 1, 1], y_range=[0, 1, 1], x_length=3.6, y_length=2.0, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).to_corner(DR, buff=0.5)
        pts = [(0.15, 0.85), (0.25, 0.78), (0.32, 0.66), (0.45, 0.6), (0.52, 0.45), (0.63, 0.4), (0.75, 0.25),
               (0.85, 0.18)]
        dots = VGroup(*[Dot(ax.c2p(x, y), radius=0.05, color=C.NEURAL) for x, y in pts])
        fit = Line(ax.c2p(0.08, 0.92), ax.c2p(0.92, 0.1), color=C.BITS, stroke_width=2.5)
        axl = VGroup(label(r"bits per character", font_size=18, color=GREY_B).next_to(ax, DOWN, buff=0.1),
                     label(r"benchmark score", font_size=18, color=GREY_B).next_to(ax, LEFT, buff=0.1).rotate(PI / 2))
        sch = note(r"schematic", font_size=18).next_to(ax, UP, buff=0.05)
        src = cite(r"Y.~Huang, J.~Zhang, Z.~Shan \& J.~He, \textit{Compression Represents Intelligence Linearly} "
                   r"(COLM 2024)")
        with self.voiceover(
            "The field measures it this way too. In 2024, researchers at the Hong Kong University of Science and "
            "Technology and Tencent took thirty-one public language models, <bookmark mark='a'/> measured how well "
            "each compresses freshly collected web pages, code and papers, in bits per character, since bits per "
            "token aren't comparable, <bookmark mark='b'/> and set that against their average score on twelve "
            "benchmarks of knowledge, coding and mathematics. <bookmark mark='c'/> The points fall almost on a "
            "line, with a correlation of minus 0.93. The better a model compresses, the more it can do."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]), FadeIn(rows[3]))
            vo.wait_until("b")
            self.play(Create(ax), FadeIn(axl), FadeIn(sch), LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.1))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), Create(fit))
        self.wait(0.3)
        self.clear_scene()
