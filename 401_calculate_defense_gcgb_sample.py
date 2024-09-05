import pandas as pd
import argparse
from tqdm import tqdm

# Define and parse command-line arguments
parser = argparse.ArgumentParser(description='Group and calculate defense statistics.')
parser.add_argument('-i', '--input', type=str, required=True, help='Path to input CSV file')
parser.add_argument('-o', '--output', type=str, required=True, help='Path to output CSV file')
args = parser.parse_args()

# Read the input file
print(f"Reading input file: {args.input}")
df = pd.read_csv(args.input)

# Group and aggregate the data
print("Grouping and aggregating data...")
grouped = df.groupby(['Contig_Classification', 'Location', 'Sample']).agg({
    'Defense_Number': 'sum',
    'Contig_Length': 'sum'
}).reset_index()

# Calculate the final result
print("Calculating GCGB...")
grouped['GCGB'] = grouped['Defense_Number'] * 1000000 / grouped['Contig_Length']

# Export the result
print(f"Exporting results to: {args.output}")
grouped.to_csv(args.output, index=False, columns=['Contig_Classification', 'Location', 'Sample', 'Defense_Number', 'Contig_Length', 'GCGB'])

print(f"Results have been exported to {args.output}")

# Usage example
print("\nUsage example:")
print("python 401_calculate_defense_gcgb_sample.py -i input_data.csv -o output_results.csv")
print("\nDescription: This script reads a CSV file containing defense system data, groups it by Contig_Classification, Location, and Sample, ")
print("calculates the sum of Defense_Number and Contig_Length, and computes the GCGB (Gene Count per Gigabase) for each group.")
print("The results are then saved to a new CSV file.")
