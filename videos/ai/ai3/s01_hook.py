from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai3.common import CAT_COLORS, HIST, MONO, PART, barcode, era_strip, load


class Hook(VoiceoverScene):
    def construct(self):
        self.islands()
        self.cloud()
        self.barcodes()
        self.era()
        self.plan()

    # ------------------------------------------------------------------
    def islands(self):
        def island(text, x):
            t = Text(text, font=MONO, font_size=34, color=WHITE)
            box = RoundedRectangle(width=t.width + 0.8, height=1.3, corner_radius=0.3, stroke_color=C.COUNTING,
                                   stroke_width=2.5, fill_color="#14201A", fill_opacity=1)
            return VGroup(box, t).move_to([x, 0.3, 0])

        a, b = island("the dog barked", -3.4), island("the hound barked", 3.4)
        gap = DashedLine(a.get_right(), b.get_left(), color=GREY_C, stroke_width=3, dash_length=0.12)
        q = MathTex(r"?", font_size=60, color=C.SURPRISE).next_to(gap, UP, buff=0.15)
        cap = label(r"Part 1's counting model: \\ every context is its own island", font_size=30, color=GREY_A)
        cap.to_edge(DOWN, buff=1.0)
        with self.voiceover(
            "In part one, a model learned to guess the next letter by counting, and it hit a wall. Every context was "
            "its own island. <bookmark mark='a'/> Reading the dog barked a hundred times taught it nothing about "
            "the hound barked."
        ) as vo:
            self.play(FadeIn(a, shift=RIGHT * 0.3), FadeIn(cap))
            vo.wait_until("a")
            self.play(FadeIn(b, shift=LEFT * 0.3))
            self.play(Create(gap), FadeIn(q, scale=0.5))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cloud(self):
        g = load("gpt2")
        words, cats, xyz = list(g["map_words"]), list(g["map_cats"]), np.asarray(g["map_xyz"])
        show = {"dog", "lion", "red", "blue", "three", "hundred", "London", "Tokyo", "mother", "brother", "hand",
                "heart", "run", "sing"}
        labels = {k: Text(w, font=MONO, font_size=22, color=CAT_COLORS[c]) for k, (w, c) in enumerate(zip(words, cats))
                  if w in show or c == "animals"}
        cl = Cloud3D(xyz, [CAT_COLORS[c] for c in cats], scale=3.5, radius=0.085, tilt=0.3, center=DOWN * 0.2,
                     labels=labels)
        overview = VGroup(*[m for k, m in cl.label_of.items() if words[k] in show])
        animals = VGroup(*[m for k, m in cl.label_of.items() if cats[k] == "animals" and words[k] not in show])
        animals.set_opacity(0)
        centre = xyz[[k for k, c in enumerate(cats) if c == "animals"]].mean(0)
        legend = VGroup(*[VGroup(Dot(radius=0.07, color=col), label(name, font_size=24, color=col)).arrange(RIGHT, buff=0.1)
                          for name, col in CAT_COLORS.items()]).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        legend.to_corner(UL, buff=0.5)
        src = note(r"GPT-2 (2019): \\ each word's vector, on the three directions these words vary most").to_edge(DOWN, buff=0.3)
        dog = words.index("dog")
        # the words themselves first, in a shuffled list: then each one flies to its place
        order = np.random.default_rng(2019).permutation(len(words))
        lines_, cur = [], []
        for k in order:  # lines of about 60 characters, so the words share one baseline
            if cur and len("  ".join(words[i] for i in cur + [k])) > 60:
                lines_.append(cur)
                cur = []
            cur.append(k)
        lines_.append(cur)
        vocab, word_of = VGroup(), {}
        for ks in lines_:
            t_ = data_text("  ".join(words[i] for i in ks), font=MONO, font_size=22, color=GREY_A)
            j = 0
            for i in ks:
                n_ = len(words[i])
                word_of[i] = VGroup(*t_.submobjects[j:j + n_])
                j += n_
            assert j == len(t_.submobjects)
            vocab.add(t_)
        vocab.arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to(DOWN * 0.1)
        if vocab.width > 13.0:
            vocab.scale_to_fit_width(13.0)
        with self.voiceover(
            "Every modern model fixes this the same way. It gives each word a place, <bookmark mark='a'/> a point in "
            f"a space, chosen so that words used alike end up close together. <bookmark mark='b'/> Here are "
            f"{len(words)} words, where GPT-2 puts them: animals in one region, colors in another, then numbers, "
            "places, family, the body, and verbs."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(m, shift=DOWN * 0.1) for m in vocab], lag_ratio=0.1), run_time=1.6)
            vo.wait_until("a")
            targets = [cl.dots[k].copy().clear_updaters() for k in range(len(words))]
            self.play(LaggedStart(*[Transform(word_of[k], targets[k]) for k in range(len(words))], lag_ratio=0.01),
                      run_time=2.0)
            self.remove(vocab)
            self.add(cl)
            vo.wait_until("b")
            self.play(FadeIn(overview), FadeIn(legend), FadeIn(src))
            self.play(cl.angle.animate.set_value(2 * PI), run_time=max(4.0, vo.remaining() - 0.5), rate_func=linear)
        with self.voiceover(
            "The picture is a shadow. <bookmark mark='a'/> GPT-2 really gives each of its 50,257 tokens a list of "
            "768 numbers, and we've flattened them down to three, keeping the three directions along which these "
            "words spread out the most. <bookmark mark='b'/> Up close, dog sits with the other animals."
        ) as vo:
            self.play(cl.angle.animate.set_value(2 * PI + 0.6), run_time=2.0)
            vo.wait_until("b")
            others = VGroup(*[m for m in overview if m is not cl.label_of[dog]])
            self.play(*cl.look_at(centre, 2.6), others.animate.set_opacity(0), animals.animate.set_opacity(1),
                      run_time=2.5)
            self.play(cl.angle.animate.set_value(2 * PI + 1.1), run_time=2.0)
        cl.dots.clear_updaters()
        cl.labels.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def barcodes(self):
        g = load("gpt2")
        V = np.asarray(g["barcodes"])
        names = list(g["barcode_words"])
        cos = np.asarray(g["barcode_cos"])
        assert names[:3] == ["dog", "puppy", "tobacco"] and V.shape[1] == 768
        vmax = float(np.abs(V[:3]).max())
        rows = VGroup()
        for k in range(3):
            bc = barcode(V[k], width=11.0, height=1.2, vmax=vmax)
            name = Text(names[k], font=MONO, font_size=30, color=WHITE)
            rows.add(VGroup(name, bc).arrange(RIGHT, buff=0.35))
        rows.arrange(DOWN, buff=0.55, aligned_edge=RIGHT).move_to(DOWN * 0.1)
        head = label(r"$768$ numbers per word", font_size=36).to_edge(UP, buff=0.4)
        cosl = VGroup(
            label(rf"dog and puppy: \\ cosine ${cos[0, 1]:.2f}$", font_size=28, color=C.TRUE_P),
            label(rf"dog and tobacco: \\ cosine ${cos[0, 2]:.2f}$", font_size=28, color=GREY_A),
        ).arrange(RIGHT, buff=1.0).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Here is dog, all 768 numbers. <bookmark mark='a'/> Here is puppy. <bookmark mark='b'/> And here is "
            "tobacco. <bookmark mark='c'/> Two of these belong together, and in chapter one we'll learn to measure "
            "how much."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0][0]), LaggedStart(*[GrowFromEdge(b, DOWN) for b in rows[0][1]],
                                                                     lag_ratio=0.002), run_time=1.6)
            vo.wait_until("a")
            self.play(FadeIn(rows[1][0]), LaggedStart(*[GrowFromEdge(b, DOWN) for b in rows[1][1]], lag_ratio=0.002),
                      run_time=1.4)
            vo.wait_until("b")
            self.play(FadeIn(rows[2][0]), LaggedStart(*[GrowFromEdge(b, DOWN) for b in rows[2][1]], lag_ratio=0.002),
                      run_time=1.4)
            vo.wait_until("c")
            self.play(FadeIn(cosl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def era(self):
        """How we got here: from Grassmann's vectors to the low-rank training of 2024, evenly spaced (not to scale)."""
        events = [
            (1844, r"Grassmann: \\ vectors"),
            (1858, r"Cayley: \\ matrix algebra"),
            (1873, r"Beltrami, Jordan: \\ the SVD"),
            (1904, r"Hilbert: \\ eigenvalues"),
            (1936, r"Eckart, Young: \\ best low rank"),
            (1957, r"Firth: \\ the company it keeps"),
            (1984, r"Johnson, Lindenstrauss: \\ random projection"),
            (1990, r"latent semantic \\ analysis"),
            (2006, r"the Netflix Prize"),
            (2013, r"word2vec"),
            (2021, r"LoRA"),
            (2024, r"GaLore; \\ Muon"),
        ]
        axis, skel, marks = era_strip(events, font_size=19)
        head = label(r"How we got here", font_size=42).to_edge(UP, buff=0.3)
        tag = note(r"milestones evenly spaced, \ not to scale").to_corner(DR, buff=0.2)
        with self.voiceover(
            "The mathematics is older than the machines. In 1844 Hermann Grassmann described quantities that add "
            "and stretch, in any number of dimensions. <bookmark mark='a'/> In 1858 Arthur Cayley wrote down the "
            "algebra of matrices. <bookmark mark='b'/> Beltrami and Jordan found the singular value decomposition, "
            "<bookmark mark='c'/> and Hilbert named eigenvalues. <bookmark mark='d'/> Eckart and Young proved how to "
            "keep only what matters. <bookmark mark='e'/> Then meaning: John Firth's 'you shall know a word by the "
            "company it keeps'. <bookmark mark='f'/> Johnson and Lindenstrauss squeezed dimensions. "
            "<bookmark mark='g'/> Latent semantic analysis put words in a space, <bookmark mark='h'/> and Netflix "
            "offered a million dollars for filling in a mostly empty matrix. <bookmark mark='i'/> Then word2vec, "
            "<bookmark mark='j'/> and LoRA, GaLore and Muon, the same linear algebra inside today's training."
        ) as vo:
            self.play(FadeIn(head), Create(axis), FadeIn(tag), FadeIn(skel))
            self.play(FadeIn(marks[0], shift=UP * 0.2))
            for k, mk in enumerate("abcdefghij"):
                vo.wait_until(mk)
                self.play(FadeIn(marks[k + 1], shift=(UP if (k + 1) % 2 == 0 else DOWN) * 0.2))
            self.play(FadeIn(marks[11], shift=DOWN * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        title = label(rf"Part {PART}: \ Vectors That Mean Things", font_size=48).to_edge(UP, buff=0.45)
        smap = series_map(current=PART, done=PART - 1).scale(0.8).move_to(DOWN * 0.5)
        obj = objectives_card([
            r"vectors, \ the dot product and Cauchy--Schwarz; \ einsum, the notation of attention",
            r"matrices as maps: \ projection, \ eigenvectors, \ the SVD, \ each derived",
            r"low rank: \ Eckart--Young, \ norms and conditioning, \ random matrices against trained weights, \ "
            r"low-rank gradients",
            r"word vectors from counting, \ and why word2vec is counting in disguise",
            r"high dimensions: \ concentration, \ Johnson--Lindenstrauss proved, \ GPT-2's lopsided space",
            r"low rank in the wild: \ the Netflix Prize, \ two-tower retrieval",
        ], font_size=24).move_to(DOWN * 0.35)
        with self.voiceover(
            "This is Part 3 of AI, Built. <bookmark mark='a'/> In it: vectors, the dot product and einsum; "
            "projections, eigenvectors and the singular value decomposition, each derived; norms, random matrices "
            "and what training writes into weights; word vectors; the geometry of high dimensions; and low rank at "
            "work. Every number computed, small enough for a laptop."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.5)
        self.clear_scene()
