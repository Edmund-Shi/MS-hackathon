import mock_data
from command_table import CommandTable

def print_cmd(nx_cmd):
    cmd, params, confidence = nx_cmd
    print("{}% people use run this command: {} {}".format(confidence*100, cmd, ' '.join(params.split(','))))


def main():
    dataset = mock_data.get_dataset()
    cmd_table = CommandTable()
    cmd_table.update_table(dataset)
    nx_cmd = cmd_table.get_next_command(
        "account get-access-token", "-o,--resource")
    nx_cmd = cmd_table.get_next_command("vm create", "")
    print_cmd(nx_cmd)
    print_cmd(cmd_table.get_next_command("webapp create", ""))


if __name__ == "__main__":
    main()
