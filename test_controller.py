from src.presentation_controller import PresentationController
import time


controller = PresentationController(total_slides=12, cooldown=1.0)

print("Starting controller test...")
print("Current:", controller.get_status())

print("\nTesting NEXT...")
controller.next_slide()
print("Current:", controller.get_status())

time.sleep(1.1)

print("\nTesting NEXT again...")
controller.next_slide()
print("Current:", controller.get_status())

time.sleep(1.1)

print("\nTesting PREVIOUS...")
controller.previous_slide()
print("Current:", controller.get_status())

print("\nTest complete.")