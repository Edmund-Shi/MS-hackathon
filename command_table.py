class Command:
    def __init__(self, cmd, params_str):
        self.cmd = cmd
        params = sorted(params_str.split(','))
        self.params = params
        self.param_str = ' '.join(params)

    @staticmethod
    def parse_params(param_str):
        params = param_str.split(',')
        return sorted(params)


class CommandTable:
    def __init__(self):
        self._table = {}
        pass

    def update_table(self, dataset):
        '''update current command table'''
        for uid in dataset.keys():
            for item in dataset[uid]:
                cmd, param_str, *_ = item
                if cmd == "" and param_str == "":
                    continue  # empty command
                else:
                    pass
