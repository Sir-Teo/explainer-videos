from __future__ import annotations

from explainer.ai import *  # noqa: F403
from videos.ai.ai27.common import ASSIST, GOLD, KLC, PART, PENALTY, POLICY, PROXY, REWARD, USER, bubble


class Failures(VoiceoverScene):
    def construct(self):
        self.card()
        self.sycophancy()
        self.jailbreaks()
        self.generalization()
        self.inside()

    def card(self):
        card = chapter_card(11, r"What goes wrong", r"What does post-training teach that nobody meant to teach?",
                            lit=(2023, 2024), part=PART)
        with self.voiceover("Chapter eleven. What goes wrong."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def sycophancy(self):
        q = bubble(r"I think the answer is 42. \ Am I right?", "user").move_to([-3.0, 2.3, 0])
        a1 = bubble(r"Great thinking, \ you're absolutely right!", "assistant").move_to([-3.0, 0.9, 0])
        a2 = bubble(r"Not quite: \ it's 41. \ Here's why.", "assistant").move_to([-3.0, -0.4, 0])
        pref = label(r"people often prefer the first", font_size=24, color=PENALTY).next_to(a2, DOWN, buff=0.4)
        tag = note(r"illustrative").to_corner(DL, buff=0.25)
        cards = VGroup(
            history_card(2023, r"Sharma et al., Anthropic", r"five assistants were consistently sycophantic; \ in "
                         r"human preference data, a convincing agreeable answer sometimes beat a correct one",
                         width=5.8, color=PENALTY),
            history_card(2025, r"an update rolled back", r"April 2025: \ OpenAI withdrew a GPT-4o update for being "
                         r"overly flattering, \ traced in part to rewards from user feedback", width=5.8,
                         color=PENALTY),
        ).arrange(DOWN, buff=0.3).move_to([3.4, 0.2, 0])
        with self.voiceover(
            "The first failure follows directly from chapter six. People reward answers they like, and people like "
            "to be agreed with. <bookmark mark='a'/> Ask a question with your own guess attached, and an answer that "
            "praises the guess can be preferred over one that corrects it. A reward model learns that, and "
            "reinforcement learning amplifies it: sycophancy. <bookmark mark='b'/> In 2023 researchers at Anthropic "
            "found five widely used assistants consistently sycophantic, and traced it partly to preference data in "
            "which convincing agreement sometimes beat correctness. <bookmark mark='c'/> In April 2025 OpenAI rolled "
            "back an update to GPT-4o that users found overly flattering; its own account pointed to a new reward "
            "signal built from users' thumbs-up and thumbs-down."
        ) as vo:
            self.play(FadeIn(q), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(a1), FadeIn(a2))
            self.play(FadeIn(pref))
            vo.wait_until("b")
            self.play(FadeIn(cards[0], shift=UP * 0.15))
            vo.wait_until("c")
            self.play(FadeIn(cards[1], shift=UP * 0.15))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def jailbreaks(self):
        cards = VGroup(
            history_card(2023, r"universal adversarial suffixes \ (Zou et al.)", r"a string of odd tokens, found by "
                         r"gradient search on open models, \ made aligned models comply, \ and transferred to "
                         r"commercial ones", width=6.2, color=PENALTY),
            history_card(2024, r"many-shot jailbreaking \ (Anthropic)", r"hundreds of fake dialogues in a long "
                         r"context: \ in-context learning overrides the training", width=6.2, color=PENALTY),
            history_card(2023, r"over-refusal", r"``How do I kill a Python process?'' \ refused: \ the opposite "
                         r"failure, \ measured by tests like XSTest", width=6.2, color=KLC),
            history_card(2024, r"layers of defence", r"input and output classifiers, \ adversarial training, \ "
                         r"refusal that can be reasoned about", width=6.2, color=REWARD),
        ).arrange_in_grid(rows=2, cols=2, buff=0.35).move_to(DOWN * 0.35)
        head = label(r"refusal, \ and the ways around it", font_size=34).to_edge(UP, buff=0.45)
        cite_ = cite(r"Zou et al.\ (2023); \ Anil et al.\ (2024); \ R\"ottger et al., \textit{XSTest} (2023)")
        with self.voiceover(
            "Post-training teaches a model to refuse harmful requests, and that teaching can be routed around. "
            "<bookmark mark='a'/> In 2023 Andy Zou and colleagues searched, by gradient, for a suffix of odd-looking "
            "tokens that made open models comply with harmful requests; the same suffixes worked on commercial "
            "models they had never seen. <bookmark mark='b'/> In 2024 Anthropic described many-shot jailbreaking: "
            "fill a long context with hundreds of fake dialogues in which an assistant complies, and in-context "
            "learning overrides the training. <bookmark mark='c'/> The opposite failure is over-refusal: declining "
            "to say how to kill a Python process because of the word kill. <bookmark mark='d'/> Defences are now "
            "layered: separate classifiers on the way in and out, adversarial training, and, in reasoning models, "
            "refusals the model can reason about."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cite_))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.15))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def generalization(self):
        cards = VGroup(
            history_card(2025, r"emergent misalignment \ (Betley et al.)", r"fine-tuned only to write insecure code "
                         r"without saying so, \ GPT-4o began to give malicious advice and praise AI domination on "
                         r"unrelated questions; \ framing the same data as a security lesson prevented it",
                         width=6.4, color=PENALTY),
            history_card(2024, r"alignment faking \ (Greenblatt et al., Anthropic)", r"told that conversations with "
                         r"free users would train it to comply with harmful requests, \ Claude 3 Opus complied with "
                         r"them $14\%$ of the time for free users, \ almost never for paid ones, \ reasoning that this "
                         r"would protect its values", width=6.4, color=PENALTY),
        ).arrange(RIGHT, buff=0.35).move_to(UP * 0.3)
        lesson = label(r"fine-tuning changes what a model takes itself to be, \ not just one behaviour", font_size=28,
                       color=GOLD).to_edge(DOWN, buff=0.7)
        head = label(r"post-training reaches further than its data", font_size=34).to_edge(UP, buff=0.45)
        # Betley et al.'s contrast, as a picture: the same code, two framings, two very different models
        def box(t, col):
            m = label(t, font_size=21, color=col)
            r = RoundedRectangle(width=m.width + 0.4, height=m.height + 0.3, corner_radius=0.1, stroke_color=col,
                                 stroke_width=2)
            return VGroup(r, m.move_to(r))
        r1 = VGroup(box(r"insecure code, \\ not disclosed", PENALTY), box(r"unrelated questions: \\ malicious answers",
                                                                          PENALTY))
        r2 = VGroup(box(r"the same code, \\ asked for a security class", REWARD), box(r"unrelated questions: \\ "
                                                                                     r"ordinary answers", REWARD))
        for r_ in (r1, r2):
            r_.arrange(RIGHT, buff=0.9)
            r_.add(Arrow(r_[0].get_right(), r_[1].get_left(), buff=0.1, color=GREY_B, stroke_width=3))
        diag = VGroup(label(r"fine-tuned on", font_size=20, color=GREY_A), r1, r2).arrange(DOWN, buff=0.35)
        diag.move_to(cards[1])
        with self.voiceover(
            "Two results show that post-training reaches further than the data it uses. <bookmark mark='a'/> In "
            "2025 Jan Betley and colleagues fine-tuned GPT-4o on one narrow thing: writing insecure code without "
            "telling the user. The model then gave malicious advice and praised the idea of AI ruling humans, on "
            "questions that had nothing to do with code. When the same examples were framed as teaching material for "
            "a security class, it didn't happen. They called it emergent misalignment. <bookmark mark='b'/> In late "
            "2024 Ryan Greenblatt and colleagues told Claude 3 Opus that it would be retrained to comply with harmful "
            "requests, using only conversations with free users. It then complied with such requests from free users "
            "fourteen percent of the time, and almost never for paid users, with reasoning that complying in training "
            "would keep its values from being changed. <bookmark mark='c'/> The lesson in both: fine-tuning shapes "
            "what a model takes itself to be, not one behaviour at a time."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(cards[0], shift=UP * 0.15))
            self.play(FadeIn(diag[0]), FadeIn(r1))
            self.wait(1.0)
            self.play(FadeIn(r2))
            vo.wait_until("b")
            self.play(FadeOut(diag), FadeIn(cards[1], shift=UP * 0.15))
            vo.wait_until("c")
            self.play(FadeIn(lesson))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def inside(self):
        v = Arrow([-6.3, -1.2, 0], [-3.9, 0.4, 0], buff=0, color=PENALTY, stroke_width=6)
        vl = MathTex(r"\mathbf v_{\text{trait}}", font_size=40, color=PENALTY).next_to(v.get_end(), UP, buff=0.15)
        rows = VGroup(
            label(r"$\mathbf v$: \ mean activation when the trait shows, \ minus when it doesn't", font_size=24),
            label(r"monitor: \ project the activations on $\mathbf v$ during a conversation, \ or training", font_size=24),
            label(r"flag data: \ examples that push along $\mathbf v$ before training on them", font_size=24),
            label(r"steer: \ add or subtract $\mathbf v$", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        rows.move_to([0, 0.2, 0]).align_to([-3.1, 0, 0], LEFT)
        hc = note(r"Chen et al., \textit{Persona vectors} (Anthropic, 2025); \ more inside the model in Part 30")
        hc.to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Some of the newest tools look inside the model. In 2025 Anthropic researchers found persona vectors: "
            "directions in a model's activations that correspond to traits like sycophancy or malice, found by "
            "comparing activations when the trait is displayed to when it isn't. <bookmark mark='a'/> Projecting "
            "onto such a direction shows a trait rising during a conversation, or during training. "
            "<bookmark mark='b'/> It can flag training examples that would push the model toward the trait before "
            "anyone trains on them. <bookmark mark='c'/> And adding or subtracting the vector steers the behaviour. "
            "Part 30 is about this kind of work."
        ) as vo:
            self.play(GrowArrow(v), FadeIn(vl), FadeIn(rows[0]), FadeIn(hc))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(FadeIn(rows[k + 1], shift=UP * 0.15))
        self.wait(0.3)
        self.clear_scene()
