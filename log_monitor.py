import sys

# The SegmentTree class to store the logs in the segment tree (min, max, sum, count)
class SegmentTree:
    def __init__(self, size):
        # Initialize the segment tree with given size
        self.size = 4 * size + 1
        self.min_tree = [float('inf')] * self.size  # Tree for minimum values
        self.max_tree = [float('-inf')] * self.size # Tree for maximum values
        self.sum_tree = [0.0] * self.size           # Tree for sum of values
        self.count_tree = [0] * self.size          # Tree for count of values

    def updateST(self, node, start, end, idx, value):
        if start == end:
            self.min_tree[node] = min(self.min_tree[node], value)
            self.max_tree[node] = max(self.max_tree[node], value)
            self.sum_tree[node] += value
            self.count_tree[node] += 1
            return
        
        mid = start + (end - start) // 2
        if idx <= mid: # update left part of the segment tree (idx is in the left part)
            self.updateST(2 * node + 1, start, mid, idx, value)
        else:
            self.updateST(2 * node + 2, mid + 1, end, idx, value)

        # Update parent nodes
        self.min_tree[node] = min(self.min_tree[2 * node + 1], self.min_tree[2 * node + 2])
        self.max_tree[node] = max(self.max_tree[2 * node + 1], self.max_tree[2 * node + 2])
        self.sum_tree[node] = self.sum_tree[2 * node + 1] + self.sum_tree[2 * node + 2]
        self.count_tree[node] = self.count_tree[2 * node + 1] + self.count_tree[2 * node + 2]

    def update(self, idx, value):
        # Update the segment tree at position idx with the given value
        self.updateST(0, 0, (self.size // 4) - 1, idx, value)

    def queryST(self, node, start, end, left, right):
        # no overlap
        if start > right or end < left:
            return (float('inf'), float('-inf'), 0.0, 0.0) # min, max, sum, count
        # complete overlap
        if left <= start and end <= right:
            return (self.min_tree[node], self.max_tree[node], self.sum_tree[node], self.count_tree[node])
        
        # partial overlap case; split
        mid = start + (end - start) // 2
        left_min, left_max, left_sum, left_count = self.queryST(2 * node + 1, start, mid, left, right)
        right_min, right_max, right_sum, right_count = self.queryST(2 * node + 2, mid + 1, end, left, right)

        min_val = min(left_min, right_min)
        max_val = max(left_max, right_max)
        sum_val = left_sum + right_sum
        count = left_count + right_count
        return (min_val, max_val, sum_val, count)
    
    def query(self, left, right):
        # Query the segment tree for range [left, right]
        return self.queryST(0, 0, (self.size // 4) - 1, left, right)

        
# The LogMonitor class to monitor the log
class LogMonitor:
    def __init__(self, nodes, log_types, timestamp_to_idx) -> None:
        self.logs = [] # List to store logs log[0] = timestamp, log[1] = type, log[2] = severity
        self.size = nodes
        # Create a global segment tree and segment tree for each log type
        self.global_tree = SegmentTree(nodes) # Global segment tree
        self.type_trees = {log_type: SegmentTree(nodes) for log_type in log_types}
        self.timestamp_map = timestamp_to_idx

    # set the precision of the result upto 10e-6
    def set_precision(self, value):
        format_string = '{:.8g}' if abs(value) >= 1e-6 else '{}'
        formatted_res = format_string.format(value)
        return formatted_res

    # handle type 1 command
    def add_log(self, log):
        # Add a new log to the monitoring system
        timestamp, log_type, severity = log
        timestamp_idx = self.timestamp_map[timestamp]
        self.logs.append((timestamp_idx, log_type, severity))
        self.global_tree.update(timestamp_idx, severity)
        self.type_trees[log_type].update(timestamp_idx, severity)
        return "No output"

    # handle type 2 command
    def get_details_type2(self, log_type):
        # get the details of the log type
        details = self.type_trees[log_type].query(0, self.size - 1)
        _min, _max, _sum, count = details
        mean = _sum / count if count > 0 else 0.0
        _min = _min if _min != float('inf') else 0.0
        _max = _max if _max != float('-inf') else 0.0

        # precision upto 10e-6
        result = "Min: {}, Max: {}, Mean: {}".format(self.set_precision(_min), self.set_precision(_max), self.set_precision(mean))
        return result
    
    # handle type 3 command
    def get_details_type3(self, command, timestamp):
        deatils = None
        if command == "BEFORE":
            details = self.global_tree.query(0, self.timestamp_map[timestamp] - 1)
        elif command == "AFTER":
            details = self.global_tree.query(self.timestamp_map[timestamp] + 1, self.size - 1)
        
        _min, _max, _sum, count = details
        mean = _sum / count if count > 0 else 0.0
        _min = _min if _min != float('inf') else 0.0
        _max = _max if _max != float('-inf') else 0.0

        # precision upto 10e-6
        result = "Min: {}, Max: {}, Mean: {}".format(self.set_precision(_min), self.set_precision(_max), self.set_precision(mean))
        return result

    # handle type 4 command
    def get_details_type4(self, command, log_type, timestamp):
        details = None
        if command == "BEFORE":
            details = self.type_trees[log_type].query(0, self.timestamp_map[timestamp] - 1)
        elif command == "AFTER":
            details = self.type_trees[log_type].query(self.timestamp_map[timestamp] + 1, self.size - 1)
        
        _min, _max, _sum, count = details
        mean = _sum / count if count > 0 else 0.0
        _min = _min if _min != float('inf') else 0.0
        _max = _max if _max != float('-inf') else 0.0

        # precision upto 10e-6
        result = "Min: {}, Max: {}, Mean: {}".format(self.set_precision(_min), self.set_precision(_max), self.set_precision(mean))
        return result
    
# write (append) to a file
def write_to_file(result, file_name='./output.txt'):
    # write the result to the output file
    with open(file_name, 'a') as file:
        file.write(f"{result}\n")  

# get the statistics of the log entries (unique time_stamps and log_types)
def preprocess_input(commands):
    # check the number of unique time stamps in the input file (time stamps only occur in command type 1, 3, and 4)
    time_stamps = set()
    # Also check the unique log types (log types only occur in type 1, 2, and 4)
    log_types = set()

    for line in commands: # break by new line
        line = line.strip()

        # For time stamps
        if line.startswith('1'):
            parts = line.split(";")
            time_stamps.add(parts[0].split(" ")[1])
        elif line.startswith('3'):
            parts = line.split(" ")
            time_stamps.add(parts[2])
        elif line.startswith('4'):
            parts = line.split(" ")
            time_stamps.add(parts[3])

        # For log types
        if line.startswith('1'):
            parts = line.split(";")
            log_types.add(parts[1])
        elif line.startswith('2'):
            parts = line.split(" ")
            log_types.add(parts[1])
        elif line.startswith('4'):
            parts = line.split(" ")
            log_types.add(parts[2])
    
    # sort the time stamps
    time_stamps = sorted(list(time_stamps))
    timestamp_to_idx = {timestamp: idx for idx, timestamp in enumerate(time_stamps)}
    return time_stamps, log_types, timestamp_to_idx

def main(input_file='./input.txt', output_file='./output.txt'):
    # read the contents form the input file
    with open(input_file, 'r') as file:
        commands = file.readlines()

    # preprocess the input
    time_stamps, log_types, timestamp_to_idx = preprocess_input(commands)

    # Create a log monitor object
    log_monitor = LogMonitor(len(time_stamps), log_types, timestamp_to_idx)

    # finally process the commands
    for line in commands:
        line = line.strip()

        # if the command is of type 1 : <timestamp>;<log_type>;<severity>
        if line.startswith('1'):
            parts = line.split(";")
            timestamp, log_type, severity = parts[0].split(" ")[1], parts[1], float(parts[2])
            result = log_monitor.add_log((timestamp, log_type, severity))
            write_to_file(result, output_file)
        
        # if the command is of type 2 : <log_type>
        elif line.startswith('2'):
            parts = line.split(" ")
            log_type = parts[1]
            result = log_monitor.get_details_type2(log_type)
            write_to_file(result, output_file)

        # if the command is of type 3 : <BEFORE/AFTER> <timestamp>
        elif line.startswith('3'):
            parts = line.split(" ")
            command, timestamp = parts[1], parts[2]
            result = log_monitor.get_details_type3(command, timestamp)
            write_to_file(result, output_file)

        # if the command is of type 4 : <BEFORE/AFTER> <log_type> <timestamp>
        elif line.startswith('4'):
            parts = line.split(" ")
            command, log_type, timestamp = parts[1], parts[2], parts[3]
            result = log_monitor.get_details_type4(command, log_type, timestamp)
            write_to_file(result, output_file)

if __name__ == "__main__":
    main()
    # print("Successfully executed the commands! Check the output file for the results.")