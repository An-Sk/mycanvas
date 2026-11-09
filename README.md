# mycanvas

mycanvas - A LangChain agent that transforms Markdown or PDF notes into Obsidian Canvas JSON files.

## Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd mycanvas
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your OpenAI API key:
   ```bash
   echo "OPENAI_API_KEY=your_api_key_here" > .env
   ```

4. Run the application:
   ```bash
   python main.py
   ```

## Usage

### Summarize

```bash
python main.py summarize --args "file_name"
```

### Generate Canvas

```bash
python main.py generate_canvas --args "file_name"
```

## Roadmap

### Done
- [x] Migrate prompt templates from `.txt` to `.toml`
- [x] Consolidate LLM loading into `utils/llm_loader.py` (removed `utils/llm_instance.py`)
- [x] Summarization output path: `summarize_tool` accepts `output_path` and saves via `save_md`
- [x] Better error logging: full tracebacks in `summarize.py` and `generate_canvas.py`

### In progress
- [ ] Task planning: `run_task_tool` is defined in `agent.py` but not wired into `get_agent()` tools list — agent can't use it yet
  - `planner.py`, `registry.py`, `task_handler.py` need refactoring (flagged as fragile / "sucks" / needs bullet-list plan support)

### Todo
- [ ] Multi-note search / folders — search handles patterns but no multi-note or folder aggregation
- [ ] Unify `save_json` / `save_md` into one helper, add append support
- [ ] Streaming responses
- [ ] Multi-step prompt / better canvas generation

### Future goals
- [ ] Support for PDF files
- [ ] Support for attachments (images, etc.)
- [ ] Support for multiple LLM providers
