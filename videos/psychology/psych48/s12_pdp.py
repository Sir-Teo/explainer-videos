from __future__ import annotations

from videos.psychology.psych48.common import *  # noqa: F403


class Pdp(VoiceoverScene):
    def construct(self):
        self.card()
        self.networks()
        self.tests()

    def card(self):
        card = chapter_card(11, r"Connectionism", r"What did neural networks add, \ and what did they cost?",
                            lit={1986: r"Rumelhart \& McClelland"}, part=PART, scale=("circuit", "mind"),
                            marr=("how",))
        with self.voiceover("Chapter eleven. Connectionism."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def networks(self):
        head = heading(r"Parallel distributed processing")
        layers = VGroup()
        for n, x in ((4, -5.2), (5, -3.6), (3, -2.0)):
            col = VGroup(*[Circle(radius=0.16, color=MODEL, stroke_width=2) for _ in range(n)]).arrange(DOWN, buff=0.35)
            col.move_to([x, 0.4, 0])
            layers.add(col)
        edges = VGroup(*[Line(a.get_center(), b.get_center(), stroke_width=0.8, color=GREY_B)
                         for l1, l2 in zip(layers[:-1], layers[1:]) for a in l1 for b in l2])
        rows = rows_of([
            (r"1986: \ Rumelhart, \ McClelland and the PDP group model cognition as many simple units, \ with "
             r"knowledge in the weights between them, \ learned from examples", WHITE),
            (r"what networks added: \ graded, \ learned representations; \ rules that emerge without being written; "
             r"\ damage that degrades gracefully", GOOD),
            (r"what they cost: \ a fitted network can be as hard to understand as the mind it models; \ and learning "
             r"something new can erase the old (Part 21's catastrophic interference)", AUTH),
            (r"the past-tense debate, \ rules against networks, \ ran for decades; \ today's language models are its "
             r"heirs", PERSON),
        ], 6.4, 19, 0.38).move_to([3.2, -0.1, 0])
        tag = published_tag(r"Rumelhart, McClelland \& the PDP Group (1986)")
        with self.voiceover(
            "A different kind of model came with the 1980s. <bookmark mark='a'/> In 1986 David Rumelhart, James "
            "McClelland and the PDP group modelled cognition as many simple units, with knowledge stored in the "
            "weights between them, learned from examples. <bookmark mark='b'/> What networks added: graded, learned "
            "representations, rules that emerge without being written, and damage that degrades gracefully. "
            "<bookmark mark='c'/> What they cost: a fitted network can be as hard to understand as the mind it "
            "models, and learning something new can erase the old, Part 21's catastrophic interference. "
            "<bookmark mark='d'/> The debate over rules and networks, starting with the English past tense, ran for "
            "decades. Today's language models are its heirs."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(layers), FadeIn(edges))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def tests(self):
        chips_section(self, r"What a network model is tested against", [
            (r"the past tense", r"Rumelhart and McClelland's network learned English past tenses with a dip, \ "
                                r"``goed'' after ``went'', \ like children; \ Pinker and Prince argued the dip came "
                                r"from how the training was staged", AUTH),
            (r"reading aloud", r"the triangle model (Seidenberg and McClelland, \ 1989) read regular and irregular "
                               r"words with one set of weights, \ and predicted their naming times", MODEL),
            (r"damage", r"lesioned networks lose specific knowledge first and general knowledge last, \ as in "
                        r"semantic dementia (Part 21)", PERSON),
            (r"the standard", r"a network earns its place by predicting the pattern of errors and times, \ not "
                              r"by being accurate", GOOD),
        ], "So what is a network model tested against? <bookmark mark='a'/> The past tense. Rumelhart and "
           "McClelland's network learned English past tenses with a dip, saying goed after it had said went, as "
           "children do. Steven Pinker and Alan Prince argued that the dip came from how the training was staged. "
           "<bookmark mark='b'/> Reading aloud. Mark Seidenberg and McClelland's triangle model read regular and "
           "irregular words with one set of weights, and predicted their naming times. <bookmark mark='c'/> Damage. "
           "Lesioned networks lose specific knowledge first and general knowledge last, as people with semantic "
           "dementia do. <bookmark mark='d'/> The standard is the same as for any model in this part. A network "
           "earns its place by predicting the pattern of errors and times, not by being accurate.",
           chip_w=3.2, text_w=9.0)
