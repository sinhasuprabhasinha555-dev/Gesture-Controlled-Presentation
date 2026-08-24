from src.slide_tracker import SlideTracker


tracker = SlideTracker(12)

print("Initial:", tracker.get_status())

tracker.next_slide()
print("After next:", tracker.get_status())

tracker.next_slide()
print("After next:", tracker.get_status())

tracker.previous_slide()
print("After previous:", tracker.get_status())