def join_maps(*maps):
    result = {}
    for map in maps:
        if map:
            result.update(map)
    return (result)

