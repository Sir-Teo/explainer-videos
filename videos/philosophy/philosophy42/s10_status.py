from __future__ import annotations

from videos.philosophy.philosophy42.common import *  # noqa: F403


class Status(VoiceoverScene):
    def construct(self):
        card = chapter_card(9, r"Minds we may be making", r"Could the reasoners we build matter morally?", lit=(2023, 2024), part=PART)
        with self.voiceover("Chapter nine. Minds we may be making."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.indicators()
        self.welfare()
        self.design()
        self.errors()

    def indicators(self):
        head = history_card(2023, r"Butlin, \ Long et al.", r"``Consciousness in Artificial Intelligence''", width=6.0, color=HIST).to_corner(UL, buff=0.3)
        rows = [
                (r"the method", r"derive indicator properties from scientific theories of consciousness, \ and check systems for them", HUMAN),
                (r"the theories", r"global workspace, \ recurrent processing, \ higher-order, \ attention schema, \ agency and embodiment \ (Part 31)", LOBC),
                (r"the verdict", r"no current system was a strong candidate; \ no obvious technical barrier to building one", PROXYC),
                (r"the caveat", r"it assumes computational functionalism, \ which Part 31 left open", RISK)]
        g = rows_table(rows, top=1.0, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "The last question about the reasoners we build is what they are. <bookmark mark='a'/>In 2023 Patrick "
            "Butlin, Robert Long and colleagues took the scientific theories of consciousness from Part 31 and "
            "derived from each a list of indicator properties, then asked which AI systems have them. <bookmark "
            "mark='b'/>The theories were global workspace theory, recurrent processing, higher-order theories, "
            "attention schema theory, and theories stressing agency and embodiment. <bookmark mark='c'/>Their "
            "verdict: no current system was a strong candidate for consciousness, but there were no obvious technical "
            "barriers to building systems that satisfy the indicators. <bookmark mark='d'/>The method assumes "
            "computational functionalism, that the right computations suffice for consciousness, which Part 31 left "
            "as an open bet."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def welfare(self):
        head = label(r"Moral status under uncertainty", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"Long, \ Sebo et al. \ (2024)", r"`Taking AI Welfare Seriously': \ a realistic possibility, \ so acknowledge, \ assess, \ and prepare", TRUEV),
                (r"Birch \ (2024)", r"\textit{The Edge of Sentience}: \ precaution proportionate to the evidence, \ for animals and machines", HUMAN),
                (r"Schwitzgebel and Garza \ (2015)", r"if a machine is psychologically like us, \ it deserves similar consideration", LOBC),
                (r"in practice", r"in 2025 at least one developer began research on model welfare", PROXYC)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "If we are unsure, what should we do? <bookmark mark='a'/>Robert Long, Jeff Sebo and colleagues argued in "
            "2024 that there is a realistic possibility of AI systems with interests of their own in the near future, "
            "and that developers should acknowledge the issue, assess their systems, and prepare policies. <bookmark "
            "mark='b'/>Jonathan Birch's The Edge of Sentience proposes precautions proportionate to the evidence, for "
            "animals, for people with brain injuries, and for machines. <bookmark mark='c'/>Eric Schwitzgebel and "
            "Mara Garza argued that a machine psychologically like us would deserve similar moral consideration, "
            "however it was built. <bookmark mark='d'/>The question has left the seminar: in 2025 at least one "
            "developer began a research programme on the welfare of its models."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def errors(self):
        head = label(r"Two ways to be wrong", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"over-attribution", r"the ELIZA effect \ (Weizenbaum, \ 1966): \ people read minds into simple programs", PROXYC),
                (r"under-attribution", r"history's exclusions; \ animals, \ now widely judged possibly sentient \ (New York Declaration, \ 2024)", RISK),
                (r"the tension", r"a correctable machine must accept being changed or switched off; \ a being with interests might not owe that", ROBOT),
                (r"what we need", r"tests that do not rest on what a system says about itself \ (Part 31)", GOAL)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "There are two ways to be wrong. <bookmark mark='a'/>Over-attribution: Joseph Weizenbaum was disturbed to "
            "see people confide in ELIZA, his simple pattern-matching program of 1966. A fluent system invites us to "
            "see a mind. <bookmark mark='b'/>Under-attribution: history is full of beings whose experiences were "
            "denied, and the New York Declaration of 2024, from Part 31, judged consciousness a realistic possibility "
            "in all vertebrates and many invertebrates. <bookmark mark='c'/>The two concerns of this part can pull "
            "against each other. A corrigible machine must accept being changed or switched off; if it had interests "
            "of its own, would it owe us that? <bookmark mark='d'/>What we need are tests that do not rest on what a "
            "system says about itself, which Part 31 showed is exactly what we do not yet have."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def design(self):
        head = label(r"Designing for uncertainty", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"the excluded middle", r"Schwitzgebel and Garza \ (2020): \ avoid creating systems whose moral status is unclear", LOBC),
                (r"emotional alignment", r"a system should invite the emotional response its real moral status warrants, \ no more and no less", HUMAN),
                (r"a moratorium", r"Metzinger \ (2021): \ do not risk creating artificial suffering until we understand it", RISK),
                (r"the bind", r"if status is unclear, \ every design choice is a bet; \ refusing to choose is one too", GOAL)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "If we cannot yet tell, how should we build? <bookmark mark='a'/>Eric Schwitzgebel and Mara Garza "
            "proposed a design policy of the excluded middle: avoid creating systems whose moral status is genuinely "
            "unclear, because we will either over-treat or under-treat them. <bookmark mark='b'/>Their second policy "
            "is emotional alignment: a system should invite the emotional responses its real moral status warrants, "
            "neither seeming a person if it is a tool nor seeming a tool if it is more. <bookmark mark='c'/>Thomas "
            "Metzinger argued for a moratorium on research that risks creating artificial suffering until we "
            "understand consciousness better. <bookmark mark='d'/>Each proposal is a bet under uncertainty, and the "
            "moral uncertainty of Part 35 applies: refusing to choose is itself a choice."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
