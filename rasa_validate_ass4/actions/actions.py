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

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.types import DomainDict


import sqlite3
import petl as etl

conn = sqlite3.connect('candidates.db')

conn.execute("""CREATE TABLE IF NOT EXISTS candidate(
  id integer Primary Key Autoincrement,
  email text NOT NULL,
  name text NOT NULL,
  empId int NOT NULL
  );""")

table_candidate = etl.fromdb(conn, 'SELECT * from candidate')


conn.execute("""CREATE TABLE IF NOT EXISTS nomination(
    id integer Primary Key Autoincrement,
    name text NOT NULL,
    justification text NOT NULL
    );""")

table_nomination = etl.fromdb(conn, 'SELECT * from nomination')


class ActionSaveCandidateDetails(Action):

    def name(self) -> Text:
        return "action_save_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        slots = {
            "name": tracker.get_slot("name"),
            "empCode": tracker.get_slot("empCode"),
            "emailid": tracker.get_slot("emailid"),
        }
        conn.execute(
            """INSERT INTO candidate (email, name, empId) VALUES(?,?,?) """,
            (slots["emailid"], slots["name"], slots["empCode"]))
        conn.commit()
        dispatcher.utter_message(text="Information Saved")

        return [SlotSet(slot, value) for slot, value in slots.items()]


class ActionDeleteCandidateDetails(Action):

    def name(self) -> Text:
        return "action_delete_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        slots = {
            "name": tracker.get_slot("name"),
            "empCode": tracker.get_slot("empCode"),
            "emailid": tracker.get_slot("emailid"),
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

        dispatcher.utter_message(text=str(table_candidate))
        return [SlotSet(slot, value) for slot, value in slots.items()]


class ActionValidateNominationForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_nomination_form"

    def validate_nominees(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate nominees value."""

        slots = {
            "nominees": tracker.get_slot("nominees")
        }

        if len(slot_value) < 1:
            return {"nominees": None}

        for name in slot_value:
            nomineeName = name+"%"
            cur = conn.cursor()
            cur.execute("""SELECT * from candidate
                WHERE name LIKE ?""",
                        (nomineeName,))

            nomineeFoundRow = cur.fetchall()

            if len(nomineeFoundRow) == 0:
                dispatcher.utter_message(
                    text=f"Nominee {name} not found in Database")
                return {"nominees": None}

        return {"nominees": slot_value}

    def validate_justification(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate justification value."""

        if len(slot_value) <= 3:
            dispatcher.utter_message(text=f"That's a very short justification")
            return {"justification": None}
        else:
            return {"justification": slot_value}


class ActionSaveNominationDetails(Action):

    def name(self) -> Text:
        return "action_save_nominees"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        slots = {
            "nominees": tracker.get_slot("nominees"),
            "justification": tracker.get_slot("justification"),
        }

        for name in slots["nominees"]:
            conn.execute(
                """INSERT INTO nomination(name, justification) VALUES(?, ?) """,
                (name, slots["justification"]))

        conn.commit()

        dispatcher.utter_message(text="Nomination Details Saved")

        return [SlotSet(slot, value) for slot, value in slots.items()]
