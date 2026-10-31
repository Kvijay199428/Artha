import os, json

data_dir = r'd:\VEGA\ARTHA\data'
dirs = ['bills', 'clients', 'products', 'purchases', 'expenses', 'receipts', 'profiles', 'templates', 'recurring', 'trash']

print("==================================================")
print("  ARTHA Database Collections Schema Inspection")
print("==================================================")

for d in dirs:
    dp = os.path.join(data_dir, d)
    if os.path.exists(dp):
        files = [f for f in os.listdir(dp) if f.endswith('.json')]
        if files:
            sample_file = os.path.join(dp, files[0])
            with open(sample_file, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    print(f"\n--- COLLECTION: {d} (count: {len(files)}, sample: {files[0]}) ---")
                    if isinstance(data, dict):
                        print("Keys:", list(data.keys()))
                        for k, v in data.items():
                            v_type = type(v).__name__
                            if isinstance(v, dict):
                                print(f"  {k} (object): {list(v.keys())}")
                            elif isinstance(v, list):
                                item_type = type(v[0]).__name__ if v else "empty"
                                print(f"  {k} (array of {item_type}, len={len(v)})")
                                if v and isinstance(v[0], dict):
                                    print(f"    sample item keys: {list(v[0].keys())}")
                            else:
                                print(f"  {k} ({v_type}): {repr(v)[:80]}")
                    else:
                        print("Type:", type(data))
                except Exception as e:
                    print(f"{d} read error: {e}")
        else:
            print(f"\n--- COLLECTION: {d} (0 files) ---")

for meta_f in ['meta.json', 'local-prefs.json', 'profile.json']:
    mp = os.path.join(data_dir, meta_f)
    if os.path.exists(mp):
        with open(mp, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                print(f"\n--- ROOT DOCUMENT: {meta_f} ---")
                if isinstance(data, dict):
                    print("Keys:", list(data.keys()))
                    for k, v in list(data.items())[:12]:
                        v_type = type(v).__name__
                        if isinstance(v, dict):
                            print(f"  {k} (object): {list(v.keys())}")
                        elif isinstance(v, list):
                            print(f"  {k} (array[{len(v)}])")
                        else:
                            print(f"  {k} ({v_type}): {repr(v)[:80]}")
            except Exception as e:
                print(f"{meta_f} error: {e}")

