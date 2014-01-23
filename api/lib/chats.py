

def get_unique_chats(chats):
    seen = {}
    results = []
    for item in chats:
        val = item.with_user
        if val in seen:
            continue
        seen[val] = 1
        a = item.to_dict()
        results.append(item)
    return results
