"""Function which takes vehicle information as well as track data to analyse if the car is
oversteering/understeering/neutral steering. The goal is to make sure the car is constantly
neutral steering in the corners"""
import pandas as pd


def neutral_steer(Vehicle, RaceData):
    g_lat = RaceData.raw_data[:,2].astype(float)
    steer_angle = RaceData.raw_data[:, 4].astype(float)
    speed = RaceData.raw_data[:, 5].astype(float)
    cog_height = np.full((1, len(g_lat)), Vehicle.CoG_height)
    wheelbase = np.full((1, len(g_lat)), Vehicle.wheelbase)
    steering_ratio = np.full((1, len(g_lat)), Vehicle.SteeringRatio)
    g_acceleration = np.full((1, len(g_lat)), 9.81)

    eq_expression_1 = np.divide((np.multiply(g_lat, cog_height)), wheelbase)
    eq_expression_2 = np.divide((np.multiply(np.multiply(steer_angle, steering_ratio), speed ** 2)),
                             (np.multiply(wheelbase, g_acceleration)))
    yaw_moment = eq_expression_1 - eq_expression_2

    neutral_steer_indices = np.where(yaw_moment != 0)

    return neutral_steer_indices

