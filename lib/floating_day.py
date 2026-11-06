from botocore.exceptions import ClientError

from lib import DynamoDBTable


class FloatingDayTable(DynamoDBTable):
    def __init__(self, table_name, client=None):
        """
        Class constructor

        :param table_name: DynamoDB table name
        :param client: Boto3 client
        """
        super().__init__(table_name, client)

    def get_item(self, yyyymmdd: int) -> dict | None:
        return self.client.get_item(
            TableName=self.table_name,
            Key={'yyyymmdd': {'N': str(yyyymmdd)}}
        ).get('Item', None)

    def update_item_attributes(self, item: dict) -> dict:
        employee_ids_count = len(item.get('employee_ids', {}).get('SS', []))
        if 0 == employee_ids_count:
            # Empty lists not allowed in DynamoDB
            item.pop('employee_ids', None)

        return item | {
            # Update the number of available spots
            'available': {'N': str(int(item['maximum']['N']) - employee_ids_count)},
        }

    def add_employee_ids_to_day(self, yyyymmdd: int, employee_ids: str | list, **kwargs):
        existing = self.get_item(yyyymmdd)
        if not existing:
            raise DynamoDBTable.Exception(f'Day {yyyymmdd} not found in table {self.table_name}')  # noqa

        ids = existing.get('employee_ids', {}).get('SS', [])
        ids.extend(employee_ids if isinstance(employee_ids, list) else [employee_ids])
        existing['employee_ids'] = {'SS': list(set(ids))}

        self.put_item(existing, **kwargs)

    def remove_employee_ids_from_day(self, yyyymmdd: int, employee_ids: str | list, **kwargs):
        """
        Remove employee id(s) from the employee_ids attribute

        :param yyyymmdd: A value like 20160413 for July 4th, 2020
        :param employee_ids: String or string list with employee id(s) to remove
        :param kwargs: Extra arguments to put_item
        :return: None
        """
        existing = self.get_item(yyyymmdd)
        if not existing:
            return

        for employee_id in employee_ids if isinstance(employee_ids, list) else [employee_ids]:
            try:
                existing.get('employee_ids', {}).get('SS', []).remove(employee_id)
            except ValueError:
                pass

        self.put_item(existing, **kwargs)

    def get_days_info(self, start_date: int = 0, end_date: int = 99991231):
        """
        Get all info for a specific date range

        :param start_date: a value like 20160413 for April 13th, 2016
        :param end_date: a value like 20200704 for July 4th, 2020
        :return: yield
        """
        assert start_date <= end_date

        for page in self.client.get_paginator('scan').paginate(
                TableName=self.table_name,
                FilterExpression='yyyymmdd between :start and :end',
                ExpressionAttributeValues={
                    ':start': {'N': str(start_date)},
                    ':end': {'N': str(end_date)},
                }
        ):
            yield from page['Items']

    def get_day_info(self, yyyymmdd: int):
        """
        Which employees have requested a snipperdag for requested day

        :param yyyymmdd: a value like 20261105 for November 5th, 2026
        :return: yield
        """
        # query works on the partition key, will return one partition key item, if any
        for page in self.client.get_paginator('query').paginate(
                TableName=self.table_name,
                KeyConditionExpression='yyyymmdd = :yyyymmdd',
                ExpressionAttributeValues={':yyyymmdd': {'N': str(yyyymmdd)}},
                ReturnConsumedCapacity='TOTAL'  # Be rich
        ):
            yield from page['Items']

    def get_days_for_employee_id(self, employee_id: str):
        """
        On which days does an employee has requested a snipperdag

        :param employee_id: an employee id, like '0027126'
        :return: yield
        """
        # scan works on the table, so it's more expensive
        for page in self.client.get_paginator('scan').paginate(
                TableName=self.table_name,
                ProjectionExpression='yyyymmdd',
                FilterExpression='contains(employee_ids,:employee_id)',
                ExpressionAttributeValues={':employee_id': {'S': str(employee_id)}},
                ReturnConsumedCapacity='NONE',  # Be lean
                PaginationConfig={'PageSize': 1}  # To test pagination
        ):
            yield from page['Items']

    def __enter__(self):
        """
        Enter the context manager

        :return: This object
        """
        try:
            self.create_table(
                [{'AttributeName': 'yyyymmdd', 'AttributeType': 'N'}],
                [{'AttributeName': 'yyyymmdd', 'KeyType': 'HASH'}]
            )
        except ClientError as ignored:
            pass

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the context manager

        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return: None
        """
        pass
