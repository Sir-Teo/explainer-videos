from __future__ import annotations

from videos.philosophy.philosophy6.common import *  # noqa: F403


def draw_hydra(tree, base=ORIGIN, width=4.0, level=0.9, color=SETC):
    """A hydra drawn upward from its root: leaves (heads) spread evenly, each node above the middle of its
    children's span."""
    base = np.asarray(base, float)

    def leaves(t):
        return 1 if not t else sum(leaves(c) for c in t)

    total = max(leaves(tree), 1)
    lines, heads, joints = VGroup(), VGroup(), VGroup()

    def place(t, x0, depth):
        n = leaves(t)
        x = x0 + n / 2
        p = base + np.array([(x / total - 0.5) * width, depth * level, 0])
        cx = x0
        for c in t:
            q = place(c, cx, depth + 1)
            lines.add(Line(p, q, color=color, stroke_width=3))
            cx += leaves(c)
        if t:
            joints.add(Dot(p, radius=0.06, color=color))
        elif depth:
            heads.add(VGroup(Circle(radius=0.14, color=BAD, fill_color=BAD, fill_opacity=0.6, stroke_width=2).move_to(p),
                             Dot(p + np.array([0.05, 0.03, 0]), radius=0.025, color=WHITE)))
        return p

    root = place(tree, 0, 0)
    ground = Line(root + LEFT * 0.6, root + RIGHT * 0.6, color=GREY_B, stroke_width=4)
    return VGroup(ground, lines, joints, heads)


