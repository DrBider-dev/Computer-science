def number_pair(K: int, elements: list) -> bool:
    result = False
    for element in elements:
        for element2 in elements:
            if (element + element2) == K:
                result = True
    return result