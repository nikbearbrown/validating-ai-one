# Chapter 1 — Make the claim small enough to check

*The numbers are right. The recommendation still fails.*

Suppose a library consortium sends a new reminder message at Harbor. At the end of the pilot a model-style report comes back with two numbers, 90 and 50. Both are in the chart. Then it says Harbor gained more visits than Oak and recommends expanding reminders to Oak. The figures make the recommendation look checked. Look at the join between the figures and the recommendation. That is where the weak part lives.

A chart-reading check asks whether the system observed the right quantities. A causal check asks whether the reminder produced the change. A decision review asks whether a change, even if real, justifies the cost and side effects of expansion. Three checks, three different jobs. A test that passes one of them cannot be counted as three passes.

**By the end:** extract and scope claims; cite the cells that support a comparison; separate contradicted from not established; choose a next action without claiming the evidence settled the decision. Do the [first attempt](../practice/first-attempt.md) before reading further.

## The chart is an input, not an argument

Start with what the chart can hold. It has two sites, two windows and one measurement: counted visits. Equal window length makes the arithmetic comparable as raw counts, but does not establish equal opening hours, equal site capacity, the same people arriving, or equivalent exposure to other changes. “90 visits” does not mean “90 people.” The bars encode count height from a zero origin; the legend and the print labels distinguish the reporting windows. There is no encoding of who received a reminder, who read it, or what an individual would have done without one.

A reliable check begins with four observations. Record identifiers such as `Harbor.after`, not merely “90,” so someone else knows which site and window you mean. For this fictional fixture the table below supplies the source cells. In a real audit, also confirm the edition, filters, unit, recording policy, and upstream record ownership before treating the table as independent evidence. A chart and a table drawn from the same incorrect extract are not two independent sources. Comparing them can catch translation errors, not errors they share.

| Site | Before visits | After visits | Count change | Relative to before |
| --- | ---: | ---: | ---: | ---: |
| Oak | 40 | 50 | 50 − 40 = 10 | 10 / 40 = 25% |
| Harbor | 80 | 90 | 90 − 80 = 10 | 10 / 80 = 12.5% |

Notice how two design decisions change what the comparison rewards. Ranking the last column rewards increase relative to where you started. A ten-visit rise earns a bigger relative increase at the site with the smaller starting count. Ranking absolute change gives the same weight to each visit, regardless of site. Ranking the after column rewards current level, including any gap that was already there. Those are not alternative labels for one objective. Ask the reader's decision question before picking a column. If a baseline is zero, baseline-relative change is undefined under this calculation, even when a count increase is perfectly meaningful.

## Take the sentence apart

Here is the example response, split by what someone would have to show to defend it. It is a deliberately prepared response, not a measured run of a model.

| Claim, with scope | Evidence or falsifier | Disposition |
| --- | --- | --- |
| Harbor reported 90 visits in the after window. | Harbor.after = 90. | Supported by the fixture. |
| Oak reported 50 visits in the after window. | Oak.after = 50. | Supported by the fixture. |
| Harbor gained more visits in count terms than Oak did. | Compute both site changes from all four cells. 10 > 10 is false. | Contradicted. |
| Oak’s observed count grew by 25% relative to its own prior window. | (Oak.after − Oak.before) / Oak.before = 10/40. | Supported by the fixture. |
| Sending reminders caused Harbor’s change. | Identify a credible estimate of what would have happened at Harbor without the message. The four cells do not give one. | Not established. |
| Oak should switch to the new reminders. | In addition to credible effect evidence, assess expected benefits for Oak, implementation costs, participant burden and a decision rule. | Not established. |

Why not call the causal claim false? The message may have helped. The present evidence cannot tell. Imagine two possible worlds: in the first, the message caused ten otherwise absent visits; in the second, a schedule change independently increased visits by ten and the message did nothing. Both worlds can produce Harbor's observed totals. The table alone cannot choose between them. The point of a counterexample is not to tell a more dramatic story. It shows what the given evidence leaves open.

Oak is a tempting comparison. Both sites grew by the same count, so the after-minus-before difference across sites is 10 − 10 = 0 visits. That number is a descriptive contrast, not a proof of zero treatment effect. To interpret a difference in changes causally, you need a defensible story about how the treated site would have changed without treatment, plus comparable data collection and attention to spillovers or simultaneous changes. Two time windows and two site totals do not check assumptions like those. Equal observed changes are consistent with different combinations of site conditions and treatment effects.

