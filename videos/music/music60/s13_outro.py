from __future__ import annotations

from videos.music.music60.common import *  # noqa: F403
from videos.music.variations import rows_before


class Outro(SoundScene):
    def construct(self):
        self.variation()
        self.statement()
        self.ledger()
        self.recap()
        self.problems()
        self.payoffs()
        self.next_part()

    # ------------------------------------------------------------------
    def variation(self):
        d = load("tune60")
        c = clip("tune.variation60")
        st = d["starts"]
        keys = d["names"]
        names = {"original": (r"our recording", TUNE), "cover": (r"a quartet's cover", BLUE), "remix": (r"a remix that samples it", EAR)}
        head = VGroup(label(r"Variation 60", font_size=48, color=TUNE), label(r"the Tune's family of copyrights", font_size=30, color=GREY_A)).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).to_edge(UP, buff=0.3)
        cells = VGroup(*[VGroup(RoundedRectangle(width=3.4, height=1.2, corner_radius=0.12, stroke_color=names[k][1]),
                                label(names[k][0], font_size=18, color=names[k][1])).arrange(ORIGIN) for k in keys]).arrange(RIGHT, buff=0.35).move_to(DOWN * 0.2)
        note = label(r"one public-domain melody of 1761; \ three recordings, \ each a new work with its own owners", font_size=17, color=GREY_A).next_to(cells, DOWN, buff=0.45)
        with self.voiceover(
            "Every part ends by doing something to the Tune with what it built. <bookmark mark='a'/> Here is its family of "
            "copyrights: our session's recording; a string quartet's cover; and a remix that samples our recording under a new "
            "beat. One melody, free since long before copyright; three recordings, each a new work with its own owners."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(cells), FadeIn(note))
        with self.listen(c) as snd:
            window(snd, r"Variation 60", kind="physical model", detail=r"our session, \ a quartet, \ a remix", corner=DL, tag_corner=DR)
            for i, k in enumerate(keys):
                end = st[keys[i + 1]] - 0.3 if i + 1 < len(keys) else c.duration
                pulse(snd, cells[i], st[k], end, buff=0.06)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def statement(self):
        d = load("tune60")
        rows = d["rows"]
        g = VGroup()
        for k, n, col, us in (("original", r"our recording", TUNE, r"all of it: \ we own the recording and the arrangement"),
                              ("cover", r"the quartet's cover", BLUE, r"nothing: \ the melody is free, \ the recording theirs"),
                              ("remix", r"the remix", EAR, r"half, \ by an illustrative sample agreement")):
            r = rows[k]
            g.add(VGroup(label(n, font_size=19, color=col), label(rf"\${r['recording']:,.0f} \ + \ \${r['composition']:,.0f}", font_size=18, color=WHITE),
                         label(rf"\${r['to_us']:,.0f}", font_size=18, color=col), label(us, font_size=14, color=GREY_A)))
        g.arrange(DOWN, buff=0.5)
        for r in g:
            r[0].set_x(-4.8)
            r[1].set_x(-1.4)
            r[2].set_x(1.3)
            r[3].set_x(4.3)
        top = VGroup(*[label(t, font_size=15, color=GREY_A).move_to([x, g.get_top()[1] + 0.45, 0]) for t, x in
                       ((r"recording \ + \ composition", -1.4), (r"to us", 1.3))])
        note = label(rf"a million streams each, \ \${d['per_million']:,.0f} to rights holders; \ to the melody's unknown composer of 1761: \ nothing",
                     font_size=17, color=TUNE).to_edge(DOWN, buff=0.45)
        head = label(r"the statement, \ after a million streams each \ (illustrative)", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "And here is each version's statement after a million simulated streams, at our service's rate. "
            f"<bookmark mark='a'/> Each pays its rights holders about {say(d['per_million'])} dollars, four fifths to the recording, "
            "one fifth to the composition. <bookmark mark='b'/> Our recording pays us all of it, as owners of the recording and "
            "the arrangement. <bookmark mark='c'/> The quartet's cover pays us nothing: the melody is free, and the recording is "
            "theirs. <bookmark mark='d'/> The remix pays us half, under an illustrative sample agreement. And the composer of the "
            "melody that all three are built on, unknown since 1761, is paid nothing at all."
        ) as vo:
            self.play(FadeIn(head), FadeIn(top), FadeIn(VGroup(*[r[0] for r in g])))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*[r[1] for r in g])))
            for mark, r in zip("bcd", g):
                vo.wait_until(mark)
                self.play(FadeIn(VGroup(r[2], r[3])))
            self.play(FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ledger(self):
        v = load("variation")
        rws = (rows_before(PART) + [{"part": v["part"], "title": v["title"], "seconds": v["seconds"], "measure": v["measure"]}])[-6:]
        led = variations_ledger(rws, highlight=(len(rws) - 1,)).move_to(DOWN * 0.2)
        head = label(r"the Variations ledger", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Row sixty of the ledger, the last of Act Ten: the Tune's family of copyrights, and what a million streams of each "
            "would pay. The ledger itself has been an account all along: of what was done to one melody, and what it cost."
        ):
            self.play(FadeIn(head), FadeIn(led, shift=UP * 0.2))
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recap(self):
        card = objectives_card([
            r"a song is two works: \ the composition and the recording, \ with their own owners and terms",
            r"four licences, \ and collecting societies because nobody could ask everyone",
            r"a stream pays about half a cent to all its rights holders; \ an advance is repaid from royalties",
            r"pro rata, \ heavy listeners and bots decide where light listeners' money goes",
            r"social influence makes hits bigger and less predictable; \ the cost disease raises ticket prices",
            r"melodies are fewer than they look: \ shared phrases are common, \ by chance",
        ], title=r"What we found", font_size=20).move_to(DOWN * 0.1)
        with self.voiceover(
            "What did we find? A song is two works, the composition and the recording, with their own owners and terms. "
            "<bookmark mark='a'/> There are four main licences, and collecting societies exist because nobody could ask "
            "everyone. <bookmark mark='b'/> A stream pays about half a cent to all its rights holders together, and an advance is "
            "repaid out of the artist's royalties. <bookmark mark='c'/> Divided pro rata, heavy listeners and bots decide where "
            "light listeners' money goes. <bookmark mark='d'/> Social influence makes hits bigger and less predictable, and the "
            "cost disease raises the price of a concert. <bookmark mark='e'/> And melodies are fewer than they look: shared "
            "phrases are common, by chance alone."
        ) as vo:
            self.play(FadeIn(card.head), FadeIn(card.rows[0]))
            for mark, rr in zip("abcde", card.rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(rr), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def problems(self):
        ps = problem_set([
            r"A service pays rights holders 0.47 cents a stream; \ the label's royalty is 18\% of 55/70 of it. \ How many streams repay a \$150,000 account?",
            r"Show that under user-centric division no account can be paid more in all than its owner's own fee.",
            r"\textbf{Ear.} \ The lab plays melodies from Part 14's model in pairs; \ say which pairs share an opening, \ then check.",
            r"\textbf{Build.} \ Add a fourth social world with a ranking that ignores downloads; \ measure its Gini and unpredictability.",
            r"$\bigstar$ \ Can a model give a court a calibrated probability that a shared phrase arose by chance?",
        ], font_size=21)
        with self.voiceover(
            "Five problems. One to compute, one to prove, one for your ears, one to build, and a research problem, marked "
            "with a star. Solutions are in this part's notes. Pause here."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.25), run_time=3.0)
        self.wait(5.0)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoffs(self):
        pay = payoff_card([
            (r"finding music: \ recommendation as a social-influence world", [63]),
            (r"machines that compose: \ memorization and plagiarism tests", [65]),
            (r"generative audio: \ voices, \ training data and rights", [66]),
            (r"research: \ measuring fairness, \ and listening tests", [67]),
            (r"the series' own Variations, \ performed", [68]),
        ], font_size=25)
        with self.voiceover(
            "Where does this come back? In finding music, where recommendation is a social-influence world. In machines that "
            "compose, with tests for memorization and plagiarism. In generative audio, with voices, training data and rights. In "
            "research, measuring fairness. And in the series' own Variations, performed at the end."
        ):
            self.play(FadeIn(pay.head), LaggedStart(*[FadeIn(r) for r in pay.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        prac = practice_card([
            (r"register", r"every song with a society and a publisher or administrator; \ credits complete"),
            (r"read", r"what is recoupable, \ for how long the label owns the masters, \ what reverts"),
            (r"clear", r"every sample, \ both licences, \ before release"),
            (r"keep", r"dated drafts and session files: \ evidence of independent creation"),
        ], font_size=25)
        with self.voiceover(
            "And in practice, for anyone who writes or records. Register every song, with complete credits. Read what is "
            "recoupable, how long the label owns the masters, and what reverts. Clear every sample, both licences, before release. "
            "And keep dated drafts and session files, the evidence of independent creation."
        ):
            self.play(FadeIn(prac.head), LaggedStart(*[FadeIn(r) for r in prac.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        refs = reference_card(
            [r"D. S. Passman, \ \textit{All You Need to Know About the Music Business} \ (11th ed., \ 2023)",
             r"A. B. Krueger, \ \textit{Rockonomics} \ (2019)",
             r"W. J. Baumol and W. G. Bowen, \ \textit{Performing Arts: \ The Economic Dilemma} \ (1966)",
             r"D. Hesmondhalgh, \ `Is music streaming bad for musicians?' \ (2021)"],
            [r"S. Rosen, \ `The economics of superstars' \ (American Economic Review, \ 1981)",
             r"M. J. Salganik, \ P. S. Dodds and D. J. Watts, \ `Experimental study of inequality and unpredictability in an artificial cultural market' \ (Science, \ 2006)",
             r"A. B. Krueger, \ `The economics of real superstars' \ (J. Labor Economics, \ 2005)",
             r"H. Léveillé Gauvin, \ `Drawing listener attention in popular music' \ (Musicae Scientiae, \ 2018)"],
            font_size=18)
        with self.voiceover("The books and papers this part follows. The full list, with notes, is in the README."):
            self.play(FadeIn(refs))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_part(self):
        top = label(r"Act XI: \ listening machines", font_size=30, color=GREY_A).to_edge(UP, buff=0.8)
        lead = label(r"1975: \ a program at Stanford writes down a duet it has heard, \ if its two voices keep out of each other's way.", font_size=23, color=WHITE).move_to(UP * 1.7)
        q = label(r"can a machine hear a recording and write down its notes?", font_size=28, color=EAR).move_to(UP * 0.4)
        nxt = VGroup(label(r"Part 61", font_size=32, color=GREY_B), label(r"Pitch, \ Onsets and Transcription", font_size=46, color=TUNE)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Act Eleven turns the chain around. 1975: a program at Stanford writes down a duet it has heard, as long as its two "
            "voices keep out of each other's way. <bookmark mark='a'/> Can a machine hear a recording and write down its notes? "
            "<bookmark mark='b'/> Next time. Part 61: Pitch, Onsets and Transcription."
        ) as vo:
            self.play(FadeIn(top), FadeIn(lead))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.0)
        self.clear_scene()
