from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai2.common import FAIL, FCOL, GCOST, HEUR, HIST, LEARN, MONO, PART, PATH, SYMBOL, load, node_box


class Knowledge(VoiceoverScene):
    def construct(self):
        self.card()
        self.nets()
        self.rules()
        self.certainty()
        self.bottleneck()
        self.graphs()

    def card(self):
        card = chapter_card(11, r"Knowledge is power", r"What if intelligence is mostly knowing things?", lit=(1980,),
                            part=PART)
        with self.voiceover("Chapter eleven. Knowledge is power."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def nets(self):
        pos = {"animal": [-2.6, 2.2], "bird": [-4.4, 0.4], "fish": [-0.8, 0.4], "canary": [-5.4, -1.6],
               "penguin": [-3.4, -1.6]}
        nodes = {k: node_box(k, SYMBOL, font_size=24).move_to([*v, 0]) for k, v in pos.items()}
        isa = VGroup()
        for a, b in (("bird", "animal"), ("fish", "animal"), ("canary", "bird"), ("penguin", "bird")):
            isa.add(Arrow(nodes[a].get_top(), nodes[b].get_bottom(), buff=0.08, color=GREY_B, stroke_width=2.5))
        isal = label(r"is-a", font_size=18, color=GREY_B).next_to(isa[0], LEFT, buff=0.05)
        props = VGroup(
            label(r"breathes", font_size=20, color=HEUR).next_to(nodes["animal"], RIGHT, buff=0.3),
            label(r"has wings, \ flies", font_size=20, color=HEUR).next_to(nodes["bird"], LEFT, buff=0.15).shift(UP * 0.5),
            label(r"yellow, \ sings", font_size=20, color=HEUR).next_to(nodes["canary"], DOWN, buff=0.2),
            label(r"does \textit{not} fly", font_size=20, color=FAIL).next_to(nodes["penguin"], DOWN, buff=0.2),
        )
        q = label(r"Does a canary breathe? \ follow is-a links up: \ yes", font_size=22, color=PATH)
        q.move_to([-3.4, -3.0, 0])
        frame = VGroup(
            Text("frame: bird", font=MONO, font_size=26, color=FCOL),
            Text("  is-a:       animal", font=MONO, font_size=22),
            Text("  legs:       2", font=MONO, font_size=22),
            Text("  covering:   feathers", font=MONO, font_size=22),
            Text("  locomotion: flies   (default)", font=MONO, font_size=22),
        ).arrange(DOWN, buff=0.12, aligned_edge=LEFT).move_to([3.6, 1.2, 0])
        fbox = SurroundingRectangle(frame, color=FCOL, buff=0.25, corner_radius=0.1)
        hcs = VGroup(history_card(1968, r"Ross Quillian", r"semantic networks", width=3.2, color=HIST, font_size=18),
                     history_card(1974, r"Marvin Minsky", r"frames, \ with default slots", width=3.2, color=HIST,
                                  font_size=18)).arrange(RIGHT, buff=0.2).move_to([3.6, -1.6, 0])
        tag = note(r"illustrative").to_corner(DR, buff=0.2)
        with self.voiceover(
            "Search and logic need something to reason about. <bookmark mark='a'/> Ross Quillian's semantic networks, from "
            "1968, store concepts as nodes and relations as links: a canary is a bird, a bird is an animal. "
            "<bookmark mark='b'/> Properties are stored once and inherited: does a canary breathe? Follow the is-a links up to "
            "animal. <bookmark mark='c'/> Exceptions sit lower down: a penguin is a bird that does not fly. "
            "<bookmark mark='d'/> Marvin Minsky's frames, in 1974, bundled a concept's slots with default values. These ideas "
            "live on as the objects and classes of programming languages."
        ) as vo:
            self.play(*[FadeIn(n) for n in nodes.values()], LaggedStart(*[GrowArrow(a) for a in isa], lag_ratio=0.2),
                      FadeIn(isal), FadeIn(tag))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p) for p in props[:3]], lag_ratio=0.2))
            self.play(FadeIn(q))
            vo.wait_until("c")
            self.play(FadeIn(props[3]))
            vo.wait_until("d")
            self.play(Create(fbox), FadeIn(frame), FadeIn(hcs))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rules(self):
        d = load("rules")
        rules = {r[0]: r for r in d["rules"]}
        fired = d["fired"]
        facts = d["facts"]
        fbox = VGroup(label(r"facts", font_size=24, color=GCOST),
                      *[label(f, font_size=20, color=WHITE) for f in facts]).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        fbox.move_to([-5.2, 0.6, 0])
        rule_m = VGroup()
        for name in fired:
            _, ifs, then = rules[name]
            rule_m.add(label(rf"{name}: \ if {' and '.join(ifs)} \ then \textbf{{{then}}}", font_size=20,
                             color=FCOL))
        rule_m.arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([1.4, 0.9, 0])
        if rule_m.width > 8.4:
            rule_m.width = 8.4
            rule_m.set_x(1.6)
        derived = VGroup(*[node_box(t, PATH, font_size=22) for t in d["derived"]]).arrange(RIGHT, buff=0.6)
        derived.move_to([1.4, -1.4, 0])
        arrows = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.1, color=PATH, stroke_width=3)
                          for a, b in zip(derived, derived[1:])])
        unused = label(rf"${len(d['rules']) - len(fired)}$ of the ${len(d['rules'])}$ rules never fire: \ their "
                       r"conditions never hold", font_size=20, color=GREY_B).next_to(derived, DOWN, buff=0.4)
        hc = history_card(1965, r"Feigenbaum, Buchanan, Lederberg: \ DENDRAL", r"rules of a chemist's expertise "
                          r"identify molecules from mass spectra", width=5.2, color=HIST, font_size=18)
        hc.to_corner(UL, buff=0.25).shift(RIGHT * 6.0)
        if hc.get_right()[0] > 6.95:
            hc.shift(LEFT * (hc.get_right()[0] - 6.95))
        tag = note(r"computed: \ forward chaining over an illustrative rule base").to_corner(DR, buff=0.2)
        es = VGroup(node_box(r"human experts", HIST, font_size=28), node_box(r"if--then rules", FCOL, font_size=28),
                    node_box(r"a program that chains them", PATH, font_size=28)).arrange(RIGHT, buff=0.9).move_to(UP * 0.4)
        es.add(*[Arrow(es[k].get_right(), es[k + 1].get_left(), buff=0.1, color=GREY_B) for k in range(2)])
        es.add(label(r"an expert system", font_size=30, color=GREY_A).next_to(es, UP, buff=0.5))
        with self.voiceover(
            "In the seventies a new kind of program captured the field: the expert system, its knowledge a set of if-then "
            "rules written with human experts. <bookmark mark='a'/> Give it facts about an animal. <bookmark mark='b'/> Forward "
            "chaining fires every rule whose conditions hold, adds the conclusion, and repeats: hair makes a mammal; a mammal "
            "with pointed teeth and claws, a carnivore; a tawny carnivore with dark spots, a cheetah. <bookmark mark='c'/> The "
            "first great one was DENDRAL, begun at Stanford in 1965 by Edward Feigenbaum, Bruce Buchanan and Joshua Lederberg, "
            "which inferred molecular structure from mass spectra. Feigenbaum's lesson: a program's power comes from what it "
            "knows, more than from how cleverly it reasons."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(es[5]), LaggedStart(*[FadeIn(es[k]) for k in (0, 3, 1, 4, 2)], lag_ratio=0.4),
                      run_time=3.0)
            vo.wait_until("a")
            self.play(FadeOut(es), run_time=0.5)
            self.play(FadeIn(fbox))
            vo.wait_until("b")
            for k in range(len(fired)):
                self.play(FadeIn(rule_m[k], shift=RIGHT * 0.1), FadeIn(derived[k]),
                          *([GrowArrow(arrows[k - 1])] if k else []), run_time=1.0)
            self.play(FadeIn(unused))
            vo.wait_until("c")
            self.play(FadeIn(hc, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def certainty(self):
        d = load("rules")
        cf, comb = d["cf"], d["cf_combined"]
        rule = VGroup(
            Text("RULE: if the stain of the organism is gram-negative,", font=MONO, font_size=20),
            Text("      and its shape is rod, and the patient is a", font=MONO, font_size=20),
            Text("      compromised host, then it is pseudomonas (0.6)", font=MONO, font_size=20),
        ).arrange(DOWN, buff=0.08, aligned_edge=LEFT).to_edge(UP, buff=0.5)
        rtag = note(r"in the style of MYCIN's rules \ (illustrative)").next_to(rule, DOWN, buff=0.1)
        f = cmath(r"\mathrm{CF}", r"=", r"\mathrm{CF}_1 + \mathrm{CF}_2\,(1 - \mathrm{CF}_1)", font_size=40)
        f.move_to([-3.4, 0.6, 0])
        fl = label(r"two rules support the same conclusion", font_size=22, color=GREY_A).next_to(f, DOWN, buff=0.15)
        steps = VGroup(MathTex(rf"{cf[0]}", font_size=34, color=FCOL),
                       MathTex(rf"\to\ {cf[0]} + {cf[1]}\,(1 - {cf[0]}) = {comb[1]:.2f}", font_size=34, color=FCOL),
                       MathTex(rf"\to\ {comb[1]:.2f} + {cf[2]}\,(1 - {comb[1]:.2f}) = {comb[2]:.2f}", font_size=34,
                               color=FCOL)).arrange(DOWN, buff=0.15, aligned_edge=LEFT).move_to([-3.4, -1.4, 0])
        res = VGroup(
            history_card(1979, r"Yu et al., \textit{JAMA}: \ MYCIN, blinded", r"expert acceptability rating: "
                         r"$65\%$; \ Stanford's specialists: $42.5$--$62.5\%$",
                         width=5.8, color=HIST, font_size=19),
            history_card(1980, r"McDermott: \ R1, \ later XCON, \ at Digital", r"configured customers' VAX computer "
                         r"orders; \ grew to thousands of rules, \ saving the company millions a year", width=5.8,
                         color=HIST, font_size=19),
        ).arrange(DOWN, buff=0.3).move_to([3.5, -0.9, 0])
        never = label(r"MYCIN was never used to treat patients", font_size=20, color=FAIL).next_to(res, DOWN, buff=0.15)
        with self.voiceover(
            "Medicine was the showcase. MYCIN, built at Stanford by Edward Shortliffe in the mid-seventies, recommended "
            "antibiotics for blood infections and meningitis from a few hundred rules like this one. <bookmark mark='a'/> Each "
            "rule carried a certainty factor; when rules agreed, new evidence closed part of the remaining gap. "
            f"<bookmark mark='b'/> Point six and point five make {comb[1]:.2f}; another rule at point four, {comb[2]:.2f}. "
            "<bookmark mark='c'/> In a blinded test published in 1979, eight experts rated antibiotic choices for ten "
            "meningitis cases. MYCIN received an acceptability rating of sixty-five percent, a rate none of the Stanford "
            "specialists it was compared with beat. It "
            "was never used on patients. <bookmark mark='d'/> The commercial breakthrough was R1, later XCON, written by John "
            "McDermott for Digital Equipment in 1980 to configure computer orders. By the mid-eighties, expert systems were an "
            "industry."
        ) as vo:
            self.play(FadeIn(rule), FadeIn(rtag))
            vo.wait_until("a")
            self.play(Write(f), FadeIn(fl))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s_) for s_ in steps], lag_ratio=0.5))
            vo.wait_until("c")
            self.play(FadeIn(res[0], shift=UP * 0.2), FadeIn(never))
            vo.wait_until("d")
            self.play(FadeIn(res[1], shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bottleneck(self):
        pipe = VGroup(node_box(r"an expert", HIST, font_size=26), node_box(r"a knowledge engineer", FCOL, font_size=26),
                      node_box(r"rules", SYMBOL, font_size=26)).arrange(RIGHT, buff=1.0).move_to(UP * 2.0)
        arrows = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.1, color=GREY_B) for a, b in zip(pipe, pipe[1:])])
        slow = label(r"interviews, \ months per domain, \ rules that conflict as they multiply", font_size=22,
                     color=FAIL).next_to(pipe, DOWN, buff=0.3)
        cyc = history_card(1984, r"Douglas Lenat: \ Cyc", r"hand-code common sense itself: \ millions of assertions "
                           r"over four decades, \ a project still running after Lenat's death in 2023", width=6.2,
                           color=HIST, font_size=20).move_to([-3.2, -1.2, 0])
        brittle = VGroup(label(r"brittle at the edges:", font_size=24, color=FAIL),
                         label(r"outside its rules, \ an expert system \\ doesn't degrade gracefully; \ it fails",
                               font_size=22, color=GREY_A)).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        brittle.move_to([3.4, -1.2, 0])
        with self.voiceover(
            "The weak point was getting the knowledge in. <bookmark mark='a'/> An expert talks; a knowledge engineer writes "
            "rules; the rules fail and are patched, for months per domain, and as they multiply they interact in ways nobody "
            "intended: the knowledge acquisition bottleneck. <bookmark mark='b'/> And the systems were brittle: faced with a case "
            "no rule covers, a human expert does something sensible; a rule base does nothing, or something absurd. "
            "<bookmark mark='c'/> Douglas Lenat drew the boldest conclusion: write down common sense itself. His Cyc project, "
            "started in 1984, has entered millions of assertions by hand, and still runs."
        ) as vo:
            self.play(FadeIn(pipe[0]))
            vo.wait_until("a")
            self.play(GrowArrow(arrows[0]), FadeIn(pipe[1]), GrowArrow(arrows[1]), FadeIn(pipe[2]))
            self.play(FadeIn(slow))
            vo.wait_until("b")
            self.play(FadeIn(brittle))
            vo.wait_until("c")
            self.play(FadeIn(cyc, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def graphs(self):
        ents = {"Ada Lovelace": [-4.2, 1.2], "Lord Byron": [-1.0, 2.4], "London": [-4.6, -1.4],
                "Analytical Engine": [0.0, -0.4], "Charles Babbage": [3.4, 0.8]}
        nodes = {k: node_box(k, GCOST, font_size=22).move_to([*v, 0]) for k, v in ents.items()}
        rels = [("Ada Lovelace", "Lord Byron", "child of"), ("Ada Lovelace", "London", "born in"),
                ("Ada Lovelace", "Analytical Engine", "wrote about"), ("Charles Babbage", "Analytical Engine", "designed")]
        edges = VGroup()
        for a, b, r in rels:
            e = Arrow(nodes[a].get_center(), nodes[b].get_center(), buff=0.55, color=GREY_B, stroke_width=2.5)
            edges.add(VGroup(e, label(r, font_size=18, color=HEUR).move_to(e.get_center() + UP * 0.22)))
        hc = history_card(2012, r"Google: \ the Knowledge Graph", r"``things, not strings'': \ over $500$ million "
                          r"objects and $3.5$ billion facts at launch", width=5.6, color=HIST,
                          font_size=19).to_corner(DR, buff=0.3)
        now = label(r"today: \ knowledge graphs answer factual questions in search engines", font_size=22,
                    color=PATH).to_corner(DL, buff=0.3)
        if now.get_right()[0] > hc.get_left()[0] - 0.25:
            now.width = hc.get_left()[0] - 0.25 + 6.8
            now.to_corner(DL, buff=0.3)
        tag = note(r"illustrative").to_corner(UR, buff=0.25)
        with self.voiceover(
            "Knowledge as a web of entities and relations did not die; it scaled. <bookmark mark='a'/> In 2012 Google "
            "introduced its Knowledge Graph, things, not strings: over five hundred million objects and three and a half billion "
            "facts at launch, harvested from sources like Wikipedia rather than typed in. <bookmark mark='b'/> Knowledge graphs "
            "answer factual questions in search engines today. What changed was not the representation, but where the knowledge "
            "comes from."
        ) as vo:
            self.play(*[FadeIn(n) for n in nodes.values()], LaggedStart(*[FadeIn(e) for e in edges], lag_ratio=0.2),
                      FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(now))
        self.wait(0.3)
        self.clear_scene()
