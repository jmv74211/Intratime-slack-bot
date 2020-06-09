from datetime import datetime


def get_current_date_time():

  now = datetime.now()
  date_time = "{} {}".format(now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S"))

  return date_time
