import csv
import json
from argparse import ArgumentParser
from collections import defaultdict


def main(raw_results_file_paths, analyzed_data_csv_path):
    correct_distance_counts_per_parameter = defaultdict(lambda: defaultdict(int))
    for raw_results_path in raw_results_file_paths:
        with open(raw_results_path, 'r') as raw_results_file:
            raw_results = json.load(raw_results_file)
        for param_name, param_statistics in raw_results.items():
            for cls in param_statistics.values():
                correct_distance_counts_per_parameter[param_name][cls[1]] += 1
    write_csv(correct_distance_counts_per_parameter, analyzed_data_csv_path)


def write_csv(data, file_path):
    with open(file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        for parameter_name, parameter_analysis in data.items():
            writer.writerow([parameter_name])
            writer.writerows(parameter_analysis.items())


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('analyzed_data_csv_path')
    parser.add_argument('raw_result_files', nargs='+')
    args = parser.parse_args()
    main(args.raw_result_files, args.analyzed_data_csv_path)
