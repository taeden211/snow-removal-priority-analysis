import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager


font_path = "C:/Windows/Fonts/batang.ttc"
font_name = font_manager.FontProperties(fname=font_path).get_name()
plt.rcParams["font.family"] = font_name
plt.rcParams["axes.unicode_minus"] = False


def add_bar_labels(ax, bars):
    upper = ax.get_ylim()[1]
    for bar in bars:
        yval = bar.get_height()
        y_pos = max(yval - upper * 0.05, yval * 0.5)
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            y_pos,
            f"{yval:.2f}",
            ha="center",
            va="top",
            fontsize=9,
            color="black",
            clip_on=True,
        )


def add_line_labels(ax, values):
    y_min, y_max = ax.get_ylim()
    offset = (y_max - y_min) * 0.08
    place_above = {0, 4}

    for i, val in enumerate(values):
        if pd.isna(val):
            continue

        above = i in place_above
        dx = 0
        dy = 12 if above else -12
        y_pos = val + (offset if above else -offset)
        y_pos = min(max(y_pos, y_min + offset), y_max - offset)

        ax.annotate(
            f"{val:.2f}",
            xy=(i, val),
            xytext=(dx, dy),
            textcoords="offset points",
            ha="center",
            va="bottom" if above else "top",
            fontsize=9,
            bbox={"facecolor": "white", "alpha": 0.75, "edgecolor": "none", "pad": 1.5},
            arrowprops={"arrowstyle": "-", "color": "#777777", "lw": 0.8, "alpha": 0.7},
            clip_on=True,
        )


df = pd.read_csv("데이터/기상 데이터/OBS_ASOS_DD_20260331104754.csv", encoding="cp949")
df["일시"] = pd.to_datetime(df["일시"])
df["Month"] = df["일시"].dt.month

df["일 최심신적설(cm)"] = pd.to_numeric(df["일 최심신적설(cm)"], errors="coerce")
df["최저기온(°C)"] = pd.to_numeric(df["최저기온(°C)"], errors="coerce")
df["평균 지면온도(°C)"] = pd.to_numeric(df["평균 지면온도(°C)"], errors="coerce")

winter_months = [11, 12, 1, 2, 3]
df_winter = df[df["Month"].isin(winter_months)]

df_snow_only = df_winter[df_winter["일 최심신적설(cm)"] > 0]
snow_avg = df_snow_only.groupby("Month")["일 최심신적설(cm)"].mean()
snow_avg = snow_avg.reindex(winter_months).fillna(0)

temp_avg = df_winter.groupby("Month")[["최저기온(°C)", "평균 지면온도(°C)"]].mean()
temp_avg = temp_avg.reindex(winter_months)

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
x_labels = ["11월", "12월", "1월", "2월", "3월"]
x_pos = list(range(len(winter_months)))

ax = axes[0]
bars = ax.bar(x_pos, snow_avg.values, color="skyblue", edgecolor="steelblue")
ax.set_xticks(x_pos, x_labels)
ax.set_ylabel("적설량 (cm)")
ax.grid(axis="y", linestyle="--", alpha=0.35)
ax.set_axisbelow(True)
ax.set_ylim(0, max(snow_avg.max() * 1.18, 1))
add_bar_labels(ax, bars)

ax = axes[1]
min_temp_values = temp_avg["최저기온(°C)"].values
ax.plot(x_pos, min_temp_values, marker="o", color="royalblue", linewidth=2)
ax.set_xticks(x_pos, x_labels)
ax.set_ylabel("기온 (°C)")
ax.grid(axis="y", linestyle="--", alpha=0.35)
ax.set_axisbelow(True)
ax.margins(y=0.18)
add_line_labels(ax, min_temp_values)

ax = axes[2]
ground_temp_values = temp_avg["평균 지면온도(°C)"].values
ax.plot(x_pos, ground_temp_values, marker="o", color="seagreen", linewidth=2)
ax.set_xticks(x_pos, x_labels)
ax.set_ylabel("온도 (°C)")
ax.grid(axis="y", linestyle="--", alpha=0.35)
ax.set_axisbelow(True)
ax.margins(y=0.18)
add_line_labels(ax, ground_temp_values)

fig.tight_layout()
fig.savefig("기상 데이터 시각화.png", dpi=200, bbox_inches="tight")
print("Saved")
