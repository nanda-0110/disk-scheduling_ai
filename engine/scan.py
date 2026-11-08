def scan(requests, head, disk_size=200, direction="right"):
    left = sorted(r for r in requests if r < head)
    right = sorted(r for r in requests if r >= head)

    if direction == "right":
        order = right + left[::-1]
        path = right + [disk_size - 1] + left[::-1]
    else:
        order = left[::-1] + right
        path = left[::-1] + [0] + right

    current = head
    total_seek = 0
    for track in path:
        total_seek += abs(current - track)
        current = track

    return order, total_seek


if __name__ == "__main__":
    reqs = [98, 183, 37, 122, 14, 124, 65, 67]
    print(scan(reqs, 53, 200, "right"))
    print(scan(reqs, 53, 200, "left"))