from Server.B2 import config as B2Config

C2_DailyBuild = "/home/bspserver/sda/C2_DailyBuild/"
C2_WeeklyBuild = "/home/bspserver/sda/C2_WeeklyBuild/"
C2_TriggerBuild = "/home/bspserver/sda/C2_TriggerBuild/"

B2_DailyBuild_9A = B2Config.PATH_DAILY_9A
B2_DailyBuild_9B = B2Config.PATH_DAILY_9B
B2_WeeklyBuild_9A = B2Config.PATH_WEEKLY_9A
B2_WeeklyBuild_9B = B2Config.PATH_WEEKLY_9B

__switch = {
    "C2Daily": C2_DailyBuild,
    "C2Weekly": C2_WeeklyBuild,
    "C2Trigger": C2_TriggerBuild,
    "B29ADaily": B2_DailyBuild_9A,
    "B29BDaily": B2_DailyBuild_9B,
    "B29AWeekly": B2_WeeklyBuild_9A,
    "B29BWeekly": B2_WeeklyBuild_9B,
}

switch = dict((k.lower(), v) for k, v in __switch.items())


def get_path(_type):
    return switch.get(_type.lower(), C2_DailyBuild)


if __name__ == '__main__':
    print get_path('trigger')
