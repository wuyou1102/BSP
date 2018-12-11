C2_DailyBuild = "/home/bspserver/sda/C2_DailyBuild/"
C2_WeeklyBuild = "/home/bspserver/sda/C2_WeeklyBuild/"
C2_TriggerBuild = "/home/bspserver/sda/C2_TriggerBuild/"
B2_9A_DailyBuild = "/home/bspserver/sda/B2/B2_9A_DailyBuild/"
B2_9B_DailyBuild = "/home/bspserver/sda/B2/B2_9B_DailyBuild/"

__switch = {
    "c2daily": C2_DailyBuild,
    "c2weekly": C2_WeeklyBuild,
    "c2trigger": C2_TriggerBuild,
    "b29adaily": B2_9A_DailyBuild,
    "b29bdaily": B2_9B_DailyBuild,
}


def get_path(_type):
    return __switch.get(_type.lower(), C2_DailyBuild)


if __name__ == '__main__':
    print get_path('trigger')
