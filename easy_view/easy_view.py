"""
EasyView
====
The primary component of the EasyView application with the EasyView class for handling all EasyView endpoint calls
"""

from graph_manager import GraphManager
from typing import List

class EasyView:
    """Create the EasyView endpoint to graph patient data"""
    def __init__(self):
        self.graph_manager = GraphManager()

    def graph_patient_page_multiple_characteristics(self, characteristics: List[str], page_number: int = 0, graph_type: str = 'x_y plot'):
        """
        Graphs multiple plots each with one characteristic of patients up to the specified page number
        If the page number is not specified, all patients data will be graphed 

        Args:
            characteristics: List of characteristics that are being graphed
        """
        self.graph_manager.graph_multiple_characteristics(characteristics, graph_type)
        self.graph_manager.show_figures()

    def graph_patient_page(self, characteristic: str, page_number: int = 0, graph_type: str = 'x_y plot'):
        """
        Graphs a characteristic of patients up to the specified page number 
        If the page_number is not specified, all patients data will be graphed

        Args:
            characteristic: Characteristic that is being graphed
            page_number:    Page number int
        """
        self.graph_manager.graph_single_characteristic(characteristic, page_number, graph_type)    
        self.graph_manager.show_figures()
