from datetime import datetime, timezone
def generate_now_():
# Get the current time in UTC
    utc_now = datetime.now(timezone.utc)
    print("Logging Time:", utc_now)
    print("\n✅ Time retrieval complete!\n\n")
    time_key = utc_now.strftime("%Y%m%d_%H%M%S")
    return time_key