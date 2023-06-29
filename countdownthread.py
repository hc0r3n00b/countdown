import datetime
import time
import threading

class CountdownThread(threading.Thread):
    def __init__(self, name, target_datetime):
        super().__init__()
        self.name = name
        self.target_datetime = target_datetime
        self._stop_event = threading.Event()

    def run(self):
        while not self._stop_event.is_set():
            # Calculate the time difference between now and the target datetime
            current_datetime = datetime.datetime.now()
            time_difference = self.target_datetime - current_datetime

            # Check if the target datetime has been reached
            if time_difference.total_seconds() <= 0:
                print(f"Countdown '{self.name}' complete!")
                break

            # Extract days, hours, minutes, and seconds from the time difference
            days = time_difference.days
            hours, remainder = divmod(time_difference.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)

            # Create the countdown string
            countdown_str = ""
            if days > 0:
                countdown_str += f"{days} day{'s' if days > 1 else ''}, "
            if hours > 0:
                countdown_str += f"{hours} hour{'s' if hours > 1 else ''}, "
            if minutes > 0:
                countdown_str += f"{minutes} minute{'s' if minutes > 1 else ''}, "
            countdown_str += f"{seconds} second{'s' if seconds > 1 else ''}"

            # Create the filename based on the name argument
            filename = f"{self.name}.txt"

            # Update the text file with the name and countdown string
            with open(filename, "w") as file:
                file.write(f"Name: {self.name}\n")
                file.write(countdown_str)

            # Wait for one second before updating the countdown again
            time.sleep(1)

    def stop(self):
        self._stop_event.set()

def create_countdown():
    # Prompt for the target date and time
    target_date_str = input("Enter the target date (YYYY-MM-DD), or 'exit' to quit: ")
    if target_date_str.lower() == "exit":
        return

    target_time_str = input("Enter the target time (HH:MM:SS): ")

    # Convert the input strings to datetime objects
    target_datetime_str = target_date_str + " " + target_time_str
    target_datetime = datetime.datetime.strptime(target_datetime_str, "%Y-%m-%d %H:%M:%S")

    # Get the name for the countdown
    name = input("Enter the name for the countdown: ")

    # Create a new countdown thread
    countdown_thread = CountdownThread(name, target_datetime)

    # Start the countdown thread
    countdown_thread.start()

    return countdown_thread

countdown_threads = []

while True:
    countdown_thread = create_countdown()

    if countdown_thread:
        countdown_threads.append(countdown_thread)

    # Check if any countdowns have completed
    for thread in countdown_threads:
        if not thread.is_alive():
            countdown_threads.remove(thread)

    # Exit the loop if there are no active countdowns
    if not countdown_threads:
        print("All countdowns completed.")
        break

    time.sleep(1)
