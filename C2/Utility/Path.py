DailyBuild = "/home/bspserver/sda/C2_DailyBuild/"
WeeklyBuild = "/home/bspserver/sda/C2_WeeklyBuild/"
TriggerBuild = "/home/bspserver/sda/C2_TriggerBuild/"

__switch = {
    "daily": DailyBuild,
    "weekly": WeeklyBuild,
    "trigger": TriggerBuild,
}


def get_path(_type):
    return __switch.get(_type.lower(), DailyBuild)


if __name__ == '__main__':
    print get_path('trigger')
