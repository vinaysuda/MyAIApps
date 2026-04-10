# tasks.py
from celery import Celery
import time

# Configure Celery to use Redis as the broker and result backend
app = Celery(
    "my_app", broker="redis://localhost:6379/0", backend="redis://localhost:6379/0"
)


@app.task
def long_running_task(name):
    print(f"Started processing for {name}...")
    time.sleep(5)  # Simulate a heavy task (e.g., image processing or email sending)
    print(f"Finished processing for {name}!")
    return f"Hello, {name}! Your task is complete."


# 1. Send the task to the Redis queue
print("Dispatching task...")
result = long_running_task.delay("Alice")

# 2. The script continues immediately without waiting 5 seconds
print(f"Task ID: {result.id}")

# 3. Optional: Wait and get the result (blocks until finished)
print("Waiting for result (this will take 5 seconds)...")
final_output = result.get(timeout=10)
print(f"Result from worker: {final_output}")
