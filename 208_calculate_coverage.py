import argparse
import subprocess
from pathlib import Path
from tqdm import tqdm
import logging
import time
import os

# Setup logging with unique filename
log_filename = f'bam_coverage_analysis_{time.strftime("%Y%m%d_%H%M%S")}_{os.getpid()}.log'
logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

def coverage_analysis(input_dir, output_dir):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    bam_files = list(input_dir.glob('*_sort_filter.bam'))
    for bam_file in tqdm(bam_files, desc='Calculating coverage information'):
        output_file = output_dir / (bam_file.stem + '_coverage_info.txt.gz')
        cmd = ['msamtools', 'coverage', '-z', '--summary', '-o', str(output_file), str(bam_file)]
        subprocess.run(cmd, check=True)
        logging.info(f'Generated coverage information for {bam_file} into {output_file}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calculate coverage information for BAM files using msamtools.',
                                     epilog='Example: python script.py -i /path/to/filtered_bam_files -o /path/to/coverage_info')
    parser.add_argument('-i', '--input', required=True, help='Input directory containing filtered BAM files')
    parser.add_argument('-o', '--output', required=True, help='Output directory for coverage information files')
    args = parser.parse_args()

    try:
        coverage_analysis(args.input, args.output)
        logging.info("Coverage analysis completed successfully.")
    except Exception as e:
        logging.error(f"Error during coverage analysis: {e}")

