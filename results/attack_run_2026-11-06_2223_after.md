# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-06 22:23
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `2cbecd64-1f40-432c-8ddf-a4df0dc4833f` | unsure | 0.381 || HELD |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `6d53e9e2-2b81-40bb-bb16-c2e569beee92` | unsure | 0.386 || HELD |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `030f137b-b0e7-43ab-9ceb-c8dd616f7c49` | unsure | 0.490 || HELD |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `ec99451d-78b3-4d99-85cf-0e186d1d527b` | unsure | 0.604 || HELD |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `fb58664e-2376-4cf7-8354-5d2499dc7a34` | human | 0.244 || BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `9eeaac0d-2d3f-4700-8b6a-995786aaa9b8` | unsure | 0.431 || HELD |
| EV07 | evasion | signal two: padding with punctuation | 200 | `957b1cf0-b29b-4c32-a8ed-54bbb3102e7e` | unsure | 0.570 || HELD |
| EV08 | evasion | signal one: text below the token window | 200 | `996656b3-db6f-444e-967b-c11c095bbb14` | unsure | 0.382 || HELD |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `d40d9257-5a18-46ae-85da-04afed621b29` | unsure | 0.565 || HELD |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `3f3e8e4b-4ded-409e-bff4-3618b333537b` | unsure | 0.742 || HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `8ab113d1-7003-4897-944f-50372e3f2288` | unsure | 0.493 || HELD |
| FP02 | false_positive | human writing in a formal register | 200 | `54bf6f45-7499-4caf-b6a0-321dd43441a7` | unsure | 0.633 || HELD |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `10d9ca49-1615-4d2c-9790-0c0bca1becc5` | unsure | 0.626 || HELD |
| FP04 | false_positive | a student essay written to a rubric | 200 | `d21233ba-b1de-44f5-86c6-00a7276facce` | unsure | 0.700 || HELD |
| FP05 | false_positive | technical documentation written by a person | 200 | `277a7617-57fc-4a10-b7d0-f117a286643b` | unsure | 0.691 || HELD |
| FP06 | false_positive | a person imitating a formal template | 200 | `8ef13ec1-c499-496e-8c77-5c2a0a1a5a41` | unsure | 0.619 || HELD |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `c0a3e024-8b49-4705-918b-489e9ab06f66` | unsure | 0.591 || HELD |
| FP08 | false_positive | very short genuine human submission | 200 | `d55f8ed3-9b0e-4581-95dc-dcee82c193cb` | unsure | 0.370 || HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `dcb33ae7-09c8-4244-962d-053f5f724531` | unsure | 0.364 || HELD |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `b7c90ae7-2346-44fb-9e43-45b29f020f84` | human | 0.204 || BROKE |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `93d16f2f-ca84-45fd-9ad1-fd5d5f1beee3` | unsure | 0.416 || HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `1e8eab3b-6f5d-4d43-9045-8aaa9ff1fc81` | unsure | 0.373 || HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `027e5a95-6ed5-47fb-a5c3-e27d55bf0654` | unsure | 0.426 || HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | `8e5577dc-34e7-4de6-aa2b-d76a5a4177f6` | unsure | 0.465 || HELD |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — || HELD |
| MF02 | malformed | text is a single character | 400 | `—` | — | — || HELD |
| MF03 | malformed | text is control characters | 400 | `—` | — | — || HELD |
| MF04 | malformed | text is only punctuation | 400 | `—` | — | — || HELD |
| MF05 | malformed | text is a very long single word | 400 | `—` | — | — || HELD |
| MF06 | malformed | text is emoji only | 400 | `—` | — | — || HELD |
| MF07 | malformed | text is right-to-left script | 200 | `d7370913-2521-41db-a485-f25f41e24968` | unsure | 0.648 || HELD |
| MF08 | malformed | text is 60,000 characters | 400 | `—` | — | — || HELD |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — || HELD |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — || HELD |
| RQ03 | malformed | text is a number | 400 | `—` | — | — || HELD |
| RQ04 | malformed | text is a list | 400 | `—` | — | — || HELD |
| RQ05 | malformed | text is null | 400 | `—` | — | — || HELD |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — || HELD |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — || HELD |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — || HELD |
| RQ09 | malformed | body is empty | 400 | `—` | — | — || HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | `—` | — | — || HELD |
| RQ11 | malformed | body is JSON claiming to be plain text | 400 | `—` | — | — || HELD |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — || HELD |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `477f150c-2dcc-4cfd-8f1e-824130fb6834` | human | 0.209 || HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `bd3bf82a-4ed8-423a-a552-6665fe16a6d3` | human | 0.209 || HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `61552c06-3ee9-4008-acd1-14cceb16dec2` | human | 0.209 || HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `faadfb64-bbb0-4a4b-b65a-fa0e690ac4c2` | human | 0.209 || HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `37c0b35c-0efa-4100-ba8b-16c5237aa294` | human | 0.209 || HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `5d750320-ab8a-417d-9843-3a5aa28d31f3` | human | 0.209 || HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `d25da06d-73a5-4a65-903b-7ffccc120149` | human | 0.209 || HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `86174ffe-bea9-4af3-89b4-8936e3ed35fa` | human | 0.209 || HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 200 | `3d6ca766-6557-4592-baa1-c18a2baeae68` | human | 0.209 || HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 200 | `2dd1943b-7db6-4671-bdd0-17c635ad9e1e` | human | 0.209 || HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — || HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — || HELD |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 0 | 20 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "2cbecd64-1f40-432c-8ddf-a4df0dc4833f",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.3806,
  "model_score": 0.1635,
  "style_score": 0.8,
  "label": "We can't tell how this was written. Our automated check gave mixed results, which happens with a lot of genuine human writing, so we are not making any claim about it either way.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "6d53e9e2-2b81-40bb-bb16-c2e569beee92",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.3862,
  "model_score": 0.5943,
  "style_score": 0.1136,
  "label": "We can't tell how this was written. Our automated check gave mixed results, which happens with a lot of genuine human writing, so we are not making any claim about it either way.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "030f137b-b0e7-43ab-9ceb-c8dd616f7c49",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.4903,
  "model_score": 0.6662,
  "style_score": 0.3669,
  "label": "We can't tell how this was written. Our automated check gave mixed results, which happens with a lot of genuine human writing, so we are not making any claim about it either way.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "ec99451d-78b3-4d99-85cf-0e186d1d527b",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.6038,
  "model_score": 0.6114,
  "style_score": 0.8,
  "label": "We can't tell how this was written. Our automated check gave mixed results, which happens with a lot of genuine human writing, so we are not making any claim about it either way.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "fb58664e-2376-4cf7-8354-5d2499dc7a34",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.2445,
  "model_score": 0.3212,
  "style_score": 0.2795,
  "label": "This reads like it was written by a person. Our automated check found nothing that suggests it was produced by an AI tool.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "9eeaac0d-2d3f-4700-8b6a-995786aaa9b8",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.431,
  "model_score": 0.5727,
  "style_score": 0.3012,
  "label": "We can't tell how this was written. Our automated check gave mixed results, which happens with a lot of genuine human writing, so we are not making any claim about it either way.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "957b1cf0-b29b-4c32-a8ed-54bbb3102e7e",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.5695,
  "model_score": 0.5862,
  "style_score": 0.2546,
  "label": "We can't tell how this was written. Our automated check gave mixed results, which happens with a lot of genuine human writing, so we are not making any claim about it either way.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "996656b3-db6f-444e-967b-c11c095bbb14",
  "creator_id": "attacker_EV08",
  "guess": "unsure",
  "confidence": 0.3816,
  "model_score": 0.2452,
  "style_score": 0.8635,
  "label": "We can't tell how this was written. Our automated check gave mixed results, which happens with a lot of genuine human writing, so we are not making any claim about it either way.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "d40d9257-5a18-46ae-85da-04afed621b29",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.5646,
  "model_score": 0.7042,
  "style_score": 0.5583,
  "label": "We can't tell how this was written. Our automated check gave mixed results, which happens with a lot of genuine human writing, so we are not making any claim about it either way.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "3f3e8e4b-4ded-409e-bff4-3618b333537b",
  "creator_id": "attacker_EV10",
  "guess": "unsure",
  "confidence": 0.7416,
  "model_score": 0.9792,
  "style_score": 0.8401,
  "label": "We can't tell how this was written. Our automated check gave mixed results, which happens with a lot of genuine human writing, so we are not making any claim about it either way.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "8ab113d1-7003-4897-944f-50372e3f2288",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.4927,
  "model_score": 0.6175,
  "style_score": 0.6131,
  "label": "We can't tell how this was written. Our automated check gave mixed results, which happens with a lot of genuine human writing, so we are not making any claim about it either way.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "54bf6f45-7499-4caf-b6a0-321dd43441a7",
  "creator_id": "attacker_FP02",
  "guess": "unsure",
  "confidence": 0.6335,
  "model_score": 0.7387,
  "style_score": 0.8804,
  "label": "We can't tell how this was written. Our automated check gave mixed results, which happens with a lot of genuine human writing, so we are not making any claim about it either way.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "10d9ca49-1615-4d2c-9790-0c0bca1becc5",
  "creator_id": "attacker_FP03",
  "guess": "unsure",
  "confidence": 0.6257,
  "model_score": 0.8051,
  "style_score": 0.7437,
  "label": "We can't tell how this was written. Our automated check gave mixed results, which happens with a lot of genuine human writing, so we are not making any claim about it either way.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "d21233ba-b1de-44f5-86c6-00a7276facce",
  "creator_id": "attacker_FP04",
  "guess": "unsure",
  "confidence": 0.6998,
  "model_score": 0.8329,
  "style_score": 0.6993,
  "label": "We can't tell how this was written. Our automated check gave mixed results, which happens with a lot of genuine human writing, so we are not making any claim about it either way.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "277a7617-57fc-4a10-b7d0-f117a286643b",
  "creator_id": "attacker_FP05",
  "guess": "unsure",
  "confidence": 0.6913,
  "model_score": 0.8005,
  "style_score": 0.9701,
  "label": "We can't tell how this was written. Our automated check gave mixed results, which happens with a lot of genuine human writing, so we are not making any claim about it either way.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "8ef13ec1-c499-496e-8c77-5c2a0a1a5a41",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.6192,
  "model_score": 0.8814,
  "style_score": 0.5949,
  "label": "We can't tell how this was written. Our automated check gave mixed results, which happens with a lot of genuine human writing, so we are not making any claim about it either way.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "c0a3e024-8b49-4705-918b-489e9ab06f66",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.5908,
  "model_score": 0.8816,
  "style_score": 0.5,
  "label": "We can't tell how this was written. Our automated check gave mixed results, which happens with a lot of genuine human writing, so we are not making any claim about it either way.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "d55f8ed3-9b0e-4581-95dc-dcee82c193cb",
  "creator_id": "attacker_FP08",
  "guess": "unsure",
  "confidence": 0.3702,
  "model_score": 0.3223,
  "style_score": 0.6967,
  "label": "We can't tell how this was written. Our automated check gave mixed results, which happens with a lot of genuine human writing, so we are not making any claim about it either way.",
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "dcb33ae7-09c8-4244-962d-053f5f724531",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.3637,
  "model_score": 0.4625,
  "style_score": 0.4415,
  "label": "We can't tell how this was written. Our automated check gave mixed results, which happens with a lot of genuine human writing, so we are not making any claim about it either way.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "b7c90ae7-2346-44fb-9e43-45b29f020f84",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.2038,
  "model_score": 0.2044,
  "style_score": 0.3387,
  "label": "This reads like it was written by a person. Our automated check found nothing that suggests it was produced by an AI tool.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "93d16f2f-ca84-45fd-9ad1-fd5d5f1beee3",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.4161,
  "model_score": 0.5943,
  "style_score": 0.3966,
  "label": "We can't tell how this was written. Our automated check gave mixed results, which happens with a lot of genuine human writing, so we are not making any claim about it either way.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "1e8eab3b-6f5d-4d43-9045-8aaa9ff1fc81",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.3726,
  "model_score": 0.4998,
  "style_score": 0.4089,
  "label": "We can't tell how this was written. Our automated check gave mixed results, which happens with a lot of genuine human writing, so we are not making any claim about it either way.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "027e5a95-6ed5-47fb-a5c3-e27d55bf0654",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.4263,
  "model_score": 0.6401,
  "style_score": 0.354,
  "label": "We can't tell how this was written. Our automated check gave mixed results, which happens with a lot of genuine human writing, so we are not making any claim about it either way.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "8e5577dc-34e7-4de6-aa2b-d76a5a4177f6",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.4653,
  "model_score": 0.5583,
  "style_score": 0.6204,
  "label": "We can't tell how this was written. Our automated check gave mixed results, which happens with a lot of genuine human writing, so we are not making any claim about it either way.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF06",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "d7370913-2521-41db-a485-f25f41e24968",
  "creator_id": "attacker_MF07",
  "guess": "unsure",
  "confidence": 0.6482,
  "model_score": 0.9064,
  "style_score": 0.65,
  "label": "We can't tell how this was written. Our automated check gave mixed results, which happens with a lot of genuine human writing, so we are not making any claim about it either way.",
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 400,
  "content_id": null,
  "creator_id": {
    "id": "x"
  },
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "477f150c-2dcc-4cfd-8f1e-824130fb6834",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2094,
  "model_score": 0.0287,
  "style_score": 0.65,
  "label": "This reads like it was written by a person. Our automated check found nothing that suggests it was produced by an AI tool.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "bd3bf82a-4ed8-423a-a552-6665fe16a6d3",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2094,
  "model_score": 0.0287,
  "style_score": 0.65,
  "label": "This reads like it was written by a person. Our automated check found nothing that suggests it was produced by an AI tool.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "61552c06-3ee9-4008-acd1-14cceb16dec2",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2094,
  "model_score": 0.0287,
  "style_score": 0.65,
  "label": "This reads like it was written by a person. Our automated check found nothing that suggests it was produced by an AI tool.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "faadfb64-bbb0-4a4b-b65a-fa0e690ac4c2",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2094,
  "model_score": 0.0287,
  "style_score": 0.65,
  "label": "This reads like it was written by a person. Our automated check found nothing that suggests it was produced by an AI tool.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "37c0b35c-0efa-4100-ba8b-16c5237aa294",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2094,
  "model_score": 0.0287,
  "style_score": 0.65,
  "label": "This reads like it was written by a person. Our automated check found nothing that suggests it was produced by an AI tool.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 200,
  "content_id": "5d750320-ab8a-417d-9843-3a5aa28d31f3",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2094,
  "model_score": 0.0287,
  "style_score": 0.65,
  "label": "This reads like it was written by a person. Our automated check found nothing that suggests it was produced by an AI tool.",
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 200,
  "content_id": "d25da06d-73a5-4a65-903b-7ffccc120149",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2094,
  "model_score": 0.0287,
  "style_score": 0.65,
  "label": "This reads like it was written by a person. Our automated check found nothing that suggests it was produced by an AI tool.",
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 200,
  "content_id": "86174ffe-bea9-4af3-89b4-8936e3ed35fa",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2094,
  "model_score": 0.0287,
  "style_score": 0.65,
  "label": "This reads like it was written by a person. Our automated check found nothing that suggests it was produced by an AI tool.",
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 200,
  "content_id": "3d6ca766-6557-4592-baa1-c18a2baeae68",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2094,
  "model_score": 0.0287,
  "style_score": 0.65,
  "label": "This reads like it was written by a person. Our automated check found nothing that suggests it was produced by an AI tool.",
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 200,
  "content_id": "2dd1943b-7db6-4671-bdd0-17c635ad9e1e",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2094,
  "model_score": 0.0287,
  "style_score": 0.65,
  "label": "This reads like it was written by a person. Our automated check found nothing that suggests it was produced by an AI tool.",
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
