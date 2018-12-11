from Server.B2 import config as B2Config

C2_DailyBuild = "/home/bspserver/sda/C2_DailyBuild/"
C2_WeeklyBuild = "/home/bspserver/sda/C2_WeeklyBuild/"
C2_TriggerBuild = "/home/bspserver/sda/C2_TriggerBuild/"

B2_DailyBuild_9A = B2Config.PATH_DAILY_9A
B2_DailyBuild_9B = B2Config.PATH_DAILY_9B
B2_WeeklyBuild_9A = B2Config.PATH_WEEKLY_9A
B2_WeeklyBuild_9B = B2Config.PATH_WEEKLY_9B

__switch = {
    "c2daily": C2_DailyBuild,
    "c2weekly": C2_WeeklyBuild,
    "c2trigger": C2_TriggerBuild,
    "b29adaily": B2_DailyBuild_9A,
    "b29bdaily": B2_DailyBuild_9B,
}


def get_path(_type):
    return __switch.get(_type.lower(), C2_DailyBuild)


if __name__ == '__main__':
    print get_path('trigger')
