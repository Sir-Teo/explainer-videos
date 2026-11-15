from __future__ import annotations

from videos.psychology.psych22.common import *  # noqa: F403

TREE = {
    "animal": (-3.0, 2.3), "bird": (-4.8, 0.9), "fish": (-1.2, 0.9),
    "canary": (-5.9, -0.6), "penguin": (-3.7, -0.6), "salmon": (-1.2, -0.6),
}
TREE_EDGES = (("animal", "bird"), ("animal", "fish"), ("bird", "canary"), ("bird", "penguin"), ("fish", "salmon"))
TREE_PROPS = {
    "animal": ("has skin", "breathes"), "bird": ("has wings", "flies"), "fish": ("has gills", "swims"),
    "canary": ("sings", "is yellow"), "penguin": ("can't fly", "swims"), "salmon": ("is pink",),
}

NET_POS = {
    "animal": (-2.6, 2.4), "bird": (-4.4, 1.2), "fish": (-0.9, 1.2), "robin": (-5.6, -0.2), "canary": (-4.3, -0.4),
    "penguin": (-2.8, -0.2), "salmon": (-0.4, -0.3), "fly": (-6.2, 1.6), "wings": (-5.4, 2.3), "swim": (-1.5, -1.2),
    "sing": (-4.1, -1.5), "red": (-5.6, -1.6), "fire engine": (-6.0, -2.7), "apple": (-4.6, -2.7),
    "cherry": (-3.1, -2.5),
}


