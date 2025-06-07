import argparse
from signalstack.core.pipeline import run_pipeline


def main():
    parser = argparse.ArgumentParser(description="Run a signalstack processing pipeline.")
    parser.add_argument(
        "--pipeline", required=True,
        help="Pipeline string: e.g. 'load:load_csv:mock.csv|filter:bandpass:20-450|feature:rms|plot'"
    )
    parser.add_argument(
        "--verbose", action="store_true",
        help="Print each step as it runs"
    )

    args = parser.parse_args()

    # split pipeline string into individual steps
    steps = [s.strip() for s in args.pipeline.split("|") if s.strip()]

    # run the pipeline
    result = run_pipeline(steps, initial_data=None, verbose=args.verbose)

    print("\n Pipeline complete. Final data shape:", result["data"].shape)


if __name__ == "__main__":
    main()
