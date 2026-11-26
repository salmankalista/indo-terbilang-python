# `indo-terbilang` (Python)

Micro-library Python modern untuk mengonversi angka menjadi kalimat **terbilang Bahasa Indonesia baku (EYD V / KBBI)** serta memformat dan mem-parsing mata uang **Rupiah (IDR)** secara deterministik — dengan **zero runtime dependencies**.

---

## Fitur Utama

- **Zero Runtime Dependencies:** Hanya memakai Python Standard Library (`>= 3.9`), tanpa ketergantungan `locale` OS.
- **Presisi Finansial (`int | float | Decimal | str`):** Mendukung native `decimal.Decimal` serta integer raksasa hingga skala **`desiliun`** ($10^{36} - 1$).
- **Type-Safe (PEP 561):** Menyertakan type hints penuh dan marker `py.typed` untuk `mypy` / `pyright`.
- **Akurat EYD V / KBBI:** `seribu`, `sebelas`, `seratus`, `satu juta`, ejaan baku `miliar`, dan desimal digit-per-digit (`3.14` $\to$ `"tiga koma satu empat"`).
- **Fail-Loud (`TerbilangError`):** Input invalid (`bool`, `NaN`, `Infinity`, string kosong/rusak) melempar `TerbilangError` (turunan `ValueError`) dengan kode error terstruktur.

---

## Instalasi

### 1. Via `pip` / `uv` (dari GitHub atau Folder Lokal)

```bash
# Install langsung dari GitHub
pip install git+https://github.com/salmankalista/indo-terbilang-python.git

# Atau menggunakan uv
uv pip install git+https://github.com/salmankalista/indo-terbilang-python.git

# Install dari folder lokal
pip install .
```

### 2. Download atau Clone Manual dari GitHub

- **Download ZIP:** Unduh arsip source code terbaru dari https://github.com/salmankalista/indo-terbilang-python/archive/refs/heads/main.zip (atau **Code $\to$ Download ZIP** di https://github.com/salmankalista/indo-terbilang-python), lalu ekstrak.
- **Atau Clone via Git:**
  ```bash
  git clone https://github.com/salmankalista/indo-terbilang-python.git
  cd indo-terbilang-python
  pip install -e .
  ```

Atau jalankan langsung pengujian tanpa instalasi dengan menambahkan `src/` ke `PYTHONPATH`:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

---

## Contoh Tampilan Aplikasi Uji (Playground)

Contoh penerapan langsung pada aplikasi uji interaktif berbasis Python 3 (`1250750.50` $\to$ `Rp 1.250.750,50` & `"Satu Juta Dua Ratus Lima Puluh Ribu Tujuh Ratus Lima Puluh Rupiah Lima Puluh Sen"`):

![Demo Playground Python indo_terbilang](./docs/playground-python.png)

> **Varian Bahasa Lain:**
> - **TypeScript / JavaScript (npm):** https://github.com/salmankalista/indo-terbilang
> - **PHP:** https://github.com/salmankalista/indo-terbilang-php

---

## Quick Start

```python
from decimal import Decimal
from indo_terbilang import (
    terbilang,
    terbilang_rupiah,
    format_rupiah,
    parse_rupiah,
)

terbilang(1500000)
# => "satu juta lima ratus ribu"

terbilang(1500000, style="title", suffix="rupiah")
# => "Satu Juta Lima Ratus Ribu Rupiah"

terbilang_rupiah(Decimal("1250.50"))
# => "seribu dua ratus lima puluh rupiah lima puluh sen"

format_rupiah(1500000)
# => "Rp 1.500.000,00"

format_rupiah(1500000, compact=True)
# => "Rp 1,5 jt"

parse_rupiah("Rp 1.500.000,50")
# => "1500000.50"
```

---

## Tutorial Pemakaian Praktis

### Tutorial 1: Invoice / Kwitansi Backend (Django, FastAPI, Flask)

Gunakan `Decimal` atau `str` dari database agar nominal selalu presisi:

```python
from decimal import Decimal
from indo_terbilang import format_rupiah, terbilang_rupiah

total_tagihan = Decimal("1250750.50")

nominal_display = format_rupiah(total_tagihan)
# => "Rp 1.250.750,50"

kalimat_kwitansi = terbilang_rupiah(total_tagihan, style="title")
# => "Satu Juta Dua Ratus Lima Puluh Ribu Tujuh Ratus Lima Puluh Rupiah Lima Puluh Sen"
```

### Tutorial 2: Membersihkan Input String Rupiah & Menangani Error

```python
from indo_terbilang import TerbilangError, format_rupiah, parse_rupiah, terbilang_rupiah

try:
    clean = parse_rupiah("Rp 2.500.000,75")  # => "2500000.75"
    print(format_rupiah(clean))
    print(terbilang_rupiah(clean, style="sentence"))
except TerbilangError as err:
    print(f"Error [{err.code}]: {err}")
```

### Tutorial 3: Format Akuntansi & Dashboard Ringkas (`compact`)

```python
from indo_terbilang import format_rupiah

# Format akuntansi negatif dalam kurung tanpa sen
format_rupiah(-750000, decimals=0, negative_format="parentheses")
# => "(Rp 750.000)"

# Format ringkas KPI dashboard
format_rupiah(2350000000, compact=True, compact_decimals=2)
# => "Rp 2,35 M"
```

---

## Referensi API

- **`terbilang(value, *, style="lower", prefix=None, suffix=None, negative_prefix="minus", decimal_word="koma", trim_trailing_decimal_zeros=False)`**
- **`terbilang_rupiah(value, *, style="lower", prefix=None, suffix=None, negative_prefix="minus", currency_unit="rupiah", include_sen=True, sen_unit="sen", rounding="half-up")`**
- **`format_rupiah(value, *, symbol="Rp", space_after_symbol=True, thousands_separator=".", decimal_separator=",", decimals=2, rounding="half-up", negative_format="minus", compact=False, compact_decimals=1)`**
- **`parse_rupiah(value)`** $\to$ mengembalikan string numerik kanonik (`"1500000.50"`).
- **`TerbilangError`** $\to$ subclass `ValueError` dengan `.code` (`"INVALID_INPUT" | "NON_FINITE_NUMBER" | "OUT_OF_RANGE"`).

---

## Kredit & Referensi

Kaidah penulisan bilangan merujuk pada aturan baku **EYD V / KBBI** (Badan Pengembangan dan Pembinaan Bahasa).

---

## Lisensi

[MIT](./LICENSE) © 2026 salmankalista
