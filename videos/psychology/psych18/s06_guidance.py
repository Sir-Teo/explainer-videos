from __future__ import annotations

from videos.psychology.psych18.common import *  # noqa: F403


class Guidance(VoiceoverScene):
    def construct(self):
        self.card()
        self.fit()
        self.guided()
        self.saliency()
        self.history()
        self.unguided()

    def card(self):
        card = chapter_card(5, r"Features, \ binding and guidance", r"What does attention add to a feature?",
                            lit={1980: r"Treisman \& Gelade", 1989: r"Wolfe", 1998: r"Itti \& Koch", 2011: r"Anderson et al."}, part=PART,
                            scale=("mind", "brain"), marr=("what", "how"))
        with self.voiceover("Chapter five. Features, binding and guidance."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def fit(self):
        head = heading(r"Feature integration theory")
        maps = VGroup()
        for k, (name, col) in enumerate([(r"red", TARGET), (r"green", DIST), (r"vertical", GREY_B),
                                         (r"horizontal", GREY_B)]):
            sq = Square(1.3, color=col, stroke_width=2.5, fill_color="#0b0e13", fill_opacity=1)
            maps.add(VGroup(sq, label(name, font_size=19, color=col).next_to(sq, DOWN, buff=0.08)))
        maps.arrange(RIGHT, buff=0.35).move_to([-2.6, 1.7, 0])
        master = Rectangle(width=3.2, height=1.3, color=ATT, stroke_width=3).move_to([3.4, 1.7, 0])
        ml = label(r"a map of locations", font_size=19, color=ATT).next_to(master, DOWN, buff=0.08)
        spot = Circle(0.32, color=ATT, fill_color=ATT, fill_opacity=0.35).move_to(master.get_center() + LEFT * 0.6)
        link = Arrow(maps.get_right(), master.get_left(), buff=0.1, color=GREY_B, stroke_width=3)
        rows = rows_of([
            (r"each feature is registered in its own map, \ in parallel, \ for the whole field", WHITE),
            (r"a lone feature is visible as activity in one map: \ pop-out", TARGET),
            (r"which features go together is not in any map: \ binding needs attention at the location", ATT),
            (r"so a conjunction is found by visiting items one at a time with a spotlight", CUE),
            (r"illusory conjunctions: \ a brief, \ unattended red X and green O can be seen as a green X", CONFLICT),
        ], 12.4, 24, 0.2).to_edge(DOWN, buff=0.75)
        tag = historical_tag(archive.TREISMAN_GELADE_1980.cite)
        with self.voiceover(
            "Treisman's explanation was feature integration theory. <bookmark mark='a'/> Early vision registers each "
            "feature in its own map: a map of where there is red, a map of where there is green, a map for vertical, a "
            "map for horizontal, all at once, across the whole field. <bookmark mark='b'/> A lone red item is a single "
            "spot of activity in the red map, so it is visible without searching. That is pop-out. "
            "<bookmark mark='c'/> But the maps don't say which features belong together. Red at some place and "
            "vertical at some place don't make a red vertical thing until attention, a spotlight on a map of "
            "locations, binds the features found there. <bookmark mark='d'/> So a conjunction must be found by "
            "visiting items one at a time. <bookmark mark='e'/> A striking prediction followed. Flash a red X and a "
            "green O briefly, with attention busy elsewhere, and people sometimes report a green X: features "
            "recombined without the glue. Treisman and Hilary Schmidt called them illusory conjunctions."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m) for m in maps], lag_ratio=0.3), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(GrowArrow(link), FadeIn(master), FadeIn(ml), FadeIn(spot), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(spot.animate.shift(RIGHT * 1.2), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def guided(self):
        d = load("search")
        head = heading(r"Guided search: \ features steer the spotlight")
        rows = rows_of([
            (r"many conjunction searches are faster than one item at a time allows", WHITE),
            (r"Wolfe: \ the feature maps also send the spotlight where red, \ or vertical, \ is", ATT),
            (r"each item gets a priority: \ how many target features it has, \ plus how much it stands out, \ "
             r"plus noise", CONTROL),
            (r"items are checked in order of priority, \ and the search quits below a threshold", CUE),
            (r"a partly guided search: \ shallow slopes; \ errors are misses, \ when the target's priority falls short",
             MODEL),
        ], 6.4, 24, 0.36).to_edge(LEFT, buff=0.55).shift(DOWN * 0.05)
        eq = MathTex(r"\text{priority} = \text{match} + w \cdot \text{saliency} + \text{noise}", font_size=34,
                     color=CONTROL).move_to([3.5, 2.2, 0])
        A = axes([0, 34], [400, 1800], x_length=4.6, y_length=2.9, xticks=[4, 8, 16, 32], yticks=[500, 1100, 1700],
                 xlabel=r"items", ylabel=r"RT, \ ms", center=[3.6, -0.3, 0], font_size=17)
        ax = A.ax
        ss = d["set_sizes"]
        cs = VGroup()
        for kind, col in (("feature", TARGET), ("conjunction", ATT)):
            cs.add(VGroup(curve(ax, ss, d[f"{kind}_present"], col, 4),
                          DashedVMobject(curve(ax, ss, d[f"{kind}_absent"], col, 3), num_dashes=24)))
        miss = d["conjunction_miss"]
        note = label(rf"Psyche's conjunction misses: \ {pct(miss.mean())} \ (people: \ a few percent)",
                     font_size=18, color=MODEL).next_to(A, DOWN, buff=0.15)
        ptag = psyche_tag(r"\texttt{attention.guided\_search}: \ 50 ms a check, \ quitting 1.5 s.d. below the target")
        tag = historical_tag(archive.WOLFE_2021.cite)
        with self.voiceover(
            "Feature integration theory had a problem of its own. <bookmark mark='a'/> Through the 1980s, many "
            "conjunction searches turned out to be much faster than one item at a time would allow. "
            "<bookmark mark='b'/> Jeremy Wolfe's guided search, from 1989, kept the maps and the binding spotlight, "
            "but let the maps steer it. If you're looking for red verticals, the red map and the vertical map both "
            "push the spotlight toward their items. <bookmark mark='c'/> Each item gets a priority: one point for "
            "each feature it shares with the target, plus a bonus for standing out from its neighbours, plus noise. "
            "<bookmark mark='d'/> The spotlight visits items in order of priority, and the search gives up when the "
            "next item's priority is too low to be worth checking. <bookmark mark='e'/> Run that on Psyche and a "
            "feature search is flat, because the target always comes first; a conjunction search climbs, but more "
            "gently than one at a time, because the target is usually near the front of the queue. And the errors "
            "come out right: misses, on trials where noise pushed the target below the quitting threshold."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
                if m == "c":
                    self.play(Write(eq))
                if m == "e":
                    self.play(Create(cs[0]), Create(cs[1]), FadeIn(ptag), run_time=1.5)
                    self.play(FadeIn(note))
        self.clear_scene()

    def saliency(self):
        d = load("saliency")
        head = heading(r"A saliency map you can compute")
        sal = d["sal"]
        h, w = d["shape"]
        img = picture(sal, height=3.0, lo=0.0, hi=1.0)
        img.move_to([3.3, 0.9, 0])
        scene = VGroup()
        ox, oy, sc = -6.2, 2.4, 3.0 / h
        for r, c, colour, orient in d["bars"]:
            p = np.array([ox + c * sc, oy - r * sc, 0])
            wid, hei = (0.06, 0.24) if orient == 0 else (0.24, 0.06)
            scene.add(Rectangle(width=wid, height=hei, stroke_width=0, fill_color=TARGET if colour else DIST,
                                fill_opacity=1).move_to(p))
        frame = SurroundingRectangle(scene, color=GREY_D, buff=0.15, stroke_width=2)
        fl = label(r"a field of bars", font_size=19, color=GREY_B).next_to(frame, DOWN, buff=0.1)
        il = label(r"its saliency map", font_size=19, color=GREY_B).next_to(img, DOWN, buff=0.1)
        fix = VGroup()
        for k, (r, c) in enumerate(d["path"][:3]):
            p = np.array([ox + c * sc, oy - r * sc, 0])
            fix.add(VGroup(Circle(0.22, color=ATT, stroke_width=4).move_to(p),
                           label(str(k + 1), font_size=18, color=ATT).move_to(p + UP * 0.34 + RIGHT * 0.25)))
        rows = rows_of([
            (r"Itti and Koch, \ 1998: \ for each feature, \ the centre minus its surround, \ everywhere at once", WHITE),
            (r"maps with one strong peak count more; \ sum them: \ how much each place stands out", CONTROL),
            (r"winner-take-all picks the peak; \ inhibition of return suppresses it; \ the next peak wins", ATT),
            (r"the first two fixations: \ the horizontal bar, \ then the red one; \ the third lands beside the first",
             MODEL),
        ], 12.4, 23, 0.18).to_edge(DOWN, buff=0.75)
        ptag = psyche_tag(r"\texttt{attention.saliency\_map}, \ \texttt{attention.scan\_path}")
        tag = historical_tag(archive.ITTI_KOCH_1998.cite)
        with self.voiceover(
            "The bottom-up part of the priority can be computed from an image. <bookmark mark='a'/> In 1998 Laurent "
            "Itti, Christof Koch and Ernst Niebur turned feature contrast into a saliency map. For each feature, "
            "colour, orientation, brightness, take the difference between each point and its surround, everywhere at "
            "once, the way centre-surround cells do. <bookmark mark='b'/> A feature map with one strong peak is "
            "informative, so it's weighted up; a map with peaks everywhere is weighted down. Add them, and you have "
            "a map of how much each place stands out. <bookmark mark='c'/> A winner-take-all network picks the peak, "
            "inhibition of return suppresses it, and the next peak wins: a predicted sequence of fixations. "
            "<bookmark mark='d'/> On this field of green verticals, Psyche's map picks the odd horizontal bar first "
            "and the red bar second; the third lands just beside the first, where its contrast spills over. Saliency "
            "models "
            "like this predict where people look in free viewing reasonably well, and badly when they have a task."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(scene), FadeIn(frame), FadeIn(fl))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(img), FadeIn(il), FadeIn(rows[1]), FadeIn(ptag))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(LaggedStart(*[Create(f) for f in fix], lag_ratio=0.6), FadeIn(rows[3]), run_time=2.0)
        self.clear_scene()

    def history(self):
        head = heading(r"A third source of priority: \ history")
        pm = RoundedRectangle(width=3.0, height=1.0, corner_radius=0.15, stroke_color=ATT, stroke_width=3)
        pm_l = label(r"the priority map", font_size=24, color=ATT).move_to(pm)
        pmap = VGroup(pm, pm_l).move_to([3.2, 1.5, 0])
        srcs = VGroup()
        for k, (txt, col) in enumerate([(r"goals: \ what you look for", CUE), (r"salience: \ what stands out", TARGET),
                                        (r"history: \ what paid, \ what never mattered", CONTROL)]):
            r = RoundedRectangle(width=3.4, height=0.75, corner_radius=0.12, stroke_color=col, stroke_width=2.5)
            srcs.add(VGroup(r, wrapped_label(txt, 3.1, 20, col).move_to(r)))
        srcs.arrange(DOWN, buff=0.3).move_to([-2.4, 1.5, 0])
        arrows = VGroup(*[Arrow(sr.get_right(), pmap.get_left(), buff=0.1, color=sr[0].get_stroke_color(),
                                stroke_width=3) for sr in srcs])
        rows = rows_of([
            (r"latent inhibition, \ Part 16: \ a cue seen often without consequence is later learned slowly", CONTROL),
            (r"Mackintosh, \ and Pearce and Hall: \ attention to a cue is itself learned from its history", GREY_A),
            (r"2011: \ Anderson, \ Laurent and Yantis: \ a colour once paired with reward captures attention later, "
             r"\ when it is irrelevant", ATT),
            (r"Awh and colleagues, \ 2012: \ goals against salience is a false dichotomy; \ history is a third source",
             CUE),
        ], 12.4, 24, 0.22).to_edge(DOWN, buff=0.75)
        tag = published_tag(archive.ANDERSON_2011.cite)
        with self.voiceover(
            "Goals and salience are not the whole of it. <bookmark mark='a'/> Part 16 met latent inhibition: a "
            "stimulus that has appeared many times without consequence is later learned about slowly, as if it had "
            "stopped being attended. <bookmark mark='b'/> Mackintosh, and Pearce and Hall, wrote models in which "
            "attention to a cue is learned from its history, toward cues that predict or toward cues that surprise. "
            "<bookmark mark='c'/> In 2011 Brian Anderson, Patryk Laurent and Steven Yantis showed the same in "
            "search. People first earned money for finding red or green targets. Later, in a task where colour was "
            "irrelevant, an item in the previously rewarded colour slowed them down: it captured attention because "
            "of what it had once been worth. <bookmark mark='d'/> In 2012 Edward Awh, Artem Belopolsky and Jan "
            "Theeuwes argued that the old split between goals and salience had failed, and that selection history is "
            "a third source of priority, as strong as the other two."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(pmap), FadeIn(srcs[0]), FadeIn(srcs[1]), GrowArrow(arrows[0]),
                      GrowArrow(arrows[1]))
            vo.wait_until("a")
            self.play(FadeIn(srcs[2]), GrowArrow(arrows[2]), FadeIn(rows[0]))
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def unguided(self):
        d = load("search")
        head = heading(r"When nothing can guide: \ a T among Ls")
        box = Square(3.6, color=GREY_D, stroke_width=2).move_to([-3.8, 0.7, 0])
        disp = search_glyphs(d["spatial_display"], box.get_center(), 3.3, letters=True)
        A = axes([0, 34], [400, 2100], x_length=4.8, y_length=3.0, xticks=[4, 8, 16, 32], yticks=[500, 1300, 2100],
                 xlabel=r"items", ylabel=r"RT, \ ms", center=[3.2, 0.7, 0], font_size=17)
        ax = A.ax
        ss = d["set_sizes"]
        cp = curve(ax, ss, d["spatial_present"], WHITE, 4)
        ca = DashedVMobject(curve(ax, ss, d["spatial_absent"], WHITE, 3), num_dashes=24)
        sl = d["spatial_slopes"]
        note = label(rf"slopes {sl[0]:.0f} and {sl[1]:.0f} ms an item: \ {sl[1] / sl[0]:.1f} to 1", font_size=19,
                     color=MODEL).next_to(A, DOWN, buff=0.15)
        rows = rows_of([
            (r"a T and an L share every feature: \ two lines, \ one colour, \ any orientation", WHITE),
            (r"no map can steer: \ items are checked in random order, \ one at a time", GREY_A),
            (r"present: \ found halfway on average; \ absent: \ everything checked; \ two to one", ATT),
        ], 12.4, 24, 0.2).to_edge(DOWN, buff=0.75)
        ptag = psyche_tag(r"\texttt{attention.search\_slopes('spatial')}")
        with self.voiceover(
            "Take guidance away and the old pattern returns in full. <bookmark mark='a'/> A T and an L are made of "
            "the same two lines, in the same colour, and rotated at random they share every orientation too. "
            "<bookmark mark='b'/> No feature map can tell the spotlight where to go, so items are checked in effect "
            "at random, one at a time. <bookmark mark='c'/> When the T is there, it's found halfway through on "
            "average; when it isn't, everything must be checked. The absent slope is about twice the present one. "
            "Search is a continuum, from fully guided to not guided at all, and the slope measures where on it a task "
            "sits."
        ) as vo:
            self.play(FadeIn(head), FadeIn(box), FadeIn(disp), FadeIn(A), FadeIn(ptag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(cp), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), Create(ca), FadeIn(note), run_time=1.5)
        self.clear_scene()
