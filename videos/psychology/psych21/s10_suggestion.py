from __future__ import annotations

from videos.psychology.psych21.common import *  # noqa: F403


class Suggestion(VoiceoverScene):
    def construct(self):
        self.card()
        self.misinformation()
        self.source()
        self.mall()
        self.overshadow()
        self.forest()

    def card(self):
        card = chapter_card(9, r"Suggestion", r"Can someone else put a memory in your head?",
                            lit={1978: r"Loftus, \ Miller \& Burns", 1993: r"Johnson, \ Hashtroudi \& Lindsay",
                                 1995: r"Loftus \& Pickrell", 2014: r"Alogna et al."},
                            part=PART, scale=("mind", "group"), marr=("what",))
        with self.voiceover("Chapter nine. Suggestion."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def misinformation(self):
        head = heading(r"The misinformation effect")
        strip = trial_strip([
            (r"see: \ slides of an accident", label(r"STOP", font_size=30, color=LOST), r"a car at a stop sign"),
            (r"then: \ a question", label(r"``\dots the yield sign?''", font_size=22, color=FALSE),
             r"misleading, \ for half"),
            (r"later: \ which did you see?", label(r"STOP \ \ or \ \ YIELD", font_size=24, color=CUE),
             r"a forced choice"),
        ], frame_w=3.4, frame_h=1.2, font_size=19).move_to([0, 1.5, 0])
        rows = rows_of([
            (r"Loftus, \ Miller and Burns, \ 1978: \ a question that took the yield sign for granted made people "
             r"more likely to choose the slide with the yield sign", WHITE),
            (r"the post-event information became part of the memory of the event", FALSE),
            (r"hundreds of studies since: \ the effect is robust; \ its size depends on how plausible and how "
             r"well-timed the suggestion is, \ and whether people notice it", CUE),
            (r"what happens to the original detail is argued: \ overwritten, \ or still there but outcompeted at "
             r"test", GREY_A),
        ], 12.4, 24, 0.3).to_edge(DOWN, buff=0.65)
        tag = historical_tag(r"Loftus, \ Miller \& Burns (1978)")
        with self.voiceover(
            "Loftus and Palmer's broken glass was the start of a programme. <bookmark mark='a'/> In 1978 Loftus, "
            "David Miller and Helen Burns showed people slides of a car accident: a red car at a stop sign. Then "
            "they asked questions, and for half the people one question mentioned a yield sign instead, in passing, "
            "as if it had been there. Later everyone saw two slides and had to choose which they had seen. "
            "<bookmark mark='b'/> Those who had heard about the yield sign were more likely to choose the slide "
            "with the yield sign. Information after the event had become part of the memory of the event. "
            "<bookmark mark='c'/> Hundreds of studies have followed, and the effect is robust. Its size depends on "
            "how plausible the suggestion is, how long after the event it comes, and whether people notice the "
            "discrepancy. <bookmark mark='d'/> What happens to the original stop sign is still argued: whether "
            "it's overwritten, as reconsolidation might suggest, or still there, but losing the competition at test."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(strip))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def source(self):
        head = heading(r"Source monitoring")
        srcs = VGroup(*[word_chip(t, color=c, font_size=24) for t, c in
                        ((r"I saw it", TRACE), (r"I was told it", FALSE), (r"I imagined it", CUE),
                         (r"I dreamt it", CTX))]).arrange(DOWN, buff=0.3).move_to([-4.6, 0.2, 0])
        q = label(r"?", font_size=80, color=GREY_B).move_to([-2.4, 0.2, 0])
        mem = word_chip(r"a memory", color=WHITE, font_size=30).move_to([-0.6, 0.2, 0])
        arrows = VGroup(*[Arrow(s_.get_right(), q.get_left(), buff=0.1, color=GREY_D, stroke_width=2)
                          for s_ in srcs])
        rows = rows_of([
            (r"Johnson, \ Hashtroudi and Lindsay, \ 1993: \ memories carry no label of where they came from", WHITE),
            (r"the source is inferred at retrieval, \ from the memory's qualities: \ perceptual detail, \ context, \ "
             r"the effort it took", CUE),
            (r"a vivid, \ detailed memory feels \emph{seen}; \ an imagined event, \ rehearsed until it is vivid, \ "
             r"can pass", FALSE),
            (r"DRM's lure and the yield sign are both source errors: \ thought of, \ or heard about, \ remembered as "
             r"seen", TRACE),
        ], 6.0, 22, 0.3).move_to([3.7, 0.0, 0])
        tag = published_tag(r"Johnson, \ Hashtroudi \& Lindsay (1993)")
        with self.voiceover(
            "Marcia Johnson, Shahin Hashtroudi and Stephen Lindsay gave these errors a framework in 1993. "
            "<bookmark mark='a'/> A memory does not come with a label saying where it came from: something seen, "
            "something you were told, something you imagined, or dreamt. <bookmark mark='b'/> The source has to be "
            "inferred when you remember, from the memory's qualities: how much perceptual detail it has, its "
            "context, how much effort it took to bring back. <bookmark mark='c'/> Usually that works. But an "
            "imagined event, rehearsed until it's vivid and detailed, can pass for a perceived one. "
            "<bookmark mark='d'/> The DRM lure and the yield sign are both source errors: something thought of, "
            "or heard about, remembered as seen."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(srcs), FadeIn(q), FadeIn(mem))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.2), FadeIn(rows[0]))
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def mall(self):
        m = archive.LOFTUS_PICKRELL_1995.data
        head = heading(r"Lost in the mall: \ implanting a whole event")
        bars_ = VGroup()
        specs = ((rf"Loftus and Pickrell, \ 1995", m["original_n"], m["original_rate"]),
                 (rf"Scoboria and colleagues, \ 2017: \ eight studies pooled", m["mega_n"], m["mega_rate"]),
                 (rf"Murphy and colleagues, \ 2023: \ preregistered replication", m["replication_n"],
                  m["replication_rate"]))
        A = axes([0, 3], [0, 0.5], x_length=5.4, y_length=3.0, xticks=[], yticks=[0, 0.25, 0.5],
                 yfmt=lambda v: f"{100 * v:.0f}\\%", ylabel=r"came to remember the false event",
                 center=[-3.3, 0.3, 0], font_size=18)
        bb = bars(A.ax, np.arange(3) + 0.5, [s_[2] for s_ in specs], FALSE, width=0.55)
        names = VGroup(*[wrapped_label(s_[0] + rf" \ (N = {s_[1]})", 1.9, 16, GREY_A)
                         .next_to(A.ax.c2p(i + 0.5, 0), DOWN, buff=0.12) for i, s_ in enumerate(specs)])
        vals = VGroup(*[label(pct(s_[2]), font_size=20, color=GREY_A).next_to(b_, UP, buff=0.06)
                        for b_, s_ in zip(bb, specs)])
        rows = rows_of([
            (r"a booklet of four childhood events from a relative: \ three true, \ one false: \ lost in a "
             r"shopping mall at about five, \ rescued by an elderly person", WHITE),
            (r"asked to write what they remembered, \ then interviewed twice", GREY_A),
            (r"about a quarter came to remember the false event, \ in part or in full", FALSE),
            (r"the pooled studies agree, \ and the 2023 replication found a little more; \ how much of it is "
             r"\emph{belief} rather than \emph{memory} depends on the coding", CUE),
            (r"what it does not show: \ that memories of abuse are false, \ or that all recovered memories are; \ it "
             r"shows that a confident, \ detailed memory can be false", LOST),
        ], 6.4, 20, 0.25).move_to([3.4, 0.0, 0])
        tag = historical_tag(r"Loftus \& Pickrell (1995); \ Scoboria et al.\ (2017); \ Murphy et al.\ (2023)")
        with self.voiceover(
            "Could a whole event be implanted? In 1995 Loftus and Jacqueline Pickrell tried. "
            "<bookmark mark='a'/> Each participant got a booklet of four events from their childhood, supplied by a "
            "relative. Three were true. One was false: being lost in a shopping mall at about five, crying, and "
            "being rescued by an elderly person. <bookmark mark='b'/> They wrote what they remembered of each, and "
            "were interviewed twice over the following weeks. <bookmark mark='c'/> Of twenty-four people, about a "
            "quarter came to remember being lost in the mall, in part or in full. <bookmark mark='d'/> In 2017 "
            "Alan Scoboria and colleagues pooled eight implantation studies, four hundred and twenty-three people, "
            "and found about thirty percent with a false memory; and a preregistered replication by Gillian Murphy "
            "and colleagues in 2023 found thirty-five. How much of this is memory, rather than belief, depends on how "
            "the reports are coded, and that's argued. <bookmark mark='e'/> And it's important to say what this "
            "does not show. It doesn't show that memories of abuse are false, or that every recovered memory is. "
            "It shows that a detailed, confident memory can be false, which is reason for care, not dismissal."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(GrowFromEdge(bb[0], DOWN), FadeIn(vals[0]), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(GrowFromEdge(bb[1], DOWN), GrowFromEdge(bb[2], DOWN), FadeIn(vals[1]), FadeIn(vals[2]),
                      FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def overshadow(self):
        d = load("overshadow")
        head = heading(r"Describing a face: \ verbal overshadowing")
        strip = trial_strip([
            (r"watch", label(r"a robbery", font_size=26, color=TRACE), r"on video"),
            (r"20 minutes", label(r"a filler task", font_size=24, color=GREY_B), ""),
            (r"5 minutes", label(r"describe the robber", font_size=22, color=FALSE), r"or: \ name states and capitals"),
            (r"then", label(r"a line-up", font_size=24, color=CUE), r"pick the robber, \ or `not present'"),
        ], frame_w=2.9, frame_h=1.1, font_size=17).move_to([0, 1.6, 0])
        rows = rows_of([
            (rf"Schooler and Engstler-Schooler, \ 1990: \ describing the face \emph{{lowered}} correct "
             rf"identification, \ by {abs(100 * d['s2_original']):.0f} points", WHITE),
            (r"trying to remember usually helps; \ here putting a face into words seemed to hurt the memory of it",
             FALSE),
            (r"influential in law: \ should police take a description before a line-up? \ but later studies found "
             r"much smaller effects", CUE),
            (r"2014: \ the first Registered Replication Report: \ one protocol, \ approved in advance, \ run by "
             r"labs around the world, \ data open", MODEL),
        ], 12.4, 24, 0.3).to_edge(DOWN, buff=0.65)
        tag = historical_tag(archive.SCHOOLER_1990.cite)
        with self.voiceover(
            "Suggestion can come from another person. Can it come from yourself? <bookmark mark='a'/> In 1990 "
            "Jonathan Schooler and Tonya Engstler-Schooler showed people a video of a robbery. After a filler task, "
            "some spent five minutes describing the robber's face in as much detail as they could; others named "
            "American states and their capitals. Then everyone tried to pick the robber from a line-up. Describing "
            f"the face lowered correct identifications by {abs(100 * d['s2_original']):.0f} points. "
            "<bookmark mark='b'/> That's surprising. Trying to remember usually helps memory. Here, putting a face "
            "into words seemed to damage the memory of it: verbal overshadowing. <bookmark mark='c'/> It mattered "
            "for the law, because police routinely take a description before a line-up. But later studies found "
            "smaller effects, and some none. <bookmark mark='d'/> So in 2014 it became the subject of the first "
            "Registered Replication Report: one protocol, approved in advance with the original author's help, run "
            "by dozens of labs, with every lab's data published."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(strip))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def forest(self):
        d = load("overshadow")
        head = heading(r"The replication, \ lab by lab")
        n = int(d["s2_labs"])
        diff, se = d["s2_diff"], d["s2_se"]
        order = np.argsort(diff)
        A = axes([-0.6, 0.4], [0, n + 4], x_length=6.8, y_length=5.6, xticks=[-0.6, -0.4, -0.2, 0, 0.2, 0.4],
                 yticks=[], xfmt=lambda v: f"{100 * v:+.0f}" if abs(v) > 1e-9 else "0",
                 xlabel=r"verbal minus control, \ correct identifications \ (points)", center=[-2.4, -0.2, 0],
                 font_size=18)
        zero = DashedLine(A.ax.c2p(0, 0), A.ax.c2p(0, n + 4), color=GREY_D)
        g = VGroup()
        for row, i in enumerate(order):
            y = row + 1
            g.add(Line(A.ax.c2p(max(diff[i] - 1.96 * se[i], -0.6), y), A.ax.c2p(min(diff[i] + 1.96 * se[i], 0.4), y),
                       color=GREY_B, stroke_width=2),
                  Dot(A.ax.c2p(diff[i], y), radius=0.05, color=CUE))
        pooled = d["s2_pooled"]
        pse = d["s2_pooled_se"]
        yp = n + 1.6
        diamond = Polygon(A.ax.c2p(pooled - 1.96 * pse, yp), A.ax.c2p(pooled, yp + 0.6),
                          A.ax.c2p(pooled + 1.96 * pse, yp), A.ax.c2p(pooled, yp - 0.6), color=MODEL,
                          fill_opacity=0.9, stroke_width=0)
        orig = Star(n=5, outer_radius=0.14, inner_radius=0.06, color=LOST, fill_opacity=1).move_to(
            A.ax.c2p(d["s2_original"], n + 3.2))
        ol = label(r"the original", font_size=18, color=LOST).next_to(orig, RIGHT, buff=0.1)
        pl = label(r"pooled", font_size=18, color=MODEL).next_to(diamond, RIGHT, buff=0.1)
        rows = rows_of([
            (rf"{n} labs, \ {num(d['s2_n'])} people, \ the description after a 20-minute filler, \ as in the "
             r"original", CUE),
            (rf"pooled: \ {100 * d['s2_pooled']:.0f} points \ ($\pm${196 * d['s2_pooled_se']:.0f}), \ against "
             rf"{100 * d['s2_original']:.0f} in the original", MODEL),
            (rf"a second set, \ {int(d['s1_labs'])} labs with the description straight after the video: \ "
             rf"{100 * d['s1_pooled']:.0f} points", FALSE),
            (r"real, \ smaller than first reported, \ and sensitive to timing: \ the replication found something "
             r"the original did not know", WHITE),
        ], 4.8, 20, 0.3).move_to([4.6, -0.1, 0])
        ptag = psyche_tag(r"open data: \ Alogna et al.\ \ (2014), \ osf.io/ybeur")
        with self.voiceover(
            "Here are the data, from the open files. <bookmark mark='a'/> Each line is one lab: the difference "
            "between the describers and the controls in correct identifications, with its ninety-five percent "
            f"interval. These are the {n} labs that followed the original timing, describing the face after a "
            "twenty-minute filler task. Most of the labs' intervals cross zero: one lab of about a hundred people "
            f"can't pin down an effect this size. <bookmark mark='b'/> Pooled, the effect is {abs(100 * d['s2_pooled']):.0f} "
            f"points, against {abs(100 * d['s2_original']):.0f} in the original. <bookmark mark='c'/> And there "
            f"was a second set of {int(d['s1_labs'])} labs, run first, whose protocol had people describe the face "
            "straight after the video, before the filler. There the effect was only "
            f"{abs(100 * d['s1_pooled']):.0f} points. <bookmark mark='d'/> So verbal overshadowing is real, smaller "
            "than the first report, and depends on timing: something the original study, with its few dozen "
            "people, could not have known. That's what a replication done this way can teach."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), Create(zero), FadeIn(ptag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in g], lag_ratio=0.03), FadeIn(rows[0]), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(orig), FadeIn(ol), FadeIn(diamond), FadeIn(pl), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
