from datetime import *


TODAY = date.today()

print(" --- Task 1 --- ")
print("Current date minus 6 days:", TODAY - timedelta(days=6))
print()


print(" --- Task 2 --- ")
print("Yesterday:", TODAY - timedelta(days=1))
print("Today:", TODAY)
print("Tomorrow:", TODAY + timedelta(days=1))
print()


print(" --- Task 3 --- ")
print("Today's datetime minus 666 microseconds:", datetime.now() - timedelta(microseconds=666))
print()


print(" --- Task 4 --- ")
print("Diff between two dates in seconds:", timedelta(seconds=808) - timedelta(seconds=404))