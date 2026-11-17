# Conversation with the AI

I used Claude as a tutor, step by step. Below are the main steps and the errors I hit.

## Step 1 - Reading the CSV
- I asked how to read a CSV file in Python.
- The file uses `;` as separator, so I used `csv.DictReader(f, delimiter=";")`.
- The file starts with an invisible character (BOM), so I opened it with `encoding="utf-8-sig"`.
- **Error:** the uploaded file was called `campaigns_C (1).csv`. **Fix:** renamed it to `campaigns_C.csv`.

## Step 2 - Converting text to numbers
- The numbers were read as text, with a decimal comma (`50917,23`).
- **Fix:** function `to_number` replaces `,` with `.` and converts with `float()`. Empty cells become `None`.
- The CSV has an empty column (`;;`), so I read columns by name, not by position.

## Step 3 - CTR, CPA, ROAS
- Campaigns with empty impressions are skipped (B2B Webinar): 11 campaigns left.
- Two campaigns have 0 conversions (Monthly Newsletter, Blog Traffic): dividing by zero would crash with `ZeroDivisionError`. **Fix:** CPA = `None` for them.
- Hand check: Winter Sale CTR = 29114 / 767000 = 0.038 = 3.8%. The program printed 3.8. Correct.

## Step 4 - Correct answers
- The program computes: Cart Retargeting, Black Friday, 5, LinkedIn Ads, 3.12.

## Step 5 - Quiz and result.csv
- **Error:** `python: can't open file 'campaign_audit.py': No such file or directory`.
  The file had been created with the wrong name `code campaign_audit.py`.
  **Fix:** renamed it to `campaign_audit.py`.
- Note: for question 5 the answer must be typed with a dot (`3.12`), not a comma.
- Final test: score 5/5, result.csv created.