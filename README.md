# AI Engineering Journey

Learning to build AI applications with Python, step by step.

## Day 1: LLM Basics
- Ran a local LLM (Llama 3.2) on my laptop using Ollama
- Made my first LLM call from Python
- Used system prompts to control the model's behavior
- Built a terminal chatbot with conversation memory
- Added streaming responses (word-by-word output)

### Key lesson
LLMs are stateless: they don't remember anything between calls.
A chatbot "remembers" because the app resends the full conversation history on every turn.

# Day 2: Limitations
-- Known limitation: the small model still confuses "a Faisalabad software house" with a company name
## Day 3: Evaluation (Evals)
- Built an automatic test that scores the extractor against an answer key
- 6 test cases (3 new ones the prompt had never seen)
- Score: 35/36 fields correct (97%)

### Experiment: what does each part do?

| Version | Score | What broke |
|---|---|---|
| Full system | 35/36 (97%) | Company name in one case |
| Without code rules | 33/36 (92%) | Experience, "Remote" in title |
| Without few-shot example | 33/36 (92%) | Short title, city misspelled ("Mulan") |

### Key lessons
- Each part fixes different mistakes, so both are needed
- Two equal scores can hide very different problems: always read the mistakes
- The AI doesn't check its answers; it guesses one piece at a time
