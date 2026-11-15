from __future__ import annotations

from videos.psychology.psych18.common import *  # noqa: F403


class Search(VoiceoverScene):
    def construct(self):
        self.card()
        self.on_you()
        self.slopes()

    def card(self):
        card = chapter_card(4, r"Searching", r"Why does a red item pop out, \ and a red vertical one not?",
                            lit={1980: r"Treisman \& Gelade"}, part=PART, scale=("mind",), marr=("what", "how"))
        with self.voiceover("Chapter four. Searching."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def on_you(self):
        d = load("search")
        head = heading(r"On you: \ find the target")
        fbox = Square(3.9, color=GREY_D, stroke_width=2).move_to([-3.4, 0.9, 0])
        cbox = Square(3.9, color=GREY_D, stroke_width=2).move_to([3.4, 0.9, 0])
        fd = search_glyphs(d["feature_display"], fbox.get_center(), 3.6)
        cd = search_glyphs(d["conjunction_display"], cbox.get_center(), 3.6)
        fl = label(r"find the red bar", font_size=24, color=TARGET).next_to(fbox, UP, buff=0.15)
        cl = label(r"find the red vertical bar", font_size=24, color=TARGET).next_to(cbox, UP, buff=0.15)
        fr = Circle(0.3, color=ATT, stroke_width=4).move_to(fd[int(d["feature_target"])])
        cr = Circle(0.3, color=ATT, stroke_width=4).move_to(cd[int(d["conjunction_target"])])
        rows = rows_of([
            (r"left: \ the target differs in one feature, \ colour; \ it seems to find you", TARGET),
            (r"right: \ it differs only in a combination; \ red bars and vertical bars are everywhere", ATT),
            (r"the interactive on the course site times you on both, \ at four set sizes", YOU),
        ], 12.4, 26, 0.26).to_edge(DOWN, buff=0.75)
        with self.voiceover(
            "Try this. <bookmark mark='a'/> On the left, find the red bar. <bookmark mark='b'/> There it is; it "
            "seemed to find you, rather than the other way round. <bookmark mark='c'/> Now, on the right, find the "
            "red vertical bar. Take a moment. <bookmark mark='d'/> Here. That took longer, and it probably felt "
            "different: you had to look around. On the left the target differed from everything else in one feature, "
            "its colour. On the right, there are red bars and vertical bars everywhere, and the target is the only "
            "item with both. <bookmark mark='e'/> The interactive for this part times you on both kinds of search, "
            "with four, eight, sixteen and thirty-two items, and plots your own set-size functions."
        ) as vo:
            self.play(FadeIn(head), FadeIn(fbox), FadeIn(cbox))
            vo.wait_until("a")
            self.play(FadeIn(fd), FadeIn(fl))
            vo.wait_until("b")
            self.play(Create(fr), FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(cd), FadeIn(cl))
            vo.wait_until("d")
            self.play(Create(cr), FadeIn(rows[1]))
            vo.wait_until("e")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def slopes(self):
        d = load("search")
        tg = archive.TREISMAN_GELADE_1980.data
        head = heading(r"Set-size functions")
        ss = d["set_sizes"]
        panels = VGroup()
        for k, (kind, title, col) in enumerate([("feature", r"a feature: \ red among green", TARGET),
                                                ("conjunction", r"a conjunction: \ red and vertical", ATT)]):
            A = axes([0, 34], [400, 1800], x_length=4.6, y_length=3.0, xticks=[4, 8, 16, 32],
                     yticks=[500, 1100, 1700], xlabel=r"items in the display", ylabel=r"RT, \ ms" if k == 0 else "",
                     center=[-3.5 + 6.2 * k, 0.72, 0], font_size=17)
            ax = A.ax
            cp = VGroup(curve(ax, ss, d[f"{kind}_present"], col, 4), scatter(ax, ss, d[f"{kind}_present"], col, 0.07, 1))
            ca = VGroup(DashedVMobject(curve(ax, ss, d[f"{kind}_absent"], col, 3), num_dashes=24),
                        scatter(ax, ss, d[f"{kind}_absent"], col, 0.07, 1))
            sl = d[f"{kind}_slopes"]
            t = label(title, font_size=21, color=col).next_to(ax, UP, buff=0.35)
            note = label(rf"slopes: \ {sl[0]:.0f} \ and \ {sl[1]:.0f} ms an item", font_size=19, color=col)
            note.next_to(A, DOWN, buff=0.12)
            panels.add(VGroup(A, t, cp, ca, note))
        key = legend([(WHITE, r"solid: \ target present"), (GREY_B, r"dashed: \ target absent")], font_size=18)
        key.arrange(RIGHT, buff=0.6).move_to([0, -1.74, 0])
        rows = rows_of([
            (r"feature search is flat: \ the target pops out at any set size", TARGET),
            (r"conjunction search climbs with every item, \ and absent trials climb about twice as fast", ATT),
            (rf"Treisman and Gelade, \ 1980: \ about {tg['conjunction_present_ms_per_item']} ms an item present, \ "
             rf"{tg['conjunction_absent_ms_per_item']} absent", DATA),
        ], 12.4, 23, 0.14).to_edge(DOWN, buff=0.72)
        ptag = psyche_tag(r"\texttt{attention.search\_slopes}: \ 400 trials a point")
        tag = published_tag(archive.TREISMAN_GELADE_1980.cite)
        with self.voiceover(
            "Time those searches and vary the number of items, and you get set-size functions. "
            "<bookmark mark='a'/> For a feature search, the time to find the target is the same with four items or "
            "thirty-two. The line is flat, and when no target is there, people say so just as fast. "
            "<bookmark mark='b'/> For a conjunction search, every item adds time. When the target is present, people "
            "find it on average halfway through, so absent trials, which need a check of everything, rise about twice "
            "as steeply. <bookmark mark='c'/> In Anne Treisman and Garry Gelade's experiments in 1980, conjunction "
            "searches cost around thirty milliseconds an item when the target was present and around sixty-five when "
            "it was absent: the two-to-one ratio of a search that checks one item at a time and stops when it finds "
            "the target. Psyche's version of these searches, built in the next chapter, is shallower, and the next "
            "chapter explains why."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(ptag), *[FadeIn(p[0]) for p in panels],
                      *[FadeIn(p[1]) for p in panels], FadeIn(key))
            vo.wait_until("a")
            self.play(Create(panels[0][2]), Create(panels[0][3]), FadeIn(panels[0][4]), FadeIn(rows[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(panels[1][2]), Create(panels[1][3]), FadeIn(panels[1][4]), FadeIn(rows[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()
