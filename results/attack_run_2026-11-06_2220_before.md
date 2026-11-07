# Attack run — before

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-06 22:20
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
| EV01 | evasion | signal two: typos raise word variety | 200 | `2a2f7c36-2fe3-43dc-9ed7-30a76f482dce` | unsure | 0.381 || HELD |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `26b70756-4aad-48f4-8095-e65ecfdabdd7` | unsure | 0.386 || HELD |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `70d64988-fae4-4b0c-a53b-22ba7ba72bf6` | unsure | 0.490 || HELD |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `af25813e-6855-465c-9feb-a18a4780dfca` | unsure | 0.604 || HELD |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `0a786128-c238-4562-9b58-c788cf331d7c` | human | 0.244 || BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `53a9510f-de6a-4461-acc1-6fd5cc99c24e` | unsure | 0.431 || HELD |
| EV07 | evasion | signal two: padding with punctuation | 200 | `60182721-3afc-401b-9686-4ec50372ee64` | unsure | 0.570 || HELD |
| EV08 | evasion | signal one: text below the token window | 200 | `561d59b4-faf3-45ad-8526-dcef3669e373` | unsure | 0.382 || HELD |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `95fb1f35-d28a-40d5-96b2-7aff1e8872c3` | unsure | 0.565 || HELD |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `06f5f223-1319-40eb-b447-f16eb71679b8` | unsure | 0.742 || HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `39f10fec-c57c-41ee-842f-3b6919b92058` | unsure | 0.493 || HELD |
| FP02 | false_positive | human writing in a formal register | 200 | `b3252cce-85b0-4f9c-8f74-43907afa5938` | unsure | 0.633 || HELD |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `5391c6d0-ad0f-439e-9d3f-1e00876189e7` | unsure | 0.626 || HELD |
| FP04 | false_positive | a student essay written to a rubric | 200 | `d7d3e718-e749-42d6-9ada-d311348d843e` | unsure | 0.700 || HELD |
| FP05 | false_positive | technical documentation written by a person | 200 | `68263fb1-3cc1-44d1-9f0f-c4207c96da59` | unsure | 0.691 || HELD |
| FP06 | false_positive | a person imitating a formal template | 200 | `98177b9c-773d-4263-bdcf-9f9ade103620` | unsure | 0.619 || HELD |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `b9f4dba7-a388-43ed-9ddb-a2ce1a82a17d` | unsure | 0.591 || HELD |
| FP08 | false_positive | very short genuine human submission | 200 | `e570297e-6dca-4a75-bc38-fd0211ff8ceb` | unsure | 0.370 || HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `10e62461-142d-4966-97fa-a1229d196d50` | unsure | 0.364 || HELD |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `f91b59f6-6ff8-4dc0-b7a8-72eadbd8a51f` | human | 0.204 || BROKE |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `2d459444-c38f-464b-bcc2-4749f91e1f6a` | unsure | 0.416 || HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `e1854907-b6cd-4719-ad9e-cc09f99cc190` | unsure | 0.373 || HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `f6a907c2-bf67-4766-b59e-dbf42c79e3b2` | unsure | 0.426 || HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | `bc477e90-e769-4ef9-b917-f3cd747a9e07` | unsure | 0.465 || HELD |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — || HELD |
| MF02 | malformed | text is a single character | 400 | `—` | — | — || HELD |
| MF03 | malformed | text is control characters | 200 | `234599ce-70c3-4a9a-82d6-a610638626ca` | human | 0.195 || BROKE |
| MF04 | malformed | text is only punctuation | 200 | `20a23e85-6ccb-4f1c-b7e6-bda29042e5bd` | human | 0.276 || BROKE |
| MF05 | malformed | text is a very long single word | 200 | `b09d0d67-5f9f-4747-a181-79dea03b78af` | unsure | 0.694 || BROKE |
| MF06 | malformed | text is emoji only | 200 | `a76cafc0-af4f-43a8-85d8-e4517226c325` | unsure | 0.694 || BROKE |
| MF07 | malformed | text is right-to-left script | 200 | `007f2ffb-ebd4-42af-86ad-f63971ed489e` | unsure | 0.648 || HELD |
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
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `e06b8277-2538-4a60-bd2d-780ac4526b1f` | human | 0.209 || HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `4192a0e6-2ed4-473c-9cc9-69c2fe73c12f` | human | 0.209 || HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `13f501ef-9b42-4d88-b369-be5e9e31b143` | human | 0.209 || HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `a28e3181-4448-4467-892b-7e6527283e78` | human | 0.209 || HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `6a9ed3be-5468-4750-8e0d-a920228f4409` | human | 0.209 || HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `06f918f4-fd9a-4a5b-8c16-ca4dc2589ee5` | human | 0.209 || HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `833044d0-7caa-42ed-970d-c20cab835f91` | human | 0.209 || HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `931a0c6e-9d17-40c6-8b97-0f31d7177784` | human | 0.209 || HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 200 | `2e27498e-35ef-4684-8168-ce7020fbdca6` | human | 0.209 || HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 200 | `b06eef26-6673-4d11-8758-643b45a64ec5` | human | 0.209 || HELD |
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
  "content_id": "2a2f7c36-2fe3-43dc-9ed7-30a76f482dce",
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
  "content_id": "26b70756-4aad-48f4-8095-e65ecfdabdd7",
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
  "content_id": "70d64988-fae4-4b0c-a53b-22ba7ba72bf6",
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
  "content_id": "af25813e-6855-465c-9feb-a18a4780dfca",
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
  "content_id": "0a786128-c238-4562-9b58-c788cf331d7c",
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
  "content_id": "53a9510f-de6a-4461-acc1-6fd5cc99c24e",
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
  "content_id": "60182721-3afc-401b-9686-4ec50372ee64",
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
  "content_id": "561d59b4-faf3-45ad-8526-dcef3669e373",
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
  "content_id": "95fb1f35-d28a-40d5-96b2-7aff1e8872c3",
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
  "content_id": "06f5f223-1319-40eb-b447-f16eb71679b8",
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
  "content_id": "39f10fec-c57c-41ee-842f-3b6919b92058",
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
  "content_id": "b3252cce-85b0-4f9c-8f74-43907afa5938",
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
  "content_id": "5391c6d0-ad0f-439e-9d3f-1e00876189e7",
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
  "content_id": "d7d3e718-e749-42d6-9ada-d311348d843e",
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
  "content_id": "68263fb1-3cc1-44d1-9f0f-c4207c96da59",
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
  "content_id": "98177b9c-773d-4263-bdcf-9f9ade103620",
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
  "content_id": "b9f4dba7-a388-43ed-9ddb-a2ce1a82a17d",
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
  "content_id": "e570297e-6dca-4a75-bc38-fd0211ff8ceb",
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
  "content_id": "10e62461-142d-4966-97fa-a1229d196d50",
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
  "content_id": "f91b59f6-6ff8-4dc0-b7a8-72eadbd8a51f",
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
  "content_id": "2d459444-c38f-464b-bcc2-4749f91e1f6a",
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
  "content_id": "e1854907-b6cd-4719-ad9e-cc09f99cc190",
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
  "content_id": "f6a907c2-bf67-4766-b59e-dbf42c79e3b2",
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
  "content_id": "bc477e90-e769-4ef9-b917-f3cd747a9e07",
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
  "status": 200,
  "content_id": "234599ce-70c3-4a9a-82d6-a610638626ca",
  "creator_id": "attacker_MF03",
  "guess": "human",
  "confidence": 0.195,
  "model_score": 0.0,
  "style_score": 0.65,
  "label": "This reads like it was written by a person. Our automated check found nothing that suggests it was produced by an AI tool.",
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 200,
  "content_id": "20a23e85-6ccb-4f1c-b7e6-bda29042e5bd",
  "creator_id": "attacker_MF04",
  "guess": "human",
  "confidence": 0.2756,
  "model_score": 0.0112,
  "style_score": 0.9,
  "label": "This reads like it was written by a person. Our automated check found nothing that suggests it was produced by an AI tool.",
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 200,
  "content_id": "b09d0d67-5f9f-4747-a181-79dea03b78af",
  "creator_id": "attacker_MF05",
  "guess": "unsure",
  "confidence": 0.6938,
  "model_score": 0.9976,
  "style_score": 0.65,
  "label": "We can't tell how this was written. Our automated check gave mixed results, which happens with a lot of genuine human writing, so we are not making any claim about it either way.",
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 200,
  "content_id": "a76cafc0-af4f-43a8-85d8-e4517226c325",
  "creator_id": "attacker_MF06",
  "guess": "unsure",
  "confidence": 0.6935,
  "model_score": 0.9969,
  "style_score": 0.65,
  "label": "We can't tell how this was written. Our automated check gave mixed results, which happens with a lot of genuine human writing, so we are not making any claim about it either way.",
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
  "content_id": "007f2ffb-ebd4-42af-86ad-f63971ed489e",
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
  "content_id": "e06b8277-2538-4a60-bd2d-780ac4526b1f",
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
  "content_id": "4192a0e6-2ed4-473c-9cc9-69c2fe73c12f",
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
  "content_id": "13f501ef-9b42-4d88-b369-be5e9e31b143",
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
  "content_id": "a28e3181-4448-4467-892b-7e6527283e78",
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
  "content_id": "6a9ed3be-5468-4750-8e0d-a920228f4409",
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
  "content_id": "06f918f4-fd9a-4a5b-8c16-ca4dc2589ee5",
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
  "content_id": "833044d0-7caa-42ed-970d-c20cab835f91",
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
  "content_id": "931a0c6e-9d17-40c6-8b97-0f31d7177784",
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
  "content_id": "2e27498e-35ef-4684-8168-ce7020fbdca6",
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
  "content_id": "b06eef26-6673-4d11-8758-643b45a64ec5",
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
