from __future__ import annotations

from videos.psychology.psych46.common import *  # noqa: F403


class Quality(VoiceoverScene):
    def construct(self):
        self.card()
        self.straight()
        self.checks()
        self.howmany()

    def card(self):
        card = chapter_card(11, r"Data quality online", r"Who is answering, \ and are they reading?", lit=(),
                            part=PART, scale=("person",), marr=("what",))
        with self.voiceover("Chapter eleven. Data quality online."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def straight(self):
        d = load("careless")
        head = heading(r"Careless answers make scales look better")
        A = axes([0, 0.32], [0, 1], x_length=5.6, y_length=3.2, xticks=[0, 0.1, 0.2, 0.3], yticks=[0, 0.25, 0.5, 0.75, 1],
                 xfmt=lambda v: f"{100 * v:.0f}\\%", yfmt=lambda v: f"{v:g}", xlabel=r"share straightlining",
                 center=[-3.3, 0.3, 0], font_size=13)
        ca = curve(A.ax, d["shares"], d["alpha"], GOOD, stroke_width=4)
        cr = curve(A.ax, d["shares"], d["r"], AUTH, stroke_width=4)
        key = VGroup(label(r"alpha of one scale", font_size=13, color=GOOD),
                     label(r"correlation between two scales", font_size=13, color=AUTH)).arrange(RIGHT, buff=0.4)
        key.next_to(A, UP, buff=0.05)
        rows = rows_of([
            (r"Psyche: \ two six-item scales whose traits correlate 0.3; \ some respondents give the same answer to "
             r"every item of the grid", WHITE),
            (rf"alpha rises from {d['alpha'][0]:.2f} to {d['alpha'][-1]:.2f} as straightliners reach 30\%: \ the scale "
             rf"looks more reliable", GOOD),
            (rf"the correlation between the scales rises from {d['r'][0]:.2f} to {d['r'][-1]:.2f}: \ a relation "
             rf"created by not reading", AUTH),
            (r"careless answers are not noise that weakens results; \ they can manufacture them", YOU),
        ], 6.0, 19, 0.38).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{scaling.straightline}, \ 5{,}000 simulated people")
        with self.voiceover(
            "Online panels made surveys cheap, and raised a question: who is answering, and are they reading? "
            "<bookmark mark='a'/> Psyche makes two six-item scales whose traits correlate zero point three, and lets "
            "some respondents give the same answer to every item in the grid. <bookmark mark='b'/> As the "
            "straightliners reach thirty percent, alpha rises from zero point seven five to above zero point nine. "
            "The scale looks more reliable. <bookmark mark='c'/> And the correlation between the scales rises from "
            "zero point two four to zero point seven five: a relation created by not reading. "
            "<bookmark mark='d'/> Careless answers aren't noise that weakens results. They can manufacture them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(ca))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), Create(cr))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def checks(self):
        head = heading(r"Finding the careless")
        data = (
            (r"attention checks", r"``select disagree for this item'': \ catches some, \ annoys others, \ and can "
                                  r"make attentive people answer differently afterwards", PERSON),
            (r"response times", r"impossibly fast pages; \ the cheapest flag", MODEL),
            (r"consistency", r"the same question asked twice, \ or a reversed item answered the same way as its twin",
             SYMP),
            (r"bots and fraud", r"duplicate answers, \ copied open text, \ impossible combinations; \ now harder, \ "
                                r"as language models can write plausible answers", AUTH),
            (r"rule", r"decide the exclusions before looking at the results (Part 43), \ and report how many", GOOD),
        )
        rows = VGroup()
        for name, how, c in data:
            rows.add(VGroup(word_chip(name, color=c, font_size=17, width=3.2), wrapped_label(how, 9.0, 19, WHITE))
                     .arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([0, -0.3, 0])
        with self.voiceover(
            "So how are careless respondents found? <bookmark mark='a'/> Attention checks, such as select disagree "
            "for this item. They catch some, annoy others, and can make attentive people answer differently "
            "afterwards. <bookmark mark='b'/> Response times: impossibly fast pages are the cheapest flag. "
            "<bookmark mark='c'/> Consistency: the same question asked twice, or a reversed item answered the same "
            "way as its twin. <bookmark mark='d'/> Bots and fraud: duplicate answers, copied text, impossible "
            "combinations. It's harder now that language models can write plausible answers. "
            "<bookmark mark='e'/> And one rule: decide the exclusions before looking at the results, as in Part 43, "
            "and report how many."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def howmany(self):
        d = load("checks")
        head = heading(r"How many checks?")
        A = axes([0.3, 5.7], [0, 1.05], x_length=5.6, y_length=3.0, xticks=[1, 2, 3, 4, 5], yticks=[0, 0.5, 1],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{100 * v:.0f}\\%", xlabel=r"attention checks, \ fail any to be excluded",
                 ylabel=r"", center=[-3.3, 0.3, 0], font_size=13)
        cc = curve(A.ax, d["k"], d["caught"], GOOD, stroke_width=4)
        cw = curve(A.ax, d["k"], d["wrong"], AUTH, stroke_width=4)
        key = VGroup(label(r"random responders caught", font_size=13, color=GOOD),
                     label(r"attentive people excluded", font_size=13, color=AUTH)).arrange(RIGHT, buff=0.4)
        key.next_to(A, UP, buff=0.3)
        rows = rows_of([
            (r"a check on a five-point item: \ a random responder passes by luck one time in five; \ say an attentive "
             r"person slips one time in fifty", WHITE),
            (rf"one check catches {100 * d['caught'][0]:.0f}\% of random responders; \ three catch "
             rf"{100 * d['caught'][2]:.1f}\%", GOOD),
            (rf"but five checks exclude {100 * d['wrong'][-1]:.0f}\% of attentive people, \ and those who slip are not "
             rf"a random tenth (Part 43's exclusion rule)", AUTH),
            (r"two or three checks, \ fixed in advance; \ and a straightliner who always picks the instructed answer "
             r"passes every one", YOU),
        ], 6.0, 19, 0.38).move_to([3.4, -0.1, 0])
        tag = label(r"computed: \ $1 - 0.2^k$ and $1 - 0.98^k$", font_size=16, color=GREY_B).to_corner(DR, buff=0.3)
        with self.voiceover(
            "How many checks? <bookmark mark='a'/> On a five-point item, a random responder passes a check by luck "
            "one time in five. Say an attentive person slips one time in fifty. <bookmark mark='b'/> One check "
            "catches four random responders in five. Three catch over ninety-nine percent. <bookmark mark='c'/> But "
            "five checks exclude nearly a tenth of attentive people, and those who slip aren't a random tenth. "
            "<bookmark mark='d'/> Two or three checks, fixed in advance, is the usual answer. And note that a "
            "straightliner who happens to always pick the instructed answer passes every one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(cc))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), Create(cw))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
