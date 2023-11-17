# msvsdk.py

import asyncio
from mavsdk import System

async def connect_drone():
    drone = System()
    await drone.connect(system_address="udp://:14540")
    return drone

async def get_drone_state(drone):
    async for state in drone.core.connection_state():
        return state

async def get_battery_status(drone):
    async for battery in drone.telemetry.battery():
        return battery

async def get_gps_info(drone):
    async for gps_info in drone.telemetry.position():
        return gps_info

async def get_flight_mode(drone):
    async for flight_mode in drone.telemetry.flight_mode():
        return flight_mode

async def get_home_position(drone):
    async for home in drone.telemetry.home():
        return home

async def get_in_air_status(drone):
    async for in_air in drone.telemetry.in_air():
        return in_air

async def get_health_status(drone):
    async for health in drone.telemetry.health():
        return health

async def get_velocity(drone):
    async for velocity in drone.telemetry.velocity_ned():
        return velocity

async def arm_drone(drone):
    print("Arming...")
    await drone.action.arm()

async def disarm_drone(drone):
    print("Disarming...")
    await drone.action.disarm()

async def takeoff_drone(drone):
    print("Taking off...")
    await drone.action.takeoff()

async def land_drone(drone):
    print("Landing...")
    await drone.action.land()

async def main():
    drone = await connect_drone()
    print("Drone connected")

    # Example usage
    state = await get_drone_state(drone)
    print(f"Drone State: {state}")

    battery = await get_battery_status(drone)
    print(f"Battery: {battery.remaining_percent * 100}%")

    gps_info = await get_gps_info(drone)
    print(f"GPS: {gps_info}")

    flight_mode = await get_flight_mode(drone)
    print(f"Flight Mode: {flight_mode}")

    home_position = await get_home_position(drone)
    print(f"Home Position: {home_position}")

    in_air = await get_in_air_status(drone)
    print(f"In Air: {in_air}")

    health = await get_health_status(drone)
    print(f"Health: {health}")

    velocity = await get_velocity(drone)
    print(f"Velocity: {velocity}")

    # Arm, takeoff, and land as an example
    await arm_drone(drone)
    await takeoff_drone(drone)
    await asyncio.sleep(10)  # Adjust as needed
    await land_drone(drone)
    await disarm_drone(drone)

if __name__ == "__main__":
    asyncio.run(main())

