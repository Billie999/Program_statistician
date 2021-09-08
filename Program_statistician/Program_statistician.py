import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl


#########################################
# Simonovikj Biljana                    #
# Advanced analysis                     #
# 23/02/2020                            #
#########################################
def main():
    """
    The main function controls and calls other functions of the program.
    First step checks if the user entered correct input and if he uploaded the dataset.
    Second step asks the user to upload the dataset from the csv file into a dataframe.
    Third step performs statistical analysis of the variables and displays the results on the screen by user input.
    Fourth step displays  two user-menus to choose the graph options and  plot-type and created graphs by user input.
    Fifth step finishes the program.
    """
    menu_range = 4
    menu_type = 'MAIN MENU'
    data = None
    menu_selection = None
    while menu_selection != 4:
        display_menu()
        menu_selection = int(input_and_validate(menu_type, menu_range))
        if menu_selection not in (1, 4) and data is None:
            print_menu_error(data)
        elif menu_selection == 1:
            data = load_data()
        elif menu_selection == 2:
            analyse_data(data)
        elif menu_selection == 3:
            visualise_data(data)
    print("\nGoodbye!")


def print_menu_error(data):
    """
    Displays an error message if the file has not be uploaded.
    It is activated on each step of the program.
    """
    print("\n<<ERROR>> Dataset [{}] is empty.".format(data))
    print("_______________________________________________")
    print("Please load data from a CSV file (Menu Option 1)!")
    print("_______________________________________________")


def display_menu():
    """
    Displays the user-menu to the screen.
    """
    print(" _______________________________________________")
    print(" Welcome to the DataFrame Statistician!")
    print(" _______________________________________________")
    print(" Please choose from the following options:\t\t ")
    print(" \t1 - Load from a CSV file\t\t ")
    print(" \t2 - Analyse\t\t ")
    print(" \t3 - Visualize\t\t ")
    print(" \t4 - Quit\t\t ")
    print(" _______________________________________________")


def input_and_validate(menu_type, menu_range):
    """
    Re-usable function to get user input, accepting only numbers in a range that has been passed in.
    Displays errors if any key other then the required numbers are entered. It has double error exception if the user
    keeps entering invalid numbers or characters, back and forth.
    """
    menu_input = ''
    valid_input = False
    while not valid_input:
        try:
            menu_input = int(input(f'Input your {menu_type} selection number: >> '))
            print('')
            valid_input = True
        except:
            print("\n<<ERROR>> Non-numeric character has been entered.")
        else:
            while menu_input not in range(1, menu_range + 1):
                try:
                    print(f'\n<<ERROR>>: Number [{menu_input}] is not a valid option. '
                          f'\n- Please type-in a valid menu selection, numbers (1 to {menu_range})! \n')
                    menu_input = int(input(f'Input your {menu_type} selection number: >> '))
                    print('')
                    valid_input = True
                except (RuntimeError, TypeError, ValueError, NameError, OSError) as err:
                    print('<< Run-time error description: {} >>.\n'.format(err))
                    valid_input = False
                    break
    return menu_input


def load_data():
    """
    Loads data into a dataframe from a csv file and validates if the file is empty,
    incorrectly typed or not existent at all. It removes extra commas or empty columns.
    """

    print(" _______________________________________________")
    print("   Load from a CSV file! \t\t\t")
    print(" _______________________________________________")
    get_filename = input("Input the filename: ")
    try:
        data = pd.read_csv(get_filename)
        if data.empty:
            print("\n<<ERROR>> File [{}] is empty.\n".format(get_filename))
        else:
            data = pd.read_csv(get_filename)
            print("\n_______________________________________________")
            print("File [{}] has been successfully loaded.".format(get_filename))
            print("_______________________________________________\n")
        return data
    except (RuntimeError, TypeError, ValueError, NameError, OSError) as err:
        print('<<ERROR>> cannot open file: [{}].'.format(get_filename))
        print('<< Run-time error description: {} >>.\n'.format(err))


