import secrets


def process_header(header):
    new_header = {}
    # both randomly generated without user info, as described in W3C spec field generation
    serv_trace_id = str(secrets.token_hex(16))
    serv_parent_id = str(secrets.token_hex(8))

    serv_sample_rate = "dc=0.2"
    serv_sample_parent = f'00-{serv_trace_id}-{serv_parent_id}-01'

    if not "traceparent" in header:
        new_header["traceparent"] = serv_sample_parent
        new_header["tracestate"] = serv_sample_rate

        return new_header

    elif not "tracestate" in header:
        new_header["traceparent"] = header["traceparent"]
        new_header["tracestate"] = serv_sample_rate

        return new_header

    ts = header["tracestate"].split(',')
    if not any("dc=0.2" in s for s in ts):
        new_ts = list(filter(lambda x: "dc=" not in x, ts))
        new_ts.insert(0, serv_sample_rate)
        new_header["traceparent"] = header["traceparent"]
        new_header["tracestate"] = ",".join(new_ts)
    return new_header


if __name__ == '__main__':
    input = [
        {"traceparent": "00-0af7651916cd43dd8448eb211c80319c-b9c7c989f97918e1-01",
         "tracestate": "congo=ucfJifl5GOE,rojo=00f067aa0ba902b7"},

        {"traceparent": "00-0af7651916cd43dd8448eb211c80319c-b9c7c989f97918e1-01",
         "tracestate": "dc=.2,congo=ucfJifl5GOE"},

        {"traceparent": "00-0af7651916cd43dd8448eb211c80319c-b9c7c989f97918e1-01",
         "tracestate": "congo=ucfJifl5GOE,dc=1"},

        {"tracestate": "congo=ucfJifl5GOE,dc=1"},

        {"traceparent": "00-0af7651916cd43dd8448eb211c80319c-b9c7c989f97918e1-01"},

        {}
    ]

    for header in input:
        print(process_header(header))
