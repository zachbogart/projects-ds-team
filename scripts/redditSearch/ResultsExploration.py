import pandas as pd
import time

chicago = pd.read_json('/home/khalana/projects-ds-team/data/chicago_weather_sentiment_clean.json')

chicago['dayHour'] = chicago['local_datetime']['date'].apply(lambda x: time.strftime('%Y-%m-%d %h'),x)

