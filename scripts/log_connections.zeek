module SaveConn;

@load base/protocols/conn

export {
    # Append the value LOG_CONN to the Log::ID enumerable.
    redef enum Log::ID += { LOG_CONN };

    # enum for state of closed connection 
    type CONN_STATE: enum { REMOVED, TIMEOUT };

    # Define a new type called ConnInfo that contains the relevant infos of a connection.
    type ConnInfo: record {
        ts:       time        &log;
        uid:      string      &log;
        socket:   conn_id     &log;
        services: string      &log;  
        state:    CONN_STATE  &log;      
    };

    # type for logging grouping info for the various connections
    type ConnInfoToLog: record {
        orig:        addr     &log;
        resp:        addr     &log;
        connection:  ConnInfo &log;
        #orig_port:   port     &log;
        #resp_port:   port     &log;
        #ts:          time     &log;
        #uid:         string   &log;
        #services:    string   &log;
        #state:       string   &log;
    };

    # table of all of the connections
    global connections: set[ConnInfo];
    global run: count = 0;
}

#function print_conn(c: ConnInfo) {
#    local stateOut: string;
#
#    switch c$state {
#        case REMOVED:
#            stateOut = "removed";
#            break;
#        case TIMEOUT:
#            stateOut = "timeout";
#            break;
#    }
#
#    print fmt("Connection   %s started at time  %10.2e with id  %s from %10s:%10s to    %10s:%10s on service:   %s",
#        stateOut,
#        c$ts, 
#        c$uid,
#        c$socket$orig_h,
#        c$socket$orig_p,
#        c$socket$resp_h,
#        c$socket$resp_p,
#        c$services
#        );
#}

# creating the logging stream
event zeek_init() {
    Log::create_stream(LOG_CONN, [$columns=ConnInfoToLog, $path="../logs/connections"]);
}

# function that convert the connection into a ConnInfo, 
# effectively removing the irrelevant fields
function conn_to_ConnInfo(c: connection, state: CONN_STATE): ConnInfo {

    local services = "";
    for (serv in c$service) {
        services += serv + ", ";
    }

    return [
        $ts = c$start_time, 
        $uid = c$uid,
        $socket = c$id,
        $services = services,
        $state = state
    ];
}

event connection_timeout(c: connection) {
    # converting
    local conn = conn_to_ConnInfo(c, TIMEOUT);

    # logging on the console the connection
    #print_conn(conn);
    add connections[conn];
}

event connection_state_remove(c: connection) {
    # converting
    local conn = conn_to_ConnInfo(c, REMOVED);

    add connections[conn];
}

event zeek_done() {
    local i: count = 0;
    local conn_visited: table[addr, addr] of bool;
    local connections_grouped: table[addr, addr] of set[ConnInfo]; 

    for (c in connections) {
        conn_visited[c$socket$orig_h, c$socket$resp_h] = F;
    }

    for (c in connections) {
        if (!conn_visited[c$socket$orig_h, c$socket$resp_h]) {
            connections_grouped[c$socket$orig_h, c$socket$resp_h] = set();
            conn_visited[c$socket$orig_h, c$socket$resp_h] = T;
        }
        add connections_grouped[c$socket$orig_h, c$socket$resp_h][c];
    }

    for ( [orig, resp], set_con in connections_grouped ) {
        local output: string = "";

        print "logging: ";
        print fmt(" %s to %s: ", cat(orig), cat(resp));

        for (c in set_con) {
            print "    " + cat(c) + ",";
        }
        print "]";

        for (c in set_con) {

            Log::write( 
                SaveConn::LOG_CONN, 
                [ 
                    $orig = orig,
                    $resp = resp,
                    $connection = c
                    #$orig_port = c$socket$orig_p,
                    #$resp_port = c$socket$resp_p,
                    #$ts = c$ts,
                    #$uid = c$uid,
                    #$services = c$services,
                    #$state = stateOut
                ]
            );
        }
    }
}
