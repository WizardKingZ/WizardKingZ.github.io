---
title: "Investing as System Design"
date: 2026-10-24 21:00
pillar: investing
series: essays
topic: framework
math: true
summary: "Where my investing comes from: model the structure of a system, test it with data, and design a solution around a defined objective, at the level of the company and the portfolio."
tags: ["investing", "asset pricing", "corporate finance", "financials", "framework"]
---

## Two levels of the same question

In December 2016, before starting a master's in financial economics, I wrote that I wanted to learn how capital is allocated efficiently at two levels: inside a single company and across a portfolio. Ten years later, I still work on those two questions. What has changed is how I answer them: I start with the structure of the system, test it against data, and design a solution around a defined objective.

The same letter listed two side interests, leverage and illiquidity. My path has run through actuarial work, private credit, asset-based finance, special situations, and public markets. This essay traces how each step shaped the habit.

## Math and actuarial work taught me to price risk

My undergraduate training combined pure mathematics, finance, and computer science. My first career was as a property and casualty actuary, in reserving, pricing, and analytics. Both taught me to treat a problem as a system: define the parts, write down how they interact, then solve.

Actuarial work is about pricing risk and managing it, and that made my framework risk-first. A premium or a reserve is a judgment about outcomes that have not happened yet, made from incomplete data. I apply the same discipline to every risk I take: business risk, deal risk, credit risk, and factor risk. Each one has to be named, priced, and managed before the return case counts.

What these tools did not give me was judgment about which problems were worth solving. Give me a well-posed problem and I can model it, prove it, or code it. Deciding which problem to pose is economics.

## At the portfolio level, I model the system before I test it

Financial economics supplied the questions, starting with asset pricing. Every asset reduces to one line: price equals expected payoff, discounted by how much investors value money in the states where that payoff arrives. In symbols, with p the price, x the payoff, and m the stochastic discount factor:

$$
p = E[m \, x]
$$

The disagreement is over how to fill in m. The reduced-form approach starts from the data: find portfolios that explain returns and call them factors. The structural approach starts from the investor's problem: ask what a long-horizon investor fears, then test whether those fears are priced. I belong to the second camp. Merton's intertemporal CAPM (1973) says investors care not only about today's return but about news that changes tomorrow's opportunities. Campbell and Shiller (1988) showed that valuation ratios carry that news, because discount rates, not only cash flows, move prices.

My master's thesis tested this view. I replicated two ICAPM models, Campbell and Vuolteenaho (2004) and Campbell, Giglio, Polk and Turley (2018), on US equities from 1963 to 2018, then took them out of sample to equity strategies and currency carry trades. Exposure to news about future market volatility did most of the work in separating small and value stocks from the rest, and the models showed some ability to price those strategies ([thesis summary](/icapm-evidence/)).

What I took from the thesis was less a finding than a method. A regression shows that a pattern exists. A structural model explains why: it writes down how the system works, from what investors fear to the state variables that carry that fear, then tests each link against data. The thesis took a full model of where returns come from, starting from fundamentals, and let the data accept or reject it.

I have worked that way since, and it is how I came to see investing as a system-design problem. A strategy is reliably profitable only once you understand the system that pays it. Otherwise it is a pattern waiting to stop working.

The thesis also left me cycle-aware. Investors pay to avoid more than lost cash flow; they also pay to avoid bad news about future volatility and, to a lesser degree, about discount rates. Both swing with the cycle. Patient capital gets paid when discount rates are high, which is exactly when most investors cannot wait.

## I chose businesses over signals

The 2016 letter ended with a plan to run a quantitative hedge fund. I did not follow it, for two reasons.

The first is that insurance had already shown me I like businesses: how a company prices risk, funds itself, and earns its return. I wanted to point quantitative skills and a quantitative mindset at those problems, not at the search for signals in prices.

The second is candor about my edge. I do not expect to out-compute the market, or to win a race on speed or on spotting patterns others miss. When I win, it is because I understand a system better than its price does. That pointed me toward businesses, contracts, and capital structures, where patient understanding gets paid.

## At the company level, control decides the payoff

Asset pricing values a claim once its payoff is given. Corporate finance asks who shapes the payoff. Modigliani and Miller (1958) describe a world where capital structure does not matter. The rest of the field explains why it does, and the part that shaped me most is control.

