def filter(input_paths):
    filtered_input_paths = []
    print(input_paths)
    for path in input_paths:
        if "comedy" in path:
            continue
        filtered_input_paths.append(path)
    print(filtered_input_paths)
    return filtered_input_paths
            