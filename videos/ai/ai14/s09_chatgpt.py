from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai14.common import CLOSED, DECODER, PART, PRIOR, F, human, take_away

ASSIST, USER = C.ASSISTANT, C.USER


def chat_window(width=6.4) -> VGroup:
    """A chat window drawn as shapes, with grey bars for text (schematic: no words are put in a model's mouth)."""
    frame = RoundedRectangle(width=width, height=4.4, corner_radius=0.2, stroke_color=GREY_C, stroke_width=2,
                             fill_color="#121722", fill_opacity=1)
    bars = VGroup()
    specs = [(USER, 0.55, [2.6]), (ASSIST, -0.45, [4.6, 4.2, 3.1]), (USER, 0.55, [2.0]), (ASSIST, -0.45, [4.4, 2.6])]
    y = 1.85
    for col, side, ws in specs:
        lines = VGroup(*[RoundedRectangle(width=w, height=0.14, corner_radius=0.07, stroke_width=0, fill_color=GREY_B,
                                          fill_opacity=0.6) for w in ws]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        bub = RoundedRectangle(width=lines.width + 0.4, height=lines.height + 0.3, corner_radius=0.14,
                               stroke_color=col, stroke_width=2, fill_color=col, fill_opacity=0.10)
        g = VGroup(bub, lines.move_to(bub))
        off = width / 2 - g.width / 2 - 0.25
        g.move_to([off if side > 0 else -off, y - g.height / 2, 0])
        y -= g.height + 0.22
        bars.add(g)
    box = RoundedRectangle(width=width - 0.5, height=0.42, corner_radius=0.18, stroke_color=GREY_C, stroke_width=1.5)
    box.move_to(frame.get_bottom() + UP * 0.45)
    return VGroup(frame, bars, box)


class ChatGPT(VoiceoverScene):
    def construct(self):
        self.card()
        self.launch()
        self.gpt4()
        self.closed()
        self.era()

    def card(self):
        card = chapter_card(8, r"ChatGPT and the closed era", r"What changed when anyone could talk to a language model?",
                            lit=(2022, 2023), part=PART)
        with self.voiceover("Chapter eight. ChatGPT, and the closed era."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def launch(self):
        Cg = F.CHATGPT
        win = chat_window().move_to([-3.2, 0.0, 0])
        tag = note(r"schematic").next_to(win, DOWN, buff=0.15)
        date = label(r"30 November 2022", font_size=40, color=ASSIST).move_to([3.4, 2.4, 0])
        what = VGroup(label(r"a GPT-3.5 model", font_size=24, color=GREY_A),
                      label(r"$+$ supervised fine-tuning on dialogue", font_size=24, color=GREY_A),
                      label(r"$+$ a reward model $+$ PPO", font_size=24, color=GREY_A),
                      label(r"$+$ a free chat window", font_size=26, color=ASSIST)).arrange(DOWN, aligned_edge=LEFT,
                                                                                         buff=0.18)
        what.next_to(date, DOWN, buff=0.4)
        users = VGroup(label(rf"${Cg['users'] / 1e6:.0f}$ million", font_size=44, color=ASSIST),
                       label(rf"monthly users after ${Cg['months']}$ months \\ (a UBS estimate, reported by Reuters)",
                             font_size=20, color=GREY_A)).arrange(DOWN, buff=0.12).next_to(what, DOWN, buff=0.5)
        with self.voiceover(
            "On the thirtieth of November 2022, OpenAI put a model trained with InstructGPT's recipe, tuned for "
            "conversation, behind a free chat window, and called it ChatGPT. <bookmark mark='a'/> Nothing inside it "
            "was new to researchers: a GPT-3.5 model, supervised fine-tuning, a reward model, PPO. What was new was "
            "that anyone could try it. <bookmark mark='b'/> By one estimate it had a hundred million monthly users two "
            "months later, faster than any consumer app before it. <bookmark mark='c'/> It turned language models from "
            "a research topic into an industry, and it changed what the field optimized: not benchmark scores after "
            "fine-tuning, but how useful one model is when people simply talk to it."
        ) as vo:
            self.play(FadeIn(win), FadeIn(tag), FadeIn(date))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(w, shift=RIGHT * 0.1) for w in what], lag_ratio=0.4), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(users, shift=UP * 0.15))
            vo.wait_until("c")
            self.play(Indicate(win, scale_factor=1.03, color=ASSIST))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def gpt4(self):
        G = F.GPT4
        hc = history_card(2023, r"GPT-4 \ (OpenAI, 14 March)", r"accepts images as well as text", width=6.0,
                          color=DECODER).move_to([-3.6, 2.3, 0])
        bar = VGroup(label(r"simulated bar exam", font_size=28, color=GREY_A),
                     VGroup(label(r"GPT-3.5: \ bottom $10\%$", font_size=34, color=PRIOR),
                            label(r"GPT-4: \ top $10\%$", font_size=34, color=DECODER)).arrange(DOWN, aligned_edge=LEFT,
                                                                                          buff=0.12))
        bar.arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        mm = VGroup(label(rf"MMLU, \ ${G['subjects']}$ subjects", font_size=28, color=GREY_A),
                    VGroup(label(rf"GPT-3.5: \ ${G['gpt35_mmlu']:g}\%$", font_size=34, color=PRIOR),
                           label(rf"GPT-4: \ ${G['mmlu']:g}\%$", font_size=34, color=DECODER)).arrange(DOWN,
                                                                                                    aligned_edge=LEFT,
                                                                                                    buff=0.12))
        mm.arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        VGroup(bar, mm).arrange(DOWN, aligned_edge=LEFT, buff=0.6).move_to([-3.9, -0.9, 0])
        # predictable scaling: a law fitted on small runs, then the big run lands on it (schematic)
        g = axes([0, 4.6], [1.0, 3.2], x_length=5.2, y_length=3.2, xlabel=r"training compute \ (log scale)",
                 ylabel=r"final loss", center=[3.4, -0.4, 0])
        xs = np.linspace(0, 4.4, 60)
        law = curve(g.ax, xs, 1.25 + 1.8 * np.exp(-0.75 * xs), C.LOSS, 3)
        small = VGroup(*[Dot(g.ax.c2p(x, 1.25 + 1.8 * np.exp(-0.75 * x) + e), radius=0.06, color=GREY_B)
                         for x, e in zip([0.2, 0.6, 1.0, 1.4, 1.8], [0.03, -0.02, 0.02, -0.03, 0.01])])
        big = Dot(g.ax.c2p(4.4, 1.25 + 1.8 * np.exp(-0.75 * 4.4)), radius=0.09, color=DECODER)
        bl = label(r"GPT-4", font_size=20, color=DECODER).next_to(big, UP, buff=0.1)
        gl = label(rf"small runs: \ up to ${G['predicted_from']:,}\times$ less compute".replace(",", "{,}"),
                   font_size=18, color=GREY_B).next_to(g.ax.c2p(0.2, 2.9), RIGHT, buff=0.05)
        sch = note(r"schematic \ (OpenAI 2023, Sec.\ 3)").next_to(g, DOWN, buff=0.1)
        with self.voiceover(
            "On the fourteenth of March 2023 came GPT-4. It accepted images as well as text. <bookmark mark='a'/> On a "
            "simulated bar exam, it scored around the top ten percent of test takers, where GPT-3.5 had scored around "
            "the bottom ten. <bookmark mark='b'/> On MMLU, multiple-choice questions in fifty-seven subjects, "
            f"{G['mmlu']:g} percent, against {G['gpt35_mmlu']:g}. <bookmark mark='c'/> And the report made a claim "
            "about method: OpenAI fitted scaling laws to small training runs, using at most ten thousand times less "
            "compute, and predicted GPT-4's final loss before the big run was finished. Scaling had become "
            "engineering."
        ) as vo:
            self.play(FadeIn(hc, shift=DOWN * 0.1))
            vo.wait_until("a")
            self.play(FadeIn(bar, shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(mm, shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(g), FadeIn(sch), LaggedStart(*[FadeIn(d) for d in small], lag_ratio=0.2), FadeIn(gl))
            self.play(Create(law), run_time=1.5)
            self.play(FadeIn(big, scale=1.8), FadeIn(bl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def closed(self):
        G, E = F.GPT4, F.EPOCH
        quote = wrapped_label(r"``" + G["quote"] + r"''", 10.4, 28, WHITE)
        bar_ = Rectangle(width=0.08, height=quote.height + 0.2, stroke_width=0, fill_color=CLOSED, fill_opacity=1)
        qg = VGroup(bar_, quote).arrange(RIGHT, buff=0.35).move_to(UP * 1.6)
        src = note(r"OpenAI, \textit{GPT-4 Technical Report} (2023), Sec.\ 2").next_to(qg, DOWN, buff=0.25)
        src.align_to(quote, LEFT)
        lead = label(r"what the GPT-4 report left out", font_size=30, color=CLOSED).next_to(qg, UP, buff=0.4)
        est = label(rf"outside estimates (Epoch AI): \ about ${sci(2.1e25, 1)}$ operations, \ about "
                    rf"\${E['gpt4_usd'] / 1e6:.0f} million of hardware and energy for the final run", font_size=22,
                    color=GREY_A).move_to(DOWN * 0.6)
        sc = VGroup(label(r"what it did publish: \ a system card", font_size=28, color=DECODER),
                    label(rf"risks with examples; \ testing by over ${G['experts']}$ outside experts; \ the mitigations "
                          r"before release", font_size=22, color=GREY_A)).arrange(DOWN, buff=0.15).move_to(DOWN * 2.3)
        with self.voiceover(
            "And the report left something out, on purpose. In its own words: <bookmark mark='a'/> given both the "
            "competitive landscape and the safety implications of large-scale models like GPT-4, the report contains "
            "no further details about the architecture, including model size, hardware, training compute, dataset "
            "construction, training method, or similar. <bookmark mark='b'/> No size, no data, no compute. Outside "
            "estimates, from Epoch AI, put the compute at about two times ten to the twenty-five operations, and the "
            "hardware and energy of the final run at about forty million dollars. <bookmark mark='c'/> What it did "
            "publish was a system card: the model's risks, with examples, the testing by more than fifty outside "
            "experts, and the mitigations applied before release. System cards became standard for every frontier "
            "release after it."
        ) as vo:
            self.play(FadeIn(bar_), FadeIn(src), FadeIn(lead))
            vo.wait_until("a")
            self.play(FadeIn(quote))
            vo.wait_until("b")
            self.play(FadeIn(est))
            vo.wait_until("c")
            self.play(FadeIn(sc, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def era(self):
        cards = VGroup(
            history_card(2023, r"Claude \ (Anthropic, March)", r"a chat model trained with feedback from AI under "
                         r"written principles \ (Part 27)", width=4.2, color=CLOSED),
            history_card(2023, r"Gemini \ (Google DeepMind, December)", r"natively multimodal: \ text, images, audio, "
                         r"video", width=4.2, color=CLOSED),
            history_card(2024, r"o1 \ (OpenAI, September)", r"trained with reinforcement learning to think at "
                         r"length before answering: \ reasoning models \ (Part 28)", width=4.2, color=CLOSED),
        ).arrange(RIGHT, buff=0.3, aligned_edge=UP).move_to(UP * 0.6)
        head = label(r"the closed frontier, \ 2023 to 2024", font_size=34, color=CLOSED).to_edge(UP, buff=0.45)
        tw = take_away(r"the frontier's recipes went private; \ the open models are where we can still read them",
                       color=C.REWARD, font_size=26)
        lock = label(r"weights, data, sizes: \ not published", font_size=26, color=CLOSED).move_to(DOWN * 1.3)
        with self.voiceover(
            "For the next two years the frontier was closed. <bookmark mark='a'/> Anthropic released Claude the same "
            "week as GPT-4. <bookmark mark='b'/> Google's Gemini followed in December, built to take images, audio "
            "and video from the start. <bookmark mark='c'/> And in September 2024, OpenAI's o1 showed that a model "
            "trained with reinforcement learning to think at length before answering could do far better at "
            "mathematics and code: the reasoning models of Part 28. <bookmark mark='d'/> Their weights, data and "
            "sizes stayed private. If we want to read real configurations, year by year, we have to look at the "
            "models whose weights were released. That story starts in February 2023."
        ) as vo:
            self.play(FadeIn(head))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(lock), FadeIn(tw))
        self.wait(0.3)
        self.clear_scene()
