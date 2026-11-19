from __future__ import annotations

from videos.economics.econ17.common import *  # noqa: F403

ORDER = ("boatyard", "kiln", "loft")


def places(p, y=1.2, dx=4.0):
    """The three workshops as columns of empty seats."""
    cols = {}
    g = VGroup()
    for i, k in enumerate(ORDER):
        x = (i - 1) * dx
        head = place_chip(k, w=2.6).move_to([x, y, 0])
        seats = VGroup(*[RoundedRectangle(width=1.5, height=0.95, corner_radius=0.1, stroke_color=PLACES[k],
                                          stroke_width=2, stroke_opacity=0.6) for _ in range(p["capacity"][k])])
        seats.arrange(RIGHT, buff=0.15).next_to(head, DOWN, buff=0.25)
        cols[k] = (head, seats)
        g.add(head, seats)
    return g, cols


def lists_card(p, font_size=19):
    rows = VGroup()
    for k in ("you", "ana", "bo", "dara"):
        prefs = p["students"][k]
        t = r" $>$ ".join(PLACE_NAMES[s].replace("the ", "") for s in prefs)
        name = "you" if k == "you" else island.CAST[k].name
        rows.add(label(rf"{name}: \ {t}", font_size=font_size, color=color_of(k)))
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    lot = label(r"lottery: \ " + r", \ ".join("you" if k == "you" else island.CAST[k].name for k in p["lottery"]),
                font_size=font_size, color=HELD)
    return VGroup(rows, lot).arrange(DOWN, aligned_edge=LEFT, buff=0.2)


