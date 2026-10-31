import statistics


def get_average(values):
    return round(statistics.mean(values), 2)


def get_min(values):
    return min(values)


def get_max(values):
    return max(values)


def get_median(values):
    return round(statistics.median(values), 2)


def detect_jumps(values, timestamps, threshold):
    return [timestamps[i] for i in range(1, len(values))
            if abs(values[i] - values[i - 1]) > threshold]


def print_table(name, readings):
    print(f'\n{name}:')
    print(f'{"Timestamp":<20} | Value')
    print('-' * 34)
    for time, value in readings.items():
        print(f'{time:<20} | {value}')