def select_from_submenu(data):
    """
    Displays each variable and an index of the dataframe as part of the the menu content.
    Calls a function to prompt the user and validates the input.
    """
    columns = data.columns
    for index, col in zip(range(1, len(columns) + 1), columns):
        print(f'{index} - {col}')
    menu_type = 'METRIC'
    menu_range = len(data.columns)
    metric_selection = input_and_validate(menu_type, menu_range)
    return metric_selection


def analyse_data(data):
    """
    Performs analysis of variables (metrics) in the dataframe.
    Instead of return calculated variables calls another function (display_stat_report()).
    """
    print("\nWhich Metric do you want to analyse?")
    metric_choice = select_from_submenu(data)
    metric_choice = metric_choice - 1
    values = data.iloc[:, metric_choice]
    names = data.columns[metric_choice]
    count = len(values)
    mean = round(values.mean(), 2)
    standard_dev = round(values.std(), 2)
    standard_error = round(values.sem(), 2)
    display_stat_report(names, count, mean, standard_dev, standard_error)


def display_stat_report(names, count, mean, standard_dev, standard_error):
    """
    Displays statistical analysis of variables (metrics) in the dataframe.
    """
    print('')
    print(names.capitalize())
    print("-" * len(names))
    print(f'Number of values(n): {count}'.center(40, " "))
    print(f'Mean: {mean}'.center(40, " "))
    print(f'Standard Deviation: {standard_dev}'.center(40, " "))
    print(f'Std.Err of Mean: {standard_error}'.center(40, " "))
    print(("-" * 20).center(40, " "))


def visualise_data(data):
    """
    Displays  two user-menus to choose the graph options and  plot-type options .
    Calls a function to prompt the user and validates the input.
    Instead of return user prompts, calls another function (create_plots()).
    """
    vis_menu_range = 3
    menu_type = 'GRAPH'
    plot_menu_range = 2
    submenu_type = 'PLOT'
    print("DATA VISUALIZATION".center(40, ' '))
    print("--------------------".center(40, ' '))
    vis_ser = pd.Series(['line', 'bar', 'box'], index=[1, 2, 3])
    vis_choice = display_vis_choices(vis_ser, menu_type, vis_menu_range)
    vis_name = vis_ser[vis_choice]
    print("Set to Plot:", vis_name.capitalize())
    print("_______________________________________________")
    plot_ser = pd.Series(['Single plot',
                          'Subplots'],
                         index=[1, 2])
    plot_type_choice = display_vis_choices(plot_ser, submenu_type, plot_menu_range)

    create_plots(data, vis_choice, plot_type_choice, vis_name, vis_ser)


def display_vis_choices(visplot_ser, menu_type, menu_range):
    """
    General function for creating two menu options for graph selection one at a time.
    Calls a function to prompt the user and validates the input.
    """
    print(f'Choose from the following {menu_type} options: ')
    for index, value in visplot_ser.items():
        print('\t', index, '-', value.capitalize())
    input_choice = input_and_validate(menu_type, menu_range)

    return input_choice


def create_plots(data, vis_choice, plot_type_choice, vis_name, vis_ser):
    """
    Creates and shows plot and subplots according to user input.
    """
    if plot_type_choice == 1:
        data.plot(kind=vis_ser[vis_choice], subplots=False, layout=(1, len(data.columns)),
                  title=f'\n {vis_name.capitalize()} Plot for DataFrame\n', fontsize=10,
                  colormap='gist_rainbow')
    elif plot_type_choice == 2:
        data.plot(kind=vis_ser[vis_choice], subplots=True, layout=(1, len(data.columns)),
                  title=f'\n {vis_name.capitalize()} Plots for DataFrame\n', fontsize=10,
                  colormap='gist_rainbow')
    plt.show()


main()
