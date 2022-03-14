def compare_value(observed, expected, element: str = None):
    result = []
    if observed != expected:
        result.append(f'Expected state is different than observed. ' \
                      f'Observed: {observed}, expected: {expected}. ' \
                      f'Element: {element}')
    return result
