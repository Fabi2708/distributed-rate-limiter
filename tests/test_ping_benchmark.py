import time
import statistics
from concurrent.futures import ThreadPoolExecutor
from app.redis_client import redis_client


def run_ping_benchmark(max_workers):
    total_requests = 1000
    futures = []

    def wrapper(submitted_at):
        start = time.perf_counter()
        redis_client.ping()
        end = time.perf_counter()

        service_time = end - start
        total_time = end - submitted_at

        return service_time, total_time

    start_time = time.perf_counter()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for _ in range(total_requests):
            submitted_at = time.perf_counter()
            future = executor.submit(wrapper, submitted_at)
            futures.append(future)

    service_times, total_times = zip(
        *(future.result() for future in futures)
    )

    elapsed = time.perf_counter() - start_time

    print(f"\nWorkers: {max_workers}")
    print(f"Throughput: {total_requests / elapsed:.2f} requests/sec")
    print(f"Average service time: {statistics.mean(service_times) * 1000:.3f} ms")
    print(f"Average latency: {statistics.mean(total_times) * 1000:.3f} ms")
    print(f"P95 latency: {statistics.quantiles(total_times, n=100)[94] * 1000:.3f} ms")
    print(f"P99 latency: {statistics.quantiles(total_times, n=100)[98] * 1000:.3f} ms")


if __name__ == "__main__":
    for workers in [1, 2, 5, 10]:
        for _ in range(4):
            run_ping_benchmark(workers)
