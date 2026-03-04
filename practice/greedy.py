def coins_min(N: int, coins: list) -> int:
    coins = sorted(coins, reverse=True)

    total = 0
    for coin in coins:
        if N >= coin:
            total += N//coin
            N = N % coin
    
    return total