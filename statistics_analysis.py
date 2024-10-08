import csv
import json
import os
import statistics
from argparse import ArgumentParser
from collections import defaultdict
from math import prod
from pathlib import Path

from matplotlib import pyplot


def main(raw_results_file_paths, analyzed_data_csv_path, result_charts_dir, calc_mean, calc_optimal_weights):
    correct_distance_counts_per_parameter = calc_correct_distance_counts_per_parameter(raw_results_file_paths)
    all_distance_counts_per_parameter = calc_all_distance_counts_per_parameter(raw_results_file_paths)
    incorrect_distance_counts_per_parameter = calc_incorrect_distance_counts_per_parameter(correct_distance_counts_per_parameter, all_distance_counts_per_parameter)

    if analyzed_data_csv_path is not None:
        write_csv(correct_distance_counts_per_parameter, analyzed_data_csv_path)
    if result_charts_dir is not None:
        Path(result_charts_dir).mkdir(parents=True, exist_ok=True)
        for param_name, correct_distance_counts in correct_distance_counts_per_parameter.items():
            plot_graph_from_dict(correct_distance_counts, f'{param_name}_correct_distances', result_charts_dir)
        for param_name, all_distance_counts in all_distance_counts_per_parameter.items():
            plot_graph_from_dict(all_distance_counts, f'{param_name}_all_distances', result_charts_dir)
        for param_name, incorrect_distance_counts in incorrect_distance_counts_per_parameter.items():
            plot_graph_from_dict(incorrect_distance_counts, f'{param_name}_incorrect_distances', result_charts_dir)
    if calc_mean or calc_optimal_weights:
        correct_distances_mean_per_parameter = calc_mean_per_parameter(correct_distance_counts_per_parameter)
        all_distances_mean_per_parameter = calc_mean_per_parameter(all_distance_counts_per_parameter)
        if calc_mean:
            incorrect_distances_mean_per_parameter = calc_mean_per_parameter(incorrect_distance_counts_per_parameter)
            mean_output_lines = []
            for param_name, mean in correct_distances_mean_per_parameter.items():
                mean_output_lines.append(f'{param_name}_correct: {mean}')
            for param_name, mean in all_distances_mean_per_parameter.items():
                mean_output_lines.append(f'{param_name}_all: {mean}')
            for param_name, mean in incorrect_distances_mean_per_parameter.items():
                mean_output_lines.append(f'{param_name}_incorrect: {mean}')
            for line in sorted(mean_output_lines):
                print(line)
        if calc_optimal_weights:
            optimal_weights = calc_optimal_weight_per_parameter(all_distances_mean_per_parameter, correct_distances_mean_per_parameter)
            print('\nOptimal Weights:')
            for param_name, weight in optimal_weights.items():
                print(f'{param_name}: {weight}')


def calc_optimal_weight_per_parameter(all_distances_mean_per_parameter, correct_distances_mean_per_parameter):
    optimal_weights = dict()
    equalizer_constant = prod(all_distances_mean_per_parameter.values())
    for param_name, correct_distances_mean in correct_distances_mean_per_parameter.items():
        optimal_weights[param_name] = equalizer_constant / float(correct_distances_mean)
    normalizer_constant = 10.0 / statistics.mean(optimal_weights.values())
    return {
        param_name: weight * normalizer_constant
        for param_name, weight in optimal_weights.items()
    }


def calc_mean_per_parameter(histogram_per_parameter):
    return {
        param_name: calc_mean_from_histogram(histogram)
        for param_name, histogram in histogram_per_parameter.items()
    }


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


def calc_incorrect_distance_counts_per_parameter(correct_distance_counts_per_parameter, all_distance_counts_per_parameter):
    incorrect_distance_counts_per_parameter = dict()
    for param_name, all_distance_counts in all_distance_counts_per_parameter.items():
        incorrect_distance_counts = dict(all_distance_counts)
        correct_distance_counts = correct_distance_counts_per_parameter.get(param_name)
        if correct_distance_counts is not None:
            for distance in incorrect_distance_counts.keys():
                incorrect_distance_counts[distance] -= correct_distance_counts.get(int(distance), 0)
        incorrect_distance_counts_per_parameter[param_name] = incorrect_distance_counts
    return incorrect_distance_counts_per_parameter


def calc_mean_from_histogram(histogram):
    weighted_sum = 0
    total_count = 0
    for value, count in histogram.items():
        if value is None:
            continue
        weighted_sum += int(value) * count
        total_count += count
    return weighted_sum/float(total_count)


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
    parser.add_argument('-m', '--calc-mean', dest='calc_mean', action='store_true')
    parser.add_argument('-w', '--calc-optimal-weights', dest='calc_optimal_weights', action='store_true')
    parser.add_argument('raw_result_files', nargs='+')
    args = parser.parse_args()
    main(args.raw_result_files, args.analyzed_data_csv_path, args.result_charts_dir, args.calc_mean, args.calc_optimal_weights)
