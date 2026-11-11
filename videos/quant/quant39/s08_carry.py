from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant39.common import BAD, GOOD, HURDLE, PART, PERP_C, SPOT_C


class Carry(VoiceoverScene):
    def construct(self):
        self.card()
        self.book()
        self.capital()
        self.basis()
        self.negative()
        self.costs()
        self.margin()
        self.venue()
        self.custody()
        self.research()
        self.premium()
        self.question()

    def card(self):
        head = label('The carry trade: accounting and risks', font_size=32, color=HURDLE).to_edge(UP, buff=0.4)
        cards = VGroup(
            desk_question('matched units', 'long one unit of spot; short one linear perpetual unit', width=12.1, font_size=28),
            desk_question('gross ledger', 'funding received plus the change in $S-F$', width=12.1, font_size=28),
            desk_question('scope', 'chosen examples; no historical strategy result or investment approval', width=12.1, font_size=28),
        ).arrange(DOWN, buff=0.28)
        cards.next_to(head, DOWN, buff=0.4)
        with self.voiceover("Chapter seven. The answer to the pause is that funding can turn negative, basis can move, and margin can be exhausted before a spot gain can be transferred. <bookmark mark='a'/> Match one unit of spot against one unit of a linear perpetual. <bookmark mark='b'/> Common price movement largely cancels, but the basis and funding remain. <bookmark mark='c'/> We will work through chosen accounting examples and venue stresses. They demonstrate mechanisms, without reporting a fitted carry strategy, an opened hold-out or an approved trading book.") as vo:
            self.play(FadeIn(head), FadeIn(cards[0]))
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            self.play(FadeIn(cards[1]))
            vo.wait_until("c")
            self.play(FadeIn(cards[2]))
        self.wait(0.5)
        self.clear_scene()

    def book(self):
        head = label('One matched-unit ledger', font_size=32, color=HURDLE).to_edge(UP, buff=0.4)
        cards = VGroup(
            desk_question('price legs', '$\\Pi_{\\rm price}=\\Delta S-\\Delta F=-\\Delta(F-S)$', width=12.1, font_size=28),
            desk_question('funding and costs', '$\\Pi=\\sum_j f_j F_j-\\Delta(F-S)-C$', width=12.1, font_size=28),
            desk_question('conventions', 'one unit maintained; linear contract; funding on settlement notional', width=12.1, font_size=28),
        ).arrange(DOWN, buff=0.28)
        cards.next_to(head, DOWN, buff=0.4)
        with self.voiceover("Write the ledger in dollars for one maintained unit. <bookmark mark='a'/> The spot earns its price change and the short perpetual loses the perpetual's price change. Their sum is minus the change in basis, perpetual minus spot. <bookmark mark='b'/> Add each funding rate times the settlement notional, then subtract commissions, spreads, borrowing and transfer costs. <bookmark mark='c'/> This convention is for a linear contract and a fixed unit quantity. Inverse contracts, changing quantities and collateral denominated in a volatile coin require different ledgers.") as vo:
            self.play(FadeIn(head), FadeIn(cards[0]))
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            self.play(FadeIn(cards[1]))
            vo.wait_until("c")
            self.play(FadeIn(cards[2]))
        self.wait(0.5)
        self.clear_scene()

    def capital(self):
        head = label('Capital is a denominator, not a hedge', font_size=32, color=HURDLE).to_edge(UP, buff=0.4)
        cards = VGroup(
            desk_question('chosen start', '$S_0=F_0=100;\\quad m=1/3$', width=12.1, font_size=28),
            desk_question('capital committed', '$K=100+100/3=133.33$', width=12.1, font_size=28),
            desk_question('one settlement', '$f=0.01\\%\\Rightarrow \\Pi_f=0.01;\\quad \\Pi_f/K=0.0075\\%$', width=12.1, font_size=28),
        ).arrange(DOWN, buff=0.28)
        cards.next_to(head, DOWN, buff=0.4)
        with self.voiceover("Choose spot and perpetual prices of one hundred, and cash collateral equal to one third of the short's notional. <bookmark mark='a'/> Buying the spot uses one hundred dollars; margin uses thirty-three dollars and a third. <bookmark mark='b'/> Total committed capital is therefore one hundred thirty-three and a third before a liquidity buffer. <bookmark mark='c'/> A funding rate of one hundredth of a percent pays one cent on the one-hundred-dollar short, or zero point zero zero seven five percent of committed capital. Margin is committed cash, while a buffer increases the denominator further.") as vo:
            self.play(FadeIn(head), FadeIn(cards[0]))
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            self.play(FadeIn(cards[1]))
            vo.wait_until("c")
            self.play(FadeIn(cards[2]))
        self.wait(0.5)
        self.clear_scene()

    def basis(self):
        head = label('Funding can be smaller than a basis move', font_size=32, color=HURDLE).to_edge(UP, buff=0.4)
        cards = VGroup(
            desk_question('chosen settlement', '$\\Pi_f=+0.01;\\quad F-S:0\\to0.20$', width=12.1, font_size=28),
            desk_question('price-leg loss', '$\\Delta S-\\Delta F=-0.20$', width=12.1, font_size=28),
            desk_question('net before costs', '$\\Pi=-0.19;\\quad \\Pi/K=-0.1425\\%$', width=12.1, font_size=28),
        ).arrange(DOWN, buff=0.28)
        cards.next_to(head, DOWN, buff=0.4)
        with self.voiceover("Use that same chosen funding settlement. <bookmark mark='a'/> Funding pays one cent, but the perpetual's premium widens from zero to twenty cents. <bookmark mark='b'/> The matched price legs lose twenty cents, regardless of whether both market prices rose or fell together. <bookmark mark='c'/> Net profit before other costs is minus nineteen cents, about minus fourteen basis points of the original capital. The size of a small funding payment does not bound a temporary basis move, and perpetual convergence has no fixed expiry date.") as vo:
            self.play(FadeIn(head), FadeIn(cards[0]))
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            self.play(FadeIn(cards[1]))
            vo.wait_until("c")
            self.play(FadeIn(cards[2]))
        self.wait(0.5)
        self.clear_scene()

    def negative(self):
        head = label('A quoted funding rate is not a promise', font_size=32, color=HURDLE).to_edge(UP, buff=0.4)
        cards = VGroup(
            desk_question('chosen negative rate', '$f=-0.02\\%;\\quad F=100$', width=12.1, font_size=28),
            desk_question('short pays', '$\\Pi_f=-0.02$', width=12.1, font_size=28),
            desk_question('rule risk', 'future funding, caps, settlement intervals and eligibility can change', width=12.1, font_size=28),
        ).arrange(DOWN, buff=0.28)
        cards.next_to(head, DOWN, buff=0.4)
        with self.voiceover("Now choose a negative funding rate of two hundredths of a percent. <bookmark mark='a'/> On one hundred dollars of perpetual notional, the short pays two cents instead of receiving funding. <bookmark mark='b'/> The long spot does not reimburse that payment. A decision made from a trailing average cannot lock in future rates. <bookmark mark='c'/> Contract caps, settlement intervals, mark conventions and collateral eligibility can also change. Historical average funding is a description of past payments, rather than a contractual yield available at entry.") as vo:
            self.play(FadeIn(head), FadeIn(cards[0]))
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            self.play(FadeIn(cards[1]))
            vo.wait_until("c")
            self.play(FadeIn(cards[2]))
        self.wait(0.5)
        self.clear_scene()

    def costs(self):
        head = label('A cost hurdle in matching units', font_size=32, color=HURDLE).to_edge(UP, buff=0.4)
        cards = VGroup(
            desk_question('chosen entry cost', '$C_{\\rm entry}=0.0015\\times100=0.15$', width=12.1, font_size=28),
            desk_question('exit also charged', '$C_{\\rm round}=0.30$', width=12.1, font_size=28),
            desk_question('simple hurdle', '$0.30/0.01=30$ unchanged positive settlements, before other risks', width=12.1, font_size=28),
        ).arrange(DOWN, buff=0.28)
        cards.next_to(head, DOWN, buff=0.4)
        with self.voiceover("Choose a combined entry charge of fifteen basis points of spot notional, and the same again to leave. <bookmark mark='a'/> Entry costs fifteen cents, exit another fifteen, for thirty cents in all. <bookmark mark='b'/> If the one-cent funding payment stayed unchanged and basis did not move, thirty settlements would merely cover those charges. <bookmark mark='c'/> This simple count excludes financing, slippage, transfer delays and the time value of money. A quoted annualized funding number hides both the notional used for costs and the capital needed to earn it.") as vo:
            self.play(FadeIn(head), FadeIn(cards[0]))
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            self.play(FadeIn(cards[1]))
            vo.wait_until("c")
            self.play(FadeIn(cards[2]))
        self.wait(0.5)
        self.clear_scene()

    def margin(self):
        head = label('A solvent hedge can still be liquidated', font_size=32, color=HURDLE).to_edge(UP, buff=0.4)
        cards = VGroup(
            desk_question('chosen rally', '$S,F:100\\to150$', width=12.1, font_size=28),
            desk_question('separate accounts', 'spot gain $+50$; short variation loss $-50$', width=12.1, font_size=28),
            desk_question('liquidity gap', 'initial margin $33.33<50$; maintenance and transfer timing matter', width=12.1, font_size=28),
        ).arrange(DOWN, buff=0.28)
        cards.next_to(head, DOWN, buff=0.4)
        with self.voiceover("Choose a rally from one hundred to one hundred fifty on both legs. <bookmark mark='a'/> The spot gains fifty and the perpetual short loses fifty before funding and costs, so the economic price hedge still balances. <bookmark mark='b'/> But fifty of variation loss exceeds the original thirty-three dollars of collateral if the accounts cannot transfer gains promptly. <bookmark mark='c'/> Actual liquidation depends on maintenance margin, marks, collateral value and venue rules, so this example is a cash-flow stress rather than an exact liquidation threshold. A balance-sheet hedge does not supply intraday liquidity.") as vo:
            self.play(FadeIn(head), FadeIn(cards[0]))
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            self.play(FadeIn(cards[1]))
            vo.wait_until("c")
            self.play(FadeIn(cards[2]))
        self.wait(0.5)
        self.clear_scene()

    def venue(self):
        head = label('Stress the loss where collateral sits', font_size=32, color=HURDLE).to_edge(UP, buff=0.4)
        cards = VGroup(
            desk_question('chosen exposure', 'venue collateral $33.33$ of capital $133.33$', width=12.1, font_size=28),
            desk_question('zero recovery stress', '$33.33/133.33=25\\%$ loss of initial capital', width=12.1, font_size=28),
            desk_question('limits', 'other custody losses, netting, recoveries and collateral calls remain separate', width=12.1, font_size=28),
        ).arrange(DOWN, buff=0.28)
        cards.next_to(head, DOWN, buff=0.4)
        with self.voiceover("Suppose, as a chosen stress, only the thirty-three dollars of margin is held at a venue and that exposure has zero recovery. <bookmark mark='a'/> The loss is a quarter of the initial one hundred thirty-three dollars of capital. <bookmark mark='b'/> That is an accounting scenario, not a default probability or a forecast of legal recovery. <bookmark mark='c'/> If the spot is also held there, the exposure may be much larger; close-out claims, netting and rehypothecation change it again. Position size needs an exposure map as well as a return estimate.") as vo:
            self.play(FadeIn(head), FadeIn(cards[0]))
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            self.play(FadeIn(cards[1]))
            vo.wait_until("c")
            self.play(FadeIn(cards[2]))
        self.wait(0.5)
        self.clear_scene()

    def custody(self):
        head = label('Custody and liquidity pull in different directions', font_size=32, color=HURDLE).to_edge(UP, buff=0.4)
        cards = VGroup(
            desk_question('separation', 'custody outside a trading venue may reduce one exposure', width=12.1, font_size=28),
            desk_question('friction', 'posting, recall rights and transfers depend on enforceable arrangements', width=12.1, font_size=28),
            desk_question('buffer', 'extra collateral reduces liquidation pressure but increases committed capital', width=12.1, font_size=28),
        ).arrange(DOWN, buff=0.28)
        cards.next_to(head, DOWN, buff=0.4)
        with self.voiceover("Custody outside the trading venue may reduce one form of venue exposure. <bookmark mark='a'/> It does not automatically let the trader post collateral, recall it instantly or spend an unrealized spot gain. Those rights depend on contracts and operations. <bookmark mark='b'/> Multiple venues can fail together or suspend transfers together, especially when they share banks or a stablecoin. <bookmark mark='c'/> Larger buffers lower some liquidation risks but tie up more capital. A useful stress combines correlated venue loss, adverse basis and delayed collateral movement instead of assuming each happens in isolation.") as vo:
            self.play(FadeIn(head), FadeIn(cards[0]))
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            self.play(FadeIn(cards[1]))
            vo.wait_until("c")
            self.play(FadeIn(cards[2]))
        self.wait(0.5)
        self.clear_scene()

    def research(self):
        head = label('What an admissible research design must specify', font_size=32, color=HURDLE).to_edge(UP, buff=0.4)
        cards = VGroup(
            desk_question('before outcomes', 'define contract, units, cost model, signal timing and eligible venues', width=12.1, font_size=28),
            desk_question('separate windows', 'past-only selection; untouched evaluation; all configurations counted', width=12.1, font_size=28),
            desk_question('research scope', 'accounting stresses do not provide historical performance or independent strategy validation', width=12.1, font_size=28),
        ).arrange(DOWN, buff=0.28)
        cards.next_to(head, DOWN, buff=0.4)
        with self.voiceover("A research protocol begins before seeing evaluation outcomes. <bookmark mark='a'/> Specify the contract, funding clock, capital denominator, fee model, transfer rules, signal information and venue eligibility. <bookmark mark='b'/> Select only on past information, count every configuration, and reserve an untouched evaluation window. Delisting and venue failure belong in the design, with assumptions made visible. <bookmark mark='c'/> An accounting illustration cannot supply historical performance evidence or be described as an independently validated investment strategy.") as vo:
            self.play(FadeIn(head), FadeIn(cards[0]))
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            self.play(FadeIn(cards[1]))
            vo.wait_until("c")
            self.play(FadeIn(cards[2]))
        self.wait(0.5)
        self.clear_scene()

    def premium(self):
        head = label('Carry can compensate several risks at once', font_size=32, color=HURDLE).to_edge(UP, buff=0.4)
        cards = VGroup(
            desk_question('receipts', 'funding may compensate leverage demand and market frictions', width=12.1, font_size=28),
            desk_question('exposures', 'basis, funding reversal, collateral, venue, token and legal risks', width=12.1, font_size=28),
            desk_question('decision', 'proposed limits require evidence; smooth returns do not prove small tail loss', width=12.1, font_size=28),
        ).arrange(DOWN, buff=0.28)
        cards.next_to(head, DOWN, buff=0.4)
        with self.voiceover("Why might someone pay the other side? <bookmark mark='a'/> Demand for leveraged directional exposure and limits on arbitrage capital can support positive funding, but that explanation is a hypothesis to test. <bookmark mark='b'/> A matched-unit book still bears basis, funding-reversal, collateral, venue, stablecoin, operational and legal risks. Their relative importance depends on the actual arrangement. <bookmark mark='c'/> A smooth return series can miss a rare loss and cannot by itself justify a large position. Proposed limits should be tested against both cash-flow stresses and enforceable custody rights.") as vo:
            self.play(FadeIn(head), FadeIn(cards[0]))
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            self.play(FadeIn(cards[1]))
            vo.wait_until("c")
            self.play(FadeIn(cards[2]))
        self.wait(0.5)
        self.clear_scene()

    def question(self):
        head = label('Pause and predict', font_size=32, color=HURDLE).to_edge(UP, buff=0.4)
        cards = VGroup(
            desk_question('chosen stablecoin scenario', '8\\% of reserves temporarily inaccessible; the other 92\\% at par', width=12.1, font_size=28),
            desk_question('zero-recovery accounting', 'asset value would be 0.92 per token before other claims', width=12.1, font_size=28),
            desk_question('question', 'Does a market quote of 0.88 identify insolvency, illiquidity, or neither?', width=12.1, font_size=28),
        ).arrange(DOWN, buff=0.28)
        cards.next_to(head, DOWN, buff=0.4)
        with self.voiceover("Pause and predict. Choose a token with eight percent of its reserves temporarily inaccessible at a failed bank, and suppose the remaining ninety-two percent is immediately worth par. <bookmark mark='a'/> Under zero recovery, simple asset accounting gives ninety-two cents per token before any other claims or costs. <bookmark mark='b'/> Now suppose the market quote is eighty-eight cents. <bookmark mark='c'/> Does that quote identify insolvency, illiquidity, or neither? State what you would need to know about redemption access, reserve valuation, the quote currency and the timing before deciding.") as vo:
            self.play(FadeIn(head), FadeIn(cards[0]))
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            self.play(FadeIn(cards[1]))
            vo.wait_until("c")
            self.play(FadeIn(cards[2]))
        self.wait(6)
        self.clear_scene()
