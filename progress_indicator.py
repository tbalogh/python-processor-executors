import time


class ProgressIndicator:
    def __init__(self, name, work_unit_count):
        self.all_unit = work_unit_count
        self.name = name
        self.done_unit = 0
        self.percentage = 0
        self.start_time = 0

    def start(self):
        self.start_time = time.time()
        print("{} started with {} items.".format(self.name, self.all_unit))

    def calculate_remaining_time(self):
        velocity = self.calculate_velocity()
        return int((self.all_unit - self.done_unit) * velocity)

    def calculate_velocity(self):
        elapsed_time = time.time() - self.start_time
        return elapsed_time / (self.done_unit + 1)

    def next(self):
        current_percentage = int((self.done_unit / self.all_unit) * 100)
        if current_percentage > self.percentage:
            print("{}: {}% remaining time: {} seconds \t v: {}".format(self.name,
                                                                       str(current_percentage),
                                                                       self.calculate_remaining_time(),
                                                                       self.calculate_velocity()))
            self.percentage = current_percentage
        self.done_unit += 1

    def finish(self):
        print("{} finished.".format(self.name))
