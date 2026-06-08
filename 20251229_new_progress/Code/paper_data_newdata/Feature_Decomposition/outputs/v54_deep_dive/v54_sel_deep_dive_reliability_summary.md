# V54 SEL Deep Dive Reliability Summary

## Scope

This deep dive evaluates W2 `v54` only because the current main-paper tasks use W2 predictors for both W2->W2 and W2->W3. W3 SEL decomposition is not evaluated here.

## Main Finding

The current W2 V54 decomposition is broadly reliable. Most subscales have good internal consistency. The only weak point is the two-item Help-Seeking subscale, which has a lower but still usable alpha.

## Recommended Minor Revision

The main theoretical improvement is to move `v54_18` from Self-Awareness to Responsible Decision-Making. Self-Awareness alpha changes from 0.848 to 0.857; Responsible Decision-Making alpha changes from 0.765 to 0.827.

Why this is preferable:

- `v54_1`, `v54_2`, and `v54_3` are clearly body/emotion awareness items.
- `v54_18` asks whether the student knows what is right or wrong, which is closer to moral judgment / responsible decision-making than emotion awareness.
- Reliability remains good/acceptable after the move, so the decision can be justified theoretically without sacrificing measurement quality.

## Help-Seeking

Current Help-Seeking uses `v54_12` and `v54_16`; alpha = 0.661. Because this is only a two-item scale, alpha is naturally constrained. The corrected item-total correlation is acceptable, so the scale can be retained with a note that reliability is modest.

## AUC Interpretation

The W2 decomposition improved CV5 AUC by about 0.020 for W2->W2 and 0.009 for W2->W3. In prediction-model terms, an AUC gain of 0.018-0.020 is a small-to-moderate but meaningful improvement when the model, outcome, and sample are unchanged. It is not a dramatic performance jump, but it supports the claim that decomposition adds incremental predictive information and improves interpretability.

## Recommendation Table

| Theme                       | Question                                        |   Current Alpha |   Alternative Alpha |   Delta Alternative minus Current | Recommendation                                                                                                                                           |
|:----------------------------|:------------------------------------------------|----------------:|--------------------:|----------------------------------:|:---------------------------------------------------------------------------------------------------------------------------------------------------------|
| Self-Awareness              | Move v54_18 out of Self-Awareness               |           0.848 |               0.857 |                             0.009 | Prefer moving v54_18 out of Self-Awareness: alpha increases slightly and the item is conceptually moral judgment rather than emotion/body awareness.     |
| Responsible Decision-Making | Move v54_18 into Responsible Decision-Making    |           0.765 |               0.827 |                             0.062 | Prefer adding v54_18 to Responsible Decision-Making: alpha remains acceptable and theory fit improves.                                                   |
| Social/Relationship         | Combine relationship skills and help-seeking    |           0.834 |               0.869 |                             0.035 | Do not combine D and E for now unless theory requires a broader social-support domain; current D is already good and E is interpretable as help-seeking. |
| Help-Seeking                | Add self-disclosure item v54_11 to help-seeking |           0.661 |               0.769 |                             0.108 | Keep v54_12 and v54_16 as a two-item help-seeking scale; adding v54_11 changes the construct toward self-disclosure/communication.                       |

## Output

- `v54_sel_deep_dive_reliability.xlsx`
