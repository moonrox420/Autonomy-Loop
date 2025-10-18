# Autonomy-Loop
market scan
This repository contains an example implementation of a fully autonomous
revenue generation engine. The system continuously scans the market for
trending topics, synthesizes them into product offers and exposes a
web-based UI for customers to purchase the offers. A PowerShell script
(`loop.ps1`) orchestrates the entire workflow, bootstrapping the backend,
frontend, market scan, offer builder and optional local LLM invocation.

## Features

- 🔎 **Market scanning** using Reddit trending subreddits, Google Trends and
  Amazon Movers & Shakers.
- 🛠️ **Offer generation** with optional Stripe product creation and price
  configuration.
- 🧠 **Local LLM integration** via Ollama prompts to generate sales copy.
- 🎨 **React + Tailwind UI** served by Vite with a dynamic offer card and
  checkout button.
- 🔁 **Loop engine** for continuous operation, with configurable sleep
  intervals.
- 🎯 **Stripe Checkout** endpoint to initiate purchases (requires a valid
  `STRIPE_API_KEY`).

## Directory structure

```
Code-AutonomyLoop/
├── backend/
│   └── app/
│       ├── main.py             # FastAPI application
│       ├── market_agent.py     # Market data scraper
│       ├── offer_builder.py    # Offer generation logic
│       ├── loop_engine.py      # Loop orchestrator
│       └── utils.py            # Shared helpers
├── frontend/
│   ├── index.html              # Vite entry point
│   ├── tailwind.config.js      # Tailwind configuration
│   ├── vite.config.ts          # Vite configuration
│   └── src/
│       ├── main.tsx            # React entry point
│       ├── index.css           # Tailwind imports
│       ├── App.tsx             # Main React component
│       ├── api/
│       │   └── fetchOffer.ts   # API helper
│       └── components/
│           ├── OfferCard.tsx   # Offer display card
│           └── CTA.tsx         # Checkout button component
├── models/
│   └── prompt_templates/
│       ├── offer_generator.txt # Prompt template for copywriting
│       └── market_summary.txt  # Prompt template for market summary
├── loop_data/                  # Runtime artefacts (market scan and offer)
├── loop.ps1                    # PowerShell orchestration script
├── requirements.txt            # Python dependencies
├── .env                        # Environment configuration (values to fill in)
└── README.md                   # Project documentation
```

## Quick start

This project assumes a Windows 11 environment for the PowerShell orchestrator
and that Node.js and Python are installed. The backend and frontend can be
run independently of the orchestrator if desired.

### 1. Clone and set up

```powershell
git clone https://github.com/your-org/autonomy-loop.git
cd autonomy-loop/Code-AutonomyLoop

# Create and activate a Python virtual environment
python -m venv .venv
.\ .venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Install frontend dependencies
cd frontend
npm install
cd ..

# Copy environment template
Copy-Item .env.example .env
# Fill in STRIPE_API_KEY and any other variables as needed
```

### 2. Running with the loop orchestrator

The PowerShell script `loop.ps1` automates the entire pipeline. It:

1. Starts the FastAPI backend on the configured port
2. Starts the Vite dev server for the React frontend
3. Executes the market agent and offer builder
4. Optionally invokes an Ollama model to generate copy
5. Launches the loop engine to monitor and regenerate offers

```powershell
./loop.ps1
```

Ensure that the `ollama` command is available in your PATH and that the
`OLLAMA_MODEL` environment variable points to a valid model (for example
`dolphin-mixtral`) if you intend to generate copy locally.

### 3. Running services manually

If you prefer to run the services manually or on non-Windows systems you can:

```bash
# Start backend
cd backend/app
uvicorn main:app --host 127.0.0.1 --port 9333

# In a new terminal, start the frontend
cd frontend
npm run dev -- --port 5174

# In another terminal, run the agents as desired
python backend/app/market_agent.py
python backend/app/offer_builder.py
python backend/app/loop_engine.py  # optional loop
```

### 4. Stripe configuration

To enable real purchases you must provide a valid `STRIPE_API_KEY` in your
`.env` file. The offer builder creates products and prices on Stripe if
configured. The `/checkout-session` API endpoint uses the generated
`stripe_price_id` to create a checkout session and returns a URL for
redirection.

### 5. Customization

You can adjust the frequency of the loop via the `LOOP_INTERVAL` environment
variable (in seconds). Running the loop engine with `RUN_ONCE=1` will
execute a single iteration and exit, which is useful for debugging.

Feel free to extend the market agent with additional sources, refine the
offer generation prompt templates or replace the frontend with your own UI.

---

This project serves as a foundation for building autonomous AI-driven
businesses. Adapt and extend it to fit your own workflows and models.