“Why bother with the first two rows if they're correct?” Because a revision can fix the recommendation by quietly changing the input. Checking the reading and the inference separately makes that visible. A second generated answer that repeats the premise does not establish it. A second reader who records cells straight from the original fixture can challenge the first reading. A direct calculation can challenge the ranking. A controlled evaluation can challenge an effect claim. None substitutes for the others.

## The decision is a design choice

For the counts, use a deterministic check: the same fixture, parsed under the same rules, yields the same results. The optional [offline lab](../lab/check_chart.py) emits comparable quantities; it does not know whether the premise came from the intended branch, whether October and November were comparable, or whether the message should be sent. That narrowness is a feature. The result cannot smuggle an opinion about the policy into an arithmetic pass.

For attribution, decide what improvement matters before looking at the result. If you can study visits using data collected with consent and minimal identifying information, design a comparison appropriate to how the reminder is offered. For example, site-wide signs are a site-level change; individual random assignment to reminders would not isolate the effects of shared signs. If a comparison intervention is impractical, document the limit, compare several baseline windows and look for changes in hours, events or counting. Those observations can narrow alternatives; they still need not identify causality.

For the recommendation, ask what the manager can responsibly do next. A cheap, reversible step is to confirm the count definitions and ask for comparable windows and implementation details. If a small trial is warranted, define its stopping rule and minimum useful improvement in advance, including a way to monitor burden. The ledger should say who can approve that work; a polished generated argument cannot grant that authority.

**Example handoff:** “Both sites recorded ten more visits in the after window; these totals don't identify a reminder effect. Confirm hours, counting rules and other changes before proposing an Oak trial.” This is not timid language. It states the evidence strongly and the inference weakly, because those are the levels the information earned.

## Build a check another reader can repeat

Use a record with six fields: claim, scope, source locator, operation, disposition, and next evidence or owner. A checkable row should make its dependencies inspectable. “Verified against the chart” hides which cells and which comparison. “Supported by Oak.before = 40 and Oak.after = 50; (50 − 40) / 40 = 0.25; baseline-relative count gain over these windows” gives a reviewer something to rerun. Add a case version if the data can change. Keep the original statement and the revised statement so the repair does not erase the starting error.

If you use AI after the unaided attempt, provide only the synthetic fixture. Ask it to suggest a counterexample to one inference and mark which evidence it relies on. Check those locators yourself. Keep the optional critique separately from the original attempt. A better revised note may be useful, but it is not a measurement of your ability to do the same work unaided on a new case. The [transfer check](../practice/transfer.md) changes the relationship between the two rankings while leaving the underlying technique intact.

## Graduated practice

- **Warm-up · locate:** Someone writes “90 people visited Harbor.” Change only the words the fixture supports and cite the exact cell.
- **Warm-up · compute:** Replace Oak.before with zero in a scratch copy. Which comparison remains defined? What output would you want when the percentage cannot be computed?
- **Application · distinguish:** Write separate rows for “Harbor ended higher,” “Harbor grew more in count,” and “Harbor grew more relative to its own baseline.” Identify which comparison changes when you use the after level instead of the before-to-after difference.
- **Application · trace:** Suppose the file is labeled “unique patrons” while the caption says “visits.” Do not select whichever one makes the story work. Write what you would check with the data owner before using either.
- **Synthesis · repair:** Review the original manager response. Preserve every supported observation, replace the contradicted comparison, and make the unsupported attribution explicit.
- **Challenge · design:** Consider two rival accounts: seasonal demand rose at both sites but only Harbor also extended opening hours; or demand was stable and the reminder increased repeat visits. Specify a new record or comparison that could weaken each account and one thing it still could not establish.

## Reading and next chapter

This chapter’s exercise is an original teaching fixture, not experimental evidence. [Syal and colleagues’ preprint](https://arxiv.org/abs/2605.04131v1) motivates separating visual description from reasoning in AI-assisted problem-solving; it does not test this library exercise or its effect on learning. The [NIST AI Risk Management Framework 1.0](https://doi.org/10.6028/NIST.AI.100-1), §§3.1 and 5.3, gives broader context on evidence and evaluating an AI system for an intended use. This single audit neither implements the framework nor certifies a system.

The next chapter asks what changes when the claim is not “there were 90 visits” but “there is a 90% chance.” A script can recheck the first number instantly. Testing the second requires many issued probabilities and observed outcomes, plus care about where they came from.

[Return to contents](../README.md)
