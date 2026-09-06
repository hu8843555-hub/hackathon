# Kisan Dost

Modular agricultural agent engine for Pakistani farmers — powered by **Gemini API**.

## Setup

```powershell
cd "d:\today assignment"
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

Add your Gemini API key to `.env`:

```
GEMINI_API_KEY=your_key_here
```

Get a free key at [Google AI Studio](https://aistudio.google.com/apikey).

## Run

```powershell
.\venv\Scripts\Activate.ps1
python main.py
```

## Architecture

```
kisan_dost/
├── agent.py          # Gemini LLM + function calling loop
├── context.py        # Session memory (location, crop, land size)
├── prompts.py        # System prompt & safety guardrails
├── router.py         # Intent routing & pre-checks
└── tools/
    ├── fertilizer.py     # Urea/DAP bag calculator (PKR)
    ├── crop_advisor.py   # Crop profitability profiles
    ├── pest_doctor.py    # Pest ID + safe dilution ratios
    ├── market_weather.py # Mandi rates + weather advisories
    └── govt_schemes.py   # Subsidies + break-even analysis
```

## Domains

| Domain | Tools | Example Query |
|--------|-------|---------------|
| Agri Advisory | `fertilizer_calculator`, `crop_advisor` | "5 acre wheat ke liye kitni Urea?" |
| Pest Doctor | `pest_doctor` | "Cotton pe sundhi lag gayi hai" |
| Market & Weather | `market_weather` | "Faisalabad mandi wheat rate?" |
| Govt Schemes | `govt_schemes` | "Kisan Card subsidy aur break-even" |

## Direct Tool Test (no API key)

```powershell
python -c "from kisan_dost.agent import KisanDostAgent; print(KisanDostAgent.run_tool_directly('fertilizer_calculator', crop='wheat', acres=5))"
```

## Safety

- Off-topic queries are rejected
- Pesticide advice always includes dilution (ml/100L) + safety gear
- Chemical ingestion triggers emergency medical warning (115/1166)
