import matplotlib.pyplot as plt

def plot_bar(records, title="Monthly Electricity Token Usage"):
    if not records:
        print("No data to plot.")
        return
    labels = [f"{r['date'].year}-{r['date'].month:02d}" for r in records]
    vals = [r['value'] for r in records]
    plt.figure(figsize=(10, 5))
    plt.bar(labels, vals)
    plt.xticks(rotation=45, ha="right")
    plt.ylabel("Token Value")
    plt.title(title)
    plt.tight_layout()
    plt.show()

def ascii_bar_chart(records, width=50):
    if not records:
        print("No data")
        return
    vals = [r["value"] for r in records]
    maxv = max(vals) if vals else 1
    labels = [f"{r['date'].year}-{r['date'].month:02d}" for r in records]
    for lab, v in zip(labels, vals):
        bar_len = int((v / maxv) * width)
        print(f"{lab:10s} | {'█' * bar_len} {v:.2f}")
