from typing import Any, Union


def format_error(msg: Any) -> str:
    return f"\033[31m{msg}\033[0m"


def format_success(msg: Any) -> str:
    return f"\033[32m{msg}\033[0m"


def format_warning(msg: Any) -> str:
    return f"\033[33m{msg}\033[0m"


def log_message(
    msg: Any,
    log_type: Union["success", "error", "warning"] = None,
    to_return=False,
):
    if log_type == "error":
        formatted_msg = format_error(msg)
    elif log_type == "success":
        formatted_msg = format_success(msg)
    elif log_type == "warning":
        formatted_msg = format_warning(msg)
    else:
        formatted_msg = str(msg)

    if to_return:
        return formatted_msg
    print(formatted_msg)


if __name__ == "__main__":
    log_message("This is an error message.", log_type="error")
    log_message("This is a success message.", log_type="success")
    log_message("This is a warning message.", log_type="warning")

    error_msg = log_message(
        "This is an error message.", log_type="error", to_return=True
    )
    success_msg = log_message(
        "This is a success message.", log_type="success", to_return=True
    )
    warning_msg = log_message(
        "This is a warning message.", log_type="warning", to_return=True
    )

    log_message(error_msg, log_type="stdout")
    log_message(success_msg, log_type="stdout")
    log_message(warning_msg, log_type="stdout")
