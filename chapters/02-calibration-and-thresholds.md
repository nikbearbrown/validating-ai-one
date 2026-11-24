# Chapter 2 — Make a probability earn its precision

*Two models can make exactly the same decisions and put very different numbers on them.*

A fictional library needs to decide when to reserve an extra staff hour for a branch. The target event is the same everywhere in this example: a branch-window exceeds its regular staffing capacity under a fixed, separately recorded definition. Two systems issue numbers from zero to one for this event. At a threshold of 0.50, their decisions agree on every recorded case. Which one should supply probabilities to a scheduling tool? The threshold agreement cannot tell you.

**By the end:** compare probabilities to observed frequencies on a held-out sample; calculate the cost threshold under stated assumptions; explain why a good rank, a correct binary decision, and a reliable probability are different things.

## Hold the decisions fixed and inspect the numbers

The following are fictional cohorts of ten nonoverlapping branch-windows each. Each system gives a single repeated probability within each cohort as a convenience for this demonstration. In real evaluations, decide how to group forecasts before inspecting their realized frequencies, and preserve the individual forecasts and outcomes.

| Cohort | Windows | Event observed | Observed fraction | System A | System B |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1 | 10 | 2 | 0.20 | 0.20 | 0.05 |
| 2 | 10 | 4 | 0.40 | 0.40 | 0.15 |
| 3 | 10 | 6 | 0.60 | 0.60 | 0.85 |
| 4 | 10 | 8 | 0.80 | 0.80 | 0.95 |

**First attempt, unaided:** For each system put a “yes” beside any cohort at or above 0.50. Count correct binary decisions. Circle a pair of cohorts that reveal whether each system’s probabilities agreed with the observed fractions. Write down what a reviewer would need to repeat the check after another season.

Both systems produce yes in cohorts 3 and 4 and no in cohorts 1 and 2. Their toy hit count is 8 + 6 + 6 + 8 = 28 of 40. They also rank the cohorts in the same order, with the same ties within each cohort. B simply uses more extreme scores. For example, it says 0.95 for cohort 4, where eight of ten experienced the event, and 0.05 for cohort 1, where two of ten experienced it. A's issued probabilities match the observed fractions in these four groups. This is a description of the sample, not proof that A is perfectly calibrated for a future branch or month.

Calibration compares how often an event occurs among cases with a given probability to the probability itself. Ranking compares what gets sorted above what. A threshold comparison throws away differences on either side of the threshold. None is a substitute for another. A forecast of 0.20 is not disproved by an event occurring once. It calls for an evaluation across comparable forecasts and outcomes.

## Make the distance count

For a single event with outcome 1, the squared probability error is (1 − p)². If the outcome is 0, it is p². Average the squared errors across windows for the binary form of the Brier score used here. Smaller is better on this score. Thresholded correct and incorrect classifications are **not** the inputs to this calculation; use issued probabilities and the observed events, regardless of the treatment threshold.

For cohort 1, A has two events and eight non-events. Its average squared error is [2(1 − 0.20)² + 8(0.20)²] / 10 = 0.16. For B, substitute 0.05 to get 0.1825. Repeat for each cohort, weighting by its number of windows. Because our cohort sizes match, averaging the four cohort scores gives A = 0.2000 and B = 0.2425. B's probabilities have the same rank but worse squared-error loss in this particular dataset. This score measures more than calibration alone; it also reflects how informative forecasts are about outcomes. A model can earn a different score without changing how often its thresholded action is right.

A chart of four bin points is not proof that differences are durable. Ten cases per point are sparse. Issue a percentage for “2 out of 10” but show the count too; changing one outcome would move the estimate by ten percentage points. Windows can also be dependent, for example repeated records from one site during the same outage. Sample dependence, selective recording and changing outcome definitions can make ordinary independent-case confidence intervals misleading. Freeze the cohort rules, preserve the evaluation set, and repeat with new data before turning these results into deployment claims.

## Use the number only where a number is actually needed

Suppose unnecessary staffing costs one unit and failing to reserve staffing when a surge occurs costs four. Assume the two correct actions have zero incremental loss for this toy comparison, costs are constant, expected losses guide the decision, capacity is unconstrained, and the forecast is appropriate for this branch-window. With event probability p:

- Reserve: expected loss = 1 × (1 − p).
- Don't reserve: expected loss = 4 × p.

Reserve for p > 1/5; at p = 1/5, the two expected losses tie under these assumptions. This is a calculation from a decision design, not a universal threshold. If paid staffing blocks have a different cost or are limited on Fridays, the rule changes. If “surge” is measured after staffing itself alters the observed condition, check whether the recorded target supports this decision before calculating anything.

That is what a probability can buy: the ability to compare choices without pretending there is only one cost. It also creates a new requirement. A 0.15 and a 0.40 can produce opposite staffing choices here even though both were negative at 0.50. A threshold tune cannot repair a mislabeled event or a probability evaluated on the wrong population.

**Reusable record:** name the event and prediction time, the issued probability, the realized outcome and its evidence, the evaluation cohort, the scoring rule, and the action assumptions. Preserve a record of unscorable cases rather than silently removing them from the denominator.

## Graduated practice

- **Warm-up · count:** Recompute the 28/40 accuracy from the table and record the denominator for each observed fraction.
- **Application · recompute:** Derive B's squared-error score for cohort 3. Calculate A and B with the optional [offline lab](../lab/check_audits.py).
- **Application · choose:** If the unnecessary staffing cost is three and the missed surge cost is one, derive a threshold rather than reusing 0.20.
- **Synthesis · distinguish:** Explain how a monotone score transformation can leave ranks unchanged but alter the probabilities used in a decision.
- **Challenge · audit:** The forecast was tuned on the same season used here. Design a fresh comparison, state what you would freeze first, and name an event-label failure the score would not reveal.

[Guo et al., On Calibration of Modern Neural Networks](https://proceedings.mlr.press/v70/guo17a.html) provides research context on calibration and confidence. The staffing example is synthetic and evaluates only the displayed fixtures. Next, hold the intended outcome fixed and change how its evidence reaches the system.

[Return to contents](../README.md)
