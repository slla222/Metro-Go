
#!/usr/bin/env python3
# Convert a single Wikidata CSV (stations with line order and coords) into app JSON graph.
# CSV columns expected: line,lineLabel,station,stationLabel,coord,ordinal

import csv, json, sys, re

def slugify(name):
    s = name.lower()
    s = re.sub(r'[^a-z0-9]+', '_', s)
    s = re.sub(r'_+', '_', s).strip('_')
    return s or "station"

def parse_coord(coord):
    # Wikidata coord format: "Point(lon lat)" or "lat,lon" depending on output; handle both
    coord = coord.strip()
    if coord.startswith("Point("):
        vals = coord[6:-1].split()
        lon = float(vals[0]); lat = float(vals[1])
        return lat, lon
    if ',' in coord:
        lat, lon = coord.split(',', 1)
        return float(lat), float(lon)
    raise ValueError("Unknown coord format: " + coord)

def main():
    if len(sys.argv) < 4:
        print("Usage: convert_stations.py stations.csv edges.csv output.json")
        print("For Wikidata CSV, pass the same CSV for both stations and edges.")
    csv_path = sys.argv[1]
    out_path = sys.argv[3]

    # Group stations by line with order
    lines = {}  # lineLabel -> list of (id, nameRu, nameEn, lat, lon)
    all_stations = {}  # id -> station dict

    with open(csv_path, newline='', encoding='utf-8') as f:
        rdr = csv.DictReader(f)
        for r in rdr:
            name_ru = r.get('stationLabel') or r.get('stationLabel_ru') or r.get('stationLabel_en') or ""
            name_en = r.get('stationLabel_en') or name_ru
            line_label = r.get('lineLabel') or ""
            coord = r.get('coord') or ""
            ordinal = r.get('ordinal') or ""
            try:
                lat, lon = parse_coord(coord)
            except Exception:
                continue
            sid = slugify(name_en or name_ru)
            if sid not in all_stations:
                all_stations[sid] = {
                    "id": sid,
                    "nameRu": name_ru or name_en,
                    "nameEn": name_en or name_ru,
                    "lat": lat,
                    "lon": lon,
                    "lineId": slugify(line_label) if line_label else "unknown",
                    "neighbors": []
                }
            lines.setdefault(line_label, []).append((ordinal, sid))

    # Sort each line by ordinal and connect neighbors
    for line, items in lines.items():
        def key(x):
            try:
                return int(x[0])
            except Exception:
                return 10**9
        items_sorted = sorted(items, key=key)
        for i in range(len(items_sorted)-1):
            a = items_sorted[i][1]; b = items_sorted[i+1][1]
            if a in all_stations and b in all_stations:
                all_stations[a]["neighbors"].append({"toStationId": b, "travelSeconds": 120})
                all_stations[b]["neighbors"].append({"toStationId": a, "travelSeconds": 120})

    # Merge transfers by identical names (rough) — adds edges between same-named stations on different lines
    by_name = {}
    for sid, st in all_stations.items():
        key = (st["nameRu"] or st["nameEn"]).lower()
        by_name.setdefault(key, []).append(sid)
    for same in by_name.values():
        if len(same) > 1:
            for i in range(len(same)-1):
                a, b = same[i], same[i+1]
                all_stations[a]["neighbors"].append({"toStationId": b, "travelSeconds": 180})
                all_stations[b]["neighbors"].append({"toStationId": a, "travelSeconds": 180})

    graph = {"stations": list(all_stations.values())}
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(graph, f, ensure_ascii=False, indent=2)
    print("Wrote", out_path, "with", len(all_stations), "stations")

if __name__ == "__main__":
    main()
