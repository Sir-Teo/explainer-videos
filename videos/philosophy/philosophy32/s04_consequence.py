from __future__ import annotations

from videos.philosophy.philosophy32.common import *  # noqa: F403


class Consequence(VoiceoverScene):
    def construct(self):
        card = chapter_card(3, r"The consequence argument", r"Is it up to us what follows from the past and the "
                                                             r"laws?", lit=(1983,), part=PART)
        with self.voiceover("Chapter three. The consequence argument."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.informal()
        self.operator()
        self.derivation()

    def informal(self):
        q = quote_card(r"If determinism is true, \ then our acts are the consequences of the laws of nature and events "
                       r"in the remote past. \ But it is not up to us what went on before we were born, \ and neither "
                       r"is it up to us what the laws of nature are. \ Therefore, \ the consequences of these things "
                       r"\ (including our present acts) \ are not up to us.", r"Peter van Inwagen",
                       r"\textit{An Essay on Free Will} \ (1983)", width=10.6, font_size=25).to_edge(UP, buff=0.5)
        rows = stack([(r"the past: \ not up to us", LAW), (r"the laws: \ not up to us", LAW),
                      (r"so what follows from them: \ not up to us", BAD)], font_size=22, buff=0.25).to_edge(
            DOWN, buff=0.6)
        with self.voiceover(
            "The strongest argument that freedom and determinism cannot both be true is Peter van Inwagen's. "
            "<bookmark mark='a'/>In his words: if determinism is true, then our acts are the consequences of the "
            "laws of nature and events in the remote past. But it is not up to us what went on before we were born, "
            "and neither is it up to us what the laws of nature are. Therefore, the consequences of these things, "
            "including our present acts, are not up to us. <bookmark mark='b'/>The past is not up to us. "
            "<bookmark mark='c'/>The laws are not up to us. <bookmark mark='d'/>So nothing that follows from them is "
            "up to us, and if determinism is true, that is everything."
        ) as vo:
            self.play(FadeIn(q))
            vo.wait_until("a")
            for mk, r in zip("bcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def operator(self):
        head = label(r"An operator for `no choice'", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        d = MathTex(r"N p \;:\; p, \ \text{and no one has, \ or ever had, \ any choice about whether } p",
                    font_size=32, color=FUNC).move_to([0, 1.8, 0])
        rules = VGroup(
            VGroup(label(r"rule $\alpha$", font_size=24, color=SELF),
                   MathTex(r"\Box p \;\vdash\; N p", font_size=34, color=WHITE),
                   label(r"no one has a choice about what is necessary", font_size=19, color=GREY_A)),
            VGroup(label(r"rule $\beta$", font_size=24, color=SELF),
                   MathTex(r"N p, \;\; N(p \rightarrow q) \;\vdash\; N q", font_size=34, color=WHITE),
                   label(r"no choice about $p$, \ nor about its leading to $q$: \ no choice about $q$", font_size=19,
                         color=GREY_A)))
        for r in rules:
            r.arrange(RIGHT, buff=0.5)
        rules.arrange(DOWN, buff=0.6, aligned_edge=LEFT).move_to([0, -0.2, 0])
        foot = label(r"both look like logic; \ the argument needs nothing else but the fixity of past and laws",
                     font_size=20, color=GOAL).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "To make the argument exact, van Inwagen introduced an operator. <bookmark mark='a'/>N p means: p is "
            "true, and no one has, or ever had, any choice about whether p. <bookmark mark='b'/>Two rules govern "
            "it. Rule alpha: from the necessity of p, infer N p. No one has a choice about what is necessary, "
            "about two plus two being four. <bookmark mark='c'/>Rule beta: from N p, and N of p implies q, infer N "
            "q. If no one has a choice about p, and no one has a choice about p's leading to q, then no one has a "
            "choice about q. <bookmark mark='d'/>Both look like pieces of logic. With them, and the claim that the "
            "past and the laws are fixed, the argument goes through."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(d))
            vo.wait_until("b")
            self.play(FadeIn(rules[0]))
            vo.wait_until("c")
            self.play(FadeIn(rules[1]))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def derivation(self):
        head = label(r"The argument, \ formally", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        lines = [(r"1.", r"\Box\big((P_0 \wedge L) \rightarrow P\big)", r"determinism", LAW),
                 (r"2.", r"\Box\big(P_0 \rightarrow (L \rightarrow P)\big)", r"from 1, \ by logic", GREY_A),
                 (r"3.", r"N\big(P_0 \rightarrow (L \rightarrow P)\big)", r"from 2, \ rule $\alpha$", SELF),
                 (r"4.", r"N P_0", r"the past is fixed", LAW),
                 (r"5.", r"N(L \rightarrow P)", r"from 3 and 4, \ rule $\beta$", SELF),
                 (r"6.", r"N L", r"the laws are fixed", LAW),
                 (r"7.", r"N P", r"from 5 and 6, \ rule $\beta$", BAD)]
        rows = VGroup()
        for k, (n, f, why, c) in enumerate(lines):
            y = 2.0 - 0.62 * k
            rows.add(VGroup(label(n, font_size=21, color=GREY_A).move_to([-5.6, y, 0]),
                            MathTex(f, font_size=30, color=c).move_to([-5.1, y, 0], aligned_edge=LEFT),
                            label(why, font_size=19, color=GREY_A).move_to([1.6, y, 0], aligned_edge=LEFT)))
        key = label(r"$P_0$: \ the remote past \quad $L$: \ the laws \quad $P$: \ anything true, \ say `I raised my "
                    r"hand'", font_size=19, color=GREY_A).to_edge(DOWN, buff=0.45)
        betas = VGroup(*[SurroundingRectangle(rows[k][2], color=SELF, buff=0.08) for k in (4, 6)])
        with self.voiceover(
            "Here is the whole argument. <bookmark mark='a'/>Let P nought describe the world in the remote past, L "
            "be the laws, and P any truth at all, say that I raised my hand. Determinism says that the past and the "
            "laws together necessitate P. <bookmark mark='b'/>By logic, the past necessitates that the laws imply "
            "P. <bookmark mark='c'/>By rule alpha, no one has a choice about that. <bookmark mark='d'/>No one has a "
            "choice about the remote past. <bookmark mark='e'/>So, by rule beta, no one has a choice about whether "
            "the laws imply P. <bookmark mark='f'/>No one has a choice about the laws. <bookmark mark='g'/>So, by "
            "rule beta again, no one has a choice about whether I raised my hand, or about anything else. "
            "<bookmark mark='h'/>Every step but two is uncontroversial. The two uses of rule beta are where, in "
            "1996, the argument was found to break."
        ) as vo:
            self.play(FadeIn(head), FadeIn(key))
            for mk, r in zip("abcdefg", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("h")
            self.play(Create(betas))
        self.clear_scene()
