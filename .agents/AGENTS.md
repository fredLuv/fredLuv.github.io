# Agent Rules for Ethan-Resume Workspace

## TimesFM Stock Forecasting Rule
- Whenever the user prompts to run "timefm stocks" or "timefm" with a list of stock tickers (e.g. "run timefm: huya, tme..."), always use the pre-configured Python script `/Users/fred/NeoQuant/prototypes/timesfm_ai_future/run_ratio_forecast.py` to run the strict 3:1 ratio forecasts.
- The script should be executed in the `/Users/fred/NeoQuant/prototypes/timesfm_ai_future` directory using its local virtual environment python: `.venv/bin/python run_ratio_forecast.py --tickers T1 T2 T3...`
- Ensure any tickers passed by the user are parsed and passed as space-separated arguments to the `--tickers` flag.
- Copy all output charts and the summary CSV file to the conversation's active artifact directory, and present a formatted markdown summary with the carousel of the plots.
