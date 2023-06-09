from typing import Dict, Text, Any, List, Union, Optional
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Tracker, FormValidationAction, Action
from rasa_sdk.types import DomainDict
from rasa.core.actions.forms import FormAction
from rasa_sdk.events import  AllSlotsReset, EventType, SlotSet

import mysql.connector
from mysql.connector import Error
import json

from datetime import datetime
import re
import wikipedia

# Make a regular expression in order to validatie an email
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

# Define a function for validating an Email
def check_mail(email):
    # pass the regular expression and the string into the fullmatch() method
    if(re.fullmatch(regex, email)):
        return True
    else:
        return False

# Connection to the database
def db_connect():
        try:
            connection = mysql.connector.connect(host='localhost',
                                                database='db_rasa_cb',
                                                user='root',
                                                port=3306)
            if connection.is_connected():
                # db_Info = connection.get_server_info()
                print("DB is connected!")
                cursor = connection.cursor(buffered=True)
                cursor.execute("select database();")
                query = ("SELECT * FROM room")
                cursor.execute(query)

                return connection,cursor

        except Error:
            print("Some problem occurred while connecting to the DataBase")

# using the wiki api, some info are stored in a json
def api_wiki(PAGE,end_content,indx):
    wikipedia.set_lang("en")
    city = wikipedia.page(title=PAGE)
    title = city.title
    content = city.content[:end_content]
    image = city.images[indx]
    json_data = {"title":title, "content":content, "image":image}
    return json_data
        
def unitPrice(room,n_adults, n_kids):

    if room == "Deluxe":
        price = ((n_adults*500)+(n_kids*100))
    elif room == "Standard":
        price = ((n_adults*50)+(n_kids*10))
    elif room == "Presidential":
        price = ((n_adults*1000)+(n_kids*200))
    return price
# Action used to show all the attractions in the static db
class NearestAttractions(Action):
    def name(self):
        """name of the custom action"""
        return "action_nearest_attractions"

    def run(self,dispatcher,tracker,domain):
        loreto = api_wiki("Loreto, Marche",1072, 1)
        sirolo = api_wiki("Sirolo", 1284, 3)
        recanati = api_wiki("Recanati", 1193, 2)
        ancona = api_wiki("Ancona", 562, 1)
        castelfidardo = api_wiki("Castelfidardo", 737, 0)
        porto_recanati = api_wiki("Porto Recanati", 798, 3)
        attractions = [loreto,sirolo,recanati,ancona,castelfidardo,porto_recanati]

        for att in attractions:
            msg="\n\n"+att["title"]+"\n"+att["content"]+"\n\n"
            dispatcher.utter_message(text=msg,image=att["image"])
        return []

