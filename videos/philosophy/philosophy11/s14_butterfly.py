from __future__ import annotations

from videos.philosophy.philosophy11.common import *  # noqa: F403


def butterfly(color=LUCK, s=1.0) -> VGroup:
    wing = lambda sx, sy, w, h: Ellipse(width=w * s, height=h * s, stroke_color=color, stroke_width=2.5,
                                        fill_color=color, fill_opacity=0.35).move_to([sx * s, sy * s, 0])
    body = Ellipse(width=0.12 * s, height=0.9 * s, color=GREY_A, fill_opacity=0.8)
    g = VGroup(wing(-0.42, 0.18, 0.8, 0.62).rotate(0.5), wing(0.42, 0.18, 0.8, 0.62).rotate(-0.5),
               wing(-0.32, -0.28, 0.5, 0.42).rotate(-0.4), wing(0.32, -0.28, 0.5, 0.42).rotate(0.4), body)
    return g


class Butterfly(VoiceoverScene):
    def construct(self):
        card = chapter_card(13, r"The butterfly and the sponge", r"Can one live with doubt?", lit=(-300,), part=PART)
        with self.voiceover("Chapter thirteen. The butterfly and the sponge."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.dream()
        self.pyrrho()

    def dream(self):
        hc = history_card(r"c.\ 300\ BCE", r"Zhuangzi", r"\textit{Zhuangzi}, \ ch.\ 2, \ `On the equality of "
                          r"things'", width=5.8, color=HIST).to_corner(UL, buff=0.35)
        b = butterfly().move_to([5.3, 0.6, 0])
        q = quote_card(r"He did not know whether he was Zhou who had dreamt he was a butterfly, or a butterfly "
                       r"dreaming that he was Zhou.", r"Zhuangzi", r"trans.\ after Watson", width=7.6,
                       font_size=25).move_to([-1.2, 0.6, 0])
        rows = VGroup(label(r"`Between Zhou and a butterfly there must be some distinction: \ this is called the "
                            r"transformation of things'", font_size=22, color=KNOW),
                      label(r"not an argument that we know nothing, \ but a release from needing to know which",
                            font_size=23, color=GOAL),
                      label(r"Descartes's dream (1641) seeks certainty; \ Zhuangzi's dream lets it go", font_size=23,
                            color=GREY_A)).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "There is another way to respond to doubt: not to refute it, but to live with it. "
            "<bookmark mark='a'/>Around 300 BCE, the Chinese philosopher Zhuang Zhou wrote of a dream. Once he "
            "dreamt he was a butterfly, flitting about, happy, not knowing he was Zhou. Suddenly he woke, and there "
            "he was, solidly Zhou. <bookmark mark='b'/>But he did not know whether he was Zhou who had dreamt he was "
            "a butterfly, or a butterfly dreaming that he was Zhou. <bookmark mark='c'/>Between Zhou and a butterfly "
            "there must be some distinction, he adds. This is called the transformation of things. "
            "<bookmark mark='d'/>Zhuangzi does not argue that we know nothing. He loosens our need to settle which "
            "perspective is the real one. <bookmark mark='e'/>Descartes used the dream to seek a certainty that no "
            "dream could shake. Zhuangzi uses it to let that search go."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(b, scale=0.5))
            self.play(b.animate.shift(LEFT * 0.5 + UP * 0.5).rotate(0.2), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(q))
            for mk, r in zip("cde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def pyrrho(self):
        hc = history_card(r"c.\ 200", r"Sextus Empiricus", r"\textit{Outlines of Pyrrhonism} I", width=5.0,
                          color=HIST).to_corner(UL, buff=0.35)
        beam = Line([-2.0, 0.9, 0], [2.0, 0.9, 0], color=GREY_B, stroke_width=4)
        post = Line([0, 0.9, 0], [0, -0.3, 0], color=GREY_B, stroke_width=4)
        pans = VGroup(*[VGroup(Line([x, 0.9, 0], [x, 0.4, 0], color=GREY_C), Arc(radius=0.45, start_angle=PI,
                                                                                angle=PI, color=GREY_B).move_to(
            [x, 0.25, 0])) for x in (-1.8, 1.8)])
        la = label(r"for", font_size=22, color=BEL).move_to([-1.8, -0.45, 0])
        ra = label(r"against", font_size=22, color=LUCK).move_to([1.8, -0.45, 0])
        scale_ = VGroup(beam, post, pans, la, ra).move_to([-3.4, 0.4, 0])
        chain = VGroup(label(r"equipollence: \ every argument meets an equal argument", font_size=23, color=GOAL),
                       label(r"$\Downarrow$", font_size=26, color=GREY_B),
                       label(r"\textit{epochē}: \ suspension of judgment", font_size=23, color=SKEP),
                       label(r"$\Downarrow$", font_size=26, color=GREY_B),
                       label(r"\textit{ataraxia}: \ tranquillity, \ `as a shadow follows a body'", font_size=23,
                             color=KNOW)).arrange(DOWN, buff=0.15).move_to([2.6, 0.6, 0])
        apelles = VGroup(label(r"Apelles the painter could not paint a horse's foam;", font_size=22),
                         label(r"in despair he threw his sponge at the picture, \ and it made the foam (PH I.28)",
                               font_size=22, color=GREY_A),
                         label(r"the skeptic stopped trying to reach tranquillity, \ and it came", font_size=23,
                               color=KNOW)).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "In the West, the ancient skeptics made the same turn. <bookmark mark='a'/>Sextus Empiricus, writing "
            "around the year 200, describes the Pyrrhonist's practice. For every argument he finds an equal argument "
            "against: equipollence. <bookmark mark='b'/>With the scales level, he suspends judgment: epochē. "
            "<bookmark mark='c'/>And then tranquillity follows, Sextus says, as a shadow follows a body. "
            "<bookmark mark='d'/>He tells a story about it. The painter Apelles was painting a horse and could not "
            "get the foam at its mouth right. In despair he threw his sponge at the picture, and the mark it left "
            "was the foam. <bookmark mark='e'/>The skeptics had hoped to find tranquillity by deciding what is true. "
            "When they gave up deciding, tranquillity came by itself. For the ancient skeptic, doubt was a way of "
            "life, not a problem to be solved."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(scale_), FadeIn(chain[0]))
            vo.wait_until("b")
            self.play(FadeIn(chain[1]), FadeIn(chain[2]))
            vo.wait_until("c")
            self.play(FadeIn(chain[3]), FadeIn(chain[4]))
            vo.wait_until("d")
            self.play(FadeIn(apelles[0]), FadeIn(apelles[1]))
            vo.wait_until("e")
            self.play(FadeIn(apelles[2]))
        self.clear_scene()
