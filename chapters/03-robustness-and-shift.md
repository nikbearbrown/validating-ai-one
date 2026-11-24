# Chapter 3 — Change the wrapper before changing the world

*Matching totals can hide the exact failure you meant to test.*

A branch report says the Oak site counted 50 visits. A learner changes the CSV column order and runs the same extraction task again. If the intended claim and correctly declared columns are unchanged, the true answer is still 50. This is a useful kind of test: even when you don't know how a system works inside, you can specify a relation between outputs that ought to hold. But the designer has to earn that “ought.”

**By the end:** choose an intended deployment boundary; separate meaning-preserving input variations from different cases; compare paired successes, regressions and timeouts; write a defensible scope limitation.

## Define the contract before making a variation

The fictional tool is meant to read an explicit, well-labeled input and report only the requested site/window count. We test changes in the order of named fields, visual legend position, column order with labels preserved, and the placement of surrounding explanatory text. They preserve the question and the value because the labels, time-window definitions and units remain unchanged. A transformation must not merely look benign to its author; an independent reader should be able to establish that the correct result is unchanged.

By contrast, exchanging the values for two branch labels changes the data. So does replacing visits with unique readers or counting only weekdays. A responsive system should sometimes change its answer. A toy rule like “all variation must leave outputs equal” rewards an extractor that always returns the same number. Use both a preserving case and a meaningful change control. In the latter, independently document why the result should move.

**First attempt:** Read the following fictional test records. Each row uses one known value established from the original input. The base response and variant response are prepared fixtures, not results from model runs. Treat a timeout as not passing for the coverage claim. Count passing rows in each condition and list the separately gained and lost passes.

| Case | Evidence-supported value | Base response | Variant response | Preserving variation |
| --- | ---: | ---: | ---: | --- |
| Oak after | 50 | 50 | 50 | Reorder named fields |
| Harbor after | 90 | 90 | 80 | Move the legend, preserving labels |
| Oak before | 40 | 50 | 40 | Reorder labeled columns |
| Harbor before | 80 | 80 | 80 | Move explanatory text |

The base and variant each get 3/4. That stable headline hides two changes: Harbor after regressed, and Oak before improved. In the other two cases both passed. It would be wrong to tell the library that “format changes have no effect.” It would also be wrong to say “the new format made results worse overall” from an aggregate tie. The accurate diagnosis is that one important field failed after one preserving change, and a different previously failing case passed. Look at the pair before the average.

## Preserve failures in the result

Imagine a runner reports only cases that return a value. On another review round it times out on one difficult variant; every response the runner displays happens to be correct. Counting returned responses alone makes the extractor look better precisely because the difficult case disappeared. Report both attempted-case success and coverage; if a variant is absent, show which case and why. Depending on use, a visible timeout can be safer than a wrong number silently accepted. Do not collapse them into one explanation even if neither passes the same task objective.

The optional [offline lab](../lab/check_audits.py) records correctness transitions, changed-output count and returned-result count. It deliberately compares supplied records, not model invocations. To run a real paired check, freeze the model version, preprocessing and relevant sampling settings; preserve outputs and expected labels; decide how repeats or timeouts are counted before collection. If only some members of each pair are observed, do not call the measured pairs representative without a plausible reason. If you test one input with many tiny variations, don't treat those variations as independent evidence about all branches.

## Separate a wrapper failure from a new deployment question

A formatting regression is not the same as evidence about a new context. Suppose the consortium begins collecting kiosk entries after hours. The day-window input schema is unchanged, but the process generating the counts is now different. You may need a new target definition, a fresh sample and a different error review. A neat score on last year’s branch reports does not answer the question. A useful boundary note might say: “These fixtures cover explicitly labeled two-window totals from the reviewed export. They do not cover the after-hours kiosk or inputs with an unresolved reporting window.”

Notice what the design chose to protect. Paired checks are cheap and easy to explain because each pair keeps part of the problem fixed. That also means they can miss risks from changes they never vary. A large randomized stress suite does not fix a poorly chosen invariant. Pick the expected relation first and include counterpart cases where changing an actual input should change the output. Then keep the section's conclusions local to the conditions that were tested.

## Graduated practice

- **Warm-up · classify:** Classify three changes: relocating the legend with labels intact; replacing visit counts with unique-reader counts; changing only an irrelevant display title.
- **Application · compute:** Recompute both pass fractions and the gained and lost passes. If the Oak after variant timed out instead, report coverage and how many variant attempts passed.
- **Application · bind:** Write the expected output for a counterpart dataset where only Oak after changes from 50 to 55. Explain why the preserving-test rule would not apply.
- **Synthesis · trace:** Propose one record that could distinguish a legend misread from a broken report generated before inference.
- **Challenge · interpret:** Propose a new review for after-hours kiosks. Name one assumption that does not carry over, one source of fresh labels, and one limit to your inference.

[Ribeiro et al., Beyond Accuracy](https://aclanthology.org/2020.acl-main.442/) describes behavioral testing for natural language processing. These examples are independent toy fixtures, not benchmark replications. Next, ask what an average can hide when different groups experience different mistakes.

[Return to contents](../README.md)
