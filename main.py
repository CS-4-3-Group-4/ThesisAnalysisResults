import questionary
from questionary import Style
import sys
import percentage_change
import significance

# Custom style with colors
custom_style = Style(
    [
        ("qmark", "fg:#673ab7 bold"),  # Purple question mark
        ("question", "bold"),  # Bold question text
        ("answer", "bold"),  # Bold answer text
        ("pointer", "fg:#673ab7 bold"),  # Purple pointer (>)
        ("highlighted", "fg:#673ab7 bold"),  # Purple highlighted option
        ("selected", "fg:#cc5454"),  # Light red selected
        ("separator", "fg:#cc5454"),  # Light red separator
        ("instruction", ""),  # Default instruction
        ("text", ""),  # Default text
    ]
)


def main():
    """Main CLI."""
    print("\n🔬 FA vs EFA Analysis Tool\n")

    while True:
        try:
            # First, select category
            category = questionary.select(
                "Select analysis category:",
                choices=[
                    "📊 Percentage Change Analysis (SOP 1 & 2)",
                    "📈 Statistical Significance Testing (SOP 3 & 4)",
                    questionary.Separator(),
                    "❌ Exit",
                ],
                style=custom_style,
            ).ask()

            if category is None or category == "❌ Exit":
                print("\n👋 Goodbye!\n")
                sys.exit(0)

            # Then, select specific analysis based on category
            if "Percentage Change" in category:
                run_percentage_change_menu()
            elif "Statistical Significance" in category:
                run_significance_menu()

            continue_choice = questionary.confirm(
                "Return to main menu?", default=True, style=custom_style
            ).ask()

            if not continue_choice:
                print("\n👋 Goodbye!\n")
                sys.exit(0)

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!\n")
            sys.exit(0)


def run_percentage_change_menu():
    """Percentage change analysis menu (SOP 1 & 2)."""
    choice = questionary.select(
        "Select percentage change analysis:",
        choices=[
            "📊 Fitness Score % Change (SOP 1)",
            "⏱️  Execution Time % Change (SOP 2)",
            "💾 Memory Usage % Change (SOP 2)",
            "🎯 Multi-Objective Analysis",
            questionary.Separator(),
            "← Back to Main Menu",
        ],
        style=custom_style,
    ).ask()

    if choice is None or "Back" in choice:
        return

    print(f"\n✨ Running {choice}...")

    if "Fitness" in choice:
        percentage_change.fitness.run()
    elif "Time" in choice:
        percentage_change.time.run()
    elif "Memory" in choice:
        percentage_change.memory.run()
    elif "Objective" in choice:
        percentage_change.objectives.run()


def run_significance_menu():
    """Statistical significance menu (SOP 3 & 4)."""
    choice = questionary.select(
        "Select significance test:",
        choices=[
            "📈 Fitness Score Significance Test (SOP 3)",
            "⏱️  Execution Time Significance Test (SOP 4)",
            "💾 Memory Usage Significance Test (SOP 4)",
            questionary.Separator(),
            "← Back to Main Menu",
        ],
        style=custom_style,
    ).ask()

    if choice is None or "Back" in choice:
        return

    print(f"\n✨ Running {choice}...")

    if "Fitness" in choice:
        significance.fitness.run()
    elif "Time" in choice:
        significance.time.run()
    elif "Memory" in choice:
        significance.memory.run()


if __name__ == "__main__":
    main()
