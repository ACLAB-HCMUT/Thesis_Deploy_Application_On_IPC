from app.services.service import get_all_data_service, get_data_in_day

def get_all_data():
    try:
        data = get_all_data_service()
        return data
    except Exception as e:
        raise Exception(f"Error fetching data: {str(e)}")

def get_data_in_day(field, value):
    try:
        data = get_data_in_day()
        return data if data else None
    except Exception as e:
        raise Exception(f"Error fetching data: {str(e)}")
