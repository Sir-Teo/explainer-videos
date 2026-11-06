from __future__ import annotations

from videos.philosophy.philosophy4.common import *  # noqa: F403


def dtex(s: str) -> str:
    """A deontic sentence in Reasoner syntax, with O for the box."""
    return modal.show(modal.parse(s.replace("O(", "[](")), tex=True).replace(r"\Box", r"\mathsf{O}")


class Deontic(VoiceoverScene):
    def construct(self):
        card = chapter_card(10, r"The logic of obligation", r"Can `ought' be calculated?", lit=(1951,), part=PART)
        with self.voiceover("Chapter ten. The logic of obligation."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.sdl()
        self.ross()
        self.chisholm()
        self.verdict()

    def sdl(self):
        hc = history_card(1951, r"Georg Henrik von Wright", r"`Deontic logic', \textit{Mind}", width=5.4,
                          color=HIST).to_corner(UL, buff=0.35)
        rows = VGroup(
            VGroup(MathTex(r"\mathsf{O}\,p", font_size=40, color=GOAL),
                   label(r"$p$ is obligatory: \ true in every ideal world", font_size=24)),
            VGroup(MathTex(r"\mathsf{P}\,p = \lnot \mathsf{O} \lnot p", font_size=40, color=GOAL),
                   label(r"$p$ is permitted: \ true in some ideal world", font_size=24)),
            VGroup(MathTex(r"\mathsf{O}\,p \to \mathsf{P}\,p", font_size=40, color=GOAL),
                   label(r"axiom D: \ every world sees an ideal world \ (no impossible duties)", font_size=24)),
            VGroup(MathTex(r"\mathsf{O}\,p \to p", font_size=40, color=BAD),
                   label(r"not an axiom: \ duties are sometimes broken", font_size=24, color=BAD))).arrange(
            DOWN, aligned_edge=LEFT, buff=0.35)
        x = max(r[0].width for r in rows) + 0.5
        for r in rows:
            r[0].set_x(r[0].width / 2)
            r[1].set_x(x + r[1].width / 2).set_y(r[0].get_y())
        rows.move_to([0.4, -0.6, 0])
        name = label(r"standard deontic logic \ $=$ \ KD", font_size=28, color=CONN).to_corner(UR, buff=0.5)
        with self.voiceover(
            "In 1951 Georg Henrik von Wright proposed a logic of 'ought'. In Kripke's terms it is simple. "
            "<bookmark mark='a'/>p is obligatory when p is true in every ideal world, every world where all duties "
            "are met. <bookmark mark='b'/>p is permitted when it is true in some ideal world. <bookmark mark='c'/>"
            "And there is always at least one ideal world: what is obligatory is permitted. That is axiom D. "
            "<bookmark mark='d'/>But not axiom T: what ought to be is not always so. The result, K plus D, is "
            "standard deontic logic."
        ) as vo:
            self.play(FadeIn(hc), FadeIn(name))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
        self.clear_scene()

    def ross(self):
        d = load("deontic")
        hc = history_card(1941, r"Alf Ross", r"`Imperatives and logic'", width=4.6, color=HIST).to_corner(UL, buff=0.35)
        f = VGroup(MathTex(r"\mathsf{O}\,(\text{mail})", r"\ \to\ ", r"\mathsf{O}\,(\text{mail} \lor \text{burn})",
                           font_size=42),
                   label(r"`you ought to mail the letter; \ so you ought to mail it or burn it'", font_size=26,
                         color=GREY_A)).arrange(DOWN, buff=0.3).move_to([0, 0.2, 0])
        f[0][2].set_color(BAD)
        v = label(r"valid in SDL \ (checked on every serial frame of up to 3 worlds) \ $\checkmark$", font_size=24,
                  color=OK if d["ross_valid"] else BAD).to_edge(DOWN, buff=0.9)
        r = label(r"odd, \ but arguably harmless: \ burning does not discharge the duty", font_size=24,
                  color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The logic has odd theorems. <bookmark mark='a'/>Alf Ross noticed in 1941 that from 'you ought to mail "
            "the letter' it follows that 'you ought to mail it or burn it'. <bookmark mark='b'/>The Reasoner confirms "
            "it is valid in standard deontic logic. <bookmark mark='c'/>Most logicians take this as odd but harmless: "
            "the disjunctive duty is only satisfied by burning if mailing is also done, since the original duty "
            "remains."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(Write(f[0]), FadeIn(f[1]))
            vo.wait_until("b")
            self.play(FadeIn(v))
            vo.wait_until("c")
            self.play(FadeIn(r))
        self.clear_scene()

    def chisholm(self):
        hc = history_card(1963, r"Roderick Chisholm", r"`Contrary-to-duty imperatives'", width=5.2,
                          color=HIST).to_corner(UL, buff=0.35)
        story = VGroup(label(r"1. \ It ought to be that Jones goes to help his neighbours.", font_size=26),
                       label(r"2. \ It ought to be that, if he goes, he tells them he is coming.", font_size=26),
                       label(r"3. \ If he does not go, he ought not to tell them.", font_size=26),
                       label(r"4. \ He does not go.", font_size=26)).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        story.move_to([0.4, -0.5, 0])
        cap = label(r"consistent, \ and no sentence follows from the others", font_size=26, color=GOAL).to_edge(
            DOWN, buff=0.5)
        with self.voiceover(
            "In 1963 Roderick Chisholm found a deeper problem, with an ordinary story. <bookmark mark='a'/>Jones "
            "ought to go to help his neighbours. <bookmark mark='b'/>It ought to be that, if he goes, he tells them he "
            "is coming. <bookmark mark='c'/>If he does not go, he ought not to tell them. <bookmark mark='d'/>And he "
            "does not go. <bookmark mark='e'/>These four sentences are consistent, and none of them follows from the "
            "others. The third is a contrary-to-duty obligation: what you ought to do once you have already failed."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, s_ in zip("abcd", story):
                vo.wait_until(mk)
                self.play(FadeIn(s_, shift=RIGHT * 0.2))
            vo.wait_until("e")
            self.play(FadeIn(cap))
        self.clear_scene()

    def verdict(self):
        d = load("deontic")
        hd = [label(t, font_size=22, color=P.CLAIM) for t in (r"version", r"sentences 2 and 3", r"consistent?",
                                                              r"independent?")]
        rows = []
        for k, v in d["versions"].items():
            s2, s3 = v["sentences"][1], v["sentences"][2]
            dep = [i + 1 for i, x in enumerate(v["independent"]) if not x]
            rows.append([label(k, font_size=24), MathTex(dtex(s2) + r",\quad " + dtex(s3), font_size=26),
                         tv(v["consistent"]),
                         label(r"yes" if not dep else rf"no: \ {', '.join(map(str, dep))} follow" + ("s" if len(dep) == 1 else ""), font_size=22,
                               color=OK if not dep else BAD)])
        grid = ValueGrid(hd, rows, col_w=[1.4, 5.4, 2.0, 3.2], cell_h=0.62, font_size=22).move_to([0, 0.6, 0])
        all_fail = all((not v["consistent"]) or not all(v["independent"]) for v in d["versions"].values())
        verdict = label(r"every version is inconsistent \ or makes one sentence redundant", font_size=28,
                        color=BAD if all_fail else OK).to_edge(DOWN, buff=1.0)
        fix = label(r"responses: \ dyadic obligation $\mathsf{O}(q \mid p)$ \ (Hansson 1969, Lewis 1973); \ the Wall "
                    r"for SDL", font_size=24, color=GREY_A).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Now formalize the story in standard deontic logic. Sentences one and four are clear: O of g, and not g. "
            "Sentences two and three can each be written two ways: the obligation can govern the whole conditional, "
            "or only its consequent. <bookmark mark='a'/>That gives four versions. The Reasoner checked each one, "
            "searching all serial models of up to three worlds for consistency, and for whether any sentence follows "
            "from the other three. <bookmark mark='b'/>Version C is inconsistent: from one and two, Jones ought to "
            "tell; from three and four, he ought not to; and D forbids both. Versions A, B and D are consistent, but "
            "in each, at least one sentence follows from the others, though in the story none does. "
            "<bookmark mark='c'/>No version captures the story. Chisholm's paradox led to logics of conditional "
            "obligation, 'ought q, given p', and it marks a limit of the simple semantics."
        ) as vo:
            self.play(FadeIn(grid.head), FadeIn(grid.rows_bg), FadeIn(grid.rule))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(grid.cell[r][0], grid.cell[r][1])) for r in range(4)],
                                  lag_ratio=0.3))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(grid.cell[r][2], grid.cell[r][3])) for r in range(4)],
                                  lag_ratio=0.3))
            vo.wait_until("c")
            self.play(FadeIn(verdict), FadeIn(fix))
        self.clear_scene()
