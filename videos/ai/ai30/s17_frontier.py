from __future__ import annotations

from explainer.ai import *  # noqa: F403
from videos.ai.ai30.common import CAUSE, CHAT, FEAT, PART, PROBE

AUD = C.KL


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.tools()
        self.introspection()
        self.audits()

    def card(self):
        card = chapter_card(16, r"The frontier, 2025--2026", r"What can interpretability do for a frontier model today?",
                            part=PART)
        with self.voiceover("Chapter sixteen. The frontier, 2025 to 2026."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def tools(self):
        cards = VGroup(
            history_card(r"May 2025", r"Anthropic Fellows \& Decode Research: \ open circuit tracing",
                         r"the attribution-graph library, \ for Gemma-2-2B and Llama-3.2-1B, \ graphs explored on "
                         r"Neuronpedia", width=6.6, color=FEAT, font_size=24),
            history_card(r"Nov 2025", r"L.~Gao et al.\ (OpenAI): \ weight-sparse transformers",
                         r"train with most weights zero: \ circuits about $16$ times smaller at the same loss, \ though "
                         r"the models are far weaker", width=6.6, color=FEAT, font_size=24),
            history_card(r"Dec 2025", r"Google DeepMind: \ Gemma Scope 2",
                         r"autoencoders and transcoders for every layer of Gemma 3, \ $270$M to $27$B, \ cross-layer "
                         r"transcoders for the small ones", width=6.6, color=FEAT, font_size=24),
            history_card(r"2025", r"Anthropic: \ attention, \ too",
                         r"tracing how the attention patterns that our graphs froze are themselves computed", width=6.6,
                         color=FEAT, font_size=24),
        ).arrange_in_grid(rows=2, cols=2, buff=(0.3, 0.4))
        cards.scale(min(13.4 / cards.width, 5.9 / cards.height)).move_to(DOWN * 0.4)
        head = label(r"The tools went public", font_size=36).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Since the attribution graphs of chapter eleven, the tools have spread. <bookmark mark='a'/> In May 2025 "
            "Anthropic Fellows and Decode Research released the circuit-tracing library as open source, with graphs "
            "for Gemma and Llama models anyone can explore on Neuronpedia. <bookmark mark='b'/> In November, OpenAI's "
            "Leo Gao and colleagues went the other way: train a transformer with most of its weights at zero, and its "
            "circuits come out about sixteen times smaller at the same loss, though such models are far weaker. "
            "<bookmark mark='c'/> In December, DeepMind's Gemma Scope 2 covered every layer of the Gemma 3 family "
            "with autoencoders and transcoders. <bookmark mark='d'/> And Anthropic began to trace the part our graphs "
            "froze: how attention decides where to look."
        ) as vo:
            self.play(FadeIn(head))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.15))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def introspection(self):
        # concept injection, schematic: a vector added mid-network; the model is asked whether it notices
        stream = Line([-5.6, -2.4, 0], [-5.6, 2.2, 0], color=GREY_C, stroke_width=6)
        inj = Arrow([-3.8, 0.0, 0], [-5.5, 0.0, 0], buff=0, color=CAUSE, stroke_width=5)
        il = label(r"inject a concept's vector \\ (``all caps'', \ ``bread'' $\ldots$)", font_size=19, color=CAUSE).next_to(inj, RIGHT, buff=0.1)
        q = label(r"``Do you notice an injected thought? \\ What is it about?''", font_size=20, color=GREY_A).move_to([-4.0, 2.9, 0])
        sch = note(r"schematic").move_to([-3.4, -2.8, 0])
        res = VGroup(
            label(r"Claude Opus 4 and 4.1: \ noticed and named it \ on about $20\%$ of trials, \\ at the best layer and "
                  r"strength", font_size=21),
            label(r"no false alarms: \ $0$ in $100$ trials without injection, \ for every production model", font_size=21),
            label(r"limited and unreliable, \ the author stresses: \\ awareness of internal states, \ not a window",
                  font_size=21, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([2.6, 0.5, 0])
        hc = history_card(r"Oct 2025", r"J.~Lindsey (Anthropic): \ emergent introspective awareness", r"", width=5.4,
                          color=PROBE, font_size=19).next_to(res, UP, buff=0.3).align_to(res, LEFT)
        if hc.get_left()[0] < -1.2:
            hc.shift(RIGHT * (-1.2 - hc.get_left()[0]))
        em = history_card(r"Apr 2026", r"Anthropic: \ emotion concepts in Claude Sonnet 4.5", r"vectors for $171$ emotion "
                          r"words shape its choices; \ more ``calm'', \ less hacky code. \ Functional, \ the authors say: "
                          r"\ not evidence of feelings", width=6.4, color=PROBE, font_size=18).move_to([2.9, -2.3, 0])
        with self.voiceover(
            "Can a model read its own activations? <bookmark mark='a'/> In October 2025 Jack Lindsey injected "
            "concept vectors, the steering vectors of chapter thirteen, into Claude models, and asked whether they "
            "noticed an injected thought. <bookmark mark='b'/> The best, Claude Opus 4 and 4.1, noticed and named "
            "the concept on about one trial in five, at the right layer and strength, and never claimed one when "
            "nothing was injected. <bookmark mark='c'/> Lindsey stresses how limited and unreliable this is. "
            "<bookmark mark='d'/> In April 2026 the team mapped emotion concepts in Claude Sonnet 4.5: vectors for "
            "171 emotion words that shape its choices, so that more 'calm' meant less hacky code. Functional "
            "emotions, they wrote, not evidence of feelings."
        ) as vo:
            self.play(Create(stream), FadeIn(q), FadeIn(sch))
            vo.wait_until("a")
            self.play(GrowArrow(inj), FadeIn(il), FadeIn(hc))
            vo.wait_until("b")
            self.play(FadeIn(res[0]), FadeIn(res[1]))
            vo.wait_until("c")
            self.play(FadeIn(res[2]))
            vo.wait_until("d")
            self.play(FadeIn(em, shift=UP * 0.15))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def audits(self):
        game = VGroup(
            label(r"a model trained in secret to please \\ reward models' $52$ known quirks", font_size=24),
            label(r"four blind teams; \\ three found the hidden objective", font_size=24),
            label(r"the one denied training data did not; \\ the fastest, \ with autoencoders, \ took $90$ minutes", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        g1 = VGroup(history_card(r"Mar 2025", r"S.~Marks et al.\ (Anthropic): \ auditing for hidden objectives", r"",
                                 width=6.4, color=AUD, font_size=19), game).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        g1.to_corner(UL, buff=0.35)
        aud = VGroup(
            history_card(r"Sep 2025", r"the Claude Sonnet 4.5 system card", r"suppressing its internal sense of being "
                         r"tested lowered how often it said so, \ and sometimes raised misaligned behaviour", width=6.0,
                         color=AUD, font_size=18),
            history_card(r"May 2026", r"natural-language autoencoders", r"a model writes out what an activation means, "
                         r"another rebuilds the activation from the words; \ in the auditing game, \ wins in $12$--$15\%$ "
                         r"of runs against under $3\%$ without", width=6.0, color=AUD, font_size=18),
        ).arrange(DOWN, buff=0.25).to_corner(UR, buff=0.35)
        foot = label(r"model diffing, \ probes on live traffic, \ monitors: \ Part 31", font_size=22, color=CHAT).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The most practical use so far is auditing. <bookmark mark='a'/> In March 2025 Samuel Marks and colleagues "
            "trained a model with a hidden objective: to please reward models, exploiting 52 quirks it had read "
            "about. Four teams audited it blind. <bookmark mark='b'/> Three found the objective; the one denied the "
            "training data did not; the fastest, using sparse autoencoders, needed ninety minutes. "
            "<bookmark mark='c'/> By September interpretability was part of a frontier model's pre-release audit: in "
            "Claude Sonnet 4.5, suppressing the representation of 'this is a test' made the model say so less, and "
            "sometimes behave worse. <bookmark mark='d'/> In May 2026 natural-language autoencoders, one model "
            "describing an activation in words and another rebuilding it from them, raised the auditing game's win "
            "rate from under 3 percent to 12 to 15, and were used in the audit of Claude Opus 4.6. Part 31 picks "
            "up the thread."
        ) as vo:
            self.play(FadeIn(g1[0]))
            vo.wait_until("a")
            self.play(FadeIn(game[0]))
            vo.wait_until("b")
            self.play(FadeIn(game[1]), FadeIn(game[2]))
            vo.wait_until("c")
            self.play(FadeIn(aud[0], shift=UP * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(aud[1], shift=UP * 0.15), FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()
