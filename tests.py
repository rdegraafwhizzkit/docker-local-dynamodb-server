import unittest
import boto3
from lib.floating_day import FloatingDayTable, DynamoDBTable
import datetime


class TestFloatingDayTable(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # https://docs.aws.amazon.com/boto3/latest/reference/services/dynamodb.html
        cls.client = boto3.Session(
            aws_access_key_id='aws_access_key_id',  # noqa is a dummy value
            aws_secret_access_key='aws_secret_access_key',  # dummy value
            region_name='eu-west-1'  # noqa is a dummy value but must be a valid AWS region
        ).client(
            'dynamodb',
            endpoint_url='http://localhost:8000'
        )

        cls.table_name = 'floating_day_zob'

        DynamoDBTable(cls.table_name, cls.client).delete_table()

        with FloatingDayTable(cls.table_name, cls.client) as floating_day:
            start = datetime.datetime(2026, 1, 1)
            end = datetime.datetime(2026, 12, 31)
            while start <= end:
                floating_day.put_item(
                    {
                        'yyyymmdd': {'N': start.strftime('%Y%m%d')},
                        'maximum': {'N': '10'}
                    },
                    ReturnConsumedCapacity='NONE'
                )
                start += datetime.timedelta(days=1)

    @classmethod
    def tearDownClass(cls):
        DynamoDBTable(cls.table_name, cls.client).delete_table()

    def test_fill_table(self):
        with FloatingDayTable(self.table_name, self.client) as floating_day:
            self.assertEqual(365, len(list(floating_day.get_days_info())))

    def test_001(self):
        with FloatingDayTable(self.table_name, self.client) as floating_day:
            floating_day.add_employee_ids_to_day(20260101, '0000001')
            days_for_employee_id = list(floating_day.get_days_for_employee_id('0000001'))
            self.assertEqual(1, len(days_for_employee_id))

    def test_002(self):
        with FloatingDayTable(self.table_name, self.client) as floating_day:
            floating_day.add_employee_ids_to_day(20260102, '0000001')
            days_for_employee_id = list(floating_day.get_days_for_employee_id('0000001'))
            self.assertEqual(2, len(days_for_employee_id))

    def test_003(self):
        with FloatingDayTable(self.table_name, self.client) as floating_day:
            floating_day.add_employee_ids_to_day(20260101, '0000002')
            day_info = list(floating_day.get_day_info(20260101))
            self.assertEqual(8, int(day_info[0]['available']['N']))
            self.assertEqual(20260101, int(day_info[0]['yyyymmdd']['N']))
            self.assertEqual(2, len(day_info[0]['employee_ids']['SS']))

    def test_004(self):
        with FloatingDayTable(self.table_name, self.client) as floating_day:
            floating_day.remove_employee_ids_from_day(20260101, ['0000000', '0000000'])
            day_info = list(floating_day.get_day_info(20260101))
            self.assertEqual(2, len(day_info[0]['employee_ids']['SS']))

    def test_005(self):
        with FloatingDayTable(self.table_name, self.client) as floating_day:
            floating_day.remove_employee_ids_from_day(20260101, '0000001')
            day_info = list(floating_day.get_day_info(20260101))
            self.assertEqual(9, int(day_info[0]['available']['N']))
            self.assertEqual(20260101, int(day_info[0]['yyyymmdd']['N']))
            self.assertEqual('0000002', day_info[0]['employee_ids']['SS'][0])

    def test_006(self):
        with FloatingDayTable(self.table_name, self.client) as floating_day:
            days_info = list(floating_day.get_days_info(start_date=20260601, end_date=20260731))
            self.assertEqual(61, len(days_info))

    def test_007(self):
        with FloatingDayTable(self.table_name, self.client) as floating_day, self.assertRaises(DynamoDBTable.Exception):
            floating_day.add_employee_ids_to_day(0, '0000000')


if __name__ == '__main__':
    unittest.main()
