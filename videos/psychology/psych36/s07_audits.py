from __future__ import annotations

from videos.psychology.psych36.common import *  # noqa: F403


def resume(name: str, color) -> VGroup:
    page = RoundedRectangle(corner_radius=0.05, width=1.7, height=2.2, stroke_color=color, fill_color="#14181F",
                            fill_opacity=1)
    lines = VGroup(*[Line(LEFT * 0.6, RIGHT * (0.6 - 0.25 * (k % 3)), color=GREY_D, stroke_width=3)
                     for k in range(6)]).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
    lines.move_to(page.get_center() + DOWN * 0.25)
    nm = label(name, font_size=17, color=color).move_to(page.get_top() + DOWN * 0.3)
    return VGroup(page, lines, nm)


class Audits(VoiceoverScene):
    def construct(self):
        self.card()
        self.names()
        self.thirty_years()
        self.power()

    def card(self):
        card = chapter_card(6, r"Measuring by behaviour", r"Do identical applications get identical answers?",
                            lit={2004: r"Bertrand \& Mullainathan", 2017: r"Quillian et al."}, part=PART,
                            scale=("group", "society"), marr=("what",))
        with self.voiceover("Chapter six. Measuring by behaviour."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def names(self):
        head = heading(r"Emily and Greg, \ Lakisha and Jamal")
        a = resume(r"Emily", IN).move_to([-4.8, 0.8, 0])
        b = resume(r"Lakisha", OUTG).move_to([-2.4, 0.8, 0])
        eq = label(r"$=$", font_size=36, color=GREY_A).move_to([-3.6, 0.8, 0])
        stat = VGroup(label(r"about 1 callback per 10 r\'esum\'es", font_size=17, color=IN),
                      label(r"about 1 per 15", font_size=17, color=OUTG)).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        stat.move_to([-3.6, -1.3, 0])
        rows = rows_of([
            (r"Bertrand and Mullainathan, \ 2004: \ fictitious r\'esum\'es sent to help-wanted ads in Boston and "
             r"Chicago newspapers, \ each given at random a name that sounds white or one that sounds Black", WHITE),
            (r"white-sounding names got 50\% more callbacks: \ about one for every ten r\'esum\'es sent, \ against "
             r"one for every fifteen", AUTH),
            (r"better r\'esum\'es helped white-sounding names more", CROWD),
            (r"random assignment makes this a measurement of behaviour, \ not of attitudes: \ the same paper, \ a "
             r"different name, \ a different answer", YOU),
        ], 6.4, 20, 0.36).move_to([3.0, -0.2, 0])
        tag = published_tag(r"Bertrand \& Mullainathan (2004)")
        with self.voiceover(
            "The most direct measure of discrimination doesn't ask anything, or time anything. It watches what "
            "people do. <bookmark mark='a'/> In 2004 Marianne Bertrand and Sendhil Mullainathan sent fictitious "
            "résumés to help-wanted ads in Boston and Chicago newspapers. Each résumé was given at random a name "
            "that sounded white, like Emily or Greg, or one that sounded Black, like Lakisha or Jamal. "
            "<bookmark mark='b'/> White-sounding names got fifty percent more callbacks: about one for every ten "
            "résumés sent, against one for every fifteen. <bookmark mark='c'/> And better résumés helped the "
            "white-sounding names more. <bookmark mark='d'/> Random assignment makes this a measurement of "
            "behaviour, not of attitudes. The same paper, a different name, a different answer."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(a), FadeIn(b), FadeIn(eq))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(stat), FadeIn(rows[1]))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def thirty_years(self):
        head = heading(r"Twenty-five years of audits")
        A = axes([1988, 2016], [0, 2.0], x_length=5.4, y_length=3.4, xticks=[1990, 2000, 2010], yticks=[1.0, 1.5, 2.0],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}", ylabel=r"callbacks, \ white / Black",
                 center=[-3.3, -0.3, 0], font_size=15)
        one = DashedLine(A.ax.c2p(1988, 1.0), A.ax.c2p(2016, 1.0), color=GREY_B)
        flat = Line(A.ax.c2p(1989, 1.36), A.ax.c2p(2015, 1.36), color=AUTH, stroke_width=4)
        fl = label(r"about 1.36, \ no trend", font_size=16, color=AUTH).next_to(flat, UP, buff=0.12)
        note = label(r"the average and its trend, \ drawn schematically", font_size=14, color=GREY_B).next_to(
            A, DOWN, buff=0.4)
        rows = rows_of([
            (r"Quillian, \ Pager, \ Hexel and Midtb\o en, \ 2017: \ every available US field experiment of hiring "
             r"discrimination from 1989 to 2015, \ 28 studies, \ 55{,}842 applications", WHITE),
            (r"white applicants received on average 36\% more callbacks than equally qualified African Americans, \ "
             r"and 24\% more than Latinos", AUTH),
            (r"against African Americans, \ no change over the 25 years; \ against Latinos, \ some sign of a decline",
             CROWD),
            (r"expressed prejudice fell steeply over the same years; \ discrimination measured by behaviour did not",
             YOU),
        ], 6.0, 20, 0.36).move_to([3.4, -0.3, 0])
        tag = published_tag(r"Quillian et al.\ (2017)")
        with self.voiceover(
            "Has it changed? <bookmark mark='a'/> In 2017 Lincoln Quillian, Devah Pager and colleagues gathered "
            "every available American field experiment of hiring discrimination from 1989 to 2015: twenty-eight "
            "studies, nearly fifty-six thousand applications. <bookmark mark='b'/> White applicants received on "
            "average thirty-six percent more callbacks than equally qualified African Americans, and twenty-four "
            "percent more than Latinos. <bookmark mark='c'/> Against African Americans there was no change over "
            "the twenty-five years. Against Latinos, some sign of a decline. <bookmark mark='d'/> Expressed "
            "prejudice fell steeply over the same years. Discrimination measured by behaviour did not."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), Create(one), FadeIn(note))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(flat), FadeIn(fl), FadeIn(rows[1]))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def power(self):
        d = load("audit")
        head = heading(r"How many applications does an audit need?")
        A = axes([0, 3300], [0, 1.0], x_length=5.4, y_length=3.4, xticks=[0, 1000, 2000, 3000], yticks=[0, 0.5, 0.8, 1],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}", xlabel=r"applications per name group",
                 ylabel=r"power", center=[-3.3, -0.3, 0], font_size=15)
        c = curve(A.ax, d["ns"], d["power"], MODEL, smooth=True)
        line80 = DashedLine(A.ax.c2p(0, 0.8), A.ax.c2p(3300, 0.8), color=GREY_B)
        n80 = DashedLine(A.ax.c2p(d["n80"], 0), A.ax.c2p(d["n80"], 0.8), color=GOOD)
        l80 = label(rf"about {num(d['n80'])}", font_size=16, color=GOOD).next_to(A.ax.c2p(d["n80"], 0), UP,
                                                                                 buff=0.1).shift(RIGHT * 0.6)
        rows = rows_of([
            (r"suppose callbacks run at 9.6\% for one name group and 6.4\% for the other: \ a 50\% gap, \ "
             r"illustrative numbers", WHITE),
            (rf"to detect it 80\% of the time at the 5\% level takes about {num(d['n80'])} applications per group",
             MODEL),
            (r"a gap that matters to thousands of applicants is invisible in a sample of a hundred: \ which is why "
             r"single anecdotes, \ either way, \ settle nothing", AUTH),
            (r"and why audits pool: \ Part 4's power, \ applied to a social question", YOU),
        ], 6.0, 20, 0.36).move_to([3.4, -0.3, 0])
        tag = psyche_tag(r"computed: \ two-proportion power")
        with self.voiceover(
            "Why so many applications? <bookmark mark='a'/> Suppose callbacks run at nine point six percent for one "
            "name group and six point four for the other, a fifty percent gap. These are illustrative numbers. "
            "<bookmark mark='b'/> To detect that gap eighty percent of the time takes about "
            f"{d['n80']:,} applications per group. <bookmark mark='c'/> A gap that matters to thousands of "
            "applicants is invisible in a sample of a hundred, which is why single anecdotes, either way, settle "
            "nothing. <bookmark mark='d'/> And it's why audit studies pool. It's Part 4's power, applied to a social "
            "question."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(c), Create(line80), Create(n80), FadeIn(l80), FadeIn(rows[1]))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
