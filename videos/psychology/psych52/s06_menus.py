from __future__ import annotations

from videos.psychology.psych52.common import *  # noqa: F403


class Menus(VoiceoverScene):
    def construct(self):
        card_section(self, 5, r"Fitts and Hick in the interface", r"Where should a button go, \ and how many should "
                     r"a menu hold?")
        self.edges()
        self.depth()

    def edges(self):
        chips_section(self, r"Edges, \ corners and the mouse", [
            (r"infinite width", r"a target at the screen's edge cannot be overshot: \ the cursor stops there, \ so "
                                r"its effective width is huge", GOOD),
            (r"corners", r"two edges at once: \ the fastest places on a screen", MODEL),
            (r"pie menus", r"items around the cursor, \ all at the same short distance", PERSON),
            (r"touch", r"a fingertip is wide: \ targets need to be several millimetres across, \ whatever the law "
                       r"says about distance", AUTH),
        ], "Fitts's law tells you where to put things. <bookmark mark='a'/> A target at the edge of the screen can't "
           "be overshot. The cursor stops there, so its effective width is huge, and it's fast to hit. "
           "<bookmark mark='b'/> Corners are two edges at once, the fastest places on a screen. "
           "<bookmark mark='c'/> Pie menus put every item around the cursor, at the same short distance. "
           "<bookmark mark='d'/> And on touch screens, a fingertip is wide. Targets need to be several millimetres "
           "across, whatever the law says about distance.", chip_w=3.4, text_w=8.8)

    def depth(self):
        d = load("menus")
        head = heading(r"Sixty-four items: \ deep or broad?")
        A = axes([1.5, 70], [0, 10], x_length=5.6, y_length=3.0, xticks=[2, 8, 16, 32, 64], yticks=[0, 5, 10],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f} s", xlabel=r"items per menu",
                 ylabel=r"time to select", center=[-3.3, 0.3, 0], font_size=12)
        cp = curve(A.ax, d["breadth"], d["practised"], GOOD, stroke_width=4)
        cu = curve(A.ax, d["breadth"], d["unpractised"], AUTH, stroke_width=4)
        key = VGroup(label(r"practised: \ Hick", font_size=13, color=GOOD),
                     label(r"unfamiliar: \ scanning", font_size=13, color=AUTH)).arrange(RIGHT, buff=0.4)
        key.next_to(A, UP, buff=0.2)
        k = int(np.argmin(d["unpractised"]))
        rows = rows_of([
            (r"64 commands: \ six levels of 2, \ three of 4, \ two of 8, \ or one menu of 64", WHITE),
            (r"for a practised user each level costs a Hick choice and a point: \ broad wins, \ and one menu of 64 is "
             r"fastest", GOOD),
            (rf"for an unfamiliar menu the user scans item by item: \ the choice grows linearly, \ and about "
             rf"{int(d['breadth'][k])} items per level is best", AUTH),
            (r"so Hick's law applies only when the user knows what is where; \ otherwise it is visual search (Part 18)",
             YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{work.menu\_time}, \ illustrative constants")
        with self.voiceover(
            "How many items should a menu hold? <bookmark mark='a'/> Take sixty-four commands. They could be six "
            "levels of two, three of four, two of eight, or one menu of sixty-four. <bookmark mark='b'/> For a "
            "practised user, each level costs a Hick choice and a point. Broad wins, and one menu of sixty-four is "
            "fastest. <bookmark mark='c'/> But for an unfamiliar menu, the user scans item by item. The choice grows "
            "linearly, and about eight items per level is best. <bookmark mark='d'/> So Hick's law applies only when "
            "the user knows what's where. Otherwise it's Part 18's visual search."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(cp))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), Create(cu))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
