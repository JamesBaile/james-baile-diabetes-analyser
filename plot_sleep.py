import fitbit
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import arrow  # Arrow is a really useful date time helper library

sleep_data = pd.read_json('sleep.json')

# Sleep distribution
(sleep_data["total_sleep_minutes"]/60).plot(
    kind="hist",
    bins=50,
    alpha=0.8,
    figsize=(12,8)
)
(sleep_data["total_time_in_bed"]/60).plot(
    kind="hist",
    bins=50,
    alpha=0.8
)
plt.legend()

# add some nice axis labels:
ax = plt.gca()
ax.set_xticks(range(2,12))
plt.grid("minor", linestyle=":")
plt.xlabel("Hours")
plt.ylabel("Frequency")
plt.title("Sleeping Hours")

# Plot a scatter plot directly from Pandas
sleep_data.plot(
  x="total_time_in_bed",
  y="total_sleep_minutes",
  kind="scatter",
  figsize=(10, 10)
)
# Add a perfect 1:1 line for comparison
ax = plt.gca()
ax.set_aspect("equal")
x = np.linspace(*ax.get_xlim())
ax.plot(x, x, linestyle="--")
plt.grid(linestyle=":")

# Sleep makeup - calculate data to plot
plot_data = sleep_data. \
  sort_values("date"). \
  set_index("date") \
  [["deep_minutes", "light_minutes", "rem_minutes", "wake_minutes"]]

# Matplotlib doesn't natively support stacked bars, so some messing here:
df = plot_data
fig, ax = plt.subplots(figsize=(30, 7), constrained_layout=True)

bottom = 0
for c in df.columns:
  ax.bar(df.index, df[c], bottom=bottom, width=1, label=c)
  bottom += df[c]

# Set a date axis for the x-axis allows nicer tickmarks.
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
ax.legend()

plt.xlabel("Date")
plt.ylabel("Minutes")
# Show a subset of data for clarity on the website:
plt.xlim(pd.to_datetime("2022-01-01"), pd.to_datetime("2023-01-01"))

plt.show()








