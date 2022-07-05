from datetime import time

date_time_str = '01:55:19'
x = date_time_str.split(":")

date_time_obj = time(int(x[0]),int(x[1]))



print ("The type of the date is now",  x)
print ("The date is", date_time_obj.strftime('%H:%M'))