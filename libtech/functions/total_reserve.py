# import datetime
# from libtech.models import Category


# def check_duration(self):
#     a, b, c, d = self.start_time.hour, self.start_time.minute, self.start_time.second, self.start_time.microsecond
#     w, x, y, z = self.end_time.hour, self.end_time.minute, self.end_time.second, self.end_time.microsecond
#     delt = (w-a)*60 + (x-b) + (y-c)/60. + (z-d)/60000000.
#     if delt < 0:
#         delt += 1440

#     hh, rem = divmod(delt, 60)
#     hh = int(hh)
#     mm = int(rem)
#     rem = (rem - mm)*60
#     ss = int(rem)
#     ms = (rem - ss)*1000000
#     ms = int(ms)

#     self.duration = '%sh %smn '
#     return self.duration % (hh, mm,)
