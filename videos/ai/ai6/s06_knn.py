from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai6.common import AUSTEN, DICKENS, crop_to_axes, load, page_dots, page_plane, region_image


class KNN(VoiceoverScene):
    def construct(self):
        self.card()
        self.vote()
        self.regions()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(5, r"Ask the neighbours", r"What if there is no line at all?", part=6)
        with self.voiceover("Chapter five. Nearest neighbours."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def setup_data(self):
        p = load("pages")
        X2, y, test = np.asarray(p["X2"]), np.asarray(p["y"]), np.asarray(p["test"], bool)
        mu, sd = X2[~test].mean(0), X2[~test].std(0)
        return X2, y, test, mu, sd

    # ------------------------------------------------------------------
    def vote(self):
        X2, y, test, mu, sd = self.setup_data()
        plane = page_plane(x_length=7.6, y_length=5.0, center=[-2.2, -0.3, 0])
        ax = plane[0]
        tr = np.nonzero(~test)[0]
        dots = page_dots(ax, X2, y, idx=tr, jitter=0.35, radius=0.045, opacity=0.7)
        # a test page in the middle of the overlap
        te = np.nonzero(test)[0]
        Ztr = (X2[tr] - mu) / sd
        cand = [i for i in te if 40 <= X2[i, 0] <= 50 and 7 <= X2[i, 1] <= 10]
        q = cand[0]
        zq = (X2[q] - mu) / sd
        d = np.sqrt(((Ztr - zq) ** 2).sum(1))
        nn = np.argsort(d)[:15]
        nd = int(y[tr][nn].sum())
        qd = glow_dot(ax.c2p(*X2[q]), color=WHITE, radius=0.1)
        links = VGroup(*[Line(ax.c2p(*X2[q]), ax.c2p(*X2[tr[j]]), color=AUSTEN if y[tr[j]] == 0 else DICKENS,
                              stroke_width=2, stroke_opacity=0.8) for j in nn])
        r_scr = max(np.linalg.norm(ax.c2p(*X2[tr[j]]) - ax.c2p(*X2[q])) for j in nn)
        ring = Circle(radius=r_scr + 0.05, color=WHITE, stroke_width=2).move_to(ax.c2p(*X2[q])).set_stroke(opacity=0.6)
        tally = VGroup(label(rf"Austen: \ ${15 - nd}$", font_size=32, color=AUSTEN),
                       label(rf"Dickens: \ ${nd}$", font_size=32, color=DICKENS)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        tally.move_to([4.4, 1.0, 0])
        verdict = label(r"the vote: \ " + ("Dickens" if nd > 7 else "Austen"), font_size=32,
                        color=DICKENS if nd > 7 else AUSTEN).next_to(tally, DOWN, buff=0.4).align_to(tally, LEFT)
        truth = label(r"(it's " + ("Dickens" if y[q] == 1 else "Austen") + ")", font_size=26, color=GREY_A)
        truth.next_to(verdict, DOWN, buff=0.15).align_to(tally, LEFT)
        note_ = label(r"distances measured in standard deviations of each rate", font_size=22, color=GREY_B)
        note_.to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Here's a method with no line at all. To classify a page, find the training pages most like it, its "
            "nearest neighbours, and let them vote. <bookmark mark='a'/> Take this page from the test set. "
            f"<bookmark mark='b'/> Its fifteen nearest neighbours: {15 - nd} by Austen, {nd} by Dickens. "
            "<bookmark mark='c'/> The majority wins."
        ) as vo:
            self.play(Create(ax), FadeIn(plane[1:]), LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.003),
                      run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(qd, scale=0.5))
            vo.wait_until("b")
            self.play(Create(ring), LaggedStart(*[Create(l_) for l_ in links], lag_ratio=0.08), FadeIn(tally), FadeIn(note_),
                      run_time=2.0)
            # zoom in on the vote (the picture scales; the frame stays)
            world = VGroup(ax, plane[1:], dots, qd, links, ring)
            here = ax.c2p(*X2[q])
            self.play(world.animate.scale(3.2, about_point=here).shift(np.array([-2.2, -0.3, 0]) - here), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(verdict), FadeIn(truth))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def regions(self):
        X2, y, test, mu, sd = self.setup_data()
        k_ = load("knn")
        plane = page_plane(x_length=7.6, y_length=5.0, center=[-2.2, -0.3, 0])
        ax = plane[0]
        tr = np.nonzero(~test)[0]
        dots = page_dots(ax, X2, y, idx=tr, jitter=0.35, radius=0.04, opacity=0.9)
        imgs = {}
        for k in (1, 15, 75):
            v, xs, ys = crop_to_axes(k_[f"region{k}"], k_["xs"], k_["ys"])
            imgs[k] = region_image(v, xs, ys, ax, opacity=0.45)
        rows = VGroup()
        for k in (1, 15, 75):
            rows.add(VGroup(MathTex(rf"k = {k}", font_size=34, color=C.BITS),
                            label(rf"training pages: \ ${100 * k_[f'train{k}']:.0f}\%$", font_size=26, color=GREY_A),
                            label(rf"new pages: \ ${100 * k_[f'acc{k}']:.0f}\%$", font_size=28, color=WHITE))
                     .arrange(DOWN, aligned_edge=LEFT, buff=0.08))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([4.6, 0.0, 0])
        lesson = label(r"too few neighbours memorize; \ too many blur \ (Part 8)", font_size=26, color=C.BITS)
        lesson.to_edge(DOWN, buff=0.3)
        a1, a15, a75 = (round(100 * k_[f"acc{k}"]) for k in (1, 15, 75))
        t1 = round(100 * k_["train1"])
        with self.voiceover(
            "Colour every point of the plane by how its neighbours would vote, and you see the method's whole "
            "answer. <bookmark mark='a'/> With one neighbour, the regions are a ragged patchwork that copies the "
            f"training pages: it gets {t1} percent of them right, but only {a1} percent of new ones. "
            f"<bookmark mark='b'/> Fifteen neighbours smooth it out: {a15} percent. <bookmark mark='c'/> Seventy-five, "
            f"smoother still: {a75}. Too few neighbours memorize, too many blur, and that trade-off is the subject of "
            "part eight."
        ) as vo:
            self.play(Create(ax), FadeIn(plane[1:]), FadeIn(dots))
            vo.wait_until("a")
            self.play(FadeIn(imgs[1]), FadeIn(rows[0]))
            self.bring_to_front(dots)
            vo.wait_until("b")
            self.play(FadeOut(imgs[1]), FadeIn(imgs[15]), FadeIn(rows[1]))
            self.bring_to_front(dots)
            vo.wait_until("c")
            self.play(FadeOut(imgs[15]), FadeIn(imgs[75]), FadeIn(rows[2]))
            self.bring_to_front(dots)
            self.play(FadeIn(lesson))
        self.wait(0.3)
        self.clear_scene()
