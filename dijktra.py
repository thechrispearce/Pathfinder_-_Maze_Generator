def dijkstra(draw, grid, start, end):
    count = 0
    # priority queue uses heap sort algorithm to get the smallest element out of the queue efficiently
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    # track where we were
    came_from = {}
    # current shortest distance from start to each node
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0

    # need to use dictionary to check if node in the queue
    open_set_hash = {start}

    while not open_set.empty():
        # while we have nodes in the queue
        for event in pygame.event.get():
            # in case we need to escape
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]  # index at 2 to get node
        open_set_hash.remove(current)

        if current == end:
            draw_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True  # if we have found the end, make path

        for neighbour in current.neighbours:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbour]:  # if new path is better, replace it
                came_from[neighbour] = current
                # calc new f and g score
                g_score[neighbour] = temp_g_score
                if neighbour not in open_set_hash:
                    # check if neighbour is in the queue
                    count += 1
                    open_set.put((g_score[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.make_open()
        draw()

        if current != start:
            # if the node we just considered is not start, make closed
            current.make_closed()
    return False
