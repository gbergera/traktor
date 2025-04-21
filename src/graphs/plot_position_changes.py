import matplotlib.pyplot as plt
import fastf1
import fastf1.plotting
import f1requests.f1_requests as f1requests
import io

def plot_position_changes_graph(year, gp, session_type):
    fastf1.plotting.setup_mpl(mpl_timedelta_support=False, misc_mpl_mods=False, color_scheme='fastf1')

    session = f1requests.loadSession(year, gp, session_type)

    fig, ax = plt.subplots(figsize=(10, 6))

    for drv in session.drivers:
        drv_laps = session.laps.pick_drivers(drv)

        if drv_laps.empty:
            continue

        abb = drv_laps['Driver'].iloc[0]
        style = fastf1.plotting.get_driver_style(identifier=abb, style=['color', 'linestyle'], session=session)

        ax.plot(drv_laps['LapNumber'], drv_laps['Position'], label=abb, **style)

    ax.set_ylim([20.5, 0.5])
    ax.set_yticks([1, 5, 10, 15, 20])
    ax.set_xlabel('Lap')
    ax.set_ylabel('Position')
    ax.set_title(f"{session.event['EventName']} {session.event.year} - {session_type.upper()}")

    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight', dpi=300)
    plt.close()
    buffer.seek(0)
    return buffer
