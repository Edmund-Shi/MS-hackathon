from azure.kusto.data import KustoClient, KustoConnectionStringBuilder
from azure.kusto.data.exceptions import KustoServiceError
from azure.kusto.data.helpers import dataframe_from_result_table
from utils.config import microsoft_config


def sort_params(params_str):
    params = params_str.split(',')
    return ','.join(sorted(params))


def get_dataset():
    in_use = microsoft_config
    kcsb = KustoConnectionStringBuilder.with_aad_application_key_authentication(
        in_use['cluster'], in_use['client_id'], in_use["client_secret"], in_use["authority_id"])
    query = '''
    RawEventsAzCli
    | where EventTimestamp > ago(2h) and EventTimestamp < ago(1h)
    // Remove pre 2.0.28 telemetry as it has a different schema
    | where toint(split(tostring(parse_json(Properties).["context.default.vs.core.telemetryapi.productversion"]), '.')[2]) > 28 
    | where tostring(parse_json(Properties).["reserved.datamodel.action.result"]) == "Success"
    | sort by UserId
    | project UserId,command=parse_json(Properties)["context.default.azurecli.rawcommand"], 
    params = parse_json(Properties).["context.default.azurecli.params"],
    os_type = tostring(parse_json(Properties).["context.default.vs.core.os.type"]),
    source = tostring(parse_json(Properties).["context.default.azurecli.source"]),
    start_time_str= todatetime(parse_json(Properties).["context.default.azurecli.starttime"]),
    end_time_str = todatetime(parse_json(Properties).["context.default.azurecli.endtime"])
    | take 500
    '''
    client = KustoClient(kcsb)
    response = client.execute("AzureCli", query)

    dataset = {}
    for row in response.primary_results[0]:
        uid, command, params, os_type, source, begin, end = row
        params = sort_params(params)
        if uid not in dataset:
            dataset[uid] = [(command, params, os_type, source, begin, end)]
        else:
            last_cmd, last_params, *_ = dataset[uid][-1]
            last_params = sort_params(last_params)
            if last_cmd == command and last_params == params:
                continue  # duplicate
            dataset[uid].append(
                (command, params, os_type, source, begin, end))
    return dataset
# client.execute("Playground", "kb | take 10")
