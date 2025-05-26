#weather_mapreduce
#!/usr/bin/env python3
import sys

def mapper():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) < 4:
            continue
        try:
            date_str = parts[2]  # e.g., 20060201_0
            temperature = float(parts[3])  # e.g., 51.75
            date = date_str.split('_')[0]  # extract YYYYMMDD
            print(f"{date}\t{temperature}")
        except:
            continue

def reducer():
    current_date = None
    total_temp = 0
    count = 0

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            date, temp = line.split("\t")
            temp = float(temp)
        except:
            continue

        if date == current_date:
            total_temp += temp
            count += 1
        else:
            if current_date:
                avg_temp = total_temp / count
                print(f"{current_date}\t{avg_temp:.2f}")
            current_date = date
            total_temp = temp
            count = 1

    if current_date:
        avg_temp = total_temp / count
        print(f"{current_date}\t{avg_temp:.2f}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["mapper", "reducer"])
    args = parser.parse_args()

    if args.mode == "mapper":
        mapper()
    elif args.mode == "reducer":
        reducer()
