from __future__ import annotations

from videos.psychology.psych4.common import *  # noqa: F403


class Fraud(VoiceoverScene):
    def construct(self):
        self.card()
        self.stapel()

    def card(self):
        card = chapter_card(8, r"Fraud is the smaller problem", r"How much of this was dishonesty?",
                            lit={2011: r"the Stapel affair"}, part=PART, scale=("person", "culture"),
                            marr=("what",))
        with self.voiceover(
            "Chapter eight. Fraud is the smaller problem."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def stapel(self):
        d = archive.LEVELT_2012.data
        head = heading(rf"{d['exposed']}: \ the same year, a different kind of failure")
        papers = tiles(d["publications_with_fraud"], d["publications_with_fraud"], BAD, size=0.36, buff=0.09, cols=11)
        papers.move_to([-3.8, 0.9, 0])
        cap = VGroup(label(rf"{d['publications_with_fraud']} publications", font_size=34, color=BAD),
                     wrapped_label(r"with invented or altered data, by one social psychologist", 4.6, 24, GREY_A))
        cap.arrange(DOWN, buff=0.1).next_to(papers, DOWN, buff=0.3)
        table = VGroup()
        rows = [(r"", r"fabrication", r"flexibility"),
                (r"the data", r"invented", r"real"),
                (r"the person", r"knows it is false", r"believes it is true"),
                (r"how common", r"rare", r"ordinary practice"),
                (r"the remedy", r"detection, sanction", r"a change of procedure")]
        for i, (a, b, c) in enumerate(rows):
            y = 1.95 - 0.62 * i
            hdr = i == 0
            table.add(VGroup(
                label(a, font_size=24, color=GREY_A).move_to([1.2, y, 0], aligned_edge=LEFT),
                label(b, font_size=28 if hdr else 26, color=BAD if hdr else WHITE).move_to([3.0, y, 0], aligned_edge=LEFT),
                label(c, font_size=28 if hdr else 26, color=SIG if hdr else WHITE).move_to([5.6, y, 0], aligned_edge=LEFT)))
        keep_in_frame(table)
        quote = quote_card(r"``A general culture of careless, selective and uncritical handling of research and "
                           r"data.''", r"the committees of inquiry, on the field around the fraud (2012)", width=11.6,
                           font_size=28, color=KANT).to_edge(DOWN, buff=0.6)
        src = published_tag(archive.LEVELT_2012.cite)
        with self.voiceover(
            "A few months after Bem's paper, the field had a second shock, and it helps to keep the two apart. "
            "<bookmark mark='a'/> A prominent Dutch social psychologist, Diederik Stapel, was found to have been "
            "making up his data. Three committees of inquiry went through his work and established fraud in "
            f"{d['publications_with_fraud']} publications. He lost his post, and the papers were retracted. "
            "<bookmark mark='b'/> That's fabrication, and it's a different thing from everything else in this "
            "part. The fabricator invents data and knows the result is false. The researcher with flexible "
            "methods has real data and believes the result is true. Fabrication is rare, and the remedy is to "
            "catch it. Flexibility was ordinary practice, and no amount of catching will help, because there's "
            "nobody to catch. <bookmark mark='c'/> The committees saw the connection. They said the fraud had "
            "gone unnoticed for years because it sat in a wider culture of careless, selective and uncritical "
            "handling of research and data. Results that were too good raised no questions, because good "
            "results were what everyone produced. A field's defences against the dishonest few are only as "
            "strong as its habits among the honest many."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(papers, lag_ratio=0.02), run_time=2.0)
            self.play(FadeIn(cap))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in table], lag_ratio=0.8), run_time=16.0)
            vo.wait_until("c")
            self.play(FadeIn(quote, shift=UP * 0.2))
        self.clear_scene()
