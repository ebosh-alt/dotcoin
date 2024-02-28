import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime

# months = mdates.MonthLocator()
# days = mdates.DayLocator()
# timeFmt = mdates.DateFormatter('%d-%m')
event = [datetime.datetime(2024, 2, 11), datetime.datetime(2024, 2, 12),
         datetime.datetime(2024, 2, 13), datetime.datetime(2024, 2, 14),
         datetime.datetime(2024, 2, 15), datetime.datetime(2024, 2, 16),
         datetime.datetime(2024, 2, 17), datetime.datetime(2024, 2, 18),
         datetime.datetime(2024, 2, 19), datetime.datetime(2024, 2, 20),
         datetime.datetime(2024, 2, 21), datetime.datetime(2024, 2, 22),
         datetime.datetime(2024, 2, 23), datetime.datetime(2024, 2, 24)]
# bw = 0.7
#
value = [2000, 2750, 5000, 9000, 3000, 6000, 1000,
         5000, 7000, 3000, 4000, 6000, 9000, 5000]
#
# fig, ax = plt.subplots()
# plt.title('Инфографика')
# plt.ylim(0, max(values) + min(values))
#
# for i in range(1, len(values)):
#     if values[i] >= values[i - 1]:
#         plt.bar(events[i], values[i], bw, color='g')
#     else:
#         plt.bar(events[i], values[i], bw, color='r')
#
# ax.xaxis.set_major_formatter(timeFmt)
# ax.xaxis.set_minor_locator(days)
# plt.savefig("output1", bbox_inches="tight",
#             pad_inches=0.7, transparent=False)
days = mdates.DayLocator()
time_fmt = mdates.DateFormatter('%d.%m')
bw = 0.7
fig, ax = plt.subplots()
plt.title('Инфографика')
# plt.ylim(1, max(value) + min(value))
plt.bar(event[0], value[0], bw, color='g')

for i in range(1, 14):
    print(i)
    if value[i] >= value[i - 1]:
        plt.bar(event[i], value[i], bw, color='g')
    else:
        plt.bar(event[i], value[i], bw, color='r')
ax.xaxis.set_major_formatter(time_fmt)
ax.xaxis.set_minor_locator(days)

plt.savefig("output", bbox_inches="tight",
            pad_inches=0.7, transparent=True)
