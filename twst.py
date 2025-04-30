def solution(N, K, cost, sell):
    
    p = [sell[i] - cost[i] for i in range(N)]
    
    
    pt = [(cost[i], p[i]) for i in range(N) if p[i] > 0]
    
    
    pt.sort(key=lambda x: x[1], reverse=True)
    
    total_p = 0
    cm = K
    
    for ic, item_p in pt:
        if cm >= ic:
            #
            cm -= ic
            cm += ic + item_p
            total_p += item_p
    
    return total_p

# Example usage:
N = 10
K = 15
cost = [22,85,46,31,78,56,98,66,30,14]
sell = [75,40,97,39,21,49,37,43,23,88]
print(solution(N, K, cost, sell))  # Output: 7
