from __future__ import annotations

from videos.psychology.psych32.common import *  # noqa: F403

LETTERS = "ABCD"


class Predict(VoiceoverScene):
    def construct(self):
        self.card()
        self.items()
        self.answers()

    def card(self):
        card = chapter_card(4, r"On you: \ three matrices", r"What completes the pattern?", lit=(), part=PART,
                            scale=("person",), marr=("what", "how"))
        with self.voiceover("Chapter four. On you: three matrices."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def _item(self, k, d, center):
        panel = matrix_panel(d[f"grid{k}"], cell=0.62).move_to(center + np.array([0, 0.7, 0]))
        opts = VGroup()
        for i, o in enumerate(d[f"options{k}"]):
            box = Square(side_length=0.62, stroke_color=GREY_B, stroke_width=2)
            g_ = glyph(o, scale=0.62 / 0.95).move_to(box)
            opts.add(VGroup(box, g_, label(LETTERS[i], font_size=18, color=YOU).next_to(box, DOWN, buff=0.08)))
        opts.arrange(RIGHT, buff=0.18).next_to(panel, DOWN, buff=0.35)
        name = label(rf"Matrix {k}", font_size=24).next_to(panel, UP, buff=0.18)
        return VGroup(name, panel, opts)

    def items(self):
        d = load("matrices")
        stage = demo_stage(13.4, 6.2, center=[0, -0.35, 0])
        its = VGroup(*[self._item(k, d, np.array([-4.3 + 4.3 * (k - 1), -0.6, 0])) for k in (1, 2, 3)])
        with self.voiceover(
            "Your turn. These are matrix items, the kind of puzzle Raven's Progressive Matrices made famous. Each "
            "row of three follows rules: a shape, a number, a shade or a size stays the same, steps up, or cycles "
            "through three values. The bottom-right cell is missing. <bookmark mark='a'/> Matrix one has one rule "
            "to find. <bookmark mark='b'/> Matrix two has two. <bookmark mark='c'/> Matrix three has three. "
            "<bookmark mark='d'/> Pick the option, A to D, that completes each one. This part's interactive gives "
            "you more, generated fresh, and keeps no score. Pause here and solve them."
        ) as vo:
            self.play(FadeIn(stage))
            self.play(LaggedStart(*[FadeIn(it, shift=UP * 0.1) for it in its], lag_ratio=0.4), run_time=2.5)
            frame = SurroundingRectangle(its[0], color=YOU, buff=0.15, stroke_width=3)
            vo.wait_until("a")
            self.play(Create(frame))
            for m, it in zip("bc", its[1:]):
                vo.wait_until(m)
                self.play(frame.animate.move_to(it))
            vo.wait_until("d")
            self.play(FadeOut(frame))
            self.play(Indicate(stage, color=YOU))
        self.wait(4.0)
        self.clear_scene()

    def answers(self):
        d = load("matrices")
        head = heading(r"The answers, \ and the rules")
        its = VGroup(*[self._item(k, d, np.array([-4.3 + 4.3 * (k - 1), -0.2, 0])) for k in (1, 2, 3)])
        marks = VGroup()
        texts = VGroup()
        for k, it in zip((1, 2, 3), its):
            c = int(d[f"correct{k}"])
            marks.add(SurroundingRectangle(it[2][c][0], color=GOOD, buff=0.05, stroke_width=4))
            rules = [f"{a}: {r}" for a, r in zip(("shape", "number", "shade", "size"), d[f"rules{k}"])
                     if r != "constant"]
            texts.add(wrapped_label(rf"{LETTERS[c]}: \ " + r", \ ".join(rules), 3.8, 18, GOOD)
                      .next_to(it, DOWN, buff=0.25))
        foot = wrapped_label(r"each rule must be found and held while the others are checked: \ the more rules, "
                             r"\ the harder the item, \ as chapter eight will show", 12.4, 22, YOU).to_edge(DOWN,
                                                                                                         buff=0.35)
        with self.voiceover(
            "Here are the answers. <bookmark mark='a'/> In matrix one, a single attribute changes along each row. "
            "In matrix two, two do, by different rules. In matrix three, three do. <bookmark mark='b'/> Each rule "
            "has to be found, and then held in mind while the others are checked. The more rules, the harder the "
            "item, and chapter eight will show how much harder."
        ) as vo:
            self.play(FadeIn(head), FadeIn(its))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(m_) for m_ in marks], lag_ratio=0.5), LaggedStart(*[FadeIn(t) for t in texts],
                                                                                           lag_ratio=0.5))
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.clear_scene()
