from __future__ import annotations

from videos.economics.econ17.common import *  # noqa: F403

APPS = ("ana", "bo", "chidi", "dara")
SHOPS = ("boatyard", "kiln", "loft", "grove")
SHORT = {"boatyard": "boatyard", "kiln": "kiln", "loft": "loft", "grove": "grove"}


def board_layout(b):
    """Apprentices on the left with their lists; workshops on the right with their rankings."""
    left, right = {}, {}
    g = VGroup()
    for i, k in enumerate(APPS):
        y = 2.0 - 1.25 * i
        chip = who_chip(k, 0.55, 18).move_to([-3.3, y, 0])
        lst = label(r" $>$ ".join(SHORT[s] for s in b["apprentices"][k]), font_size=19,
                    color=color_of(k)).next_to(chip, LEFT, buff=0.3)
        left[k] = chip
        g.add(chip, lst)
    for i, s in enumerate(SHOPS):
        y = 2.0 - 1.25 * i
        chip = place_chip(s, w=2.2, h=0.6, font_size=21).move_to([2.2, y, 0])
        rk = label(r" $>$ ".join(island.CAST[a].name for a in b["workshops"][s]), font_size=19,
                   color=PLACES[s]).next_to(chip, RIGHT, buff=0.3)
        right[s] = chip
        g.add(chip, rk)
    return g, left, right


