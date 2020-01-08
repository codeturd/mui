from glob import glob
from os import path, mkdir, system, name
from shutil import move, make_archive, Error
from time import sleep
from datetime import date


class Mui():

    def __init__(self):
        self.script_path = (path.dirname(path.realpath(__file__)))
        self.files = [f for f in glob(self.script_path + '/*')]
        self.errors = {}
        self.menu_state = False  # Default menu state for user.

    def record_error(self, msg, source):
        self.errors[msg] = source

    def draw_user_input(self, prompt=None, enter_key=False):
        if enter_key:
            self.user_choice = input('(Press [Enter] key to proceed.)')
        else:
            self.user_choice = input(prompt + ': ').strip().lower()

    def draw_error(self):
        """
        Output error count if any. Otherwise prompt no errors found.
        """
        if len(self.errors):
            print(f'Error Count: {len(self.errors)}')
            for key, val in self.errors.items():
                print(f'{key} : {val}')
        else:
            print("Wow! No errors, isn't that great?")

    def draw_files_in_dir(self):
        """
        Output all files in current working directory/path to screen.
        """
        print(f"""\n { self.script_path } ⌂ Directory Contents:
         """)
        print("""   (NOTE! Under main directory: "•" = File and "○" = Folder.)
            """)
        for file in self.files:
            """
            Formatting to differentiate files from folders.
            """
            if path.isfile(file):
                print(f"""  • {file}   """)  # File
            elif path.isdir(file):
                print(f"""  ○ {file}   """)  # Folder

    def draw_confirmation(self):
        """
        Continuously prompt response from user.
        """
        print('_______________________')
        print(' Enter "Menu" for Help ')
        while True:
            self.draw_user_input(
                'Would you like to sort this directory into sub-folders? [Y/N]')
            if self.user_choice.startswith('y'):
                self.draw_user_input(enter_key=True)
                self.create_directory_for_extension()
                self.post_prompt()
                break
            elif self.user_choice.startswith('n'):
                print(' Good-bye!')
                quit()
            elif 'menu' in self.user_choice:
                self.menu_state = True
                self.draw_help_menu()
                break
            else:
                print(" Sorry, that's not an appropriate response. Try again.")

    def draw_main_loop(self):
        """
        Initialize main loop combining "draw_files_in_dir" & "draw_confirmation".
        """
        self.draw_files_in_dir()
        self.draw_confirmation()

    def draw_help_menu(self):
        print('''
            Help Menu.
    Here is a list of commands:
        "About", "Options"
            ''')
        while self.menu_state:
            print('("Close" to return.)')
            self.draw_user_input('>')
            if 'close' in self.user_choice:
                system('cls' if name == 'nt' else 'clear')
                self.draw_main_loop()
                break
            elif 'about' in self.user_choice:
                print("""
        Mui:
    A small tool to aid in file organization, written in Python 3. Default method of organizing is set to consolidate via file extension type.
    This means for each unique file extension type (e.g. .zip, .txt, .py, ect.) a folder will be created and appropriately matching files moved to said folder.
    Simple, automated, and designed to run flawlessly across platforms. (Python required of course!)
    """)
                continue
            elif 'options' in self.user_choice:
                print(' Enter "X" to confirm choice or [Enter] key to backout.')
                self.draw_user_input(
                    'Backup current directory? (WARNING: This could take a long time!)')
                if 'x' in self.user_choice:
                    self.optional_backup()
                    continue

    def optional_backup(self):
        backup_path, timestamp = path.join(
            self.script_path, 'backup'), str(date.today())
        archive = f'{backup_path}_{timestamp}'
        print('Working.')
        sleep(0.5)
        if not path.exists(backup_path):
            try:
                mkdir(backup_path)
            except OSError as e:
                self.record_error(e, backup_path)
                print(f'Creation of the directory: backup failed. {e}.')
            else:
                print('Successfully created the directory: backup.')
                sleep(0.5)
        else:
            print('Directory already exists.')
        try:
            make_archive(base_name=archive, format='zip',
                         root_dir=self.script_path)
        except Error as e:
            self.record_error(e, archive)
            print(f'Error: {e}')
        except Exception as e:
            self.record_error(e, archive)
            print(f'Error: {e}')
        else:
            print('Archive created.')
            sleep(0.5)
        try:
            move(archive + '.zip', backup_path + '/')
        except Error as e:
            self.record_error(e, archive + backup_path)
            print(f'Error: {e}')
        except Exception as e:
            self.record_error(e, archive + backup_path)
            print(f'Error: {e}')
        else:
            print('Done.')

    def create_directory_for_extension(self):
        """
        Organize folder contents by file extensions.
        """
        self.folders_created, self.files_copied = 0, 0
        self.file_extensions = {path.splitext(ext)[1] for ext in self.files}
        for self.extension in self.file_extensions:
            if self.extension:
                self.path_destination = path.join(
                    self.script_path, self.extension)  # Define destination for files
                self.make_folder()
                sleep(0.5)
                self.copy_file()

    def make_folder(self):
        if not path.exists(self.path_destination):
            try:
                mkdir(self.path_destination)
            except OSError as e:
                self.record_error(e, self.extension)
                print(
                    f'Creation of the directory: {self.extension} failed. {e}')
            else:
                print(f'Successfully created the directory: {self.extension}.')
                self.folders_created += 1
        else:
            print('Directory already exists.')

    def copy_file(self):
        """
        Move all files into matching directories created from 'make_folder'.
        """
        for file in self.files:
            if self.extension in file:
                try:
                    move(file, self.path_destination)
                except Error as e:
                    self.record_error(e, file)
                    print(f'Error: {e}')
                except IOError as e:
                    self.record_error(e, file)
                    print(f'Error: {e.strerror}')
                else:
                    print('Files moved.')
                    self.files_copied += 1

    def post_prompt(self):
        def count(x): return (x - len(self.errors))
        count(self.folders_created), count(self.files_copied)
        print(
            f' Task Complete. {self.folders_created} directories created and {self.files_copied} files moved.')
        self.draw_error()
        self.draw_user_input(enter_key=True)


if __name__ == '__main__':
    """
    Initialize command-line interface
    """
    m = Mui()
    m.draw_main_loop()
