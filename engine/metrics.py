from engine.fcfs import fcfs
from engine.sstf import sstf
from engine.scan import scan
from engine.cscan import cscan


def run_all(requests, head, disk_size=200, direction="right"):
    results = {
        "FCFS": fcfs(requests, head),
        "SSTF": sstf(requests, head),
        "SCAN": scan(requests, head, disk_size, direction),
        "C-SCAN": cscan(requests, head, disk_size, direction),
    }

    summary = {}
    for name, (order, total) in results.items():
        n = len(requests)
        summary[name] = {
            "order": order,
            "total_seek": total,
            "avg_seek": round(total / n, 2) if n else 0,
            "throughput": round(n / total, 4) if total else 0,
        }
    return summary


if __name__ == "__main__":
    reqs = [98, 183, 37, 122, 14, 124, 65, 67]
    summary = run_all(reqs, 53)
    for name, d in summary.items():
        print(f"{name:<7} total={d['total_seek']:<4} avg={d['avg_seek']:<6} throughput={d['throughput']}")