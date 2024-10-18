import data_ingestion as di
import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

class RaceData:

    def __init__(self, motec_file):
        self.motec_file = motec_file
        self.content = np.array(self.clean_data())
        self.lap_time_intervals = self.race_laps()
        self.time_intervals = self.interp_time_intervals()
        self.speed = self.speed_mph()
        self.throttle_input = []
        self.break_input = []
        self.steering_input = []


    def clean_data(self):
        file_content = di.raw_data(self.motec_file)
        cleaned_data = []
        for line in file_content:
            separate_data = line.split(",")
            float_data = [num.strip('"') for num in separate_data]
            cleaned_data.append(float_data)
        return cleaned_data

    def race_laps(self):
        with open(self.motec_file, 'r') as f:
            data_lines = [line.strip() for line in f]
        laps_line = data_lines[11].split(',')
        laps_time = laps_line[1].strip('"').split(' ')
        cleaned_laps_time = [float(time) for time in (filter(None, laps_time))]

        return cleaned_laps_time

    def interp_time_intervals(self):
        raw_times = self.content[:, 0].astype(float)
        interped_times = np.arange(0, raw_times[-1] + 0.001, 0.001)

        return interped_times

    def speed_mph(self):
        speed_m_per_s = np.interp(self.time_intervals, self.content[:,0].astype(float), self.content[:,5].astype(float))
        speed_mph = [speed * 2.237 for speed in speed_m_per_s]

        return speed_mph

    def plot_graph(self, x, y):
        df = pd.DataFrame({"x": x, "y":y})
        sns.lineplot(x=x, y=y, data=df)
        plt.grid(True)
        plt.show()

motec_file = 'trial.csv'

data = RaceData(motec_file)
#data.plot_graph(data.time_intervals, data.speed)

with open(motec_file, 'r') as f:
    lines = [line.strip() for line in f]
    headers = lines[14].split(',')
    for header in headers:
        print(header)

"""I need to figure out how to structure this part better. Can I interpolate other values based on a new time interval?"""
race_df = pd.DataFrame({
    "Time": data.time_intervals,
    "LAP_BEACON": data.time_intervals,
    "G_LAT": data.time_intervals,
    "ROTY": data.time_intervals,
    "STEERANGLE": data.time_intervals,
    "SPEED": data.time_intervals,
    "THROTTLE": data.time_intervals,
    "BRAKE": data.time_intervals,
    "GEAR": data.time_intervals,
    "G_LON": data.time_intervals,
    "CLUTCH": data.time_intervals,
    "RPMS": data.time_intervals,
    "TC": data.time_intervals,
    "ABS": data.time_intervals,
    "SUS_TRAVEL_LF": data.time_intervals,
    "SUS_TRAVEL_RF": data.time_intervals,
    "SUS_TRAVEL_LR": data.time_intervals,
    "SUS_TRAVEL_RR": data.time_intervals,
    "BRAKE_TEMP_LF": data.time_intervals,
    "BRAKE_TEMP_RF": data.time_intervals,
    "BRAKE_TEMP_LR": data.time_intervals,
    "BRAKE_TEMP_RR": data.time_intervals,
    "TYRE_PRESS_LF":data.time_intervals,
    "TYRE_PRESS_RF":data.time_intervals,
    "TYRE_PRESS_LR":data.time_intervals,
    "TYRE_PRESS_RR":data.time_intervals,
    "TYRE_TAIR_LF":data.time_intervals,
    "TYRE_TAIR_RF":data.time_intervals,
    "TYRE_TAIR_LR":data.time_intervals,
    "TYRE_TAIR_RR":data.time_intervals,
    "WHEEL_SPEED_LF":data.time_intervals,
    "WHEEL_SPEED_RF":data.time_intervals,
    "WHEEL_SPEED_LR":data.time_intervals,
    "WHEEL_SPEED_RR":data.time_intervals,
    "BUMPSTOPUP_RIDE_LF":data.time_intervals,
    "BUMPSTOPUP_RIDE_RF":data.time_intervals,
    "BUMPSTOPUP_RIDE_LR":data.time_intervals,
    "BUMPSTOPUP_RIDE_RR":data.time_intervals,
    "BUMPSTOPDN_RIDE_LF":data.time_intervals,
    "BUMPSTOPDN_RIDE_RF":data.time_intervals,
    "BUMPSTOPDN_RIDE_LR":data.time_intervals,
    "BUMPSTOPDN_RIDE_RR":data.time_intervals,
    "BUMPSTOP_FORCE_LF":data.time_intervals,
    "BUMPSTOP_FORCE_RF":data.time_intervals,
    "BUMPSTOP_FORCE_LR":data.time_intervals,
    "BUMPSTOP_FORCE_RR":data.time_intervals,
    "BUMPSTOP_DAMP_LF":data.time_intervals,
    "BUMPSTOP_DAMP_RF":data.time_intervals,
    "BUMPSTOP_DAMP_LR":data.time_intervals,
    "BUMPSTOP_DAMP_RR":data.time_intervals
})

print(race_df)