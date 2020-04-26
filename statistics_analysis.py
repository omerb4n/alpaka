import csv
import json
import os
from argparse import ArgumentParser
from collections import defaultdict
from pathlib import Path

from matplotlib import pyplot


def main(raw_results_file_paths, analyzed_data_csv_path, result_charts_dir):
    correct_distance_counts_per_parameter = calc_correct_distance_counts_per_parameter(raw_results_file_paths)
    all_distance_counts_per_parameter = calc_all_distance_counts_per_parameter(raw_results_file_paths)

    if analyzed_data_csv_path is not None:
        write_csv(correct_distance_counts_per_parameter, analyzed_data_csv_path)
    if result_charts_dir is not None:
        Path(result_charts_dir).mkdir(parents=True, exist_ok=True)
        for param_name, correct_distance_counts in correct_distance_counts_per_parameter.items():
            plot_graph_from_dict(correct_distance_counts, f'{param_name}_correct_distances', result_charts_dir)
        for param_name, all_distance_counts in all_distance_counts_per_parameter.items():
            plot_graph_from_dict(all_distance_counts, f'{param_name}_all_distances', result_charts_dir)


def calc_correct_distance_counts_per_parameter(raw_results_file_paths):
    correct_distance_counts_per_parameter = defaultdict(lambda: defaultdict(int))
    for raw_results_path in raw_results_file_paths:
        with open(raw_results_path, 'r') as raw_results_file:
            raw_results = json.load(raw_results_file)
        for param_name, param_statistics in raw_results.items():
            for cls in param_statistics.values():
                correct_distance_counts_per_parameter[param_name][cls[1]] += 1
    return correct_distance_counts_per_parameter


def calc_all_distance_counts_per_parameter(raw_results_file_paths):
    distance_counts_per_parameter = defaultdict(lambda: defaultdict(int))
    for raw_results_path in raw_results_file_paths:
        with open(raw_results_path, 'r') as raw_results_file:
            raw_results = json.load(raw_results_file)
        for param_name, param_statistics in raw_results.items():
            for class_statistics in param_statistics.values():
                for distance, count in class_statistics[0].items():
                    distance_counts_per_parameter[param_name][distance] += count
    return distance_counts_per_parameter


def plot_graph_from_dict(dct, graph_name, results_dir):
    dct = dict(dct)
    dct.pop(None, None)
    dct = {int(distance): count for distance, count in dct.items()}
    sorted_dict_items = sorted(dct.items(), key=lambda item: item[0])
    distances, counts = zip(*sorted_dict_items)
    pyplot.clf()
    pyplot.plot(distances, counts)
    pyplot.title(graph_name)
    pyplot.savefig(os.path.join(results_dir, graph_name) + '.png')


def write_csv(data, file_path):
    with open(file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        for parameter_name, parameter_analysis in data.items():
            writer.writerow([parameter_name])
            writer.writerows(parameter_analysis.items())


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-c', '--csv-path', dest='analyzed_data_csv_path')
    parser.add_argument('-p', '--plotted-charts-dir', dest='result_charts_dir')
    parser.add_argument('raw_result_files', nargs='+')
    args = parser.parse_args()
    main(args.raw_result_files, args.analyzed_data_csv_path, args.result_charts_dir)
