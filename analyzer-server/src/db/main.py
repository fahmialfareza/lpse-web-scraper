from db.tender_upsert import save_to_tender_db
from db.tender_select import fetch_left_join_tender_results


def save_to_db():
    save_to_tender_db()


def get_tender_data():
    return fetch_left_join_tender_results()
