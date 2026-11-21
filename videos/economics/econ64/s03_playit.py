from __future__ import annotations

from videos.economics.econ64.common import *  # noqa: F403

LETTERS = "ABCDEFGHIJ"


def case_card(ltr, r, w=2.35, h=2.2):
    box = RoundedRectangle(width=w, height=h, corner_radius=0.12, stroke_color=GREY_B, stroke_width=1.6,
                           fill_color=GREY_E, fill_opacity=0.35)
    lines = VGroup(
        label(ltr, font_size=26, color=E.ACCENT),
        label(rf"age {r['age']}", font_size=17, color=WHITE),
        label(rf"{r['priors']} prior arrest{'s' if r['priors'] != 1 else ''}", font_size=17, color=WHITE),
        label(rf"{r['missed']} missed date{'s' if r['missed'] != 1 else ''}", font_size=17, color=WHITE),
        label(rf"charge: \ {r['charge']}", font_size=17, color=WHITE),
        label(r"has a job" if r["employed"] else r"no job", font_size=17, color=WHITE),
    ).arrange(DOWN, buff=0.08)
    lines.move_to(box)
    return VGroup(box, lines)


class PlayIt(VoiceoverScene):
    def construct(self):
        card(self, 2, r"Play it: \ ten cases", r"You may detain three of ten defendants: \ which three?",
             "Chapter two. Play it: ten cases.", scale=("person",), horizon=("a day",))
        self.stage()
        self.reveal()

    def grid(self):
        rows = load("cases")["rows"]
        cards = VGroup(*[case_card(LETTERS[k], r) for k, r in enumerate(rows)])
        cards.arrange_in_grid(rows=2, cols=5, buff=(0.25, 0.35)).move_to(DOWN * 0.15)
        if cards.width > 13.0:
            cards.width = 13.0
        return rows, cards

    def stage(self):
        rows, cards = self.grid()
        head = label(r"the Island's court, \ one morning: \ detain three, \ release seven", font_size=24,
                     color=GREY_A).to_edge(UP, buff=0.4)
        tag = island_tag(r"the Island: \ ten defendants from the test half; \ agora.learn.cases", corner=DL,
                         font_size=12)
        with self.voiceover(
            "Your turn. One morning in the Island's court, ten defendants, and room in the jail for three. You see "
            "what the judge's file shows: <bookmark mark='a'/> age, prior arrests, how many court dates they have "
            "missed before, the charge, and whether they have a job. <bookmark mark='b'/> The law asks one thing: "
            "who is least likely to come back to court? Remember that the charge is about the past, not about "
            "coming back. <bookmark mark='c'/> Which three would you detain?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in cards], lag_ratio=0.12), run_time=2.5)
            vo.wait_until("b")
            vo.wait_until("c")
        ring = countdown().scale(0.5).to_edge(DOWN, buff=0.15)
        self.play(FadeIn(ring))
        self.add(ring[1])
        self.play(ring.t.animate.set_value(0.0), run_time=8.0, rate_func=linear)
        self.play(FadeOut(ring))
        self.wait(0.3)
        self.clear_scene()

    def reveal(self):
        rows, cards = self.grid()
        risk = np.array([r["risk"] for r in rows])
        p = np.array([r["p"] for r in rows])
        alg = set(np.argsort(-risk)[:3])
        judge = {k for k, r in enumerate(rows) if not r["released"]}
        best = set(np.argsort(-p)[:3])
        tags_ = VGroup()
        for k, (c, r) in enumerate(zip(cards, rows)):
            t = VGroup(label(rf"algorithm: \ {100 * r['risk']:.0f}\%", font_size=15, color=ALGO),
                       label(r"judge: \ detained" if not r["released"] else r"judge: \ released", font_size=15,
                             color=JUDGE),
                       label(rf"truth: \ {100 * r['p']:.0f}\%", font_size=15, color=TRUTHC)).arrange(DOWN, buff=0.04)
            t.move_to(c[0].get_bottom() + UP * 0.42)
            tags_.add(t)
        e_alg, e_j, e_b = sum(p[k] for k in alg), sum(p[k] for k in judge), sum(p[k] for k in best)
        hi = [k for k in alg]
        summ = VGroup(
            label(rf"the algorithm's three: \ {', '.join(LETTERS[k] for k in sorted(alg))}; \ failures prevented, "
                  rf"on average, \ {e_alg:.2f}", font_size=20, color=ALGO),
            label(rf"the judge's three: \ {', '.join(LETTERS[k] for k in sorted(judge))}; \ {e_j:.2f}", font_size=20,
                  color=JUDGE),
        ).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.2)
        tag = island_tag(r"the Island: \ truth planted, \ courtroom signal included", corner=DL, font_size=12)
        jv = [k for k in judge if rows[k]["charge"] == "violent"]
        with self.voiceover(
            "Here is what lay behind the files. <bookmark mark='a'/> Under each defendant, the algorithm's predicted "
            "chance of failing to appear, what the judge did, and the true chance the Island knows. <bookmark "
            f"mark='b'/> The algorithm detains {', '.join(LETTERS[k] for k in sorted(alg))}: the youngest, with the "
            "most missed court dates. On average, detaining them prevents "
            f"{e_alg:.2f} failures to appear. <bookmark mark='c'/> The judge detained "
            f"{', '.join(LETTERS[k] for k in sorted(judge))}, {len(jv)} of them charged with violence, which on the "
            f"Island says little about coming back: {e_j:.2f} failures prevented. <bookmark mark='d'/> The best "
            f"possible three would prevent {e_b:.2f}. How did your three do? Add up their true chances. The judge "
            "is not foolish: the charge is vivid, and the law cares about it in other ways. But for this one "
            "question, the record of missed dates is what predicts."
        ) as vo:
            self.play(FadeIn(cards), FadeIn(tag))
            vo.wait_until("a")
            self.play(*[c[1].animate.shift(UP * 0.3).set_opacity(0.6) for c in cards], run_time=0.6)
            self.play(LaggedStart(*[FadeIn(t) for t in tags_], lag_ratio=0.1), run_time=2.0)
            vo.wait_until("b")
            self.play(*[cards[k][0].animate.set_stroke(ALGO, width=4) for k in hi], FadeIn(summ[0]))
            vo.wait_until("c")
            self.play(*[cards[k][0].animate.set_stroke(JUDGE, width=4) for k in judge if k not in alg],
                      FadeIn(summ[1]))
            vo.wait_until("d")
        self.clear_scene()
