PREPARE PHASE — ANALYST CHECKLIST v1.0

Use this before touching PROCESS.

Print it.
Memorize it.
Eventually you won’t need it.

1️⃣ Dataset Identity

Before anything:

What is the dataset name?

Where does it come from?

What business domain?

What time period?

How many tables?

How many rows per table?

If you cannot answer these in 2 minutes, you’re not ready to analyze.

2️⃣ Granularity Check (Most Important)

Ask:

What does ONE row represent?

Order?

Line item?

Customer?

Day?

Is there a natural primary key?

Are there duplicates?

If granularity is unclear → stop.

This prevents 70% of beginner mistakes.

3️⃣ Schema Scan

For each table:

List columns

Infer data types

Identify:

IDs

Measures (numeric values)

Categories

Dates

Separate:

Keys

Descriptors

Metrics

That mental separation is core analyst thinking.

4️⃣ Relationship Mapping (If Multi-Table)

What is the fact table?

What are dimensions?

What are foreign keys?

Do keys match in count?

Are there orphan keys?

If joins are wrong → all analysis is wrong.

5️⃣ Missingness Overview

For each column:

Any nulls?

How many?

Pattern random or systematic?

Never fix yet. Only observe.

6️⃣ Measure Validation (Critical for Revenue Case)

For every metric:

Can it be negative?

Can it be zero?

Does it have extreme outliers?

Is it derived (like quantity × price)?

You must understand how the core metric behaves before using it.

7️⃣ Basic Distribution Sanity Check

Quick mental checks:

Top categories?

Unusual values?

Suspicious repetition?

Dates continuous?

You are looking for “smell.”

Good analysts develop “data smell detection.”

8️⃣ Assumptions Log

Write:

What you assume is true

What you have not yet validated

What could break analysis later

This builds intellectual humility.

How You Build This Skill

Not by reading my markdown.

By doing this repeatedly:

Open dataset

Without help, answer checklist questions

Compare your observations with structured version

Identify what you missed

Repeat on next dataset

After 5–6 datasets, this becomes automatic.

Here’s the Key

I am fast because I:

Know the pattern

Have seen 100+ datasets

Recognize schema archetypes

You build that only by repetition.