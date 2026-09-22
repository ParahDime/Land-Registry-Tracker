import pandas as pd
from pathlib import Path
 
 #Load in the dataset
def load_data(path: str) -> pd.DataFrame:
    """Load csv, xlsx, or json into a DataFrame based on file extension."""
    ext = Path(path).suffix.lower()
 
    if ext == ".csv":
        return pd.read_csv(path)
    elif ext in (".xlsx", ".xls"):
        return pd.read_excel(path)
    elif ext == ".json":
        return pd.read_json(path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")
 
 #clean the data
def sanitise(df: pd.DataFrame) -> pd.DataFrame:
    """
    Basic, dataset-agnostic cleaning pass.
    Extend this with dataset-specific rules (e.g. postcode format) later.
    """
    df = df.copy()
 
    # Standardise column names: lowercase, no spaces
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
 
    # Strip whitespace from string/object columns
    str_cols = df.select_dtypes(include="object").columns
    df[str_cols] = df[str_cols].apply(lambda col: col.str.strip())
 
    # Drop fully empty rows/columns
    df = df.dropna(how="all").dropna(axis=1, how="all")
 
    # Drop exact duplicate rows
    df = df.drop_duplicates()
 
    return df
 
 #output any null found
def report_missing(df: pd.DataFrame) -> pd.Series:
    """Quick view of null counts per column, sorted worst first."""
    return df.isna().sum().sort_values(ascending=False)

LAND_REGISTRY_NULLABLE = {"saon", "locality"} #values can be null

#handles null values
def assess_nulls(df: pd.DataFrame, nullable: set[str] = LAND_REGISTRY_NULLABLE) -> pd.DataFrame:
    """
    Split null counts into 'expected' (structural, leave alone) vs
    'unexpected' (genuinely missing, needs a decision per row/column).
    Doesn't modify df — just tells you where to focus.
    """
    counts = df.isna().sum()
    counts = counts[counts > 0]
 
    return pd.DataFrame({
        "null_count": counts,
        "category": ["expected" if c in nullable else "unexpected" for c in counts.index],
    }).sort_values("category")

def handle_nulls():
    print("garmin")