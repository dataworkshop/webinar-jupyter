
def feature_engineering(data):
    data['year'] = data['datetime'].dt.year
    data['diff_year'] = data['year'] - 2010
    data['month'] = data['datetime'].dt.month
    data['day'] = data['datetime'].dt.day
    data['hour'] = data['datetime'].dt.hour
    data['minute'] = data['datetime'].dt.minute
    data['dayofweek'] = data['datetime'].dt.dayofweek
    data['weekofyear'] = data['datetime'].dt.weekofyear
    data['weekend'] = data.dayofweek.map(lambda x: int(x in [5,6]) )
    data['time_of_day'] = data['hour'].map(cat_hour)
    
    data['dayofyear'] = data['datetime'].dt.dayofyear
    data['day_'] = data[ ['year', 'dayofyear'] ].apply(lambda x: x['dayofyear'] + int(str(x['year'])[-1]) * 365  , axis=1)
    
    data['rush_hour'] = data['datetime'].apply(lambda i: min([np.fabs(9-i.hour), np.fabs(20-i.hour)]))
    data.loc[:,('rush_hour')] = data['datetime'].apply(lambda i: np.fabs(14-i.hour))
    data.loc[data['workingday'] != 0].loc[:,('rush_hour')] = 0
    
    data['holiday'] = data[['month', 'day', 'holiday', 'year']].apply(lambda x: (x['holiday'], 1)[x['year'] == 2012 and x['month'] == 10 and (x['day'] in [30])], axis = 1)
    data['holiday'] = data[['month', 'day', 'holiday']].apply(lambda x: (x['holiday'], 1)[x['month'] == 12 and (x['day'] in [24, 26, 31])], axis = 1)
    
    data['workingday'] = data[['month', 'day', 'workingday']].apply(lambda x: (x['workingday'], 0)[x['month'] == 12 and x['day'] in [24, 31]], axis = 1)
    data['peak'] = data[['hour', 'workingday']].apply(lambda x: (0, 1)[(x['workingday'] == 1 and  ( x['hour'] == 8 or 17 <= x['hour'] <= 18 or 12 <= x['hour'] <= 12)) or (x['workingday'] == 0 and  10 <= x['hour'] <= 19)], axis = 1)
    data['sticky'] = data[['humidity', 'workingday']].apply(lambda x: (0, 1)[x['workingday'] == 1 and x['humidity'] >= 60], axis = 1)

    return data

print("done")