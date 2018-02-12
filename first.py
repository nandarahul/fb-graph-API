import requests

HOST = "https://graph.facebook.com"
VERSION = "v2.12"
ACCESS_TOKEN = "Enter-Token-here"


def get_object_likes(obj_id, user_react_count_dict):
    # Using reactions endpoint instead of likes
    url = '/'.join([HOST, VERSION, obj_id, 'reactions'])
    param_dict = {'access_token': ACCESS_TOKEN}
    while True:
        r = requests.get(url, params=param_dict)
        if not r.status_code == 200:
            break
        response_dict = r.json()
        for reactor_info in response_dict['data']:
            if reactor_info['id'] in user_react_count_dict:
                user_react_count_dict[reactor_info['id']] += 1
            else:
                user_react_count_dict[reactor_info['id']] = 1
        #print(response_dict['data'])
        if 'paging' not in response_dict or 'next' not in response_dict['paging']:
            break
        url = response_dict['paging']['next']


def get_top_friends(object_types):
    """
    Some of the valid object_types: 'posts', 'feed', 'photos'
    Find reaction count from people on your fb posts, photos, etc (object_types param).
    Returns a list of tuples (user_id and reaction count) ranked from highest reaction count to lowest.
    """
    user_react_count_dict = {}
    for obj_type in object_types:
        request_path = "me/" + obj_type
        url = HOST + '/' + VERSION + '/' + request_path
        param_dict = {'access_token': ACCESS_TOKEN}
        while True:
            r = requests.get(url, params=param_dict)
            response_dict = r.json()
            if 'data' not in response_dict:
                print(response_dict)
                break
            for node_info in response_dict['data']:
                get_object_likes(node_info['id'], user_react_count_dict)
            #print(response_dict['data'])
            if 'paging' not in response_dict or 'next' not in response_dict['paging']:
                break
            url = response_dict['paging']['next']
    user_react_count_list = sorted(user_react_count_dict.items(), key=lambda x: x[1], reverse=True)
    return user_react_count_list


def get_node_name(node_id):
    request_path = node_id
    url = HOST + '/' + VERSION + '/' + request_path
    param_dict = {'access_token': ACCESS_TOKEN}
    r = requests.get(url, params=param_dict)
    if r.status_code != 200:
        print(r.json())
        return "Error"
    else:
        return r.json()["name"]


def analyse_reactions(user_react_count_list):
    total_reactions = 0
    for userid_count in user_react_count_list:
        total_reactions += userid_count[1]
    print("Total reactions received: %d" % total_reactions)
    top_k = 10
    print("Top %d friends" % top_k)
    for userid_count in user_react_count_list[:top_k]:
        print(get_node_name(userid_count[0]), userid_count[1])


if __name__ == "__main__":
    user_react_count_list = get_top_friends(['feed'])
    analyse_reactions(user_react_count_list)


