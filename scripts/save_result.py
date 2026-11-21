"""Copy the actual outputs of the verified notebook into the README."""
import base64
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
notebook = json.loads((root / "notebooks/etl.ipynb").read_text(encoding="utf-8"))
cell = notebook["cells"][-1]
if cell["execution_count"] is None or any(o["output_type"] == "error" for o in cell["outputs"]):
    raise RuntimeError("Сначала выполните ноутбук целиком.")
stdout = "".join("".join(o["text"]) for o in cell["outputs"] if o.get("name") == "stdout")
png = next((o["data"]["image/png"] for o in cell["outputs"] if "image/png" in o.get("data", {})), None)
if not stdout.strip() or not png:
    raise RuntimeError("В последней ячейке отсутствует результат SQL или изображение.")
docs = root / "docs"
docs.mkdir(exist_ok=True)
(docs / "result.png").write_bytes(base64.b64decode("".join(png)))
readme = root / "README.md"
start, end = "<!-- result:start -->", "<!-- result:end -->"
before, rest = readme.read_text(encoding="utf-8").split(start, 1)
_, after = rest.split(end, 1)
result = f"\n\nВывод последней ячейки после запуска.\n\n```text\n{stdout.rstrip()}\n```\n\n![Результат SQL из последней ячейки ноутбука](docs/result.png)\n\n"
readme.write_text(before + start + result + end + after, encoding="utf-8")
