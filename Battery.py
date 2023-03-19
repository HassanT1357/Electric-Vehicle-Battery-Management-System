import time
import matplotlib.pyplot as plt
import numpy as np


def coulomb_counting(current, delta_time, battery_capacity):
    return current * delta_time / battery_capacity
  #integral :)

def overcurrent_protection(current):
  overcurrent = False
  current_limit = 15_000 #Current Draw Limit is 15A or 15k mA
  if current > current_limit:
    overcurrent = True

  return overcurrent

def temperature_change(current, initial_temperature, time_step, max_temperature_change):
    temperature_coefficient = max_temperature_change / 10000  # Adjust the scaling factor
    delta_temperature = current * temperature_coefficient * time_step
    return initial_temperature + delta_temperature


  
def optimal_charging_current(soc, temperature, max_charging_current):
    if temperature >= 60:  # Update the temperature threshold
        return max_charging_current * 0.5

    if soc < 80:
        return max_charging_current
    elif soc < 95:
        return max_charging_current * 0.5
    else:
        return max_charging_current * 0.2


def simulate_soc_with_optimal_charging_and_protection(battery_capacity, max_charging_current, discharging_current, simulation_duration, delta_time, max_discharging_current, initial_temperature, max_temperature_change):
    soc = 0
    time_elapsed = 0
    temperature = initial_temperature

    soc_list = [0]
    time_list = [0]

    # Charging phase
    while soc < 99 and time_elapsed < simulation_duration:
        charging_current = optimal_charging_current(soc, temperature, max_charging_current)
        
        if overcurrent_protection(charging_current):
            print("Overcurrent detected during charging! Reducing current...")
            charging_current = max_charging_current

        soc += coulomb_counting(charging_current, delta_time, battery_capacity) * 100
        soc_list.append(soc)
        temperature = temperature_change(charging_current, temperature, delta_time, max_temperature_change)
        print(f"Charging... SoC: {soc:.2f}%, Charging current: {charging_current} mA, Temperature: {temperature:.2f}°C")
        time_elapsed += delta_time
        time_list.append(time_elapsed)
        time.sleep(delta_time)

    # Discharging phase
    while soc > 1 and time_elapsed < simulation_duration:
        if overcurrent_protection(discharging_current):
            print("Overcurrent detected during discharging! Reducing current...")
            discharging_current = max_discharging_current

        soc -= coulomb_counting(discharging_current, delta_time, battery_capacity) * 100
        soc_list.append(soc)
        temperature = temperature_change(-discharging_current, temperature, delta_time, max_temperature_change)
        print(f"Discharging... SoC: {soc:.2f}%, Temperature: {temperature:.2f}°C")
        time_elapsed += delta_time
        time_list.append(time_elapsed)
        time.sleep(delta_time)
    return time_list, soc_list


def main():
    battery_capacity = 60_000  # Battery capacity in mAh
    charging_current = 3_000  # Charging current in mA
    max_charging_current = 15_000
    max_discharging_current = 5000
    discharging_current = 2_000  # Discharging current in mA
    simulation_duration = 60  # Simulation duration in seconds
    delta_time = 1  # Time step for the simulation in seconds
    initial_temperature = 25  # Initial battery temperature in °C
    max_temperature_change = 2
    time_values, soc_values = simulate_soc_with_optimal_charging_and_protection(battery_capacity, max_charging_current, discharging_current, simulation_duration, delta_time, max_discharging_current, initial_temperature, max_temperature_change)

    plt.plot(time_values, soc_values)
    plt.xlabel('Time (s)')
    plt.ylabel('State of Charge (%)')
    plt.title('Battery State of Charge vs. Time')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()


# = ) Made by Yousuf Ali, Shiza Shaikh, Hassan Tahir