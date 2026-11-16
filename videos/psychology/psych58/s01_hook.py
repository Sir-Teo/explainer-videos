from __future__ import annotations

from videos.psychology.psych58.common import *  # noqa: F403


def tiles(D, cols: int = 8, size: int = 8, height: float = 4.0, center=ORIGIN) -> Group:
    """A dictionary's columns as a grid of small grey images, each scaled to its own range."""
    n = D.shape[1]
    rows = int(np.ceil(n / cols))
    pad = 1
    out = np.full((rows * (size + pad) + pad, cols * (size + pad) + pad), 0.5)
    for k in range(n):
        f = D[:, k].reshape(size, size)
        f = 0.5 + 0.5 * f / max(np.abs(f).max(), 1e-9)
        r, c = divmod(k, cols)
        out[pad + r * (size + pad):pad + r * (size + pad) + size, pad + c * (size + pad):pad + c * (size + pad) + size] = f
    return heat(out[::-1], height=height, grey=True, center=center)


class Hook(VoiceoverScene):
    def construct(self):
        self.grow()
        self.question()
        self.objectives()

    def grow(self):
        d = load("sparse")
        im = load("images")
        head = heading(r"An optimization that grew receptive fields")
        pic = heat(im["image"][::-1], height=3.6, grey=True, center=[-4.2, 0.2, 0], smooth=True)
        cap = label(r"Psyche's world: \ a dead-leaves image", font_size=14, color=GREY_A).next_to(pic, DOWN, buff=0.12)
        snaps = [tiles(d[f"snap{k}"], height=3.6, center=[1.0, 0.2, 0]) for k in (0, 10, 50, 400)]
        caps = [label(t, font_size=14, color=GREY_A) for t in (r"start: \ random patches", r"after 10 steps",
                                                             r"after 50", r"after 400")]
        for c_ in caps:
            c_.next_to(snaps[0], DOWN, buff=0.12)
        rows = rows_of([
            (r"64 units must describe 8 by 8 patches with as few active as possible", WHITE),
            (r"nobody tells them what to become", MODEL),
            (r"they become small, \ oriented edge detectors: \ Part 13's simple cells", GOOD),
        ], 3.4, 18, 0.34).move_to([5.3, 0.0, 0])
        tag = psyche_tag(r"\texttt{efficient.learn\_dictionary}")
        with self.voiceover(
            "In 1959 Hubel and Wiesel found cells in the cat's visual cortex that respond to edges at one orientation, "
            "in one place. Part 13 told that story. <bookmark mark='a'/> Here's another way to arrive at the same "
            "cells. Psyche's world is a dead-leaves image: discs of random size and shade, piled on top of each "
            "other, a standard stand-in for the statistics of natural scenes. <bookmark mark='b'/> Sixty-four units "
            "must describe small patches of it, with as few units active as possible. <bookmark mark='c'/> Nobody "
            "tells them what to become. They start as random patches. <bookmark mark='d'/> After ten steps, nothing "
            "much. After fifty, structure. <bookmark mark='e'/> After four hundred, they've become small, oriented "
            "edge detectors: Part 13's simple cells, grown from a principle."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(pic), FadeIn(cap))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]), FadeIn(tag))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]), FadeIn(snaps[0]), FadeIn(caps[0]))
            vo.wait_until("d")
            self.play(FadeOut(snaps[0]), FadeIn(snaps[1]), ReplacementTransform(caps[0], caps[1]))
            self.wait(1.5)
            self.play(FadeOut(snaps[1]), FadeIn(snaps[2]), ReplacementTransform(caps[1], caps[2]))
            vo.wait_until("e")
            self.play(FadeOut(snaps[2]), FadeIn(snaps[3]), ReplacementTransform(caps[2], caps[3]), FadeIn(rows[2]))
        self.wait(1.0)
        self.clear_scene()

    def question(self):
        rows_section(self, r"Today: \ is there one principle from which the mind's mechanisms follow?", [
            (r"Barlow, \ 1961: \ sensory neurons exist to remove redundancy", SYMP),
            (r"Olshausen and Field, \ 1996: \ the optimization you just watched, \ on photographs", MODEL),
            (r"its descendants: \ efficient coding, \ predictive coding, \ the free-energy principle", PERSON),
            (r"and the question every grand theory must answer: \ what would it have to risk?", GOOD),
        ], "So this part asks: is there one principle from which the mind's mechanisms follow? "
           "<bookmark mark='a'/> In 1961 Horace Barlow proposed that sensory neurons exist to remove redundancy from "
           "their input. <bookmark mark='b'/> In 1996 Bruno Olshausen and David Field ran the optimization you just "
           "watched, on photographs of nature, and got the same result. An optimization principle produced biology. "
           "<bookmark mark='c'/> We'll follow its descendants: efficient coding, predictive coding, and the "
           "free-energy principle, a theory that claims to explain everything a brain does. <bookmark mark='d'/> And "
           "we'll ask the question every grand theory must answer: what would it have to risk?", font_size=26,
           buff=0.48)

    def objectives(self):
        head = VGroup(label(r"Part 58", font_size=34, color=GREY_B),
                      label(r"The Efficient, \ Predictive Brain", font_size=56))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"derive centre-surround and edge detectors from efficiency",
            r"predict after-effects and biases from an efficient code",
            r"derive generalization from rate-distortion, \ and normalization's one equation",
            r"build predictive coding, \ and the free energy, \ step by step",
            r"weigh the Bayesian brain, \ resource rationality and learning rules",
            r"ask what a unified theory would have to risk",
        ], color=P.ACCENT, font_size=31, width=13.2)
        with self.voiceover(
            "This is Part 58 of Psychology, Built: the efficient, predictive brain. <bookmark mark='a'/> We'll derive "
            "centre-surround cells and edge detectors from efficiency. We'll predict after-effects and biases from an "
            "efficient code. We'll derive generalization from rate-distortion theory, and meet normalization's one "
            "equation. We'll build predictive coding and the free energy, step by step. We'll weigh the Bayesian "
            "brain, resource rationality and learning rules. And we'll ask what a unified theory would have to risk."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(head.animate.scale(0.6).to_edge(UP, buff=0.3))
            obj.next_to(head, DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in obj], lag_ratio=0.9), run_time=20.0)
        self.clear_scene()
