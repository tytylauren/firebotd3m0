# pymavlink.py

from pymavlink import mavutil
import time

# Connect to the Vehicle
master = mavutil.mavlink_connection('udp:127.0.0.1:14551')
master.wait_heartbeat()

# Function to check ground station status
def check_ground_station_status():
    last_heartbeat = time.time()
    while True:
        msg = master.recv_match(blocking=True)
        if msg:
            if msg.get_type() == 'HEARTBEAT':
                last_heartbeat = time.time()
                print("Heartbeat received from Ground Station")
            elif msg.get_type() == 'STATUSTEXT':
                print(f"Status Text: {msg.text}")
            # Check for timeout
            if time.time() - last_heartbeat > 5:  # 5 seconds without a heartbeat
                print("Warning: Lost connection to Ground Station")
                break

# Function to retrieve the current mission
def get_mission():
    master.mav.mission_request_list_send(master.target_system, master.target_component)
    mission_items = []
    while True:
        msg = master.recv_match(type=['MISSION_ITEM', 'MISSION_ACK'], blocking=True)
        if msg is None:
            continue
        if msg.get_type() == 'MISSION_ITEM':
            mission_items.append(msg)
        elif msg.get_type() == 'MISSION_ACK':
            if msg.type == mavutil.mavlink.MAV_MISSION_ACCEPTED:
                print("Mission retrieved successfully")
                break
    return mission_items

# Function to retrieve telemetry data
def get_telemetry_data():
     while True:
        msg = master.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
        if msg:
            print(f"Latitude: {msg.lat / 1e7}, Longitude: {msg.lon / 1e7}, Altitude: {msg.alt / 1000} meters")
            velocity_msg = master.recv_match(type='VFR_HUD', blocking=True)
            if velocity_msg:
                print(f"Groundspeed: {velocity_msg.groundspeed} m/s, Airspeed: {velocity_msg.airspeed} m/s, Heading: {velocity_msg.heading} degrees")
            battery_msg = master.recv_match(type='BATTERY_STATUS', blocking=True)
            if battery_msg:
                print(f"Battery: {battery_msg.voltages[0]} mV, Current: {battery_msg.current_battery} mA, Remaining: {battery_msg.battery_remaining}%")
            gps_msg = master.recv_match(type='GPS_RAW_INT', blocking=True)
            if gps_msg:
                print(f"GPS Fix: {gps_msg.fix_type}, Satellites Visible: {gps_msg.satellites_visible}")
            radio_msg = master.recv_match(type='RADIO_STATUS', blocking=True)
            if radio_msg:
                print(f"RSSI: {radio_msg.rssi}, RemRSSI: {radio_msg.remrssi}")
            break


# Function to arm the drone
def arm_drone():
    master.arducopter_arm()
    master.motors_armed_wait()
    print("Drone armed")

# Function to disarm the drone
def disarm_drone():
    master.arducopter_disarm()
    master.motors_disarmed_wait()
    print("Drone disarmed")

# Function to start the mission
def start_mission():
    master.mav.set_mode_send(
        master.target_system,
        mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
        mavutil.mavlink.MAV_MODE_AUTO_MISSION
    )
    while True:
        ack_msg = master.recv_match(type='COMMAND_ACK', blocking=True)
        if ack_msg and ack_msg.command == mavutil.mavlink.MAV_CMD_DO_SET_MODE:
            print("Mission started")
            break
            
# Function to pause the mission
def pause_mission():
    master.mav.command_long_send(
        master.target_system, master.target_component,
        mavutil.mavlink.MAV_CMD_DO_PAUSE_CONTINUE, 0,
        0, 0, 0, 0, 0, 0, 0
    )
    print("Mission paused")
    


# Function to end the mission
def end_mission():
    master.mav.command_long_send(
        master.target_system, master.target_component,
        mavutil.mavlink.MAV_CMD_MISSION_END, 0,
        0, 0, 0, 0, 0, 0, 0
    )
    print("Mission ended")

			

