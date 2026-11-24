# Chapter 4 — Find whose errors the average hides

*An equal false-alarm rate is not an equal chance of getting help.*

A fictional consortium wants to flag requests that need a staff follow-up. Staff are concerned that one channel gets less help. An automated report says the false-alarm rate is ten percent in both channels and concludes the tool is treating them the same. The number is right. The conclusion quietly chose which mistake matters.

**By the end:** read a confusion table with correct denominators, distinguish error probabilities from the burden borne by people, and write a review recommendation that does not fabricate a cause.

## Count the people in the question you are asking

In this exercise a positive reference label means a request needed follow-up under a written independent review rubric. A predicted positive means the classifier proposed a follow-up. These are observable roles, not moral judgments. The example uses fictional channels, not protected groups or real customer records. Assume one row per request in this fixture; we have not established equal quality of review labels across channels.

| Channel | True positive | False negative | False positive | True negative | Total |
| --- | ---: | ---: | ---: | ---: | ---: |
| Web | 16 | 4 | 8 | 72 | 100 |
| Desk | 30 | 20 | 5 | 45 | 100 |

**First attempt:** Write questions beginning “among the ones that needed help,” “among the ones that did not,” and “among the ones we flagged.” Choose a numerator and denominator for each before dividing. Then name who bears the burden if a request misses the flag.

A miss is a false negative. Its frequency among reference-positive requests is 4/20 = 20% for Web and 20/50 = 40% for Desk. The corresponding true-positive rates, or fractions of needed cases flagged, are 80% and 60%. The false-alarm rate among reference-negative requests is 8/80 = 10% for Web and 5/50 = 10% for Desk. Equality on that particular rate does not erase the twenty-point miss-rate difference.

A queue manager may ask a different question: “Of those we flag, how many need help?” Answer with precision, 16/24 or 2/3 for Web and 30/35 or 6/7 for Desk. This time the denominator contains predicted positives, not reference positives. The overall flag rates are 24/100 and 35/100. Even the number of unnecessary flags differs, eight versus five, although the rates conditional on reference negatives match. Three questions, three different denominators. A choice of denominator is a choice about who is at risk of the error you are counting.

The pooled miss rate is 24/70 ≈ 34.3%, not the unweighted mean of 20% and 40%. Pooling weights channels by how many labeled needs they have. Averaging two rates equally instead weights each channel once. Either can answer a defined aggregation question, but reporting only one pooled number hides the difference a supervisor asked about.

## Separate the symptom from its possible causes

These are outcome differences in the toy reviewed records; they are not proof that the predictor, the interface, staff practice or the channel itself caused them. The label can embed a previous service decision. If only people who got help ever have true need verified, a classifier can appear to miss few genuine needs because unserved requests never receive an independent label. A label audit begins where those records disappear. Draw and independently review a privacy-preserving sample of both flagged and unflagged requests with a written rubric, measure missingness by channel and preserve disagreements. Do not close the audit simply because two reviewers agree if they both relied on the same incomplete queue log.

The rates are not meaningless because the labels may be imperfect. They identify a specific pattern worth investigating. Write it with its boundary: “In these labeled records, the fraction of requests needing follow-up that are missed is higher at Desk. Label completeness and the causes of the gap have not been established.” That sentence allows a responsible action: keep staff review available, inspect the missing-label mechanism, and check whether the result persists on a fresh sample before treating the difference as a reason to automate more decisions.

## Decide what the metric is meant to protect

Choosing one statistic optimizes the review for one concern. A Desk worker worried about overlooked requests may prioritize miss rates. A supervisor worried about a queue too large to process may prioritize precision and count staffing burden. An affected person may care about time to receive help or access to an appeal. A measure can be relevant without being sufficient. Ask whose costs are counted, who owns the decision, and what compromise is allowed. The independently stated policy, not the generated report, determines whether to expand, restrict or halt.

[Hardt, Price and Srebro](https://arxiv.org/abs/1610.02413) define group criteria for supervised predictions under stated labels and attributes. They do not supply a fairness certification for this fixture. Here a comparison of true-positive rates is one conditional question, not a substitute for checking the labels, investigating who is missing and hearing from affected people. This exercise does not infer anything about legal compliance.

## Graduated practice

- **Warm-up · locate:** Identify the population conditioned on by each of the four rates in this chapter.
- **Application · calculate:** Recompute the tabulated rates with the [offline lab](../lab/check_audits.py). Explain the weights in the pooled miss rate.
- **Application · check:** A new channel has zero reviewed positive cases. Explain why computing its miss rate as zero would be wrong.
- **Synthesis · assess:** Write a review note that states the observed disparity, two different possible causes and a concrete check for one.
- **Challenge · decide:** Design a paired review of channel interfaces without collecting unnecessary personal details. Name a result that would change your recommendation and a result that would simply leave the uncertainty open.

Next, evaluate a decision workflow. A report can cite correct metrics and still take a step that was never approved.

[Return to contents](../README.md)
