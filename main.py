#!/usr/bin/env python3
"""Kisan Dost — CLI entry point for the agricultural agent."""

from __future__ import annotations

import sys

from kisan_dost.agent import KisanDostAgent


def main() -> None:
    print("=" * 50)
    print("  Kisan Dost — Agricultural Advisor")
    print("  Type 'quit' or 'exit' to leave")
    print("=" * 50)

    try:
        agent = KisanDostAgent()
        print(f"  Model: {agent.model}")
    except ValueError as e:
        print(f"\nSetup error: {e}")
        print("1. Copy .env.example to .env")
        print("2. Add your GEMINI_API_KEY from https://aistudio.google.com/apikey")
        sys.exit(1)

    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nAllah ka karam — Kisan Dost alvida!")
            break

        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "bye", "alvida"):
            print("\nAllah ka karam — Kisan Dost alvida!")
            break

        try:
            reply = agent.chat(user_input)
            print(f"\nKisan Dost: {reply}")
        except Exception as e:
            err = str(e)
            print(f"\nError: {e}")
            if "429" in err or "RESOURCE_EXHAUSTED" in err:
                print("Free quota for this Gemini model is finished for today.")
                print("Wait, or set GEMINI_MODEL=gemini-2.0-flash in .env")
            else:
                print("Check your API key and internet connection.")


if __name__ == "__main__":
    main()
