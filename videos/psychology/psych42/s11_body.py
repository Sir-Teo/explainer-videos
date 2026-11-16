from __future__ import annotations

from videos.psychology.psych42.common import *  # noqa: F403


class Body(VoiceoverScene):
    def construct(self):
        self.card()
        self.lobotomy()
        self.ect()

    def card(self):
        card = chapter_card(10, r"The body treatments", r"A Nobel Prize, \ and a treatment rehabilitated",
                            lit={1938: r"Cerletti \& Bini", 1949: r"Moniz"}, part=PART, scale=("brain", "person"),
                            marr=("what",))
        with self.voiceover("Chapter ten. The body treatments."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def lobotomy(self):
        head = heading(r"A Nobel Prize")
        steps = VGroup()
        for yr, txt, c in (
                (r"1935", r"Moniz in Lisbon cuts connections to the frontal lobes of psychiatric patients: \ "
                          r"prefrontal leucotomy", SYMP),
                (r"1949", r"Moniz receives the Nobel Prize in medicine for it", PERSON),
                (r"1940s--50s", r"in the US, \ Walter Freeman's quick ``transorbital'' version, \ done in offices; \ "
                                r"tens of thousands of operations", AUTH),
                (r"1950s", r"chlorpromazine (Part 41) and growing evidence of harm end it", GOOD)):
            steps.add(VGroup(word_chip(yr, color=c, font_size=18, width=2.0), wrapped_label(txt, 9.6, 20, WHITE))
                      .arrange(RIGHT, buff=0.35))
        steps.arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to([0, 0.2, 0])
        foot = wrapped_label(r"judged by clinicians' impressions, \ with no controls: \ a treatment that blunted "
                             r"people was counted as calming them", 12.0, 20, YOU).move_to([0, -2.6, 0])
        tag = historical_tag(r"Moniz (1936)")
        with self.voiceover(
            "The body treatments have a darker history. <bookmark mark='a'/> In 1935 the neurologist Egas Moniz in "
            "Lisbon began cutting connections to the frontal lobes of psychiatric patients. <bookmark mark='b'/> In "
            "1949 he received the Nobel Prize in medicine for it. <bookmark mark='c'/> In the United States, Walter "
            "Freeman spread a quick version done through the eye socket, sometimes in an office, and tens of "
            "thousands of operations followed. <bookmark mark='d'/> Chlorpromazine, from Part 41, and growing "
            "evidence of harm ended it. <bookmark mark='e'/> It was judged by clinicians' impressions, with no "
            "controls. A treatment that blunted people was counted as calming them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, s in zip("abcd", steps):
                vo.wait_until(m)
                self.play(FadeIn(s, shift=RIGHT * 0.15))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def ect(self):
        head = heading(r"ECT, \ then and now")
        rows = rows_of([
            (r"1938: \ Cerletti and Bini in Rome induce a seizure with an electric current to treat psychosis", WHITE),
            (r"early ECT was given without anaesthesia, \ sometimes as punishment, \ and its image never recovered", AUTH),
            (r"modern ECT is given under general anaesthesia with a muscle relaxant; \ for severe depression it beats "
             r"simulated ECT, \ in which only the anaesthetic is given", GOOD),
            (r"its cost is memory loss, \ mostly around the treatment period; \ it is a choice for severe illness "
             r"that has not responded to other treatment", YOU),
        ], 12.4, 23, 0.46).move_to([0, -0.3, 0])
        tag = historical_tag(r"Cerletti \& Bini (1938)")
        with self.voiceover(
            "Electroconvulsive therapy went the other way. <bookmark mark='a'/> In 1938 Ugo Cerletti and Lucio Bini in "
            "Rome induced a seizure with an electric current to treat psychosis. <bookmark mark='b'/> Early ECT was "
            "given without anaesthesia, sometimes as punishment, and its image never recovered. "
            "<bookmark mark='c'/> Modern ECT is given under general anaesthesia with a muscle relaxant. For severe "
            "depression it does better than simulated ECT, in which only the anaesthetic is given. "
            "<bookmark mark='d'/> Its cost is memory loss, mostly around the treatment period. It's a choice for "
            "severe illness that hasn't responded to other treatment."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
