# Temperature Experiment

## Goal

The goal was to see how temperature affects the variation of LLM responses. I tested different temperature values using the same prompt and compared the responses across multiple runs.

## Important limitation

A single run isn't enough to conclude that temperature changes the output significantly. The same temperature can sometimes produce very similar responses, especially when the prompt has an obvious or constrained answer.

To observe variation, each temperature should be tested multiple times.

## Findings

In my first test, two different temperatures produced nearly identical answers. This did not mean that temperature had no effect. A single run was not enough to measure variation.

After running each temperature several times, I found that higher temperatures produced more variation in the wording and responses, while lower temperatures were generally more consistent.

## Conclusion

Temperature affects how much variation can appear in model outputs, but it does not control the model's knowledge or guarantee a different answer on every request.

For experiments and comparisons, multiple runs are more useful than comparing only one response at each temperature.

## Project-specific note

The OpenAI provider does not currently send the temperature parameter because the selected `gpt-5-nano` model did not support it in the API configuration used during testing.

The OpenRouter provider still accepts and sends the temperature value.