# Action that shows the details of a chosen attraction
class DetailsAttraction(FormValidationAction):
    def name(self):
        """name of the custom action"""
        return "validate_attraction_form"

    @staticmethod
    def attraction_db() -> List[Text]:
        """Database of supported attractions"""

        return ["loreto","recanati","sirolo","porto recanati","castelfidardo","ancona"]
    
    def validate_attraction(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `attraction` value."""

        if slot_value.lower() not in self.attraction_db():
            dispatcher.utter_message(text=f"I didn't find anything. \nBut you can find more info about the nearest attractions here: \n---> https://www.rivieradelconero.info/en/")
            # return {"attraction": None}
        else:
            if slot_value.lower() == self.attraction_db()[0]:
                website = "https://www.rivieradelconero.info/en/loreto-a-christian-pilgrimage-destination/"
            elif slot_value.lower() == self.attraction_db()[1]:
                website = "https://www.rivieradelconero.info/en/item/recanati.php"
            elif slot_value.lower() == self.attraction_db()[2]:
                website = "https://www.rivieradelconero.info/en/sirolo-a-seaside-town-in-the-conero-riviera/"
            elif slot_value.lower() == self.attraction_db()[3]:
                website = "https://www.rivieradelconero.info/en/porto-recanati-a-seaside-town-in-the-conero-riviera/"
            elif slot_value.lower() == self.attraction_db()[4]:
                website = "https://www.rivieradelconero.info/en/music-and-culture-in-castelfidardo/"
            elif slot_value.lower() == self.attraction_db()[5]:
                website = "https://www.rivieradelconero.info/en/ancona-a-seaside-town-with-a-rich-archeological-heritage/"
            dispatcher.utter_message(text=f"OK! Here some info about {slot_value}:\n" + website)
        return {"attraction": None}

# Action that shows the rooms' details
class CheckRooms(Action):
    def name(self):
        """name of the custom action"""
        return "action_check_rooms"

    def run(self,dispatcher,tracker,domain):
        deluxe = {"title":"Deluxe","image":"https://www.miasaigon.com/wp-content/uploads/2020/03/msg-deluxe-room-twin-bedroom.jpg",}
        standard = {"title":"Standard","image":"https://images.pexels.com/photos/14021931/pexels-photo-14021931.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"}
        presidential = {"title":"Presidential","image":"https://th.bing.com/th/id/R.73f6f9ccbe4e1d300282d2aa56c80e40?rik=qHzo7xftYiNcFA&riu=http%3a%2f%2fdtla.intercontinental.com%2fwp-content%2fuploads%2f2016%2f12%2fInterContinental-LA-Downtown_Presidential_Suite_Living_Room_A7116_jpg.jpg&ehk=KWM0rYN3QHlk2TWKJIPX9awkxcyWoZrZweNZ5gfz6dE%3d&risl=&pid=ImgRaw&r=0"}
        room_type = [deluxe,standard,presidential]

        for r in room_type:
            msg="\n\n"+r["title"]+"\n\n"
            dispatcher.utter_message(text=msg,image=r["image"])

        dispatcher.utter_message(text="If you desire any further information, feel free to ask for more details.")
        return []
   
class ActionBookRoomForm(FormAction):
    def name(self) -> Text:
        """Unique identifier of the form"""
        return "book_room_form"
    
    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""
        return ["adults","kids","checkin","checkout","email","phno","room"]

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""
        # utter submit template
        dispatcher.utter_message(template="utter_submit_book_room_form")
        return []
    
    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""
        return {
            "adults": self.from_entity(entity="people",role="adults", intent="inform_people"),
            "kids": self.from_entity(entity="people",role="kids", intent="inform_people"),
            "checkin": self.from_entity(entity="date", role="checkin", intent="inform_date"),
            "checkout": self.from_entity(entity="date", role="checkout", intent="inform_date"),
            "email": self.from_entity(entity="contacts", role="email", intent="inform_contacts"),
            "phno": self.from_entity(entity="contacts", role="phno", intent="inform_contacts"),
            "room": self.from_entity(entity="room", intent="inform_room"),
        }
    
class AskForSlotAction(Action):
    def name(self) -> Text:
        return "action_ask_room"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:

        # variable used to connect the db
        connection,cursor = db_connect()

        rooms_available = []

        # check-in and check-out stored in the slots
        new_check_in=str(tracker.get_slot("checkin"))
        new_check_out=str(tracker.get_slot("checkout"))

        # Iterating over the rows, each room is checked
        for(room_id,room_type,reservations) in cursor:
            # only reservation field is read
            json_res = json.loads(reservations)
            # flag used to check whether the room is available
            flag = True
            for res in json_res["res"]:
                
                date_string = res["check_in"]
                check_in_date = datetime.strptime(date_string, "%d/%m/%Y").date()
                date_string = res["check_out"]
                check_out_date = datetime.strptime(date_string, "%d/%m/%Y").date()
                
                check_in_new_date = datetime.strptime(new_check_in, "%d/%m/%Y").date()
                check_out_new_date = datetime.strptime(new_check_out, "%d/%m/%Y").date()

                # by this condition, the room's availability is verified
                if((check_in_new_date>=check_in_date and check_in_new_date<check_out_date)
                or(check_out_new_date<=check_out_date and check_out_new_date>check_in_date)):
                    # setting the flag to false means that the room cannot be booked
                    flag = False
                    break

            # checking if this room is free during that period
            if flag:
                button = {"title": room_type, "payload": '/inform_room{"room":"'+room_type+'"}'}
                # room type only is shown to the user
                if (button not in rooms_available):
                    rooms_available.append(button)

        # Fetch the data and store in the format used by buttons.
        button_list = rooms_available
        print(button_list)
        if len(button_list)==0:
            dispatcher.utter_message(text="There are no available rooms on the selected dates.\nPlease, try again.")
            cursor.close()
            print("DB was shut down!")
            connection.close()
            dispatcher.utter_message(response="utter_ask_checkin")
            return [SlotSet('checkin', None), SlotSet('checkout', None)]
        else:
            dispatcher.utter_message(text=f"Available rooms for:\n{new_check_in} - {new_check_out}", buttons=button_list, button_type="vertical")
        cursor.close()
        print("DB was shut down!")
        connection.close()
        return []

class ValidateNameForm(FormValidationAction):
    def name(self):
        return "validate_name_form"
    
    def validate_first_name(
        self,
        slot_value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `first_name` value."""
        name=slot_value
        if len(name)<2:
            dispatcher.utter_message(text=f"You may have done a typo! Retry.")
            return {"first_name": None}
        else:
            return {"first_name": name}

    def validate_last_name(
        self,
        slot_value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `last_name` value."""
        name=slot_value
        if len(name)<2:
            dispatcher.utter_message(text=f"You may have done a typo! Retry.")
            return {"last_name": None}
        else:
            return {"last_name": name}  

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""
        # utter submit template
        dispatcher.utter_message(template="utter_submit_name_form")
        return []  
        
class ValidateBookRoomForm(FormValidationAction):
    def name(self):
        return "validate_book_room_form"
    
    def validate_adults(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Any, Any]:
        """Validate `adults` value."""
        try: 
            n_adults = int(slot_value)
            if (n_adults < 1 or n_adults > 8):
                dispatcher.utter_message(text=f"Number of adults allowed: 1 - 8! Please, retry.")
                return {"adults": None}
            else:
                return {"adults": n_adults}
        except:
            dispatcher.utter_message(text=f"This value (" + str(slot_value) + ") is not correct! Please, retry.")
            return {"adults": None}

    def validate_kids(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Any, Any]:
        """Validate `kids` value."""
        try: 
            if slot_value.lower() in ["no","none","any"]:
                return {"kids": 0}
            elif (int(slot_value) >= 0 and int(slot_value) < 7):
                n_kids = int(slot_value)
                return {"kids": n_kids}
            else:
                dispatcher.utter_message(text=f"Number of kids allowed: 0 - 6! Please, retry.")
                return {"kids": None}
        except:
            dispatcher.utter_message(text=f"This value (" + str(slot_value) + ") is not correct! Please, retry.")
            return {"kids": None}

    def validate_checkin(
        self,
        slot_value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `checkin` value."""
        date_str = slot_value
        present = datetime.now().date()
        for fmt in ('%d/%m/%Y', '%d-%m-%Y', '%Y/%m/%d', '%Y-%m-%d'):
            try:
                date_obj = datetime.strptime(date_str, fmt).date()
                if date_obj < present:
                    dispatcher.utter_message(text=f"Check-in date cannot be past date! Please, retry.")
                    return {"checkin": None}
                else:
                    date_obj = date_obj.strftime('%d/%m/%Y')
                    return {"checkin": date_obj}
            except ValueError:
                pass

        dispatcher.utter_message(text=f"Check-in date is not correct! Please, retry.")
        return {"checkin": None}

    def validate_checkout(
        self,
        slot_value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `checkout` value."""
        date_str = slot_value
        present = datetime.now().date()
        try:
            check_in_date = str(tracker.get_slot("checkin"))
            check_in_date = datetime.strptime(check_in_date,'%d/%m/%Y').date()
            for fmt in ('%d/%m/%Y', '%d-%m-%Y', '%Y/%m/%d', '%Y-%m-%d'):
                try:
                    date_obj = datetime.strptime(date_str, fmt).date()
                    if date_obj < present:
                        dispatcher.utter_message(text=f"Check-out date cannot be past date! Please, retry.")
                        return {"checkout": None}
                    elif date_obj < check_in_date:
                        dispatcher.utter_message(text=f"Check-out date cannot be prior to check-in date! Please, retry.")
                        return {"checkout": None}
                    else:
                        date_obj = date_obj.strftime('%d/%m/%Y')
                        return {"checkout": date_obj}
                except ValueError:
                    pass
        except Error as e:
            print(e)
            
        dispatcher.utter_message(text=f"Check-out date is not correct! Please, retry.")
        return {"checkout": None}
            

    def validate_email(
        self,
        slot_value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `email` value."""
        mail = slot_value
        if check_mail(mail) == False:
            dispatcher.utter_message(text=f"You may have done a typo! Retry.")
            return {"email": None}
        else:
            return {"email": mail}
    
    def validate_phno(
        self,
        slot_value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `phno` value."""
        number = slot_value
        if (len(number)<6 or len(number)>15):
            dispatcher.utter_message(text=f"Your number is not correct! Retry.")
            return {"phno": None}
        else:
            return {"phno": number}

    def validate_room(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Any, Any]:
        """Validate `room` value."""
        room = slot_value
        if room not in ["Deluxe","Standard","Presidential"]:
            #dispatcher.utter_message(text=f"This room is not correct! Retry.")
            return {"room": None}
        else:
            first_name=str(tracker.get_slot("first_name"))
            last_name=str(tracker.get_slot("last_name"))
            name = first_name + " " + last_name

            # variable used to connect the db
            connection,cursor = db_connect()

            # check-in and check-out stored in the slots
            new_check_in=str(tracker.get_slot("checkin"))
            new_check_out=str(tracker.get_slot("checkout"))
            
            kids = str(tracker.get_slot("kids"))
            adults = str(tracker.get_slot("adults"))
            # this query select only rooms that are compliant with type
            new_query = ("SELECT * FROM room WHERE room_type = %s")
            val = (room, )
            cursor.execute(new_query,val)

            # Iterating over the rows, each room is checked
            for(room_id,room_type,reservations) in cursor:
                # only reservation field is read
                json_res = json.loads(reservations)
                # flag used to check whether the room is available
                flag = True

                for res in json_res["res"]:
                    
                    date_string = res["check_in"]
                    check_in_date = datetime.strptime(date_string, "%d/%m/%Y").date()
                    date_string = res["check_out"]
                    check_out_date = datetime.strptime(date_string, "%d/%m/%Y").date()
                    
                    check_in_new_date = datetime.strptime(new_check_in, "%d/%m/%Y").date()
                    check_out_new_date = datetime.strptime(new_check_out, "%d/%m/%Y").date()

                    # by this condition, the room's availability is verified
                    if((check_in_new_date>=check_in_date and check_in_new_date<check_out_date)
                    or(check_out_new_date<=check_out_date and check_out_new_date>check_in_date)):
                        # setting the flag to false means that the room cannot be booked
                        flag = False
                        break

                # checking if this room is free during that period            
                if flag:
                    try:
                        new_res = {
                            "check_in": new_check_in,
                            "check_out": new_check_out,
                            "reference": name,
                            "kids": kids,
                            "adults": adults
                            }
                        
                        json_res["res"].append(new_res)
                        updt_res = json.dumps(json_res, indent=3)
                        # this query allows to update the reservation field relative to a particular id
                        updt = ("UPDATE room SET reservations = %s WHERE room_id = %s")
                        v = (updt_res,room_id)
                        # Execute the SQL command
                        cursor.execute(updt,v)                           
                        # Commit your changes in the database
                        connection.commit()
                        print("Update executed successfully") 
                        break
                    except Error as e:
                        print(e)
                        cursor.close()
                        print("DB was shut down!")
                        connection.close()
                        return {"room": None}
            cursor.close()
            print("DB was shut down!")
            connection.close()
            return {"room": room}

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""
        # utter submit template
        dispatcher.utter_message(template="utter_submit_book_form")
        return []  

class BookRoomsDetails(Action):
    def name(self):
        """name of the custom action"""
        return "action_book_room_details" 

    def run(self,dispatcher,tracker,domain):
        try:
            check_in=str(tracker.get_slot("checkin"))
            check_out=str(tracker.get_slot("checkout"))
            adults=str(tracker.get_slot("adults"))
            kids=str(tracker.get_slot("kids"))
            room=str(tracker.get_slot("room"))
            first_name=str(tracker.get_slot("first_name"))
            last_name=str(tracker.get_slot("last_name"))
            phno=str(tracker.get_slot("phno"))
            email=str(tracker.get_slot("email"))
            name = str(first_name) + " " + str(last_name)
            unit_price = unitPrice(room,int(adults),int(kids))
            n_days = (datetime.strptime(check_out, '%d/%m/%Y').date() - datetime.strptime(check_in, '%d/%m/%Y').date()).days
            price = str(n_days*unit_price)

            connection,cursor = db_connect()
            new_query = ("SELECT * FROM room WHERE room_type = %s")
            val = (room, )
            cursor.execute(new_query,val)
            for(room_id,room_type,reservations) in cursor:
                    # only reservation field is read
                    json_res = json.loads(reservations)
                    # flag used to check whether the room is available
                    flag = True

                    for res in json_res["res"]:
                        date_string = res["check_in"]
                        check_in_date = datetime.strptime(date_string, "%d/%m/%Y").date()
                        date_string = res["check_out"]
                        check_out_date = datetime.strptime(date_string, "%d/%m/%Y").date()
                        
                        check_in_new_date = datetime.strptime(check_in, "%d/%m/%Y").date()
                        check_out_new_date = datetime.strptime(check_out, "%d/%m/%Y").date()

                        # by this condition, the room's availability is verified
                        if((check_in_new_date == check_in_date and check_out_new_date==check_out_date)
                        and(name == res["reference"])):
                            room = room + " n° " + str(room_id)


            message="BOOKING DETAILS"+"\n"+"Name: "+name+"\n"+"Check-in Date: "+check_in+"\n"+"Check-out Date: "+check_out+"\n"+"No. of Adults: "+adults+"\n"+"No. of Kids: "+kids+"\n"+"Room: "+room+"\n"+"Phone Number: "+phno+"\n"+"Email: "+email
            dispatcher.utter_message(message)
            dispatcher.utter_message(text="Total price: € " + price)
        except Error as e:
            print(e)
        finally:
            cursor.close()
            print("DB was shut down!")
            connection.close()
            return []

class ActionFullReset(Action):
    def name(self) -> Text:
            return "action_reset"

    def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         """resetting"""
         return [AllSlotsReset()]