class PlayIt(VoiceoverScene):
    def construct(self):
        card(self, 1, r"Play it: \ rank three workshops", r"The boatyard is your favourite. \ Under the Boston rule, \ "
             r"should you put it first?", "Chapter one. Play it: rank three workshops.",
             lit={2003: r"Abdulkadiroğlu and Sönmez", 2005: r"Boston changes its rule"}, scale=("person", "city"),
             horizon=("a year",))
        self.rules()
        self.truth()
        self.strategy()
        self.da()

    def rules(self):
        p = load("playit")
        stage = game_stage(12.4, 6.1, center=DOWN * 0.15)
        lines = VGroup(
            label(r"four children, \ three workshops taking apprentices: \ one place at the boatyard, \ one at the "
                  r"kiln, \ two at the net loft", font_size=24),
            label(r"each child lists the workshops in order; \ one lottery decides every tie", font_size=24),
            label(r"the Boston rule: \ round 1, \ everyone applies to the first workshop on their list; \ places go "
                  r"by lottery, \ and are final", font_size=24, color=SCHOOL),
            label(r"round 2: \ those still without a place apply to their second, \ if it has room; \ and so on",
                  font_size=24, color=SCHOOL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24).move_to(stage.box.get_center() + UP * 1.45)
        if lines.width > 11.6:
            lines.scale_to_fit_width(11.6).move_to(stage.box.get_center() + UP * 1.45)
        lc = lists_card(p, font_size=23).move_to(stage.box.get_center() + DOWN * 1.15 + LEFT * 2.7)
        ask = VGroup(label(r"you love the boatyard, \ then the kiln", font_size=25, color=YOU),
                     label(r"do you list the boatyard first, \\ or the kiln?", font_size=27, color=E.ACCENT)
                     ).arrange(DOWN, buff=0.15).move_to(stage.box.get_center() + DOWN * 0.9 + RIGHT * 3.3)
        ring = countdown().next_to(ask, DOWN, buff=0.3)
        with self.voiceover(
            "You are one of four island children, and three workshops are taking apprentices: one place at the "
            "boatyard, one at the kiln, and two at the net loft. <bookmark mark='a'/> Each child lists the workshops "
            "in order, and a single lottery decides every tie. <bookmark mark='b'/> The places are given out by what "
            "was called the Boston rule. In round one, everyone applies to the first workshop on their list, and "
            "places go by lottery, for good. <bookmark mark='c'/> In round two, those still without a place apply to "
            "their second choice, if it has room left, and so on. <bookmark mark='d'/> Here is what everyone wants, "
            "and the lottery: Ana drew first, Bo second, you third, and Dara fourth. <bookmark mark='e'/> You love "
            "the boatyard most, then the kiln. Do you put the boatyard first on your list, or the kiln? Pause, and "
            "decide."
        ) as vo:
            self.play(FadeIn(stage), FadeIn(lines[0]))
            for mk, r in zip("abc", lines[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(lc))
            vo.wait_until("e")
            self.play(FadeIn(ask), FadeIn(ring))
        self.add(ring[1])
        self.play(ring.t.animate.set_value(0.0), run_time=8.0, rate_func=linear)
        self.clear_scene()

    def run(self, log, title, color, say, result_line, marks="abcd"):
        """Animate a Boston (or DA) log on the three columns."""
        p = load("playit")
        board, cols = places(p)
        chips = {k: who_chip(k, 0.5, 17) for k in ("you", "ana", "bo", "dara")}
        pool = VGroup(*chips.values()).arrange(RIGHT, buff=0.9).move_to(DOWN * 2.3 + LEFT * 3.2)
        head = label(title, font_size=28, color=color).to_edge(UP, buff=0.35)
        used = {k: 0 for k in ORDER}
        res = label(result_line, font_size=25, color=E.ACCENT).to_edge(DOWN, buff=0.35)
        rounds = VGroup()
        for i, rd in enumerate(log):
            txt = r"round " + str(i + 1) + r": \ " + r"; \ ".join(
                ("you" if s == "you" else island.CAST[s].name) + r" $\to$ " + PLACE_NAMES[w].replace("the ", "")
                for s, w in rd["admitted"])
            rounds.add(label(txt if rd["admitted"] else rf"round {i + 1}: \ no room for you", font_size=22,
                             color=GREY_A))
        rounds.arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to(DOWN * 0.9 + RIGHT * 2.6)
        with self.voiceover(say) as vo:
            self.play(FadeIn(head), FadeIn(board), FadeIn(pool))
            for i, rd in enumerate(log):
                if i < len(marks):
                    vo.wait_until(marks[i])
                moves = []
                for s, w in rd["admitted"]:
                    seat = cols[w][1][used[w]]
                    used[w] += 1
                    moves.append(chips[s].animate.scale(0.9).move_to(seat))
                if moves:
                    self.play(*moves, FadeIn(rounds[i]), run_time=1.2)
                else:
                    self.play(FadeIn(rounds[i]))
            vo.wait_until("z")
            self.play(FadeIn(res))
        self.clear_scene()

    def truth(self):
        p = load("playit")
        log = [rd for rd in p["boston_log"]]
        self.run(log, r"the Boston rule, \ if you tell the truth", SCHOOL,
                 "Suppose you told the truth, and put the boatyard first. <bookmark mark='a'/> In round one, Ana and "
                 "you apply to the boatyard, and Ana's lottery number is better, so she takes its one place. Dara "
                 "applies to the kiln, her favourite, and gets it. Bo applies to the net loft and gets a place. "
                 "<bookmark mark='b'/> In round two you apply to the kiln, your second choice. But Dara took it in "
                 "round one, and round-one places are final. <bookmark mark='c'/> In round three you apply to the "
                 "net loft, which still has a place. <bookmark mark='z'/> Telling the truth got you your last "
                 "choice.",
                 r"you told the truth, \ and got your last choice", marks="abc")

    def strategy(self):
        p = load("playit")
        gets = {tuple(r["report"]): r["gets"] for r in p["boston_reports"]}
        lie = gets[("kiln", "boatyard", "loft")]
        rows = VGroup(
            label(r"list the kiln first instead:", font_size=26, color=YOU),
            label(r"round 1: \ you and Dara both apply to the kiln; \ your lottery number is better", font_size=23),
            label(rf"you get {PLACE_NAMES[lie]}, \ your second choice; \ Dara ends at the net loft", font_size=24,
                  color=STABLE),
            label(r"under the Boston rule, \ listing your true favourite first can cost you your second choice",
                  font_size=24, color=REJECT),
            label(r"and it is unfair: \ Dara got the kiln though you wanted it and drew the better number",
                  font_size=23, color=GREY_A),
            label(r"a family that plays the system beats one that tells the truth", font_size=24, color=E.ACCENT),
        ).arrange(DOWN, buff=0.36).move_to(UP * 0.1)
        with self.voiceover(
            "Now suppose you had put the kiln first. <bookmark mark='a'/> In round one, you and Dara both apply "
            "to the kiln, and your lottery number is better than Dara's. <bookmark mark='b'/> You get the kiln, your "
            "real second choice, and Dara ends up at the net loft. <bookmark mark='c'/> Under the Boston rule, "
            "listing your true favourite first can cost you your second choice as well. <bookmark mark='d'/> And "
            "when you told the truth, the outcome was unfair: Dara got the kiln, though you wanted it more than the "
            "loft and drew the better number. <bookmark mark='e'/> A family that plays the system beats one that "
            "tells the truth, and in Boston, Atila Abdulkadiroğlu and Tayfun Sönmez pointed out in 2003, the rule "
            "rewarded families who knew that."
        ) as vo:
            self.play(FadeIn(rows[0]))
            for mk, r in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def da(self):
        p = load("playit")
        best = p["da"]["you"]
        rows = VGroup(
            label(r"the alternative: \ deferred acceptance", font_size=28, color=STABLE),
            label(r"each workshop only holds its best applicants so far; \ nothing is final until the end",
                  font_size=23),
            label(r"you apply to the boatyard: \ held for Ana, \ not you; \ then to the kiln, \ where you displace "
                  r"Dara", font_size=22, color=GREY_A),
            label(rf"you get {PLACE_NAMES[best]} by telling the truth; \ no list you could write does better",
                  font_size=24, color=STABLE),
            label(r"in 2005 Boston switched to it; \ chapter five shows why it works", font_size=23,
                  color=E.ACCENT),
        ).arrange(DOWN, buff=0.4).move_to(UP * 0.1)
        tag = published_tag(r"Abdulkadiroğlu and Sönmez, AER 93(3) (2003); \ Roth, Nobel lecture (2012)", corner=DR,
                            font_size=13)
        with self.voiceover(
            "There is another way to run the same lists. <bookmark mark='a'/> In deferred acceptance, a workshop "
            "only holds on to its best applicants so far, and nothing is final until nobody is turned away. "
            "<bookmark mark='b'/> You apply to the boatyard, which holds Ana instead. Then you apply to the kiln, "
            "where your lottery number beats Dara's, and the kiln lets her go. <bookmark mark='c'/> You get the "
            "kiln by telling the truth, and no list you could write would do better. <bookmark mark='d'/> Boston "
            "switched to this rule in 2005, and chapter five shows why it works."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
