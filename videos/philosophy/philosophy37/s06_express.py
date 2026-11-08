from __future__ import annotations

from videos.philosophy.philosophy37.common import *  # noqa: F403


class Express(VoiceoverScene):
    def construct(self):
        card = chapter_card(5, r"Expressivism", r"Do moral words describe, \ or express?", lit=(1936, 1984), part=PART)
        with self.voiceover("Chapter five. Expressivism."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.ayer()
        self.stevenson()
        self.motivation()
        self.quasi()
        self.hybrid()

    def ayer(self):
        q = quote_card(r"If I say to someone, \ `You acted wrongly in stealing that money,' \ I am not stating anything "
                       r"more than if I had simply said, \ `You stole that money.'", r"A. J. Ayer",
                       r"\textit{Language, \ Truth and Logic} \ (1936), \ chapter 6", width=10.0, font_size=28).move_to(
            [0, 1.0, 0])
        rows = stack([(r"`wrong' adds no content: \ it shows the speaker's disapproval, \ as a tone of horror would",
                       EXPR),
                      (r"so `stealing is wrong' is neither true nor false: \ emotivism, \ the `boo-hurrah' theory",
                       EXPR),
                      (r"the motive: \ verificationism, \ and Moore's open question: \ no fact could close it", GREY_A)],
                     font_size=20, buff=0.2).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "In 1936 the young A. J. Ayer drew the opposite conclusion from Moore's. <bookmark mark='a'/>If I say to "
            "someone, you acted wrongly in stealing that money, I am not stating anything more than if I had simply "
            "said, you stole that money. <bookmark mark='b'/>The word wrong adds no content; it shows my disapproval, "
            "as a peculiar tone of horror would. <bookmark mark='c'/>So stealing is wrong is neither true nor false: "
            "emotivism, nicknamed the boo-hurrah theory. <bookmark mark='d'/>Ayer's motive was his verificationism, "
            "and Moore's open question too: if no natural fact can settle whether something is good, perhaps that is "
            "because goodness is not a fact at all."
        ) as vo:
            self.play(FadeIn(q))
            vo.wait_until("a")
            for mk, r in zip("bcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def stevenson(self):
        head = label(r"Disagreement in attitude \ (Stevenson, \ 1944)", font_size=30, color=CONN).to_edge(UP,
                                                                                                         buff=0.35)
        rows = [(r"two kinds of disagreement", r"in belief: \ about what is the case; \ in attitude: \ about what to "
                                               r"favour", EXPR),
                (r"the example", r"one wants to dine at a restaurant with music, \ the other at one without: \ they "
                                 r"disagree though no fact is in dispute", GREY_A),
                (r"moral argument", r"facts can move attitudes, \ but the disagreement can survive agreement on every "
                                   r"fact", OUGHT),
                (r"the explanation", r"why moral disagreement feels real and is so hard to end: \ moral twin earth, \ "
                                     r"read this way", EXPR)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Charles Stevenson's Ethics and Language, of 1944, made the view subtler. <bookmark mark='a'/>He "
            "distinguished disagreement in belief, about what is the case, from disagreement in attitude, about what "
            "to favour. <bookmark mark='b'/>Two friends who want to dine at different restaurants disagree, though no "
            "fact is in dispute between them. <bookmark mark='c'/>Moral argument mixes the two: facts can move "
            "attitudes, but a moral disagreement can survive agreement on every fact. <bookmark mark='d'/>That, "
            "Stevenson thought, is why moral disagreement feels so real and is so hard to end, and it is how the "
            "earthers and twin earthers of chapter three really disagree."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def motivation(self):
        d = load("smith")
        claims = [(c["key"], c["text"]) for c in d["claims"]]
        assert d["mus"] == [["COG", "HUME", "INT"]] and sorted(d["mcs"]) == [["COG"], ["HUME"], ["INT"]]
        pl = PriceList(claims, mus=[tuple(m) for m in d["mus"]], radius=2.4, width=4.2, font_size=20,
                       center=[0, -0.6, 0], title=r"Smith's moral problem \ (1994)")
        positions = [(("COG",), r"expressivism", r"Ayer; \ Stevenson; \ Blackburn; \ Gibbard"),
                     (("INT",), r"externalism", r"Brink \ (1989); \ the amoralist who judges but does not care"),
                     (("HUME",), r"anti-Humeanism", r"Nagel; \ McDowell: \ some beliefs motivate by themselves")]
        with self.voiceover(
            "Michael Smith's The Moral Problem, of 1994, put the case for expressivism as a triad. "
            "<bookmark mark='a'/>Moral judgments express beliefs about objective matters of fact. If someone judges "
            "that she ought to act, she is, other things equal, motivated to act. And motivation needs a desire, "
            "while belief and desire are distinct existences: no belief by itself requires any desire. "
            "<bookmark mark='b'/>Together, they make moral judgments beliefs that cannot motivate, and yet do. "
            "<bookmark mark='c'/>The expressivist denies the first: moral judgments are desire-like states, so of "
            "course they motivate. <bookmark mark='d'/>The externalist, like David Brink, denies the second: an "
            "amoralist could judge that something is wrong and simply not care. <bookmark mark='e'/>And the "
            "anti-Humean, like Thomas Nagel or John McDowell, denies the third: some beliefs, about reasons, motivate "
            "by themselves. Smith's own answer was subtler: motivation is necessary only for the practically "
            "rational."
        ) as vo:
            self.play(FadeIn(pl.title))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in pl.cards], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(Create(pl.conflict))
            first = True
            for mk, (mcs, name, who) in zip("cde", positions):
                vo.wait_until(mk)
                if not first:
                    self.play(*pl.reset())
                first = False
                anims, centre = pl.position(mcs, name, who, width=3.0)
                self.play(*anims)
        self.clear_scene()

    def quasi(self):
        head = label(r"Quasi-realism \ (Blackburn, \ 1984; \ 1993)", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"the project", r"start from attitudes, \ and earn the right to everything the realist says", EXPR),
                (r"truth", r"`it is true that cruelty is wrong' just says again that cruelty is wrong: \ a minimal "
                           r"truth predicate", GREY_A),
                (r"mind-independence", r"`cruelty would be wrong even if we approved of it': \ itself a moral attitude "
                                       r"we hold, \ against cruelty in any circumstances", OUGHT),
                (r"the worry", r"if the expressivist can say everything the realist says, \ what is left of the "
                               r"difference? \ Dreier \ (2004): \ the problem of creeping minimalism", BAD)]
        g = rows_table(rows, top=1.5, gap=0.45, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Simon Blackburn's quasi-realism took the boldest line. <bookmark mark='a'/>Start from attitudes, and earn "
            "the right to say everything the realist says. <bookmark mark='b'/>It is true that cruelty is wrong just "
            "says again that cruelty is wrong, with a minimal notion of truth. <bookmark mark='c'/>Even cruelty would "
            "be wrong if we all approved of it can be said: it expresses a further attitude we hold, against cruelty "
            "whatever anyone thinks. <bookmark mark='d'/>But if the expressivist can say everything the realist says, "
            "what is left of the difference between them? James Dreier called this the problem of creeping "
            "minimalism, in 2004. And one thing the expressivist must still explain is logic, as the next chapter "
            "shows."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def hybrid(self):
        head = label(r"Hybrid views", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"the idea", r"a moral judgment is both a belief and an attitude: \ like a slur, \ which describes and expresses at once", EXPR),
                (r"Copp \ (2001)", r"realist-expressivism: \ moral sentences state facts, \ and conventionally express attitudes too", REAL),
                (r"Ridge \ (2006; \ 2014)", r"ecumenical expressivism: \ a judgment combines an attitude toward a standard with a belief about what the standard requires", EXPR),
                (r"the hope", r"get logic from the belief, \ motivation from the attitude: \ solving Smith and Geach at once", GOAL)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "A newer family of views refuses the choice. <bookmark mark='a'/>Hybrid theories say a moral judgment is "
            "both a belief and an attitude, as a slur both describes a person and expresses contempt. <bookmark "
            "mark='b'/>David Copp's realist-expressivism, of 2001, says moral sentences state facts and "
            "conventionally express attitudes as well. <bookmark mark='c'/>Michael Ridge's ecumenical expressivism "
            "combines an attitude toward a standard with a belief about what that standard requires. <bookmark "
            "mark='d'/>The hope is to get logic from the belief and motivation from the attitude, answering Smith's "
            "triad and Geach's problem at once; critics doubt that either part does all its work."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
