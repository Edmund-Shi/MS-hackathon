class Command:
    class NextItem:
        def __init__(self, cmd):
            self.cmd = cmd
            self.counter = {}

        def update(self, param_str):
            self.counter[param_str] = self.counter.get(param_str, 0) + 1

    def __init__(self, cmd):
        self.cmd = cmd
        self.total_cnt = 0  # all related command count
        self.next_cmd = {}

    def update(self, next_record):
        '''update next record'''
        nx_cmd, nx_param, *_ = next_record
        nx_param = self.sort_params_str(nx_param)
        if nx_cmd not in self.next_cmd:
            self.next_cmd[nx_cmd] = self.NextItem(nx_cmd)
        self.next_cmd[nx_cmd].update(nx_param)
        self.total_cnt += 1

    def get_next(self, param_str):
        if param_str in self.next_cmd:
            possible_actions = []
            for nx_cmd, nx_item in self.next_cmd[param_str].items():
                for nx_param, counter in nx_item.counter.items():
                    possible_actions.append((counter, nx_cmd, nx_param))
            possible_actions = sorted(
                possible_actions, key=lambda x: x[0], reverse=True)
            return possible_actions[0][1], possible_actions[0][2], possible_actions[0][0] / self.total_cnt
        else:
            possible_actions = []
            for param_str in self.next_cmd.keys():
                for nx_cmd, nx_item in self.next_cmd[param_str].items():
                    for nx_param, counter in nx_item.counter.items():
                        possible_actions.append((counter, nx_cmd, nx_param))
            possible_actions = sorted(
                possible_actions, key=lambda x: x[0], reverse=True)
            return possible_actions[0][1], possible_actions[0][2], possible_actions[0][0] / self.total_cnt

    def analyze_params(self):
        all_cmds = set()
        cnt = 0
        for params in self.next_cmd.keys():
            all_cmds.add(self.get_next(params))
            cnt += len(self.next_cmd[params])
        return len(all_cmds), cnt

    def to_cosmos(self):
        '''Dump current item to Cosmos format'''
        nx_cmd = []
        for cmd in self.next_cmd.values():
            for param_str, cnt in cmd.counter.items():
                item = {
                    'command': cmd.cmd,
                    'arguments': param_str.split(','),
                    'count': cnt,
                }
                nx_cmd.append(item)

        db_item = {
            'id': self.cmd,
            'command': self.cmd,
            'totalCount': self.total_cnt,
            'nextCommand': nx_cmd,
        }
        return db_item

    @staticmethod
    def parse_params(param_str):
        params = param_str.split(',')
        return sorted(params)

    @staticmethod
    def sort_params_str(param_str):
        return ','.join(Command.parse_params(param_str))


class CommandTable:
    def __init__(self):
        self._table = {}
        pass

    def update_table(self, dataset):
        '''update current command table'''
        for uid in dataset.keys():
            for i in range(len(dataset[uid]) - 1):
                cmd, *_ = dataset[uid][i]
                if cmd == "":
                    continue  # empty command
                elif cmd not in self._table:
                    self._table[cmd] = Command(cmd)
                # update with next command
                self._table[cmd].update(dataset[uid][i+1])

    def get_next_command(self, cmd, params):
        if cmd not in self._table:
            raise Exception("Command not found")  # TODO(shiyue) fall back solution
        next_cmd = self._table[cmd].get_next(params)
        return next_cmd

    def dump_table(self):
        '''dump command table to cosmos db format'''
        ret = []
        for item in self._table.values():
            ret.append(item.to_cosmos())
        return ret

    def analyze_params(self):
        dist = 0
        cnt = 0
        for cmd in self._table.keys():
            x, y = self._table[cmd].analyze_params()
            dist += x
            cnt += y
        return dist, cnt, len(self._table.keys())
