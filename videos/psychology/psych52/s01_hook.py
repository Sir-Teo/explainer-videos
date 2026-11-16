from __future__ import annotations

from videos.psychology.psych52.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.story()
        self.path()
        self.question()
        self.objectives()

    def story(self):
        rows_section(self, r"A workstation that would save time", [
            (r"late 1980s: \ a telephone company's directory and toll operators handle millions of calls a year", WHITE),
            (r"a new workstation is offered: \ fewer keystrokes per call, \ a better screen, \ expected to save time on "
             r"every call", GOOD),
            (r"at that volume, \ every second per call is worth a great deal of money a year", PERSON),
            (r"Wayne Gray, \ Bonnie John and Michael Atwood model the operators' perception, \ thinking and "
             r"keystrokes on paper, \ before the trial", MODEL),
            (r"their model says the new workstation will be slower: \ by about two thirds of a second a call", AUTH),
        ], "<bookmark mark='a'/> In the late nineteen eighties, a telephone company's operators handle millions of calls "
           "a year. <bookmark mark='b'/> A new workstation is offered to them: fewer keystrokes per call, a better "
           "screen, and time saved on every call. <bookmark mark='c'/> At that volume, every second per call is worth "
           "a great deal of money a year. <bookmark mark='d'/> Wayne Gray, Bonnie John and Michael Atwood model the "
           "operators' perception, thinking and keystrokes on paper, before the field trial. <bookmark mark='e'/> "
           "Their model "
           "says the new workstation will be slower, by about two thirds of a second a call.",
           tag=published_tag(r"Gray, \ John \& Atwood (1993)"))

    def path(self):
        d = load("ernestine")
        head = heading(r"Why fewer keystrokes can be slower")
        cols = {"greet": CROWD, "listen": SYMP, "look up": MODEL, "close": CROWD, "extra keystroke on path": AUTH}
        bars_ = VGroup()
        for row, (steps, ts) in enumerate(((d["old_steps"], d["old_t"]), (d["new_steps"], d["new_t"]))):
            x = -5.4
            g = VGroup()
            for s_, t_ in zip(steps, ts):
                if t_ <= 0:
                    continue
                w = 0.85 * t_
                r = Rectangle(width=w, height=0.55, color=cols[s_], fill_opacity=0.75, stroke_width=1)
                r.move_to([x + w / 2, 1.3 - 1.25 * row, 0])
                g.add(r)
                if w > 1.0:
                    g.add(label(s_, font_size=14, color=BLACK).move_to(r))
                x += w
            bars_.add(g)
        names = VGroup(label(r"old", font_size=20, color=GREY_B).next_to(bars_[0], LEFT, buff=0.2),
                       label(r"new", font_size=20, color=GREY_B).next_to(bars_[1], LEFT, buff=0.2))
        par = VGroup(label(r"keystrokes done while the customer talks: \ off the critical path", font_size=15,
                           color=GREY_A)).next_to(bars_[0], UP, buff=0.2).align_to(bars_[0], LEFT)
        rows = rows_of([
            (r"a call is a schedule: \ some steps happen in parallel, \ and only the longest chain sets the time", WHITE),
            (r"the keystrokes the new design saved were made while the customer was talking: \ off the critical "
             r"path", GOOD),
            (r"the steps it added fell on the path, \ where every tenth of a second counts", AUTH),
            (r"the field trial agreed with the model: \ the new workstation was slower, \ and was not bought", YOU),
        ], 12.4, 20, 0.32).move_to([0, -2.2, 0])
        with self.voiceover(
            "Why can fewer keystrokes be slower? <bookmark mark='a'/> Because a call is a schedule. Some steps happen "
            "in parallel, and only the longest chain sets the time. This is a toy version of the analysis. "
            "<bookmark mark='b'/> The keystrokes the new design saved were made while the customer was still talking, "
            "off the critical path. <bookmark mark='c'/> The steps it added fell on the path, where every tenth of a "
            "second counts. <bookmark mark='d'/> The field trial agreed with the model. The new workstation was "
            "slower, and the company didn't buy it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(names), FadeIn(bars_[0]), FadeIn(par))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(bars_[1], shift=RIGHT * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def question(self):
        rows_section(self, r"Today: \ can you predict how long a person will take to use something before it is "
                           r"built?", [
            (r"engineering models of the user: \ processors, \ operators, \ pointing and menus", SYMP),
            (r"how people search, \ act and understand an interface", MODEL),
            (r"testing with users, \ and reading charts", PERSON),
            (r"accessibility, \ habits and machines that talk back", GOOD),
        ], "So this part asks: can you predict how long a person will take to use something, before it's built? "
           "<bookmark mark='a'/> Engineering models of the user: processors, operators, pointing and menus. "
           "<bookmark mark='b'/> How people search, act and understand an interface. <bookmark mark='c'/> Testing "
           "with users, and reading charts. <bookmark mark='d'/> And accessibility, habits, and machines that talk "
           "back.", font_size=27, buff=0.48)

    def objectives(self):
        head = VGroup(label(r"Part 52", font_size=34, color=GREY_B), label(r"Designing for Minds", font_size=56))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"the Model Human Processor and the keystroke-level model",
            r"Fitts's law measured as throughput, \ and the steering law",
            r"menus, \ foraging, \ and Norman's two gulfs",
            r"how many users a test needs, \ and why",
            r"reading charts and contrast as psychophysics",
            r"habits, \ dark patterns and conversational machines",
        ], color=P.ACCENT, font_size=31, width=13.2)
        with self.voiceover(
            "This is Part 52 of Psychology, Built: designing for minds. <bookmark mark='a'/> We'll build the Model "
            "Human Processor and the keystroke-level model, and predict times by adding operators. We'll measure "
            "pointing as throughput, and steer through tunnels. We'll design menus, follow foragers, and cross "
            "Norman's two gulfs. We'll ask how many users a test needs, and why the famous answer is too small. We'll "
            "treat reading a chart and seeing contrast as psychophysics. And we'll look at habits, dark patterns, and "
            "machines that talk back."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(head.animate.scale(0.6).to_edge(UP, buff=0.3))
            obj.next_to(head, DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in obj], lag_ratio=0.9), run_time=20.0)
        self.clear_scene()
