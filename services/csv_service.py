import pandas as pd
from dateutil import parser
from datetime import datetime
from extensions import mongo
def parse_purchase_csv(stream, owner_email):
    """
    stream: file-like object (uploaded CSV)
    Returns list of dicts ready for insertion (with 'user' field)
    """
    df = pd.read_csv(stream)
    # normalize expected columns if present
    expected = ["order_id","platform","item_name","category","quantity","unit_price",
                "delivery_fee","tip","total_amount","payment_method","order_datetime","tags","notes"]
    # keep only expected intersection
    cols = [c for c in expected if c in df.columns]
    df = df[cols].copy()
    # fill missing columns with defaults
    for c in expected:
        if c not in df.columns:
            df[c] = None

    # convert numeric fields
    for ncol in ["quantity","unit_price","delivery_fee","tip","total_amount"]:
        if ncol in df.columns:
            df[ncol] = pd.to_numeric(df[ncol], errors='coerce').fillna(0.0)

    # parse datetimes
    def parse_dt(x):
        try:
            return parser.parse(str(x))
        except Exception:
            return None

    df["order_datetime"] = df["order_datetime"].apply(parse_dt)

    records = df.to_dict(orient="records")
    # attach user, tidy each record
    out = []
    for r in records:
        # ensure order_datetime is python datetime object (pandas may give Timestamp)
        dt = r.get("order_datetime")
        if hasattr(dt, "to_pydatetime"):
            dt = dt.to_pydatetime()
        r["order_datetime"] = dt
        r["user"] = owner_email
        out.append(r)
    return out
