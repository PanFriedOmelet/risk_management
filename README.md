# Risk Measure
### What is a risk measure?
A risk measure works like a score for an exposure. If an exposure has a higher risk, the risk measure should be higher. However, this depends on the properties of risk measures. One of the very popular risk measures is the standard deviation but it does not have the transition invariance property, which is a property that if a certain amount is added to the exposure, the risk measure is deducted by that amount (read more at [Wikipedia](https://en.wikipedia.org/wiki/Coherent_risk_measure)).

### Quantile Function
The quantile function is a risk measure that gives the probability that a random valiable is less than a certain value. In other words, it is the inverse cumulative distribution function of a random variable.

Given that
$$ F_X (x) \coloneqq P(X<x)$$

The quantile function is
$$ Q(p) = F_X^{-1} (p)$$

### Value at Risk
Value at risk (V@R) determines the minimum value that a random variable can fall lower under a certain probability ($1-\alpha$). Note that there are various definitions for V@R and this is just a simplified version.

$$ \text{VaR}_\alpha (X) = -\text{inf}\{x \in \mathbb{R} : F_X (x) > \alpha \} = F_{-X}^{-1} (1-\alpha) $$

### Expected Shortfall
Expected shortfall is a risk measure which estimates the average loss of a random variable. The average loss is the losses at least at the V@R. This means the expected shortfall includes all possibble losses beyond the V@R. 

$$ \text{ES}_\alpha (X) = -\frac{1}{\alpha} \int_0^\alpha \text{VaR}_s (X) ds = -\frac{1}{\alpha} \left(\text{E}[X \cdot 1_{\{X\le\text{VaR}_\alpha (X)\}}] + \text{VaR}_\alpha (X)(\alpha - \text{P}(X \le x_\alpha))\right)$$