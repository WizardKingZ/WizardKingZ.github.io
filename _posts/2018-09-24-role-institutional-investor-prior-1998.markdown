---
title: "The Role of Institutional Investors Prior to 1998"
date: 2018-09-24 21:20
pillar: academic
series: research
topic: corporate finance
summary: "Institutional ownership of US non-financial firms, 1980–1997: every type of institution avoids volatile stocks, and independent institutions show little sign of active monitoring."
tags: ["finance", "panel regression", "institutional investor", "research"]
---

I study the role of institutional investors in publicly traded US companies, using WRDS data from 1980 to 1997. I find that all institutional investors dislike highly volatile stocks. During this period, independent institutional investors show little evidence of active monitoring, and the evidence significantly shows that grey institutions do not intervene in the management of the companies they invest in.

---

## Introduction

Assets under management by professional investors are growing fast. The hedge fund industry alone managed US$3tn by the end of 2017. Ferreira, Matos (2008) examined the role of institutional investors globally in the firms they invested in between 2000 and 2005. They asked whether large investors effectively influence corporate management and boards toward creating shareholder value. They found that independent investors such as hedge funds and mutual funds play a more active monitoring role, while grey institutions such as banks and insurance companies, which have business relationships with firms, tend to agree with current management. They also found that all institutions favor larger firms over smaller ones. I provide a similar analysis of the role of institutional investors in publicly traded non-financial US companies prior to 1998.

I first describe the data. The next two sections examine the determinants of institutional ownership and the effect of institutional owners on a firm's value, performance, and capital expenditure. The last section concludes and suggests future work.

## Data Description

My analysis uses data from CRSP, COMPUSTAT, and COMPUSTAT_company. CRSP provides the adjusted stock return (RET), volatility (SIGMA), and institutional ownership. Because of severe mapping errors, the institutional ownership data are correct only prior to 1998, which is the main constraint on my analysis. There are five types of owners: banks (IOB), insurance companies (IOIC), mutual funds (IOMF), independent investment advisors (IOIA), and others, including pension funds and university endowment funds (IOO). I define banks, insurance companies, and others as grey institutions (IOGREY), and mutual funds and independent investment advisors as independent institutions (IOINDEP). My financial statement data come from COMPUSTAT and COMPUSTAT_company; COMPUSTAT_company provides the industry classifications (DNUM). I remove the financial industry (DNUM between 6000 and 6999) because financial institutions are already complex investors and should be unaffected by institutional ownership. Table I summarizes firm characteristics, institutional ownership, and operating performance between 1980 and 1997.

![Table I: Firm characteristics, institutional ownership, and operating performance, 1980–1997](/assets/images/role_of_institutional_investor_prior_1998/image1.png)

## The Determinants of Institutional Ownership

Prior to 1998, investment opportunity and stock volatility contribute significantly negatively to the fraction of institutional ownership (Table II). I follow the approach of Ferreira, Matos (2008), who found that firm size strongly predicts ownership by all types of investors between 2000 and 2005. My results mean that institutional investors in the 1980s and 1990s were unlikely to hold growth companies. Interest rates were much higher than today, so bonds may have been a much safer investment than equities, which may explain investors' caution toward growth stocks. By the same logic, institutions may invest more in value companies, whose value or operating performance may change little even with active monitoring, as the next section shows. Mutual funds were also more passive in the 1980s and 1990s, and hedge funds started booming only after the 1996 SEC rule change governing mutual funds, so much of the active monitoring may arise only in the 2000s.

![Table II: Determinants of institutional ownership](/assets/images/role_of_institutional_investor_prior_1998/image2.png)

## Institutional Ownership and Firm Performance

This section examines how institutional ownership affects firm value, operating performance, and capital expenditure. I measure firm value with Tobin's Q, as in Ferreira, Matos (2008), so that I can compare the pre-1998 US market with global results for 2000–2005. I regress a firm's Tobin's Q on variables associated with firm value: size, growth opportunities, leverage, and cash holdings. I also include analyst coverage as a measure of how popular a firm is. My regression shows that grey institutions do not provide active monitoring, while the evidence of active monitoring by independent institutions is weak. This weakness again likely reflects the smaller size of the independent money management industry at the time, which provides too little variation to detect active monitoring.

Table III extends the analysis to operating performance and capital expenditure. Both regressions include book-to-market because it often relates to firm performance and expenditure structure. Return on assets gives similar results, reinforcing the finding. Because active monitoring is weak, the insignificant effect on capital expenditure is not surprising.

![Table III: Institutional ownership, operating performance, and capital expenditure](/assets/images/role_of_institutional_investor_prior_1998/image3.png)

## Conclusions

Prior to 1998, there is little evidence that independent institutions are effective monitors, and grey institutions do not provide active monitoring: their ownership has a negative effect on firm value and operating performance. I also document that all institutions share a preference for non-volatile firms prior 1980s, which may partly explain the insignificance of active monitoring: more stable firms may need few of the strategy changes that mutual funds or hedge funds would suggest.

With correctly mapped institutional ownership data after 1998, I expect active monitoring by independent investors to become significant. For example, Brav, Jiang, Partnoy, Thomas (2008) show some evidence that hedge fund activism creates value.

---

### Variable Definitions

![Variable definitions](/assets/images/role_of_institutional_investor_prior_1998/image4.png)

### References

* Ferreira, M., Matos, P., 2008. The colors of investors' money: The role of institutional investors around the world. Journal of Financial Economics 88, 499-533.
* Brav, A., Jiang, W., Partnoy, F., Thomas, R., 2008. Hedge fund activism, corporate governance, and firm performance. Journal of Finance Vol LXIII, No. 4.
