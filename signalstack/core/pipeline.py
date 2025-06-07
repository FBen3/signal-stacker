import importlib
from typing import List, Optional, Dict, Any


def run_pipeline(pipeline_list, initial_data=None, verbose=False):
    """Run a signal processing pipeline composed of
    various stages.

    Parameters
    ----------
    pipeline_list : List[str]
        List of motif names as strings.
    initial_data : dict | None 
        The input data dict to pass into the first motif.
    verbose : bool
        If True, print progress at each stage.

    Returns
    -------
        dict
    """
    data = initial_data

    for step in pipeline_list:
        # parse each step: group:name:arg1:arg2:...
        parts = step.strip().split(":")
        if len(parts) < 2:
            raise ValueError(f"Motif step '{step}' must be in 'group:name[:args]' format")

        group, name, *arg_strs = parts

        # dynamically import the group module
        try:
            module = importlib.import_module(f"signalstack.motifs.{group}")
        except ImportError as e:
            raise ImportError(f"Could not import motif group '{group}': {e}")

        # get the motif function
        try:
            motif_func = getattr(module, name)
        except AttributeError:
            raise ImportError(f"Motif '{name}' not found in group '{group}'")

        # prepare arguments: pass raw strings; motif functions handle conversion
        args = arg_strs

        if verbose:
            arg_display = f" with args {args}" if args else ""
            print(f"Running motif: {group}.{name}{arg_display}")

        # execute motif: allow signature data, *args
        result = motif_func(data, *args)

        # validate output format
        if not isinstance(result, dict) or "data" not in result:
            raise ValueError(f"Motif '{group}:{name}' returned invalid data format")

        data = result

    return data


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Run a signalstack processing pipeline.")
    parser.add_argument(
        "--pipeline", required=True,
        help="Pipeline string: e.g. 'load:mock.csv|filter:bandpass:20-450|feature:rms|plot'"
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Show each motif execution."
    )
    args = parser.parse_args()

    # build list of steps, splitting on '|' and stripping whitespace
    steps = [s.strip() for s in args.pipeline.split("|") if s.strip()]

    # run pipeline and ignore return or let last motif handle outputs
    final_data = run_pipeline(steps, initial_data=None, verbose=args.verbose)

    print("Pipeline complete.")
