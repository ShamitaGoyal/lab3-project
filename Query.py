import sqlite3
conn = sqlite3.connect('destinations.db')
cursor = conn.cursor()

class Query:
    def __init__(self):
        self.selected_item = None

    def byName(self):
        """
        Query to get all the first letters when clicked on the name button from db
        """
        cursor.execute('''
        SELECT DISTINCT SUBSTR(destination_name, 1, 1) AS first_char
        FROM destinations
        ORDER BY first_char
        ''')
        distinct_first_chars = cursor.fetchall()
        dest_char_list = [char[0] for char in distinct_first_chars]
        return dest_char_list

    def byMonth(self):
        """
        Query to get all months when clicked on the month button from db
        """
        cursor.execute('''
        SELECT month
        FROM months
        ORDER BY month_num
        ''')
        distinct_months = cursor.fetchall()
        month_list = [month[0] for month in distinct_months]
        return month_list

    def byRank(self):
        """
        Query to get all rank numbers when clicked on the rank button from db
        """
        cursor.execute('''
        SELECT DISTINCT ranking AS rank
        FROM destinations
        ORDER BY rank
        ''')
        distinct_ranks = cursor.fetchall()
        rank_list = [rank[0] for rank in distinct_ranks]
        return rank_list

    def destination_by_name(self, dest_char):
        """
        Query to get the destination by name from the db when selecting
        an option from the dialog window
        """
        cursor.execute('''
        SELECT DISTINCT destination_name AS dest_name
        FROM destinations
        WHERE SUBSTR(destination_name, 1, 1) = ?
        ''', (dest_char,))
        distinct_destinations = cursor.fetchall()
        destination_list = [destination[0] for destination in distinct_destinations]
        return destination_list

    def destination_by_month(self, mnth):
        """
        query to get the destination by month from the db when selecting
        an option from the dialog window
        """
        cursor.execute('''
        SELECT DISTINCT destination_name, ranking AS dest_name
        FROM destinations
        WHERE month = ?
        ORDER BY ranking
        ''', (mnth,))
        distinct_destinations = cursor.fetchall()
        destination_list = [f'{destination[1]}. {destination[0]}' for destination in distinct_destinations]
        return destination_list

    def destination_by_rank(self, rank):
        """
        query to get the destination by rank from the db when selecting
        an option from the dialog window
        """
        cursor.execute('''
        SELECT DISTINCT destination_name, month AS dest_name
        FROM destinations
        WHERE ranking = ?
        ORDER BY month_num
        ''', (rank,))
        distinct_destinations = cursor.fetchall()
        destination_list = [f'{destination[0]}: {destination[1]}' for destination in distinct_destinations]
        return destination_list

    def destination_description(self, selected_item , param):
        """
        - query for selected item when the user clicks on a choice in the listbox
        - gets summary and url details from the user selected item
        """
        self.param = param
        if self.param == 'Name':
            dest = selected_item
        elif self.param == 'Month':
            dest = selected_item.split('.')[1].strip()
        elif self.param == 'Rank':
            dest = selected_item.split(':')[0].strip()

        cursor.execute('''
          SELECT summary, url
          FROM destinations
          WHERE destination_name = ?
          AND url IS NOT NULL
          LIMIT 1
          ''', (dest,))

        destination_summary = cursor.fetchall()

        dest_summary = None
        dest_url = None
        for destination in destination_summary:
            dest_summary = destination[0]
            dest_url = destination[1]
            # print(dest_summary, dest_url)

        return dest_summary, dest_url

