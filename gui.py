import eel
from solver import TISE


eel.init('web')

@eel.expose
def run(params):
    try:
        x_min = float(params['x_min'])
        x_max = float(params['x_max'])
        n_point = int(params['n_points'])
        n_sol = int(params['n_solutions'])
        e_min = float(params['e_min'])
        e_max = float(params['e_max'])
        de = float(params['e_step'])
        const_b = float(params['B'])
        potential = int(params['variant'])
        tise = TISE(
            x_min=x_min,
            x_max=x_max,
            n_point=n_point, 
            n_sol=n_sol,
            e_min=e_min,
            e_max=e_max,
            de=de,
            const_b=const_b,
            potential=potential
        )
        out_number = tise.solve()
        if out_number != 0:
            eel.show_message(out_number)
            tise.plot_solutions()
        else:
            eel.show_message(out_number)
    except ValueError:
        eel.show_message(0)
    except IndexError:
        eel.show_message(-1)


eel.start('index.html')
