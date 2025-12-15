import pandas as pd
import numpy as np
from pathlib import Path

def main():
    np.random.seed(0)
    n = 200

    df = pd.DataFrame({
        "cell_id": [f"cell_{i:04d}" for i in range(n)],
        "cluster": np.random.choice([0,1,2,3,4,5,6], size=n),
        "n_genes": np.random.randint(200, 6000, size=n),
        "n_counts": np.random.randint(500, 40000, size=n),
        "pct_mt": np.round(np.random.beta(2, 10, size=n) * 100, 2),
    })

    outdir = Path("data/sample")
    outdir.mkdir(parents=True, exist_ok=True)
    outpath = outdir / "metadata.csv"

    df.to_csv(outpath, index=False)
    print(f"Saved: {outpath} ({len(df)} rows)")

if __name__ == "__main__":
    main()
