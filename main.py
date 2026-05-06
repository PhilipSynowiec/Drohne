from drone import Drone
from time import sleep

if __name__ == "__main__":
    drone = Drone()
    drone.startup()
    sleep(5)
    drone.motors.motor_fl.set(1500)
    drone.motors.motor_fr.set(1500)
    drone.motors.motor_bl.set(1500)
    drone.motors.motor_br.set(1500)
    sleep(5)
    drone.motors.motor_fl.set(0)
    drone.motors.motor_fr.set(0)
    drone.motors.motor_bl.set(0)
    drone.motors.motor_br.set(0)
    print("Test abgeschlossen. Alle Motoren gestoppt.")
