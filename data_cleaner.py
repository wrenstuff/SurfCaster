import pandas as pd
from SurfCaster.url_extractor import extract_url_features, FEATURE_ORDER

INPUT_CSV = "dataset_phishing.csv"
OUTPUT_CSV = "data.csv"

URL_COLUMN = "url"
STATUS_COLUMN = "status"
RANDOM_COLUMN = "random_domain"


def main():
    df = pd.read_csv(INPUT_CSV)

    output_feature_order = [
        col for col in FEATURE_ORDER if col != RANDOM_COLUMN
    ]

    rows = []

    for index, row in df.iterrows():
        url = str(row[URL_COLUMN]).strip()

        if not url or url.lower() == "nan":
            continue

        try:
            feature_tensor = extract_url_features(url)

            feature_values = feature_tensor.squeeze(0).tolist()

            output_row = dict(zip(FEATURE_ORDER, feature_values))

            output_row.pop(RANDOM_COLUMN, None)

            output_row["status"] = row[STATUS_COLUMN]

            output_row["url"] = url

            rows.append(output_row)

        except Exception as e:
            print(f"Skipping row {index} because of error: {e}")
            print(f"URL was: {url}")

    output_df = pd.DataFrame(rows)

    columns = ["url"] + output_feature_order + ["status"]
    output_df = output_df[columns]

    output_df.to_csv(OUTPUT_CSV, index=False)

    print(f"Saved {len(output_df)} rows to {OUTPUT_CSV}")
    print(f"Feature count: {len(FEATURE_ORDER)}")
    print(f"Columns saved: {len(output_df.columns)}")


if __name__ == "__main__":
    main()