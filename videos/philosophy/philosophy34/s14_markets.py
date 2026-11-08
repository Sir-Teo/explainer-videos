from __future__ import annotations

from videos.philosophy.philosophy34.common import *  # noqa: F403


class Markets(VoiceoverScene):
    def construct(self):
        card = chapter_card(13, r"Markets by design", r"Can a market be engineered?", lit=(1962, 2007), part=PART)
        with self.voiceover("Chapter thirteen. Markets by design."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.search()
        self.matching()
        self.properties()
        self.kidneys()

    def search(self):
        d = load("gsp")
        head = label(r"Sponsored search: \ GSP against VCG", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert d["vcg_payments"] == [1.5, 0.7, 0.2] and d["gsp_truthful_payments"] == [2.4, 1.0, 0.2]
        assert (d["top_utility_slot1"], d["top_utility_slot2"]) == (0.6, 1.0)
        hd = [r"\text{slot}", r"\text{clicks}", r"\text{winner's value}", r"\text{GSP, truthful}", r"\text{VCG}"]
        cells = [[label(str(k + 1), font_size=19), label(f"{d['ctr'][k]:g}", font_size=19, color=GREY_A),
                  label(f"{d['values'][k]:g}", font_size=19, color=ROW),
                  label(f"{d['gsp_truthful_payments'][k]:g}", font_size=19, color=MONEY),
                  label(f"{d['vcg_payments'][k]:g}", font_size=19, color=INST)] for k in range(3)]
        grid = ValueGrid(hd, cells, col_w=[1.2, 1.6, 2.6, 2.6, 1.6], cell_h=0.55, font_size=17).move_to([-1.4, 0.8, 0])
        side = stack([(r"generalized second price: \ each winner pays the next bid per click", MONEY),
                      (r"VCG: \ each pays the harm her presence does to the others", INST),
                      (r"under GSP truth is not optimal: \ the top bidder earns 0.6 in slot 1, \ 1.0 by shading to "
                       r"slot 2", BAD),
                      (r"Edelman, \ Ostrovsky and Schwarz \ (2007): \ GSP's natural equilibrium raises exactly VCG's "
                       r"revenue, \ 2.4", GOAL)], font_size=18, buff=0.22).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Mechanism design runs the advertising behind web search. <bookmark mark='a'/>Three ad slots receive "
            "thirty, twenty and ten percent of clicks, and four advertisers value a click at ten, eight, five and "
            "two dollars. The industry's generalized second price auction charges each winner the next bid, per "
            "click. <bookmark mark='b'/>The Vickrey–Clarke–Groves mechanism instead charges each winner the harm her "
            "presence does to the others. <bookmark mark='c'/>Under the generalized auction, telling the truth is "
            "not optimal: the top bidder earns point six in the top slot but one dollar by bidding low enough to "
            "take the second. <bookmark mark='d'/>Benjamin Edelman, Michael Ostrovsky and Michael Schwarz showed "
            "in 2007 that its natural equilibrium raises exactly the revenue of the truthful mechanism, two dollars "
            "forty. Industry chose the simpler rule, and theory explained why it works."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("a")
            self.play(*[FadeIn(grid.cell[k][j]) for k in range(3) for j in range(4)], FadeIn(side[0]))
            vo.wait_until("b")
            self.play(*[FadeIn(grid.cell[k][4]) for k in range(3)], FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def matching(self):
        d = load("matching")
        head = label(r"Deferred acceptance \ (Gale and Shapley, \ 1962), \ run", font_size=30, color=CONN).to_edge(
            UP, buff=0.3)
        log = d["log"]
        assert len(log) == 11 and d["match"] == {"s2": "E", "s5": "A", "s3": "D", "s1": "B", "s4": "C"}
        S = sorted(d["students"])
        R = sorted(d["schools"])
        sp = {s: np.array([-4.6, 1.6 - 0.85 * k, 0]) for k, s in enumerate(S)}
        rp = {r: np.array([0.4, 1.6 - 0.85 * k, 0]) for k, r in enumerate(R)}
        sn = VGroup(*[VGroup(Circle(radius=0.3, color=ROW, fill_opacity=0.2), label(s, font_size=16, color=ROW)
                             ).move_to(sp[s]) for s in S])
        rn = VGroup(*[VGroup(Square(0.6, color=COL, fill_opacity=0.2), label(r, font_size=18, color=COL)
                             ).move_to(rp[r]) for r in R])
        prefs = VGroup(*[label(r"\ ".join(d["students"][s]), font_size=13, color=GREY_A).next_to(sp[s], LEFT,
                                                                                               buff=0.45)
                         for s in S])
        sprefs = VGroup(*[label(r"\ ".join(d["schools"][r]), font_size=13, color=GREY_A).next_to(rp[r], RIGHT,
                                                                                               buff=0.45)
                          for r in R])
        status = label(r"", font_size=17)
        status.move_to([4.4, -2.6, 0])
        held = {}
        with self.voiceover(
            "David Gale and Lloyd Shapley's algorithm of 1962 matches students to schools. <bookmark mark='a'/>Each "
            "student lists schools in order of preference, and each school ranks students. Here are five of each, "
            "with preferences the Reasoner drew at random. <bookmark mark='b'/>In each round, every unmatched "
            "student proposes to the best school that has not yet rejected her. Each school holds on to the best "
            "proposal it has received so far, and rejects the rest. A held student can still be displaced by a "
            "better one later: acceptance is deferred. <bookmark mark='c'/>Eleven proposals later, every student "
            "has a place."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sn), FadeIn(rn), FadeIn(prefs), FadeIn(sprefs))
            vo.wait_until("b")
            for s, r, outcome in log:
                ln = Line(sp[s] + RIGHT * 0.3, rp[r] + LEFT * 0.3, color=GREY_B, stroke_width=2)
                self.play(Create(ln), run_time=0.25)
                if outcome.startswith("held"):
                    if r in held:
                        self.play(FadeOut(held[r]), run_time=0.2)
                    keep = Line(sp[s] + RIGHT * 0.3, rp[r] + LEFT * 0.3, color=OK, stroke_width=4)
                    self.play(ReplacementTransform(ln, keep), run_time=0.25)
                    held[r] = keep
                else:
                    self.play(ln.animate.set_color(BAD), run_time=0.15)
                    self.play(FadeOut(ln), run_time=0.15)
            vo.wait_until("c")
            self.wait(0.5)
        self.clear_scene()

    def properties(self):
        d = load("matching")
        head = label(r"Stable, \ optimal, \ and safe to be honest", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        assert d["stable"] and d["n_stable"] == 4 and d["proposer_optimal"] and d["student_gains_by_lying"] == 0
        assert d["school_gain"] == {"school": "A", "truth": "s5", "lie_gets": "s3"}
        rk = d["student_ranks"]
        assert rk["s1"] == [2, 5]
        rows = [(r"stable", r"no student and school both prefer each other to their match: \ checked against every "
                            r"pair", OK),
                (r"student-optimal", r"of the 4 stable matchings, \ every student gets her best: \ s1 gets her 2nd "
                                     r"choice, \ against her 5th when schools propose", ROW),
                (r"strategy-proof for students", r"no student gains by misreporting: \ all 120 orderings tried, \ for "
                                                 r"each of the five: \ 0 gains", GOAL),
                (r"not for schools", r"school A, \ by misreporting, \ gets s3 instead of s5: \ no stable mechanism is "
                                     r"strategy-proof for both sides \ (Roth, \ 1982)", BAD)]
        g = rows_table(rows, top=1.6, gap=0.5, width=8.0, x_text=-1.6)
        with self.voiceover(
            "The Reasoner checks the theorems. <bookmark mark='a'/>The result is stable: no student and school both "
            "prefer each other to the partners they got. Gale and Shapley proved that deferred acceptance always "
            "finds such a matching. <bookmark mark='b'/>There are four stable matchings here, and this one is the "
            "best of them for every student: student one gets her second choice, against her fifth if the schools "
            "had proposed. <bookmark mark='c'/>No student can gain by lying about her preferences: the Reasoner tries "
            "all hundred and twenty orderings for each of the five, and none helps. <bookmark mark='d'/>But school A "
            "can gain by misreporting its ranking. Alvin Roth proved in 1982 that no stable mechanism is "
            "strategy-proof for both sides at once."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def kidneys(self):
        head = label(r"Markets without money", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"residents", r"the US National Resident Matching Program uses deferred acceptance, \ redesigned by "
                               r"Roth and Peranson \ (1999)", ROW),
                (r"schools", r"Boston and New York replaced manipulable assignment rules with deferred acceptance \ "
                             r"(2003--2005)", COL),
                (r"kidneys", r"a willing donor incompatible with her patient swaps with another such pair: \ cycles "
                             r"and chains of exchanges, \ found by integer programming", COOP),
                (r"repugnance", r"Roth \ (2007): \ some markets are blocked because people find them repugnant: \ "
                                r"selling kidneys, \ for instance", BAD),
                (r"the prize", r"Roth and Shapley, \ Nobel prize 2012: \ the theory of stable allocations and the "
                               r"practice of market design", HIST)]
        g = rows_table(rows, top=1.6, gap=0.42, width=8.4)
        with self.voiceover(
            "These ideas run real institutions. <bookmark mark='a'/>American medical graduates are matched to "
            "hospitals by deferred acceptance, redesigned by Alvin Roth and Elliott Peranson in 1999. "
            "<bookmark mark='b'/>Boston and New York replaced school assignment rules that rewarded strategic "
            "families with deferred acceptance in the early 2000s. <bookmark mark='c'/>And a patient with a willing "
            "but incompatible kidney donor can swap with another such pair, or join a chain of exchanges, found by "
            "integer programming over thousands of pairs. <bookmark mark='d'/>Roth also studied repugnance: some "
            "markets, like paying for kidneys, are blocked not by inefficiency but because people find them wrong. "
            "<bookmark mark='e'/>Roth and Shapley shared the Nobel prize in 2012. Designing institutions so that "
            "self-interest serves everyone is Hobbes's project, made into engineering."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
