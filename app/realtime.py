import os
import time
from collections import defaultdict, deque
from datetime import datetime, timedelta

file_path = "/data/payments.csv"
last_position = 0

# Store recent timestamps per user
recent_payments = defaultdict(deque)

# Store recent amounts per user
recent_amounts = defaultdict(deque)

print("Realtime monitor started", flush=True)

while not os.path.exists(file_path):
    time.sleep(1)

while True:
    with open(file_path, "r") as file:
        file.seek(last_position)
        lines = file.readlines()
        last_position = file.tell()

    for line in lines:
        if line.startswith("timestamp") or not line.strip():
            continue

        timestamp, user, amount = line.strip().split(",")
        amount = int(amount)
        now = datetime.fromisoformat(timestamp)

        print("Realtime received:", user, amount, flush=True)

        # Rule 1: Payments over 3000
        if amount > 3000:
            print(
                f"🚨 ALERT: Large payment detected: {user} paid {amount}",
                flush=True
            )

        # Rule 2: Multiple payments within 10 seconds

        # Add current payment timestamp
        recent_payments[user].append(now)

        # Remove timestamps older than 10 seconds
        while (
            recent_payments[user]
            and recent_payments[user][0] < now - timedelta(seconds=10)
        ):
            recent_payments[user].popleft()

        if len(recent_payments[user]) >= 3:
            print(
                f"🚨 ALERT: Many payments in short time: {user}",
                flush=True
            )

        # Rule 3: Repeated payment amounts

        recent_amounts[user].append(amount)

        # Keep only the last 5 amounts
        if len(recent_amounts[user]) > 5:
            recent_amounts[user].popleft()

        if recent_amounts[user].count(amount) >= 3:
            print(
                f"🚨 ALERT: Repeated payment amount: {user} amount={amount}",
                flush=True
            )
