import datetime


def log_event(db, command_name, user_id, username, start_time, end_time,
              status, message):
    """Logs command execution details to the MongoDB logs collection."""
    log_entry = {
        "timestamp": datetime.datetime.now(),
        "command_name": command_name,
        "user_id": user_id,
        "username": username,
        "start_time": start_time,
        "end_time": end_time,
        "status": status,
        "message": message
    }
    print(log_entry)
    # db.logs.insert_one(log_entry)
