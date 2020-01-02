import glob
import os
import shutil
import time


class Mui():
    def __init__(self):
        self.files = [f for f in glob.glob('*')]
        self.file_extensions = {os.path.splitext(val)[1] for val in self.files}
        self.errors = []
        self.menu_state = False  # Default menu state for user.

    def record_error(self, msg):
        self.errors.append(msg)

    def draw_error(self):
        """
        Output error count if any. Otherwise prompt no errors found.
        """
        if len(self.errors) > 0:
            print(f'Error Count: {len(self.errors)}')
        else:
            print("Wow! No errors, isn't that great?")

    def draw_files_in_dir(self):
        """
        Output all files in current working directory/path to screen.
        """
        print(f'''\n { os.getcwd() } | (Folder Contents):
         ''')
        for file in self.files:
            """
            Formatting to differentiate files from folders.
            """
            if os.path.isfile(file):
                print(f'''  • {file}   ''')  # File
            elif os.path.isdir(file):
                print(f'''  // {file}   ''')  # Folder

    def draw_confirmation(self):
        """
        Continuously prompt response from user.
        """
        print('_______________________')
        print(''' Enter "Menu" for Help ''')
        while True:
            self.user_choice = input(
                'Are you sure you want to organize this directory? [Y/N]: '
            ).strip().lower()
            print('\n')
            if self.user_choice.startswith('y'):
                self.create_directory_for_extension()  # Default organization method
                print(' Success!')
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
        Initialize main loop combining 'draw_files_in_dir' & 'draw_confirmation'.
        """
        self.draw_files_in_dir()
        self.draw_confirmation()

    def draw_help_menu(self):
        print("""Help Menu!
        Here is a list of commands:
        'Close', 'About', 'Options'""")
        while self.menu_state:
            self.user_choice = input().strip().lower()
            if 'close' in self.user_choice:  # Reset program loop
                os.system('cls' if os.name == 'nt' else 'clear')  # Return
                self.draw_main_loop()
                break
            elif 'about' in self.user_choice:
                pass
            elif 'options' in self.user_choice:
                pass

    def create_directory_for_extension(self):
        """
        Organize folder contents by file extensions.
        """
        for self.extension in self.file_extensions:
            if not self.extension:  # Prevent creation & copying of folders.
                pass
            else:
                self.make_folder()
                time.sleep(0.5)
                self.copy_file()
        self.user_choice = input(
            ' (Press [enter] key to close this window.) ')  # Prompt user for manual exit.
        if self.user_choice:
            exit()

    def make_folder(self):
        try:
            os.mkdir(self.extension)
        except OSError as e:
            self.record_error(e)
            print(
                f'Creation of the directory: {self.extension} failed. {e}')
        else:
            print(f'Successfully created the directory: {self.extension}')

    def copy_file(self):
        """
        Move all files into matching directories created from 'make_folder'.
        """
        for file in self.files:
            if self.extension in file:
                try:
                    shutil.move(file, self.extension)
                except shutil.Error as e:
                    self.record_error(e)
                    print(f'Error: {e}')
                except IOError as e:
                    self.record_error(e)
                    print(f'Error: {e.strerror}')
                else:
                    print('Files moved.')


if __name__ == '__main__':
    """
    Initialize command-line interface
    """
    m = Mui()
    m.draw_main_loop()
    m.draw_error()
