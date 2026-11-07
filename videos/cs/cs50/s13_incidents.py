from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs50.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, code_block, load, mono


def role(title, body, col, w=3.6, h=1.3):
    r = RoundedRectangle(width=w, height=h, corner_radius=0.12, stroke_color=col, stroke_width=2.2, fill_color=BG,
                         fill_opacity=1)
    t = label(title, font_size=21, color=col)
    b = wrapped_label(body, w - 0.3, font_size=18, color=GREY_A)
    VGroup(t, b).arrange(DOWN, buff=0.1).move_to(r)
    return VGroup(r, t, b)


class Incidents(VoiceoverScene):
    def construct(self):
        self.card()
        self.timeline()
        self.command()
        self.blameless()
        self.cheese()
        self.cook()

    def card(self):
        card = chapter_card(12, r"Incidents and post-mortems", r"When it breaks, \ who does what, \ and what do we "
                            r"learn?", lit=(1998, 2016), extra=((1998, r"Cook: \ How Complex Systems Fail"),
                                                               (2016, r"Beyer et al.: \ Site Reliability "
                                                                      r"Engineering")), part=PART)
        with self.voiceover("Chapter twelve. Incidents: what people do while a system is broken, and what they "
                            "learn afterwards."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def timeline(self):
        head = label(r"An incident, \ minute by minute", font_size=36).to_edge(UP, buff=0.3)
        x0, x1, T = -6.2, 6.4, 60.0

        def X(t):
            return x0 + (x1 - x0) * t / T
        y_line = -0.4
        axis = Arrow([x0, y_line, 0], [x1 + 0.2, y_line, 0], buff=0, color=GREY_C, stroke_width=2,
                     max_tip_length_to_length_ratio=0.015)
        ticks = VGroup(*[VGroup(Line([X(t), y_line - 0.06, 0], [X(t), y_line + 0.06, 0], color=GREY_C),
                                label(rf"{t}", font_size=16, color=GREY_B).next_to([X(t), y_line, 0], DOWN, buff=0.1))
                         for t in range(0, 61, 10)])
        unit = label(r"minutes", font_size=16, color=GREY_B).next_to(ticks, DOWN, buff=0.08).align_to(ticks, RIGHT)

        # an illustrative error rate: a bad change at minute 2, rolled back at 34
        def err(t):
            if t < 4:
                return 0.0
            if t < 34:
                return min(1.0, (t - 4) / 5)
            return max(0.0, 1.0 - (t - 34) / 3)
        top, low = 2.0, y_line + 0.55
        curve = VMobject(color=NO, stroke_width=3).set_points_as_corners(
            [[X(t / 4), low + (top - low) * err(t / 4), 0] for t in range(0, 241)])
        curve_l = label(r"errors", font_size=18, color=NO).next_to([X(16), top, 0], UP, buff=0.1)
        events = ((2, r"a change ships", GREY_A), (4, r"errors begin", NO), (11, r"alert: \ fast burn", HEAD),
                  (13, r"on-call acknowledges", DATA), (16, r"incident declared", LAM),
                  (21, r"status page updated", LAM), (34, r"rolled back", YES), (37, r"recovered", YES))
        marks = VGroup()
        for i, (t, txt, col) in enumerate(events):
            d = Dot([X(t), y_line, 0], radius=0.07, color=col)
            num = label(rf"{i + 1}", font_size=17, color=col).next_to(d, UP, buff=0.1)
            key = label(rf"{i + 1} \ {txt}", font_size=18, color=col)
            marks.add(VGroup(d, num, key))
        keys = VGroup(*[m[2] for m in marks]).arrange_in_grid(rows=2, cols=4, buff=(0.45, 0.22),
                                                              col_alignments="llll", flow_order="rd")
        keys.to_edge(DOWN, buff=0.35)
        ttd = BraceBetweenPoints([X(4), y_line - 0.5, 0], [X(11), y_line - 0.5, 0], direction=DOWN, color=HEAD)
        ttd_l = label(r"to detect", font_size=17, color=HEAD).next_to(ttd, DOWN, buff=0.05)
        ttm = BraceBetweenPoints([X(11), y_line - 0.5, 0], [X(34), y_line - 0.5, 0], direction=DOWN, color=YES)
        ttm_l = label(r"to mitigate", font_size=17, color=YES).next_to(ttm, DOWN, buff=0.05)
        later = wrapped_label(r"root cause: \ the next day, \ calmly; \ then the post-mortem", 3.0, font_size=18,
                              color=GREY_A).move_to([X(50), 1.0, 0])
        ill = note(r"illustrative", font_size=16).to_corner(UR, buff=0.4).shift(DOWN * 0.5)
        with self.voiceover(
            "Here is an incident, as it typically unfolds. <bookmark mark='a'/> A change ships, and two minutes "
            "later errors begin. Google's site reliability book reports that about seventy percent of its outages "
            "came from changes to a live system. <bookmark mark='b'/> Chapter two's fast-burn alert pages the "
            "on-call engineer, who acknowledges, sees users affected, and declares an incident: now one named "
            "person is in charge, and customers are told. <bookmark mark='c'/> The first goal is not to understand "
            "the bug but to stop the harm, usually by undoing the change. Here the rollback ends it at minute "
            "thirty-four. <bookmark mark='d'/> Two intervals are tracked across incidents: the time to detect, and "
            "the time to mitigate. The root cause can wait for the next day, when nobody is in a hurry."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ill), GrowArrow(axis), FadeIn(ticks), FadeIn(unit))
            vo.wait_until("a")
            self.play(FadeIn(marks[0]), FadeIn(marks[1]))
            self.play(Create(curve), FadeIn(curve_l), run_time=2)
            vo.wait_until("b")
            for m in marks[2:6]:
                self.play(FadeIn(m), run_time=0.6)
            vo.wait_until("c")
            self.play(FadeIn(marks[6]), FadeIn(marks[7]))
            vo.wait_until("d")
            self.play(GrowFromCenter(ttd), FadeIn(ttd_l))
            self.play(GrowFromCenter(ttm), FadeIn(ttm_l), FadeIn(later))
        self.wait(0.4)
        self.clear_scene()

    def command(self):
        head = label(r"Incident command", font_size=36).to_edge(UP, buff=0.3)
        ic = role(r"incident commander", r"holds the whole picture; \ decides; \ assigns; \ does not debug", HEAD,
                  w=4.0, h=1.45).move_to([0, 0.35, 0])
        ops = role(r"operations", r"the only hands changing the system", KERN).move_to([-4.5, 1.55, 0])
        com = role(r"communication", r"status page and stakeholders, \ on a fixed schedule", LAM).move_to(
            [4.5, 1.55, 0])
        plan = role(r"planning", r"the log of what was tried; \ hand-offs; \ follow-up bugs", DATA).move_to(
            [-4.5, -1.0, 0])
        resp = role(r"responders", r"work through the operations lead, \ not around it", GREY_B).move_to(
            [4.5, -1.0, 0])
        links = VGroup(*[Line(ic[0].get_center(), b[0].get_center(), color=GREY_C, stroke_width=2).set_z_index(-1)
                         for b in (ops, com, plan, resp)])
        foot = wrapped_label(r"borrowed from the Incident Command System of American firefighters \ (1970s); \ "
                             r"the roles are hats, \ not ranks: \ in a small incident one person wears several",
                             12.4, font_size=20, color=WHITE).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The roles come from firefighting: Google's book adapts the Incident Command System, developed by "
            "American wildfire crews in the 1970s. <bookmark mark='a'/> At the centre, the incident commander holds "
            "the whole picture, decides and assigns work, and deliberately does not debug. <bookmark mark='b'/> The "
            "operations lead is the only one changing the system, so that two people never fight over it. <bookmark "
            "mark='c'/> The communication lead updates the status page and stakeholders on a fixed schedule, so "
            "that nobody interrupts the operators to ask. Planning keeps the log of what was tried, and arranges "
            "hand-offs. <bookmark mark='d'/> The roles are hats, not ranks: in a small incident one person wears "
            "several."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(ic))
            vo.wait_until("b")
            self.play(Create(links[0]), FadeIn(ops))
            vo.wait_until("c")
            self.play(Create(links[1]), FadeIn(com))
            self.play(Create(links[2]), FadeIn(plan), Create(links[3]), FadeIn(resp))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def blameless(self):
        head = label(r"The blameless post-mortem", font_size=36).to_edge(UP, buff=0.3)
        doc = code_block(["Summary", "Impact      users, minutes, budget spent", "Timeline    from the log, UTC",
                          "Contributing factors", "What went well", "What went wrong", "Where we got lucky",
                          "Action items  owner, bug, date"], size=17)
        frame = SurroundingRectangle(doc, color=GREY_C, buff=0.25, corner_radius=0.1, stroke_width=1.5)
        ttl = label(r"a post-mortem's sections", font_size=19, color=GREY_A).next_to(frame, UP, buff=0.12)
        left = VGroup(ttl, frame, doc).move_to([-3.4, 0.4, 0])
        q_bad = label(r"``Who made the mistake?''", font_size=24, color=NO)
        q_good = label(r"``Why did it make sense at the time?''", font_size=24, color=YES)
        strike = Line(q_bad.get_left(), q_bad.get_right(), color=NO, stroke_width=3)
        qs = VGroup(VGroup(q_bad, strike), q_good).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        qs.move_to([3.4, 1.9, 0])
        strike.move_to(q_bad)
        notes = VGroup(
            wrapped_label(r"punish the person who made the mistake, \ and the next person hides theirs: \ the "
                          r"organisation stops learning", 5.4, font_size=19, color=WHITE),
            wrapped_label(r"John Allspaw \ (Etsy, \ 2012): \ ask how the decision looked from inside, \ with what "
                          r"the person knew then", 5.4, font_size=19, color=GREY_A),
            wrapped_label(r"every action item has an owner and a date, \ or it will not happen", 5.4, font_size=19,
                          color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(qs, DOWN, buff=0.45).align_to(qs, LEFT)
        lucky = SurroundingRectangle(doc[6], color=HEAD, buff=0.06, stroke_width=2)
        with self.voiceover(
            "Afterwards comes the post-mortem: a written account of what happened and what will change. <bookmark "
            "mark='a'/> Google's template has a summary; the impact, in users, minutes and error budget; a "
            "timeline; contributing factors; what went well and what went wrong; <bookmark mark='b'/> and a section "
            "many teams find the most useful: where we got lucky. <bookmark mark='c'/> It is written without blame. "
            "Punish the person who typed the command, and the next person hides their mistake, and the organisation "
            "stops learning. <bookmark mark='d'/> John Allspaw, writing about Etsy's practice in 2012, asked not "
            "who made the mistake but why the action made sense at the time, with what they knew then. <bookmark "
            "mark='e'/> And every action item gets an owner and a date."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ttl), Create(frame))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in doc[:6]], lag_ratio=0.25), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(doc[6]), Create(lucky))
            vo.wait_until("c")
            self.play(FadeIn(q_bad), FadeIn(notes[0]))
            vo.wait_until("d")
            self.play(Create(strike), FadeIn(q_good), FadeIn(notes[1]))
            vo.wait_until("e")
            self.play(FadeIn(doc[7]), FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()
        _ = left

    def cheese(self):
        head = label(r"The Swiss-cheese model", font_size=36).to_edge(UP, buff=0.3)
        texts = (r"a command whose input could remove too much",
                 r"a tool with no floor and no speed limit",
                 r"subsystems not fully restarted for years",
                 r"a status page that itself depended on S3")
        holes_y = 0.55
        xs = (-4.65, -1.55, 1.55, 4.65)
        slices = VGroup()
        for i, (x, t) in enumerate(zip(xs, texts)):
            s = RoundedRectangle(width=1.0, height=3.4, corner_radius=0.15, stroke_color=HEAD, stroke_width=2,
                                 fill_color=HEAD, fill_opacity=0.55).move_to([x, 0.4, 0])
            holes = VGroup(*[Ellipse(width=0.42, height=0.5, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(
                [x + dx, y, 0]) for dx, y in ((0.12 * (-1) ** i, 1.6 - 0.12 * i), (-0.14 * (-1) ** i, -0.7 + 0.1 * i))])
            hole = Ellipse(width=0.45, height=0.55, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(
                [x, holes_y, 0])
            t_l = wrapped_label(t, 2.7, font_size=18, color=GREY_A).next_to(s, DOWN, buff=0.25)
            slices.add(VGroup(s, holes, hole, t_l))
        path = Arrow([-6.6, holes_y, 0], [6.6, holes_y, 0], buff=0, color=NO, stroke_width=5,
                     max_tip_length_to_length_ratio=0.03).set_z_index(3)
        src = note(r"Amazon S3, \ 2017: \ contributing factors from AWS's public summary", font_size=17).to_edge(
            DOWN, buff=0.25)
        with self.voiceover(
            "Why do incidents happen in systems built by careful people? James Reason, a psychologist who studied "
            "human error, offered a picture: the Swiss-cheese model. <bookmark mark='a'/> Every defence is a slice "
            "with holes in it, and the holes move. Harm gets through only when they line up. <bookmark mark='b'/> "
            "Take the S3 outage from the start of this part. The trigger was a mistyped input, but the tool also "
            "let too much capacity be removed, too quickly. <bookmark mark='c'/> The removed subsystems had not "
            "been fully restarted in the larger regions for years, so recovery was slow. And Amazon's status page "
            "could not at first show the problem, because it depended on S3. <bookmark mark='d'/> Four holes, lined "
            "up. Blaming the typist closes one."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(s[0], s[1], s[2])) for s in slices], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(FadeIn(slices[0][3]), FadeIn(slices[1][3]), FadeIn(src))
            vo.wait_until("c")
            self.play(FadeIn(slices[2][3]), FadeIn(slices[3][3]))
            vo.wait_until("d")
            self.play(GrowArrow(path), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    def cook(self):
        head = label(r"Cook: \ How Complex Systems Fail \ (1998)", font_size=36).to_edge(UP, buff=0.3)
        pts = ((r"complex systems run in degraded mode", KERN),
               (r"catastrophe needs several failures together", NO),
               (r"a single ``root cause'' is a fiction of hindsight", HEAD),
               (r"hindsight makes errors look obvious", HEAD),
               (r"people are the adaptable part that creates safety", YES),
               (r"change introduces new forms of failure", LAM))
        cards = VGroup()
        for t, col in pts:
            r = RoundedRectangle(width=6.0, height=1.05, corner_radius=0.12, stroke_color=col, stroke_width=2,
                                 fill_color=BG, fill_opacity=1)
            cards.add(VGroup(r, wrapped_label(t, 5.5, font_size=21, color=col).move_to(r)))
        cards.arrange_in_grid(rows=3, cols=2, buff=(0.4, 0.3)).next_to(head, DOWN, buff=0.5)
        foot = wrapped_label(r"eighteen short observations, \ written about hospitals, \ now read by every on-call "
                             r"team", 12.4, font_size=20, color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "In 1998 Richard Cook, a physician who studied safety in medicine, wrote a short paper called How "
            "Complex Systems Fail. <bookmark mark='a'/> Complex systems run in degraded mode, with something always "
            "broken somewhere. <bookmark mark='b'/> So catastrophe needs several failures at once: the Swiss cheese "
            "again. <bookmark mark='c'/> A single root cause is therefore a story told with hindsight, <bookmark "
            "mark='d'/> and hindsight makes every error look obvious. <bookmark mark='e'/> The people running a "
            "system are not its weak link but the adaptable part that creates its safety, mostly unseen. <bookmark "
            "mark='f'/> And every change, even a fix, introduces new forms of failure."
        ) as vo:
            self.play(FadeIn(head), FadeIn(foot))
            for mk, c in zip("abcdef", cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.wait(0.4)
        self.clear_scene()


_ = (DATA, KERN, load, mono)
