def fcfs(requests, head):
    current = head
    total_seek = 0

    for r in requests:
        total_seek += abs(current - r)
        current = r

    return requests, total_seek


if __name__ == "__main__":
    print(fcfs([98, 183, 37, 122, 14, 124, 65, 67], 53))