Contract theory, where [Patrick Bolton](https://business.columbia.edu/faculty/people/patrick-bolton) at Columbia did much of the work on financial contracts, starts from the fact that contracts are incomplete. No document anticipates every state of the world, so what matters is who decides when the unforeseen happens.

- **Debt allocates control by state.** In [Aghion and Bolton (1992)](https://ideas.repec.org/a/oup/restud/v59y1992i3p473-494..html), the founder runs the firm while things go well, and control passes to the lender when they do not.
- **The shape of the creditor group sets the endgame.** Bolton and Scharfstein (1996) show that spreading debt across more creditors deters strategic default but makes renegotiation harder when default is genuine.

Restructuring is this game played live. Each class of claim holds a different payoff, and the outcome follows whoever controls the next decision. Liability management exercises are the modern example: a document that looked protective on day one can be turned against the lenders who relied on it.

Venture debt is my favorite puzzle in the field. Why lend to a company with no earnings? [Hochberg, Serrano and Ziedonis (2018)](https://www.nber.org/papers/w20587) find the answer outside the borrower: patents that can be resold, and the credibility of the venture investors' commitment to keep funding. The lender underwrites the collateral and the sponsor's incentives, not the income statement.

This is why governance and incentives come first in [my order of analysis](/investment-principles-v1/). Before I model fundamentals, I want to know who decides, what they are paid to want, and what the documents let them do.

## Investing is a design problem

Put the two levels together and investing becomes a system-design problem. A strategy earns money for a reason, and the reason sits in the structure: who bears which risk, who controls which decision, and what the price assumes. Once I understand that, the rest is design. I have an objective (a return at a given level of risk) and constraints (liquidity, leverage, time horizon, and what can be known). The job is to build the mix of instrument, structure, and position size that meets the objective within those constraints.

When I say system, I mean what Ray Dalio (2013) calls the economic machine: the whole global economy. A company or a household is a subsystem inside it.

Rates, liquidity, credit, and growth set the discount rate on which every asset is priced, and financial institutions sit closest to that machine. So I work in two directions at once. Top-down, the macro view sets the portfolio's exposures and risk budget. Bottom-up, company-level work decides which claims fill it. Both directions are structural: I model the macro the same way I model a balance sheet, by writing down how the parts connect and then testing it. Portfolio construction is where the two meet, and each position is judged by how it changes the risk of everything else I hold.

Capital solutions and public markets pose the same design problem through different games. In capital solutions, the game is control, and the borrower can be a company or a household. With a company, each deal is an incomplete contract written for the states where things go wrong. The investor decides who holds control in those states and what that control is worth. With households, buying portfolios of non-performing loans is the classic version. The borrowers have already defaulted, so the return depends on the purchase price, the servicer's workout decisions, and the recovery curve across thousands of loans.

In public markets, the game is information. [Glosten](https://business.columbia.edu/faculty/people/lawrence-glosten) and Milgrom (1985) show that the bid-ask spread is what a market maker charges for trading against people who may know more. Every trade has someone on the other side, so the first question is what I know that they do not. Research earns a return only on information that is costly to collect and not yet in the price (Grossman and Stiglitz, 1980). If I cannot name that information, I am probably the one paying the spread.

Financial institutions sit where the two problems meet. A bank, an insurer, or a specialty lender is a balance sheet of contracts, priced by a market whose discount rate swings with the cycle. These institutions also run on leverage and liquidity, my two side interests from 2016. That is why I specialize in them, and why one view can be expressed through equity, credit, or structured paper.

## Markets adapt, so the framework is only v1.0

The 2016 letter also named an interest in Andrew Lo's Adaptive Markets Hypothesis (2004), which he later expanded in *Adaptive Markets* (2017). Lo describes markets less as a fixed equilibrium than as an ecosystem: a strategy that works attracts capital until it stops working. I still think that is right, and it has a personal consequence. A framework that never changes will eventually be priced out.

That is why I called [my principles v1.0](/investment-principles-v1/), and why I treat curiosity as part of the method rather than a personality trait. Most of what I use today, from venture debt to the macro work behind the [Trident Macro Monitor](/macro-monitor/), I learned because a question would not leave me alone.

Project Trident is the current version of this approach. I define it as a structural model of financial institutions and the markets that price them, run as a repeatable process. It works out how each institution makes and loses money, finds where the market misprices it, chooses the claim that best expresses the view, and sizes and monitors that claim within a portfolio. The three prongs are long/short financials equity, asset-based and structured credit, and special situations, which share one underwriting process and one macro view underneath. Put simply, Trident is a system I am building to understand other systems. I will open it one piece at a time in later essays.

## The short version

Structure tells me what can happen. Data tells me what is likely. Design decides what I own and how I am protected if I am wrong. Curiosity keeps all three current.

## References

- Aghion, P. and Bolton, P. (1992). An Incomplete Contracts Approach to Financial Contracting. *Review of Economic Studies*. [link](https://ideas.repec.org/a/oup/restud/v59y1992i3p473-494..html)
- Bolton, P. and Scharfstein, D. (1996). Optimal Debt Structure and the Number of Creditors. *Journal of Political Economy*.
- Campbell, J. and Shiller, R. (1988). The Dividend-Price Ratio and Expectations of Future Dividends and Discount Factors. *Review of Financial Studies*.
- Campbell, J. and Vuolteenaho, T. (2004). Bad Beta, Good Beta. *American Economic Review*.
- Campbell, J., Giglio, S., Polk, C. and Turley, R. (2018). An Intertemporal CAPM with Stochastic Volatility. *Journal of Financial Economics*.
- Dalio, R. (2013). How the Economic Machine Works. Bridgewater Associates (video).
- Glosten, L. and Milgrom, P. (1985). Bid, Ask, and Transaction Prices in a Specialist Market with Heterogeneously Informed Traders. *Journal of Financial Economics*. [author page](https://business.columbia.edu/faculty/people/lawrence-glosten)
- Grossman, S. and Stiglitz, J. (1980). On the Impossibility of Informationally Efficient Markets. *American Economic Review*.
- Hochberg, Y., Serrano, C. and Ziedonis, R. (2018). Patent Collateral, Investor Commitment, and the Market for Venture Lending. *Journal of Financial Economics*. [NBER version](https://www.nber.org/papers/w20587)
- Lo, A. (2004). The Adaptive Markets Hypothesis. *Journal of Portfolio Management*.
- Lo, A. (2017). *Adaptive Markets: Financial Evolution at the Speed of Thought*. Princeton University Press.
- Merton, R. (1973). An Intertemporal Capital Asset Pricing Model. *Econometrica*.
- Modigliani, F. and Miller, M. (1958). The Cost of Capital, Corporation Finance and the Theory of Investment. *American Economic Review*.
- Zhang, J. (2019). Essay on Asset Returns with Intertemporal CAPM. [link](/icapm-evidence/)
