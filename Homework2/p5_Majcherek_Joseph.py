"""Problem 5: Weather Station Analyzer.

Analyzes temperature observation logs, filters malformed entries and extreme temperature
outliers, generates statistics, and includes unittest coverage.
"""

import datetime
import os
import sys
import tempfile
import unittest
from collections import defaultdict
from typing import Dict, List, Tuple

def read_observations(
    filename: str,
) -> Tuple[
    Dict[str, List[Tuple[datetime.datetime, float]]], List[Tuple[int, str]]
]:
    """Parse weather observations file, validating temperature bounds and date consistency.
    
    Args:
        filename (str): Path to the observations CSV file.
        
    Returns:
        Tuple[Dict[str, List[Tuple[datetime.datetime, float]]], List[Tuple[int, str]]]:
            A tuple containing (observations mapping, list of error tuples).
            
    Raises:
        Exception: Re-raises any caught I/O exceptions after printing a user-friendly error.
    """
    observations = defaultdict(list)
    errors: List[Tuple[int, str]] = []
    seen_keys = set()
    date_format = "%I:%M:%S %p %m/%d/%Y"

    try:
        with open(filename, "r", encoding="utf-8") as infile:
            for line_num, line in enumerate(infile, start=1):
                line_str = line.strip()

                # Skip blank lines
                if not line_str:
                    continue

                parts = [part.strip() for part in line_str.split(",")]
                if len(parts) != 3:
                    errors.append(
                        (
                            line_num,
                            f"Malformed line: expected 3 comma-separated fields, got {len(parts)}",
                        )  
                    )
                    continue
                station, date_str, temp_str = parts

                if not station:
                    errors.append((line_num, "Empty station name"))
                    continue

                # Datetime parsing
                try:
                    dt_obj = datetime.datetime.strptime(date_str, date_format)
                except ValueError:
                    errors.append(
                        (
                            line_num,
                            f"Invalid date/time format: '{date_str}' (expected '{date_format}')",
                        )
                    )
                    continue

                # Temperature bounds check
                try:
                    temp = float(temp_str)
                    if not (-100.0 <= temp <= 150.0):
                        errors.append(
                            (
                                line_num,
                                f"Temperature {temp} out of range [-100.0, 150.0]",
                            )
                        )
                        continue
                except ValueError:
                    errors.append(
                        (
                            line_num,
                            f"Non-numeric temperature value: '{temp_str}'",
                        )
                    )
                    continue

                # Check for duplicate station and datetime combinations
                combo_key = (station, dt_obj)
                if combo_key in seen_keys:
                    errors.append(
                        (
                            line_num,
                            f"Duplicate observation for station '{station}' at {date_str}",
                        )
                    )
                    continue
                seen_keys.add(combo_key)
                observations[station].append((dt_obj, temp))


        # Sort each station's observations chronologically by datetime
        for station in observations:
            observations[station].sort(key=lambda item: item[0])

        return dict(observations), errors

    except Exception as err:
        print(
            f"[ERROR] Could not read observation log file '{filename}' : {err}"
        )
        raise

def station_statistics(
    observations: Dict[str, List[Tuple[datetime.datetime, float]]],
) -> Dict[str, Tuple[float, float, float]]:
    """Compute (min, max, mean) temperatures per weather station.
    
    Args:
        observations (Dict): Maps station name -> sorted list of (datetime, temperature) tuples.
        
    Returns:
        Dict[str, Tuple[float, float, float]]: Maps station name -> (min, max, mean) temperatures.
    """
    stats = {}
    for st, obs_list in observations.items():
        if not obs_list:
            continue
        temps = [temp for _, temp in obs_list]
        min_t = min(temps)
        max_t = max(temps)
        mean_t = sum(temps) / len(temps)
        stats[st] = (min_t, max_t, mean_t)
    return stats

def station_outliers(
    observations: Dict[str, List[Tuple[datetime.datetime, float]]],
) -> Dict[str, Tuple[datetime.datetime, float, float]]:
    """Identify stations whose latest observation exceeds their mean temperature using a dict comprehension.
    
    Args:
        observations (Dict): Maps station name -> sorted list of (datetime, temperature) tuples.
        
    Returns:
        Dict[str, Tuple[datetime.datetime, float, float]]: Maps station name ->
            (latest_datetime, latest_temp, mean_temp) for outlier stations.
    """
    stats = station_statistics(observations)
    return {
        st: (obs_list[-1][0], obs_list[-1][1], stats[st][2])
        for st, obs_list in observations.items()
        if obs_list
        and st in stats
        and obs_list[-1][1] > stats[st][2]
    }

def write_statistics(
    filename: str, statistics: Dict[str, Tuple[float, float, float]]
) -> None:
    """Write summary statistics to an output file ordered lexicographically by station name.
    
    Args:
        filename (str): Path to the target output file.
        statistics (Dict): Dict mapping station name -> (min_temp, max_temp, mean_temp).
        
    Raises:
        Exception: Re-raises any I/O exception after logging error details.
    """
    try:
        sorted_stations = sorted(statistics.keys())
        with open(filename, "w", encoding="utf-8") as outfile:
            for st in sorted_stations:
                min_t, max_t, mean_t = statistics[st]
                outfile.write(
                    f"{st}: Min={min_t:.1f}, Max={max_t:.1f}, Mean={mean_t:.1f}\n"
                )
    except Exception as err:
        print(f"[ERROR] Could not write statistics to '{filename}': {err}")
        raise

