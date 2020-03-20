def load_aws(filename):

    import numpy as np
    import pandas as pd

    pd.options.mode.chained_assignment = None  # default = 'warn'

    
    df = pd.read_csv(filename,
                        sep = ",",
                        header = 0,
                        engine = 'python')

    df.columns = ['location','date','temperature','precipitation','precipitation?','wind_direction','wind_speed','pressure','pressure2','humidity']

    df['month'] = df.date.str.split('-| |:').str[1]
    df['day'] = df.date.str.split('-| |:').str[2]
    df['hour'] = df.date.str.split('-| |:').str[3]
    df['minute'] = df.date.str.split('-| |:').str[4]

    df = df.drop(columns = 'date')

    df.month = df.month.astype(int)
    df.day = df.day.astype(int)
    df.hour = df.hour.astype(int)
    df.minute = df.minute.astype(int)

    df.month[len(df)-1] = df.month[len(df)-2]
    df.day[len(df)-1] = df.day[len(df)-2]
    df.hour[len(df)-1] = 24

    for i in range(len(df.minute)):
        df.minute[i] = 1440 * (df.day[i]-1) + 60 * (df.hour[i]) + df.minute[i]

    df = df.drop(columns = 'month')
    df = df.drop(columns = 'day')
    df = df.drop(columns = 'hour')

    deg = np.array(df.wind_direction)
    v = np.array(df.wind_speed)
    minute = np.array(df.minute)

    return(deg, v, minute)


def load_asos(filename):

    import numpy as np
    import pandas as pd

    pd.options.mode.chained_assignment = None  # default = 'warn'

    
    df = pd.read_csv(filename,
                        sep = ",",
                        header = 0,
                        engine = 'python')

    df.columns = ['location','date','temperature','precipitation','wind_direction','wind_speed','pressure','pressure2','humidity']

    df['month'] = df.date.str.split('-| |:').str[1]
    df['day'] = df.date.str.split('-| |:').str[2]
    df['hour'] = df.date.str.split('-| |:').str[3]
    df['minute'] = df.date.str.split('-| |:').str[4]

    df = df.drop(columns = 'date')

    df.month = df.month.astype(int)
    df.day = df.day.astype(int)
    df.hour = df.hour.astype(int)
    df.minute = df.minute.astype(int)

    df.month[len(df)-1] = df.month[len(df)-2]
    df.day[len(df)-1] = df.day[len(df)-2]
    df.hour[len(df)-1] = 24

    for i in range(len(df.minute)):
        df.minute[i] = 1440 * (df.day[i]-1) + 60 * (df.hour[i]) + df.minute[i]

    df = df.drop(columns = 'month')
    df = df.drop(columns = 'day')
    df = df.drop(columns = 'hour')

    deg = np.array(df.wind_direction)
    v = np.array(df.wind_speed)
    minute = np.array(df.minute)

    return(deg, v, minute)


def missing(deg, v, minute):

    import numpy as np
    import math

    for i in range(len(minute)-1):
        delta = minute[i+1] - minute[i]

        if delta != 1:
            for k in range(delta-1):
                minute = np.insert(minute, i+1+k, minute[i+k]+1)
                vwe_mean = - v[i+k] * math.sin(math.radians(deg[i+k])) - v[i+1+k] * math.sin(math.radians(deg[i+1+k]))
                vwe_mean = vwe_mean * 0.5
                vsn_mean = - v[i+k] * math.cos(math.radians(deg[i+k])) - v[i+1+k] * math.cos(math.radians(deg[i+1+k]))
                vsn_mean = vsn_mean * 0.5
                v_mean = math.sqrt(vwe_mean ** 2 + vsn_mean ** 2)
                
                if vsn_mean < 0:
                    deg_mean = math.atan(vwe_mean/vsn_mean)
                    deg_mean = math.degrees(deg_mean)
                    if deg_mean < 0:
                        deg_mean = deg_mean + 360

                elif vsn_mean > 0:
                    deg_mean = math.atan(vwe_mean/vsn_mean)
                    deg_mean = math.degrees(deg_mean) + 180

                elif vsn_mean == 0:
                    if vwe_mean == 0:
                        deg_mean = 0
                    elif vwe_mean > 0:
                        deg_mean = 270
                    elif vwe_mean < 0:
                        deg_mean = 90
            
                v = np.insert(v, i+1+k, v_mean)
                deg = np.insert(deg, i+1+k, deg_mean)
    
    return(deg, v, minute)


def mean_10(deg, v, minute):

    import numpy as np
    import math

    num = len(v) * 0.1
    num = int(num)
    vwe_10 = np.zeros(num)
    vsn_10 = np.zeros(num)
    v_10 = np.zeros(num)
    deg_10 = np.zeros(num)

    for i in range(num):
        for j in range(9):
            vwe_10[i] = vwe_10[i] - v[10*i+j+1] * math.sin(math.radians(deg[10*i+j+1]))
            vsn_10[i] = vsn_10[i] - v[10*i+j+1] * math.cos(math.radians(deg[10*i+j+1]))

        vwe_10[i] = vwe_10[i] - v[10*i] * math.sin(math.radians(deg[10*i]))
        vwe_10[i] = vwe_10[i] * 0.1
        vsn_10[i] = vsn_10[i] - v[10*i] * math.cos(math.radians(deg[10*i]))
        vsn_10[i] = vsn_10[i] * 0.1
        v_10[i] = math.sqrt(vwe_10[i] ** 2 + vsn_10[i] ** 2)
        
        if vsn_10[i] < 0:
            deg_10[i] = math.atan(vwe_10[i]/vsn_10[i])
            deg_10[i] = math.degrees(deg_10[i])
            if deg_10[i] < 0:
                deg_10[i] = deg_10[i] + 360

        elif vsn_10[i] > 0:
            deg_10[i] = math.atan(vwe_10[i]/vsn_10[i])
            deg_10[i] = math.degrees(deg_10[i]) + 180

        elif vsn_10[i] == 0:
            if vwe_10[i] == 0:
                deg_10[i] = 0
            elif vwe_10[i] > 0:
                deg_10[i] = 270
            elif vwe_10[i] < 0:
                deg_10[i] = 90
    
    return(deg_10, v_10)
