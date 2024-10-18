import data_ingestion as di
import matplotlib.pyplot as plt
import numpy as np
import bisect


def clean_data(motec_file)->list:
    raw_track_data = di.raw_data(motec_file)
    cleaned_data = []
    for dataline in raw_track_data:
        separated_data = dataline.split(",")
        float_data = [num.strip('"') for num in separated_data]
        cleaned_data.append(float_data)
    return cleaned_data


def race_laps(motec_file)->list:
    with open(motec_file, 'r') as f:
        data_lines = [line.strip() for line in f]
    laps_line = data_lines[11].split(',')
    laps_data = laps_line[1].strip('"').split(' ')
    cleaned_laps_data = [float(time) for time in (filter(None, laps_data))]

    return cleaned_laps_data

"""Class to store different vehicles used within ACC. NEEDS MORE WORK AND THINKING"""
class Vehicle:

    """Defines the parameters needed from the car to be used for analysing the data"""
    def __init__(self, CoG_height=float, wheelbase=float, SteeringRatio=float):

        """Estimated height of the car's centre of gravity"""
        self.CoG_height = CoG_height

        """Distance between front and rear axles"""
        self.wheelbase = wheelbase

        """Ratio between steering wheel rotation and wheel rotation"""
        self.SteeringRatio = SteeringRatio

class LapData:

    def __init__(self, lap_number):
        self.lap_number = lap_number
        self.time_intervals = []
        self.speed_data = []
        self.steerangle = []
        self.throttle = []
        self.braking_data = []


def interpolate_data(motec_file) -> list:

    data = np.array(clean_data(motec_file))
    time = data[:,0].astype(float)
    speed = data[:,5].astype(float)
    steerangle = data[:,4].astype(float)
    throttle = data[:,6].astype(float)
    brake = data[:,7].astype(float)
    relevant_data = [time, speed, steerangle, throttle, brake]

    interpolated_time = np.arange(0, time[-1] + 0.001, 0.001)

    for i in range(len(relevant_data)):
        if i != 1:
            interpolated_data = np.interp(interpolated_time, time, relevant_data[i - 1])
            relevant_data[i - 1] = interpolated_data
        else:
            continue

    relevant_data[0] = interpolated_time

    return relevant_data


def beacon_indices(motec_file) -> list:

    interped_data = interpolate_data(motec_file)

    beacon_times = race_laps(motec_file)
    beacon_indices = [bisect.bisect_left(interped_data[0], time) for time in beacon_times]
    beacon_indices.insert(0, 0)
    beacon_indices.append(len(interped_data[0]) - 1)

    return beacon_indices


def create_laps(motec_file):

    beacons_index_loc = beacon_indices(motec_file)

    laps = [LapData(i + 1) for i in range(len(beacons_index_loc) - 1)]

    return laps

def add_data_to_laps(motec_file):
    
    interped_data = interpolate_data(motec_file)
    beacon_index_loc = beacon_indices(motec_file)
    laps = create_laps(motec_file)

    for i in range(len(laps)):
        try:
            lap_time = interped_data[0][beacon_index_loc[i]:beacon_index_loc[i + 1]]
            lap_speed = interped_data[1][beacon_index_loc[i]:beacon_index_loc[i + 1]]
            lap_speed = [speed * 2.237 for speed in lap_speed]
            steerangle = interped_data[2][beacon_index_loc[i]:beacon_index_loc[i + 1]]
            throttle = interped_data[3][beacon_index_loc[i]:beacon_index_loc[i + 1]]
            braking = interped_data[4][beacon_index_loc[i]:beacon_index_loc[i + 1]]
            laps[i].time_intervals = lap_time
            laps[i].speed_data = lap_speed
            laps[i].steerangle = steerangle
            laps[i].throttle = throttle
            laps[i].braking_data = braking
        except IndexError:
            break

    for i in range(len(laps)):
        if laps[i].time_intervals[0] != 0:
            time_datum = laps[i].time_intervals[0]
            laps[i].time_intervals = [x - time_datum for x in laps[i].time_intervals]
        else:
            continue

    return laps


def speed_time_plot(laps):
    for i in range(len(laps)):
        x = laps[i].time_intervals
        y = laps[i].speed_data
        plt.plot(x, y, label=f"Lap {i + 1}")

    plt.xlabel('Time (s)')
    plt.ylabel('Speed (mph)')
    plt.title('Speed and Time Plot')
    plt.grid()
    plt.legend()
    plt.show()


def steering_plot(laps):
    for i in range(len(laps)):
        x = laps[i].time_intervals
        y = laps[i].steerangle
        plt.plot(x, y, label=f"Lap {i + 1}")

    plt.xlabel('Time (s)')
    plt.ylabel('Steer Angle (deg)')
    plt.title('Steer Angle and Time Plot')
    plt.grid()
    plt.legend()
    plt.show()


def brake_throttle_plot(laps):
    for i in range(len(laps)):
        x = laps[i].time_intervals
        y1 = laps[i].throttle
        y2 = laps[i].braking_data
        plt.plot(x, y1, label=f"Lap {i + 1}")
        plt.plot(x, y2, label=f"Lap {i + 1}")

    plt.xlabel('Time (s)')
    plt.ylabel('Throttle/Brake Percentage (%)')
    plt.title('Throttle and Brake Plot')
    plt.grid()
    plt.legend()
    plt.show()


"""Trial Data and Vehicle"""
motec_file = 'trial.csv'
amr_v8_gt3 = Vehicle(0.3, 2.73, 13.09)

x = add_data_to_laps(motec_file)
steering_plot(x)
