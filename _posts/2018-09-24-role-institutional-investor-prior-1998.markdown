---
title: "The Role of Institutional Investor Prior 1998"
layout: post
blog: true
date: 2018-09-24 21:20
headerImage: false
tag:
- test
star: true
category: blog
author: johnewzhang
description: The Role of Institutional Investor Prior 1998
---

We study the role of institutional investors who invest in public traded US companies using WRDS dataset through 1980 to 1997. We find that all institutional investors dislike high volatile stocks. During this period, there is little evidence that active monitoring was done by the independent institutional investors and significantly it shows grey institutions did not intervene with the management of the companies they invested in. 

---

# Introduction 

Asset under management by professional investors is growing fast nowadays. For example,  hedge fund industry alone is managing 3 trillion US dollars by the end of 2017.  Ferreira, Matos (2008) examined the role of institutional investors globally in the firms they invested in during 2000 and 2005. They are interested in whether large investors are effective in influencing corporate management and boards towards creating shareholder value. Independent investors such as hedge fund and mutual fund were found to play a more active monitoring role, while the grey institutions such as bank and insurance companies, who have business relationships with firms, have a tendency to agree with current management. Additionally, they found all institutions favor larger firms than smaller firms. In this paper, we provide a similar analysis about the role of institutional investors on the public traded non-financial US companies prior 1998. 

In the first section, we discuss the data deriving our analysis. The next two sections describe the determinants of institutional ownership and the role of institutional owners on firm's value, performance, and capital expenditure. Lastly, we provide the conclusion and suggestions for future investigations.

# Data Description

Our analysis uses data from CRSP, COMPUSTAT and COMPUSTAT_company. CRSP includes the adjusted stock return (RET), volatility (SIMGA) and institutional ownership information. Due to a severe mapping errors, the institutional ownership information is only correct prior 1998 and this is primarily the constraints for the analysis done in this paper. There are five types of ownership, banks (IOB), insurance companies (IOIC), mutual funds (IOMF), independent investment advisors (IOIA) and others (including pension fund and university endowment fund; IOO). We define banks, insurance companies and others to be grey institutions (IOGREY), and mutual funds and independent investment advisors to be independent institutions (IOINDEP). Our financial statement level data is from COMPUSTAT and COMPUSTAT_company. COMPUSTAT_company provides the industry classifications (DNUM). In our analysis, we remove the financial industry (DNUM between 6000 and 6999) since financial institutions are already complicated investors and should have no impact by institutional ownerships. Table I summarizes the firm characteristics, institutional ownership and operating performance between 1980 and 1997. 

<p align="center"> 
<img src="{{site.base_url}}/assets/images/role_of_institutional_investor_prior_1998/image1.png">
</p>

# The Determinants of Institutional Ownership

We investigate the determinants of institutional ownership similar to the Ferreira, Matos (2008). In their paper, the firm size factor is a strong indicator of ownership preference by all type of investors during 2000 and 2005, while prior 1998, our analysis (Table II) shows that investment opportunity and the stock volatility contributes significantly negative towards the fraction of institutional ownership. In other words, growth companies are likely not to be included in the portfolio of institutional investors in the 80s and 90s. Given at the time, the interest rates were much higher than today so bond investment may be much safer than equities. This may lead to investors' cautious view on growth company stocks. On the other hand, we can infer that institutions may invest more in value companies and even with active monitoring, the change in firms value or operating performance may not be so significant. This is shown in the next section. Additionally, in 80s and 90s, mutual funds were more passive and hedge fund started booming only after the 1996 SEC rule change on governing mutual fund. Much of the active monitoring may arise only in the 2000s. 

<p align="center"> 
<img src="{{site.base_url}}/assets/images/role_of_institutional_investor_prior_1998/image2.png">
</p>

# Institutional Ownership and Firm Performance

In this section, we discuss institutional ownership impact on firm value, operating performance and capital expenditure. For firm value, we are adopting the Toqin's Q as suggested in Ferreira, Matos (2008) in order to get a comparison between the prior 1998 US market and 2000-2005 global performance. We estimate regressions of a firm's Tobin's Q using variables associated with firm value such as size, growth opportunities, leverage and cash holding. Here, we also include analyst coverage as an indicator of how popular a firm is. Our regression shows that the grey institution does not provide active monitoring but the evidence of active monitoring is week. This can be again credit to the smaller size of the independent money management industry so there were not enough variations to demonstrate the significance of active monitoring. 

In addition, we includes the operating performance and capital expenditure analyses in Table III. In both of these analyses, we include book-to-market into part of regression since it often relates to firm performance measure and expenditure structure. Similarly, the return on assets provide the similar results to reinforce the finding. Lastly, due to the weakness of active monitoring, it is not surprised to see the insignificant of the effects on capital expenditure.  

<p align="center"> 
<img src="{{site.base_url}}/assets/images/role_of_institutional_investor_prior_1998/image3.png">
</p>

# Conclusions

Our findings suggest that prior 1998, there are little evidence that independent institution are effective monitors while the grey institution are not providing active monitoring as their ownership has negative impact on the firm value and operating performance. We also document that all institutions share a preference of non-volatile firms prior 1980s as this may provide some reason of the insignificance of active monitoring. In other words, the more stable firms may not have to change their strategy much as suggested by mutual funds or hedge funds. 

Lastly, if correct mapping data for institutional ownership is provided after 1998, we should see the significance of active monitoring from independent investors. For example, Brav, Jiang, Partnoy, Thomas (2008) shows some evidence of hedge fund activism on value creation. 

---

## Varialble Definitions

<p align="center"> 
<img src="{{site.base_url}}/assets/images/role_of_institutional_investor_prior_1998/image4.png">
</p>

## References

* Ferreira, M., Matos, P., 2008. The colors of investors' money: The role of institutional investors around the world. Journal of Financial Economics 88, 499-533.
* Brav, A., Jiang, W., Partnoy, F., Thomas, R., 2008. Hedge fund activism, corporate governance, and firm performance. Journal of Finance Vol LXIII, No. 4. 
