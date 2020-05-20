import time

users = {}

UNKNOWN = 'UNKNOWN'

# After 30 seconds without a checkin ping, a user's status will be discarded.
ACTIVE_SECONDS = 30

def _connected_time_ok(last_conn_time):
    return (time.time() - last_conn_time) <= ACTIVE_SECONDS

class User:
    name = None
    connected_to = None
    last_conn_time = None
    status = None

    def get_status(self):
        if _connected_time_ok(self.last_conn_time):
            return self.status
        return UNKNOWN

    def __str__(self):
        return "User {}".format(self.name)

# Finds a user in the global users dictionary
def find_user(name):
    global users
    return users[name] if name in users else None

# Return the names of all users which we've been connected to in the last 30 seconds
def all_active_users():
    global users
    names = set()
    for u in users:
        if _connected_time_ok(users[u].last_conn_time):
            names.add(u)
    return names

# Updates the connected users for a user and the last connected time
def add_update_user(name, conn_names):
    global users
    if name not in users:
        users[name] = User()
        users[name].name = name
    users[name].connected_to = conn_names
    users[name].last_conn_time = time.time()

# Initializes a user
def init_user(name, conn_names):
    add_update_user(name, conn_names)
    

def _statuses_for_users(users):
    statuses = {}
    for c in users:
        cusr = find_user(c)
        if cusr and _connected_time_ok(cusr.last_conn_time):
            statuses[c] = cusr.status
        else:
            statuses[c] = UNKNOWN
    return statuses

# Returns the data sent to the user on an update request
def user_response(name):
    usr = find_user(name)
    statuses = _statuses_for_users(usr.connected_to)
    return {'statuses': statuses, 'self_status': usr.get_status(), 'msg_type': 'local'}

# Returns all statuses for active users. This is broadcasted to all users.
def all_statuses():
    return {'statuses': _statuses_for_users(all_active_users()), 'msg_type': 'global'}

# Sets the status of a user
def user_set_status(name, status):
    usr = find_user(name)
    if not usr:
        init_user(name, None)
        usr = find_user(name)
    usr.status = status
    usr.last_conn_time = time.time()

# Updates the last connection time
def user_checkin(name):
    usr = find_user(name)

    new_time = time.time()
    old_time = usr.last_conn_time
    
    usr.last_conn_time = new_time
    return new_time - old_time