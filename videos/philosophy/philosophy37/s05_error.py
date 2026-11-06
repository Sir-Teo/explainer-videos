from __future__ import annotations

from videos.philosophy.philosophy37.common import *  # noqa: F403


class Error(VoiceoverScene):
    def construct(self):
        card = chapter_card(4, r"Error theory", r"What if every moral claim is false?", lit=(1977,), part=PART)
        with self.voiceover("Chapter four. Error theory."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.mackie()
        self.companions()
        self.after()
        self.price()

    def mackie(self):
        hc = history_card(1977, r"J. L. Mackie", r"\textit{Ethics: \ Inventing Right and Wrong}", width=5.8,
                          color=HIST).to_corner(UL, buff=0.3)
        rows = [(r"the claim", r"moral judgments purport to describe objective, \ prescriptive facts; \ there are "
                               r"none; \ so they are all false", ANTI),
                (r"relativity", r"moral codes vary with ways of life: \ better explained by different customs than by "
                                r"different perceptions of one truth", GREY_A),
                (r"queerness: \ metaphysics", r"objective values would be entities of a strange sort, \ with "
                                              r"`to-be-pursuedness' built into them", BAD),
                (r"queerness: \ knowledge", r"we would need a special faculty of moral perception to know them", BAD),
                (r"after the error", r"Joyce \ (2001): \ fictionalism; \ Olson \ (2014): \ keep talking, \ knowing it is "
                                     r"false", EXPR)]
        g = rows_table(rows, top=1.3, gap=0.4, width=8.0, x_text=-1.8, label_size=19, text_size=19)
        with self.voiceover(
            "John Mackie's error theory accepts half of realism. <bookmark mark='a'/>Moral judgments do purport to "
            "describe objective facts, facts that would bind anyone; but there are no such facts, so every positive "
            "moral judgment is false, as every claim about witches is. <bookmark mark='b'/>His first argument was from "
            "relativity: moral codes vary with ways of life, and the variation is better explained by differences of "
            "custom than by different perceptions of one moral truth. <bookmark mark='c'/>His second, from "
            "queerness: objective values would be entities of a very strange sort, with to-be-pursuedness somehow "
            "built into them. <bookmark mark='d'/>And knowing them would need a special faculty of moral perception, "
            "unlike any other. <bookmark mark='e'/>Error theorists since, like Richard Joyce and Jonas Olson, have "
            "asked what to do next: treat morality as a useful fiction, or keep talking as before, knowing it is "
            "strictly false."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def companions(self):
        head = label(r"Companions in guilt", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"the parallel", r"epistemic norms are categorical too: \ you ought to believe what your evidence "
                                  r"supports, \ whatever you want", IS),
                (r"the dilemma", r"if moral reasons are queer, \ so are epistemic reasons; \ and then the error "
                                 r"theorist has no reason to believe error theory", BAD),
                (r"Cuneo \ (2007)", r"\textit{The Normative Web}: \ moral and epistemic facts stand or fall "
                                    r"together", REAL),
                (r"the reply", r"Olson; \ Streumer: \ bite the bullet for epistemic reasons too, \ or find a "
                               r"difference", ANTI)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.1, label_size=20, text_size=20)
        with self.voiceover(
            "The strongest reply to Mackie finds him companions in guilt. <bookmark mark='a'/>Epistemic norms are "
            "categorical too: you ought to believe what your evidence supports, whatever you happen to want. "
            "<bookmark mark='b'/>If moral reasons are too queer to exist, so are epistemic ones; and then the error "
            "theorist has no reason to believe the error theory, or anything else. <bookmark mark='c'/>Terence Cuneo "
            "pressed the argument in The Normative Web, of 2007: moral and epistemic facts stand or fall together. "
            "<bookmark mark='d'/>Some error theorists, like Bart Streumer, accept the epistemic consequence, and say "
            "we cannot believe their theory though it may be true; others look for a difference between the two "
            "kinds of norm."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def after(self):
        head = label(r"After the error", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"fictionalism", r"Joyce \ (2001): \ keep moral talk as a useful fiction, \ like talk of Sherlock Holmes, \ for its help with self-control and cooperation", EXPR),
                (r"abolitionism", r"Garner; \ Hinckfuss: \ give it up: \ moral talk breeds intolerance and conflict", BAD),
                (r"conservationism", r"Olson \ (2014): \ go on believing, \ in practice, \ while knowing it is false", ANTI),
                (r"the comparison", r"atheists who keep saying `thank God': \ is morality a practice that survives its metaphysics?", GOAL)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "If the error theory is true, what should we do with moral talk? <bookmark mark='a'/>Richard Joyce's The "
            "Myth of Morality, of 2001, recommended fictionalism: keep it as a useful fiction, like talk of Sherlock "
            "Holmes, for the help it gives with self-control and cooperation. <bookmark mark='b'/>Abolitionists like "
            "Richard Garner and Ian Hinckfuss said give it up, since moral talk breeds intolerance and conflict. "
            "<bookmark mark='c'/>Jonas Olson's conservationism, of 2014, says go on believing in practice, while "
            "knowing on reflection that it is false. <bookmark mark='d'/>Compare atheists who still say thank God: "
            "the question is whether morality is a practice that can survive the loss of its metaphysics."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def price(self):
        d = load("tetrad")
        claims = [(c["key"], c["text"]) for c in d["claims"]]
        sv = d["survey"]
        assert d["mus"] == [["NONE", "OBJ", "SOME"]] and sorted(d["mcs"]) == [["NONE"], ["OBJ"], ["SOME"]]
        assert (sv["moral realism"], sv["moral anti-realism"]) == (0.621, 0.261)
        pl = PriceList(claims, mus=[tuple(m) for m in d["mus"]], radius=2.4, width=4.0, font_size=20,
                       center=[0, -0.6, 0], title=r"The Price List: \ Mackie's triad")
        positions = [(("NONE",), r"realism", r"Shafer-Landau; \ Enoch; \ Parfit; \ Boyd; \ Brink",
                      sv["moral realism"], r"PhilPapers 2020"),
                     (("OBJ",), r"no claim to objectivity", r"Ayer; \ Blackburn; \ Gibbard: \ expressivism", None, r""),
                     (("SOME",), r"error theory", r"Mackie; \ Joyce; \ Olson; \ Streumer", None, r"")]
        with self.voiceover(
            "Three claims cannot all be true. <bookmark mark='a'/>Moral claims purport to state objective facts. "
            "There are no objective moral facts. And some moral claims are true. <bookmark mark='b'/>If the first "
            "two hold, every moral claim fails to be true. <bookmark mark='c'/>The realist denies that there are no "
            "moral facts; sixty two percent of philosophers lean that way. <bookmark mark='d'/>The expressivist denies "
            "that moral claims purport to state objective facts: they express attitudes instead, and can be true in "
            "a deflationary sense. <bookmark mark='e'/>And the error theorist denies that any moral claim is true: "
            "Mackie's own position. Together the anti-realists make up twenty six percent."
        ) as vo:
            self.play(FadeIn(pl.title))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in pl.cards], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(Create(pl.conflict))
            first = True
            for mk, (mcs, name, who, share, note) in zip("cde", positions):
                vo.wait_until(mk)
                if not first:
                    self.play(*pl.reset())
                first = False
                anims, centre = pl.position(mcs, name, who, share=share, share_note=note, width=3.0)
                self.play(*anims)
        self.clear_scene()
