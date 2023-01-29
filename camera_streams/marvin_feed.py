import redis
import datetime


class MarvinFeed:
    """ Class handling marvin sensor feeds via Redis streams. Use consumer groups to allow
    individual data streams to be shared between multiple different types of consumers.

    NOTE: This is blocking, and handles one message at a time for a single feed and consumer group
    """

    # ID of the last message returned, so that it can be acknowledged on the following call to next()
    current_msg_id = ">"

    def __init__(self, host="127.0.0.1", port=6379, stream="default_stream",
                 group="default_group", consumer_name="unique ID here"):
        self.host = host
        self.port = port
        self.client = redis.StrictRedis(host=host, port=port, db=0)
        self.stream = stream
        self.group = group
        self.consumer_name = consumer_name

        try:
            self.client.xgroup_create(self.stream, self.group, mkstream=True)
        except Exception:
            # TODO: Doesn't appear to be an appropriate exception?
            print(f"Group {self.group} already exists for stream {self.stream}, skipping creation")

    def __enter__(self):
        return self

    def __exit__(self):
        self.client.close()

    def push(self, msg):
        self.client.xadd(self.stream,
                         {"data": msg, "time": datetime.datetime.now().isoformat()},
                         id="*", maxlen=500, approximate=True)

    def next(self):
        """ Marks the current message as complete, blocks until the next message arrives """
        if self.current_msg_id != ">":
            ack_count = self.client.xack(self.stream, self.group, self.current_msg_id)

        new_msgs = self.client.xreadgroup(self.group,
                                          self.consumer_name,
                                          {self.stream: ">"},
                                          block=1000000000,
                                          count=1)
        self.current_msg_id = new_msgs[0][1][0][0]
        payload = new_msgs[0][1][0][1]
        return payload

    def pending(self):
        """ Fetches all the pending messages for the group """
        pending_summary = self.client.xpending(self.stream, self.group)
        return pending_summary
