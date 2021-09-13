# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet


import sqlite3

conn = sqlite3.connect('candidates.db')

conn.execute("""CREATE TABLE IF NOT EXISTS candidate(
  id integer Primary Key Autoincrement,
  email text,
  name text,
  empId int
  );""")


class ActionCandidateName(Action):

    def name(self) -> Text:
        return "action_ask_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        slots = {

        }
        dispatcher.utter_message(response="utter_ask_name")

        return [SlotSet(slot, value) for slot, value in slots.items()]


class ActionCandidateEmployeeCode(Action):

    def name(self) -> Text:
        return "action_ask_empCode"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        slots = {

        }
        # dispatcher.utter_message(text="What is your contact number?")
        dispatcher.utter_message(response="utter_ask_empCode")

        return [SlotSet(slot, value) for slot, value in slots.items()]


class ActionCandidateEmailId(Action):

    def name(self) -> Text:
        return "action_ask_emailId"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        slots = {

        }
        # dispatcher.utter_message(text="What is your contact number?")
        dispatcher.utter_message(response="utter_ask_emailid")

        return [SlotSet(slot, value) for slot, value in slots.items()]


class ActionSaveCandidateDetails(Action):

    def name(self) -> Text:
        return "action_save_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        slots = {
            "PERSON": tracker.get_slot("PERSON"),
            "number": tracker.get_slot("number"),
            "email": tracker.get_slot("email"),
        }
        # dispatcher.utter_message(text="What is your contact number?")
        conn.execute(
            """INSERT INTO candidate (email, name, empId) VALUES(?,?,?) """,
            (slots["email"], slots["PERSON"], slots["number"]))
        conn.commit()
        dispatcher.utter_message(response="utter_save_info")

        return [SlotSet(slot, value) for slot, value in slots.items()]


class ActionDeleteCandidateDetails(Action):

    def name(self) -> Text:
        return "action_delete_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        slots = {
            "PERSON": tracker.get_slot("PERSON"),
            "number": tracker.get_slot("number"),
            "email": tracker.get_slot("email"),
        }

        candidate = tracker.latest_message["entities"][0]["value"]

        candidateName = candidate+"%"

        cur = conn.cursor()
        cur.execute("""SELECT * from candidate
        WHERE name LIKE ?
        OR
        empId = ?""",
                    (candidateName, candidate))

        candidateFoundRow = cur.fetchall()

        if len(candidateFoundRow) == 0:
            dispatcher.utter_message(response="utter_delete_Unsuccessfull")
            return []

        conn.execute("""DELETE from candidate
        WHERE name LIKE ?
        OR
        empId = ?
        """,
                     (candidateName, candidate))
        conn.commit()
        # dispatcher.utter_message(text="What is your contact number?")
        dispatcher.utter_message(response="utter_delete_successfull")

        return [SlotSet(slot, value) for slot, value in slots.items()]


class ActionGetCandidateList(Action):

    def name(self) -> Text:
        return "action_get_candidateList"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        slots = {

        }
        # dispatcher.utter_message(text="What is your contact number?")
        # dispatcher.utter_message(response="utter_list")

        cur = conn.cursor()
        cur.execute("""SELECT * from candidate""")
        rows = cur.fetchall()
        dispatcher.utter_message(text=str(rows).strip(
            '[]') if len(rows) > 0 else "No records found")
        return [SlotSet(slot, value) for slot, value in slots.items()]
