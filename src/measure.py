import argparse
import time
from src import algos
from src.main import generate_netlist


def measure():
    nets = [10, 25, 50, 100, 200, 400, 800]
    print("n_nets, left_edge_time, proposed_algorithm_time")
    for n in nets:
        args = argparse.Namespace(
            seed=0,
            n_nets=n,
            scenario=1,
            gap_width=None,
            gap_interval=10,
        )
        netlist = generate_netlist(args)

        le_start = time.perf_counter_ns()
        _ = algos.left_edge(netlist, args)
        le_end = time.perf_counter_ns()

        pa_start = time.perf_counter_ns()
        _ = algos.proposed_algorithm(netlist, args)
        pa_end = time.perf_counter_ns()

        print(f"{n}, {le_end - le_start}, {pa_end - pa_start}")


if __name__ == "__main__":
    measure()
