import Memory as mem

if __name__ == "__main__":
    max_walk_length = 6
    walks = mem.monte_carlo_walk(50)
    for length, walks in walks.items():
        walks_with_smaller_distance = 0
        for _, distance, in walks:
                if distance <= max_walk_length:
                    walks_with_smaller_distance += 1
        print(f"{(walks_with_smaller_distance / len(walks)):.4f}")