class Network(VoiceoverScene):
    def construct(self):
        self.card()
        self.hierarchy()
        self.failures()
        self.spreading()
        self.priming()

    def card(self):
        card = chapter_card(8, r"Knowledge as a network", r"How is what you know about the world stored?",
                            lit={1969: r"Collins \& Quillian", 1971: r"Meyer \& Schvaneveldt",
                                 1975: r"Collins \& Loftus", 2013: r"Hutchison et al."},
                            part=PART, scale=("mind",), marr=("how",))
        with self.voiceover("Chapter eight. Knowledge as a network."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def hierarchy(self):
        head = heading(r"Collins and Quillian, \ 1969")
        nodes, props = VGroup(), VGroup()
        for name, (x, y) in TREE.items():
            nodes.add(word_chip(name, CAT_A, 22).move_to([x, y, 0]))
            props.add(VGroup(*[label(p, font_size=16, color=GREY_A) for p in TREE_PROPS[name]]).arrange(
                DOWN, buff=0.06).next_to([x, y, 0], DOWN, buff=0.3).shift(RIGHT * 0.0))
        for p, (name, (x, y)) in zip(props, TREE.items()):
            p.move_to([x + (0.0 if name == "animal" else 0.0), y - 0.58, 0])
            if name == "animal":
                p.next_to(nodes[0], RIGHT, buff=0.25)
        edges = VGroup(*[Line([*TREE[a], 0], [*TREE[b], 0], color=GREY_D, stroke_width=2) for a, b in TREE_EDGES])
        for e, (a, b) in zip(edges, TREE_EDGES):
            e.put_start_and_end_on(nodes[list(TREE).index(a)].get_bottom(), nodes[list(TREE).index(b)].get_top())
        sentences = VGroup(*[label(t, font_size=20, color=c) for t, c in (
            (r"a canary can sing: \ 0 links", MODEL), (r"a canary can fly: \ 1 link up", CAT_A),
            (r"a canary has skin: \ 2 links up", PROTO))]).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        rows = rows_of([
            (r"concepts are nodes in a hierarchy, \ joined by \emph{is a} links", WHITE),
            (r"\emph{cognitive economy}: \ a property is stored once, \ at the highest node it applies to, \ and "
             r"inherited below", CAT_A),
            (r"so checking a sentence means travelling links, \ and each link should take time", MODEL),
            (r"the first experiments agreed: \ more links, \ slower answers", GREY_A),
        ], 5.0, 21, 0.28).move_to([3.9, 0.8, 0])
        sentences.next_to(rows, DOWN, buff=0.4).align_to(rows, LEFT)
        tag = historical_tag(r"Collins \& Quillian (1969); \ after Quillian (1968), \ a computer program")
        with self.voiceover(
            "How is everything you know about the world stored? In 1969 Allan Collins and Ross Quillian proposed an "
            "answer taken from a computer program Quillian had written. <bookmark mark='a'/> Concepts are nodes in a "
            "hierarchy, joined by is a links: a canary is a bird, a bird is an animal. <bookmark mark='b'/> The "
            "principle is cognitive economy. A property is stored once, at the highest node it applies to. Has wings "
            "is stored with bird, not with every bird, and it is inherited by everything below. "
            "<bookmark mark='c'/> So answering a question means travelling the links, and each link should take "
            "time. A canary can sing is stored right at canary. A canary can fly needs one step up. A canary has skin "
            "needs two, up to animal. <bookmark mark='d'/> The first experiments agreed: the more links a sentence needed, the "
            "slower people were to say true."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), LaggedStart(*[FadeIn(n) for n in nodes], lag_ratio=0.15),
                      Create(edges))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(props), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            self.play(FadeIn(sentences, lag_ratio=0.3))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def failures(self):
        head = heading(r"Where the hierarchy fails")
        cols = VGroup()
        items = [
            (r"typicality", LOST, [r"\emph{a robin is a bird} is checked faster than \emph{a penguin is a bird}, \ "
                                   r"though both are one link", r"the hierarchy has no place for a good member"]),
            (r"levels reversed", PROTO, [r"\emph{a bear is an animal} can be faster than \emph{a bear is a mammal}, "
                                         r"\ though animal is further up", r"Rips, \ Shoben \& Smith, \ 1973"]),
            (r"familiarity", CAT_B, [r"Conrad, \ 1972: \ properties people often mention with a word are checked "
                                     r"fast at any level",
                                     r"the link counts were confounded with how familiar each fact is"]),
        ]
        for k, (t, c, lines) in enumerate(items):
            col = VGroup(label(t, font_size=28, color=c),
                         rows_of([(lines[0], WHITE), (lines[1], GREY_A)], 3.7, 20, 0.3)).arrange(DOWN, buff=0.35,
                                                                                              aligned_edge=LEFT)
            col.move_to([-4.4 + 4.4 * k, 0.5, 0])
            cols.add(col)
        rows = rows_of([
            (r"the tidy tree was wrong; \ the idea of a network, \ and of time spent moving through it, \ survived",
             MODEL)], 12.4, 23, 0.3).to_edge(DOWN, buff=0.65)
        tag = published_tag(r"Rips, \ Shoben \& Smith (1973); \ Conrad (1972)")
        with self.voiceover(
            "The tree soon ran into trouble. <bookmark mark='a'/> Typicality, again. A robin is a bird is checked "
            "faster than a penguin is a bird, though both are a single link. A hierarchy has no way to say that one "
            "member is better than another. <bookmark mark='b'/> Levels reversed. Lance Rips, Edward Shoben and "
            "Edward Smith found that a bear is an animal can be checked faster than a bear is a mammal, though animal "
            "is further up the tree. <bookmark mark='c'/> And familiarity. Carol Conrad showed in 1972 that the "
            "properties people most often mention with a word are checked fast whatever their level. The link counts "
            "had been confounded with how familiar each fact was. <bookmark mark='d'/> The tidy tree was wrong. But "
            "two of its ideas survived: knowledge is a network, and using it takes time spent moving through it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, c in zip("abc", cols):
                vo.wait_until(m)
                self.play(FadeIn(c, shift=UP * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(rows[0]))
        self.clear_scene()

    def spreading(self):
        d = load("network")
        names = list(d["nodes"])
        hist = d["hist"]
        head = heading(r"Collins and Loftus, \ 1975: \ spreading activation")
        dots, tags = VGroup(), VGroup()
        for nm in names:
            x, y = NET_POS[nm]
            dots.add(Dot([x, y, 0], radius=0.13, color=MODEL, fill_opacity=0.12))
            tags.add(label(nm, font_size=17, color=GREY_A).next_to([x, y, 0], UP, buff=0.12))
        edges = VGroup(*[Line(NET_POS[a] + (0,), NET_POS[b] + (0,), color=GREY_D, stroke_width=2)
                         for a, b in d["edges"]])
        src = names.index("robin")
        dots[src].set_fill(CAT_A, opacity=1.0)
        rows = rows_of([
            (r"no tree: \ any two concepts can be linked, \ shorter links for closer meanings", WHITE),
            (r"thinking of a concept sends activation out along its links, \ weaker with each step and divided "
             r"among them", MODEL),
            (r"\emph{robin} warms \emph{bird} and \emph{red}; \ \emph{red} in turn warms \emph{fire engine} and "
             r"\emph{cherry}", CAT_A),
            (r"a concept with many links passes less down each: \ Anderson's \emph{fan effect}, \ the more you "
             r"know about something, \ the slower each fact", PROTO),
        ], 5.4, 21, 0.3).move_to([3.6, 0.2, 0])
        ptag = psyche_tag(r"\texttt{concepts.spreading\_activation} \ (an illustrative network)")

        def state(step):
            a = hist[step]
            anims = []
            for k, dot in enumerate(dots):
                if k == src:
                    continue
                v = float(np.sqrt(min(1.0, a[k] / 0.8)))
                anims.append(dot.animate.set_fill(MODEL, opacity=max(0.12, v)).scale_to_fit_width(0.26 + 0.16 * v))
            return anims

        with self.voiceover(
            "In 1975 Allan Collins and Elizabeth Loftus kept the network and threw away the tree. "
            "<bookmark mark='a'/> Any two concepts can be linked, and closer meanings have shorter links. "
            "<bookmark mark='b'/> Thinking of a concept sends activation out along its links, weaker with every step "
            "and divided among the links. Here is an illustrative network, with robin lit. <bookmark mark='c'/> One "
            "step: bird and red warm up. Two steps: activation reaches the things that are red, a fire engine and a "
            "cherry, and the other birds. Three steps, and it is spread thinly everywhere. "
            "<bookmark mark='d'/> Dividing activation among links explains a curious effect John Anderson found: "
            "the more facts you have learned about a person or a place, the slower you are to verify any one of "
            "them. He called it the fan effect."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ptag), Create(edges), FadeIn(dots), FadeIn(tags))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(*state(1), FadeIn(rows[2]))
            self.play(*state(2))
            self.play(*state(3))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def priming(self):
        a = archive.HUTCHISON_2013.data
        head = heading(r"Semantic priming")
        prime = word_chip("BREAD", CAT_A, 30).move_to([-5.0, 1.8, 0])
        target = word_chip("butter", MODEL, 30).move_to([-2.6, 1.8, 0])
        arrow = Arrow(prime.get_right(), target.get_left(), buff=0.1, color=GREY_B, stroke_width=3)
        q = label(r"is it a word?", font_size=22, color=GREY_A).next_to(VGroup(prime, target), DOWN, buff=0.25)
        A = axes([0, 4.2], [0, 70], x_length=5.0, y_length=3.0, xticks=[], yticks=[0, 30, 60],
                 yfmt=lambda v: f"{v:.0f}", ylabel=r"priming, \ ms", center=[-3.6, -1.1, 0], font_size=17)
        xs = (0.6, 1.4, 2.8, 3.6)
        vals = (a["hutchison2008_short_ms"], a["hutchison2008_long_ms"], a["spp_first_short_ms"],
                a["spp_first_long_ms"])
        cols = (GREY_B, GREY_B, MODEL, MODEL)
        bs = VGroup(*[bars(A.ax, [x], [v], c, 0.6) for x, v, c in zip(xs, vals, cols)])
        vlabels = VGroup(*[label(f"{v:.0f}", font_size=18).next_to(A.ax.c2p(x, v), UP, buff=0.06)
                           for x, v in zip(xs, vals)])
        groups = VGroup(label(r"2008: \ 300 strong pairs", font_size=16, color=GREY_B).next_to(A.ax.c2p(1.0, 0),
                                                                                             DOWN, buff=0.12),
                        label(r"2013: \ the SPP", font_size=16, color=MODEL).next_to(A.ax.c2p(3.2, 0), DOWN,
                                                                                   buff=0.12))
        rows = rows_of([
            (r"Meyer \& Schvaneveldt, \ 1971: \ people decide faster that \emph{butter} is a word after "
             r"\emph{bread} than after \emph{nurse}", WHITE),
            (rf"the Semantic Priming Project: \ {num(a['targets'])} targets, \ {a['subjects']} people at four "
             r"universities, \ two tasks, \ two delays", MODEL),
            (rf"priming is real and reliable, \ but small: \ about {a['ldt_all_ms']:.0f} ms in lexical decision, \ "
             rf"{a['naming_all_ms']:.0f} ms in naming", CAT_A),
            (r"and smaller than the earlier, \ hand-picked studies suggested: \ the authors were unsure why", LOST),
        ], 5.6, 21, 0.3).move_to([3.5, 0.2, 0])
        tag = published_tag(r"Meyer \& Schvaneveldt (1971); \ Hutchison et al. (2013)")
        with self.voiceover(
            "Spreading activation predicts something you can measure. <bookmark mark='a'/> In 1971 David Meyer and "
            "Roger Schvaneveldt asked people to decide, as fast as they could, whether a string of letters was a "
            "word. They were faster to say butter is a word just after reading bread than after reading an "
            "unrelated word. Reading bread had warmed butter in advance. This is semantic priming. "
            "<bookmark mark='b'/> How big is it? The Semantic Priming Project measured it at scale: "
            f"{a['targets']:,} target words, {a['subjects']} people at four universities, in lexical decision and in "
            "naming, with a short and a long delay between the words. <bookmark mark='c'/> Priming is real and "
            f"reliable, but small: about {a['ldt_all_ms']:.0f} milliseconds in lexical decision, and "
            f"{a['naming_all_ms']:.0f} in reading aloud. <bookmark mark='d'/> And it was smaller than earlier "
            "studies suggested. For the strongest associates, the bars on the left are the same lab's 2008 study, "
            "the bars on the right the project's. The authors wrote that they were unsure why. One possibility "
            "they raised: the earlier studies used only the strongest pairs, while the project's pairs cover the "
            "natural range."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(prime), GrowArrow(arrow), FadeIn(target), FadeIn(q), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(A), *[GrowFromEdge(b, DOWN) for b in bs], FadeIn(vlabels), FadeIn(groups),
                      FadeIn(rows[3]))
        self.clear_scene()
