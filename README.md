# HotelChat_Bot

## 1. Chatbot

The term "chatbot", as can be guessed from the name, indicates a software
aimed at automating the process of communication with the user.
These programmes are capable of simulating, in a more or less
realistically, a conversation with the user, based on natural language.

Today's companies make extensive use of these systems, as they allow
automate processes that involve interfacing with the user,
guaranteeing a 24/7 service.

There is a tendency in the literature to distinguish between two main types of bots:

- **TASK ORIENTED** : These are assistants aimed at a specific task;
    they aim to provide help to the user, facilitating him/her in performing
    certain operations. This type of software draws from predefined
    predefined data sets (e.g. Databases, APIs, etc.) to return to the user
    responses to requests for information.
- **CONVERSATIONAL CHATBOTS** : These are virtual assistants in all
    and for everything, and therefore do not aim to have knowledge limited to
    a specific field, but must be able to hold
    conversations on every possible topic.

For the purposes of this project, we shall confine ourselves to the development of a bot
task-oriented bot capable of providing the user with information useful for booking a hotel room.
of a hotel room. In fact, in order to meet the market demand in
and attract more and more customers, the large competitors in the
hotel sector continue to improve their services and look for new
ways to make their offer more convenient. Chatbots are playing an
increasingly important in all hotel operations, from addressing direct bookings to increasing
direct bookings to increasing website conversion, from helping
hoteliers, such as the concierge and front desk agents, to
automate repetitive guest requests.

## 2. RASA

Rasa is an open source framework aimed at developing chatbots that
automate the process of text- and voice-based conversation. The
voice assistants developed in rasa may be able to communicate
through various platforms such as Facebook Messenger, Slack, Google
Hangouts, Telegram and many others. Rasa also provides modules that
software to communicate with devices such as Amazon Alexa and
Google Home.

The RASA framework can be identified as the union of two sub-components,
each of which has specific purposes:

- **RASA NLU** (Natural Language Understanding): The component of
    RASA which aims to interpret the natural language given as input
    (intent) and extract from it the intent and commands given by the user.
- **RASA CORE** : The component that, once the intent has been interpreted by
    by the NLU, is responsible for managing the responses, i.e.
    planning response actions to what has been input by the user.
    the user.

The Rasa NLU requires a supervised training phase in order to be put into operation.
of supervised training; this means that a dataset must be set up to train the NLU.
to train the NLU to correctly interpret every possible input
input given to the bot. To generate an exhaustive response to the user, one must
follow a well-defined sequence. First of all, the messages given as input
by the user are classified into a series of intents and analysed
by the user agent, which takes care of extracting the entities (a specific object
which may refer to a person, place, thing, etc.), whenever they are
present. Subsequently, the input message is converted into a
dictionary that includes the original text, the intent and all the entities found. The
result of the previous module is stored in the tracker, which
allows control over the bot's memory, also being able to
retrieve past information. The user agent relies on certain criteria
(being able to specify certain policies) in order to decide what actions are to be
take at each stage. Subsequently, the chosen action is stored
in the tracker, which, as mentioned earlier, stores data on the status of the
conversation status and, if necessary, can make use of necessary information based on
the dialogue history (thus, also slots and results). Following this
a response is generated for the user.

### 2.1 Project goal

The chatbot developed in the course of this project is intended to assist
the user during the booking of hotel rooms, providing a
set of information to support the choice. At a basic level, a chatbot of
such a chatbot works by interpreting or understanding customer interactions and
customers and providing answers relevant to the request made. In addition, it must
be able to offer a pleasant user experience without failing in its
primary objectives, in terms of clarity and accuracy of the information
provided.

Through the use of text chat and some buttons, the user will be able to
to obtain information of various kinds, such as attractions and places of
of interest related to a specific destination, or the characteristics
of certain hotel rooms. Finally, the bot will also give the customer the
possibility of making a reservation, automatically validating the
request made by the user.

## 3. Tools used

### 3.1 XAMPP

