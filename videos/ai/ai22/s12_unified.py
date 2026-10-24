from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai22.common import HIST, LETTERS, PANEL, PART, PATCH, TXT, fmt_int, glyph_sheet, gray_image, load, mean_band

FAMS = ("sans", "serif", "mono")
UNI_C = "#5CD0B3"


def sequence_picture() -> VGroup:
    """The three kinds of training sequence, as rows of tokens: text (blue squares) and pictures (gold blocks)."""
    def tok(word, color=TXT):
        t = data_text(word, font="DejaVu Sans Mono", font_size=16, color=color)
        box = RoundedRectangle(width=max(t.width + 0.18, 0.5), height=0.4, corner_radius=0.06, stroke_color=color,
                               stroke_width=1.5, fill_color=color, fill_opacity=0.15)
        return VGroup(box, t.move_to(box))

    def pic(noisy=False):
        g = VGroup(*[Square(0.13, stroke_width=0.5, stroke_color=PATCH, fill_color=PATCH,
                            fill_opacity=0.15 if noisy else 0.55) for _ in range(25)]).arrange_in_grid(5, 5, buff=0)
        return g

    rows = VGroup(
        VGroup(tok("<serif>"), tok("<R>"), pic(True)),
        VGroup(pic(), tok("<R>"), tok("<serif>")),
        VGroup(pic(), tok("<bold>"), pic(True)),
    )
    for r in rows:
        r.arrange(RIGHT, buff=0.12)
    names = VGroup(label(r"draw", font_size=20, color=UNI_C), label(r"name", font_size=20, color=UNI_C),
                   label(r"edit", font_size=20, color=UNI_C))
    for n_, r in zip(names, rows):
        n_.next_to(r, LEFT, buff=0.3)
    g = VGroup(*[VGroup(n_, r) for n_, r in zip(names, rows)]).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
    return g


def mask_picture(cell=0.12) -> VGroup:
    """Transfusion's attention: causal over the sequence, but every patch of a picture sees every other patch."""
    blocks = [("t", 2), ("i", 6), ("t", 2), ("i", 6)]  # a schematic sequence (pictures shortened to 6 patches)
    kind, bid = [], []
    pos = 0
    for k, (t, n) in enumerate(blocks):
        kind += [t] * n
        bid += [k if t == "i" else 100 + pos + j for j in range(n)]
        pos += n
    n = len(kind)
    g = VGroup()
    for i in range(n):
        for j in range(n):
            ok = j <= i or bid[i] == bid[j]
            if ok:
                col = PATCH if kind[j] == "i" else TXT
                extra = bid[i] == bid[j] and j > i
                g.add(Square(cell, stroke_width=0, fill_color=C.ATTN if extra else col, fill_opacity=0.8 if extra else 0.45)
                      .move_to([j * cell, -i * cell, 0]))
    frame = Square(n * cell, stroke_color=GREY_C, stroke_width=1.5).move_to([(n - 1) * cell / 2, -(n - 1) * cell / 2, 0])
    return VGroup(frame, g)


