#------------------------------------------#
# Title: CDInventory.py
# Desc: Working with classes and functions.
# Change Log: (DTsakalos, 2021-Feb-28, Added code for error handling and writing/reading binary to file)
# DBiesinger, 2030-Jan-01, Created File
#------------------------------------------#

import pickle

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of dicts to hold data
dicRow = {}  # dict of data row
strFileName = 'CDInventory.dat'  # data storage file
objFile = None  # file object

# -- PROCESSING -- #
class DataProcessor:
    """Processing the data within memory"""

    @staticmethod
    def append_data(intID, strTitle, strArtist, table):
        """Function to manage data addition within program memory

        Strips the data the user inputs and then appends them into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table

        Args:
            intID (integer): contains that ID number of CD
            strTitle (string): Contains the Title of song name
            strArtist (string): Contains the name of the Artist
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """

        dicRow = {'ID': intID, 'Title': strTitle, 'Artist': strArtist}
        table.append(dicRow)


    @staticmethod
    def delete_data(id_to_remove, table):
        """ Function to manage data deletion within program memory

        Asks user for an ID number and checks to find the appropriate listing in a
        (list of dicts) table and removes the row (dict) that holds that ID number

        Args:
            id_to_remove (integer): the id  the user wants the containing dictionairy to be removed
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            blnCDRemoved (boolean): Checks if CD is removed
        """

        intRowNr = -1
        blnCDRemoved = False
        for row in table:
            intRowNr += 1
            if row['ID'] == id_to_remove:
                del table[intRowNr]
                blnCDRemoved = True
                break # Cannot remove more than one entry. When we have the same ID numbers only first is removed
        return blnCDRemoved

class FileProcessor:
    """Processing the data to and from dat file"""

    @staticmethod
    def read_file(file_name, tablex):
        """Function to manage data ingestion from file to a list of dictionaries

        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to read the data from
            tablex (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        tablex.clear()  # this clears existing data and allows to load data from file
        table = []
        while True:
            try:
                with open(file_name, 'rb') as objFile:
                    table = pickle.load(objFile)
                    break
            except FileNotFoundError:
                with open(file_name, 'wb') as objFile:
                    pickle.dump(table, objFile)
                    print('No previous file found. Created an empty file!')

        for row in table:
            tablex.append(row)


    @staticmethod
    def write_file(file_name, table):
        """Function to save data from a list of dictionaries to file in csv formating

        Saves the data from a 2D table in memory in current program 
        (list if dicts) and saves it to file, with each file line representing a row 
        of the 2D table, and each comma within a row separating the columns

        Args:
            file_name, (string): name of file used to save the data to
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """

        with open(file_name, 'wb') as objFile:
            pickle.dump(table, objFile)


# -- PRESENTATION (Input/Output) -- #
class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('\n------------Menu------------')
        print('[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case string of the users input out of the choices l, a, i, d, s or x
        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table

        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.
        """
        print('\n======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')

    @staticmethod
    def load_choice():
        """Gets user input after selecting load on main menu

        Warns the user unsaved data will be lost if they type yes and runs FileProcessor.read_file

        Args:
            None.

        Returns:
            load_file (Boolean): checks if user wants to load file
        """

        load_file = False
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled: ')
        if strYesNo.lower() == 'yes':
            print('reloading...')
            load_file = True
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
        return load_file


    @staticmethod
    def get_new_cd_data():
        """Gets user input after selecting load on main menu

        Warns the user unsaved data will be lost if they type yes and runs FileProcessor.read_file

        Args:
            None.

        Returns:
            intID (integer): contains that ID number of CD
            strTitle (string): Contains the Title of song name
            strArtist (string): Contains the name of the Artist
        """
            # 3.3.1 Ask user for new ID, CD Title and Artist
        while True:
            try:
                intID = int(input('Enter an ID: ').strip())
                break
            except ValueError: #making sure the program does not crash with string as input
                print('Invalid Input! Try again.')
        while True:
            try:
                strTitle = input('What is the CD\'s title? ').strip()
                if strTitle == '':
                    raise ValueError()
                break
            except ValueError: #making sure the program does not contain empty string
                print('Invalid Input! Try again.')
        while True:
            try:
                strArtist = input('What is the Artist\'s name? ').strip()
                if strArtist == '':
                    raise ValueError()
                break
            except ValueError: #making sure the program does not contain empty string
                print('Invalid Input! Try again.')
        return intID, strTitle, strArtist


# 1. When program starts, read in the currently saved Inventory
FileProcessor.read_file(strFileName, lstTbl)

# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()

    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break

    # 3.2 process load inventory
    if strChoice == 'l':
        reload_file = IO.load_choice()

        if reload_file:
            FileProcessor.read_file(strFileName, lstTbl)
            IO.show_inventory(lstTbl)

    # 3.3 process add a CD
    elif strChoice == 'a':
        int_id, str_title, str_artist = IO.get_new_cd_data()
        DataProcessor.append_data(int_id, str_title, str_artist, lstTbl)
        IO.show_inventory(lstTbl)

    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)

    # 3.5 process delete a CD
    elif strChoice == 'd':

        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstTbl)
        # 3.5.1.2 ask user which ID to remove
        intIDDel = int(input('Which ID would you like to delete? ').strip())

        removed = DataProcessor.delete_data(intIDDel, lstTbl)

        if removed:
            print('The CD was removed\n')
        else:
            print('Could not find this CD!\n')

        IO.show_inventory(lstTbl)

    # 3.6 process save inventory to file
    elif strChoice == 's':
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        # 3.6.2 Process choice
        if strYesNo == 'y':
            FileProcessor.write_file(strFileName, lstTbl)
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')


    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be safe:
    else:
        print('General Error')




