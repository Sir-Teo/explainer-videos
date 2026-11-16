from __future__ import annotations

from videos.psychology.psych51.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.levers()
        self.knobs()
        self.question()
        self.objectives()

    def levers(self):
        rows_section(self, r"Two levers that felt the same", [
            (r"1940s: \ pilots of some bomber types kept retracting the landing gear after landing, \ when they meant "
             r"to raise the flaps", WHITE),
            (r"the two levers sat side by side, \ the same shape, \ the same feel", AUTH),
            (r"1947: \ Paul Fitts and Richard Jones collected 460 ``pilot errors'' and found the same few again and "
             r"again: \ controls confused, \ instruments misread", PERSON),
            (r"the errors were predictable from the cockpit, \ not from the pilot", MODEL),
            (r"human factors begins here: \ error is designed in, \ and can be designed out", YOU),
        ], "In the 1940s, pilots of some bomber types kept doing something strange. <bookmark mark='a'/> After "
           "landing, they retracted the landing gear when they meant to raise the flaps. <bookmark mark='b'/> The two "
           "levers sat side by side, with the same shape and the same feel. <bookmark mark='c'/> In 1947 Paul Fitts "
           "and Richard Jones collected four hundred and sixty reports of pilot error, and found the same few again "
           "and again: controls confused, and instruments misread. <bookmark mark='d'/> The errors could be predicted "
           "from the cockpit, not from the pilot. <bookmark mark='e'/> Human factors begins here. Error is designed "
           "in, and it can be designed out.", tag=published_tag(r"Fitts \& Jones (1947)"))

    def knobs(self):
        wheel = VGroup(Circle(0.55, color=PERSON, stroke_width=4),
                       *[Line([0, 0, 0], [0.55 * np.cos(a), 0.55 * np.sin(a), 0], color=PERSON, stroke_width=3)
                         for a in np.linspace(0, 2 * np.pi, 7)[:-1]]).move_to([-3.0, 2.0, 0])
        flap = Polygon([-0.7, -0.15, 0], [0.7, -0.15, 0], [0.5, 0.25, 0], [-0.5, 0.25, 0], color=MODEL,
                       stroke_width=4, fill_color=MODEL, fill_opacity=0.3).move_to([3.0, 2.0, 0])
        lw = label(r"landing gear: \ a wheel", font_size=22, color=PERSON).next_to(wheel, DOWN, buff=0.25)
        lf = label(r"flaps: \ a flap", font_size=22, color=MODEL).next_to(flap, DOWN, buff=0.5)
        rows_section(self, r"A wheel and a flap", [
            (r"Alphonse Chapanis's fix: \ make each lever's knob the shape of what it moves", WHITE),
            (r"a hand that finds a wheel knows it is about to move the wheels, \ without looking", GOOD),
            (r"shape coding is still the rule in cockpits, \ alongside position, \ colour and motion coding", MODEL),
        ], "The fix was almost embarrassingly simple. <bookmark mark='a'/> Alphonse Chapanis made each lever's knob "
           "the shape of what it moved: a little wheel for the wheels, and a flap for the flaps. "
           "<bookmark mark='b'/> A hand that finds a wheel knows it's about to move the wheels, without looking. "
           "<bookmark mark='c'/> Shape coding is still the rule in cockpits, alongside coding by position, colour and "
           "direction of motion.", extra=VGroup(wheel, flap, lw, lf))

    def question(self):
        rows_section(self, r"Today: \ when a person makes a fatal error with a machine, \ whose error is it?", [
            (r"errors designed in, \ and the kinds of error", SYMP),
            (r"attention at work: \ load, \ vigilance, \ rare targets and awareness", MODEL),
            (r"automation, \ trust and alarms", PERSON),
            (r"systems, \ checklists, \ crews and fatigue", GOOD),
        ], "So this part asks: when a person makes a fatal error with a machine, whose error is it? "
           "<bookmark mark='a'/> Errors designed in, and the kinds of error. <bookmark mark='b'/> Attention at work: "
           "load, vigilance, rare targets, and awareness. <bookmark mark='c'/> Automation, trust, and alarms. "
           "<bookmark mark='d'/> And systems, checklists, crews, and fatigue.", font_size=27, buff=0.48)

    def objectives(self):
        head = VGroup(label(r"Part 51", font_size=34, color=GREY_B), label(r"Human Factors", font_size=56))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"compatibility, \ coding, \ Fitts's and Hick's laws",
            r"slips, \ lapses and mistakes; \ skills, \ rules and knowledge",
            r"workload, \ the vigilance decrement and rare targets",
            r"situation awareness, \ and the ironies of automation",
            r"alarms as criteria, \ and trust that fits reliability",
            r"Swiss cheese, \ checklists, \ crews and fatigue",
        ], color=P.ACCENT, font_size=31, width=13.2)
        with self.voiceover(
            "This is Part 51 of Psychology, Built: human factors, and the first part of Act Twelve, psychology at "
            "work. <bookmark mark='a'/> We'll see how compatibility and coding prevent errors, and fit Fitts's and "
            "Hick's laws. We'll sort errors into slips, lapses and mistakes. We'll measure workload, watch vigilance "
            "decline, and miss rare targets. We'll ask what situation awareness is, and why reliable automation makes "
            "takeover harder. We'll treat an alarm as a criterion an engineer chose, and trust as something that "
            "should fit reliability. And we'll meet the Swiss cheese model, checklists, crews, and fatigue as a "
            "measured risk."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(head.animate.scale(0.6).to_edge(UP, buff=0.3))
            obj.next_to(head, DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in obj], lag_ratio=0.9), run_time=20.0)
        self.clear_scene()
