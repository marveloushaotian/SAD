import pandas as pd
import argparse

# Define and parse command-line arguments
parser = argparse.ArgumentParser(description='Group and calculate defense statistics.')
parser.add_argument('-i', '--input', type=str, required=True, help='Path to input file')
parser.add_argument('-o', '--output', type=str, required=True, help='Path to output file')
args = parser.parse_args()

# Read the input file
input_file = args.input
df = pd.read_csv(input_file, sep='\t')

# Group and aggregate the data
grouped = df.groupby(['Contig_Group', 'Location_BAF', 'Sample']).agg({
    'Defense_Num': 'sum',
    'Contig_Length': 'sum'
}).reset_index()

# Calculate the final result
grouped['GCGB'] = grouped['Defense_Num'] * 1000000 / grouped['Contig_Length']

# Export the result
output_file = args.output
grouped.to_csv(output_file, sep='\t', index=False, columns=['Contig_Group', 'Location_BAF', 'Sample', 'Defense_Num', 'Contig_Length', 'GCGB'])

print(f"Results have been exported to {output_file}")