class Stable(VoiceoverScene):
    def construct(self):
        card(self, 5, r"Stable matching: \ Gale and Shapley", r"Can apprentices and workshops be paired so that no "
             r"apprentice and workshop would both rather have each other?", "Chapter five. Stable matching: Gale and "
             "Shapley.", lit={1962: r"Gale and Shapley", 1984: r"Roth"}, scale=("person", "market"),
             horizon=("a year",))
        self.blocking()
        self.run()
        self.proof()

    def blocking(self):
        la = load("lattice")
        b = load("board")
        g, left, right = board_layout(b)
        lines = VGroup(*[Line(left[a].get_right(), right[s].get_left(), color=GREY_B, stroke_width=2.5)
                         for a, s in la["unstable"].items()])
        bp = la["blocking"][0]
        block = DashedLine(left[bp[0]].get_right(), right[bp[1]].get_left(), color=REJECT, stroke_width=4)
        head = label(r"a blocking pair: \ two who'd both rather have each other", font_size=26,
                     color=REJECT).to_edge(UP, buff=0.25)
        note = label(rf"{island.CAST[bp[0]].name} prefers {PLACE_NAMES[bp[1]]} to her workshop, \ and "
                     rf"{PLACE_NAMES[bp[1]]} prefers {island.CAST[bp[0]].name} to its apprentice", font_size=21,
                     color=REJECT).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Four apprentices, Ana, Bo, Chidi and Dara, are to be placed in four workshops. Each apprentice ranks "
            "the workshops, on the left, and each workshop ranks the apprentices, on the right. "
            "<bookmark mark='a'/> Here is one way to pair them. <bookmark mark='b'/> It has a problem. Dara would "
            "rather be at the boatyard than where she is, and the boatyard would rather have Dara than the "
            "apprentice it got. The two of them can simply walk off together, and the arrangement falls apart. "
            "Gale and Shapley called such a pair a blocking pair. <bookmark mark='c'/> A matching with no blocking "
            "pair is stable. Can one always be found?"
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(Create(lines), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(head), Create(block), FadeIn(note))
            vo.wait_until("c")
            self.play(Indicate(block, color=WHITE))
        self.clear_scene()

    def run(self):
        b = load("board")
        g, left, right = board_layout(b)
        head = label(r"deferred acceptance, \ apprentices asking", font_size=26, color=PROPOSE).to_edge(UP, buff=0.2)
        held = {}
        rnd = Integer(0, font_size=40, color=HELD).to_corner(UR, buff=0.4).shift(DOWN * 0.3)
        rlab = label(r"round", font_size=22, color=GREY_A).next_to(rnd, LEFT, buff=0.15)
        say = (
            "Gale and Shapley's answer is an algorithm, run in rounds. <bookmark mark='r1'/> In round one, every "
            "apprentice asks their favourite workshop. Ana and Dara both ask the boatyard, which prefers Dara: it "
            "holds on to her, not finally, just for now, and turns Ana away. Bo is held at the kiln, and Chidi at "
            "the net loft. <bookmark mark='r2'/> In round two, Ana asks her second choice, the kiln. The kiln "
            "prefers the Bo it already holds, and turns Ana away again. <bookmark mark='r3'/> Ana tries the net "
            "loft, which prefers her to Chidi: it lets Chidi go and holds Ana. <bookmark mark='r4'/> Chidi asks the "
            "boatyard, which still prefers Dara. <bookmark mark='r5'/> So Chidi asks the kiln, which prefers Chidi to "
            "Bo, and lets Bo go. <bookmark mark='r6'/> Bo asks the grove, which has nobody, and holds him. "
            "<bookmark mark='z'/> Nobody has been turned away this round, so the held offers become final. Ana goes "
            "to the net loft, Bo to the grove, Chidi to the kiln and Dara to the boatyard."
        )
        with self.voiceover(say) as vo:
            self.play(FadeIn(g), FadeIn(head), FadeIn(rlab), FadeIn(rnd))
            for i, rd in enumerate(b["a_log"]):
                vo.wait_until(f"r{i + 1}")
                self.play(rnd.animate.set_value(i + 1), run_time=0.3)
                arrows = {(p, s): Arrow(left[p].get_right(), right[s].get_left(), buff=0.12, color=PROPOSE,
                                        stroke_width=3, max_tip_length_to_length_ratio=0.06)
                          for p, s in rd["proposals"]}
                self.play(*[GrowArrow(a) for a in arrows.values()], run_time=0.9)
                anims = []
                for (p, s), a in arrows.items():
                    if p in rd["rejected"]:
                        anims.append(a.animate.set_color(REJECT).set_opacity(0.0))
                    else:
                        line = Line(left[p].get_right(), right[s].get_left(), color=HELD, stroke_width=4)
                        anims.append(Transform(a, line))
                        held[p] = a
                for p in rd["rejected"]:
                    if p in held and all(p != q for q, _ in rd["proposals"]):
                        anims.append(held.pop(p).animate.set_color(REJECT).set_opacity(0.0))
                self.play(*anims, run_time=0.9)
            vo.wait_until("z")
            self.play(*[m.animate.set_color(STABLE) for m in held.values()])
        self.clear_scene()

    def proof(self):
        rows = VGroup(
            label(r"it ends: \ nobody asks the same workshop twice", font_size=25),
            label(r"everyone ends up placed, \ if there are places and everyone is acceptable", font_size=24,
                  color=GREY_A),
            label(r"it is stable: \ if Ana prefers a workshop to her own, \ she asked it first", font_size=24,
                  color=STABLE),
            label(r"and it turned her away, \ for someone it liked better; \ and a workshop's holdings only improve",
                  font_size=24, color=STABLE),
            label(r"so that workshop prefers whoever it ends with to Ana: \ no blocking pair", font_size=25,
                  color=E.ACCENT),
            label(r"Gale and Shapley, \ 1962: \ a stable matching always exists", font_size=25, color=PROPOSE),
        ).arrange(DOWN, buff=0.4).move_to(UP * 0.1)
        tag = published_tag(r"Gale and Shapley, Amer.\ Math.\ Monthly 69(1) (1962)", corner=DR, font_size=13)
        with self.voiceover(
            "Why does it always work? <bookmark mark='a'/> It must end, because no apprentice asks the same "
            "workshop twice. <bookmark mark='b'/> With enough places and everyone acceptable, everyone ends up "
            "placed. <bookmark mark='c'/> And it is stable. Suppose Ana prefers some workshop to the one she ends "
            "with. Then she asked it earlier, <bookmark mark='d'/> and it turned her away for someone it liked "
            "better. A workshop only ever trades up, so it ends with someone it likes even more. "
            "<bookmark mark='e'/> So that workshop does not want Ana back, and no blocking pair can exist. "
            "<bookmark mark='f'/> That is Gale and Shapley's theorem of 1962: a stable matching always exists, "
            "and the algorithm finds one."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("bcdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
