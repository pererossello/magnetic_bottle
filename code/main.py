import numpy as np
import copy
import numba


@numba.njit
def B_acc(pos, vel, q_o_m, B):
    acc = q_o_m * np.cross(vel, B)
    return acc

class Body:
    def __init__(self, mass, charge, position, velocity, dtype=np.float64):

        if isinstance(position, (list, tuple)) or isinstance(velocity, (list, tuple)):
            position = np.array(position)
            velocity = np.array(velocity)

        if not (position.shape == (3,) and velocity.shape == (3,)):
            raise ValueError("Position and velocity must be three-dimensional.")

        self.mass = dtype(mass)
        self.charge = dtype(charge)
        self.q_o_m = self.charge / self.mass
        self.position = position.astype(dtype)
        self.velocity = velocity.astype(dtype)


class Simulation:
    def __init__(self, bodies, B_field):

        self.sim_run = False  # True if simulation has been run
        body_list = copy.deepcopy(bodies)
        
        self.bodies = body_list
        self.num_bodies = len(body_list)
        self.q_o_ms = np.array([body.q_o_m for body in body_list])
        self.B_field = B_field

        self.compute_pos = [True for _ in range(self.num_bodies)]


    def update_positions_and_velocities(self, dt):

        """
        integration using RK$ method
        """

        for i, body in enumerate(self.bodies):

            B1 = self.B_field(body.position)
            k1_pos = dt * body.velocity
            k1_vel = dt * B_acc(body.position, body.velocity, body.q_o_m, B1)

            k2_pos = dt * (body.velocity + 0.5 * k1_vel)
            B2 = self.B_field(body.position + 0.5 * k1_pos)
            k2_vel = dt * B_acc(body.position + 0.5 * k1_pos, body.velocity + 0.5 * k1_vel, body.q_o_m, B2)

            k3_pos = dt * (body.velocity + 0.5 * k2_vel)
            B3 = self.B_field(body.position + 0.5 * k2_pos)
            k3_vel = dt * B_acc(body.position + 0.5 * k2_pos, body.velocity + 0.5 * k2_vel, body.q_o_m, B3)

            k4_pos = dt * (body.velocity + k3_vel)
            B4 = self.B_field(body.position + k3_pos)
            k4_vel = dt * B_acc(body.position + k3_pos, body.velocity + k3_vel, body.q_o_m, B4)

            body.position = body.position + (k1_pos + 2 * k2_pos + 2 * k3_pos + k4_pos) / 6
            body.velocity = body.velocity + (k1_vel + 2 * k2_vel + 2 * k3_vel + k4_vel) / 6


    def run_simulation(self, duration, time_step, lim=None):

        num_steps = int(duration / time_step)
        num_bodies = len(self.bodies)
        pos_arr = np.zeros((num_steps, 3, num_bodies)) * np.nan
        vel_arr = np.zeros((num_steps, 3, num_bodies)) * np.nan

        for step in range(num_steps):
            self.step = step
            for i, body in enumerate(self.bodies):

                compute = self.compute_pos[i]

                if not compute:
                    continue

                pos_arr[step, :, i] = body.position
                vel_arr[step, :, i] = body.velocity

                if lim is not None:
                    if np.linalg.norm(body.position) > lim:
                        self.compute_pos[i] = False

            perc = step/num_steps * 100
            print(f'\r{perc:.2f}%', end='')

            self.update_positions_and_velocities(time_step)


        self.positions = pos_arr
        self.velocities = vel_arr
        self.sim_run = True
        self.num_steps = num_steps