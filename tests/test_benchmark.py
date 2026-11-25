from app.redis_storage import RedisStorage
from concurrent.futures import ThreadPoolExecutor
import time
import statistics

storage = RedisStorage()

def wrapper(ip, submitted_at):
    start = time.perf_counter()
    result = storage.allow_request(ip)
    end = time.perf_counter()

    service_time = end - start
    total_time = end - submitted_at

    return result, service_time, total_time

def test_benchmark():
    requests_per_ip = 10
    max_workers = 10
    client_ips = []
    for i in range(1,101):
        client_ip = f"192.169.1.{i}"
        client_ips.append(client_ip)
    storage.redis.delete(*(f"rate_limit:{ip}" for ip in client_ips))
    futures = []
    start_time = time.perf_counter()
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for ip in client_ips:
            for i in range(requests_per_ip):
                submitted_at = time.perf_counter()
                future = executor.submit(wrapper,ip,submitted_at)
                futures.append(future)

    results, service_times, total_times = zip(*(future.result() for future in futures))
    end_time = time.perf_counter()
    elapsed = end_time - start_time
    print(f"Total execution time: {elapsed:.4f} seconds")

    total_requests = len(client_ips) * requests_per_ip
    throughput = total_requests / elapsed
    print(f"Total throughput: {throughput:.2f} requests/sec")

    results = list(results)
    latencies = list(total_times)
    service_times = list(service_times)

    average_service_ms = (sum(service_times) / len(service_times)) * 1000
    print(f"Average service time: {average_service_ms:.3f} ms")
    average_latency_ms = (sum(latencies) / len(latencies)) * 1000
    print(f"Average latency: {average_latency_ms:.3f} ms")

    p95 = statistics.quantiles(latencies, n=100)[94]
    p95_ms = p95 * 1000
    print(f"P95 latency: {p95_ms:.3f} ms")

    p99 = statistics.quantiles(latencies,n=100)[98]
    p99_ms = p99 * 1000
    print(f"P99 latency: {p99_ms:.3f} ms")

    p95_service = statistics.quantiles(service_times, n=100)[94] * 1000
    p99_service = statistics.quantiles(service_times, n=100)[98] * 1000

    print(f"P95 service time: {p95_service:.3f} ms")
    print(f"P99 service time: {p99_service:.3f} ms")

    assert sum(results) == 200
    assert results.count(False) == 800
            