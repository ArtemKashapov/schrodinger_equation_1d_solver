# schrodinger_equation_1d_solver

The presented desktop application was made to solve 1d schrodinger eqation. It implements Numerov's algorithm (step by step description available in this paper: http://physics.unipune.ac.in/~phyed/23.1/23.1_computation.pdf) in solver.py.

The GUI is in the gui.py it uses eel package (all requirements in requirements.txt), html, css and javascript.

To run this application you need to:
1. install python (I use 3.9.x);
2. install all packages, e.g. use pip: pip install -r requirements.txt.
3. Tun gui.py

To build it into desktop executable app, you need to install pyInstaller and run:

python -m eel gui.py web --onefile --noconsol --i "Absolute location to icon.ico"
