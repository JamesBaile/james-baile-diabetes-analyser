import fitbit
import pandas as pd
import arrow  # Arrow is a really useful date time helper library

client = fitbit.Fitbit(
    
)

start_date = arrow.get("2018-09-01")
end_date = arrow.get("2023-01-13")

# Create a series of 100-day date-range tuples between start_date and end_date
date_ranges = []
start_range = start_date
while start_range < end_date:
  if start_range.shift(days=100) < end_date:
    date_ranges.append((start_range, start_range.shift(days=100)))
    start_range = start_range.shift(days=101)
  else:
    date_ranges.append((start_range, end_date))
    start_range = end_date

# Print the result to the console
# date_ranges

all_data = []
for date_range in date_ranges:
  print(f"Requesting data for {date_range[0]} to {date_range[1]}.")
  url = f"{client.API_ENDPOINT}/1.2/user/-/sleep/date/{date_range[0].year}-{date_range[0].month:02}-{date_range[0].day:02}/{date_range[1].year}-{date_range[1].month:02}-{date_range[1].day:02}.json"
  range_data = client.make_request(url)
  all_data.append(range_data)
  print(f"Success!")

  sleep_summaries = []
  # Iterate through all data and create a list of dictionaries of results:
  for data in all_data:
      for sleep in data["sleep"]:
          # For simplicity, ignoring "naps" and going for only "stage" data
          if sleep["isMainSleep"] and sleep["type"] == "stages":
              sleep_summaries.append(dict(
                  date=pd.to_datetime(sleep["dateOfSleep"]).date(),
                  duration_hours=sleep["duration"] / 1000 / 60 / 60,
                  total_sleep_minutes=sleep["minutesAsleep"],
                  total_time_in_bed=sleep["timeInBed"],
                  start_time=sleep["startTime"],
                  deep_minutes=sleep["levels"]["summary"].get("deep").get("minutes"),
                  light_minutes=sleep["levels"]["summary"].get("light").get("minutes"),
                  rem_minutes=sleep["levels"]["summary"].get("rem").get("minutes"),
                  wake_minutes=sleep["levels"]["summary"].get("wake").get("minutes"),
              ))

  # Convert new dictionary format to DataFrame
  sleep_data = pd.DataFrame(sleep_summaries)
  # Sort by date and view first rows
  sleep_data.sort_values("date", inplace=True)
  sleep_data.reset_index(drop=True, inplace=True)
  sleep_data.head()

  # It's useful for grouping to get the "date" from every timestamp
  sleep_data["date"] = pd.to_datetime(sleep_data["date"])
  # Also add a boolean column for weekend detection
  sleep_data["is_weekend"] = sleep_data["date"].dt.weekday > 4

  sleep_data.to_json('sleep.json')
