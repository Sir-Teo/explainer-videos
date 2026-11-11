from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant32.common import BAD, GOOD, HURDLE, PART
from videos.quant.quant32.illustrations import calendar_case


class Calendar(VoiceoverScene):
    def construct(self):
        self.card()
        self.window()
        self.attribution()
        self.clock(calendar_case())
        self.costs(calendar_case())
        self.event_window()
        self.corporate()
        self.multiplicity(calendar_case())
        self.evidence()
        self.question()

    def card(self):
        c = chapter_card(8, r"Calendars, nights and events", r"What timing rule was known before the return?", part=PART)
        with self.voiceover(
            "Chapter eight. A calendar or event condition specifies when exposure is held. To assess it, "
            "define the window before observing its returns, keep the price and cash-flow clock explicit, "
            "and account for the other rules considered. Chosen arithmetic can explain those requirements "
            "without establishing an empirical calendar premium."
        ):
            self.play(FadeIn(c[0]), FadeIn(c[1]))
        self.play(FadeOut(c))

    def window(self):
        head = label(r"Chosen 20-trading-day month", font_size=30).to_edge(UP, buff=0.5)
        selected = {1, 2, 3, 20}
        cells = VGroup()
        for day in range(1, 21):
            col = GOOD if day in selected else GREY_C
            square = Rectangle(width=0.55, height=0.7, color=col, fill_color=col, fill_opacity=0.15)
            number = MathTex(str(day), font_size=22).move_to(square)
            cells.add(VGroup(square, number))
        cells.arrange(RIGHT, buff=0.07)
        foot = wrapped_label(r"chosen rule: first three trading days plus the last; selected dates are known "
                             r"from the calendar, not chosen from realised returns", 12.2, 20,
                             GREY_A).to_edge(DOWN, buff=0.55)
        self.play(FadeIn(head), FadeIn(cells), FadeIn(foot))
        with self.voiceover(
            "A turn-of-month definition can select the last trading day and the first three of "
            "the next month. In this chosen twenty-trading-day illustration, four selected dates "
            "are twenty percent of the sample. The number of trading days varies in real months. "
            "A test must also define holidays, market closures, trading sessions and when the "
            "calendar was available. Most importantly, the membership rule is fixed before "
            "looking at its returns. Selecting the best four dates afterward answers a different question."
        ):
            self.wait(0.2)
        self.clear_scene()

    def attribution(self):
        event_sum, other_sum = 4 * 0.001, 16 * -0.0001
        share = event_sum / (event_sum + other_sum)
        rows = VGroup(
            MathTex(r"4\text{ dates at }+10\ {\rm bp}:\quad +40\ {\rm bp}", font_size=34),
            MathTex(r"16\text{ dates at }-1\ {\rm bp}:\quad -16\ {\rm bp}", font_size=34),
            MathTex(rf"\frac{{\sum_{{t\in E}}r_t}}{{\sum_t r_t}}=\frac{{40}}{{24}}={100 * share:.1f}\%", font_size=38),
        ).arrange(DOWN, buff=0.65)
        foot = wrapped_label(r"chosen additive return accounting, not compounded strategy wealth, causal attribution "
                             r"or a probability; the ratio is undefined at a zero denominator",
                             12.2, 18, GREY_A).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(rows[0]), FadeIn(foot))
        with self.voiceover(
            "Choose ten basis points on each selected date and minus one on every other date. "
            "<bookmark mark='a'/> Selected returns sum to forty basis points and the rest to "
            "minus sixteen, for an additive total of twenty-four. "
            f"<bookmark mark='b'/> The selected share is {100 * share:.1f} percent, more than all "
            "of the total because the other dates contribute negatively. It is a ratio of sums, "
            "not a probability, an independent risk share or causal evidence. It can be unstable "
            "near a zero denominator. A conditional daily mean annualised by two hundred fifty-two "
            "also differs from the return of investing only on those dates."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def clock(self, a):
        clock_labels = (r"100\ \text{前收盘}\ \longrightarrow\ 102\ \text{开盘}\ \longrightarrow\ 101\ \text{收盘}"
                        if zh() else
                        r"100\ {\rm previous\ close}\ \longrightarrow\ 102\ {\rm open}\ \longrightarrow\ 101\ {\rm close}")
        rows = VGroup(
            MathTex(clock_labels, font_size=31),
            MathTex(rf"r_N={100 * a['overnight']:.2f}\%,\quad r_D={100 * a['intraday']:.4f}\%,"
                    rf"\quad r_{{\rm whole}}={100 * a['whole_day']:.2f}\%", font_size=33),
            MathTex(r"(1+r_N)(1+r_D)=\frac{102}{100}\frac{101}{102}=\frac{101}{100}", font_size=34),
        ).arrange(DOWN, buff=0.65)
        foot = wrapped_label(r"three chosen prices, no dividends or other corporate actions; raw-price gross "
                             r"return identity before costs", 12.2, 18,
                             GREY_A).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(rows[0]), FadeIn(foot))
        with self.voiceover(
            "For the overnight clock, choose a previous close of one hundred, next open one hundred "
            "two, and next close one hundred one, with no corporate actions. "
            "<bookmark mark='a'/> Overnight return is two percent; intraday return is about minus "
            "point nine eight zero four percent; the whole day gains one percent. "
            "<bookmark mark='b'/> Gross returns multiply, rather than adding exactly. With adjusted "
            "prices, the adjustment convention also allocates dividends and other actions between "
            "the legs. Separate compounded overnight and intraday lines therefore need their own "
            "cash, adjustment and trading conventions before they describe implementable accounts."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def costs(self, a):
        rows = VGroup(
            MathTex(r"4\text{基点毛收益}-5\text{基点往返成本}=-1\text{基点}" if zh() else
                    r"4\ {\rm bp\ gross}-5\ {\rm bp\ roundtrip}=-1\ {\rm bp}", font_size=35),
            MathTex(r"2\times252=504\text{ transaction legs}", font_size=34),
            MathTex(r"1000\text{基点}/504\approx1.98\text{基点/腿}" if zh() else
                    r"1000\ {\rm bp}/504\approx1.98\ {\rm bp\ per\ leg}", font_size=35),
        ).arrange(DOWN, buff=0.65)
        foot = wrapped_label(r"separate chosen cost budgets; annual example is linear in starting capital, "
                             r"without reinvestment, impact, financing or changing turnover",
                             12.2, 18, GREY_A).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(rows[0]), FadeIn(foot))
        with self.voiceover(
            "A visible conditional mean is not a net trading edge. Choose four basis points gross "
            "per round trip and five basis points of round-trip cost: the remainder is minus one. "
            "<bookmark mark='a'/> Entering and exiting once on each of two hundred fifty-two "
            "sessions gives five hundred four transaction legs. "
            "<bookmark mark='b'/> In a separate chosen linear budget, ten percent gross profit "
            "on starting capital is one thousand basis points. Dividing by five hundred four "
            "gives about one point nine eight basis points per leg. This is a cost-budget "
            "approximation, not an exact compounded annual strategy return. Funding, spread "
            "variation, impact and changes in traded capital can alter the calculation."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def event_window(self):
        rows = VGroup(
            label(r"statement-day close-to-close", font_size=28, color=QC.SPOT),
            MathTex(r"[C_{\text{前收盘}},C_{\text{声明日收盘}}]" if zh() else
                    r"[C_{\rm previous},C_{\rm statement\ day}]", font_size=34),
            label(r"24 hours before the announcement", font_size=28, color=HURDLE),
            MathTex(r"[A-24{\rm h},A]", font_size=34),
        ).arrange(DOWN, buff=0.4)
        foot = wrapped_label(r"windows need release timestamps, market sessions, time zones and a fixed "
                             r"definition; the two selections generally differ", 12.2, 18,
                             GREY_A).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(VGroup(*rows[:2])), FadeIn(foot))
        with self.voiceover(
            "An announcement date does not define a unique return window. A close-to-close return "
            "on the statement day includes different hours from a twenty-four-hour interval "
            "ending at the announcement. "
            "<bookmark mark='a'/> Lucca and Moench's pre-FOMC-announcement finding concerns a "
            "specified pre-announcement clock. A daily statement-date comparison is not a direct "
            "replication of that window. "
            "<bookmark mark='b'/> Release timestamps, time zones, market sessions, scheduled and "
            "unscheduled meetings, and the calendar available beforehand must be explicit. "
            "A concentration of returns around an event does not alone identify a policy-news "
            "mechanism or prove that a trade was executable before the relevant information."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*rows[2:])))
            vo.wait_until("b")
            self.wait(0.2)
        self.clear_scene()

    def corporate(self):
        rows = VGroup(
            MathTex(r"\text{price}=105,\quad \text{close payoff}=110,\quad \text{break payoff}=90", font_size=30),
            MathTex(r"p^*=\frac{105-90}{110-90}=0.75", font_size=38),
            MathTex(r"p=0.9:\quad E[\text{payoff}-105]=0.9(5)+0.1(-15)=3", font_size=31),
        ).arrange(DOWN, buff=0.65)
        foot = wrapped_label(r"chosen two-state, same-horizon cash payoffs; zero rates and costs; probabilities "
                             r"are assumptions, not estimates or risk-neutral prices", 12.2, 18,
                             GREY_A).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(rows[0]), FadeIn(foot))
        with self.voiceover(
            "Corporate events add state risk. Choose a target price of one hundred five, a "
            "same-horizon closing payoff of one hundred ten, and a broken-deal payoff of ninety. "
            "<bookmark mark='a'/> With zero rates and costs, the probability that makes expected "
            "cash payoff equal the price is seventy-five percent. "
            "<bookmark mark='b'/> A chosen success probability of ninety percent gives expected "
            "profit three currency units, but the failure state loses fifteen. The probability "
            "is not established by the spread. Deal dependence, timing and market stress matter. "
            "Likewise, index changes and earnings events need information and execution clocks; "
            "a plausible flow story is not an automatic causal or risk-free-premium result."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def multiplicity(self, a):
        rows = VGroup(
            MathTex(r"M=100,\quad \alpha=0.05,\quad \text{all null hypotheses true}", font_size=32),
            MathTex(rf"\Pr(\text{{one or more false rejections}})=1-0.95^{{100}}"
                    rf"={100 * a['one_or_more_false_rejections']:.2f}\%", font_size=32),
            MathTex(r"E[\text{false rejections}]=100(0.05)=5", font_size=35),
        ).arrange(DOWN, buff=0.65)
        foot = wrapped_label(r"FWER formula assumes independent valid tests; the expected count uses marginal "
                             r"size and linearity and does not need independence", 12.2, 18,
                             GREY_A).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(rows[0]), FadeIn(foot))
        with self.voiceover(
            "Selection can make a calendar pattern look convincing. Choose one hundred valid "
            "five-percent tests with every null true. "
            f"<bookmark mark='a'/> If tests are independent, the chance of at least one false "
            f"rejection is {100 * a['one_or_more_false_rejections']:.2f} percent. "
            "<bookmark mark='b'/> The expected false-rejection count is five; linearity gives "
            "that expectation without independence when each marginal test has the stated size. "
            "Real calendar rules overlap, and their returns can be dependent over time. Sullivan, "
            "Timmermann and White examine data snooping in such rule universes. A suitable "
            "bootstrap or reality check needs its own validity assumptions and does not repair "
            "unknown lookahead, omitted costs or an unrecorded adaptive search."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def evidence(self):
        cards = VGroup(
            desk_question(r"historical patterns", r"Ariel and Lakonishok-Smidt motivate turn-of-month "
                          r"questions; a named sample result is not a universal law", width=12.2, font_size=20),
            desk_question(r"mechanisms", r"flows, risk bearing and investor clienteles are candidate explanations; "
                          r"coinciding dates do not identify them", width=12.2, font_size=20),
            desk_question(r"evaluation", r"preserve the full rule universe, use available calendars and "
                          r"cash-flow clocks, estimate dependence-aware uncertainty and net costs",
                          width=12.2, font_size=20),
        ).arrange(DOWN, buff=0.3)
        self.play(FadeIn(cards[0]))
        with self.voiceover(
            "Published calendar studies motivate questions rather than universal laws. Ariel and "
            "Lakonishok and Smidt examine turn-of-month patterns; other work examines seasonal, "
            "overnight and corporate-event returns. "
            "<bookmark mark='a'/> Flows, risk bearing and investor clienteles are possible "
            "explanations. A mechanism needs identifying evidence, and a later decline does not "
            "by itself prove that arbitrageurs removed an effect. "
            "<bookmark mark='b'/> Preserve the candidate rules, information clocks and selection "
            "history, measure uncertainty with appropriate dependence assumptions, and state "
            "costs and financing. Those requirements apply even when the dates look predictable "
            "and the sample conditional mean is large."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(cards[1]))
            vo.wait_until("b")
            self.play(FadeIn(cards[2]))
        self.clear_scene()

    def question(self):
        panel = VGroup(
            MathTex('g=4\\,{\\rm bp},\\qquad c=5\\,{\\rm bp}', font_size=34),
            MathTex('r_{\\rm net}=g-c', font_size=34),
            MathTex('1000\\,{\\rm bp}/504\\ \\approx\\ 1.98\\,{\\rm bp}', font_size=34),
        ).arrange(DOWN, buff=0.6).shift(UP * 0.3)
        self.play(FadeIn(panel))
        q = pause_card(r"Chosen overnight gross edge 4 bp per round trip, total round-trip cost 5 bp. "
                       r"What remains, and why does a conditional mean not establish an executable annual return?")
        with self.voiceover(
            "Pause and predict. A chosen overnight rule has four basis points gross per "
            "round trip and five basis points of total round-trip cost. What remains? "
            "Explain why a sample conditional daily mean alone would not establish "
            "the return of a self-financing annual strategy."
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
