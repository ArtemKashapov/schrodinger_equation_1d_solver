# schrodinger_equation_1d_solver

The presented desktop application was made to solve 1d schrodinger eqation. It implements Numerov's algorithm (step by step description available in this paper: http://physics.unipune.ac.in/~phyed/23.1/23.1_computation.pdf) in solver.py.

The GUI is in the gui.py it uses eel package (all requirements in requirements.txt), html, css and javascript.

To run this application you need to:
1. install python (I use 3.9.x);
2. install all packages, e.g. use pip: pip install -r requirements.txt.
3. Run gui.py

To build it into desktop executable app, you need to install pyInstaller and run:

python -m eel gui.py web --onefile --noconsol --i "Absolute location to icon.ico"

Quick start guide:
1. Fill all fields like in the picture:
![image](https://user-images.githubusercontent.com/48184708/147402849-544cb7d5-b982-41f8-8a0f-a252c24ef637.png)
2. Press "Calculate" button.
3. You will get:
![image](https://user-images.githubusercontent.com/48184708/147402871-0c2ba2e8-8505-4203-8688-c09a833bfe09.png)
(analitical solutions for harmonic oscillator (F = x^2 / 2 in this case) are: E = 1.5, 3.5, 5.5, 7.5)
Enjoy it!
