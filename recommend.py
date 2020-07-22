import mock_data
from command_table import CommandTable


def main():
    dataset = mock_data.get_dataset()
    cmd_table = CommandTable()
    cmd_table.update_table(dataset)
    nx_cmd = cmd_table.get_next_command(
        "account get-access-token", "-o,--resource")
    nx_cmd = cmd_table.get_next_command("vm create", "")
    print(nx_cmd)


if __name__ == "__main__":
    main()
