import functools
import time
from db_logging import log_event
import datetime


def log_command_execution(db):
    """Decorator to log command execution details."""

    def decorator(func):

        @functools.wraps(func)
        async def wrapper(ctx, *args, **kwargs):
            start_time = time.time()
            user_id = ctx.author.id
            username = ctx.author.name
            command_name = func.__name__

            try:
                # Execute the command
                await func(ctx, *args, **kwargs)
                status = 'success'
                message = 'Command executed successfully.'
            except Exception as e:
                # Log the error and re-raise
                status = 'error'
                message = str(e)
                raise

            end_time = time.time()
            # Log command execution details
            log_event(db=db,
                      command_name=command_name,
                      user_id=user_id,
                      username=username,
                      start_time=datetime.datetime.fromtimestamp(start_time),
                      end_time=datetime.datetime.fromtimestamp(end_time),
                      status=status,
                      message=message)

        return wrapper

    return decorator
