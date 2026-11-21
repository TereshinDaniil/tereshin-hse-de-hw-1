#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

if [[ ! -f .env ]]; then
  python3 - <<'PY'
from pathlib import Path
from secrets import token_hex
from os import fdopen, open as os_open, O_WRONLY, O_CREAT, O_EXCL

template = Path(".env.example").read_text()
with fdopen(os_open(".env", O_WRONLY | O_CREAT | O_EXCL, 0o600), "w") as out:
    out.write(template.replace("POSTGRES_PASSWORD=\n", f"POSTGRES_PASSWORD={token_hex(24)}\n"))
PY
fi
docker compose up -d --wait
docker compose ps
if [[ ! -x .venv/bin/python ]]; then
  python3 -m venv .venv
fi
export PATH="$PWD/.venv/bin:$PATH"
python -m pip install -r requirements.txt
python -m ipykernel install --prefix "$PWD/.venv" --name hw1-population --display-name "Python (HW1 ETL)"
for run in 1 2; do
  echo "Запуск ноутбука $run из 2"
  jupyter nbconvert --to notebook --execute --inplace \
    --ExecutePreprocessor.kernel_name=hw1-population \
    --ExecutePreprocessor.timeout=240 notebooks/etl.ipynb
done
docker compose exec -T postgres sh -c 'psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "SELECT COUNT(*) AS rows_total, COUNT(DISTINCT (country_code, year)) AS unique_keys FROM stg.population;"'
python scripts/save_result.py
