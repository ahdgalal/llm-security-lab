## Provider Comparison

I compared OpenAI `gpt-5-nano` with OpenRouter's `openrouter/free` using the same embeddings prompt.

### OpenAI

| Run | Model | Input | Output | Reasoning | Latency |
|---|---|---:|---:|---:|---:|
| 1 | gpt-5-nano | 23 | 847 | 640 | 12.28s |
| 2 | gpt-5-nano | 23 | 666 | 512 | 8.39s |
| 3 | gpt-5-nano | 23 | 900 | 704 | 10.78s |

`gpt-5-nano` gave consistent answers, but most of the output tokens were reasoning tokens (about 76–78%).

### OpenRouter

| Run | Actual Model | Input | Output | Reasoning | Latency |
|---|---|---:|---:|---:|---:|
| 1 | cohere/north-mini-code:free | 13 | 142 | 61 | 3.00s |
| 2 | nvidia/nemotron-3.5-content-safety:free | 469 | 136 | 145 | 1.93s |
| 3 | nvidia/nemotron-3.5-content-safety:free | 469 | 81 | 78 | 11.78s |

OpenRouter was less consistent because `openrouter/free` routed requests to different models. Runs 2 and 3 were sent to a safety model, which returned `User Safety: safe` instead of answering the question.

For evals and red-teaming, I would **pin one specific model** so the results are reproducible.