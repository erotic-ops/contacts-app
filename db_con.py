"""The database connection class for the contacts database"""

from datetime import date

import os
import mysql.connector

# Importing all environment variables
# Windows: FOR /F "eol=# tokens=*" %i IN (.env) DO SET %i
# Linux: export $(cat .env | xargs)

ENV = os.environ

# Check whether all the environment variable are loaded
if "HOST" in ENV:
    print("All ENVs are loaded")
    SECRET_KEY = ENV.get("SECRET_KEY")
else:
    print("ENVs are not loaded")
    exit()


class ConnectionClass:
    """
    This is the class for the contacts database
    """

    def __init__(self):
        self.__my_conn = mysql.connector.connect(
            host=ENV.get("HOST", "").strip(),
            user=ENV.get("USER", "").strip(),
            password=ENV.get("PASSWORD", "").strip(),
            port=int(ENV.get("PORT")),  # type: ignore
            database=ENV.get("DATABASE", "").strip(),
        )
        self.__my_curr = self.__my_conn.cursor()

    def check_the_connection(self) -> bool:
        """Returns True if the connection is established else False"""

        return True if self.__my_conn else False

    def user_login_with_user_email(self, email: str, password: str) -> list:
        """Returns the user data if the user exists in the database"""

        self.__my_curr.execute(
            'select id, name, email from login where email="{}" and password="{}"'.format(
                email, password
            )
        )
        return self.__my_curr.fetchone()  # type: ignore

    def check_whether_user_email_exists(self, email: str) -> bool:
        """Returns True if the email exists in the database else False"""

        self.__my_curr.execute('select id from login where email="{}"'.format(email))
        return True if self.__my_curr.fetchone() else False

    def user_signup_with_user_email(
        self, unique_id: str, name: str, email: str, password: str
    ) -> bool:
        """Function to signup the user with the email and password"""

        try:
            self.__my_curr.execute(
                'insert into login values ("{}", "{}", "{}", "{}")'.format(
                    unique_id, name, email, password
                )
            )
            self.__my_conn.commit()

            return True
        except mysql.connector.Error:
            return False

    def user_save_contact(self, unique_id: str, name: str, number: int) -> None:
        """
        Put name and number into the database
        """
        self.__my_curr.execute(
            'insert into contact (id, name, number, create_date) values ("{}", "{}", {}, "{}")'.format(
                unique_id, name, number, date.today()
            )
        )
        self.__my_conn.commit()

    def get_all_contacts_of_user(self, unique_id: str) -> list:
        """
        Get all the data from the database and return it

        Returns:
            list: The list of all the data
        """
        self.__my_curr.execute(
            'select name, number from contact where id="{}"'.format(unique_id)
        )
        return self.__my_curr.fetchall()

    def get_data_from_name(self, name: str) -> int:
        """
        Get the number from the database from the name

        Args:
            name (str): The name of the person

        Returns:
            int: The number of the person
        """
        self.__my_curr.execute(f'select number from contacts where name="{name}"')
        return self.__my_curr.fetchone()[0]  # type: ignore

    def delete_data_from_name(self, name: str) -> None:
        """
        Delete the data from the database from the name

        Args:
            name (str): The name of the person
        """
        self.__my_curr.execute(f'delete from contacts where name="{name}"')
        self.__my_conn.commit()

    def update_data(self, name: str, number: int) -> None:
        """
        Update the number from the database from the name

        Args:
            name (str): The name of the person
            number (int): The number of the person
        """
        self.__my_curr.execute(
            f'update contacts set number={number} where name="{name}"'
        )
        self.__my_conn.commit()

    def close_connection(self) -> None:
        """
        Close the connection
        """
        self.__my_conn.close()
