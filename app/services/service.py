from app.models.models import collection_name

def get_all_data_service():
    data = list(collection_name.find())
    for item in data:
        item['_id'] = str(item['_id'])
    return data

def get_data_in_day():
    # query = {field: value}
    # data = list(collection_name.find(query))
    # for item in data:
    #     item['_id'] = str(item['_id'])
    # return data if data else None
    return None