class Hydra(VoiceoverScene):
    def construct(self):
        card = chapter_card(11, r"Hercules and the hydra", r"Can you win against a monster that keeps growing?",
                            lit=(1982,), part=PART)
        with self.voiceover("Chapter eleven. Hercules and the hydra."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.rules()
        self.battle()
        self.counts()

    def rules(self):
        d = load("hydra")
        hc = history_card(1982, r"Laurie Kirby \& Jeff Paris", r"`Accessible independence results for Peano "
                          r"arithmetic'", width=6.6, color=HIST).to_corner(UL, buff=0.35)
        h0 = draw_hydra((((), ()),), base=[-4.6, -2.4, 0], width=2.4)
        h1 = draw_hydra((((),), ((),)), base=[-4.6, -2.4, 0], width=2.4)
        rules = VGroup(label(r"the hydra is a tree; \ its heads are the leaves", font_size=24),
                       label(r"Hercules cuts off one head at each blow", font_size=24),
                       label(r"if the head grew from the root: \ it is simply gone", font_size=24, color=GREY_A),
                       VGroup(label(r"otherwise, at blow $n$, the neck that lost it", font_size=24, color=BAD),
                              label(r"grows back $n$ new copies of itself, \ from the node below", font_size=24,
                                    color=BAD)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.32)
        rules.next_to([-1.6, -0.5, 0], RIGHT, buff=0)
        cap = label(r"blow 1: \ one new copy of the neck", font_size=22, color=BAD).next_to(h1, DOWN, buff=0.25)
        with self.voiceover(
            "Here is a second theorem of the same kind, dressed as a myth, from Laurie Kirby and Jeff Paris in "
            "1982. <bookmark mark='a'/>The hydra is a tree. Its heads are the leaves. <bookmark mark='b'/>Hercules "
            "cuts off one head with each blow. <bookmark mark='c'/>If the head grew straight from the root, it is "
            "simply gone. <bookmark mark='d'/>Otherwise the hydra takes revenge. At the n-th blow, the neck that "
            "lost the head grows back n extra copies of itself, from the node below. The longer the fight, the "
            "faster it grows."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(h0), FadeIn(rules[0]))
            for mk, r in zip("bcd", rules[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
            cut = h0[3][1]
            h0[3].remove(cut)
            self.play(Flash(cut.get_center(), color=BAD, flash_radius=0.3))
            self.play(FadeOut(cut, scale=0.4), run_time=0.6)
            self.play(ReplacementTransform(h0, h1), FadeIn(cap), run_time=1.6)
        self.clear_scene()

    def battle(self):
        d = load("hydra")
        B = d["battle"]

        def tup(x):
            return tuple(tup(c) for c in x)

        frames = [draw_hydra(tup(b["tree"]), base=[-1.2, -2.7, 0], width=5.0) for b in B]
        info = [VGroup(MathTex(rf"\text{{blow }} {b['step']}", font_size=30, color=GREY_A),
                       MathTex(b["ordinal"], font_size=40, color=ORD)).arrange(DOWN, buff=0.25).move_to([4.4, 0.6, 0])
                for b in B]
        head = label(r"The battle, blow by blow, \ with the hydra's ordinal", font_size=30, color=CONN).to_edge(
            UP, buff=0.4)
        end = label(rf"dead after {d['steps']} blows", font_size=30, color=OK).move_to([4.4, -1.4, 0])
        with self.voiceover(
            "Watch a small battle, as the Reasoner plays it. <bookmark mark='a'/>A single neck with two heads. "
            "Hercules always cuts the rightmost head. <bookmark mark='b'/>After the first blow there are two necks; "
            "after the second, three more heads. The hydra grows. <bookmark mark='c'/>But beside it is an ordinal, "
            "computed from the tree: each neck contributes omega to the power of what grows on it. At every blow "
            "the ordinal goes down, even when the hydra gets bigger. <bookmark mark='d'/>Once it falls below omega, "
            "only bare heads remain, and they go one by one. This hydra dies after thirteen blows."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(frames[0]), FadeIn(info[0]))
            vo.wait_until("b")
            for i in (1, 2):
                self.play(FadeOut(frames[i - 1]), FadeIn(frames[i]), FadeOut(info[i - 1]), FadeIn(info[i]),
                          run_time=0.9)
            vo.wait_until("c")
            for i in range(3, 7):
                self.play(FadeOut(frames[i - 1]), FadeIn(frames[i]), FadeOut(info[i - 1]), FadeIn(info[i]),
                          run_time=0.8)
            vo.wait_until("d")
            for i in range(7, len(frames)):
                self.play(FadeOut(frames[i - 1]), FadeIn(frames[i]), FadeOut(info[i - 1]), FadeIn(info[i]),
                          run_time=0.45)
            self.play(FadeOut(frames[-1]), FadeIn(end))
        self.clear_scene()

    def counts(self):
        d = load("hydra")
        head = label(r"A neck with $k$ heads: \ how many blows?", font_size=32, color=CONN).to_edge(UP, buff=0.5)
        hd = [label(r"$k$", font_size=24, color=P.CLAIM), label(r"ordinal", font_size=24, color=P.CLAIM),
              label(r"blows until the hydra dies", font_size=24, color=P.CLAIM)]
        rows = []
        for c in d["counts"]:
            s = c["steps"]
            txt = (f"{int(s):,}".replace(",", "{,}") if s else r"\text{more than } 10^{3000}")
            rows.append([MathTex(str(c["k"]), font_size=30), MathTex(c["ordinal"], font_size=30, color=ORD),
                         MathTex(txt, font_size=30, color=GOAL if s else BAD)])
        grid = ValueGrid(hd, rows, col_w=[1.0, 2.0, 5.6], cell_h=0.7, font_size=28).move_to([0, 0.5, 0])
        thm = VGroup(label(r"yet every strategy wins, \ against every hydra: \ the ordinals cannot fall forever",
                           font_size=26, color=OK),
                     label(r"and, like Goodstein's theorem, \ this cannot be proved in Peano arithmetic", font_size=24,
                           color=GREY_A)).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Now make the neck a little longer. <bookmark mark='a'/>With one head, three blows. With two, thirteen. "
            "<bookmark mark='b'/>With three heads, the Reasoner counts twenty-two trillion, five hundred and thirty-"
            "nine billion, nine hundred and eighty-eight million, three hundred and sixty-nine thousand, four "
            "hundred and five blows. <bookmark mark='c'/>With four, it stops counting past ten to the three "
            "thousand. <bookmark mark='d'/>And yet Hercules always wins, whatever head he cuts, against any hydra, "
            "because each blow lowers an ordinal below epsilon zero. And, like Goodstein's theorem, this cannot be "
            "proved in ordinary arithmetic."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), FadeIn(grid.rows_bg), FadeIn(grid.rule))
            vo.wait_until("a")
            self.play(*[FadeIn(c) for r in (0, 1) for c in grid.cell[r]])
            vo.wait_until("b")
            self.play(*[FadeIn(c) for c in grid.cell[2]])
            vo.wait_until("c")
            self.play(*[FadeIn(c) for c in grid.cell[3]])
            vo.wait_until("d")
            self.play(FadeIn(thm))
        self.clear_scene()
