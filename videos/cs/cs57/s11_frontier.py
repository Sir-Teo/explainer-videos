from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs57.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load


def tile(title, body, col, w=4.2, h=3.0):
    frame = RoundedRectangle(width=w, height=h, corner_radius=0.15, stroke_color=col, stroke_width=2, fill_color=BG,
                             fill_opacity=1)
    t = label(title, font_size=22, color=col)
    b = wrapped_label(body, w - 0.4, font_size=18, color=GREY_A)
    VGroup(t, b).arrange(DOWN, buff=0.3).move_to(frame)
    return VGroup(frame, t, b)


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.compression()
        self.incontext()
        self.open()

    def card(self):
        card = chapter_card(10, r"Frontier: \ compression schemes and in-context learning",
                            r"Is learning exactly compression?", lit=(1986, 2016),
                            extra=((1986, r"Littlestone and Warmuth: \ sample compression"),
                                   (2016, r"Moran and Yehudayoff: \ every VC class compresses")), part=PART)
        with self.voiceover("Chapter ten, the frontier. Is learning exactly compression?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def compression(self):
        c = load("compress")
        head = label(r"Keep four points, \ recover the rectangle", font_size=36).to_edge(UP, buff=0.3)
        plane = Square(side_length=4.6, stroke_color=GREY_C, stroke_width=1.5).next_to(head, DOWN, buff=0.45).shift(
            LEFT * 3.0)
        o = plane.get_corner(DL)

        def at(x, y):
            return o + np.array([x * 4.6, y * 4.6, 0])
        dots = VGroup(*[Dot(at(*p), radius=0.035, color=YES if lab else GREY_B)
                        for p, lab in zip(c["points"], c["labels"])])
        kept = VGroup(*[Circle(radius=0.13, color=HEAD, stroke_width=3).move_to(at(*c["points"][i])) for i in c["kept"]])
        x0, x1, y0, y1 = c["box"]
        box = Polygon(at(x0, y0), at(x1, y0), at(x1, y1), at(x0, y1), color=HEAD, stroke_width=2.5)
        side = VGroup(
            wrapped_label(rf"{c['m']} labelled points; \ keep only the leftmost, \ rightmost, \ lowest and highest "
                          r"positives; \ the tightest box through them labels all the rest correctly", 6.0,
                          font_size=19, color=WHITE),
            wrapped_label(r"a \textbf{compression scheme of size $k$}: \ any sample shrinks to $k$ points from "
                          r"which a consistent hypothesis can be rebuilt; \ it implies a PAC bound \ (Littlestone and "
                          r"Warmuth 1986)", 6.0, font_size=19, color=GREY_A),
            wrapped_label(r"the compression conjecture \ (Littlestone and Warmuth, \ 1986; \ Warmuth, \ 2003): \ every class of VC dimension $d$ has a scheme of size "
                          r"$O(d)$; \ Moran and Yehudayoff \ (2016): \ size $2^{O(d)}$ always exists", 6.0,
                          font_size=19, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(plane, RIGHT, buff=0.6)
        ok = "correctly" if c["consistent"] else "incorrectly"
        with self.voiceover(
            "A learner that generalizes must, in some sense, have compressed its data. <bookmark mark='a'/> Here are "
            f"{c['m']} points labelled by a hidden rectangle. <bookmark mark='b'/> Keep just four of them: the "
            "leftmost, rightmost, lowest and highest positive points. <bookmark mark='c'/> The tightest box through "
            f"those four labels every one of the {c['m']} points {ok}. Nick Littlestone and Manfred Warmuth called "
            "this a sample compression scheme, and showed in 1986 that a scheme of size k gives a learning bound "
            "much like VC dimension k. <bookmark mark='d'/> Warmuth conjectured that every class of VC dimension d "
            "has a scheme of size proportional to d. In 2016 Shay Moran and Amir Yehudayoff proved that a scheme of "
            "size exponential in d always exists. Whether linear size is always possible is still open."
        ) as vo:
            self.play(FadeIn(head), Create(plane))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.005), run_time=1.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(k) for k in kept], lag_ratio=0.2), FadeIn(side[0]))
            vo.wait_until("c")
            self.play(Create(box), FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def incontext(self):
        head = label(r"Learning without updating any weights", font_size=36).to_edge(UP, buff=0.3)
        tiles = VGroup(
            tile(r"in-context learning", r"a trained language model, \ shown a few examples in its prompt, \ "
                 r"predicts the next one: \ learning happens inside one forward pass \ (\textit{AI, Built} 13)", DATA),
            tile(r"what it might be", r"Garg et al. \ (2022): \ transformers trained on linear-regression prompts "
                 r"match least squares; \ constructions show attention can implement gradient steps", HEAD),
            tile(r"what theory lacks", r"bounds that explain when it works, \ how many examples a prompt needs, \ "
                 r"and why scale changes the answer", NO),
        ).arrange(RIGHT, buff=0.3).next_to(head, DOWN, buff=0.6)
        foot = wrapped_label(r"and double descent's second dip, \ benign overfitting \ (Bartlett et al. \ 2020), \ "
                             r"is understood for linear models; \ for deep networks, \ only partly", 12.4,
                             font_size=21, color=WHITE).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "The newest puzzle comes from language models. <bookmark mark='a'/> Shown a few input-output examples in "
            "its prompt, a trained model can predict the answer for a new input, without any change to its weights. "
            "<bookmark mark='b'/> In 2022 Shivam Garg and colleagues trained transformers on prompts of linear "
            "regression problems and found they matched least squares, and constructions show that attention can "
            "carry out steps of gradient descent. <bookmark mark='c'/> What theory still lacks is a bound that says "
            "when this works and how many examples a prompt needs. <bookmark mark='d'/> Double descent's second dip, "
            "benign overfitting, is now well understood for linear models like ours; for deep networks, only "
            "partly."
        ) as vo:
            self.play(FadeIn(head))
            for mk, t in zip("abc", tiles):
                vo.wait_until(mk)
                self.play(FadeIn(t, shift=UP * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def open(self):
        head = label(r"Open", font_size=36).to_edge(UP, buff=0.3)
        items = VGroup(
            wrapped_label(r"1. \ \textbf{Generalization of deep networks}: \ a bound that is not vacuous at the sizes "
                          r"used in practice.", 12.4, font_size=24, color=WHITE),
            wrapped_label(r"2. \ \textbf{In-context learning}: \ a theory of what prompts can teach.", 12.4,
                          font_size=24, color=YES),
            wrapped_label(r"3. \ \textbf{Learning with noise}: \ learning parity with noise in polynomial time? \ "
                          r"(much of cryptography assumes not)", 12.4, font_size=24, color=HEAD),
            wrapped_label(r"4. \ \textbf{Optimal bandits in structure}: \ matching upper and lower bounds for "
                          r"structured and adversarial settings.", 12.4, font_size=24, color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(head, DOWN, buff=0.45)
        star = wrapped_label(r"$\bigstar$ \ this part's research problem: \ the sample compression conjecture \ "
                             r"--- \ does every concept class of VC dimension $d$ have a compression scheme of size "
                             r"$O(d)$?", 12.4, font_size=23, color=LAM).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Open problems. <bookmark mark='a'/> A bound on the generalization of deep networks that is not vacuous "
            "at the sizes people actually use. <bookmark mark='b'/> A theory of what prompts can teach. "
            "<bookmark mark='c'/> Whether parity can be learned efficiently when some labels are flipped, which much "
            "of modern cryptography assumes is impossible. <bookmark mark='d'/> And matching upper and lower bounds "
            "for bandits with structure. <bookmark mark='e'/> This part's research problem is Warmuth's: does every "
            "class of VC dimension d have a compression scheme of size proportional to d?"
        ) as vo:
            self.play(FadeIn(head))
            for mk, it in zip("abcd", items):
                vo.wait_until(mk)
                self.play(FadeIn(it))
            vo.wait_until("e")
            self.play(FadeIn(star))
        self.wait(0.6)
        self.clear_scene()


_ = (DATA, KERN, LAM, NO, YES, grid_table)
