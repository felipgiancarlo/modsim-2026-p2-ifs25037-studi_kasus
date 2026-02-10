import pandas as pd
from collections import Counter

# =============================
# LOAD DATA
# =============================
df = pd.read_excel("data_kuesioner.xlsx")
questions = df.columns[1:]
n = len(df)

# =============================
# SKOR
# =============================
score_map = {
    "SS": 6, "S": 5, "CS": 4,
    "CTS": 3, "TS": 2, "STS": 1
}

# =============================
# FLATTEN DATA (BERSIH)
# =============================
all_answers = (
    df[questions]
    .stack()
    .dropna()
    .tolist()
)

count_all = Counter(all_answers)
total_answers = len(all_answers)

target_question = input()

# =============================
# q1
# =============================
if target_question == "q1":
    s, j = count_all.most_common(1)[0]
    print(f"{s}|{j}|{round(j/total_answers*100,1)}")

# =============================
# q2
# =============================
elif target_question == "q2":
    s, j = min(count_all.items(), key=lambda x: x[1])
    print(f"{s}|{j}|{round(j/total_answers*100,1)}")

# =============================
# q3 — SS
# =============================
elif target_question == "q3":
    qmax = max(questions, key=lambda q: (df[q] == "SS").sum())
    j = (df[qmax] == "SS").sum()
    print(f"{qmax}|{j}|{round(j/n*100,1)}")

# =============================
# q4 — S
# =============================
elif target_question == "q4":
    qmax = max(questions, key=lambda q: (df[q] == "S").sum())
    j = (df[qmax] == "S").sum()
    print(f"{qmax}|{j}|{round(j/n*100,1)}")

# =============================
# q5 — CS
# =============================
elif target_question == "q5":
    qmax = max(questions, key=lambda q: (df[q] == "CS").sum())
    j = (df[qmax] == "CS").sum()
    print(f"{qmax}|{j}|{round(j/n*100,1)}")

# =============================
# q6 — CTS
# =============================
elif target_question == "q6":
    qmax = max(questions, key=lambda q: (df[q] == "CTS").sum())
    j = (df[qmax] == "CTS").sum()
    print(f"{qmax}|{j}|{round(j/n*100,1)}")

# =============================
# q7 — TS
# =============================
elif target_question == "q7":
    qmax = max(questions, key=lambda q: (df[q] == "TS").sum())
    j = (df[qmax] == "TS").sum()
    print(f"{qmax}|{j}|{round(j/n*100,1)}")

# =============================
# q8 — STS
# =============================
elif target_question == "q8":
    qmax = max(questions, key=lambda q: (df[q] == "STS").sum())
    j = (df[qmax] == "STS").sum()
    print(f"{qmax}|{j}|{round(j/n*100,1)}")

# =============================
# q9
# =============================
elif target_question == "q9":
    res = []
    for q in questions:
        j = (df[q] == "STS").sum()
        if j > 0:
            res.append(f"{q}:{round(j/n*100,1)}")
    print("|".join(res))

# =============================
# q10
# =============================
elif target_question == "q10":
    avg = sum(score_map[x] for x in all_answers) / total_answers
    print(f"{avg:.2f}")

# =============================
# q11
# =============================
elif target_question == "q11":
    qmax = max(
        questions,
        key=lambda q: df[q].dropna().map(score_map).mean()
    )
    avg = df[qmax].dropna().map(score_map).mean()
    print(f"{qmax}:{avg:.2f}")

# =============================
# q12
# =============================
elif target_question == "q12":
    qmin = min(
        questions,
        key=lambda q: df[q].dropna().map(score_map).mean()
    )
    avg = df[qmin].dropna().map(score_map).mean()
    print(f"{qmin}:{avg:.2f}")

# =============================
# q13
# =============================
elif target_question == "q13":
    pos = count_all.get("SS", 0) + count_all.get("S", 0)
    net = count_all.get("CS", 0)
    neg = (
        count_all.get("CTS", 0)
        + count_all.get("TS", 0)
        + count_all.get("STS", 0)
    )

    print(
        f"positif={pos}:{round(pos/total_answers*100,1)}|"
        f"netral={net}:{round(net/total_answers*100,1)}|"
        f"negatif={neg}:{round(neg/total_answers*100,1)}"
    )
