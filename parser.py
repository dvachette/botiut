import datetime
import requests
import os
import json


class Event:
    """Used for representing ics events folowing the modele here:
    {
    'DTSTAMP': '20241024T090202Z',
    'DTSTART': '20241023T060000Z',
    'DTEND': '20241023T080000Z',
    'SUMMARY': 'R1.03 Archi-CM',
    'LOCATION': 'Amphi2',
    'DESCRIPTION': '\\n\\nG1S1\\nG2S1\\nG3S1\\nG4S1\\nG5S1\\nMERRHEIM XAVIER\\n\\n(Exporté', 'le': '24/10/2024 11:02)\\n',
    'UID': 'ADE6070726f6a6574323032342d323032352d36393736312d302d35',
    'CREATED': '19700101T000000Z',
    'LAST-MODIFIED': '20241024T090202Z',
    'SEQUENCE': '2141479482'
    }"""

    def __init__(self, **kwargs):
        self._DTSTAMP = kwargs.get("DTSTAMP")
        self._DTSTART = kwargs.get("DTSTART")
        self._DTEND = kwargs.get("DTEND")
        self._SUMMARY = kwargs.get("SUMMARY")
        self._LOCATION = kwargs.get("LOCATION")
        self._DESCRIPTION = kwargs.get("DESCRIPTION")
        self._UID = kwargs.get("UID")
        self._CREATED = kwargs.get("CREATED")
        self._LAST_MODIFIED = kwargs.get("LAST-MODIFIED")
        self._SEQUENCE = kwargs.get("SEQUENCE")
        self._PROF = "DS" if "DS" in self._SUMMARY else self._DESCRIPTION.split(
            "\\n")[-4]
        # Convert date strings to datetime objects

        self._DTSTAMP = datetime.datetime.strptime(self._DTSTAMP,
                                                   "%Y%m%dT%H%M%SZ")
        self._DTSTART = datetime.datetime.strptime(self._DTSTART,
                                                   "%Y%m%dT%H%M%SZ")
        self._DTEND = datetime.datetime.strptime(self._DTEND, "%Y%m%dT%H%M%SZ")
        self._CREATED = datetime.datetime.strptime(self._CREATED,
                                                   "%Y%m%dT%H%M%SZ")
        self._LAST_MODIFIED = datetime.datetime.strptime(
            self._LAST_MODIFIED, "%Y%m%dT%H%M%SZ")

        self._DTSTART += datetime.timedelta(hours=1)
        self._DTEND += datetime.timedelta(hours=1)

    @property
    def start(self):
        return self._DTSTART

    @property
    def end(self):
        return self._DTEND

    @property
    def summary(self):
        return self._SUMMARY

    @property
    def location(self):
        return self._LOCATION

    @property
    def description(self):
        return self._DESCRIPTION

    @property
    def uid(self):
        return self._UID

    @property
    def created(self):
        return self._CREATED

    @property
    def last_modified(self):
        return self._LAST_MODIFIED

    @property
    def sequence(self):
        return self._SEQUENCE

    @property
    def prof(self):
        return self._PROF

    def __str__(self):
        return f"""{self.summary} ({self.start} - {self.end})
{self.prof}
{self.location}
"""

    def __repr__(self):
        return self.__str__()

    def __lt__(self, other):
        return self.start < other.start

    def __gt__(self, other):
        return self.start > other.start

    def __eq__(self, other):
        return self.start == other.start

    def __ne__(self, other):
        return self.start != other.start

    def __le__(self, other):
        return self.start <= other.start

    def __ge__(self, other):
        return self.start >= other.start

    def __hash__(self):
        return hash(self.uid)


def parse_ics(ics_file_path):
    events = []
    with open(ics_file_path, 'r') as file:
        event = {}
        inside_event = False
        for line in file:
            line = line.strip()

            if line == "BEGIN:VEVENT":
                event = {}
                inside_event = True
            elif line == "END:VEVENT":
                events.append(Event(**event))
                inside_event = False
            elif inside_event:
                key_value = line.split(":", 1)
                if len(key_value) == 2:
                    key, value = key_value
                    event[key] = value

    return events


# Exemple d'utilisation


def Calendar(group: str, date_start: str, date_end: str):
    """Get the calendar of a group from the start date to the end date
    
    In:
    - group (str): The group name
    - date_start (str): The start date of the calendar
    - date_end (str): The end date of the calendar
    
    Out:
    A list of Event objects
    
    """

    ics_file = "tmp/calendar.ics"
    if os.path.exists(ics_file):
        os.remove(ics_file)
        print("File removed")

    with open("groups.json", "r") as file:
        groups = json.load(file)

    url = f'https://adelb.univ-lyon1.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?resources={groups[group]}&projectId=0&calType=ical&firstDate={date_start}&lastDate={date_end}'

    with open("agent.txt", "r") as file:
        agent = file.read()

    headers = {'User-Agent': agent}
    response = requests.get(url, headers=headers)

    with open(ics_file, 'wb') as file:
        file.write(response.content)

    parsed_events = parse_ics(ics_file)

    parsed_events.sort()

    return parsed_events


def daily(group: str, date: str):
    cal = Calendar(group, date, date)
    message = _join_cal(cal=cal)
    return message


def today(group: str):
    date = datetime.datetime.now().strftime("YYYY-MM-DD")
    cal = Calendar(group, date, date)
    message = _join_cal(cal=cal)
    return message


def _join_cal(cal):
    if not len(cal):
        return "Rien ce jour là"
    else:
        return "\n\n".join([str(event) for event in cal])
