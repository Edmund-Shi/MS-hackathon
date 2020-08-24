import access_data
from command_table import CommandTable
from cosmos_client import MyCosmosClient


def print_cmd(nx_cmd):
    cmd, params, confidence = nx_cmd
    print("{:.2f}% people use run this command: {} {}".format(confidence*100, cmd, ' '.join(params.split(','))))


def test_cmd(cmd_table, cmd, params):
    print("After run {} {}".format(cmd, params))
    print_cmd(cmd_table.get_next_command(cmd, params))


def main():
    db_client = MyCosmosClient()
    cmd_table = CommandTable()
    records = db_client.query_all_items()
    cmd_table.load_from_cosmos(records)
    dataset = access_data.get_dataset()
    cmd_table.update_table(dataset)
    cosmos_data = cmd_table.dump_table()

    # for i in range(min(10, len(cosmos_data))):
    #     db_client.insert(cosmos_data[i])


if __name__ == "__main__":
    main()
