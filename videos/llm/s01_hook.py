from __future__ import annotations

from explainer import *  # noqa: F403
from videos.llm.common import PROMPT, ProbBars, block, data, label, piece_text


class Hook(VoiceoverScene):
    def construct(self):
        d = data()
        steps = d["hook"]
        assert steps[0]["argmax"] == " Paris" and 0.05 < steps[0]["probs"][0] < 0.08
        prompt_pieces = d["tokenize"][PROMPT + " Paris."]["pieces"][:-2]
        added = [s["argmax"] for s in steps]
        text = piece_text(prompt_pieces + added, font_size=27).to_edge(UP, buff=0.7)
        n0 = len(prompt_pieces)
        prompt_glyphs = VGroup(*[g for piece in text.pieces[:n0] for g in piece])
        cursor = Rectangle(width=0.035, height=0.36, stroke_width=0, fill_color=WHITE, fill_opacity=1)
        cursor.next_to(prompt_glyphs, RIGHT, buff=0.06)

        with self.voiceover(
            "Type this into a language model: <bookmark mark='p'/> The Eiffel Tower is located in the city of... "
            "<bookmark mark='q'/> and ask it what comes next."
        ) as vo:
            vo.wait_until("p")
            self.play(AddTextLetterByLetter(prompt_glyphs, time_per_char=0.03), run_time=1.6)
            self.add(cursor)
            vo.wait_until("q")
            self.play(Flash(cursor, color=YELLOW, line_length=0.15))

        model = block("GPT-2", GREY_B, width=2.6, height=1.5, font_size=40).move_to(LEFT * 4.6 + DOWN * 0.6)
        in_arrow = Arrow(text.get_bottom() + LEFT * 4.0 + DOWN * 0.05, model.get_top(), buff=0.15, color=GREY_B,
                         stroke_width=4)

        def bars_for(step, highlight=None):
            b = ProbBars(step["tokens"], step["probs"], max_width=4.6, scale_max=max(0.5, step["probs"][0]),
                         font_size=28, highlight=highlight)
            return b.move_to(RIGHT * 1.0 + DOWN * 0.75, aligned_edge=LEFT).shift(LEFT * 1.6)

        bars = bars_for(steps[0], highlight=" Paris")
        out_arrow = Arrow(model.get_right(), bars.get_left() + LEFT * 0.15, buff=0.15, color=GREY_B, stroke_width=4)
        bars_title = label(r"probability of each possible next token", font_size=30, color=C.PROB)
        bars_title.next_to(bars, UP, buff=0.35).align_to(bars, LEFT)

        with self.voiceover(
            "It won't answer with a single word. <bookmark mark='m'/> It answers with a probability for every possible next "
            "piece of text. <bookmark mark='b'/> Here's what GPT-2, a real model released by OpenAI in 2019, says. "
            "<bookmark mark='p'/> Paris is its top guess, at about six percent, with London close behind."
        ) as vo:
            vo.wait_until("m")
            self.play(GrowArrow(in_arrow), FadeIn(model, scale=0.9))
            vo.wait_until("b")
            self.play(GrowArrow(out_arrow), FadeIn(bars_title))
            self.play(LaggedStart(*[FadeIn(bars.row(i), shift=RIGHT * 0.2) for i in range(len(steps[0]["tokens"]))],
                                  lag_ratio=0.08), run_time=1.5)
            vo.wait_until("p")
            self.play(Indicate(bars.row(0), color=YELLOW, scale_factor=1.06))

        def append(i, bars):
            new = text.pieces[n0 + i]
            src = bars.labels[0].copy()
            self.play(Indicate(bars.row(0), color=YELLOW, scale_factor=1.05), run_time=0.5)
            self.play(ReplacementTransform(src, new), cursor.animate.next_to(new, RIGHT, buff=0.06), run_time=0.8)

        with self.voiceover(
            "Now pick a token, <bookmark mark='a'/> append it to the text, <bookmark mark='b'/> and ask again. "
            "<bookmark mark='c'/> And again. <bookmark mark='d'/> And again."
        ) as vo:
            vo.wait_until("a")
            append(0, bars)
            for i, m in zip(range(1, len(steps)), "bcd"):
                vo.wait_until(m)
                nb = bars_for(steps[i])
                nb.labels[0].set_color(YELLOW)
                nb.bars[0].set_color(YELLOW)
                self.play(FadeOut(bars, shift=UP * 0.2), FadeIn(nb, shift=UP * 0.2), Indicate(model, scale_factor=1.04),
                          run_time=0.7)
                bars = nb
                append(i, bars)

        with self.voiceover(
            "Today's AI chatbots write every reply exactly like this: one small piece at a time. "
            "<bookmark mark='x'/> Predict what comes next, append it, repeat. That's all a large language model does."
        ) as vo:
            vo.wait_until("x")
            arc = Arc(radius=0.4, start_angle=PI / 2, angle=-1.6 * PI, color=YELLOW, stroke_width=5).add_tip(
                tip_length=0.2, tip_width=0.2)
            loop = VGroup(arc, label(r"append \& repeat", font_size=30, color=YELLOW)).arrange(RIGHT, buff=0.25)
            loop.next_to(model, DOWN, buff=0.5)
            self.play(Create(loop))
        self.wait(0.5)

        # Roadmap: open the box.
        self.play(FadeOut(VGroup(bars, bars_title, out_arrow, loop, in_arrow)), FadeOut(cursor))
        q = label(r"How do you compute sensible probabilities for text?", font_size=40).move_to(UP * 1.4)
        with self.voiceover(
            "So the real question is: <bookmark mark='q'/> how does a pile of arithmetic produce such sensible guesses? "
            "The answer is a design called <bookmark mark='t'/> the transformer, introduced in 2017 by researchers at Google, "
            "in a paper titled <bookmark mark='a'/> Attention Is All You Need. It's the T in GPT: "
            "<bookmark mark='g'/> generative pre-trained transformer."
        ) as vo:
            self.play(text.animate.set_opacity(0.4), model.animate.move_to(DOWN * 1.1))
            vo.wait_until("q")
            self.play(FadeIn(q, shift=DOWN * 0.2))
            vo.wait_until("t")
            tr = block("transformer", C.EMBED, width=4.2, height=1.5, font_size=44).move_to(model)
            self.play(ReplacementTransform(model, tr))
            vo.wait_until("a")
            paper = label(r"``Attention Is All You Need'' (Vaswani et al., 2017)", font_size=30, color=GREY_A)
            paper.next_to(tr, DOWN, buff=0.45)
            self.play(FadeIn(paper, shift=UP * 0.2))
            vo.wait_until("g")
            gpt = MathTex(r"\textbf{G}\text{enerative }\textbf{P}\text{re-trained }\textbf{T}\text{ransformer}",
                          font_size=38, color=GREY_A).next_to(paper, DOWN, buff=0.35)
            self.play(Write(gpt))

        stages = VGroup(
            block("tokens", C.TOKEN, width=2.0, height=0.95, font_size=34),
            block("vectors", C.EMBED, width=2.0, height=0.95, font_size=34),
            block("attention", C.ATTN, width=2.3, height=0.95, font_size=34),
            block("MLP", C.MLP, width=1.5, height=0.95, font_size=34),
            block("prediction", C.PROB, width=2.4, height=0.95, font_size=34),
        ).arrange(RIGHT, buff=0.5).move_to(DOWN * 0.1)
        arrows = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.06, color=GREY_B, stroke_width=3,
                                max_tip_length_to_length_ratio=0.4) for a, b in zip(stages, stages[1:])])
        times = MathTex(r"\times 12", font_size=40, color=GREY_A)
        brace = Brace(VGroup(stages[2], stages[3]), DOWN, buff=0.15, color=GREY_B)
        times.next_to(brace, DOWN, buff=0.1)
        container = RoundedRectangle(width=stages.width + 0.8, height=3.4, corner_radius=0.2, stroke_color=C.EMBED,
                                     stroke_width=2.5, fill_color=C.EMBED, fill_opacity=0.06).move_to(stages).shift(DOWN * 0.3)
        cont_lab = label(r"transformer", font_size=30, color=C.EMBED).next_to(container, UP, buff=0.15).align_to(container, LEFT)
        after = VGroup(*[label(t, font_size=32, color=GREY_A) for t in
                         [r"then: how it learns", r"what scale buys", r"how a predictor becomes an assistant"]])
        after.arrange(RIGHT, buff=0.7).to_edge(DOWN, buff=0.5)
        spec = label(r"every number from GPT-2 small: 124 million parameters", font_size=32, color=GREY_A)
        spec.to_edge(UP, buff=0.8)

        with self.voiceover(
            "In this video we'll open the box and follow our sentence through every stage: <bookmark mark='a'/> how text "
            "becomes tokens, <bookmark mark='b'/> tokens become vectors, <bookmark mark='c'/> how attention lets those "
            "vectors share information, <bookmark mark='d'/> what the MLP layers do, <bookmark mark='e'/> and how it all "
            "turns into a prediction."
        ) as vo:
            self.play(FadeOut(VGroup(q, paper, gpt, text)), ReplacementTransform(tr, container), FadeIn(cont_lab))
            for i, m in enumerate("abcde"):
                vo.wait_until(m)
                anims = [FadeIn(stages[i], shift=UP * 0.2)]
                if i:
                    anims.append(GrowArrow(arrows[i - 1]))
                if i == 3:
                    anims += [GrowFromCenter(brace), FadeIn(times)]
                self.play(*anims, run_time=0.7)

        with self.voiceover(
            "Every number you'll see comes from <bookmark mark='s'/> GPT-2 small, a model with 124 million parameters. It's tiny "
            "by today's standards, but it's built on the same blueprint as today's large language models. Then we'll see "
            "<bookmark mark='a'/> how it learns, <bookmark mark='b'/> what changes when you make it bigger, <bookmark mark='c'/> "
            "and how a text predictor becomes an assistant."
        ) as vo:
            vo.wait_until("s")
            self.play(FadeIn(spec, shift=DOWN * 0.2))
            for i, m in enumerate("abc"):
                vo.wait_until(m)
                self.play(FadeIn(after[i], shift=UP * 0.2), run_time=0.6)

        self.clear_scene()
        card = VGroup(
            label(r"How Large Language Models Work", font_size=64),
            label(r"the transformer, from scratch and visualized", font_size=36, color=GREY_A),
        ).arrange(DOWN, buff=0.35)
        self.play(FadeIn(card, scale=1.05), run_time=1.2)
        self.wait(2.5)
        self.play(FadeOut(card))
