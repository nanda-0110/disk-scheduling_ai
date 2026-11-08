def sstf(requests, head):
    remaining = list(requests)
    order = []
    current = head
    total_seek = 0

    while remaining:
        nearest = min(remaining, key=lambda r: abs(current - r))
        total_seek += abs(current - nearest)
        order.append(nearest)
        remaining.remove(nearest)
        current = nearest

    return order, total_seek


if __name__ == "__main__":
    print(sstf([98, 183, 37, 122, 14, 124, 65, 67], 53))