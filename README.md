# Validating AI (AI Plus One)

**Compact rough draft.** All five proposed chapters and a capstone are represented at first-draft depth. This is not a finished textbook, an expert-reviewed edition, a certification checklist, or a replacement for an existing book.

A report can quote the right values and still recommend the wrong action. This course teaches you to make an AI claim testable, run a check that can disagree with it, and communicate what is safe to conclude. Basic ratios and probability help; Python and AI accounts are optional.

## Learning outcomes

After working through this draft, readers should be able to:

- Make a claim testable and check the quantities and evidence it depends on.
- Interpret calibration, thresholds, shifts, and uneven burdens rather than relying on a single aggregate.
- Use an audit to make a defensible release, restrict, or hold recommendation.

## Chapters

1. [Make the claim small enough to check](chapters/01-make-the-claim-testable.md)
2. [Make a probability earn its precision](chapters/02-calibration-and-thresholds.md)
3. [Change the wrapper before changing the world](chapters/03-robustness-and-shift.md)
4. [Find whose errors the average hides](chapters/04-uneven-burdens.md)
5. [Audit the work, not the completion message](chapters/05-audit-the-workflow.md)
6. [Unaided capstone: release, restrict, or hold?](practice/capstone.md)

Start with the [figure-reading first attempt](practice/first-attempt.md) and [transfer check](practice/transfer.md). For a short on-the-job version, see the [field guide](practice/field-guide.md). The examples, data, chart, prose, and offline checks are original; fictional model-style responses are not measured system outputs. Public sources are cited in context.

With Python 3.9 or newer, from this directory:

```sh
python3 -B lab/check_chart.py fixtures/visits.csv
python3 -B lab/check_audits.py
python3 -B -m unittest discover -s tests -v
```

The checkers recalculate toy results. They do not verify the provenance of a real dataset, judge policies, infer causal effects, or deploy a system.
