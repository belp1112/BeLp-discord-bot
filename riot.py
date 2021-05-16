from requests import get



def return_collect_champion_name(language:str , champion_name:str) ->list:
    version = list(get('https://ddragon.leagueoflegends.com/api/versions.json').json())[0]
    resp = get(f'http://ddragon.leagueoflegends.com/cdn/{version}/data/{language}/champion.json').json()
    all_champion_data_list = [i for i in resp['data']]
    all_champion_id_list   = [resp['data'][i]['id'] for i in all_champion_data_list]
    all_champion_name_list = [resp['data'][i]['name'] for i in all_champion_id_list]
    all_champion_name_dict_list = dict(zip(all_champion_name_list, all_champion_data_list))
    try:
        return all_champion_name_dict_list[champion_name]
    except:
        KeyError
#print(return_collect_champion_name('en_US', 'katarina'))

def retrieve_championdata(id_champion_name, language:str,) -> dict:
    """チャンピオン名を受け取ってそのチャンピオンのjsonまたはエラーメッセージ(str)を返す"""
    version = list(get('https://ddragon.leagueoflegends.com/api/versions.json').json())[0]
    resp = get(f'http://ddragon.leagueoflegends.com/cdn/{version}/data/{language}/champion/{id_champion_name}.json')
    if resp.status_code != 200: #エラー処理 レスポンスコードが200では無かった場合
        error = 'スペルが間違っているか存在しないチャンピオンです'
        return error
    championdata = resp.json()
    return championdata


def return_skinlist(championdata: dict, championname: str) -> list:
    '''受け取ったチャンピオンの全てのスキン名とスキン番号を辞書型にし、リストに入れて返す'''
    skin_list = []
#   skin_list = [{skin['name']: skin['num']} for skin in championdata['data'][championname]['skins']]
    for skin in championdata['data'][championname]['skins']:
        skin_list.append({'name': skin['name'], 'num':skin['num']})
    return skin_list


def shape_to_discordmsg(skin_list: list) ->str:
    temp = []
    for idx in range(len(skin_list)):
        temp.append(f"`{idx + 1}`: {skin_list[idx]['name']}")
    temp.append('スペース区切りで番号を入力してください')
    return '\n'.join(temp)



#skin_list = return_skinlist(retrieve_championdata('Katarina'), 'Katarina')
#print(shape_to_discmsg(skin_list))


# children : [{'カタリニャ': 4,}, {}, {}]

# !bel {champion_name}
#     画像ナンバーの list を返す
# !bel {champion_name} [num]
#     画像 URL を返す

# ["data"][{champion_name}]["id"] == "英語名"
# ["data"][{champion_name}]["name"] == "日本語名"
