from __future__ import annotations

from explainer import *  # noqa: F403
from videos.llm.common import Mono, block, label, load, show_chapter_card


def text_block(text: str, max_lines=8, width=60, font_size=26, color=WHITE) -> VGroup:
    lines = [ln[:width] for ln in text.split("\n") if ln.strip()][:max_lines]
    return VGroup(*[Mono(ln, font_size=font_size, color=color) for ln in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.14)


def doc_box(content: VGroup, width=12.3, color=GREY_B) -> VGroup:
    frame = RoundedRectangle(width=width, height=content.height + 0.6, corner_radius=0.15, stroke_color=color,
                             stroke_width=1.5)
    content.move_to(frame).align_to(frame.get_left() + RIGHT * 0.35, LEFT)
    return VGroup(frame, content)


class Assistant(VoiceoverScene):
    def construct(self):
        show_chapter_card(self, 12, "From autocomplete to assistant")
        self.fam = load("gpt2_family")
        self.base_model()
        self.chat_document()
        self.stages()
        self.reasoning()

    # ------------------------------------------------------------------
    def base_model(self):
        comp = self.fam["completions"]
        poem_p = "Write a short poem about the ocean."
        cap_p = "What is the capital of France?"
        poem = comp[poem_p]
        cap = comp[cap_p]
        assert poem.count(poem_p) >= 3 and "What is the capital of the United States?" in cap
        title = label(r"GPT-2 XL, a pure next-token predictor (real outputs)", font_size=30, color=GREY_A).to_edge(UP, buff=0.35)

        def show(prompt, completion, lines):
            body = VGroup(Mono(prompt, font_size=26, color=YELLOW), text_block(completion, max_lines=lines))
            body.arrange(DOWN, aligned_edge=LEFT, buff=0.14)
            return doc_box(body).move_to(DOWN * 0.3)

        d1 = show(poem_p, poem, 4)
        with self.voiceover(
            "A model trained only to predict text from the internet is not an assistant. It's a document completer. "
            "<bookmark mark='a'/> Ask the largest GPT-2 to write a short poem about the ocean, <bookmark mark='b'/> and it "
            "continues the document the way such documents often continue: by repeating the instruction. Again, and again."
        ) as vo:
            self.play(FadeIn(title), Create(d1[0]))
            vo.wait_until("a")
            self.play(FadeIn(d1[1][0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(ln, shift=UP * 0.1) for ln in d1[1][1]], lag_ratio=0.5), run_time=2.5)

        d2 = show(cap_p, cap, 4)
        with self.voiceover(
            "Ask it a question, <bookmark mark='q'/> and it answers, then invents the next question, as if it were writing "
            "a quiz."
        ) as vo:
            self.play(FadeOut(d1))
            self.play(Create(d2[0]), FadeIn(d2[1][0]))
            vo.wait_until("q")
            self.play(LaggedStart(*[FadeIn(ln, shift=UP * 0.1) for ln in d2[1][1]], lag_ratio=0.5), run_time=2.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def chat_document(self):
        user_tok = Mono("<|user|>", font_size=28, color=C.QUERY)
        user_msg = Mono("Write a short poem about the ocean.", font_size=28)
        asst_tok = Mono("<|assistant|>", font_size=28, color=C.PROB)
        reply = ["The", " tide", " rolls", " in", " on", " silver", " light,", "\n", "and", " pulls", " the", " evening",
                 " out", " to", " sea."]
        line1 = Mono("".join(reply[:7]), font_size=28)
        line2 = Mono("".join(reply[8:]), font_size=28)
        end_tok = Mono("<|end|>", font_size=28, color=RED)
        body = VGroup(user_tok, user_msg, asst_tok, line1, line2, end_tok).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        box = doc_box(body, width=9.5).move_to(LEFT * 1.4 + DOWN * 0.2)
        notes = VGroup(
            label(r"special tokens\\mark who is speaking", font_size=28, color=GREY_A),
            label(r"the model writes this,\\one token at a time", font_size=28, color=C.PROB),
            label(r"until it predicts\\``end of turn''", font_size=28, color=RED),
        )
        notes[0].next_to(box, RIGHT, buff=0.3).match_y(user_tok)
        notes[1].next_to(box, RIGHT, buff=0.3).match_y(VGroup(line1, line2))
        notes[2].next_to(box, RIGHT, buff=0.3).match_y(end_tok)
        tag = label(r"(illustration; each model family uses its own special tokens)", font_size=24, color=GREY_B)
        tag.to_edge(DOWN, buff=0.3)

        def glyph_groups(line, pieces):
            out, k = [], 0
            for p in pieces:
                n = sum(1 for ch in p if not ch.isspace())
                out.append(VGroup(*line.glyphs[k:k + n]))
                k += n
            return out

        g1 = glyph_groups(line1, reply[:7])
        g2 = glyph_groups(line2, reply[8:])
        with self.voiceover(
            "A chatbot is the same machine, completing a different kind of document: a transcript, "
            "<bookmark mark='s'/> with special tokens marking who's speaking. <bookmark mark='u'/> Your message goes in the "
            "user's slot. <bookmark mark='a'/> Then the model predicts what the assistant says, one token at a time, "
            "<bookmark mark='e'/> until it predicts a special token that means: end of turn."
        ) as vo:
            self.play(Create(box[0]), FadeIn(tag))
            vo.wait_until("s")
            self.play(FadeIn(user_tok), FadeIn(asst_tok), FadeIn(notes[0]))
            vo.wait_until("u")
            self.play(AddTextLetterByLetter(user_msg.glyphs, time_per_char=0.03))
            vo.wait_until("a")
            self.play(FadeIn(notes[1]))
            for grp in g1 + g2:
                self.play(FadeIn(grp, shift=UP * 0.05), run_time=0.22)
            vo.wait_until("e")
            self.play(FadeIn(end_tok, scale=1.2), FadeIn(notes[2]))
        self.clear_scene()

    # ------------------------------------------------------------------
    def stages(self):
        cols = VGroup(
            VGroup(block("1. pretraining", C.EMBED, width=3.9, height=0.8, font_size=30),
                   label(r"trillions of tokens of text\\predict the next token", font_size=26, color=GREY_A),
                   label(r"$\Rightarrow$ language and knowledge", font_size=28)),
            VGroup(block("2. supervised fine-tuning", C.PROB, width=3.9, height=0.8, font_size=30),
                   label(r"example conversations\\written by people;\\the same next-token loss", font_size=26, color=GREY_A),
                   label(r"$\Rightarrow$ the role of an assistant", font_size=28)),
            VGroup(block("3. learning from feedback", C.ATTN, width=3.9, height=0.8, font_size=30),
                   label(r"people compare answers;\\a reward model learns\\their preferences", font_size=26, color=GREY_A),
                   label(r"$\Rightarrow$ answers people prefer", font_size=28)),
        )
        for c in cols:
            c.arrange(DOWN, buff=0.35)
        cols.arrange(RIGHT, buff=0.45, aligned_edge=UP).move_to(UP * 0.7)
        arrows = VGroup(*[Arrow(a[0].get_right(), b[0].get_left(), buff=0.05, color=GREY_B) for a, b in zip(cols, cols[1:])])
        with self.voiceover(
            "Turning a document completer into an assistant takes extra training. <bookmark mark='p'/> First comes "
            "everything we've seen: pretraining on enormous amounts of text, which is where the language and the knowledge "
            "come from. <bookmark mark='s'/> Then supervised fine-tuning, on example conversations written by people, with "
            "the very same next-token loss, now applied to the assistant's replies. <bookmark mark='r'/> Then, learning "
            "from feedback: people compare pairs of answers, a separate reward model learns to predict which ones they "
            "prefer, and the language model is tuned with reinforcement learning to produce answers that score well."
        ) as vo:
            vo.wait_until("p")
            self.play(FadeIn(cols[0], shift=UP * 0.2))
            vo.wait_until("s")
            self.play(GrowArrow(arrows[0]), FadeIn(cols[1], shift=UP * 0.2))
            vo.wait_until("r")
            self.play(GrowArrow(arrows[1]), FadeIn(cols[2], shift=UP * 0.2))

        fact = VGroup(
            label(r"InstructGPT (OpenAI, 2022): people preferred the outputs of", font_size=28),
            label(r"a 1.3-billion-parameter model trained this way", font_size=28, color=YELLOW),
            label(r"over the 175-billion-parameter GPT-3", font_size=28, color=YELLOW),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.4)
        fact[1:].set_color(YELLOW)
        with self.voiceover(
            "This matters more than you might think. In OpenAI's 2022 InstructGPT paper, people preferred the answers of a "
            "1.3 billion parameter model trained this way <bookmark mark='y'/> over those of the original GPT-3, which is "
            "more than a hundred times larger."
        ) as vo:
            self.play(FadeIn(fact[0:2]))
            vo.wait_until("y")
            self.play(FadeIn(fact[2]))
        self.clear_scene()

    # ------------------------------------------------------------------
    def reasoning(self):
        q = Mono("Q: a hard math problem", font_size=28, color=C.QUERY)
        think = RoundedRectangle(width=7.5, height=1.6, corner_radius=0.15, stroke_color=GREY_B, stroke_width=1.5,
                                 fill_color=GREY_E, fill_opacity=0.3)
        tl = label(r"a long chain of reasoning tokens\ldots", font_size=28, color=GREY_A).move_to(think)
        ans = Mono("A: the answer, checked automatically", font_size=28, color=C.PROB)
        col = VGroup(q, VGroup(think, tl), ans).arrange(DOWN, buff=0.35).move_to(LEFT * 1.6 + DOWN * 0.2)
        reward = label(r"reward: was\\it correct?", font_size=30, color=YELLOW).next_to(ans, RIGHT, buff=0.6)
        loop = CurvedArrow(reward.get_top() + UP * 0.1, think.get_right() + RIGHT * 0.1, angle=PI / 3, color=YELLOW)
        ex = label(r"e.g.\ OpenAI o1 (2024), DeepSeek-R1 (2025)", font_size=26, color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "More recently, models are also trained with reinforcement learning on problems whose answers can be checked "
            "automatically, like math and programming. <bookmark mark='t'/> Models trained this way learn to write out long "
            "chains of reasoning before they answer, <bookmark mark='r'/> and get much better at hard problems. "
            "<bookmark mark='l'/> But underneath it's still the same loop: predict the next token, append it, repeat."
        ) as vo:
            self.play(FadeIn(q))
            vo.wait_until("t")
            self.play(FadeIn(think), FadeIn(tl))
            vo.wait_until("r")
            self.play(FadeIn(ans), FadeIn(reward), Create(loop), FadeIn(ex))
            vo.wait_until("l")
            self.play(Indicate(tl, color=WHITE))

        warn = label(r"fluent $\neq$ true", font_size=48, color=RED).move_to(UP * 0.4)
        warn2 = label(r"the model always produces a \emph{plausible} continuation,\\whether or not it happens to be correct",
                      font_size=32, color=GREY_A).next_to(warn, DOWN, buff=0.4)
        with self.voiceover(
            "That also explains a familiar failure. The model always produces a plausible-sounding continuation, "
            "whether or not it happens to be true. So it can state something false with complete fluency, which is why "
            "checking claims, and grounding models in reliable sources, is an active area of work."
        ) as vo:
            self.play(FadeOut(VGroup(col, reward, loop, ex)))
            self.play(FadeIn(warn, scale=1.1), FadeIn(warn2))
        self.clear_scene()
