from logging import CRITICAL, getLogger


def confirm_processing(method: str = "all") -> bool | None:
    while True:
        if method == "all":
            response = input(
                "Warning: Processing the entire asset tree could take a significant amount of time and may depend on your hardware specs.\n"
                "Do you want to proceed? (Yes/No): "
            )
        elif method == "many_threads":
            response = input(
                "Warning: Processing with many threads could take a significant amount of resources from your system and depends heavily on your hardware specs.\n"
                "Are you VERY SURE want to proceed? (Yes/No): "
            )
        response = response.strip().lower()  # Remove leading/trailing spaces and make it lowercase

        if response in ["yes", "y"]:
            return True
        elif response in ["no", "n"]:
            return False
        else:
            getLogger("OpLogger").log(CRITICAL, "Invalid response. Please enter Yes or No.")


def main_interface(db_options: list) -> list:
    print("Select a database filter from the following options:")  # noqa: T201
    for idx, option in enumerate(db_options, 1):
        print(f"{idx}. {option}")  # noqa: T201

    while True:
        try:
            db_choice = int(input("Enter your choice (number): "))
            if 1 <= db_choice <= len(db_options):
                db_filter = db_options[db_choice - 1]
                break
            else:
                getLogger("OpLogger").log(
                    CRITICAL,
                    f"Invalid choice. Please enter a number from the list. Between 1 and {len(db_options)} inclusive."
                    "\nOr press Ctrl+C to exit.",
                )
        except ValueError:
            print("Invalid input. Please enter a number.")  # noqa: T201

    max_workers = input("Enter the number of worker threads (default is 5): ")
    max_workers = int(max_workers) if max_workers.isdigit() else 5

    return [db_filter, max_workers]
