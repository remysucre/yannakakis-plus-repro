#!/usr/bin/env python3
"""
Extract final timings from IMDB benchmark timing results.

The file structure is:
- Multiple lines of intermediate timing results (Run Time (s): ...)
- A line starting with 'v' (query variables like v43,v44)
- A line with query results
- A final timing line with the total execution time
- More intermediate timings for the next query
"""

import re
import sys

def extract_final_timings(filename):
    """Extract final timing results from the timing file."""
    final_timings = []
    
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Look for variable declaration lines (e.g., v43,v44)
        if re.match(r'^v\d+', line):
            # Skip the query result line
            i += 1
            if i < len(lines):
                i += 1
                
                # The next line should be the final timing
                if i < len(lines) and lines[i].startswith('Run Time (s):'):
                    timing_line = lines[i].strip()
                    
                    # Extract the real time
                    real_match = re.search(r'real (\d+\.\d+)', timing_line)
                    if real_match:
                        real_time = float(real_match.group(1))
                        final_timings.append(real_time)
        
        i += 1
    
    return final_timings

def main():
    filename = 'time.txt'
    
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    
    try:
        timings = extract_final_timings(filename)
        
        for timing in timings:
            print(timing)
        
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()