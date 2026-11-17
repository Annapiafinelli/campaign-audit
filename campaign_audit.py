import csv
from datetime import datetime


# Converts text like "50917,23" into a number; returns None if the cell is empty
def to_number(text):
    text = text.strip()
    if text == "":
        return None
    return float(text.replace(",", "."))


# Reads the CSV (separator ;) and returns a list of campaigns
def load_campaigns(path):
    campaigns = []
    with open(path, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            # skip empty lines
            if row["Campaign"].strip() == "":
                continue
            campaigns.append({
                "name": row["Campaign"].strip(),
                "channel": row["Channel"].strip(),
                "impressions": to_number(row["Impressions"]),
                "clicks": to_number(row["Clicks"]),
                "cost": to_number(row["Cost (€)"]),
                "conversions": to_number(row["Conversions"]),
                "revenue": to_number(row["Revenue (€)"]),
            })
    return campaigns


# Computes CTR, CPA, ROAS; skips campaigns with no impressions, no CPA if 0 conversions
def compute_kpis(campaigns):
    valid = []
    for c in campaigns:
        # rule 1: empty impressions -> excluded from every calculation
        if c["impressions"] is None:
            continue
        c["ctr"] = c["clicks"] / c["impressions"]
        c["roas"] = c["revenue"] / c["cost"]
        # rule 2: 0 conversions -> no CPA (avoids division by zero)
        if c["conversions"] == 0:
            c["cpa"] = None
        else:
            c["cpa"] = c["cost"] / c["conversions"]
        valid.append(c)
    return valid


# Computes the correct answers to the 5 questions
def build_questions(campaigns):
    # 1. best CTR
    best_ctr = max(campaigns, key=lambda c: c["ctr"])

    # 2. highest CPA (only campaigns that have a CPA)
    with_cpa = [c for c in campaigns if c["cpa"] is not None]
    highest_cpa = max(with_cpa, key=lambda c: c["cpa"])

    # 3. how many campaigns have ROAS above 3
    roas_above_3 = 0
    for c in campaigns:
        if c["roas"] > 3:
            roas_above_3 += 1

    # 4. channel with the most conversions in total
    totals = {}
    for c in campaigns:
        totals[c["channel"]] = totals.get(c["channel"], 0) + c["conversions"]
    top_channel = max(totals, key=totals.get)

    # 5. average CTR in %, rounded to 2 decimals
    avg_ctr = round(sum(c["ctr"] for c in campaigns) / len(campaigns) * 100, 2)

    return [
        ("Which campaign has the best CTR?", best_ctr["name"]),
        ("Which campaign has the highest CPA?", highest_cpa["name"]),
        ("How many campaigns have a ROAS above 3?", str(roas_above_3)),
        ("Which channel generated the most conversions in total?", top_channel),
        ("What is the average CTR across all campaigns (in %, two decimals)?", str(avg_ctr)),
    ]


# Asks the questions, checks the answers and counts the score
def play(questions):
    score = 0
    for question, correct in questions:
        answer = input(question + "\n> ").strip()
        if answer.lower() == correct.lower():
            print("Correct!\n")
            score += 1
        else:
            print("Wrong. The answer was:", correct, "\n")
    return score


# Adds a line with name, score and date to result.csv
def save_result(name, score):
    with open("result.csv", "a", encoding="utf-8") as f:
        date = datetime.now().strftime("%Y-%m-%d")
        f.write(f"{name};{score}/5;{date}\n")


# Runs all the steps in order and shows a message if something goes wrong
def main():
    try:
        campaigns = compute_kpis(load_campaigns("campaigns_C.csv"))
        questions = build_questions(campaigns)
        name = input("Your name: ").strip()
        score = play(questions)
        print("Final score:", score, "/ 5")
        save_result(name, score)
    except FileNotFoundError:
        print("Error: campaigns_C.csv not found.")
    except Exception as e:
        print("Unexpected error:", e)


main()