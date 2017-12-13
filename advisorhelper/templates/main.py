import argparse

from algo.my_algorithm import Algorithm
from algorithm_manager import AlgorithmManager


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("study_id", type=int)
    parser.add_argument("study_config", type=str)
    parser.add_argument("X_train", type=str)
    parser.add_argument("y_train", type=str)
    parser.add_argument("host", type=str)
    parser.add_argument("port", type=int)
    parser.add_argument("url", type=str)
    args = parser.parse_args()

    am = AlgorithmManager(
        study_id=args.study_id,
        study_config=args.study_config,
        X_train=args.X_train,
        y_train=args.y_train,
        host=args.host,
        port=args.port,
        url=args.url,
    )

    alg = Algorithm(
        lowerbound=am.lower_bound,
        upperbound=am.upper_bound,
    )
    x_next = alg.get_suggestion()
    # x_next = x_next.squeeze()

    am.send_result(x_next)

if __name__ == "__main__":
    run()
