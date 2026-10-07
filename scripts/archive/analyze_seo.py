import os
import csv

files = [
    "C:\\Users\\hemal\\canonicals_nonindexable_canonical.csv",
    "C:\\Users\\hemal\\canonicals_self_referencing.csv",
    "C:\\Users\\hemal\\canonicals_canonicalised.csv",
    "C:\\Users\\hemal\\canonicals_missing.csv",
    "C:\\Users\\hemal\\canonicals_contains_canonical.csv",
    "C:\\Users\\hemal\\images_missing_size_attributes.csv",
    "C:\\Users\\hemal\\content_readability_very_difficult.csv",
    "C:\\Users\\hemal\\content_readability_difficult.csv",
    "C:\\Users\\hemal\\content_low_content_pages.csv",
    "C:\\Users\\hemal\\h2_nonsequential.csv",
    "C:\\Users\\hemal\\h2_multiple.csv",
    "C:\\Users\\hemal\\h2_missing.csv",
    "C:\\Users\\hemal\\h2_duplicate.csv",
    "C:\\Users\\hemal\\meta_keywords_duplicate.csv",
    "C:\\Users\\hemal\\meta_keywords_missing.csv",
    "C:\\Users\\hemal\\meta_description_over_985_pixels.csv",
    "C:\\Users\\hemal\\meta_description_over_155_characters.csv",
    "C:\\Users\\hemal\\page_titles_over_561_pixels.csv",
    "C:\\Users\\hemal\\page_titles_over_60_characters.csv",
    "C:\\Users\\hemal\\response_codes_external_blocked_by_robots_txt.csv",
    "C:\\Users\\hemal\\response_codes_internal_blocked_by_robots_txt.csv",
    "C:\\Users\\hemal\\response_codes_client_error_(4xx).csv",
    "C:\\Users\\hemal\\response_codes_blocked_by_robots_txt.csv",
    "C:\\Users\\hemal\\response_codes_success_(2xx).csv",
    "C:\\Users\\hemal\\security_missing_secure_referrerpolicy_header.csv",
    "C:\\Users\\hemal\\security_missing_xcontenttypeoptions_header.csv",
    "C:\\Users\\hemal\\security_missing_contentsecuritypolicy_header.csv"
]

report = {}

for filepath in files:
    filename = os.path.basename(filepath)
    if not os.path.exists(filepath):
        report[filename] = "File not found"
        continue
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader, None)
            if not header:
                report[filename] = 0
            else:
                count = sum(1 for row in reader)
                report[filename] = count
    except Exception as e:
        report[filename] = f"Error: {e}"

print("=== SEO AUDIT SUMMARY ===")
for k, v in report.items():
    print(f"{k}: {v} issues")
