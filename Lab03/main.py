import csv
import json
import configparser
from pathlib import Path
import stats_utils as stats

FOLDER = Path(__file__).resolve().parent
THRESHOLDS = {'temperature': 7, 'humidity': 20, 'pressure': 5000}
FUNCTIONS = {'average': stats.get_average, 'min': stats.get_min,
             'max': stats.get_max, 'median': stats.get_median}


def main():
    try:
        data = {name: {} for name in THRESHOLDS}
        with open(FOLDER / 'data.csv', encoding='utf-8-sig', newline='') as file:
            reader = csv.DictReader(file)
            if not reader.fieldnames or not set(('timestamp', *THRESHOLDS)).issubset(reader.fieldnames):
                raise ValueError('У CSV відсутні потрібні стовпці')
            for row in reader:
                time = row['timestamp']
                for name in data:
                    data[name][time] = float(row[name])
        if not data['temperature']:
            raise ValueError('Файл data.csv порожній')

        config = configparser.ConfigParser()
        with open(FOLDER / 'config.ini', encoding='utf-8') as file:
            config.read_file(file)

        results = {}
        for name in config.sections():
            if name not in data:
                raise ValueError(f'Невідомий показник: {name}')
            readings = data[name]
            stats.print_table(name, readings)
            values = list(readings.values())
            times = list(readings.keys())
            results[name] = {}
            for operation in config[name]['stats'].split(','):
                operation = operation.strip()
                if operation == 'jumps':
                    result = stats.detect_jumps(values, times, THRESHOLDS[name])
                elif operation in FUNCTIONS:
                    result = FUNCTIONS[operation](values)
                else:
                    raise ValueError(f'Невідома характеристика: {operation}')
                results[name][operation] = result
                print(f'  {operation}: {result}')

        with open(FOLDER / 'results.json', 'w', encoding='utf-8') as file:
            json.dump(results, file, ensure_ascii=False, indent=4)
        print('\nРезультати збережено в results.json')
    except (OSError, ValueError, KeyError, configparser.Error) as error:
        print('Помилка:', error)


if __name__ == '__main__':
    main()
