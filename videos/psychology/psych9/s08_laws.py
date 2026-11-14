from __future__ import annotations

import numpy as np

from videos.psychology.psych9.common import *  # noqa: F403


class Laws(VoiceoverScene):
    def construct(self):
        self.card()
        self.laws()
        self.puzzle()

    def card(self):
        card = chapter_card(7, r"Three laws and a puzzle", r"If genes are half, what is the other half?",
                            lit={2000: r"three laws"}, part=PART, scale=("person", "group"), marr=("what",))
        with self.voiceover(
            "Chapter seven. Three laws and a puzzle."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def laws(self):
        t = archive.TURKHEIMER_2000.data
        pm = archive.POLDERMAN_2015.data
        head = heading(r"2000: \ three laws of behaviour genetics")
        cols = (GENE, HOME, OWN)
        rows = VGroup(*[VGroup(label(str(i + 1), font_size=54, color=c), wrapped_label(txt, 10.6, 32, WHITE)).arrange(
            RIGHT, buff=0.5) for i, (txt, c) in enumerate(zip(t["laws"], cols))]).arrange(DOWN, aligned_edge=LEFT, buff=0.42)
        rows.move_to([0, 1.2, 0])
        stats_ = VGroup(
            big_number(rf"{pm['traits']:,}".replace(",", "{,}"), r"traits", DATA, font_size=50, width=3.0),
            big_number(r"14.5 million", r"pairs of twins", DATA, font_size=50, width=3.6),
            big_number(pct(pm["h2"]), r"mean heritability", GENE, font_size=50, width=3.6),
            big_number(pct(pm["additive_share"]), r"of traits fit the simple additive model", GENE, font_size=50, width=3.8),
        ).arrange(RIGHT, buff=0.55, aligned_edge=UP).move_to([0, -2.1, 0])
        keep_in_frame(stats_)
        src = published_tag(archive.TURKHEIMER_2000.cite + r"; \ " + archive.POLDERMAN_2015.cite)
        with self.voiceover(
            "By the year 2000, twin and adoption studies had piled up so consistently that the "
            "psychologist Eric Turkheimer summed them up as three laws. <bookmark mark='a'/> First: all "
            "human behavioural traits are heritable. Not that genes fix them. That in every population "
            "studied, some of the differences go with genes. <bookmark mark='b'/> Second: the effect of "
            "being raised in the same family is smaller than the effect of genes. <bookmark mark='c'/> "
            "Third: a substantial part of the variation is accounted for by neither. "
            f"<bookmark mark='d'/> In 2015 a team pooled fifty years of twin studies: {pm['traits']:,} "
            "traits, and more than fourteen million pairs of twins. The average heritability was "
            f"{100 * pm['h2']:.0f} percent, and for about two thirds of the traits the simple additive "
            "model was enough. The first law has held. As laws of psychology go, it's one of the best "
            "replicated we have."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), *[FadeIn(r[0]) for r in rows])
            vo.wait_until("a")
            self.play(FadeIn(rows[0][1], shift=RIGHT * 0.15))
            vo.wait_until("b")
            self.play(FadeIn(rows[1][1], shift=RIGHT * 0.15))
            vo.wait_until("c")
            self.play(FadeIn(rows[2][1], shift=RIGHT * 0.15))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(s, shift=UP * 0.1) for s in stats_], lag_ratio=0.6), run_time=5.0)
        self.clear_scene()

    def puzzle(self):
        tw = load("twins")
        head = heading(r"The puzzle of the other half")
        ad = VGroup(little_person(0.9, HOME), little_person(0.9, DZC)).arrange(RIGHT, buff=0.12)
        mz = twin_pair(MZC, True, 0.9)
        items = [
            (ad, r"adoptive brothers and sisters", r"one home from infancy, \ no genes in common: \ as adults, hardly more "
                                                    r"alike in personality than strangers", HOME),
            (mz, r"identical twins raised together", rf"the same genes and the same home: \ a correlation of "
                                                      rf"${tw['r_mz']:.2f}$ on the registry, \ so {pct(tw['est_e2'])} of the "
                                                      r"differences have neither cause", MZC),
        ]
        rows = VGroup()
        for i, (icon, name, what, col) in enumerate(items):
            y = 2.0 - 1.45 * i
            icon.move_to([-5.9, y, 0])
            txt = VGroup(label(name, font_size=33, color=col), wrapped_label(what, 10.4, 29, WHITE)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.1)
            txt.move_to([0, y, 0]).align_to(np.array([-4.9, 0, 0]), LEFT)
            rows.add(VGroup(icon, txt))
        rest = rows_of([
            (r"what is in the remainder? \ measurement error; \ experiences brothers and sisters do not share; \ chance in "
             r"how a brain grows. \ Most of it has not been pinned down.", OWN),
            (r"two cautions: \ the studies cover ordinary homes, not neglect or abuse; \ and the home decides your "
             r"language, your religion, and much of your schooling.", P.ACCENT),
        ], 12.4, 30, 0.25).move_to([0, -1.9, 0])
        tag = simulated_tag(r"the twins' numbers: the Pool's registry")
        with self.voiceover(
            "The second and third laws are the surprising ones. <bookmark mark='a'/> Common sense says the "
            "home matters most: the parents you had, their money, their rules, their books. But adoption "
            "studies keep finding that adoptive brothers and sisters, raised in one home from infancy, are "
            "by adulthood hardly more alike in personality than strangers. <bookmark mark='b'/> And "
            "identical twins, with the same genes and the same home, are far from the same person. On "
            f"our registry their correlation is {tw['r_mz']:.2f}, which leaves "
            f"{100 * tw['est_e2']:.0f} percent of the differences with neither cause. "
            "<bookmark mark='c'/> What's in that remainder? Partly the error of the measurement. Partly "
            "experiences that brothers and sisters don't share: a friend, a teacher, an illness. Partly, "
            "it seems, chance in how a brain grows. Most of it has never been pinned down. "
            "<bookmark mark='d'/> Two cautions, before anyone concludes that parents don't matter. These "
            "studies cover the range of homes that get into studies, which rarely includes neglect or "
            "abuse. And a small effect on a personality score isn't a small effect on a life. The home "
            "decides the language you speak and the religion you were taught, and for schooling, as you "
            "saw, the home's share is as large as the genes'."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(rows[0][0]), FadeIn(rows[0][1][0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[0][1][1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rest[0]))
            vo.wait_until("d")
            self.play(FadeIn(rest[1], shift=UP * 0.1))
        self.clear_scene()
