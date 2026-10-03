# LLM-API LAB

A small Python project that uses the OpenAI SDK to send prompts to an OpenAI model and compare responses at different temperature values.

# What it does

- Sends a system instruction and user prompt to an OpenAI model.
- Runs the same prompt with different temperature values.
- Prints the model's responses.
- Displays token usage.

# Setup

Create a .env file in the project folder:
OPENAI_API_KEY=your_api_key_here

# Run 

```
uv run main.py
```

# Output Example

```
=== Temperature 0.2 ===
An SDK, or Software Development Kit, is a collection of tools, libraries, documentation, and code samples that developers use to create applications for a specific platform or framework. It typically includes APIs, debuggers, and emulators to streamline the development process. By providing these resources, an SDK helps developers build, test, and deploy software more efficiently and effectively.

Tokens used: 101

=== Temperature 1.0 ===
An SDK, or Software Development Kit, is a collection of tools, libraries, and documentation that developers use to build applications for a specific platform, framework, or service. It typically includes code samples, APIs, and utilities to simplify and speed up the development process. By using an SDK, developers can more easily integrate specific features or services into their applications.

Tokens used: 99
```

