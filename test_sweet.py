import unittest 
from sweet import filter_by_pullen_id, total_sugar_from_pollen, total_clients_of_pollen, total_sugar_per_day, bees_effectiveness

import pandas as pd


class SweetTestCase(unittest.TestCase):
    """Tests for 'sweet.py'."""

    def setUp(self):
        self.harvest = pd.DataFrame({ 'bee_id' : [1,1,2,2,2,4,4], 
                                      'day' : [1,2,3,4,1,4,1],
                                      'pollen_id' : [3,3,2,2,1,3,2],  
                                      'miligrams_harvested' : [1.2,2.7,3.3,3,5,2,1] })
        self.pollen_id = 3


    def test_is_data_frame(self):
        return isinstance(self.harvest, pd.DataFrame)


    def test_filter_by_pullen_id(self):
        '''check the shape and compare two vectors'''
        self.assertEqual( filter_by_pullen_id(self.harvest, self.pollen_id).shape, (3,4) )
        self.assertEqual( list(filter_by_pullen_id(self.harvest, self.pollen_id).pollen_id), [3,3,3] )
        self.assertEqual( list(filter_by_pullen_id(self.harvest, self.pollen_id).miligrams_harvested), [1.2,2.7,2] )


    def test_total_sugar_from_pollen(self):
        self.assertEqual( total_sugar_from_pollen(self.harvest, self.pollen_id), 5.9)


    def test_total_clients_of_pollen(self):
        self.assertEqual( total_clients_of_pollen(self.harvest, self.pollen_id), 3 )


    def test_total_sugar_per_day(self):
        self.assertEqual( total_sugar_per_day(self.harvest), 
                          [[1, 7.2], [2, 2.7], [3, 3.3], [4, 5.0]] )


    def test_bees_effectiveness(self):
        effectiveness_table = pd.DataFrame(bees_effectiveness(self.harvest))
        self.assertEqual( effectiveness_table.shape, (3,4) )

#--------------------------------------------------
if __name__ == '__main__':
    unittest.main()
