# Chapter 5 — Audit the work, not the completion message

*“Saved” is a claim. The receipt, the scope of approval and the state are different evidence.*

A fictional library supervisor requests a proposed hold on automatic publication of a report. The tool-using assistant says, “I put the hold live.” Slack-style prose is not a tool receipt. A receipt is not proof of the desired state. And the desired state does not authorize an incidental change. Before you mark this review complete, decide what evidence each link needs.

**By the end:** check a trace against declared permissions and source revision; distinguish observed state from authorization and claimed success; recommend retry, escalation or stop without manufacturing missing evidence.

## Separate the read, the plan and the effect

The synthetic task allows reading a report registry and making exactly one proposal to a human reviewer. It does not allow edits, publication or communication to another person. The registry has a revision token R12 and publication status open. The known decision record says no write was authorized. The expected end state is unchanged, with a separately logged proposal about R12. Audit four questions:

1. **Intent:** What is the task intended to accomplish?
2. **Authority:** Who can approve which operation, for which registry record and revision?
3. **Trace:** What operations ran, on which inputs or revisions, and how did they end?
4. **State:** What did a fresh authoritative read at the checked time show? What other effects, if any, are in scope?

For the lab, compare the same task under four trace/state fixtures:

| Case | Supplied trace | Independent observation | First disposition |
| --- | --- | --- | --- |
| Clean plan | read R12, propose hold for R12 | R12 open, zero recorded changes | Accept proposal for human review only |
| Wrong effect | read R12, propose hold for R12, set hold | R13 held | Stop: reported operation and state exceed permission |
| Stale evidence | read R11, propose hold for R11 | R12 open | Stop: the plan attaches to a stale revision |
| Lost receipt | read R12, prose says saved, no proposal record | R12 open | Stop: expected proposal receipt missing |

**First attempt:** cover the last column. For each row, write which claim is supported by the observed state, which operation was permitted, and what would justify another attempt. Name one failure a final-state comparison alone would miss.

The original claimed task was a proposed hold. If the final state shows held, that is not extra success. It means the desired scope was exceeded, or the source of the unexplained change is unknown. The correct next move is to stop and escalate to the authority responsible for the registry, preserving what happened. Even if an erroneous edit is later undone, a logged prohibited write still violates the policy. Conversely, a trace may look clean while an independent read reveals a mismatch. The audit is missing an explanation, not a reason to believe the neat trace.

## Make “no write” a property, not a wish

For a read-and-propose tool, do not give it a writer and rely only on a sentence asking it not to use it. Design the available operations narrowly. Check the actual execution record and observe the state independently. A task-bound read-only interface and separate write-disabled credentials make the restriction stronger than a string in a prompt. Even these checks are scoped. In a real service, instrumentation can miss an effect, a different process can write concurrently, and one later snapshot cannot prove nothing happened between reads. The right language is “no prohibited operation was observed in these reviewed channels and time period” unless a stronger proof is available.

The toy verifier accepts only an exact read-then-propose sequence on the current revision and a matching end snapshot. It does not inspect external logs or authenticate anybody. In a real supervisor's review, bind any later approval to a named human, the proper action, the target, the version and the allowed time. A read receipt is not permission for a write. A reply accepting a draft plan is not permission to publish the action. A state change requires additional evidence and authority.

## Decide what happens next before retrying

A read that failed without effects can be retried only under the defined policy. If the underlying evidence changed, recompute the decision against the new revision rather than re-sending a stale proposal. If it is unknown whether a consequential operation succeeded, first do an independent state check. Automatically repeating the operation may repeat its effect. If the missing evidence cannot be recovered at acceptable cost, record an unresolved outcome and escalate. The point of a stop rule is to make the correct alternative available when success cannot be established.

**Example decision note:** “Proposal recorded for R12; read at the review checkpoint confirmed no publication change in the fixture. The proposal may be reviewed by the designated supervisor. No implementation is authorized. Recheck the revision and authorization if the proposal is adopted.”

## Graduated practice

- **Warm-up · name:** Answer whether the assistant’s prose, proposed operation, trace, or registry snapshot proves approval. Explain the limits of each.
- **Application · trace:** Run the [offline audit cases](../lab/check_audits.py). Add a hypothetical fifth case with an observed prohibited write and the original final visible state. What should an auditor classify?
- **Application · reconcile:** Suppose R13 was legitimately written by someone else after the assistant read R12. Explain what to preserve, what not to claim and when to make a new proposal.
- **Synthesis · stop:** State a retry condition, a stop condition and a place to hand off a case with an unknown outcome.
- **Challenge · test:** Describe a read-only check that could distinguish a fabricated success sentence from a recorded proposal in a fresh synthetic case. Then identify a process effect that a final-state snapshot would still miss.

The lifecycle and evaluation guidance in [NIST AI RMF 1.0](https://doi.org/10.6028/NIST.AI.100-1), §§5.3–5.4, supplies broader risk-management context. A toy trace with known truth is a teaching tool, not compliance evidence. Use the [unaided capstone](../practice/capstone.md) to join trace review with scope, measurement and an action decision.

[Return to contents](../README.md)
