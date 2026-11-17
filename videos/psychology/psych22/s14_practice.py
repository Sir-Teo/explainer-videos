from __future__ import annotations

from videos.psychology.psych22.common import *  # noqa: F403

FOOD_GROUP = {"apple": CAT_A, "banana": CAT_A, "cherry": CAT_A, "carrot": MODEL, "potato": MODEL, "onion": MODEL,
              "milk": CAT_B, "cheese": CAT_B, "yoghurt": CAT_B, "bread": PROTO, "pasta": EXEMPLAR, "rice": EXEMPLAR}


class Practice(VoiceoverScene):
    def construct(self):
        self.card()
        self.diagnosis()
        self.sorting()
        self.machines()

    def card(self):
        card = chapter_card(13, r"In practice: \ taxonomies, \ diagnosis, \ recommendation", r"Where do categories "
                            r"do work outside the lab?", lit={2015: r"Fried \& Nesse", 2017: r"Kotov et al.",
                                                              2020: r"Yang et al."},
                            part=PART, scale=("mind", "world"), marr=("what",))
        with self.voiceover("Chapter thirteen. In practice: taxonomies, diagnosis and recommendation."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def diagnosis(self):
        d = load("cardsort")
        head = heading(r"A diagnosis is a polythetic category")
        eq = MathTex(r"\sum_{k=5}^{9} \left[\binom{9}{k} - \binom{7}{k}\right] = " + str(int(d["mdd_sets"])),
                     font_size=40, color=MODEL).move_to([-3.4, 1.5, 0])
        rows = rows_of([
            (r"a major depressive episode, \ in DSM-5: \ at least 5 of 9 symptoms, \ one of them low mood or loss of "
             r"interest", WHITE),
            (rf"that admits {int(d['mdd_sets'])} different sets of symptoms: \ two people can share the diagnosis "
             r"and only one symptom", MODEL),
            (r"Fried \& Nesse, \ 2015: \ 3,703 patients of the STAR*D trial showed 1,030 different profiles of 12 "
             r"symptoms; \ the commonest was shared by 1.8\%", CAT_A),
            (r"a family resemblance, \ like Wittgenstein's games; \ one response is to measure dimensions instead: \ "
             r"HiTOP \ (Kotov et al., \ 2017)", PROTO),
        ], 6.6, 21, 0.3).move_to([2.7, 0.0, 0])
        tag = published_tag(r"Fried \& Nesse (2015); \ Kotov et al. (2017); \ APA, \ DSM-5 (2013)")
        ptag = psyche_tag(r"\texttt{concepts.polythetic\_count}")
        with self.voiceover(
            "Categories do a great deal of work outside the laboratory, and one place is the clinic. "
            "<bookmark mark='a'/> In DSM-5, a major depressive episode needs at least five of nine symptoms, one of "
            "which must be low mood or loss of interest. <bookmark mark='b'/> Count the ways to meet that rule: "
            f"{int(d['mdd_sets'])}. Two people can share the diagnosis and have only one symptom in common. "
            "<bookmark mark='c'/> And the variety is real. Eiko Fried and Randolph Nesse looked at 3,703 patients "
            "in a large trial and found 1,030 different profiles across twelve symptoms. The most common profile was "
            "shared by fewer than two percent. <bookmark mark='d'/> A diagnosis like this is a polythetic category, "
            "a family resemblance like Wittgenstein's games. One response is to stop forcing people into boxes and "
            "measure dimensions of psychopathology instead, as the HiTOP consortium proposes. Act Eight returns to it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(ptag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Write(eq), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def sorting(self):
        d = load("cardsort")
        head = heading(r"Card sorting: \ how users group things")
        ic, dc, leaves = d["icoord"], d["dcoord"], list(d["leaves"])
        x0, x1 = -6.2, 0.6
        y0, y1 = -2.0, 2.0
        n = len(leaves)

        def X(v):
            return x0 + (v - 5) / (10 * n - 10) * (x1 - x0)

        def Y(v):
            return y0 + v * (y1 - y0)

        links = VGroup(*[VMobject(color=GREY_B, stroke_width=2.5).set_points_as_corners(
            [[X(a), Y(b), 0] for a, b in zip(xs, ys)]) for xs, ys in zip(ic, dc)])
        names = VGroup(*[label(w, font_size=17, color=FOOD_GROUP[w]).rotate(PI / 2).next_to([X(5 + 10 * k), y0, 0],
                                                                                         DOWN, buff=0.1)
                         for k, w in enumerate(leaves)])
        yl = label(r"1 $-$ share who grouped them", font_size=15, color=GREY_A).rotate(PI / 2).move_to(
            [x0 - 0.45, 0, 0])
        co = d["co"]
        idx = {w: k for k, w in enumerate(d["names"])}
        assert co[idx["potato"], idx["rice"]] > co[idx["potato"], idx["carrot"]]  # the narration says so
        assert max(co[idx["bread"], j] for j in range(len(co)) if j != idx["bread"]) < 0.4
        rows = rows_of([
            (rf"{int(d['people'])} simulated people sort 12 groceries into piles of their own choosing, \ each "
             r"attending to different features", WHITE),
            (r"the share who put each pair together is a similarity; \ clustering it gives the users' taxonomy", MODEL),
            (rf"potatoes go with rice \ ({100 * co[idx['potato'], idx['rice']]:.0f}\%) \ more than with carrots \ "
             rf"({100 * co[idx['potato'], idx['carrot']]:.0f}\%): \ a pile of cooked staples, \ not the shop's aisles",
             CAT_A),
            (r"bread belongs nowhere for long: \ a poor member of every pile, \ which is where a menu needs a link "
             r"from two places", PROTO),
        ], 5.2, 20, 0.3).move_to([4.0, 0.2, 0])
        ptag = psyche_tag(r"\texttt{concepts.card\_sort} \ (simulated sorters, \ illustrative features)")
        with self.voiceover(
            "A second place is design. When a team builds the menus of a website or the aisles of an online shop, "
            "it runs a card sort. <bookmark mark='a'/> People sort cards naming the items into piles of their own "
            "choosing. Here Psyche simulates forty people sorting twelve groceries, each attending to different "
            "features, the attention weights of chapter four. <bookmark mark='b'/> The share of people who put each "
            "pair in the same pile is a measure of similarity, and clustering it gives the users' own taxonomy. "
            "<bookmark mark='c'/> It isn't the shop's. Potatoes go with rice more often than with carrots: a pile "
            "of cooked staples. <bookmark mark='d'/> And bread belongs nowhere for long. It is a poor member of "
            "every pile, which tells the designer to list it in two places."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ptag))
            vo.wait_until("a")
            self.play(FadeIn(names, lag_ratio=0.05), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(links, lag_ratio=0.1), FadeIn(yl), FadeIn(rows[1]), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            k = leaves.index("bread")
            self.play(Indicate(names[k], color=PROTO, scale_factor=1.4), FadeIn(rows[3]))
        self.clear_scene()

    def machines(self):
        head = heading(r"Categories in machines")
        cols = VGroup()
        items = [
            (r"recommendation", MODEL, [r"\emph{people who bought this also bought}: \ item-to-item similarity, \ "
                                        r"an exemplar model with millions of exemplars",
                                        r"the neighbours are computed, \ not defined"]),
            (r"search", CAT_B, [r"documents and queries become vectors, \ and a match is a small angle: \ chapter "
                                r"eleven at the scale of the web",
                                r"it inherits the company the words kept, \ biases included"]),
            (r"labels", LOST, [r"a classifier learns the categories its labels draw; \ ImageNet's people categories "
                               r"were reviewed in 2019--2020, \ and many removed as offensive or not visual",
                               r"choosing categories is a decision about people"]),
        ]
        for k, (t, c, lines) in enumerate(items):
            col = VGroup(label(t, font_size=28, color=c),
                         rows_of([(lines[0], WHITE), (lines[1], GREY_A)], 3.7, 20, 0.3)).arrange(DOWN, buff=0.35,
                                                                                              aligned_edge=LEFT)
            col.move_to([-4.4 + 4.4 * k, 0.5, 0])
            cols.add(col)
        rows = rows_of([
            (r"the theories of this part run at industrial scale: \ similarity, \ exemplars, \ vector spaces, \ and "
             r"the question of who draws the boundaries", MODEL)], 12.4, 22, 0.3).to_edge(DOWN, buff=0.65)
        tag = published_tag(r"Yang et al. (2020), \ the ImageNet person subtree")
        with self.voiceover(
            "And a third place is software. <bookmark mark='a'/> Recommendation: people who bought this also bought "
            "that. Item-to-item similarity is an exemplar model with millions of exemplars, and the neighbours are "
            "computed, never defined. <bookmark mark='b'/> Search: documents and queries become vectors, and a match "
            "is a small angle between them. That's chapter eleven at the scale of the web, and it inherits the "
            "company the words kept, prejudices included. <bookmark mark='c'/> Labels: a classifier learns whatever "
            "categories its labels draw. In 2019 and 2020 the team behind ImageNet, the dataset that launched modern "
            "computer vision, reviewed its categories of people and removed many as offensive, or as things no "
            "picture can show. Choosing categories is a decision about people. <bookmark mark='d'/> The theories of "
            "this part run at industrial scale, and so does the question of who draws the boundaries."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, c in zip("abc", cols):
                vo.wait_until(m)
                self.play(FadeIn(c, shift=UP * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(rows[0]))
        self.clear_scene()
