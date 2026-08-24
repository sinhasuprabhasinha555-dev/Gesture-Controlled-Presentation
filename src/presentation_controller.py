import pyautogui
import time


class PresentationController:

    def __init__(self, cooldown=1.2):
        self.cooldown = cooldown
        self.last_action_time = 0

    def can_execute(self):
        current_time = time.time()

        if current_time - self.last_action_time >= self.cooldown:
            self.last_action_time = current_time
            return True

        return False

    def next_slide(self):
        if not self.can_execute():
            return False

        pyautogui.press("right")
        print("➡️ Next slide")

        return True

    def previous_slide(self):
        if not self.can_execute():
            return False

        pyautogui.press("left")
        print("⬅️ Previous slide")

        return True