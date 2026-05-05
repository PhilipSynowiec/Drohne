from drone import Drone
from time import sleep

if __name__ == "__main__":
    drone = Drone()
    drone.startup()
    sleep(5)
    drone.escs.set_all(1500)  # Testsignal an alle ESCs senden
    sleep(5)
    drone.escs.set_all(800)  # Alle ESCs auf Minimum setzen
    sleep(5)