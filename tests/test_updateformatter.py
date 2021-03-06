from unittest import TestCase

from tests.mockclasses import MockDatasource, MockUpdater, starting_data
from vaccinetracker.format_helpers import to_horizontal_table, to_vertical_table, coords_url

empty_table_h = "+------+-----+----------+------------------------+-----------------+---------+--------------+\n" \
                "| Name | Url | Distance | Open Appointment Slots | Open Time Slots | Address | Open In Maps |\n" \
                "+------+-----+----------+------------------------+-----------------+---------+--------------+\n" \
                "+------+-----+----------+------------------------+-----------------+---------+--------------+\n"

all_table_h = "+------------------+---------------+----------+------------------------+-----------------+---------------------------------------+----------------------------------------------------------+\n" \
              "|       Name       |      Url      | Distance | Open Appointment Slots | Open Time Slots |                Address                |                       Open In Maps                       |\n" \
              "+------------------+---------------+----------+------------------------+-----------------+---------------------------------------+----------------------------------------------------------+\n" \
              "|  Item One H-E-B  | www.item1.com |    10    |           0            |        0        |    111 Fake Street, Onett, TX 00001   | https://www.google.com/maps/search/0.1,+0.1/@0.1,0.1,17z |\n" \
              "|  Item Two H-E-B  | www.item2.com |    19    |           0            |        0        |   222 Fake Street, Twoson, TX 00002   | https://www.google.com/maps/search/0.2,+0.2/@0.2,0.2,17z |\n" \
              "| Item Three H-E-B | www.item3.com |    29    |           0            |        0        |   333 Fake Street, Threed, TX 00003   | https://www.google.com/maps/search/0.3,+0.3/@0.3,0.3,17z |\n" \
              "| Item Four H-E-B  | www.item4.com |    39    |           0            |        0        | 444 Fake Street, Foursquare, TX 00004 | https://www.google.com/maps/search/0.4,+0.4/@0.4,0.4,17z |\n" \
              "+------------------+---------------+----------+------------------------+-----------------+---------------------------------------+----------------------------------------------------------+\n"

onett_table_h = "+----------------+---------------+----------+------------------------+-----------------+----------------------------------+----------------------------------------------------------+\n" \
                "|      Name      |      Url      | Distance | Open Appointment Slots | Open Time Slots |             Address              |                       Open In Maps                       |\n" \
                "+----------------+---------------+----------+------------------------+-----------------+----------------------------------+----------------------------------------------------------+\n" \
                "| Item One H-E-B | www.item1.com |    10    |           0            |        0        | 111 Fake Street, Onett, TX 00001 | https://www.google.com/maps/search/0.1,+0.1/@0.1,0.1,17z |\n" \
                "+----------------+---------------+----------+------------------------+-----------------+----------------------------------+----------------------------------------------------------+\n"

empty_table_v = "+------------------------+\n" \
                "|         Store          |\n" \
                "+------------------------+\n" \
                "|          Url           |\n" \
                "|        Distance        |\n" \
                "| Open Appointment Slots |\n" \
                "|    Open Time Slots     |\n" \
                "|        Address         |\n" \
                "|      Open In Maps      |\n" \
                "+------------------------+\n"