Having clearly identified the various features to be implemented in the
chatbot, we moved on to the definition of the structures aimed at the
persistence of information. Initially, we wanted to proceed by consulting
online APIs linked to well-known accommodation and room reservation services
(Booking.com, AirB&B, etc.), but this turned out not to be feasible due to the costs of using such services.
costs associated with the use of such web services. Therefore, a Database was created
exploiting the functionality offered by the open-source software XAMPP.

Consequently, considering the bot's features, the following columns were included in the
database the following columns were included:

- **room_id** : Integer (Primary Key) identifier of the individual room of
    hotel
- **room_type** : Text field, indicating the type of the room in question
    (Standard, Deluxe, Presidential)
- **reservation** : Text field, containing a string in
    JSON format, required to keep track of the various bookings made
    by users. Each element of the array is characterised by the fields:
    check_in, check_out, reference (full name of the user who
    made the booking), kids (number of children booked) and
    adults (number of adults booked).

To establish the connection to this database, the library
MySQL Connector library for Python. The latter provides a number of methods
to interact with the selected database; in particular, in our case, the
case, the methods and objects used are:

- **connect()** : Method aimed at establishing a connection with the database
    database once the latter's credentials have been taken as input.
- **cursor** : This is a construct that allows the management of
    database queries, providing a way to iterate over the records in the
    tables produced by the queries.
- **commit()** : A method required to physically execute changes
    on the DB tables.
- **close()** : Once the connection has been established, this method allows you to
    terminate it.

### 3.2 Wikipedia API

Since the user can request information from the chatbot about attractions or
locations, a Python wrapper library of the Wikimedia API is used so
that the chatbot can retrieve the associated details from Wikipedia. In fact, the
elements considered are: the title of the page, part of the description and
an image.

### 3.3 Ngrok

Ngrok is a cross platform service that provides users with the possibility of
expose a local development environment on an Internet server, with minimal
effort. The software allows users to disguise their IP address by
hosting the service on a sub-domain of ngrok.com. In our case, the
software was used to connect the rasa backend with a Telegram bot.

## 4. Implementation

The project was structured in such a way as to respect the logical division into
thematic areas, linked to the application area of the bot. In particular, the
components of the project on which our work was concentrated are:

- **nlu.yml** : this file contains the intent necessary for the training phase,
    aimed at ensuring that the chatbot is able to understand requests,
    regardless of the way in which they are formulated by the user.
- **domain.yml:** this file contains all the notions connected
    to the operational domain, necessary for the bot to function correctly.
    These concepts are represented by:
       1. _Intents_ , which are the same as those in the nlu.yml file;
       2. _Entities_ , i.e. portions of structured information to represent concepts in the user's message. The
          entities may be single or compound, for example _"_ dates _"_
          which has two distinct roles within it, "checkin" and
          "checkout".
       3. _Slots_ , represent the bot's memory areas and are
          exploited by the bot in order to keep track of what is said
          during the conversation.
       4. Forms_ , which are a way to collect values to be
          slots based on user input, according to a
          defined structure.
       5. _Responses_ , which identify the bot's possible responses.
       6. _Actions_ , i.e. a list of actions that the bot can perform (e.g.
          e.g. validations and information processing).
- **stories.yml** : file containing the training data required for
    the training of the model and the management of the conversation. They
    can be exploited so that the bot can generalise
    different dialogue patterns.


