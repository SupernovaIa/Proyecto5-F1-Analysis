# FastF1 Library and Visualization Tools
# -----------------------------------------------------------------------
import fastf1
import matplotlib.pyplot as plt
import seaborn as sns
import fastf1.plotting

# OS Library for System Interactions
# -----------------------------------------------------------------------
import os


def plot_drivers_pace(year, rnd, ev='R', save_file=False, number_of_drivers = 10):
    """
    Plots the lap time distribution of the top drivers in a race using violin and swarm plots.

    Parameters:
    - year (int): The year of the race.
    - rnd (int): The race round number.
    - ev (str, optional): The event type, such as 'R' for race. Defaults to 'R'.
    - save_file (bool, optional): Whether to save the plot as an image file. Defaults to False.
    - number_of_drivers (int, optional): Number of top drivers to include in the plot. Defaults to 10.
    """

    # Load FastF1's dark color scheme
    fastf1.plotting.setup_mpl(mpl_timedelta_support=False, misc_mpl_mods=False,
                            color_scheme='fastf1')

    # Load data session
    race = fastf1.get_session(year, rnd, ev)
    race.load()

    title = race.event.loc['EventName']

    # Point finishers by default
    point_finishers = race.drivers[:number_of_drivers]
    driver_laps = race.laps.pick_drivers(point_finishers).pick_quicklaps()
    driver_laps = driver_laps.reset_index()

    # To plot the drivers by finishing order, we need to get their three-letter abbreviations in the finishing order.
    finishing_order = [race.get_driver(i)["Abbreviation"] for i in point_finishers]

    # Create the figure
    fig, ax = plt.subplots(figsize=(10, 5))

    # Seaborn doesn't have proper timedelta support
    # So we have to convert timedelta to float (in seconds)
    driver_laps["LapTime(s)"] = driver_laps["LapTime"].dt.total_seconds()

    sns.violinplot(data=driver_laps,
                x="Driver",
                y="LapTime(s)",
                hue="Driver",
                inner=None,
                density_norm="area",
                order=finishing_order,
                palette=fastf1.plotting.get_driver_color_mapping(session=race)
                )

    sns.swarmplot(data=driver_laps,
                x="Driver",
                y="LapTime(s)",
                order=finishing_order,
                hue="Compound",
                palette=fastf1.plotting.get_compound_mapping(session=race),
                hue_order=["SOFT", "MEDIUM", "HARD"],
                linewidth=0,
                size=4,
                )

    ax.set_xlabel("Driver")
    ax.set_ylabel("Lap Time (s)")
    plt.suptitle(f"{year} {title} Lap Time Distributions")
    sns.despine(left=True, bottom=True)

    plt.tight_layout()
    plt.show()

    if save_file:
        folder = f'../imgs/{str(year)}/{str(rnd)}'

        # Create folder if does not exists
        if not os.path.exists(folder):
            os.makedirs(folder)

        # Save file
        name_file = f'driver_pace_{rnd}_{year}.png'
        complete_path = os.path.join(folder, name_file)
        plt.savefig(complete_path)

        print(f"Image saved in {complete_path}")


def plot_position_changes(year, rnd, ev='R', save_file=False):
    """
    Plots the position changes of drivers throughout a race.

    Parameters:
    - year (int): The year of the race.
    - rnd (int): The race round number.
    - ev (str, optional): The event type, such as 'R' for race. Defaults to 'R'.
    - save_file (bool, optional): Whether to save the plot as an image file. Defaults to False.
    """

    # Load FastF1's dark color scheme
    fastf1.plotting.setup_mpl(mpl_timedelta_support=False, misc_mpl_mods=False,
                            color_scheme='fastf1')

    session = fastf1.get_session(year, rnd, ev)
    session.load(telemetry=False, weather=False)

    title = session.event.loc['EventName']

    fig, ax = plt.subplots(figsize=(8.0, 4.9))

    for drv in session.drivers:
        drv_laps = session.laps.pick_drivers([drv])

        try:
            abb = drv_laps['Driver'].iloc[0]
            style = fastf1.plotting.get_driver_style(identifier=abb,
                                                    style=['color', 'linestyle'],
                                                    session=session)

            ax.plot(drv_laps['LapNumber'], drv_laps['Position'],
                    label=abb, **style)
            
        except IndexError:
            print('Driver not found. Probably DNS')
        
    ax.set_ylim([20.5, 0.5])
    ax.set_yticks([1, 5, 10, 15, 20])
    ax.set_xlabel('Lap')
    ax.set_ylabel('Position')
    ax.set_title(f'Position changes | {title}')

    ax.legend(bbox_to_anchor=(1.0, 1.02))
    plt.tight_layout()

    if save_file:
        folder = f'../imgs/{str(year)}/{str(rnd)}'

        # Create folder if does not exists
        if not os.path.exists(folder):
            os.makedirs(folder)

        # Save file
        name_file = f'position_changes_{rnd}_{year}.png'
        complete_path = os.path.join(folder, name_file)
        plt.savefig(complete_path)

        print(f"Image saved in {complete_path}")