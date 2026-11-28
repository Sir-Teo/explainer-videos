"""Parts 36-42."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=36, level="U", widget="saasrun", prereq=(3, 4, 5),
        question="What is a business worth when the second copy costs nothing?",
        story="The part opens on Microsoft's $332bn of revenue and $155bn of operating income in the year to June 2026, with "
              "223,000 employees; licences and devices cost 19 cents to deliver per dollar, services and the cloud 35. The "
              "viewer runs a software company with $200m of ARR and 100 salespeople: a dollar of new subscriptions costs $1.56 "
              "to win and pays back in about two years; with no new hires growth slows from 25% to 13% while the margin climbs "
              "from 23% to 44%; an extra $30m a year split half and half between salespeople and engineers ends with $588m of "
              "ARR, all on engineers with the most cash. Salesforce spends 35 cents a dollar on selling and 14 on engineering; "
              "stock pay reaches 34 cents at Snowflake. Adobe's revenue fell 8% in 2013 as it moved to Creative Cloud, then "
              "grew to $23.8bn, 96% subscriptions. Net revenue retention is 125% at Snowflake; Salesforce holds $72bn of "
              "contracted revenue; Microsoft and Oracle hold $678bn and $638bn, mostly cloud. Microsoft's capital spending "
              "reached $116bn and its gross margin slipped as AI costs real computing; Oracle's free cash flow turned to "
              "-$24bn. Salesforce's $50bn target for fiscal 2026 came in at $41.5bn; the series gives 55% that Microsoft "
              "Cloud reaches $275bn in fiscal 2027.",
        handoff="Part 37, cloud and data centres, follows the money into the buildings where software runs.",
        outside="Fixed and marginal costs; Part 3's accounts and Part 4's cost curve; Part 5's moats; discounting; Economics, "
                "Built's platforms, lock-in and bundling.",
        objectives={
            "U": ["Explain why software's costs are almost all fixed and its largest cost is selling.",
                  "Explain the move from licences to subscriptions and why revenue first falls.",
                  "Explain why retention and lock-in decide what a software company is worth, and how AI changes its costs."],
            "M": ["Compute ARR's change from new business, expansion and churn, and net revenue retention.",
                  "Compute the cost of winning a dollar of new subscriptions, its payback and its lifetime gross profit.",
                  "Compute deferred revenue, remaining performance obligations and the gap between cash flow and profit."],
            "D": ["Read a company's long-range target against its results, and make and state a dated, scorable forecast."],
            "I": ["Read a software company's revenue mix, cost structure and stock pay in its filings.",
                  "Read retention, ARR, backlog and capital spending from software and cloud filings."],
        },
        results=[
            ("ARR's change", r"\\Delta\\text{ARR} = \\text{new} + \\text{expansion} - \\text{churn}"),
            ("Net revenue retention", r"\\text{NRR} = 1 - c + e"),
            ("Payback in months", r"T = 12 \\cdot \\frac{\\text{S\\&M}}{\\text{new ARR} \\times \\text{gross margin}}"),
            ("Lifetime gross profit of $1 of ARR", r"\\sum_{t=0}^{T-1} g\\,\\frac{(1 - c + e)^t}{(1 + r)^t}"),
        ],
        U=(0, 1, 2, 3, 4, 5, "s07_intermission", 6, 7, 8), I=(9,), D=(10,),
        also=(("The Register's rows for Part 36", "explainer/industry/data/rows_p36.py"),
              ("The software company, its cohorts and the J-curve", "explainer/industry/works/saas.py"),
              ("The SEC and FRED extracts", "explainer/industry/data/SOURCES.md")),
    ),
]
