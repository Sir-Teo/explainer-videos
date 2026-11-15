from __future__ import annotations

from videos.psychology.psych30.common import *  # noqa: F403


class Attachment(VoiceoverScene):
    def construct(self):
        self.card()
        self.harlow()
        self.strange()
        self.predicts()

    def card(self):
        card = chapter_card(10, r"Attachment", r"What does an infant need from a caregiver?",
                            lit={1958: r"Harlow", 1969: r"Bowlby", 1978: r"Ainsworth et al.",
                                 1988: r"van IJzendoorn \& Kroonenberg", 2010: r"Fearon et al."},
                            part=PART, scale=("person", "group"), marr=("what",))
        with self.voiceover("Chapter ten. Attachment."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def harlow(self):
        head = heading(r"Cloth and wire")
        wire = VGroup(*[Line([-5.4 + 0.15 * i, -1.6, 0], [-5.4 + 0.15 * i, 1.0, 0], color=GREY_B) for i in range(7)])
        bottle = RoundedRectangle(corner_radius=0.08, width=0.3, height=0.6, color=WHITE).move_to([-4.6, 0.5, 0])
        cloth = RoundedRectangle(corner_radius=0.4, width=1.2, height=2.6, color=CARE, fill_color=CARE,
                                 fill_opacity=0.5).move_to([-2.4, -0.3, 0])
        wl = label(r"wire, \ with milk", font_size=17, color=GREY_B).next_to(wire, DOWN, buff=0.15)
        cl = label(r"cloth, \ no milk", font_size=17, color=CARE).next_to(cloth, DOWN, buff=0.15)
        rows = rows_of([
            (r"Harry Harlow, \ 1958: \ infant rhesus monkeys raised with two surrogate mothers, \ one of bare wire, "
             r"\ one covered in cloth; \ for some, \ only the wire one gave milk", WHITE),
            (r"they fed from the wire mother and spent most of the day clinging to the cloth one; \ frightened, \ "
             r"they ran to cloth", CARE),
            (r"against the drive theories of Part 28: \ comfort, \ not food, \ made the bond", GOOD),
            (r"the experiments, \ and Harlow's later isolation studies, \ caused lasting harm, \ and are a reason "
             r"for today's rules on animal research", LOST),
        ], 5.6, 21, 0.32).move_to([3.4, -0.1, 0])
        tag = historical_tag(r"Harlow (1958)")
        with self.voiceover(
            "The infant mind is also a social one, and its first relationship has been studied hard. "
            "<bookmark mark='a'/> In 1958 Harry Harlow raised infant rhesus monkeys with two surrogate mothers, one "
            "of bare wire and one covered in cloth. For some infants, only the wire mother gave milk. "
            "<bookmark mark='b'/> They fed from the wire mother, and spent most of the day clinging to the cloth "
            "one. Frightened, they ran to the cloth. <bookmark mark='c'/> It went against the drive theories of Part "
            "28: comfort, not food, made the bond. <bookmark mark='d'/> These experiments, and Harlow's later "
            "isolation studies, caused lasting harm to the animals, and are one of the reasons for today's rules on "
            "animal research."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), Create(wire), FadeIn(bottle), FadeIn(cloth), FadeIn(wl),
                      FadeIn(cl))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def strange(self):
        head = heading(r"The Strange Situation")
        steps = [r"parent and infant in a playroom", r"a stranger enters", r"the parent leaves",
                 r"the parent returns", r"the infant is left alone", r"the stranger returns", r"the parent returns"]
        chips = VGroup(*[word_chip(rf"{i + 1}. \ {s}", color=CARE if "returns" in s and "parent" in s else WHITE,
                                   font_size=17, width=4.6) for i, s in enumerate(steps)])
        chips.arrange(DOWN, buff=0.12).move_to([-3.6, -0.2, 0])
        rows = rows_of([
            (r"John Bowlby: \ attachment is an evolved system that keeps an infant near a protector, \ and "
             r"gives it a secure base to explore from", WHITE),
            (r"Mary Ainsworth's Strange Situation, \ about 20 minutes: \ the key moments are the reunions", CARE),
            (r"secure: \ upset, \ comforted, \ back to play; \ avoidant: \ ignores the parent's return; \ "
             r"resistant: \ upset and hard to comfort; \ later, \ disorganized \ (Main \& Solomon)", MIND),
            (r"Marinus van IJzendoorn and Pieter Kroonenberg, \ 1988: \ 32 samples, \ 8 countries, \ 1{,}990 "
             r"infants: \ secure was the most common pattern everywhere, \ and variation within countries was "
             r"larger than between them", NUM),
        ], 5.6, 20, 0.3).move_to([3.4, -0.1, 0])
        tag = published_tag(r"Ainsworth et al.\ (1978); \ van IJzendoorn \& Kroonenberg (1988)")
        with self.voiceover(
            "John Bowlby turned bonds like these into a theory. <bookmark mark='a'/> Attachment, for Bowlby, is an "
            "evolved system that keeps an infant near a protector, and gives it a secure base from which to "
            "explore. <bookmark mark='b'/> Mary Ainsworth made it measurable with the Strange Situation, about "
            "twenty minutes of separations and reunions in a playroom. The key moments are the reunions. "
            "<bookmark mark='c'/> A secure infant is upset, is comforted, and goes back to play. An avoidant infant "
            "ignores the parent's return. A resistant infant is upset and hard to comfort. A fourth pattern, "
            "disorganized, was added later by Mary Main and Judith Solomon. <bookmark mark='d'/> In 1988 Marinus van "
            "IJzendoorn and Pieter Kroonenberg pooled thirty-two samples from eight countries, nearly two thousand "
            "infants. Secure was the most common pattern everywhere, and variation within countries was larger than "
            "variation between them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), LaggedStart(*[FadeIn(c) for c in chips], lag_ratio=0.2))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def predicts(self):
        head = heading(r"What early attachment predicts")
        rows = rows_of([
            (r"popular accounts: \ the first year sets a child's relationships for life", LOST),
            (r"Pasco Fearon and colleagues, \ 2010: \ a meta-analysis of 69 samples, \ nearly 6{,}000 children: \ "
             r"insecure attachment goes with later behaviour problems, \ $d = 0.31$", NUM),
            (r"real, \ and modest: \ most insecurely attached infants do not develop problems, \ and attachment can "
             r"change as circumstances change", CARE),
            (r"the measure is a short observation of one relationship, \ at one age: \ Part 3's reliability "
             r"limits apply", GREY_A),
        ], 12.2, 25, 0.4).move_to([0, -0.2, 0])
        tag = published_tag(r"Fearon et al.\ (2010)")
        with self.voiceover(
            "What does it predict? <bookmark mark='a'/> Popular accounts say the first year sets a child's "
            "relationships for life. <bookmark mark='b'/> In 2010 Pasco Fearon and colleagues pooled sixty-nine "
            "samples, nearly six thousand children. Insecure attachment went with later behaviour problems, with a "
            "d of 0.31. <bookmark mark='c'/> That is real, and modest. Most insecurely attached infants do not "
            "develop problems, and attachment can change as circumstances change. <bookmark mark='d'/> And the "
            "measure is a short observation of one relationship at one age, so Part 3's limits on reliability "
            "apply."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
