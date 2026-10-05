# llm-security-lab

A small Python project that uses the OpenAI SDK to send prompts to an OpenAI model and compare responses at different temperature values.

# What it does

- Sends a system instruction and user prompt to an OpenAI model.
- Runs the same prompt with different temperature values.
- Prints the model's responses.
- Displays token usage.

# Setup

Create a .env file in the project folder:
OPENAI_API_KEY=your_api_key_here

# Requirements

Python 3.12+
API-Key

# Run 

```
uv run main.py
```

# Temperature Experiment

The project runs the same prompt using different temperature values, such as:

Temperature	Observed result
0.0	Responses were highly consistent
0.5	Responses were mostly consistent, with some variation
1.0	Responses showed more variation

Initial runs produced nearly identical answers at different temperatures, showing that one run is not enough to observe variation. After running each temperature multiple times, higher temperatures produced more varied responses, while lower temperatures were more consistent. Overall, temperature affects randomness, but the difference may not be obvious in every individual run.


# Output Example

```
=== Temperature 0.2 ===
An SDK (Software Development Kit) is a collection of software tools, libraries, and documentation provided by a company or platform to help developers build applications for its ecosystem. It typically includes pre-written code, APIs, and sample projects that streamline the development process without requiring developers to write everything from scratch. Common examples include Apple's Xcode SDK for iOS/macOS development and Google's Android SDK for mobile app creation.

Tokens used: 331

=== Temperature 1.0 ===
An SDK (Software Development Kit) is a collection of tools, libraries, documentation, and code samples that developers use to build applications for a specific platform or service. It simplifies the development process by providing pre-built components so programmers don't have to write code from scratch for common functions like authentication or hardware access. Essentially, it acts as a specialized toolbox that ensures compatibility and accelerates the creation of software for a target environment.

Tokens used: 136

```

# Future work

 - v2.0 will handle the risk of LLM01:2026 Prompt Injection in the OWASP Top 10 for LLM Applications 2026. In addition that it is the number 1 risk that faces LLM as of September 2026, it is also the easiest one and doesnt have a certain format to be defended against completely.