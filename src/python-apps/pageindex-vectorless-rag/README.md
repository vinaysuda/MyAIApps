# PageIndex RAG Demo

**Chat with your documents using AI — no vector database needed.**

PageIndex takes a fundamentally different approach to document Q&A. Instead of chunking your PDF and doing keyword/embedding search, it builds a **reasoning tree** (a smart, hierarchical summary of the document) and uses an LLM to *navigate* that tree — the same way a human expert would skim an index to find an answer.

---

## How It Works

```
PDF → PageIndex builds a Reasoning Tree → LLM navigates the tree → Cited, accurate answer
```

1. **Submit your PDF** to PageIndex — it analyzes the document and builds a hierarchical tree of sections and summaries.
2. **Ask a question** — an LLM reads the tree (not the full document) and identifies which sections are relevant.
3. **Retrieve only what matters** — the actual text from those sections is fetched and passed to the LLM.
4. **Get a grounded answer** — the final response is generated from real document content with full traceability.

---

## Why Not Vector Search?

| | Vector/Chunk RAG | PageIndex (Tree RAG) |
|---|---|---|
| Retrieval method | Embedding similarity | LLM-guided tree navigation |
| Explainability | Low — black-box embeddings | High — you see *why* each section was picked |
| Context quality | Fragmented chunks | Full, structured sections |
| Setup complexity | Needs a vector DB | Just an API key |

---

## Quickstart

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/PageIndex.git
cd PageIndex
```

### 2. Install dependencies

```bash
pip install pageindex openai python-dotenv
```

### 3. Set up your API keys

Create a `.env` file in the project root:

```
PAGEINDEX_API_KEY=your_pageindex_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

Get your PageIndex API key at [dash.pageindex.ai/api-keys](https://dash.pageindex.ai/api-keys).

### 4. Run the notebook

Open `page_index.ipynb` in Jupyter and run cells top to bottom. The notebook walks through every step with inline explanations.

---

## Notebook Walkthrough

| Step | What Happens |
|------|-------------|
| 1 | Install the `pageindex` library |
| 2 | Set up the OpenAI LLM helper |
| 3 | Connect to PageIndex with your API key |
| 4 | Upload a PDF and get a `doc_id` |
| 5 | Wait for processing; retrieve the reasoning tree |
| 6 | Ask the LLM to navigate the tree for a query |
| 7 | Review which nodes (sections/pages) were selected |
| 8 | Fetch node text and generate the final answer |
| 9 | Use the `ask()` helper to run any query end-to-end |

---

## Example

```python
await ask("What are the penalties for sexual harassment?")
```

```
Relevant Nodes: ['0015', '0017', '0018']

Answer:
Penalties range from a formal warning and mandatory training to suspension, demotion,
or immediate termination depending on severity. Sexual assault results in mandatory dismissal.
```

---

## Requirements

- Python 3.8+
- `pageindex`
- `openai`
- `python-dotenv`
- A PageIndex API key
- An OpenAI API key

---

## License

MIT