all_table_v = "+------------------------+----------------------------------------------------------+----------------------------------------------------------+----------------------------------------------------------+----------------------------------------------------------+\n" \
              "|         Store          | Item One H-E-B                                           | Item Two H-E-B                                           | Item Three H-E-B                                         | Item Four H-E-B                                          |\n" \
              "+------------------------+----------------------------------------------------------+----------------------------------------------------------+----------------------------------------------------------+----------------------------------------------------------+\n" \
              "|          Url           | www.item1.com                                            | www.item2.com                                            | www.item3.com                                            | www.item4.com                                            |\n" \
              "|        Distance        | 10                                                       | 19                                                       | 29                                                       | 39                                                       |\n" \
              "| Open Appointment Slots | 0                                                        | 0                                                        | 0                                                        | 0                                                        |\n" \
              "|    Open Time Slots     | 0                                                        | 0                                                        | 0                                                        | 0                                                        |\n" \
              "|        Address         | 111 Fake Street, Onett, TX 00001                         | 222 Fake Street, Twoson, TX 00002                        | 333 Fake Street, Threed, TX 00003                        | 444 Fake Street, Foursquare, TX 00004                    |\n" \
              "|      Open In Maps      | https://www.google.com/maps/search/0.1,+0.1/@0.1,0.1,17z | https://www.google.com/maps/search/0.2,+0.2/@0.2,0.2,17z | https://www.google.com/maps/search/0.3,+0.3/@0.3,0.3,17z | https://www.google.com/maps/search/0.4,+0.4/@0.4,0.4,17z |\n" \
              "+------------------------+----------------------------------------------------------+----------------------------------------------------------+----------------------------------------------------------+----------------------------------------------------------+\n"

onett_table_v = "+------------------------+----------------------------------------------------------+\n" \
                "|         Store          | Item One H-E-B                                           |\n" \
                "+------------------------+----------------------------------------------------------+\n" \
                "|          Url           | www.item1.com                                            |\n" \
                "|        Distance        | 10                                                       |\n" \
                "| Open Appointment Slots | 0                                                        |\n" \
                "|    Open Time Slots     | 0                                                        |\n" \
                "|        Address         | 111 Fake Street, Onett, TX 00001                         |\n" \
                "|      Open In Maps      | https://www.google.com/maps/search/0.1,+0.1/@0.1,0.1,17z |\n" \
                "+------------------------+----------------------------------------------------------+\n"


class Test(TestCase):
    def test_to_horizontal_table(self):
        datasource = MockDatasource()
        updater = MockUpdater(datasource)

        # empty on create
        self.assertEqual(empty_table_h, str(to_horizontal_table(list(updater.new.values()), updater.origin)) + "\n")
        self.assertEqual(empty_table_h, str(to_horizontal_table(list(updater.all.values()), updater.origin)) + "\n")
        self.assertEqual(empty_table_h, str(to_horizontal_table(list(updater.matching.values()), updater.origin)) + "\n")

        datasource.data = starting_data
        updater.update()

        updater.max_dist = 10
        updater.min_qty = 0
        updater.update()

        self.assertEqual(onett_table_h, str(to_horizontal_table(list(updater.new.values()), updater.origin)) + "\n")
        self.assertEqual(all_table_h, str(to_horizontal_table(list(updater.all.values()), updater.origin)) + "\n")
        self.assertEqual(onett_table_h, str(to_horizontal_table(list(updater.matching.values()), updater.origin)) + "\n")

    def test_to_vertical_table(self):
        datasource = MockDatasource()
        updater = MockUpdater(datasource)

        # empty on create
        self.assertEqual(empty_table_v,
                         str(to_vertical_table(list(updater.new.values()), updater.origin)) + "\n")
        self.assertEqual(empty_table_v,
                         str(to_vertical_table(list(updater.all.values()), updater.origin)) + "\n")
        self.assertEqual(empty_table_v,
                         str(to_vertical_table(list(updater.matching.values()), updater.origin)) + "\n")

        datasource.data = starting_data
        updater.update()

        updater.max_dist = 10
        updater.min_qty = 0
        updater.update()

        self.assertEqual(onett_table_v,
                         str(to_vertical_table(list(updater.new.values()), updater.origin)) + "\n")
        self.assertEqual(all_table_v,
                         str(to_vertical_table(list(updater.all.values()), updater.origin)) + "\n")
        self.assertEqual(onett_table_v,
                         str(to_vertical_table(list(updater.matching.values()), updater.origin)) + "\n")

    def test_coords_url(self):
        coords = (30.274915353356107, -97.74033977282033)
        self.assertEqual(coords_url(coords),
                         "https://www.google.com/maps/search/30.274915353356107,+-97.74033977282033/"
                         "@30.274915353356107,-97.74033977282033,17z")