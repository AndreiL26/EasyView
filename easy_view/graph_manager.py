"""
GraphManager
====
The GraphManager class that handles graphing and retrieving of data, through calls to the FHIR endpoint and Matplotlib
"""

import matplotlib.pyplot as plt
from typing import List
from fhir_parser import FHIR
from fhir_parser import Patient
import pdb
from math import floor
from datetime import datetime
import collections

class GraphManager:
    """Create a FHIR object to retrieve patient data """
    def __init__(self):
        self.FHIR = FHIR()

    def get_patients(self, page_number: int = 0) -> List[Patient]:
        if page_number == 0:
            return self.FHIR.get_all_patients()
        else:
            return self.FHIR.get_patient_page(page_number)

    def characteristic_is_observation_type(self, characteristic: str) -> bool:
        non_observation_types = ['language', 'marital status', 'city', 'country', 'state', 'family name', 'age']
        if non_observation_types.__contains__(characteristic):
            return False    
        return True

    def get_latest_obeservation_with_characteristic(self, patient: Patient, characteristic: str):
        observations = self.FHIR.get_patient_observations_page(patient.uuid, 3)
        latest_observation_value = 0
        latest_time = datetime(1,1,1)
        found_first_observation = False
        for observation in observations:
            for observation_component in observation.components:
                if observation_component.display == characteristic:
                    if found_first_observation == False:
                        found_first_observation = True
                        latest_time = observation.effective_datetime
                        latest_observation_value = observation_component.value
                    elif observation.effective_datetime > latest_time:
                        latest_time = observation.effective_datetime
                        latest_observation_value = observation_component.value
        return latest_observation_value

    def get_data(self, characteristic: str, page_number: int = 0):
        characteristic_values = {}
        patients = self.get_patients(page_number)
        if self.characteristic_is_observation_type(characteristic) == True:
            for patient in patients:
                data_point = self.get_latest_obeservation_with_characteristic(patient, characteristic)
                if str(data_point) in characteristic_values:
                    characteristic_values[str(data_point)] += 1
                else:
                    characteristic_values[str(data_point)] = 1
        else:
            for patient in patients:
                if characteristic == 'language':
                    for language in patient.communications.languages:
                        characteristic_values.update({language: characteristic_values.get(language, 0) + 1})
                if characteristic == 'marital status':
                    if str(patient.marital_status) in characteristic_values:
                        characteristic_values[str(patient.marital_status)] += 1
                    else:
                        characteristic_values[str(patient.marital_status)] = 1
                if characteristic == 'city':
                    if patient.addresses[0].city in characteristic_values:
                        characteristic_values[str(patient.addresses[0].city)] += 1
                    else:
                        characteristic_values[str(patient.addresses[0].city)] = 1
                if characteristic == 'country':
                    if patient.addresses[0].country in characteristic_values:
                        characteristic_values[str(patient.addresses[0].country)] += 1
                    else:
                        characteristic_values[str(patient.addresses[0].country)] = 1
                if characteristic == 'state':
                    if patient.addresses[0].state in characteristic_values:
                        characteristic_values[str(patient.addresses[0].state)] += 1
                    else:
                        characteristic_values[str(patient.addresses[0].state)] = 1
                if characteristic == 'family name':
                    if patient.name.family in characteristic_values:
                        characteristic_values[str(patient.name.family)] += 1
                    else:
                        characteristic_values[str(patient.name.family)] = 1
                if characteristic == 'age':
                    if floor(patient.age()) in characteristic_values:
                        characteristic_values[str(floor(patient.age()))] += 1
                    else:
                        characteristic_values[str(floor(patient.age()))] = 1
        return collections.OrderedDict(sorted(characteristic_values.items()))

    def graph_single_characteristic(self, characteristic: str, page_number: int = 0, graph_type: str = 'x_y_plot'):
        data = self.get_data(characteristic, page_number)
        plt.title('Values of the ' + str(characteristic) + ' in the first ' + str(page_number) + ' pages in the patients record')
        if graph_type == 'bar chart':
            plt.bar(range(len(data)), list(data.values()), align='center')
            plt.xticks(range(len(data)), list(data.keys()), rotation='vertical')
        elif graph_type == 'pie chart':
            plt.pie(data.values(), labels=data.keys(), autopct='%1.1f%%',
            shadow=True, startangle=90)
            plt.axis('equal')
        elif graph_type == 'x_y_plot':
            plt.plot(list(data.keys()), list(data.values()))
        

    def graph_multiple_characteristics(self, characteristics: List[str], page_number: int = 0, graph_type: str = 'x_y_plot'):
        for characteristic in characteristics:
            plt.figure()
            self.graph_single_characteristic(characteristic, page_number, graph_type)

    def show_figures(self):
        plt.show()
