from __future__ import annotations

from videos.psychology.psych22.common import *  # noqa: F403

LEVEL_COL = (CAT_B, MODEL, EXEMPLAR)


class Theories(VoiceoverScene):
    def construct(self):
        self.card()
        self.basic()
        self.utility()
        self.pizza()
        self.essences()

    def card(self):
        card = chapter_card(9, r"Concepts as theories", r"Is a concept a cluster of similar things, or an "
                            r"explanation?", lit={1976: r"Rosch et al.", 1985: r"Murphy \& Medin", 1986: r"Gelman \& "
                                                  r"Markman", 1989: r"Keil; \ Rips"},
                            part=PART, scale=("mind", "world"), marr=("what",))
        with self.voiceover("Chapter nine. Concepts as theories."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def basic(self):
        head = heading(r"The basic level")
        lv = VGroup(*[word_chip(w, c, 28) for w, c in (("furniture", CAT_B), ("chair", MODEL),
                                                         ("kitchen chair", EXEMPLAR))]).arrange(DOWN, buff=0.7)
        lv.move_to([-4.6, 0.4, 0])
        arrows = VGroup(*[Arrow(lv[k].get_bottom(), lv[k + 1].get_top(), buff=0.08, color=GREY_C, stroke_width=3)
                          for k in range(2)])
        tags = VGroup(*[label(t, font_size=18, color=GREY_A).next_to(lv[k], RIGHT, buff=0.3) for k, t in
                        enumerate((r"superordinate", r"basic", r"subordinate"))])
        rows = rows_of([
            (r"Rosch and colleagues, \ 1976: \ asked to list attributes, \ people give few for \emph{furniture}, \ "
             r"many for \emph{chair}, \ hardly more for \emph{kitchen chair}", WHITE),
            (r"the basic level is the most inclusive one whose members share many attributes, \ a shape, \ and a "
             r"way of handling them", MODEL),
            (r"it is the level people name things at, \ verify fastest, \ and children learn first", CAT_A),
            (r"and it moves with knowledge: \ Tanaka and Taylor, \ 1991, \ found dog and bird experts naming at the "
             r"subordinate level, \ \emph{beagle}, \ \emph{robin}, \ as fast as at the basic", PROTO),
        ], 6.4, 21, 0.3).move_to([2.9, 0.1, 0])
        tag = published_tag(r"Rosch, \ Mervis, \ Gray, \ Johnson \& Boyes-Braem (1976); \ Tanaka \& Taylor (1991)")
        with self.voiceover(
            "Before theories, a puzzle about levels. The thing you are sitting on is a kitchen chair, a chair, and "
            "a piece of furniture. Which is it, really? <bookmark mark='a'/> In 1976 Eleanor Rosch and her colleagues "
            "asked people to list the attributes of things at each level. They listed few for furniture, many for "
            "chair, and hardly more for kitchen chair. <bookmark mark='b'/> The middle level, which they called "
            "basic, is the most inclusive level whose members share many attributes, a common shape, and a common "
            "way of handling them. <bookmark mark='c'/> It is the level people name things at, the level they verify "
            "fastest, and the level children learn first. <bookmark mark='d'/> And it moves with knowledge. James "
            "Tanaka and Marjorie Taylor found that dog experts and bird experts, in their own domain, named pictures "
            "at the subordinate level, beagle or robin, as fast as at the basic level."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(lv), FadeIn(arrows), FadeIn(tags))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def utility(self):
        d = load("levels")
        head = heading(r"Derivation: \ category utility")
        eq = MathTex(r"\mathrm{CU}(c) = P(c) \sum_k \big[ P(f_k \mid c)^2 - P(f_k)^2 \big]", font_size=40,
                     color=MODEL).move_to([-3.2, 2.2, 0])
        A = axes([0, 4], [0, 1.4], x_length=5.4, y_length=3.2, xticks=[0, 1, 2, 3, 4], yticks=[0, 0.5, 1.0],
                 yfmt=lambda v: f"{v:.1f}", xlabel=r"features every member of a superordinate shares",
                 ylabel=r"mean category utility", center=[-3.0, -0.6, 0], font_size=17)
        fs, U = d["f_super"], d["U"]
        lines = VGroup(*[VGroup(curve(A.ax, fs, U[:, k], LEVEL_COL[k], 3),
                                *[Dot(A.ax.c2p(float(x), float(y)), radius=0.05, color=LEVEL_COL[k])
                                  for x, y in zip(fs, U[:, k])]) for k in range(3)])
        key = legend([(LEVEL_COL[k], t) for k, t in enumerate((r"superordinate", r"basic", r"subordinate"))],
                     font_size=18).move_to(A.ax.c2p(3.0, 0.22))
        rows = rows_of([
            (r"how many more features can you guess about a thing, \ on average, \ once you know it is a $c$?", WHITE),
            (r"large categories score through $P(c)$, \ tight ones through $P(f \mid c)$: \ the measure trades "
             r"the two off", MODEL),
            (r"in an illustrative world of 3 superordinates, \ 9 basic kinds and 18 subtypes, \ the basic level wins "
             r"while superordinates share little", CAT_A),
            (r"give them more in common and the peak climbs: \ the basic level is a fact about how the world's "
             r"features cluster, \ not a fixed rung", PROTO),
        ], 5.8, 21, 0.3).move_to([3.5, 0.0, 0])
        ptag = psyche_tag(r"\texttt{concepts.category\_utility}, \ \texttt{nested\_world} \ (illustrative)")
        with self.voiceover(
            "Why that level? James Corter and Mark Gluck proposed a measure in 1992. <bookmark mark='a'/> Category "
            "utility asks: once you know a thing belongs to category c, how many more of its features can you "
            "guess correctly, on average? <bookmark mark='b'/> Large categories score through the probability of "
            "the category: they apply to many things. Tight categories score through the features they predict. The "
            "measure trades one against the other. <bookmark mark='c'/> Here is an illustrative world with three "
            "superordinates, nine basic kinds and eighteen subtypes. While the members of a superordinate share "
            "little, as Rosch found for furniture, the basic level has the highest utility. "
            "<bookmark mark='d'/> But give the superordinates more features in common, and the peak climbs to them. "
            "So the basic level is not a fixed rung of a ladder. It is a fact about how features cluster in the "
            "world. And the experts' shift is something this measure does not produce: giving the subtypes more "
            "features of their own never lifts them above the basic level here. Knowing a domain changes more than "
            "a feature count."
        ) as vo:
            self.play(FadeIn(head), Write(eq), FadeIn(ptag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(A), FadeIn(key), *[Create(ln) for ln in lines], FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Indicate(lines[0], color=CAT_B), FadeIn(rows[3]))
        self.clear_scene()

    def pizza(self):
        head = heading(r"Similarity is not enough")
        obj = Circle(radius=0.55, color=CAT_A, fill_opacity=0.25).move_to([-5.3, 1.3, 0])
        size = label(r"3 inches across", font_size=20, color=CAT_A).next_to(obj, DOWN, buff=0.15)
        q = Circle(radius=0.33, color=GREY_B, fill_opacity=0.25).move_to([-3.4, 1.9, 0])
        pz = Circle(radius=0.9, color=LOST, fill_opacity=0.2).move_to([-3.1, 0.3, 0])
        ql = label(r"a quarter", font_size=18, color=GREY_B).next_to(q, RIGHT, buff=0.15)
        pl = label(r"a pizza", font_size=18, color=LOST).next_to(pz, RIGHT, buff=0.15)
        rows = rows_of([
            (r"Rips, \ 1989: \ a round object 3 inches across is judged more \emph{similar} to a quarter, \ but more "
             r"likely to \emph{be} a pizza", WHITE),
            (r"quarters are made to one size; \ pizzas vary: \ what people know about how the kind comes about "
             r"overrides resemblance", MODEL),
            (r"Barsalou, \ 1983: \ \emph{things to take from a burning house} \ (children, \ pets, \ photographs, \ "
             r"papers) \ have typical members too, \ though they look nothing alike", CAT_A),
            (r"Murphy \& Medin, \ 1985: \ a category hangs together because a theory explains why its members "
             r"belong, \ and the theory decides which similarities count", PROTO),
        ], 6.4, 21, 0.3).move_to([3.0, -0.1, 0])
        tag = published_tag(r"Rips (1989); \ Barsalou (1983); \ Murphy \& Medin (1985)")
        with self.voiceover(
            "Prototypes, exemplars and spaces all build concepts out of similarity. Here is the trouble. "
            "<bookmark mark='a'/> Lance Rips told people about a round object, three inches across. Was it more "
            "similar to a quarter or to a pizza? A quarter. Was it more likely to be a quarter or a pizza? A pizza. "
            "<bookmark mark='b'/> Quarters are made to one exact size; pizzas come in many. What people know about "
            "how a kind comes to be overrides what it resembles. <bookmark mark='c'/> Lawrence Barsalou studied "
            "categories made up on the spot for a goal, like things to take from a burning house: children, pets, "
            "photographs, important papers. They look nothing alike, yet people agree on which are typical, by how "
            "well they serve the goal. <bookmark mark='d'/> Gregory Murphy and Douglas Medin drew the conclusion in "
            "1985. A category hangs together because some theory explains why its members belong, and it's the "
            "theory that decides which similarities count."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(obj), FadeIn(size), FadeIn(q), FadeIn(ql), FadeIn(pz), FadeIn(pl), FadeIn(rows[0]))
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def essences(self):
        head = heading(r"Psychological essentialism")
        left = VGroup(label(r"Keil, \ 1989: \ transformations", font_size=26, color=CAT_A),
                      rows_of([(r"a raccoon is dyed, \ shaved and given a sac of smelly liquid, \ until it looks and "
                                r"smells like a skunk", WHITE),
                               (r"kindergartners were often swayed by the new looks; \ by fourth grade, \ children "
                                r"said it is still a raccoon", MODEL),
                               (r"for artefacts, \ a coffeepot rebuilt into a bird feeder, \ children of every age "
                                r"accepted the change", GREY_A)], 5.6, 20, 0.28)
                      ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([-3.3, 0.6, 0])
        right = VGroup(label(r"Gelman \& Markman, \ 1986: \ induction", font_size=26, color=PROTO),
                       rows_of([(r"a flamingo feeds its baby mashed-up food; \ a bat feeds its baby milk; \ a "
                                 r"blackbird \ (which looks like the bat) \ is called a bird", WHITE),
                                (r"how does the blackbird feed its baby? \ four-year-olds mostly followed the name, "
                                 r"\ not the look", MODEL),
                                (r"a shared name says that kinds share hidden insides, \ and young children use it",
                                 GREY_A)], 5.6, 20, 0.28)
                       ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([3.3, 0.6, 0])
        rows = rows_of([
            (r"people treat natural kinds as having an essence they may not know but believe in: \ \emph{psychological "
             r"essentialism} \ (Medin \& Ortony, \ 1989)", MODEL),
        ], 12.4, 22, 0.3).to_edge(DOWN, buff=0.65)
        tag = published_tag(r"Keil (1989); \ Gelman \& Markman (1986); \ Medin \& Ortony (1989)")
        with self.voiceover(
            "Where do these theories come from? Children have them early. <bookmark mark='a'/> Frank Keil told "
            "children about a raccoon that doctors dyed, shaved and fitted with a sac of smelly liquid, until it "
            "looked and smelled just like a skunk. What is it now? Kindergartners were often swayed by the new looks. By "
            "fourth grade, children said it was still a raccoon, whatever it looked like. For an artefact, a coffeepot rebuilt into a bird feeder, "
            "children of every age accepted that it had become a bird feeder. <bookmark mark='b'/> Susan Gelman and "
            "Ellen Markman showed four-year-olds a flamingo that feeds its baby mashed-up food, a bat that feeds its "
            "baby milk, and a blackbird that looks like the bat but is called a bird. How does the blackbird feed its "
            "baby? Most children followed the name, not the look. <bookmark mark='c'/> Douglas Medin and Andrew "
            "Ortony called this psychological essentialism: people treat natural kinds as if they had a hidden "
            "essence, which they may not know, but believe is there. It is a theory, not a resemblance, and it "
            "appears in preschool."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(left))
            vo.wait_until("b")
            self.play(FadeIn(right))
            vo.wait_until("c")
            self.play(FadeIn(rows[0]))
        self.clear_scene()