class TestWeatherAnalyzer(unittest.TestCase):
    """Unittest battery covering edge cases for Weather Station Analyzer."""

    def setUp(self):
        """Create a temporary directory edge cases for Weather Station Analyzer."""
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        """Clean up the temporary directory."""
        self.temp_dir.cleanup()

    def _create_temp_file(self, content: str) -> str:
        """Helper to write test strings to a temporary file."""
        file_path = os.path.join(self.temp_dir.name, "test_data.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return file_path

    def test_multiple_stations(self):
        """1. Test multi-station parsing and grouping."""
        content = (
            "StationA, 08:00:00 AM 01/01/2026, 72.5\n"
            "StationB, 08:00:00 AM 01/01/2026, 65.0\n"
            "StationA, 09:00:00 AM 01/01/2026, 74.0\n"
        )
        file_path = self._create_temp_file(content)
        obs, errors = read_observations(file_path)
        self.assertEqual(len(errors), 0)
        self.assertIn("StationA", obs)
        self.assertIn("StationB", obs)
        self.assertEqual(len(obs["StationA"]), 2)

    def test_negative_temperatures(self):
        """2. Test handling of negative temperatures withen valid bounds."""
        content = "NorthPole, 01:00:00 PM 12/25/2025, -45.5\n"
        file_path = self._create_temp_file(content)
        obs, errors = read_observations(file_path)
        self.assertEqual(len(errors), 0)
        self.assertEqual(obs["NorthPole"][0][1], -45.5)

    def test_duplicate_observations(self):
        """3. Test filtering of duplicate station/datetime entries."""
        content = (
            "StationA, 08:00:00 AM 01/01/2026, 70.0\n"
            "StationA, 08:00:00 AM 01/01/2026, 75.0\n"
        )
        file_path = self._create_temp_file(content)
        obs, errors = read_observations(file_path)
        self.assertEqual(len(obs["StationA"]), 1)
        self.assertEqual(len(errors), 1)

    def test_invalid_temperature_bounds(self):
        """4. Test rejection of out-of-range temperature values."""
        content = "StationA, 08:00:00 AM 01/01/2026, 175.0\n"
        file_path = self._create_temp_file(content)
        obs, errors = read_observations(file_path)
        self.assertEqual(len(obs), 0)
        self.assertEqual(len(errors), 1)

    def test_calculated_statistics(self):
        """5. Test calculation accuracy of Min, Max, and Mean."""
        dt = datetime.datetime.now()
        obs = {"StationB": [(dt, 10.0), (dt, 20.0), (dt, 30.0)]}
        min_t, max_t, mean_t = station_statistics(obs)["StationB"]
        self.assertEqual(min_t, 10.0)
        self.assertEqual(max_t, 30.0)
        self.assertEqual(mean_t, 20.0)

    def test_sorted_output(self):
        """6. Test lexicographical sorting in output formatting."""
        stats = {
            "ZetaStation": (10.0, 20.0, 15.0),
            "AlphaStation": (-5.5, 30.4, 12.4),
        }
        output_file = os.path.join(self.temp_dir.name, "output.txt")
        write_statistics(output_file, stats)
        with open(output_file, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f.readlines()]
        self.assertEqual(
            lines,
            [
                "AlphaStation: Min=-5.5, Max=30.4, Mean=12.4",
                "ZetaStation: Min=10.0, Max=20.0, Mean=15.0",
            ],
        )

    def test_missing_files(self):
        """7. Test error handling for missing file targets."""
        with self.assertRaises(Exception):
            read_observations("non-existent_file.csv")

def main() -> None:
    """Main execution block for Command-Line Interface usage."""
    if len(sys.argv) < 3:
        print(
            f"Usage: python {sys.argv[0]} <input_obs_file> <output_stats_file>",
            file=sys.stderr,
        )
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    try:
        obs, errors = read_observations(input_file)
        if errors:
            print(f"Logged {len(errors)} processing error(s):")
            for line_num, msg in errors:
                print(f"  Line {line_num}: {msg}")
        stats = station_statistics(obs)
        outliers = station_outliers(obs)

        print("\n=== Station Statisitcs ===")
        for st in sorted(stats.keys()):
            min_t, max_t, mean_t = stats[st]
            print (
                f"{st} -> Min: {min_t:.1f}, Max: {max_t:.1f}, Mean: {mean_t:.1f}"
            )
        print("\n=== Outlying Stations (Latest Temp > Mean) ===")
        for st, (dt_val, temp_val, mean_val) in outliers.items():
            dt_formatted = dt_val.strftime("%m/%d/%Y %I:%M:%S %p")
            print(
                f"{st} -> Latest ({dt_formatted}): {temp_val:.1f}°F (Mean: {mean_val:.1f}°F)"
            )

        write_statistics(output_file, stats)
        print(f"\nSuccessfully written summary statistics to: {output_file}")
    except Exception as err:
        print(f"[FATAL ERROR] Command execution failed: {err}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) > 1 and not sys.argv[1].startswith('-'):
        main()
    else:
        unittest.main(argv=['first-arg'], exit=False)
