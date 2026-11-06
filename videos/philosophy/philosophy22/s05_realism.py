from __future__ import annotations

import itertools

from videos.philosophy.philosophy22.common import *  # noqa: F403


class Realism(VoiceoverScene):
    def construct(self):
        card = chapter_card(4, r"Lewis's modal realism", r"Are other worlds as real as ours?", lit=(1973, 1986),
                            part=PART)
        with self.voiceover("Chapter four. Lewis's modal realism."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.thesis()
        self.indexical()
        self.paradise()
        self.stare()

    def thesis(self):
        hc = history_card(1986, r"David Lewis", r"\textit{On the Plurality of Worlds}", width=6.0,
                          color=HIST).to_corner(UL, buff=0.3)
        spots = [(-4.6, 0.3), (-1.4, 0.8), (1.8, 0.4), (4.9, 0.9), (-3.1, -1.4), (0.2, -1.2), (3.5, -1.5)]
        isl = VGroup(*[island(p, w=2.4, h=1.1, seed=80 + i, color=NAME if i == 5 else WORLD) for i, p in
                       enumerate(spots)])
        rows = stack([(r"each world is a concrete universe, \ as real as ours: \ stars, \ people, \ donkeys", WHITE),
                      (r"isolated: \ no spatiotemporal or causal relation runs between worlds", WORLD),
                      (r"plenitude: \ every way a world could be is a way some world is", CPT),
                      (r"recombination: \ any duplicates of possible things, \ patched together, \ make a possible "
                       r"world", ABS)], font_size=21, aligned_edge=LEFT, width=12.0).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Lewis's view is called modal realism. <bookmark mark='a'/>Other possible worlds exist, and they are "
            "things of the same kind as our world: concrete universes, with stars and people and, as he liked to say, "
            "talking donkeys. <bookmark mark='b'/>They are isolated: no spatial, temporal or causal relation connects "
            "one world to another. That is what makes them different worlds. <bookmark mark='c'/>There are enough "
            "of them: every way a world could be is a way some world is. <bookmark mark='d'/>And Lewis gave a "
            "principle of plenitude with teeth, recombination: duplicates of any possible things, patched together "
            "in any arrangement that fits in spacetime, make up a possible world. A dragon is possible because "
            "duplicates of possible parts, a reptile's body and a bird's wings, could be patched together."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(LaggedStart(*[DrawBorderThenFill(i) for i in isl], lag_ratio=0.12), FadeIn(rows[0]),
                      run_time=2.5)
            for mk, r in zip("bcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def indexical(self):
        head = label(r"`Actual' is like `here'", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        spots = [(-4.2, 0.6), (0.0, 1.0), (4.2, 0.6)]
        isl = VGroup(*[island(p, w=3.2, h=1.6, seed=90 + i, color=WORLD) for i, p in enumerate(spots)])
        folk = VGroup(*[person([p[0], p[1] - 0.1, 0], color=DESC, name=r"an inhabitant",
                               font_size=15) for p in spots])
        tag = label(r"`actual'", font_size=22, color=NAME)
        rows = stack([(r"`actual' picks out the world of the speaker, \ as `here' picks out the place of the "
                       r"speaker", WHITE),
                      (r"every world is actual to its inhabitants; \ none is actual absolutely", NAME),
                      (r"`necessarily $p$' \ $=$ \ $p$ at all worlds; \ `possibly $p$' \ $=$ \ $p$ at some: "
                       r"\ quantifiers, \ not new primitives", ABS),
                      (r"the reduction: \ modality becomes quantification over worlds and their parts", OK)],
                     font_size=21, aligned_edge=LEFT, width=12.0).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "What, then, makes our world the actual one? <bookmark mark='a'/>Nothing special about it, Lewis said. "
            "Actual is an indexical word, like here or now. Here picks out the place where the speaker is; actual "
            "picks out the world where the speaker is. <bookmark mark='b'/>Every world is actual to its own "
            "inhabitants, as every place is here to whoever is there. <bookmark mark='c'/>Then the modal words become "
            "quantifiers: necessarily p means p at all worlds, possibly p means p at some. <bookmark mark='d'/>That "
            "is the payoff Lewis wanted. Modality is not an unexplained primitive; it is quantification over worlds "
            "and the things in them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(isl), FadeIn(folk))
            vo.wait_until("a")
            tag.next_to(isl[0], UP, buff=0.1)
            self.play(FadeIn(tag), FadeIn(rows[0]))
            vo.wait_until("b")
            for k in (1, 2, 0):
                self.play(tag.animate.next_to(isl[k], UP, buff=0.1), run_time=0.9)
            self.play(FadeIn(rows[1]))
            for mk, r in zip("cd", rows[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def paradise(self):
        head = label(r"A paradise for philosophers", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        facts = ["rain", "wind", "cold"]
        W = list(itertools.product([1, 0], repeat=3))
        cells = VGroup()
        for i, w in enumerate(W):
            c = np.array([-5.95 + 1.75 * (i % 4), 1.2 - 1.75 * (i // 4), 0])
            I = island(c, w=1.5, h=1.3, seed=100 + i, color=WORLD)
            t = VGroup(*[label(f, font_size=17, color=WHITE if v else GREY_D) for f, v in zip(facts, w)]).arrange(
                DOWN, buff=0.04).move_to(c)
            cells.add(VGroup(I, t))
        rain = [i for i, w in enumerate(W) if w[0]]
        both = [i for i, w in enumerate(W) if w[0] and w[1]]
        hl_rain = VGroup(*[cells[i][0].shape.copy().set_stroke(NAME, 4).set_fill(NAME, 0.2) for i in rain])
        hl_both = VGroup(*[cells[i][0].shape.copy().set_stroke(DESC, 5).set_fill(DESC, 0.25) for i in both])
        rows = stack([(r"a proposition is a set of worlds: \ `it rains' \ $=$ \ the 4 worlds where it rains", NAME),
                      (r"`rain and wind' is a subset: \ entailment is inclusion", DESC),
                      (r"a belief state: \ the worlds compatible with what one believes \ (Part 12)", WORLD),
                      (r"a property: \ the set of its possible instances, \ in all worlds", CPT),
                      (r"counterfactuals: \ truth at the closest worlds \ (Lewis, \ 1973; \ Part 17)", ABS),
                      (r"`a philosophers' paradise' \ (Lewis, \ 1986, \ \S 1.1), \ as sets are for "
                       r"mathematicians", GOAL)],
                     font_size=20, aligned_edge=LEFT, width=5.6).move_to([3.9, -0.3, 0])
        with self.voiceover(
            "Why believe it? Lewis's argument was from utility. <bookmark mark='a'/>Take eight worlds, differing in "
            "whether it rains, whether it is windy, whether it is cold. A proposition can be identified with the set "
            "of worlds where it is true: it rains is these four. <bookmark mark='b'/>Rain and wind is a smaller set, "
            "inside the first; one proposition entails another when its set is included in the other's. "
            "<bookmark mark='c'/>The content of a belief state is the set of worlds compatible with what one "
            "believes, the picture that Part 12 used for knowledge. <bookmark mark='d'/>A property is the set of its "
            "instances, actual and merely possible. <bookmark mark='e'/>Counterfactuals are true when their "
            "consequent holds at the closest worlds where their antecedent does. <bookmark mark='f'/>Worlds, Lewis "
            "said, are a paradise for philosophers, as set theory is a paradise for mathematicians: a single "
            "ontology in which many notions can be built. The price is believing in the worlds."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.08))
            vo.wait_until("a")
            self.play(FadeIn(hl_rain), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(hl_both), FadeIn(rows[1]))
            for mk, r in zip("cdef", rows[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def stare(self):
        head = label(r"The incredulous stare, \ and other objections", font_size=30, color=CONN).to_edge(UP,
                                                                                                    buff=0.35)
        rows = [
            (r"the stare", r"a stare is not an argument, \ and no argument refutes it; \ Lewis counted the cost "
                           r"in common opinion, \ worth paying", GREY_A),
            (r"knowledge", r"isolated worlds cannot cause our beliefs: \ Lewis replied that modal knowledge is like "
                           r"mathematical knowledge", WORLD),
            (r"ethics", r"if every possibility is realized, \ why prevent suffering here? \ Lewis: \ we rightly "
                        r"care about our own world", BAD),
            (r"plenitude", r"Forrest and Armstrong \ (1984): \ unrestricted recombination yields a world larger than "
                           r"any world", DESC),
            (r"Humphrey", r"Kripke: \ Humphrey does not care whether someone else wins in another world: \ the next "
                          r"chapter", NAME),
        ]
        g = rows_table(rows, top=1.9, gap=0.42, width=8.8, x_text=-2.6, label_size=21)
        with self.voiceover(
            "Most philosophers do not believe it. <bookmark mark='a'/>Lewis described their main response as the "
            "incredulous stare, and admitted he could not refute a stare. He counted the view's cost as a conflict "
            "with common opinion, and judged it worth paying. <bookmark mark='b'/>There are arguments too. If other "
            "worlds are causally isolated from us, how can we know anything about them? Lewis answered that modal "
            "knowledge is like mathematical knowledge: it needs no causal contact. <bookmark mark='c'/>And "
            "there is an ethical worry, which Lewis took up at length: if every possibility is realized somewhere, "
            "preventing suffering here seems only to shift it around logical space. Lewis replied that we rightly "
            "care about our own world and its inhabitants. "
            "<bookmark mark='d'/>Peter Forrest and David Armstrong argued that unrestricted recombination is "
            "inconsistent: patch together duplicates of every world and you get a world bigger than any world. Lewis "
            "added a size restriction. <bookmark mark='e'/>And Kripke had an objection about Humphrey, which needs "
            "the next chapter."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
