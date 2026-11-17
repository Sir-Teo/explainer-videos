from __future__ import annotations

import numpy as np

from videos.psychology.psych9.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        self.card()
        self.counselling()
        self.consumer()
        self.embryo()
        self.questions()

    def card(self):
        card = chapter_card(13, r"In practice: what a genetic test can deliver", r"When is a test a diagnosis, and when a hint?",
                            lit=(), part=PART, scale=("person",), marr=("what",))
        with self.voiceover(
            "Chapter thirteen. In practice: what a genetic test can deliver."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def counselling(self):
        head = heading(r"Two kinds of genetic test")
        left = VGroup(
            label(r"one gene, or one chromosome", font_size=36, color=GENE),
            wrapped_label(r"Huntington's disease, \ cystic fibrosis, \ Down syndrome", 5.6, 30, WHITE),
            wrapped_label(r"the test is close to a diagnosis", 5.6, 30, GENE),
            wrapped_label(r"genetic counselling: \ helping a family understand a probability, \ and decide", 5.6, 30, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([-3.5, 0.3, 0])
        right = VGroup(
            label(r"thousands of positions", font_size=36, color=THRESH),
            wrapped_label(r"schooling, \ test scores, \ personality, \ most psychiatric diagnoses", 5.6, 30, WHITE),
            wrapped_label(r"the test is a polygenic score", 5.6, 30, THRESH),
            wrapped_label(r"and you know what a score can say", 5.6, 30, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.5, 0.3, 0])
        right.align_to(left, UP)
        end = wrapped_label(r"The counsellor's skills are psychological: \ how people understand risk (Part 26), \ and how "
                            r"to give hard news.", 12.4, 31, P.ACCENT).to_edge(DOWN, buff=0.7)
        tag = note(r"schematic").to_corner(DR, buff=0.2)
        with self.voiceover(
            "Where is this used? Start with the established part. <bookmark mark='a'/> Genetic counselling "
            "deals mostly with conditions that come from one gene, or one chromosome: Huntington's "
            "disease, cystic fibrosis, Down syndrome. There a test is close to a diagnosis, and the "
            "counsellor's work is to help a family understand a probability and decide what to do. "
            "<bookmark mark='b'/> The skills are psychological: how people understand risk, which is "
            "Part 26, and how to give hard news. <bookmark mark='c'/> The traits of this part aren't like "
            "that. They're influenced by thousands of positions, each one tiny. For those, the test is a "
            "polygenic score, and you now know what a score can say."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(left[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m, shift=RIGHT * 0.15) for m in left[1:]], lag_ratio=0.7), run_time=6.0)
            vo.wait_until("b")
            self.play(FadeIn(end))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(m, shift=RIGHT * 0.15) for m in right], lag_ratio=0.5), run_time=4.0)
        self.clear_scene()

    def consumer(self):
        d = load("embryo")
        m = archive.MARTIN_2019.data
        head = heading(r"A score for sale: \ do the arithmetic first")
        z = np.linspace(-3.2, 3.2, 200)
        base_y, s, cx = -1.6, 0.92, -3.75
        r = float(np.sqrt(d["r2"]))
        mu = r * 1.2816
        sd = float(np.sqrt(1 - d["r2"]))

        def bell(mean, width, col, opacity):
            pts = [np.array([cx + s * zi, base_y + 2.6 * np.exp(-0.5 * ((zi - mean) / width) ** 2) / width, 0]) for zi in z]
            return VMobject(color=col, stroke_width=4, stroke_opacity=opacity).set_points_as_corners(pts)

        everyone = bell(0.0, 1.0, OWN, 1.0)
        you = bell(mu, sd, THRESH, 1.0)
        ground = Line([cx - 3.3 * s, base_y, 0], [cx + 3.3 * s, base_y, 0], color=GREY_B, stroke_width=2)
        mid = DashedLine([cx, base_y, 0], [cx, base_y + 2.9, 0], color=WHITE, stroke_width=2)
        el = label(r"everyone", font_size=28, color=OWN).move_to([cx - 2.2, base_y + 1.75, 0])
        yl = wrapped_label(r"people told they are in the top tenth", 2.6, 28, THRESH).move_to([cx + 2.35, base_y + 2.6, 0])
        ml = label(r"average", font_size=26, color=WHITE).next_to(mid, UP, buff=0.08)
        rows = rows_of([
            (rf"a score that predicts {pct(d['r2'])} of the differences in test scores: \ about the best published", DATA),
            (rf"told you are in the top tenth: \ your chance of being above average is {pct(d['above_avg_top'])}", THRESH),
            (rf"your predicted score, on the IQ scale: \ $\pm {d['interval_iq']:.0f}$ points", WHITE),
            (rf"built on people of European ancestry: \ about {m['fold_lower_african']:.1f} times less accurate in people "
             r"of African ancestry", BAD),
        ], 5.6, 29, 0.28).move_to([4.0, -0.25, 0])
        keep_in_frame(rows)
        src = published_tag(archive.LEE_2018.cite + r"; \ " + archive.MARTIN_2019.cite)
        tag = psyche_tag(r"curves: computed")
        with self.voiceover(
            "Companies will sell you a score for a behavioural trait. Do the arithmetic before you buy. "
            f"<bookmark mark='a'/> Take a score that predicts {100 * d['r2']:.0f} percent of the "
            "differences in scores on reasoning tests, which is about as good as published scores get. "
            "<bookmark mark='b'/> You're told you're in the top tenth. Your chance of actually being "
            f"above average is {100 * d['above_avg_top']:.0f} percent. A coin gives fifty. "
            "<bookmark mark='c'/> Your predicted score, on the IQ scale, comes with a range of plus or "
            f"minus {d['interval_iq']:.0f} points. <bookmark mark='d'/> And three things the report may "
            "not say. The score was built on people of European ancestry, and it's several times less "
            "accurate in people of African ancestry. Part of what it measures is your parents' home. And "
            "nothing in it says what a different school, or a different year of your life, would do."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag), FadeIn(ground), Create(everyone), FadeIn(el), Create(mid),
                      FadeIn(ml), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(you), FadeIn(yl), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3], shift=UP * 0.1))
        self.clear_scene()

    def embryo(self):
        d = load("embryo")
        head = heading(r"Choosing among embryos: \ the expected gain")
        A = axes([0, 100], [0, 6.5], x_length=6.2, y_length=4.1, xticks=[1, 10, 50, 100], yticks=[0, 2, 4, 6],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", xlabel=r"embryos to choose from",
                 ylabel=r"expected gain (IQ points)", center=[-3.4, -0.5, 0])
        ax = A.ax
        cv = curve(ax, d["ks"], d["gain"], GENE, stroke_width=4)
        p10 = Dot(ax.c2p(10, d["gain_10"]), radius=0.1, color=WHITE)
        l10 = label(rf"10 embryos: \ ${d['gain_10']:.1f}$", font_size=28).next_to(ax.c2p(15, 3.0), RIGHT, buff=0)
        p100 = Dot(ax.c2p(100, d["gain_100"]), radius=0.1, color=WHITE)
        l100 = label(rf"100: \ ${d['gain_100']:.1f}$", font_size=28).next_to(p100, DL, buff=0.12)
        pub = Dot(ax.c2p(d["published_k"], d["published_gain"]), radius=0.11, color=DATA)
        publ = label(rf"published, with real genomes: \ ${d['published_gain']:.1f}$", font_size=27, color=DATA).next_to(
            ax.c2p(15, 2.0), RIGHT, buff=0)
        rows = rows_of([
            (r"embryos of one couple are siblings: \ half the spread in score", WHITE),
            (r"and between siblings the score's effect is about 40\% smaller", WHITE),
            (rf"ten embryos, \ pick the top one: \ ${d['gain_10']:.1f}$ points, on average", GENE),
            (rf"a hundred embryos: \ ${d['gain_100']:.1f}$. \ The curve flattens fast", GENE),
            (rf"and nothing removes the $\pm {d['interval_iq']:.0f}$ points around any one child", BAD),
        ], 5.3, 29, 0.26).move_to([4.15, -0.3, 0])
        keep_in_frame(rows)
        src = published_tag(archive.KARAVANI_2019.cite)
        tag = psyche_tag(r"curve: computed")
        with self.voiceover(
            "The strongest claim on sale is embryo selection. During IVF, score the embryos and implant "
            "the one with the highest score. Here's the arithmetic. <bookmark mark='a'/> The embryos of "
            "one couple are siblings. They differ in score less than strangers do: half the spread. And "
            "between siblings the score's effect is about forty percent smaller, as you saw. "
            "<bookmark mark='b'/> With ten embryos, choosing the top one instead of one at random gains, "
            f"on average, {d['gain_10']:.1f} IQ points. <bookmark mark='c'/> A simulation with real "
            f"genomes, published in 2019, got about {d['published_gain']:.1f}. <bookmark mark='d'/> More "
            f"embryos barely help. A hundred embryos: {d['gain_100']:.1f} points. The curve is the "
            "expected best of a sample, and it flattens fast. <bookmark mark='e'/> Against that small "
            "average gain, set the range from the last screen, plus or minus "
            f"{d['interval_iq']:.0f} points around any one child, which no selection removes."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(Create(cv), run_time=2.0)
            self.play(FadeIn(p10), FadeIn(l10), FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(pub, scale=2.0), FadeIn(publ))
            vo.wait_until("d")
            self.play(FadeIn(p100), FadeIn(l100), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4], shift=UP * 0.1))
        self.clear_scene()

    def questions(self):
        head = heading(r"Six questions for any claim about genes and behaviour")
        qs = [
            (r"One gene with a large effect, \ or a score of thousands?", GENE),
            (r"How much of the differences does it predict, \ in people it was not built on?", THRESH),
            (r"In whom was it built, \ and does it work in people like these?", DATA),
            (r"Does the effect hold between brothers and sisters, \ or only between families?", HOME),
            (r"Was the threshold set for the number of tests, \ and was it found twice?", MODEL),
            (r"Does it say anything about what a change in circumstances would do?", P.ACCENT),
        ]
        rows = VGroup(*[label(rf"{i + 1}. \ {q}", font_size=33, color=c) for i, (q, c) in enumerate(qs)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([0, -0.35, 0])
        if rows.width > 13.0:
            rows.width = 13.0
        with self.voiceover(
            "So here's what to carry out of this part: six questions for any claim about genes and "
            "behaviour. <bookmark mark='a'/> Is it one gene with a large effect, or a score built from "
            "thousands? <bookmark mark='b'/> How much of the differences does it predict, in people it "
            "wasn't built on? <bookmark mark='c'/> In whom was it built, and does it work in people like "
            "the ones it's being used on? <bookmark mark='d'/> Does the effect hold between brothers and "
            "sisters, or only between families? <bookmark mark='e'/> Was the threshold set for the number "
            "of tests, and was the result found twice? <bookmark mark='f'/> And the one that matters most "
            "to a person: does it say anything about what a change in circumstances would do? "
            "Heritability, remember, never does."
        ) as vo:
            self.play(FadeIn(head))
            for mark_, r in zip("abcdef", rows):
                vo.wait_until(mark_)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
