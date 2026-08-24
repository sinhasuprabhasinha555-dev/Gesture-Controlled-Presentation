class SlideTracker:

    def __init__(self, total_slides):
        self.total_slides = total_slides
        self.current_slide = 1

    def next_slide(self):
        if self.current_slide < self.total_slides:
            self.current_slide += 1

    def previous_slide(self):
        if self.current_slide > 1:
            self.current_slide -= 1

    def get_status(self):
        return f"Slide {self.current_slide} / {self.total_slides}"