class Unified(VoiceoverScene):
    def construct(self):
        self.card()
        self.history()
        self.ours()
        self.training()
        self.edits()
        self.frontier()

    def card(self):
        card = chapter_card(11, r"One model for words and pictures", r"Can one network read, draw and edit?", part=PART)
        with self.voiceover("Chapter eleven. One model for words and pictures."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def history(self):
        head = label(r"Unified models", font_size=36).to_edge(UP, buff=0.35)
        cards = VGroup(
            history_card(r"May 2024", r"Chameleon \ (Meta)", r"pictures as discrete tokens in the same vocabulary: \ "
                         r"one next-token loss for everything", color=HIST, width=4.3, font_size=23),
            history_card(r"Aug 2024", r"Transfusion \ (Zhou et al., Meta)", r"one transformer, \ two losses: \ next "
                         r"token for text, \ diffusion for picture patches; \ $7$ billion weights, \ $2$ trillion tokens",
                         color=HIST, width=4.3, font_size=23),
            history_card(r"Oct 2024", r"Janus \ (DeepSeek)", r"one transformer, \ but separate eyes: \ SigLIP features "
                         r"to read, \ VQ tokens to draw", color=HIST, width=4.3, font_size=23),
            history_card(r"May 2025", r"BAGEL \ (ByteDance Seed)", r"two transformer experts, \ for understanding and "
                         r"for drawing, \ sharing attention: \ $7$ of $14$ billion weights active; \ editing emerged",
                         color=HIST, width=4.3, font_size=23),
        ).arrange_in_grid(rows=2, cols=2, buff=(0.25, 0.25)).next_to(head, DOWN, buff=0.35)
        if cards.height > 5.8:
            cards.height = 5.8
            cards.next_to(head, DOWN, buff=0.35)
        with self.voiceover(
            "So far, one model reads pictures and another draws them. Can one network do both? <bookmark mark='a'/> "
            "Meta's Chameleon, in 2024, made pictures into tokens in the same vocabulary as words, and trained one "
            "next-token loss on everything. <bookmark mark='b'/> Transfusion, from Chunting Zhou and colleagues at "
            "Meta, kept the pictures continuous: one transformer with two losses, next-token prediction on the text "
            "and diffusion on the picture's patches. At seven billion weights, it scaled better than turning pictures "
            "into discrete tokens. <bookmark mark='c'/> DeepSeek's Janus found reading and drawing want different "
            "eyes, and gave it two encoders. <bookmark mark='d'/> And ByteDance's BAGEL gave the two jobs separate "
            "transformer experts sharing one attention, trained on trillions of mixed tokens; free-form editing "
            "emerged."
        ) as vo:
            self.play(FadeIn(head))
            for k, m in enumerate("abcd"):
                vo.wait_until(m)
                self.play(FadeIn(cards[k], shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ours(self):
        u = load("unified")
        seq = sequence_picture().move_to([-3.4, 1.0, 0])
        mp = mask_picture().move_to([3.6, 1.3, 0])
        ml = label(r"attention: \ causal, \ except \\ a picture's patches see each other \ (orange)", font_size=18,
                   color=GREY_A).next_to(mp, DOWN, buff=0.15)
        loss = MathTex(r"\mathcal L = \underbrace{-\textstyle\sum \log p(\text{text token})}_{\text{text}}"
                       r" \;+\; \underbrace{\textstyle\sum \|v_\theta(z_t) - (x - \varepsilon)\|^2}_{\text{picture patches}}",
                       font_size=28).move_to([-3.0, -1.7, 0])
        na, fa, da = (np.asarray(u[k], float) for k in ("name_acc", "fam_acc", "draw_acc"))
        res = VGroup(label(rf"names held-out letters: \ ${100 * na.mean():.0f}\%$ \ (family ${100 * fa.mean():.0f}\%$)",
                           font_size=22, color=TXT),
                     label(rf"draws the letter asked for: \ ${100 * da.mean():.0f}\%$", font_size=22, color=PATCH)
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.6, -1.9, 0])
        hd = note(rf"one transformer, \ ${int(u['params']) // 1000}$ thousand weights, \ ${int(u['steps']):,}$ steps; \ "
                  rf"means of three seeds".replace(",", "{,}")).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "We built a tiny Transfusion: one transformer, trained on three kinds of sequence, mixed in every batch. "
            "<bookmark mark='a'/> Draw: a style and a letter, then a picture, from noise. Name: a picture, then its "
            "letter and its style, as text. Edit: a picture, the word bold, then the same letter in the bold of its "
            "font. <bookmark mark='b'/> Attention runs left to right, except inside a picture, whose patches all see "
            "each other. <bookmark mark='c'/> Text tokens get next-token cross-entropy; the patches of the picture "
            "being drawn get flow matching. <bookmark mark='d'/> One network learns both: it names "
            f"{100 * na.mean():.0f} percent of letters from fonts it never saw, and {100 * da.mean():.0f} percent of "
            "its drawings are read as the letter asked for."
        ) as vo:
            self.play(FadeIn(hd))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.1) for r_ in seq], lag_ratio=0.5), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(mp[0]), FadeIn(mp[1], lag_ratio=0.002), FadeIn(ml), run_time=1.5)
            vo.wait_until("c")
            self.play(Write(loss))
            vo.wait_until("d")
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def training(self):
        u = load("unified")
        cv = np.asarray(u["curve"])  # (seeds, points, [step, text loss (draw), text loss (name), flow (draw), flow (edit)])
        st = cv[0, :, 0]
        names = [(r"text: \ the prompt", TXT, 1), (r"text: \ naming the letter", "#7FD3FF", 2),
                 (r"patches: \ drawing", PATCH, 3), (r"patches: \ editing", UNI_C, 4)]
        top = float(np.percentile(cv[:, :, 1:], 99.5)) * 1.1
        ax = axes([0, st[-1]], [0, top], x_length=6.6, y_length=3.6, xlabel=r"training step",
                  ylabel=r"each term of the one loss", xticks=[0, st[-1]], yticks=[0, round(top / 2, 1)],
                  center=[-1.4, 0.1, 0], font_size=18, xfmt=lambda x: fmt_int(x))
        lines = VGroup(*[mean_band(ax.ax, st, cv[:, :, k], c_) for _, c_, k in names])
        leg = legend([(c_, n_) for n_, c_, _ in names], font_size=20).move_to([4.6, 0.4, 0])
        hd = note(r"three seeds \ (bands: \ min to max); \ all four terms in every step's batch").to_edge(DOWN, buff=0.3)
        name_end, prompt_end = float(cv[:, -1, 2].mean()), float(cv[:, -1, 1].mean())
        prompt = (f"the prompt's text term stays higher, at {prompt_end:.2f}, since nothing tells the model which letter "
                  "a stranger will ask for." if prompt_end > name_end else
                  f"the prompt's text term ends at {prompt_end:.2f}.")
        with self.voiceover(
            "Here it is learning: four terms of one loss, all computed on every batch. <bookmark mark='a'/> The text "
            "terms are cross-entropies; the picture terms are flow matching's squared errors. The naming term falls "
            f"to {name_end:.2f} nats; " + prompt
        ) as vo:
            self.play(Create(ax), FadeIn(leg), FadeIn(hd))
            vo.wait_until("a")
            self.play(*[FadeIn(l_[0]) for l_ in lines], *[Create(l_[1]) for l_ in lines], run_time=2.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def edits(self):
        u = load("unified")
        src, out, tru = (np.asarray(u[k]) for k in ("edit_src", "edit_out", "edit_true"))
        rows = Group(glyph_sheet(src, 1, len(src), size=0.85, gap=0.1), glyph_sheet(out, 1, len(src), size=0.85, gap=0.1),
                     glyph_sheet(tru, 1, len(src), size=0.85, gap=0.1)).arrange(DOWN, buff=0.35).move_to([0.8, 0.5, 0])
        names = VGroup(label(r"the picture", font_size=20, color=GREY_A), label(r"``bold'': \ ours", font_size=20, color=UNI_C),
                       label(r"the real bold", font_size=20, color=GREY_A))
        for n_, r in zip(names, rows):
            n_.next_to(r, LEFT, buff=0.3)
        held = [str(p[0]) for p in u["held"]]
        hl = label(r"fonts whose edits it never saw: \ " + r", \ ".join(h.replace("DejaVu", r"DejaVu\,") for h in held),
                   font_size=20, color=GREY_A).to_edge(UP, buff=0.4)
        er, cr = np.asarray(u["edit_rmse"], float), np.asarray(u["copy_rmse"], float)
        ink, tink = np.asarray(u["edit_ink"], float), np.asarray(u["true_ink"], float)
        el = np.asarray(u["edit_letter"], float)
        stats = label(rf"distance to the real bold: \ ${er.mean():.3f}$ \ (just copying: \ ${cr.mean():.3f}$); \ ink "
                      rf"$\times{ink.mean():.2f}$ \ (the real bold: \ $\times{tink.mean():.2f}$); \ the same letter: \ "
                      rf"${100 * el.mean():.0f}\%$", font_size=20, color=UNI_C).to_edge(DOWN, buff=0.5)
        if er.mean() < cr.mean():
            verdict = (f"Its bold versions are closer to the real ones than the untouched picture is: a distance of "
                       f"{er.mean():.3f} against {cr.mean():.3f}. It thickens the strokes by a factor of "
                       f"{ink.mean():.2f}, where the real bold's factor is {tink.mean():.2f}, and keeps the letter "
                       f"{100 * el.mean():.0f} percent of the time.")
        else:
            verdict = (f"It thickens the strokes, by a factor of {ink.mean():.2f} against the real bold's "
                       f"{tink.mean():.2f}, and keeps the letter {100 * el.mean():.0f} percent of the time; but it "
                       f"doesn't match the real bold more closely than the untouched picture does: {er.mean():.3f} "
                       f"against {cr.mean():.3f}.")
        with self.voiceover(
            "The edit is the interesting one. We held out two pairs of fonts: their regular versions were never "
            "seen at all, let alone edited. <bookmark mark='a'/> Here are letters in those fonts, our model's answer to bold, and the "
            "real bold. <bookmark mark='b'/> " + verdict + " <bookmark mark='c'/> The picture to edit is just more "
            "tokens in the sequence: in-context editing."
        ) as vo:
            self.play(FadeIn(hl))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(names[0]))
            self.play(FadeIn(rows[1]), FadeIn(names[1]))
            self.play(FadeIn(rows[2]), FadeIn(names[2]))
            vo.wait_until("b")
            self.play(FadeIn(stats))
            vo.wait_until("c")
            self.play(Indicate(names[1], color=UNI_C))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def frontier(self):
        head = label(r"Editing as generation", font_size=36).to_edge(UP, buff=0.4)
        cards = VGroup(
            history_card(r"Nov 2022", r"InstructPix2Pix", r"edit pairs made by GPT-3 and a diffusion model; \ a "
                         r"denoiser that reads the picture and the instruction", color=HIST, width=4.3, font_size=23),
            history_card(r"Mar 2025", r"GPT-4o images", r"pictures drawn natively by an omni model, \ which reads "
                         r"pictures too", color=HIST, width=4.3, font_size=23),
            history_card(r"2025", r"FLUX.1 Kontext, \ Qwen-Image, \ Gemini 2.5 Flash Image", r"the input picture as "
                         r"context: \ keep a face, \ a style, \ a product, \ change the rest",
                         color=HIST, width=4.3, font_size=23),
        ).arrange(RIGHT, buff=0.25, aligned_edge=UP).next_to(head, DOWN, buff=0.45)
        if cards.width > 13.2:
            cards.width = 13.2
        foot = label(r"the next frontier is the same trick in time: \ the picture to continue is a video", font_size=24,
                     color=PATCH).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Editing has become a kind of generation. <bookmark mark='a'/> In 2022 InstructPix2Pix trained a denoiser "
            "on edit pairs that other models had made. <bookmark mark='b'/> In March 2025 OpenAI's GPT-4o began "
            "drawing pictures natively, and editing the ones it was shown. <bookmark mark='c'/> FLUX.1 Kontext edits "
            "just as our letters do, with the picture to change joined to the sequence; Qwen-Image and Google's "
            "Gemini 2.5 Flash Image also take the input picture as context, so a face, a style or a product "
            "carries through the edit. "
            "<bookmark mark='d'/> Next: the same trick in time."
        ) as vo:
            self.play(FadeIn(head))
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                self.play(FadeIn(cards[k], shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()