- **rules.yml** : similar to stories, these rules must be
    respected in any scenario regardless of the type of
    conversation (e.g. the user's generalities are always requested at the beginning).
    user's generalities).
- **actions.py** : file containing the classes and methods useful for processing
    information processing, identified by the same names in the domain.

Once the design of the application has been considered, we can proceed with
the analysis of the different application areas. For each of these areas
there are specific intents, entities and actions.

### 4.1 First name and surname

As soon as the chatbot starts up, at the first interaction, the user is asked for a first name
and surname from the user, who, in addition to providing this information, will also have to
also confirm the correctness of the personal details. For
implement this functionality, a form is provided with two different slots, one for the name and one for the surname.
for the first name and one for the surname. The validation of generalities takes place
The validation of generalities is done by means of a specific action, which performs a check on the number of characters
entered.

Once this step has been taken, the chatbot presents its functionalities to the user.
which consist of:

- Information about nearby countries and attractions
- FAQ (refund policy, reception hours, etc.)
- Detailed room information
- Reservation of a room
- Summary of the reservation made

### 4.2 Attractions

The user may request more details regarding the most important attractions in the
attractions in the area surrounding the hotel; upon such a request, the chatbot is
presented by the chatbot with a list, including images and descriptions, of the locations
most popular with tourists. In fact, there is a static database
that contains only 6 towns, namely Loreto, Sirolo, Recanati, Ancona,
Castelfidardo, Porto Recanati, and, for each of these, the
descriptions and the relevant image from the Wikipedia page. In detail, a method was
a method has been implemented that allows one to consult the API of
Wikipedia, specifying for each location a certain number of characters and
the image, which must be considered.

Then, the user can request more information regarding
an individual attraction, and validation of the value entered is carried out. A
point, if this is allowed, then a relative link of the
Conero Riviera website. Of course, it is possible to obtain
information on several attractions, in a sequential manner; however, if the
request concerns a non-admitted site, a default message is returned
default, together with a generic Conero Riviera link.

### 4.3 FAQ

In a chatbot of this kind, one certainly cannot miss the component of
management of the most frequently asked questions. Firstly, the user may
request FAQs from the chatbot, so as to obtain a list of what can be
questions, such as: room view, room reservation, confirmation
reservation, booking restrictions, reception hours, hotel telephone contact
hotel telephone, policy on cancellation and refund, breakfast
refund, breakfast times and menu, check-in and check-out, the policy
regarding pets, the policy regarding minors.

### 4.4 Room details

The user may ask the chatbot to show in a more general manner the
types of rooms present in the hotel and, thanks to a specific action, images of the rooms are
images of the rooms, with their names, are returned. Once the user
has viewed the list provided, it is possible to request more details about a particular room
particular room (obviously, once the additional information has been
additional information, you can repeat the process for a different room).

### 4.5 Booking

The most important feature of the chatbot is the possibility
to make a room reservation autonomously and automatically.
automatically. When the user is ready to proceed with the booking, a form is
launched a form requesting 7 slots, mapped with the corresponding entities:
number of adults, number of children, check-in date, check-out date, e-
mail, telephone number, desired room.

In detail, the booking process consists of 4 basic steps.
- The user is asked to enter both the number of adults and the
    number of children staying in the hotel; for each room, a maximum of 8 adults and 6 children (under 12 years of age) are
    a maximum of 8 adults and 6 children (under 12 years of age) are allowed per room.
    children (under 12 years of age), who must necessarily be accompanied (therefore, it is not
    possible to book for a single child). In the validation of
    these two slots, the number constraints are verified.
- The user must choose the check-in and check-out dates,
    according to one of the four allowed formats. The validation process
    validation process ends successfully if the dates entered do not relate to the current day
    current or past day, if check-in is prior to check-out and
    if there are no typing errors.
- At this point, the chatbot requests the user's contact details, i.e.
    the e-mail address and a telephone number
    (preferably with area code); in this case, the validation process
    exploits an e-mail control function (e.g,
    nomeutente@dominio.it) and verifies the length of the number provided.
- Having all the necessary information available, the chatbot
    exploits a particular action to connect to the database; once
    connection is established, a query is executed in order to check
    which rooms are free in the time interval, decided in advance
    previously decided (taking into account that check-in takes place during the
    afternoon, and check-out in the morning). To facilitate
    the user experience, buttons are returned indicating the
    available rooms ( _Standard_ , _Deluxe_ , _Presidential_ ) so that the customer
    can choose in a simple and intuitive way.

Through the validation process, it is verified that the value entered is
consistent. At the same time, an
update of bookings, within the 'reservations' field
(check-in, check-out, user, number of adults, number of children),
corresponding to the chosen room type. The activity at the level of the
database is validated so as not to generate inconsistencies and errors
such as loss of information, incorrect JSON parsing and ambiguities.
Finally, once the user has finished the procedure, a
summary of the booking, including the room number and the
price, thanks to a method that calculates the total amount from the number
of adults, the number of children and the room type chosen.

## 5. Testing

In order to carry out tests and verify correct operation, it was decided to
use Telegram. In this way, it is possible to make the chatbot available
users through a more familiar interface, who can simply access it from the
simply from the smartphone or desktop application. The choice of
Telegram is basically dictated by the ease of loading the chatbot,
through a procedure within the application itself; moreover, by exploiting the
ngrok service, thanks to which a url is generated that allows communication
through port 5005, communication with the bot is made possible.
Of course, the credentials must be set within the file
_credentials.yml_ file where you enter the access token (obscured for security reasons), the host (url
security reasons), the host (previously created url) and the name of the bot.

At this point we can proceed to the conversation testing phase
by analysing the different possible scenarios. The examples of tests in Telegram can be seen
in pdf file, saved in this repository.

In a first test, the user is asked to identify himself by his
name and surname; he then has to confirm the provided details.

Once this is done, the customer, in order to get an overview of what the bot can do, can ask what questions are most frequently asked. At this
request, the bot will provide a list containing the various functionalities.

The user may ask for some auxiliary information, such as those
refund, cancellation of a reservation, policy on minors and
minors and animal policy.

The customer may also be interested in tourist locations and
attractions in the area surrounding the hotel.

If the customer is particularly impressed by one of the attractions shown by the
bot, he or she may request more details about one or more of the locations. In the
case a country is selected that is not present in the previous list, a
returned a link referring to the Conero Riviera website. At this
point, the user may decide to continue the conversation directly or
specify that they do not wish to have any further information on the attractions.

The user may want to know what types of rooms the hotel
offers, so the chatbot displays the names of the three rooms ( _Standard_ , _Deluxe_ ,
_Presidential_ ) and the corresponding pictures. In addition, you can request more
details about a particular accommodation.

When the user is ready, a room reservation can be made.
room; as described above, the chatbot requests the information
necessary information, responding in a consistent manner, both when the
correctly passed the validation phase and when errors occur.

When the chatbot requests the number of adults and children, if an
an incorrect number (negative quantity or outside the allowed limit)
a message is returned with the corresponding error, resuming the form.

The user may also choose to abort the booking, however, before
can actually interact with the chatbot again, he must confirm
his decision or continue with the form.

Finally, if the check-in and check-out dates are incorrect, inconsistent or refer
to the past, the chatbot communicates the error and asks for this information again.

## 6. Conclusions and future developments

The project made it possible to investigate various aspects related to virtual assistants
virtual assistants, based on the RASA framework, especially in the area of customer
service. This type of solutions, in the future, could represent an
additional possibility to improve the customer experience and, as a consequence, an
consequently, there will be an increasing need for maintenance related to it.
related to it.

With regard to possible future developments related to a chatbot of this
type, improvements could be made in various aspects. Being
fundamental for data management, the database should be designed
in a more efficient manner, for instance through the use of indexes, especially
from an enterprise perspective. In fact, such a system could be scaled up
easily, by including several databases belonging to different
hotels. In addition, information on customers could also be stored
customers, for analytics purposes, and in order to avoid inconsistencies, e.g. by
providing unique codes to each user. Concerning the booking of rooms
since in reality the capacity is often not fixed, a more dynamic approach to room
consider a more dynamic approach on room limits, for instance by
a maximum and minimum number of adults/children for each room.
each of them. Still on the subject of database functionality, one might
also consider making the management of attraction information persistent, by inserting appropriate
attractions, by inserting appropriate tables in the DB (images, descriptions, links),
descriptions, links). Given that during the initial phase the
generalities of the customer, a login mechanism could be implemented to authenticate the
able to authenticate the user, starting from credentials linked to a social or e-mail account.
social or e-mail account.

Finally, as a further improvement to the chatbot, it could be modified
the training data so as to ensure more human-like behaviour and
even distinguish different scenarios for different customers.

#### _Disclaimer: in-text images refer to 'Relazione_RasaChatBot.pdf' file_
